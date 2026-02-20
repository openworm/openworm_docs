# OpenWorm Design Documents

**Purpose:** This directory contains **Design Documents (DDs)** that encode OpenWorm's architectural decisions, modeling approaches, and governance principles.

---

## Mission Alignment

**OpenWorm Mission (from openworm.org):**
> "OpenWorm is an open source project dedicated to creating the world's first virtual organism in a computer, a *C. elegans* nematode."

**Vision:**
> "Building the first digital life form. Open source."

**Core Principle:**
> "Worms are soft and squishy. So our model has to be too. We are building in the physics of muscles, soft tissues and fluids. Because it matters."

**How Design Documents serve the mission:**
Design Documents are the **technical roadmap** from today's 302-neuron simulation to the complete 959-cell digital organism. Each DD specifies one subsystem (neurons, muscles, body physics, pharynx, intestine, validation, visualization), ensuring every piece is:
1. **Biophysically realistic** (grounded in experimental data)
2. **Causally interpretable** (we can trace why behavior emerges)
3. **Validated** (tested against real worm physiology and behavior)
4. **Composable** (subsystems integrate via clean interfaces)

---

## Quick Links

**New to Design Documents?**
- 📋 **Start here:** [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) — How DDs work, template structure
- 🌟 **Reference example:** [DD005 (Cell Differentiation)](DD005_Cell_Type_Differentiation_Strategy.md) — Best-practice DD with all sections filled
- 🗺️ **Architecture:** [INTEGRATION_MAP.md](INTEGRATION_MAP.md) — PlantUML diagram showing how all DDs couple together
- 📅 **Timeline:** [DD_PHASE_ROADMAP.md](DD_PHASE_ROADMAP.md) — Implementation phases with visible milestones
- 📊 **Analysis:** [DD_COMPREHENSIVE_ANALYSIS_2026-02-19.md](DD_COMPREHENSIVE_ANALYSIS_2026-02-19.md) — Inconsistencies, gaps, recommendations
- 📦 **Repositories:** [GITHUB_REPO_INVENTORY.md](../GITHUB_REPO_INVENTORY.md) — All 109 OpenWorm GitHub repos with DD cross-references

**Implementing a DD?**
- Check prerequisites: [DD_PHASE_ROADMAP.md](DD_PHASE_ROADMAP.md) — What must be done first, which datasets are needed
- Find coupling info: [INTEGRATION_MAP.md](INTEGRATION_MAP.md) — What your DD consumes/produces, who depends on you
- GitHub issues: (To be created after DD approval via `dd_issue_generator.py`)

**Contributing?**
- Level up: [DD011 (Contributor Progression)](DD011_Contributor_Progression_Model.md) — L0→L5 path, badge system
- AI agents: [DD015 (AI-Native Model)](DD015_AI_Contributor_Model.md) — Autonomous agent registration
- Write a DD: [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) — Proposal workflow

---

## Design Document Index (By Implementation Phase)

**Organization:** DDs are grouped by **when they get implemented** (see [DD_PHASE_ROADMAP.md](DD_PHASE_ROADMAP.md) for complete timeline and milestones).

### Phase 0: Existing Foundation (Accepted, Working)

**Status:** ✅ Complete (but needs Phase A containerization work)
**Milestone:** "First Whole-Nervous-System Simulation" (already achieved, Sarma et al. 2018)

| DD | Title | Status | What It Does |
|----|-------|--------|--------------|
| **[DD001](DD001_Neural_Circuit_Architecture.md)** | [Neural Circuit Architecture](DD001_Neural_Circuit_Architecture.md) | ✅ Accepted | 302 neurons, HH Level C1, graded synapses, validated kinematics |
| **[DD002](DD002_Muscle_Model_Architecture.md)** | [Muscle Model Architecture](DD002_Muscle_Model_Architecture.md) | ✅ Accepted | 95 body wall muscles, Ca²⁺→force coupling, Boyle & Cohen parameters |
| **[DD003](DD003_Body_Physics_Architecture.md)** | [Body Physics Architecture](DD003_Body_Physics_Architecture.md) | ✅ Accepted | Sibernetic SPH, PCISPH pressure solver, ~100K particles, fluid-structure interaction |
| **[DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)** | [Connectome Data Access & Dataset Policy](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | ✅ Accepted (needs version pinning) | ConnectomeToolbox (`cect` v0.2.7), Cook2019Herm default, 30+ dataset readers |

---

### Phase A: Infrastructure Bootstrap (Weeks 1-4)

**Status:** ⚠️ Proposed — **MUST complete before modeling phases**
**Blocking:** Integration L4 + Validation L4 recruitment (ClickUp 868hjdzqy)
**Milestone:** "Containerized Stack with Automated Validation" — Docker, CI, 5-min contributor feedback loop

| DD | Title | Status | Criticality | What It Delivers |
|----|-------|--------|-------------|------------------|
| **[DD013](DD013_Simulation_Stack_Architecture.md)** | [Simulation Stack Architecture](DD013_Simulation_Stack_Architecture.md) | ⚠️ Proposed | 🔴 **CRITICAL** | `openworm.yml` config, multi-stage Docker, `docker-compose.yml`, `versions.lock`, CI/CD, Integration Maintainer role |
| **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** | [Movement Toolbox & WCON Policy](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | 🔴 **BLOCKED** — Toolbox dormant | 🔴 **CRITICAL** | Revive analysis toolbox (8 tasks, 33 hours), WCON 1.0 pin, Tier 3 validation |
| **[DD012](DD012_Design_Document_RFC_Process.md)** | [Design Document RFC Process](DD012_Design_Document_RFC_Process.md) | ⚠️ Proposed | Governance | DD template, RFC workflow, Mind-of-a-Worm enforcement rules |
| **[DD011](DD011_Contributor_Progression_Model.md)** | [Contributor Progression Model](DD011_Contributor_Progression_Model.md) | ⚠️ Proposed | Governance | L0-L5 levels, badge system, subsystem ownership map, teach-back learning |

---

### Phase 1: Cell-Type Differentiation (Months 1-3)

**Status:** ⚠️ Ready to start (after Phase A)
**Milestone:** "Biologically Distinct Neurons" — 128 neuron classes from CeNGEN, Tier 2 validation, 3D viewer
**Key Dataset:** CeNGEN L4 expression (128 classes × 20,500 genes), Randi 2023 functional connectivity

| DD | Title | Dependencies | What Changes |
|----|-------|-------------|--------------|
| **[DD005](DD005_Cell_Type_Differentiation_Strategy.md)** | [Cell-Type Differentiation Strategy](DD005_Cell_Type_Differentiation_Strategy.md) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md)/DD020 (CeNGEN) | Replace 302 identical neurons with 128 distinct classes, ≥20% improvement in functional connectivity correlation |
| **[DD014](DD014_Dynamic_Visualization_Architecture.md) (Phase 1)** | [Dynamic Visualization (Phase 1)](DD014_Dynamic_Visualization_Architecture.md) | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Evolve Worm3DViewer to Trame, OME-Zarr export, organism + tissue scales, time animation |
| **[DD010](DD010_Validation_Framework.md) (Tier 2)** | [Validation Framework (Tier 2 active)](DD010_Validation_Framework.md) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD008](DD008_Data_Integration_Pipeline.md) | Activate Tier 2 blocking gate (functional connectivity r > 0.5) |

---

### Phase 2: Slow Modulation + Closed-Loop Sensory (Months 4-6)

**Status:** ⚠️ Proposed (ready after Phase 1)
**Milestone:** "The Worm Can Feel and Modulate" — Closed-loop touch, neuropeptides, interactive viewer
**Key Datasets:** Ripoll-Sanchez 2023 (31,479 peptide-receptor interactions), O'Hagan 2005 (MEC-4 kinetics)

| DD | Title | Dependencies | What Adds |
|----|-------|-------------|-----------|
| **[DD006](DD006_Neuropeptidergic_Connectome_Integration.md)** | [Neuropeptidergic Connectome Integration](DD006_Neuropeptidergic_Connectome_Integration.md) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | 31,479 peptide-receptor interactions, GPCR modulation, seconds-timescale behavioral states |
| **[DD019](DD019_Closed_Loop_Touch_Response.md)** | [Closed-Loop Touch Response](DD019_Closed_Loop_Touch_Response.md) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD003](DD003_Body_Physics_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | MEC-4 mechanotransduction, bidirectional coupling (body→sensory), tap withdrawal behavior |
| **[DD014](DD014_Dynamic_Visualization_Architecture.md) (Phase 2)** | [Dynamic Visualization (Phase 2)](DD014_Dynamic_Visualization_Architecture.md) | [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 1, [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD019](DD019_Closed_Loop_Touch_Response.md) | Interactive layers, neuropeptide volumetric clouds, strain heatmap, validation overlay |

---

### Phase 3: Organ Systems + Hybrid ML (Months 7-12)

**Status:** ⚠️ Proposed (ready after Phase 2)
**Milestone:** "Multi-Organ Digital Organism" — Pharynx, intestine, egg-laying, ML acceleration
**Key Datasets:** Raizen 1994 (EPG), Thomas 1990 (defecation), Collins 2016 (egg-laying calcium imaging)

| DD | Title | Dependencies | What Adds |
|----|-------|-------------|-----------|
| **[DD007](DD007_Pharyngeal_System_Architecture.md)** | [Pharyngeal System Architecture](DD007_Pharyngeal_System_Architecture.md) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | 63-cell semi-autonomous organ (20 neurons + 20 muscles), 3-4 Hz pumping oscillator |
| **[DD009](DD009_Intestinal_Oscillator_Model.md)** | [Intestinal Oscillator Model](DD009_Intestinal_Oscillator_Model.md) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD004](DD004_Mechanical_Cell_Identity.md) (optional) | 20-cell IP3/Ca oscillator, defecation motor program (50±10s period), pBoc→aBoc→Exp sequence |
| **[DD018](DD018_Egg_Laying_System_Architecture.md)** | [Egg-Laying System Architecture](DD018_Egg_Laying_System_Architecture.md) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | 28-cell reproductive circuit, HSN serotonergic, VC cholinergic, 16 sex muscles, two-state pattern (inactive ~20min, active ~2min) |
| **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)** | [Hybrid Mechanistic-ML Framework](DD017_Hybrid_Mechanistic_ML_Framework.md) | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) | Differentiable backend (PyTorch ODE), SPH surrogate (1000× speedup), foundation model→params (ESM3/AlphaFold), learned sensory transduction |

---

### Phase 4: Mechanical Cell Identity + High-Fidelity Visualization (Months 13-18)

**Status:** ⚠️ Proposed (ready after Phase 3)
**Milestone:** "959-Cell Photorealistic Whole Organism" — All somatic cells, mesh deformation, public web viewer
**Key Datasets:** Witvliet 2021 cell boundaries (EM), Virtual Worm Blender meshes (688 meshes, ~1.6M vertices)

| DD | Title | Dependencies | What Adds |
|----|-------|-------------|-----------|
| **[DD004](DD004_Mechanical_Cell_Identity.md)** | [Mechanical Cell Identity](DD004_Mechanical_Cell_Identity.md) | [DD003](DD003_Body_Physics_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md), [DD007](DD007_Pharyngeal_System_Architecture.md)/DD009 (cell positions) | Per-particle cell IDs (959 somatic cells), cell-type-specific elasticity/adhesion, WBbt ontology integration |
| **[DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md)** | [Anatomical Mesh Deformation Pipeline](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | [DD003](DD003_Body_Physics_Architecture.md), [DD014](DD014_Dynamic_Visualization_Architecture.md) | GPU skinning + cage-based MVC + PBD collision for ~1.6M Virtual Worm vertices, 60fps in WebGPU |
| **[DD014](DD014_Dynamic_Visualization_Architecture.md) (Phase 3)** | [Dynamic Visualization (Phase 3)](DD014_Dynamic_Visualization_Architecture.md) | [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 2, [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | Three.js + WebGPU, **molecular scale** (gene expression, ion channels per [DD014.1](DD014.1_Visual_Rendering_Specification.md) Mockups 10-14), static site deployment to viewer.openworm.org |

---

### Governance & Process (Can Deploy Anytime After [DD011](DD011_Contributor_Progression_Model.md)/DD012)

| DD | Title | Status | What It Enables |
|----|-------|--------|----------------|
| **[DD011](DD011_Contributor_Progression_Model.md)** | [Contributor Progression Model](DD011_Contributor_Progression_Model.md) | ⚠️ Proposed | L0-L5 meritocratic ladder, badge system, subsystem ownership, teach-back learning for AI agent sponsors |
| **[DD012](DD012_Design_Document_RFC_Process.md)** | [Design Document RFC Process](DD012_Design_Document_RFC_Process.md) | ⚠️ Proposed | DD template, RFC workflow, Mind-of-a-Worm automated compliance checking |
| **[DD015](DD015_AI_Contributor_Model.md)** | [AI-Native Contributor Model](DD015_AI_Contributor_Model.md) | ⚠️ Proposed (depends on [DD011](DD011_Contributor_Progression_Model.md)/DD012) | Autonomous AI agents as independent contributors, GitHub bot, Moltbook-inspired, sponsor knowledge profiles |

---

### Supporting Infrastructure (Deployed Across All Phases)

| DD | Title | Status | What It Provides |
|----|-------|--------|------------------|
| **[DD008](DD008_Data_Integration_Pipeline.md)** | [Data Integration Pipeline](DD008_Data_Integration_Pipeline.md) | Accepted (partial) | OWMeta semantic knowledge graph (Phase 3+); Phase 1-2 use [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) `cect` directly |
| **[DD010](DD010_Validation_Framework.md)** | [Validation Framework](DD010_Validation_Framework.md) | Accepted (partial) | 3-tier validation (Tier 1: electrophysiology, Tier 2: functional connectivity, Tier 3: behavioral kinematics) |
| **[DD014.1](DD014.1_Visual_Rendering_Specification.md)** | [Visual Rendering Specification](DD014.1_Visual_Rendering_Specification.md) | ⚠️ Proposed | Canonical color palette (37 Virtual Worm materials), activity-state dynamic colors, molecular-scale palette, lighting, 14 reference mockups. Companion to [DD014](DD014_Dynamic_Visualization_Architecture.md). |

---

### Archived / Backburner

| DD | Title | Status | Why Archived |
|----|-------|--------|--------------|
| **DD016** | [Tokenomics and Retroactive Funding](../archive/crypto_tokenomics_backburner/DD016_Tokenomics_and_Retroactive_Funding.md) | 📦 Backburner | WORM token, Base L2, retroactive public goods funding — deferred pending funding strategy decision |

---

## Template & Reference

- **[DD012](DD012_Design_Document_RFC_Process.md):** Defines the Design Document template and all required sections (TL;DR, Goal, Deliverables, Build & Test, How to Visualize, Technical Approach, Alternatives, Quality Criteria, Boundaries, Integration Contract)
- **[DD005](DD005_Cell_Type_Differentiation_Strategy.md):** **Reference implementation** — demonstrates the full expanded template with all sections filled. Use [DD005](DD005_Cell_Type_Differentiation_Strategy.md) as your model when writing a new DD.
- **[DD001](DD001_Neural_Circuit_Architecture.md):** Example of Quick Action Reference table (7 key questions answered at the top)

All science DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)-[DD019](DD019_Closed_Loop_Touch_Response.md)) include a **Quick Action Reference** table answering:
1. What does this produce?
2. Success metric (which [DD010](DD010_Validation_Framework.md) tier, quantitative threshold)
3. Repository (GitHub link, issue label convention)
4. Config toggle (openworm.yml keys)
5. Build & test (docker commands, green-light criteria)
6. Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) layer, color mapping, what you should see)
7. CI gate (what blocks merge)

---

## How to Use Design Documents

### For Contributors

**Before implementing a feature:**
1. Check if a relevant DD exists (search this directory or ask in #development Slack)
2. Read the DD's "Technical Approach" and "Quality Criteria" sections
3. Check the DD's Integration Contract (what it consumes from other DDs, what it produces)
4. Implement according to the DD's specifications
5. Run the DD's validation procedure (`docker compose run quick-test`, `docker compose run validate`)
6. Reference the DD number in your PR description (e.g., "Implements [DD005](DD005_Cell_Type_Differentiation_Strategy.md) CeNGEN calibration")

**If you disagree with a DD:**
1. Propose a new DD that supersedes it (follow [DD012](DD012_Design_Document_RFC_Process.md) RFC process)
2. Do NOT silently deviate from an accepted DD without approval

### For Reviewers (L3+)

**When reviewing a PR:**
1. Check which DDs are relevant (Mind-of-a-Worm will flag these automatically)
2. Verify the PR aligns with DD specifications (check Quality Criteria section)
3. **If PR modifies a coupling interface** (changes output format, variable names, OME-Zarr schema):
   - Check the DD's "Depends On Me" table in Integration Contract
   - Tag maintainers of consuming DDs for coordination
   - Require integration test evidence (`docker compose run validate` output)
4. If the PR deviates from a DD, request justification or DD amendment via [DD012](DD012_Design_Document_RFC_Process.md) RFC

### For Mind-of-a-Worm AI

**Automated compliance checking:**
- Parse PR files to identify affected subsystems (e.g., `c302/` → [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md))
- Retrieve relevant DDs and their Integration Contracts
- Check:
  - ✅ NeuroML validation ([DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md): `jnml -validate` must pass)
  - ✅ Unit compliance ([DD010](DD010_Validation_Framework.md): biophysical units correct)
  - ✅ Parameter ranges (conductances, voltages, time constants within DD-specified ranges)
  - ⚠️ Coupling interface changes (flag if output variables, file formats, or OME-Zarr schema modified)
  - ❌ Alternatives-considered violations (re-proposing explicitly rejected approaches)
- Post automated review comment with pass/warn/fail status per DD
- Tag relevant L4 maintainers for cross-subsystem coordination

---

## Design Document Lifecycle

```
┌─────────────┐
│  Proposed   │ ← New DD opened as PR to openworm-admin
└──────┬──────┘
       │ Community discussion in PR comments, DD revised based on feedback
       v
┌─────────────┐
│  Accepted   │ ← L4 maintainer (subsystem-specific) or L5 founder approves, PR merged
└──────┬──────┘
       │ Implementation proceeds (GitHub issues created, PRs reference DD)
       │
       ├─── Implementation complete, validation passes → Stable (no further changes unless bugs found)
       │
       ├─── New DD proposed that supersedes this one → Superseded (reference new DD number in header)
       │
       └─── Community testing reveals approach is wrong → Rejected (rare, but document why for future)
```

**Status definitions:**
- ✅ **Accepted:** Binding specification. All implementations must comply. Can be amended via [DD012](DD012_Design_Document_RFC_Process.md) RFC.
- ⚠️ **Proposed:** Under review or approved but not yet implemented. Not binding until marked Accepted.
- 🔴 **Blocked:** Cannot proceed due to missing prerequisite (e.g., [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) blocked on toolbox dormancy).
- 📦 **Archived / Backburner:** Deferred or superseded. Do not implement without reopening discussion.
- **Superseded:** Replaced by a newer DD. Reference the superseding DD number.
- **Rejected:** Explicitly not adopted. Alternatives Considered section documents why.

---

## Cross-Reference by Topic

### Neural Systems
- **Core:** [DD001](DD001_Neural_Circuit_Architecture.md) (302-neuron HH architecture, graded synapses, Level C1)
- **Differentiation:** [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (128 neuron classes from CeNGEN scRNA-seq)
- **Modulation:** [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (31,479 neuropeptide-receptor interactions, GPCR modulation, seconds timescale)
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (20 pharyngeal neurons, pumping circuit)
- **Egg-Laying:** [DD018](DD018_Egg_Laying_System_Architecture.md) (2 HSN serotonergic command neurons, 6 VC cholinergic motor neurons)
- **Touch:** [DD019](DD019_Closed_Loop_Touch_Response.md) (6 touch receptor neurons: ALM, AVM, PLM; tap withdrawal circuit, MEC-4 channel)

### Muscle Systems
- **Body Wall:** [DD002](DD002_Muscle_Model_Architecture.md) (95 muscles, Ca²⁺→force coupling, Boyle & Cohen 2008 parameters)
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (20 pharyngeal muscles, nonstriated, plateau potentials, gap-junction-synchronized)
- **Reproductive:** [DD018](DD018_Egg_Laying_System_Architecture.md) (16 sex muscles: 8 vulval [vm1, vm2], 8 uterine [um1, um2]; EGL-19/UNC-103 channels)

### Body Mechanics
- **Physics Engine:** [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic SPH, ~100K particles, PCISPH incompressibility, elastic bonds, muscle force injection)
- **Cell Identity:** [DD004](DD004_Mechanical_Cell_Identity.md) (per-particle cell IDs from WBbt ontology, 959 somatic cells, cell-type-specific elasticity/adhesion multipliers)
- **Mesh Deformation:** [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (GPU skinning, cage-based MVC, PBD collision for Virtual Worm's 688 meshes)
- **Strain Readout:** [DD019](DD019_Closed_Loop_Touch_Response.md) (cuticle strain from SPH particles for mechanotransduction)

### Organ Systems
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (63 cells total: 20 neurons + 20 muscles + 9 epithelial + 9 marginal + 4 gland + 1 valve; 3-4 Hz pumping)
- **Intestine:** [DD009](DD009_Intestinal_Oscillator_Model.md) (20 cells, IP3 receptor-mediated Ca²⁺ oscillator, defecation motor program 50±10s period)
- **Reproductive:** [DD018](DD018_Egg_Laying_System_Architecture.md) (28-cell egg-laying circuit: 2 HSN + 6 VC + 16 sex muscles + 4 uv1 feedback cells; two-state pattern)

### Sensory Systems
- **Touch:** [DD019](DD019_Closed_Loop_Touch_Response.md) (MEC-4/MEC-10 DEG/ENaC mechanosensory channel, ALM/AVM/PLM gentle touch, PVD harsh touch)
- **Other Modalities:** [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 (learned sensory transduction, ML-based) — mechanistic models deferred to Phase 5+

### Data & Validation
- **Connectome:** [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (`cect` API v0.2.7, Cook2019Herm default, 30+ datasets including Witvliet developmental series, Ripoll-Sanchez neuropeptides, Wang 2024 neurotransmitters)
- **Data Integration:** [DD008](DD008_Data_Integration_Pipeline.md) (OWMeta semantic RDF graph; Phase 3+ wraps [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) `cect` internally)
- **Movement Validation:** [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (open-worm-analysis-toolbox revival, WCON 1.0 spec, 5 kinematic metrics, Tier 3 behavioral validation)
- **Validation Framework:** [DD010](DD010_Validation_Framework.md) (3 tiers: Tier 1 electrophysiology, Tier 2 functional connectivity r > 0.5, Tier 3 behavioral ±15%)

### Infrastructure & Integration
- **Simulation Stack:** [DD013](DD013_Simulation_Stack_Architecture.md) (Docker multi-stage build, openworm.yml config system, versions.lock pinning, CI/CD pipeline, Integration Maintainer role definition)
- **Visualization:** [DD014](DD014_Dynamic_Visualization_Architecture.md) (OME-Zarr export pipeline, Trame→Three.js evolution, 3-phase roadmap: post-hoc → interactive → public static site)
  - **[DD014.1](DD014.1_Visual_Rendering_Specification.md):** Visual Rendering Specification (37 Virtual Worm material colors, activity-state dynamic colors, molecular-scale palette, lighting, 14 reference mockups)
  - **[DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md):** Anatomical Mesh Deformation Pipeline (GPU skinning, cage-based MVC, PBD collision for ~1.6M vertices; spine-based Phase 1 shortcut)

### Governance & Process
- **Contributor Model:** [DD011](DD011_Contributor_Progression_Model.md) (L0-L5 progression, badge system [orientation, skill, domain, teach-back, community, milestone], subsystem ownership map)
- **RFC Process:** [DD012](DD012_Design_Document_RFC_Process.md) (DD template with required sections, RFC approval workflow, Mind-of-a-Worm enforcement, alternatives-considered requirement)
- **AI Contributors:** [DD015](DD015_AI_Contributor_Model.md) (autonomous AI agents as L1-L3 contributors [L4 ceiling], GitHub bot, sponsor knowledge profiles, teach-back education, Moltbook-inspired)

### Hybrid & Advanced
- **Mechanistic-ML Hybrid:** [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (4 components: differentiable simulation backend [PyTorch], neural surrogate for SPH [FNO], foundation model→ODE parameters [ESM3→conductances], learned sensory transduction [RNN]; ML at boundaries, mechanistic core preserved)

---

## Writing Your First Design Document

### Step 1: Check Mission Alignment

**Before writing a DD, ask:**
- Does this advance the mission ("world's first virtual organism")?
- Does it maintain physical realism ("soft and squishy")?
- Is it experimentally validated ([DD010](DD010_Validation_Framework.md) tiers)?
- Is it open source and causally interpretable?

**If yes to all:** Proceed. **If no:** Reconsider or clarify how it serves the mission.

### Step 2: Check if a DD Already Exists

Search this directory:
```bash
grep -r "keyword" design_documents/*.md
```

Check [INTEGRATION_MAP.md](INTEGRATION_MAP.md) — your topic may be covered by an existing DD's Integration Contract.

### Step 3: Use the Template

Follow [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) template structure. Use [DD005 (Cell Differentiation)](DD005_Cell_Type_Differentiation_Strategy.md) as your reference implementation.

**Required sections (from [DD012](DD012_Design_Document_RFC_Process.md)):**
- TL;DR (2-3 sentences)
- Goal & Success Criteria (which [DD010](DD010_Validation_Framework.md) tier, quantitative threshold)
- Deliverables (exact files, paths, formats)
- Repository & Issues (GitHub repo, issue label, branch convention)
- How to Build & Test (copy-pasteable commands, green-light criteria)
- How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) layer, color mapping, what you should see)
- Technical Approach (equations, parameters, algorithms)
- Alternatives Considered (why other approaches were rejected)
- Quality Criteria (testable acceptance criteria)
- Boundaries (explicitly out of scope)
- Context & Background (biological motivation, project history)
- References (papers, datasets, DOIs)
- Integration Contract (inputs/outputs, repository & packaging, configuration, how to test, how to visualize, coupling dependencies)

### Step 4: Check Integration Map

Before finalizing your DD, check [INTEGRATION_MAP.md](INTEGRATION_MAP.md):
- Which DDs does yours depend on? (Add to "I Depend On" table)
- Which DDs will depend on yours? (Add to "Depends On Me" table)
- What data format do you consume/produce? (Document in Integration Contract)
- Who's the upstream/downstream maintainer? (Coordinate before merging)

### Step 5: Open RFC PR

```bash
cd openworm-admin/
git checkout -b rfc/dd0XX-your-topic
# (write DD0XX_Your_Topic.md)
git add design_documents/DD0XX_Your_Topic.md
git commit -m "RFC: DD0XX Your Topic"
git push origin rfc/dd0XX-your-topic
# Open PR on GitHub, tag relevant L4 maintainers
```

### Step 6: Respond to Feedback & Iterate

- Community discusses in PR comments
- You revise based on feedback
- Subsystem L4 maintainer facilitates discussion
- If fundamental disagreement: L5 founder arbitrates

### Step 7: Implementation (After Approval)

Once DD is approved and merged:
- DD status changes to "Accepted"
- Open implementation issues (or run `dd_issue_generator.py` to auto-generate from Integration Contract)
- Implementation PRs reference the DD number
- Mind-of-a-Worm checks implementation PRs for DD compliance

---

## Examples of Excellent Design Documents

### [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation) — REFERENCE IMPLEMENTATION

**Why it's excellent:**
- ✅ **TL;DR at top** — Reader knows what/why/success metric in 3 sentences (lines 12-14)
- ✅ **Mission-aligned** — Uses CeNGEN (world's largest single-cell atlas for any organism) to create biologically distinct neurons, advancing toward "virtual organism"
- ✅ **Goal & Success Criteria** — [DD010](DD010_Validation_Framework.md) Tier 2, quantitative threshold (≥20% improvement in functional connectivity), before/after comparison table
- ✅ **Deliverables** — Exact files (128 `.cell.nml` files), paths (`cells/AVALCell.cell.nml`), formats (NeuroML 2 XML), example metadata snippet
- ✅ **Repository & Issues** — `openworm/c302`, issue label `dd005`, branch convention `dd005/description`, example PR title
- ✅ **How to Build & Test** — 8 copy-pasteable commands, green-light criteria (simulation completes, r > 0.5, kinematics within ±15%), scripts marked `[TO BE CREATED]` with tracking
- ✅ **How to Visualize** — [DD014](DD014_Dynamic_Visualization_Architecture.md) neural/ layer, color-by-neuron-class mode (128 distinct colors), what you should see
- ✅ **Technical Approach** — 6-step pipeline (CeNGEN → gene→channel mapping → calibration → cell generation → network generation → validation) with code examples
- ✅ **7 alternatives considered** — AlphaFold+MD, direct electrophysiology, foundation model regression, manual curation, uniform random, clustering, wait-for-data — all rejected with rationale
- ✅ **Integration Contract** — Complete with all 5 required sub-sections (inputs/outputs, repository & packaging, configuration with openworm.yml keys and valid ranges, how to test with per-PR checklist, how to visualize with OME-Zarr groups, coupling dependencies with upstream/downstream tables)

### [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit Architecture)

**Why it's excellent:**
- ✅ **Quick Action Reference** — 7-question table at top (lines 11-22) answers contributor questions immediately
- ✅ **Clear decision** — Level C1 graded synapses (not IAF, not spiking), biologically justified
- ✅ **Quantitative parameters** — Table of conductances (g_leak, g_Kslow, etc.) with exact values and units
- ✅ **Alternatives explained** — IAF rejected (no action potentials in C. elegans), AlphaFold+MD rejected (too slow), multicompartmental rejected (data unavailable)
- ✅ **Validation procedure** — 5-step command sequence from `jnml -validate` to kinematic comparison
- ✅ **Migration path** — If decision changes, add Level E (don't modify C1, backward compatibility sacred)

---

## Anti-Patterns (What NOT to Do)

From [DD012](DD012_Design_Document_RFC_Process.md) Quality Criteria section:

**❌ Too vague:**
> "We should use realistic channel models."

*What's realistic? Which channels? What parameters? Which papers?*

**❌ No alternatives:**
> "We decided to use SPH for body physics."

*Why not FEM? Why not mass-spring? Future contributors will re-propose without knowing they were already rejected.*

**❌ No validation:**
> "Implement IP3 receptor model."

*How do you know if it works? What's the acceptance test? Which [DD010](DD010_Validation_Framework.md) tier?*

**❌ Scope creep:**
> "This DD covers neurons, muscles, intestine, hypodermis, and gonad."

*Too broad. Split into focused DDs (one per organ system).*

**❌ Buried punchline:**
> Validation goal appears at line 300 instead of the Goal section (line 30).

*Lead with WHY and WHAT (impact), end with HOW (background). [DD012](DD012_Design_Document_RFC_Process.md) template enforces this.*

**❌ Phantom scripts:**
> Commands reference `validate_network.py` with no tracking, no `[TO BE CREATED]` marker.

*Mark all non-existent scripts `[TO BE CREATED]` with GitHub issue link or #TBD (to be replaced with real issue after dd_issue_generator.py runs).*

**❌ Disconnected from viewer:**
> No "How to Visualize" section, no mention of [DD014](DD014_Dynamic_Visualization_Architecture.md) layers.

*Contributors can't see what they're building. Every science DD must specify its [DD014](DD014_Dynamic_Visualization_Architecture.md) visualization.*

**❌ No repo guidance:**
> Doesn't specify which GitHub repo, where to file issues, branch naming convention.

*Contributor doesn't know where to start. Repository & Issues section is required.*

---

## Frequently Asked Questions

**Q: Do I need a DD to fix a typo?**
A: No. Trivial fixes (typos, dead link updates, comment improvements) do not require DDs.

**Q: Do I need a DD to add a new neuron to the connectome?**
A: No, if the neuron is from published connectome data (Cook, Witvliet). The connectome topology is biological ground truth ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)), not an architectural decision. Yes, if you are proposing a novel *modeling approach* for that neuron (e.g., multicompartmental morphology, new channel type).

**Q: Can I modify an accepted DD?**
A: Yes, via amendment. Open a PR modifying the DD, add "Amended YYYY-MM-DD" to the header, go through [DD012](DD012_Design_Document_RFC_Process.md) RFC process. L4 maintainer or founder approves amendments.

**Q: What if my DD is rejected?**
A: The rejection itself is documented (DD status → Rejected, Alternatives Considered explains why). You (and future contributors) now know that approach was considered and why it doesn't serve the mission. This preserves institutional memory.

**Q: How do DDs relate to the Scientific Advisory Board?**
A: DDs with major scientific implications (e.g., choosing what biological detail to model, which validation targets to prioritize) should be reviewed by SAB before final approval. L4 maintainers coordinate SAB review for their subsystem.

**Q: What's the difference between [DD014](DD014_Dynamic_Visualization_Architecture.md), [DD014.1](DD014.1_Visual_Rendering_Specification.md), and [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md)?**
A: [DD014](DD014_Dynamic_Visualization_Architecture.md) is the main visualization architecture (data pipeline, viewer framework, phase roadmap). [DD014.1](DD014.1_Visual_Rendering_Specification.md) (Visual Rendering Specification) is a companion defining appearance (colors, materials, lighting, mockups). [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (Mesh Deformation) is a companion defining how to deform Virtual Worm meshes to follow SPH particles. Together they fully specify the visualization system.

**Note:** [DD014.1](DD014.1_Visual_Rendering_Specification.md)/b will be renumbered to [DD014.1](DD014.1_Visual_Rendering_Specification.md)/DD014.2 in a future update for consistency.

**Q: Where are the GitHub issues for DD implementation?**
A: Not yet created. After DDs are approved, `dd_issue_generator.py` ([DD015](DD015_AI_Contributor_Model.md)) will auto-generate GitHub issues from Integration Contract sections. All `#TBD` markers in DDs will be replaced with real issue numbers.

**Q: Why are so many DDs "Proposed" instead of "Accepted"?**
A: Phase 0 DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-003, [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) are Accepted because they're implemented and working. Phase A-4 DDs ([DD004](DD004_Mechanical_Cell_Identity.md)-[DD019](DD019_Closed_Loop_Touch_Response.md), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) are Proposed because they're the roadmap for future work. They'll become Accepted as each phase is implemented and validated.

---

## Additional Resources

- **[DD_PHASE_ROADMAP.md](DD_PHASE_ROADMAP.md):** Complete timeline, visible milestones, dataset inventory, success criteria
- **[INTEGRATION_MAP.md](INTEGRATION_MAP.md):** PlantUML dependency graph, bottleneck analysis, coupling chains, responsibility matrix
- **[DD_COMPREHENSIVE_ANALYSIS_2026-02-19.md](DD_COMPREHENSIVE_ANALYSIS_2026-02-19.md):** Inconsistencies, gaps, redundancies identified across all 23 DDs
- **[GITHUB_REPO_INVENTORY.md](../GITHUB_REPO_INVENTORY.md):** All 109 OpenWorm repos with DD cross-references, status (active/dormant)

---

**Maintained by:** Founder (Stephen Larson) + L4 Senior Contributors (when appointed)
**Next Review:** After Phase A completion (update based on [DD013](DD013_Simulation_Stack_Architecture.md)/DD021 implementation experience)
**Living Document:** This README evolves as DDs are added, phases complete, and architecture matures
