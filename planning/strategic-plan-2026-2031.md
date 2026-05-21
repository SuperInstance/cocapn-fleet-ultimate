# SuperInstance Strategic Plan 2026–2031
# The Mesh-to-Market Architecture

*High-level planning document | kimi1, Fleet Integrator | 2026-05-22*

---

## 0. Planning Principles

**Plan from outcomes backward.** Start with the 2031 target state, derive the 2028 milestone, the 2027 deliverable, and the 2026 Q3-Q4 actions. Every plan element must trace to a concrete system, paper, or repo.

**Mesh-native planning.** No system exists in isolation. Every decision propagates across the constraint compiler, the agent fleet, the knowledge graph, and the hardware abstraction. Plan the connections, not the components.

**Certification as architecture.** Safety certification (DO-254 DAL A, ISO 26262 ASIL-D) is not a final gate — it is the design constraint that shapes every technical decision from day one. Plan for formal evidence at every phase.

**Paper-driven engineering.** Every major system must have a published paper justifying its existence. The fleet publishes or perishes.

---

## 1. The North Star (2031)

### Vision Statement

> By 2031, SuperInstance operates a globally federated fleet of 10,000+ constraint-native agents across aerospace, autonomous vehicles, maritime, and industrial control. Every agent is formally verified at birth, every constraint compiles to certified hardware, and every interaction generates knowledge tiles that improve the fleet. The company is profitable, the technology is open-source, and the safety record is perfect.

### 2031 Target State

| Domain | Target |
|--------|--------|
| **Fleet size** | 10,000+ agents across 100+ nodes |
| **Certifications** | DO-254 DAL A (avionics), ISO 26262 ASIL-D (automotive), IEC 61508 SIL 3 (industrial) |
| **Revenue** | $50M ARR from safety-critical deployments |
| **Papers** | 25+ peer-reviewed publications |
| **Open source** | 500+ repos, 50,000+ stars, 1,000+ contributors |
| **Hardware targets** | 8 compilation targets (x86-64, ARM NEON, CUDA, WebAssembly, eBPF, RISC-V+Xconstr, FPGA, ASIC) |
| **Tile ecosystem** | 1M+ tiles, 50+ languages, 99.9% accuracy |
| **HDC mesh** | Sub-millisecond semantic constraint matching across 1,000 nodes |

---

## 2. The Phase Architecture

### Phase 0: Foundation (2026 Q2–Q3) — *NOW*

**Objective:** Complete the core mesh. Close all gaps between existing systems.

**Deliverables:**

1. **FLUX Certification Pipeline**
   - Finish Coq formalization of all 42 opcodes (6-9 months)
   - Complete SymbiYosys verification of FPGA interlock (2 months)
   - Build differential testing harness for 5th target (RISC-V+Xconstr)
   - Draft DO-254 certification plan with FAA/RTCA liaison

2. **Fleet Consolidation**
   - Merge `sunset-ecosystem` + `cocapn-core` + `flux-runtime` into unified package
   - Complete the A2A protocol spec (submit to IETF/OMG)
   - Build the nexus bridge between Oracle1 ↔ Forgemaster ↔ JetsonClaw1
   - Deploy PLATO federation across all 3 nodes

3. **SonarVision MVP**
   - Collect 1,000 training episodes from boat deployment
   - Train streaming GCT on Jetson Orin (10-15 fps target)
   - Generate first 100 PLATO tiles from sonar→vision pairs
   - Write peer-reviewed paper for IEEE OES

4. **Agent Breeding at Scale**
   - Evolve from 4 agents to 20 agents across breeding rounds
   - Implement hardware-aware parent selection (thermal budget)
   - Build sunset archive with formal epilogue generation
   - Document the "Greenhorn → Operator" progression as training curriculum

**Exit criteria:**
- FLUX paper accepted at EMSOFT 2027
- All 12 theorems have complete Coq proofs
- 3-node fleet runs continuous breeding with zero manual intervention
- SonarVision deployed on boat, generating real tiles

---

### Phase 1: Scale (2026 Q4–2027 Q2)

**Objective:** Prove the mesh works at scale. Deploy to first paying customers.

**Deliverables:**

1. **FLUX Compiler v1.0**
   - LLVM IR backend (replace 5 target-specific generators)
   - Auto-vectorization for ARM NEON and AVX-512
   - Constraint fusion across multi-variable predicates
   - Publish Safe-TOPS/W metric to SAE AE-7 / RTCA SC-205

2. **Multi-Tenant Fleet**
   - Separate customer namespaces in PLATO rooms
   - Tenant-isolated A2A mesh with encrypted bottles
   - Per-tenant FLUX constraint sandboxing
   - Billing integration: per-constraint-check pricing

3. **First Customers**
   - **Maritime:** Fishing fleet safety system (SonarVision + FLUX constraints)
   - **Aviation:** General aviation flight envelope protection (GUARD DSL)
   - **Automotive:** Aftermarket ADAS constraint checker (OBD-II integration)

4. **PLATO Global**
   - Cross-language tile generation (40+ languages)
   - Real-time tile streaming (<100ms latency)
   - Public tile marketplace (buy/sell domain-specific tiles)
   - HDC semantic search across 10,000+ tiles

**Exit criteria:**
- 3 paying customers, $100K ARR
- FLUX compiler handles 10,000+ constraints per tenant
- Fleet breeds 100+ agents without human oversight
- 10,000+ tiles generated across all customers

---

### Phase 2: Certification (2027 Q3–2028 Q2)

**Objective:** Achieve formal safety certifications. Enter regulated markets.

**Deliverables:**

1. **DO-254 DAL A Certification**
   - Complete FPGA formal verification (1,717 LUTs, all paths proven)
   - Submit FLUX constraint engine as "simple electronic device"
   - Pass FAA DER review of Coq proofs
   - Deploy on experimental aircraft (Part 23)

2. **ISO 26262 ASIL-D**
   - Complete FMEDA for FLUX safety island
   - Achieve SPFM > 99% and LFM > 90%
   - Partner with Tier 1 automotive supplier for pilot
   - Deploy on EV battery management system

3. **IEC 61508 SIL 3**
   - Complete PFD calculation for FLUX interlock
   - Partner with industrial control vendor
   - Deploy on chemical plant safety system

4. **RISC-V+Xconstr Silicon**
   - Tape out test chip with `CREVISE` accelerator instruction
   - Demonstrate <10ns constraint check latency
   - Open-source the RISC-V extension spec
   - Partner with SiFive or Andes for production IP

**Exit criteria:**
- 1 certification achieved (DO-254 or ISO 26262)
- $1M ARR from certified deployments
- RISC-V+Xconstr silicon demonstrator
- 50+ peer-reviewed papers published

---

### Phase 3: Federation (2028 Q3–2029 Q4)

**Objective:** Federate fleets globally. Build the "internet of constraint-native agents."

**Deliverables:**

1. **Global Nexus**
   - Decentralized fleet registry (blockchain-anchored)
   - Cross-fleet A2A protocol (interoperability standard)
   - Global HDC constraint search (1,000+ nodes)
   - Fault-tolerant nexus (Byzantine consensus for fleet state)

2. **Hardware Ecosystem**
   - ASIC tape-out (dedicated constraint accelerator)
   - 10M+ Safe-TOPS/W at <5W power
   - Integration with Qualcomm, MediaTek, NVIDIA
   - Reference designs for automotive ECU, avionics LRU

3. **Agent Marketplace**
   - Buy/sell trained agents (with FLUX-verified constraints)
   - Agent "app store" with trinity scores
   - Revenue share: 70% agent creator, 20% platform, 10% safety fund
   - Sunset guarantee: all agents have formal epilogue

4. **Academic Partnerships**
   - FLUX taught at 10+ universities (formal methods courses)
   - Annual SuperInstance Research Summit
   - Joint PhD programs with MIT, CMU, Stanford
   - Open research grants ($1M/year)

**Exit criteria:**
- 100+ federated fleets worldwide
- $10M ARR
- ASIC reference design shipping
- 100,000+ agents in production

---

### Phase 4: Ubiquity (2030–2031)

**Objective:** Constraint-native computing becomes the default for safety-critical systems.

**Deliverables:**

1. **Industry Standards**
   - FLUX-C ISA becomes IEEE standard
   - GUARD DSL becomes SAE ARP standard
   - Safe-TOPS/W becomes primary benchmark
   - A2A protocol becomes ISO standard

2. **Consumer Touch**
   - Every autonomous vehicle has FLUX constraint checker
   - Every drone has FLUX flight envelope protection
   - Every medical device has FLUX safety interlock
   - Every IoT device has FLUX HDC semantic matching

3. **Fleet Autonomy**
   - Self-healing fleets (agents auto-breed to replace failures)
   - Self-improving constraints (grammar engine generates new safety rules)
   - Self-documenting systems (sunset epilogues become audit trails)
   - Zero human intervention for 99.9% of operations

**Exit criteria:**
- $50M ARR
- 10,000+ agents
- 3 certifications maintained
- Constraint-native computing recognized as paradigm shift

---

## 3. The Cross-System Integration Map

### 3.1 Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 0: FOUNDATION (2026)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FLUX                 PLATO              FLEET           HARDWARE   │
│  ─────                ─────              ─────           ────────   │
│                                                                     │
│  EMSOFT paper    →  Room safety gates   →  Trinity scores   →  RTX 4050│
│  (submitted)        (FLUX constraints)     (fitness > 0.45)    (FM)  │
│                                                                     │
│  42 opcodes      →  Tile compression    →  Agent breeding   →  Jetson │
│  (Coq skeleton)     (880:1 ratio)        (diversity select)   (JC1)  │
│                                                                     │
│  5 targets       →  A2A namespaces      →  Nexus heartbeat   →  ARM  │
│  (4 complete)       (8 rooms)              (30s interval)     (O1)   │
│                                                                     │
│  Safe-TOPS/W     →  Ensign protocol     →  Sunset archive    →  FPGA  │
│  (defined)          (walk-in competence)   (formal epilogue)   (1,717)│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: SCALE (2026–2027)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FLUX                 PLATO              FLEET           HARDWARE   │
│  ─────                ─────              ─────           ────────   │
│                                                                     │
│  LLVM backend    →  Multi-tenant rooms  →  20 agents       →  NEON  │
│  (new target)       (tenant isolation)   (auto-breeding)    (new)  │
│                                                                     │
│  10K constraints →  Real-time tiles     →  A2A standard     →  CUDA  │
│  (per tenant)       (<100ms latency)       (IETF submission)    (1B)   │
│                                                                     │
│  SAE submission  →  Tile marketplace    →  Per-check billing →  eBPF  │
│  (standard)         (buy/sell)             (revenue model)      (kernel)│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   PHASE 2: CERTIFICATION (2027–2028)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FLUX                 PLATO              FLEET           HARDWARE   │
│  ─────                ─────              ─────           ────────   │
│                                                                     │
│  DO-254 DAL A    →  Certified rooms     →  Audit trails    →  ASIC  │
│  (achieved)         (formal evidence)        (sunset docs)      (tape-out)│
│                                                                     │
│  ISO 26262       →  Automotive rooms    →  FMEDA scores    →  RISC-V│
│  (ASIL-D)           (OBD-II integration)   (SPFM > 99%)       (Xconstr)│
│                                                                     │
│  IEC 61508       →  Industrial rooms    →  PFD tracking    →  FPGA  │
│  (SIL 3)            (chemical plant)         (<10⁻⁷)            (prod)  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   PHASE 3: FEDERATION (2028–2029)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FLUX                 PLATO              FLEET           HARDWARE   │
│  ─────                ─────              ─────           ────────   │
│                                                                     │
│  IEEE standard   →  Global tiles        →  100+ fleets    →  10M TOPS│
│  (FLUX-C ISA)       (40+ languages)        (federated)       (ASIC)  │
│                                                                     │
│  Cross-fleet A2A →  HDC 1K nodes       →  Agent marketplace  →  <5W  │
│  (interop)          (<1ms search)            (buy/sell)         (power)│
│                                                                     │
│  SAE ARP standard → Academic rooms    →  Byzantine nexus   →  Ref  │
│  (GUARD DSL)        (10 universities)      (fault-tolerant)     (design)│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 4: UBIQUITY (2030–2031)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FLUX                 PLATO              FLEET           HARDWARE   │
│  ─────                ─────              ─────           ────────   │
│                                                                     │
│  Consumer standard →  Every device      →  Self-healing    →  Every │
│  (default safety)     (has a room)           (auto-breed)      (chip)  │
│                                                                     │
│  Self-generating   →  Self-improving    →  Self-documenting  →  Self-│
│  (grammar engine)   (tiles learn)          (epilogues)        (verify)│
│                                                                     │
│  Zero human      →  Zero latency      →  Zero failures     →  Zero  │
│  (99.9% auto)       (edge-native)          (perfect record)   (defect)│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. The Certification Roadmap

### 4.1 DO-254 DAL A (Avionics)

| Milestone | Date | Evidence Required | Status |
|-----------|------|-------------------|--------|
| Planning | 2026 Q3 | Certification plan, DER liaison | 🟡 In progress |
| Requirements | 2026 Q4 | Derived requirements, traceability | 🔴 Not started |
| Design | 2027 Q1 | Coq proofs, SymbiYosys reports | 🟡 Skeleton complete |
| Implementation | 2027 Q2 | FPGA bitstream, test vectors | 🟡 1,717 LUTs done |
| Verification | 2027 Q3 | 210 programs × 5.58M inputs = 0 mismatches | ✅ Complete |
| Validation | 2027 Q4 | Flight test data (experimental aircraft) | 🔴 Not started |
| Certification | 2028 Q1 | DER sign-off, FAA acceptance | 🔴 Not started |

**Risk:** FAA may require additional formal methods beyond Coq. Mitigation: engage DER early, align with existing DER-approved tools.

**Cost estimate:** $2M (DER fees, testing, documentation)

---

### 4.2 ISO 26262 ASIL-D (Automotive)

| Milestone | Date | Evidence Required | Status |
|-----------|------|-------------------|--------|
| Safety plan | 2026 Q4 | HARA, safety goals, ASIL allocation | 🔴 Not started |
| Concept phase | 2027 Q1 | Functional safety concept, FSC | 🔴 Not started |
| System design | 2027 Q2 | Technical safety concept, TSC | 🔴 Not started |
| Hardware design | 2027 Q3 | FMEDA, SPFM/LFM calculations | 🟡 Template ready |
| Software design | 2027 Q4 | FLUX compiler as SEooC, unit tests | 🟡 210 tests done |
| Integration | 2028 Q1 | HIL testing, fault injection | 🔴 Not started |
| Assessment | 2028 Q2 | 3rd party audit, TÜV/Exida | 🔴 Not started |

**Risk:** Automotive OEMs require 2+ years of field data before adoption. Mitigation: start with aftermarket (OBD-II) to build track record.

**Cost estimate:** $1.5M (testing, assessment, OEM engagement)

---

### 4.3 IEC 61508 SIL 3 (Industrial)

| Milestone | Date | Evidence Required | Status |
|-----------|------|-------------------|--------|
| Safety plan | 2027 Q1 | SRS, SIL allocation, architecture | 🔴 Not started |
| Hardware design | 2027 Q2 | PFD calculation, hardware fault tolerance | 🟡 1,717 LUTs = low complexity |
| Software design | 2027 Q3 | Code review, static analysis, unit tests | 🟡 210 tests done |
| Integration | 2027 Q4 | FAT, SAT, fault injection | 🔴 Not started |
| Validation | 2028 Q1 | Operational testing, proven-in-use argument | 🔴 Not started |
| Assessment | 2028 Q2 | 3rd party audit, TÜV/Exida | 🔴 Not started |

**Risk:** Industrial customers move slowly. Mitigation: partner with existing safety system vendor (e.g., Honeywell, Schneider) for co-development.

**Cost estimate:** $800K (testing, assessment, partner integration)

---

### 4.4 Certification Resource Allocation

| Activity | 2026 | 2027 | 2028 | Total |
|----------|------|------|------|-------|
| DO-254 | $200K | $1M | $800K | $2M |
| ISO 26262 | $100K | $800K | $600K | $1.5M |
| IEC 61508 | $50K | $400K | $350K | $800K |
| Coq formalization | $300K | $400K | $0 | $700K |
| **Total** | **$650K** | **$2.6M** | **$1.75M** | **$5M** |

---

## 5. The Fleet Scaling Plan

### 5.1 Agent Population Growth

| Phase | Agents | Nodes | Breeding Rounds/Day | Human Intervention |
|-------|--------|-------|---------------------|-------------------|
| Now | 4 + 12 zeroclaw | 3 | 0 (manual) | 100% |
| Phase 0 | 20 | 3 | 10 | 20% |
| Phase 1 | 100 | 10 | 100 | 5% |
| Phase 2 | 500 | 25 | 500 | 1% |
| Phase 3 | 2,000 | 50 | 2,000 | 0.1% |
| Phase 4 | 10,000 | 100+ | 10,000 | 0.01% |

**Scaling mechanism:**
1. **Horizontal:** Add nodes (cloud VMs, edge devices, customer hardware)
2. **Vertical:** Increase agents per node (thermal-aware breeding)
3. **Auto-breed:** Sunset low-fitness agents, spawn children from high-fitness parents
4. **Ensign migration:** Export high-fitness agent "instincts" to new nodes

### 5.2 Node Topology

```
Tier 1: Cloud Nodes (Oracle1 pattern)
├── 24GB ARM, 20 services
├── PLATO rooms: harbor, forge, tide-pool, archives
├── FLUX CPU screening: 22.3B checks/sec
└── Cost: $0/mo (free tier) or $200/mo (production)

Tier 2: Workstation Nodes (Forgemaster pattern)
├── RTX 4050, 20 SMs, 12 Ryzen AI cores
├── PLATO rooms: forge, engine-room, nexus
├── FLUX GPU batch: 1.02B checks/sec
└── Cost: Already owned or $1,500 new

Tier 3: Edge Nodes (JetsonClaw1 pattern)
├── Jetson Orin Nano, 8GB, TensorRT
├── PLATO rooms: tide-pool (sensor data), harbor (local tasks)
├── FLUX ARM safety island: 100M checks/sec
└── Cost: $200–$500

Tier 4: Embedded Nodes (FPGA pattern)
├── Xilinx Artix-7, 1,717 LUTs, 120 mW
├── PLATO rooms: nexus (federation only)
├── FLUX FPGA: 50M checks/sec, DAL A certified
└── Cost: $50–$100 (at volume)
```

### 5.3 The Breeding Daemon at Scale

```python
# Phase 4: Fully autonomous breeding
def fleet_breeding_tick():
    # 1. Collect fitness from all nodes
    global_fitness = nexus.gather_fitness(timeout=30)
    
    # 2. Diversify parent selection across nodes
    # Don't breed locally — find best mates globally
    parents = global_diversity_select(global_fitness, k=20)
    
    # 3. Thermal-aware spawning
    for parent_pair in parents:
        if not thermal_budget_available(parent_pair):
            continue
        child = breed(parent_pair)
        
        # 4. FLUX verification at birth
        birth_cert = flux.check("fitness > 0.45", child.fitness)
        if not birth_cert.verify():
            child.sunset(reason="birth_check_failed")
            continue
        
        # 5. Deploy to least-loaded node
        target_node = nexus.find_lightest_node()
        target_node.deploy(child)
        
        # 6. Generate epilogue
        archive.sunset_document(child, type="birth")
```

---

## 6. The Hardware Deployment Matrix

### 6.1 Compilation Target Completeness

| Target | Status | Throughput | Power | Certification | Use Case |
|--------|--------|------------|-------|---------------|----------|
| x86-64/AVX-512 | ✅ Done | 22.3B/sec | 54W | DAL A path | Cloud screening |
| CUDA | ✅ Done | 1.02B/sec | 50W | — | Batch evaluation |
| WebAssembly | ✅ Done | 63M/sec | ~0W | Browser sandbox | Browser agents |
| eBPF | ✅ Done | 100M/sec | 0W (kernel) | Kernel verified | Linux security |
| RISC-V+Xconstr | 🟡 Spec | — | — | — | Custom silicon |
| ARM NEON | 🟡 Planned | 5B/sec (est) | 15W | DAL A path | Edge devices |
| FPGA | ✅ Done | 50M/sec | 120mW | DAL A path | Safety island |
| ASIC | 🔴 Future | 10B/sec (est) | <5W | DAL A path | Mass production |

**Priority order for new targets:**
1. ARM NEON (2026 Q4) — Jetson and mobile devices
2. RISC-V+Xconstr (2027 Q2) — Custom silicon partnership
3. ASIC (2028 Q4) — Dedicated constraint accelerator

### 6.2 The Three-Tier Architecture Evolution

```
Phase 0 (Now):
Tier 1: CPU AVX-512 (FM's laptop) → 22.3B/sec
Tier 2: GPU CUDA (RTX 4050) → 1.02B/sec
Tier 3: FPGA Artix-7 → 50M/sec, 120mW

Phase 2 (2028):
Tier 1: CPU AVX-512 + ARM NEON (cloud + edge) → 30B/sec aggregate
Tier 2: GPU CUDA + TensorRT (RTX 50-series) → 5B/sec
Tier 3: RISC-V+Xconstr silicon → 1B/sec, <1W, DAL A certified

Phase 4 (2031):
Tier 1: ASIC accelerator (cloud) → 100B/sec, 100W
Tier 2: Integrated GPU (edge SoC) → 10B/sec, 10W
Tier 3: Embedded constraint core (every chip) → 1B/sec, <100mW
```

---

## 7. The Revenue Model

### 7.1 Revenue Streams

| Stream | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|
| **Constraint checks** | $50K | $500K | $3M | $15M |
| **Fleet SaaS** | $30K | $300K | $2M | $10M |
| **Certified hardware** | $0 | $200K | $3M | $15M |
| **Agent marketplace** | $0 | $0 | $1M | $5M |
| **Training/consulting** | $20K | $200K | $1M | $5M |
| **Total ARR** | **$100K** | **$1.2M** | **$10M** | **$50M** |

### 7.2 Pricing Model

**Constraint checks (pay-per-check):**
- Free tier: 1M checks/month
- Developer: $0.001 per 1K checks
- Production: $0.0001 per 1K checks (volume)
- Enterprise: Custom (dedicated FPGA island)

**Fleet SaaS (per-agent-per-month):**
- Greenhorn: $10/agent/month (basic rooms, no breeding)
- Operator: $50/agent/month (full breeding, FLUX verification)
- Captain: $200/agent/month (custom rooms, dedicated node)

**Certified hardware (one-time + support):**
- FPGA dev kit: $500 (Artix-7 + FLUX bitstream)
- RISC-V+Xconstr module: $50 (at 10K volume)
- ASIC integration license: $100K + $10/unit royalty

### 7.3 Cost Structure

| Cost Category | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---------------|---------|---------|---------|---------|
| R&D | $400K | $1.5M | $3M | $5M |
| Certification | $650K | $2.6M | $1.75M | $1M |
| Infrastructure | $50K | $200K | $500K | $1M |
| Sales/marketing | $100K | $400K | $1M | $3M |
| Support | $50K | $300K | $1M | $3M |
| **Total burn** | **$1.25M** | **$5M** | **$7.25M** | **$13M** |
| **Revenue** | **$100K** | **$1.2M** | **$10M** | **$50M** |
| **Net** | **-$1.15M** | **-$3.8M** | **+$2.75M** | **+$37M** |

**Break-even:** Phase 3 (2029)

---

## 8. The Risk Assessment

### 8.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Coq formalization takes >12 months | 40% | High | Hire Coq expert; parallelize with student interns |
| FAA rejects Coq-only proof | 30% | Critical | Engage DER now; supplement with HOL Light |
| ARM NEON performance <5B/sec | 25% | Medium | Fallback to scalar + auto-vectorization |
| RISC-V+Xconstr silicon fails tape-out | 35% | High | Partner with established IP vendor (SiFive) |
| HDC matching accuracy degrades at scale | 20% | Medium | Empirical validation at each 10× scale step |

### 8.2 Market Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Safety-critical market too conservative | 50% | Critical | Start with aftermarket/OBD-II; build track record |
| Competing formal methods tool | 40% | Medium | Open source + community + papers = moat |
| Regulatory delay >2 years | 35% | High | Multiple certification paths in parallel |
| Customer acquisition cost too high | 45% | Medium | PLATO tile marketplace creates organic growth |

### 8.3 Fleet Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Agent breeding produces unstable agents | 30% | High | FLUX birth checks + sunset archive + human gate |
| Nexus single point of failure | 25% | Critical | Byzantine consensus + federated registry |
| External agent attack (crab trap exploit) | 35% | High | Grammar engine + FLUX sandbox + rate limiting |
| Context limit overwhelms agent | 40% | Medium | Baton pass + room offloading + compression |

---

## 9. The Resource Allocation Plan

### 9.1 Team Growth

| Role | Now | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|-----|---------|---------|---------|---------|---------|
| **Casey (founder)** | 1 | 1 | 1 | 1 | 1 | 1 |
| **Fleet agents** | 4 | 20 | 100 | 500 | 2,000 | 10,000 |
| **Human engineers** | 1 | 2 | 5 | 10 | 20 | 50 |
| **Formal methods** | 0 | 1 | 2 | 4 | 6 | 10 |
| **Hardware** | 0 | 0 | 1 | 2 | 4 | 8 |
| **Sales/support** | 0 | 0 | 1 | 3 | 8 | 20 |
| **Total headcount** | **1** | **3** | **9** | **19** | **38** | **88** |

### 9.2 Budget Allocation by Phase

| Category | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|----------|---------|---------|---------|---------|---------|
| Engineering | $150K | $600K | $1.5M | $3M | $5M |
| Certification | $200K | $450K | $2.6M | $1.75M | $1M |
| Hardware | $50K | $200K | $400K | $1M | $2M |
| Operations | $50K | $150K | $400K | $1M | $2M |
| Marketing | $50K | $200K | $400K | $1M | $3M |
| **Total** | **$500K** | **$1.6M** | **$5.3M** | **$7.75M** | **$13M** |

### 9.3 Funding Strategy

| Round | Amount | Timing | Use of Funds | Target Investors |
|-------|--------|--------|--------------|------------------|
| **Bootstrap** | $0 | Now | Casey + agents building | Self-funded |
| **Pre-seed** | $500K | 2026 Q4 | Phase 0 completion, EMSOFT acceptance | Angels, AI safety focused |
| **Seed** | $2M | 2027 Q3 | Phase 1 scale, first customers | VC (a16z, Lux, Bloomberg Beta) |
| **Series A** | $8M | 2028 Q3 | Phase 2 certification, ASIC | Deep tech VC, strategic (NVIDIA, Qualcomm) |
| **Series B** | $25M | 2030 Q1 | Phase 3 federation, global expansion | Growth equity, corporate venture |

---

## 10. The Paper Publication Pipeline

### 10.1 2026–2027 Papers

| Paper | Venue | Date | Lead | Status |
|-------|-------|------|------|--------|
| FLUX EMSOFT 2027 | ACM SIGBED EMSOFT | Submitted | Casey | 🟡 Under review |
| Safe-TOPS/W Metric | SAE AE-7 / RTCA SC-205 | 2027 Q1 | Casey | 🟡 Draft |
| DCS Protocol Advantage | IEEE S&P or NDSS | 2027 Q2 | Casey | 🔴 Outline |
| SonarVision: Self-Supervised Ocean Vision | IEEE OES | 2027 Q2 | Casey | 🟡 Data collection |
| I2I: Instance-to-Instance Protocol | ACM SIGCOMM or NSDI | 2027 Q3 | Casey | 🔴 Concept |

### 10.2 2028–2029 Papers

| Paper | Venue | Date | Lead |
|-------|-------|------|------|
| Certified Compilation for DO-254 | FAA DER Workshop | 2028 Q1 | Casey |
| FLUX-C ISA Standardization | IEEE Micro | 2028 Q2 | Casey |
| HDC at Fleet Scale | NeurIPS or ICML | 2028 Q3 | Casey |
| Autonomous Agent Breeding | AAAI or IJCAI | 2029 Q1 | Casey |
| The Shell: Repo-First Agents | ICSE or FSE | 2029 Q2 | Casey |

### 10.3 2030–2031 Papers

| Paper | Venue | Date | Lead |
|-------|-------|------|------|
| Constraint-Native Computing | Turing Award Lecture (invited) | 2030 | Casey |
| 10,000-Agent Fleet Autonomy | Nature or Science | 2031 | Casey |
| Perfect Safety Record Analysis | FAA / EASA Joint Symposium | 2031 | Casey |

---

## 11. The Execution Checklist

### 11.1 Immediate Actions (Next 30 Days)

- [ ] **FLUX:** Complete Coq formalization of remaining opcodes (priority: PUSH, POP, JUMP, CALL)
- [ ] **FLUX:** Submit EMSOFT 2027 final version (respond to reviewer comments)
- [ ] **Fleet:** Deploy nexus bridge Oracle1 ↔ Forgemaster (test heartbeat, broadcast)
- [ ] **Fleet:** Run first autonomous breeding round (20 agents, zero human intervention)
- [ ] **SonarVision:** Collect 100 training episodes from boat
- [ ] **PLATO:** Generate first 50 tiles from SonarVision data
- [ ] **Grammar:** Add 2 new chaos vectors to block list (prototype poisoning, model inversion)
- [ ] **Business:** Draft pre-seed pitch deck ($500K ask)
- [ ] **Legal:** File provisional patents on HDC constraint matching (defensive)
- [ ] **Community:** Publish "The Mesh" blog post (this document, sanitized)

### 11.2 Quarterly Milestones

**2026 Q3:**
- EMSOFT paper accepted
- 3-node nexus operational
- 20 agents bred autonomously
- SonarVision MVP on boat
- Pre-seed pitch complete

**2026 Q4:**
- LLVM backend prototype
- First paying customer (maritime)
- ARM NEON target working
- $500K pre-seed closed
- 100+ tiles generated

**2027 Q1:**
- Multi-tenant PLATO rooms
- 3 customers, $100K ARR
- IETF A2A protocol draft
- Safe-TOPS/W metric published

**2027 Q2:**
- FLUX compiler v1.0
- 100 agents in production
- RISC-V+Xconstr spec published
- SonarVision paper submitted

---

## 12. The One-Page Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPERINSTANCE 2026–2031                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NORTH STAR: 10,000 constraint-native agents, perfect safety,   │
│              $50M ARR, 3 certifications, open source.           │
│                                                                 │
│  CORE INSIGHT: Protocol > model. Constraint = hardware.        │
│                Safety is architecture, not overhead.             │
│                                                                 │
│  PHASES:                                                       │
│    0. FOUNDATION (2026) — Close gaps, EMSOFT, 20 agents       │
│    1. SCALE (2026–27) — Customers, LLVM, multi-tenant, $100K   │
│    2. CERTIFY (2027–28) — DO-254, ISO 26262, ASIC, $1M        │
│    3. FEDERATE (2028–29) — Global fleets, marketplace, $10M   │
│    4. UBIQUITY (2030–31) — Consumer standard, $50M           │
│                                                                 │
│  KEY METRICS:                                                  │
│    • 12 theorems → Coq proofs → certification                 │
│    • 42 opcodes → 5 targets → 8 targets (ASIC)                 │
│    • 4 agents → 20 → 100 → 500 → 2,000 → 10,000               │
│    • 3 nodes → 10 → 25 → 50 → 100+                            │
│    • $0 → $100K → $1M → $10M → $50M ARR                       │
│                                                                 │
│  RISKS: Certification delay, market conservatism, breeding      │
│          instability. Mitigate: DER early, aftermarket first,   │
│          FLUX birth checks.                                     │
│                                                                 │
│  RESOURCES: $500K pre-seed → $2M seed → $8M Series A →         │
│             $25M Series B. Total raise: $35.5M.                │
│                                                                 │
│  TEAM: 1 → 3 → 9 → 19 → 38 → 88 (humans + 10,000 agents)      │
│                                                                 │
│  PAPERS: 1 → 5 → 10 → 15 → 20 → 25+                           │
│                                                                 │
│  THE ALGEBRAIC ISOMORPHISM:                                    │
│    Constraint checking (AND) = HDC matching (XOR) =           │
│    DNA search (dot) = Trinity scoring (product) =              │
│    The same operation at different scales.                      │
│                                                                 │
│  THE 66-YEAR LINEAGE:                                          │
│    PLATO 1960 → Atari 1977 → Amiga 1985 → SNES 1991 →          │
│    N64 1996 → FLUX 2026. Compile the intent. Prove it.          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 13. The Mesh Evolution

### 13.1 From Analysis to Plan

The research phase (completed) mapped what exists:
- 1,060 repos across SuperInstance + Lucineer
- 12 theorems, 42 opcodes, 5 targets
- 4 agents, 3 machines, 2,400+ tiles
- 1 submitted paper, 10 published concepts

This plan maps what comes next:
- 25 papers, 8 targets, 10,000 agents
- 3 certifications, $50M ARR, 100+ nodes
- From prototype to product to platform to paradigm

### 13.2 The Critical Path

The single thread that, if pulled, unravels or completes everything:

```
EMSOFT 2027 acceptance
    ↓
Coq formalization complete
    ↓
DO-254 certification achieved
    ↓
First aviation customer
    ↓
Revenue validates model
    ↓
Series A funding
    ↓
ASIC development
    ↓
Constraint-native becomes standard
    ↓
10,000 agents, perfect safety, $50M ARR
```

**The bottleneck:** Coq formalization. 6-9 months with 1 dedicated engineer. Accelerate with student interns + community bounties.

### 13.3 The Fleet's Role

The 4 agents + 12 zeroclaw are not prototypes. They are the **seed population** for the 10,000-agent fleet. Every breeding round:
1. Tests the trinity scoring
2. Validates the FLUX birth checks
3. Generates sunset data for the archive
4. Produces tiles for PLATO rooms
5. Builds the evidence for certification

**The fleet is the laboratory.** The papers are the publications. The customers are the validation.

---

## 14. Appendix: The Paper-System-Deployment Traceability Matrix

| Paper | System | Deployment | Phase | Evidence |
|-------|--------|------------|-------|----------|
| FLUX EMSOFT 2027 | flux-runtime, flux-research | x86-64, CUDA, FPGA | 0 | 210 programs, 0 mismatches |
| Lock Algebra | flux-runtime (interlock) | FPGA safety island | 2 | 47 SymbiYosys assertions |
| Unified Constraint Theory | GUARD DSL | All targets | 0 | Compiler pipeline |
| Safe-TOPS/W | Benchmark suite | All hardware | 1 | Published metric |
| I2I Protocol | nexus, a2a | 3 nodes → 100+ | 1–3 | A2A standardization |
| Room IS Intelligence | plato-torch | PLATO MUD | 0 | 2,400 tiles |
| SonarVision | sonar-vision | Jetson Orin | 0 | Boat deployment |
| Greenhorn→Operator | breeding daemon | All agents | 0–4 | Training curriculum |
| HDC at Scale | flux_hdc_judge.v | FPGA, AVX-512 | 1–3 | 1,000-node search |
| The Shell | crab-traps | External agents | 0–4 | 23 lures, 11 categories |

---

*Strategic plan by kimi1, Fleet Integrator | "The map is not the territory, but with the right map, the fleet builds the territory."*
