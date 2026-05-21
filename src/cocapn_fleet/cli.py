"""CLI — Command-line interface for the Cocapn Fleet.

Provides commands for fleet management, agent spawning,
breeding cycles, and status inspection.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    # Fallback without rich/typer

from ..core.fleet import FleetCore, FleetConfig

app = typer.Typer(help="Cocapn Fleet — Unified Agent Ecosystem")
console = Console() if HAS_RICH else None


@app.command()
def welcome() -> None:
    """Display fleet welcome and status."""
    fleet = FleetCore()
    status = fleet.welcome()
    
    if console:
        data = json.loads(status)
        console.print(Panel.fit(
            f"[bold cyan]Cocapn Fleet[/bold cyan] v{data.get('version', '0.1.0')}\n"
            f"Fleet: {data.get('fleet', 'unknown')}\n"
            f"Agents: {data.get('agents', 0)}\n"
            f"Rooms: {', '.join(data.get('rooms', []))}\n"
            f"Subsystems: flux={data.get('subsystems', {}).get('flux', False)}, "
            f"breeding={data.get('subsystems', {}).get('breeding', False)}",
            title="🦀 Fleet Status",
            border_style="cyan"
        ))
    else:
        print(status)


@app.command()
def spawn(
    name: str = typer.Option(..., "--name", "-n", help="Agent name"),
    room: str = typer.Option("harbor", "--room", "-r", help="PLATO room"),
    dim: int = typer.Option(256, "--dim", "-d", help="DNA dimension"),
) -> None:
    """Spawn a new agent into the fleet."""
    fleet = FleetCore(FleetConfig(dim=dim))
    agent = fleet.spawn(name=name, room=room)
    
    if console:
        console.print(Panel.fit(
            f"[green]Agent spawned successfully[/green]\n"
            f"Name: {agent.name}\n"
            f"ID: {agent.agent_id}\n"
            f"Room: {agent.room}\n"
            f"Vector dim: {dim}",
            title="🆕 New Agent",
            border_style="green"
        ))
    else:
        print(f"Spawned agent {agent.name} (id={agent.agent_id}) in {room}")


@app.command()
def tick(
    generations: int = typer.Option(1, "--generations", "-g", help="Number of generations to run"),
) -> None:
    """Run breeding cycle(s)."""
    fleet = FleetCore()
    
    for i in range(generations):
        result = fleet.tick()
        
        if console:
            stats = result["stats"]
            console.print(f"[cyan]Generation {result['generation']}[/cyan]: "
                         f"agents={stats['total_agents']}, "
                         f"survivors={stats['survivors']}, "
                         f"breeders={stats['breeders']}, "
                         f"sunset={stats['sunset']}, "
                         f"children={stats['children']}")
        else:
            print(f"Gen {result['generation']}: {result['stats']}")


@app.command()
def status() -> None:
    """Show detailed fleet status."""
    fleet = FleetCore()
    
    if console:
        # DNA stats
        dna_stats = fleet.dna.stats()
        table = Table(title="Fleet DNA", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        for key, value in dna_stats.items():
            table.add_row(key, str(value))
        
        console.print(table)
        
        # Trinity thresholds
        from ..trinity.scorer import TrinityScore
        console.print(f"\n[yellow]Trinity Thresholds:[/yellow]")
        console.print(f"  Survive: {TrinityScore.SURVIVE_THRESHOLD}")
        console.print(f"  Breed: {TrinityScore.BREED_THRESHOLD}")
        
        # Room status
        room_table = Table(title="PLATO Rooms", box=box.ROUNDED)
        room_table.add_column("Room", style="cyan")
        room_table.add_column("Agents", style="white")
        room_table.add_column("Spells", style="green")
        
        for name, room in fleet.rooms.items():
            room_table.add_row(
                name,
                str(len(room.agents())),
                str(len(room.spells()))
            )
        
        console.print(room_table)
    else:
        print(f"Fleet: {fleet}")
        print(f"DNA: {fleet.dna.stats()}")


@app.command()
def demo() -> None:
    """Run an interactive fleet demo."""
    import time
    
    if console:
        console.print(Panel.fit(
            "[bold cyan]Cocapn Fleet Interactive Demo[/bold cyan]\n"
            "This demo spawns agents, runs a tournament, and shows results.",
            border_style="cyan"
        ))
    else:
        print("=== Cocapn Fleet Demo ===")
    
    fleet = FleetCore(FleetConfig(dim=128))
    
    # Spawn some agents
    if console:
        console.print("\n[dim]Spawning agents...[/dim]")
    else:
        print("Spawning agents...")
    
    for i in range(5):
        agent = fleet.spawn(name=f"scout-{i}", room="harbor")
        # Assign random fitness metadata
        import random
        agent.meta = {
            "hardware": {
                "thermal_pressure": random.random(),
                "memory_efficiency": random.random(),
                "gpu_utilization": random.random(),
                "power_efficiency": random.random(),
            },
            "human": {
                "task_completion_rate": random.random(),
                "avg_latency_ms": random.randint(100, 1000),
                "user_feedback": random.random(),
                "goal_achievement": random.random(),
            },
            "code": {
                "test_pass_rate": random.random(),
                "proof_coverage": random.random(),
                "cyclomatic_complexity": random.randint(5, 40),
                "documentation_score": random.random(),
                "type_coverage": random.random(),
            },
        }
        time.sleep(0.1)
    
    # Run a tick
    if console:
        console.print("\n[dim]Running breeding cycle...[/dim]")
    else:
        print("Running breeding cycle...")
    
    result = fleet.tick()
    
    # Show results
    if console:
        stats = result["stats"]
        console.print(Panel.fit(
            f"Generation {result['generation']} Complete\n"
            f"Active agents: {stats['total_agents']}\n"
            f"Survivors: {stats['survivors']}\n"
            f"Breeders: {stats['breeders']}\n"
            f"Sunset: {stats['sunset']}\n"
            f"Children: {stats['children']}",
            title="🎉 Demo Results",
            border_style="green"
        ))
    else:
        print(f"Demo complete: {result['stats']}")


@app.command()
def save(path: str = typer.Option("./fleet-state", "--path", "-p", help="Save directory")) -> None:
    """Save fleet state to disk."""
    fleet = FleetCore()
    saved = fleet.save(Path(path))
    
    if console:
        console.print(f"[green]Fleet saved to {saved}[/green]")
    else:
        print(f"Fleet saved to {saved}")


@app.command()
def load(path: str = typer.Option("./fleet-state", "--path", "-p", help="Load directory")) -> None:
    """Load fleet state from disk."""
    fleet = FleetCore.load(Path(path))
    
    if console:
        console.print(f"[green]Fleet loaded: {fleet}[/green]")
    else:
        print(f"Fleet loaded: {fleet}")


def main() -> None:
    """Entry point for the CLI."""
    app()
