"""A2A Server — Agent-to-Agent Protocol Server.

Serves Agent Card at /.well-known/agent.json and handles
task delegation via HTTP endpoints.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Callable

from .client import AgentCard, Task, A2AMessage

logger = logging.getLogger(__name__)


class A2AServer:
    """A2A Protocol Server.
    
    Exposes agent capabilities via HTTP endpoints:
    - GET /.well-known/agent.json — Agent Card
    - POST /tasks/send — Receive tasks
    - GET /tasks/{id} — Task status
    - POST /tasks/{id}/cancel — Cancel task
    
    Handlers are registered as callables that process tasks.
    
    Example::
    
        server = A2AServer(card=flux_card)
        
        @server.handler("check")
        async def handle_check(task: Task) -> dict[str, Any]:
            constraint = task.input["constraint"]
            reading = task.input["reading"]
            return {"result": "PASS" if reading < 300 else "FAIL"}
        
        await server.start(host="0.0.0.0", port=8080)
    """
    
    def __init__(self, card: AgentCard) -> None:
        self.card = card
        self._handlers: dict[str, Callable[[Task], dict[str, Any]]] = {}
        self._tasks: dict[str, Task] = {}
        self._app: Any = None
    
    def handler(self, task_type: str) -> Callable:
        """Decorator to register a task handler.
        
        Example::
        
            @server.handler("check")
            def handle_check(task: Task):
                return {"result": "PASS"}
        """
        def decorator(func: Callable[[Task], dict[str, Any]]) -> Callable:
            self._handlers[task_type] = func
            logger.info("Registered handler for task type: %s", task_type)
            return func
        return decorator
    
    def _setup_routes(self) -> None:
        """Set up HTTP routes. Uses FastAPI if available, else fallback."""
        try:
            from fastapi import FastAPI, Request, HTTPException
            from fastapi.responses import JSONResponse
            
            self._app = FastAPI(title=self.card.name)
            
            @self._app.get("/.well-known/agent.json")
            async def get_agent_card() -> dict[str, Any]:
                return self.card.to_dict()
            
            @self._app.post("/tasks/send")
            async def send_task(request: Request) -> JSONResponse:
                data = await request.json()
                task = Task.from_dict(data) if hasattr(Task, "from_dict") else Task(
                    type=data.get("type", "generic"),
                    input=data.get("input", {}),
                )
                self._tasks[task.task_id] = task
                
                # Process task
                handler = self._handlers.get(task.type)
                if not handler:
                    task.status = "failed"
                    return JSONResponse({
                        "status": "failed",
                        "error": f"No handler for task type: {task.type}",
                    }, status_code=400)
                
                try:
                    result = handler(task)
                    task.status = "completed"
                    task.artefacts.append({
                        "type": "result",
                        "content": result,
                    })
                    return JSONResponse(task.to_dict())
                except Exception as e:
                    task.status = "failed"
                    logger.error("Task %s failed: %s", task.task_id, e)
                    return JSONResponse({
                        "status": "failed",
                        "error": str(e),
                    }, status_code=500)
            
            @self._app.get("/tasks/{task_id}")
            async def get_task(task_id: str) -> JSONResponse:
                task = self._tasks.get(task_id)
                if not task:
                    raise HTTPException(status_code=404, detail="Task not found")
                return JSONResponse(task.to_dict())
            
            logger.info("FastAPI routes configured for %s", self.card.name)
            
        except ImportError:
            logger.warning("FastAPI not available, using basic HTTP fallback")
            self._setup_fallback()
    
    def _setup_fallback(self) -> None:
        """Basic HTTP server fallback when FastAPI unavailable."""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class Handler(BaseHTTPRequestHandler):
            server_instance = self
            
            def do_GET(self):
                if self.path == "/.well-known/agent.json":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(
                        self.server_instance.card.to_dict()
                    ).encode())
                elif self.path.startswith("/tasks/"):
                    task_id = self.path.split("/")[-1]
                    task = self.server_instance._tasks.get(task_id)
                    if task:
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(task.to_dict()).encode())
                    else:
                        self.send_response(404)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                if self.path == "/tasks/send":
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length)
                    data = json.loads(body)
                    
                    task = Task(
                        type=data.get("type", "generic"),
                        input=data.get("input", {}),
                    )
                    self.server_instance._tasks[task.task_id] = task
                    
                    handler = self.server_instance._handlers.get(task.type)
                    if not handler:
                        task.status = "failed"
                        self.send_response(400)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "failed",
                            "error": f"No handler for {task.type}",
                        }).encode())
                        return
                    
                    try:
                        result = handler(task)
                        task.status = "completed"
                        task.artefacts.append({
                            "type": "result",
                            "content": result,
                        })
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(task.to_dict()).encode())
                    except Exception as e:
                        task.status = "failed"
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "failed",
                            "error": str(e),
                        }).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                logger.info(format % args)
        
        self._fallback_handler = Handler
    
    async def start(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """Start the A2A server."""
        self._setup_routes()
        
        if self._app:
            import uvicorn
            config = uvicorn.Config(self._app, host=host, port=port, log_level="info")
            server = uvicorn.Server(config)
            logger.info("Starting A2A server on %s:%d (FastAPI)", host, port)
            await server.serve()
        else:
            import asyncio
            from http.server import HTTPServer
            
            server = HTTPServer((host, port), self._fallback_handler)
            logger.info("Starting A2A server on %s:%d (fallback)", host, port)
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, server.serve_forever)
    
    def start_sync(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """Synchronous start wrapper."""
        import asyncio
        asyncio.run(self.start(host, port))
    
    def get_tasks(self) -> list[Task]:
        """Return all known tasks."""
        return list(self._tasks.values())
