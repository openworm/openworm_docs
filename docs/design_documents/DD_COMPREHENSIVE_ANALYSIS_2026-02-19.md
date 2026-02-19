# Comprehensive Design Document Analysis
## OpenWorm Architecture Review — February 19, 2026

**Prepared by:** Claude (Sonnet 4.5)
**Scope:** All 23 Design Documents (DD001-DD021 + DD014.1/b + DD016 archived)
**Purpose:** Identify inconsistencies, gaps, redundancies, and propose reorganization

---

## Executive Summary: The Top 10 Critical Findings

### 🚨 CRITICAL (Blocking)

1. **Tier 3 Validation Is Currently Impossible**
   - DD010 requires `open-worm-analysis-toolbox` for behavioral validation
   - DD021 reveals the toolbox is **completely broken** (dormant since Jan 2020, fails on Python 3.12)
   - **Impact:** DD013's CI/CD pipeline Steps 4-5 cannot be implemented; Tier 3 validation doesn't work
   - **Resolution:** DD021's 8-task revival plan (33 hours) must be **Phase A priority** alongside DD013

2. **Integration Maintainer Role Is Vacant**
   - DD013 creates this critical L4 role (owns Docker, CI, openworm.yml, versions.lock, master_openworm.py)
   - DD011 Subsystem Ownership Map: "Integration Stack: **TBD — Critical hire**"
   - Padraig is de facto owner but it's not formalized
   - **Impact:** Bus factor = 1; integration work falls on already-overloaded maintainer
   - **Resolution:** Recruit or appoint L4 Integration Maintainer (DD011 process)

3. **Missing Hundreds of Scripts with No Issue Tracking**
   - Every science DD (DD001-DD009, DD018-DD019) marks scripts `[TO BE CREATED]` with "GitHub issue: openworm/XXX#TBD"
   - **But these issues don't actually exist**
   - Contributors can't find or claim this work
   - **Impact:** Implementation stalls because scripts to track progress don't exist
   - **Resolution:** Run `scripts/dd_issue_generator.py` (mentioned in DD015) to create GitHub issues from all Integration Contracts

### ⚠️ MAJOR (Needs Resolution)

4. **OWMeta (DD008) vs. cect (DD020) Data Access Contradiction**
   - DD008 line 138: "All modeling code MUST access data through OWMeta"
   - DD020 line 27: "Never parse raw files — always use cect"
   - **Both are positioned as mandatory**, but they're different APIs
   - DD020 acknowledges the phasing (cect now, OWMeta Phase 3+), **but DD008 doesn't**
   - **Resolution:** Update DD008 to acknowledge DD020's phasing: "Phase 1-2 use cect directly; Phase 3+ OWMeta calls cect internally"

5. **DD014 Phase 1 Scope Unclear**
   - DD014 says Phase 1 is "post-hoc static viewer" with "organism and tissue scales"
   - DD014.1 specifies **molecular scale** in extreme detail (nucleus, gene transcription, vesicle trafficking, 14 reference mockups)
   - Is molecular scale Phase 1, 2, or 3?
   - DD014.1 Mockups 13-14 are molecular — but roadmap suggests this is Phase 3
   - **Resolution:** Clarify in DD014: molecular scale is **Phase 3 only**; Phase 1 = organism + tissue scales

6. **Phase Numbering Is Inconsistent**
   - No master phase document
   - DD004 "Phase 4", DD005 "Phase 1", DD006 "Phase 2", DD007/DD009/DD018 "Phase 3"
   - DD019 "Phase 2-3" (ambiguous)
   - **Resolution:** Create **DD_PHASE_ROADMAP.md** with canonical phase definitions and DD assignments

### 📊 STRUCTURAL (Reorganization Needed)

7. **Coupling Dependencies Are Local, Not Global**
   - Every DD has "Coupling Dependencies" tables (I Depend On / Depends On Me)
   - **But there's no master coupling diagram**
   - A reader must synthesize 21 separate tables to understand the full dependency graph
   - **Resolution:** Generate **INTEGRATION_MAP.md** with visual coupling diagram (auto-generated from DD Integration Contracts)

8. **DD014 Companions Should Be Renumbered**
   - DD014.1 and DD014.2 are companions to DD014, not standalone
   - Current numbering (DD014.1/b) is informal
   - **Better:** DD014.1 (Visual Rendering), DD014.2 (Mesh Deformation) — signals they're sub-documents
   - **Alternative:** Fold into DD014 as sections (single massive DD)
   - **Resolution:** Renumber to DD014.1 and DD014.2, update all cross-references

9. **Validation L4 Maintainer Is Vacant**
   - DD011 Subsystem Ownership Map: "Validation: **TBD**"
   - DD021 revival plan assigns all 8 tasks to "Validation L4" — **but this person doesn't exist**
   - **Resolution:** Recruit Validation L4 or assign revival to existing contributor (could be community L2 promoted to L3)

10. **Missing Master Coupling Between DD013 and All Science DDs**
    - DD013 says "every DD now has an Integration Contract section" (line 750)
    - But DD013 doesn't list which DDs it depends on or which depend on it
    - DD013's coupling table is incomplete
    - **Resolution:** Update DD013 Integration Contract to reference **all** science DDs it orchestrates

---

## Part 1: Inconsistencies (Contradictions Between DDs)

### I1. Data Access Layer: OWMeta (DD008) vs. cect (DD020)

**The Contradiction:**

| DD | Line | Statement |
|----|------|-----------|
| DD008 | 138 | "All modeling code MUST access biological data through OWMeta, not by parsing raw files." |
| DD008 | 372 | "OWMeta is **optional** (Phase 1). Direct file access is acceptable with documented provenance." |
| DD020 | 27 | "Never parse raw CSV/Excel connectome files directly — always use `cect`." |
| DD020 | 589-600 | "Phase 1-2: Use `cect` directly... Phase 3+: OWMeta calls `cect` internally." |

**DD008 contradicts itself** (line 138 says MUST, line 372 says optional). DD020 resolves this by phasing cect → OWMeta, but **DD008 doesn't acknowledge DD020's existence** (DD008 was written before DD020).

**Impact:**
Contributors don't know which API to use. DD001-DD009 reference "ConnectomeToolbox" but don't specify whether to use `cect` directly or wrap via OWMeta.

**Resolution:**
1. **Update DD008 (add phasing section):**
   ```markdown
   ## Phased OWMeta Mandate (Reconciliation with DD020)

   OWMeta and `cect` (DD020) serve complementary purposes:
   - **Phase 1-2 (now):** Use `cect` directly for connectome data (DD020). OWMeta is optional for semantic queries.
   - **Phase 3+ (future):** OWMeta wraps `cect` internally. Consuming DDs can use either API.

   See DD020 for connectome data access policy.
   ```

2. **Update all science DDs' Integration Contracts:**
   Replace "OWMeta (DD008)" with "DD020 (Connectome Data via cect)" in Input tables

---

### I2. Validation Status: DD010 (Optimistic) vs. DD021 (Realistic)

**The Contradiction:**

| DD | Line | Statement |
|----|------|-----------|
| DD010 | 447 | "Implementation Status: **Partial** (toolbox exists, automation incomplete)" |
| DD021 | 27 | "The toolbox is **dormant** (last commit: January 16, 2020 — 6 years ago) with 28 open issues and **broken Python 3.12 compatibility**... **Without a working analysis toolbox, Tier 3 validation is impossible**" |

DD010 implies the toolbox is usable but needs CI hookup. DD021 reveals it's **completely broken** (doesn't even import on modern Python).

**Impact:**
DD010's acceptance criteria (Tier 3 behavioral validation) **cannot currently be enforced**. DD013's CI/CD pipeline has unimplemented steps. Contributors attempting Tier 3 validation will fail.

**Resolution:**
1. **Update DD010 Implementation Status:**
   ```markdown
   **Implementation Status:** Partial
   - Tier 1 validation: Scripts exist but not automated
   - Tier 2 validation: Randi 2023 data needs ingestion (DD008)
   - **Tier 3 validation: BLOCKED** — Analysis toolbox is dormant (see DD021 revival plan)
   ```

2. **Make DD021 revival a Phase A blocker in DD013 roadmap**

---

### I3. Simulation Stack Backend Support: Config (DD013) vs. Reality (DD003)

**The Contradiction:**

| DD | Line | Statement |
|----|------|-----------|
| DD013 | 133 | `body.backend: opencl` with options `opencl, taichi-metal, taichi-cuda, pytorch` |
| DD003 | 354-360 | Taichi Metal/CUDA are "Experimental"; OpenCL is "Stable" |
| DD013 | 50 | "What Actually Runs Today... Step 3... Sibernetic simulates body physics" (implies OpenCL only) |

Config suggests 4 backends work. DD003 says 2 are experimental. DD013's reality check says only OpenCL actually runs.

**Impact:**
Contributors might set `body.backend: taichi-metal` and expect it to work (it might not).

**Resolution:**
1. **Update DD013 openworm.yml schema with status annotations:**
   ```yaml
   body:
     backend: opencl  # opencl (stable), taichi-metal (experimental), taichi-cuda (experimental), pytorch (reference only)
   ```

2. **Add runtime backend validation:**
   ```python
   # In master_openworm.py
   if config['body']['backend'] in ['taichi-metal', 'taichi-cuda']:
       logging.warning("Taichi backends are experimental (DD003). Use opencl for production.")
   ```

---

### I4. DD014 Companions Numbering (DD014.1/b vs. DD014.1/DD014.2)

**The Issue:**
DD014.1 and DD014.2 are **companion documents** to DD014, not standalone DDs. The "a/b" suffix is informal and doesn't appear in other DDs (no DD001a, DD002a, etc.).

**Impact:**
- Inconsistent numbering scheme
- Cross-references use "DD014.1" which looks like a typo
- Index/README tables need special cases for companion DDs

**Resolution:**
**Option A:** Renumber to DD014.1 (Visual Rendering) and DD014.2 (Mesh Deformation)
**Option B:** Fold into DD014 as sections (single 2000-line mega-DD)
**Option C:** Keep as-is but document the companion convention in DD012

**Recommendation:** **Option A** (renumber to .1/.2). Signals they're subordinate to DD014, consistent with software versioning conventions.

---

### I5. Parameter Sources: DD001 (Boyle & Cohen) vs. DD002 (Also Boyle & Cohen)

**The Confusion:**
DD001 line 179 says neuron channel kinetics are "derived from Boyle & Cohen 2008 **muscle model**."
DD002 line 4 says muscle model is "based on Boyle & Cohen 2008."

Both neurons AND muscles use parameters from the same paper about muscle electrophysiology.

**This is actually correct** (not a contradiction), but it's confusing:
- Boyle & Cohen measured body wall **muscle** ion channels
- DD001 borrowed those parameters for **neurons** because no neuron-specific data existed
- DD002 uses the muscle parameters for muscles (original purpose)

**Impact:**
Reads like circular logic. Contributors might think it's an error.

**Resolution:**
**Update DD001 line 179 to clarify:**
```markdown
**Ion channels (derived from Boyle & Cohen 2008 muscle model):**

NOTE: We currently use muscle channel kinetics for neurons because direct neuronal
electrophysiology is scarce. This is biologically inaccurate but the best available
starting point. DD005 (Cell-Type Differentiation) will replace generic parameters
with neuron-class-specific conductances derived from CeNGEN expression data.
```

---

## Part 2: Gaps (Missing Coverage)

### G1. Missing Scripts / Phantom GitHub Issues (CRITICAL)

**The Pattern:**
Almost every science DD (DD001, DD002, DD003, DD005, DD006, DD007, DD009, DD018, DD019, DD021) marks validation/coupling scripts as `[TO BE CREATED]` with tracking like:

```markdown
| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/extract_trajectory.py` | `[TO BE CREATED]` | openworm/c302#TBD |
```

**But `#TBD` is not a real GitHub issue number.** The issues don't exist.

**Count of missing scripts:**
- DD001: 3 scripts
- DD002: 2 scripts
- DD003: 2 scripts
- DD005: 5 scripts
- DD006: 3 scripts
- DD007: 4 scripts
- DD009: 8 scripts
- DD014.2: 9 scripts
- DD018: 6 scripts
- DD019: 7 scripts
- DD021: 0 (toolbox itself is the issue)

**Total: ~50 missing scripts across 10 DDs.**

**Impact:**
- Contributors can't discover or claim this work (no issues to browse)
- No one owns creating these scripts
- Implementation roadmaps reference scripts that don't exist

**Resolution:**
1. **Immediate:** Run DD015's `dd_issue_generator.py` (if it exists) to create GitHub issues from all Integration Contracts
2. **If script doesn't exist:** Create it as first DD015 task
3. **Label all generated issues:** `dd###`, `ai-workable` or `human-expert`, difficulty level (`L1`/`L2`/`L3`)
4. **Update all DDs:** Replace `#TBD` with actual issue numbers after creation

---

### G2. No DD for Environment / Boundary Conditions

**What's Missing:**
Multiple DDs reference "environment" but no DD specifies it:

| DD | Reference | What It Mentions |
|----|-----------|------------------|
| DD003 | Line 293 | "Environmental complexity: flat surface, infinite medium. Realistic soil mechanics, bacterial food, geometric obstacles out of scope." |
| DD019 | Line 676 | "Environmental mechanics beyond flat agar: Soil, bacterial lawns, geometric obstacles, microfluidic channels." |
| DD018 | Line 543 | "Food-dependent modulation: Egg-laying rate varies with food availability. Environmental coupling is future work." |

**What's Needed:**
A DD that specifies:
- Substrate types (agar stiffness, liquid viscosity, soil particle dynamics)
- Chemical gradient delivery (NaCl, diacetyl, attractants/repellents)
- Temperature gradient (thermotaxis)
- Geometric obstacles (pillars, channels, barriers)
- Bacterial lawns (OP50, food availability, consumption mechanics)
- Light (phototaxis — *C. elegans* has photosensory neurons)

**Resolution:**
**Create DD022: Environmental Modeling and Stimulus Delivery**

Scope:
- Substrate mechanics (couples to DD003 boundary particles)
- Chemical/thermal gradient fields (couples to DD019/DD017 Component 4 sensory transduction)
- Food particle dynamics (couples to DD007 pharyngeal pumping)
- Geometric environment (microfluidic channels for validation)

---

### G3. No DD for Cuticle Fine Structure

**What's Missing:**
Cuticle is mentioned in 5 DDs but never fully specified:

| DD | Reference | What It Mentions |
|----|-----------|------------------|
| DD003 | Line 290 | "Cuticle fine structure: basal, medial, cortical layers with distinct mechanical properties. Homogeneous elastic particles used. Phase 4 work." |
| DD004 | Line 144-148 | Cuticle elasticity multipliers (5x basal, 3x medial, 10x cortical) but no implementation |
| DD014.1 | Line 263 | Cuticle opacity 0.85, roughness 0.3, subsurface scattering — visual only, not mechanical |
| DD019 | Line 595 | "Detailed cuticle layer mechanics... homogeneous elastic particles sufficient for DD019." |

**The Gap:**
Cuticle mechanical properties (3 layers, anisotropy, annuli, alae) are deferred to "Phase 4" but never get their own DD.

**Resolution:**
**Option A:** Fold into DD004 (Mechanical Cell Identity) — cuticle layers are a special case of cell-type-specific mechanics
**Option B:** Create DD023: Cuticle Microstructure and Mechanical Anisotropy (if detailed enough to warrant standalone DD)

**Recommendation:** **Option A** (fold into DD004). Cuticle is acellular but can use the same particle-tagging + elasticity-multiplier system.

---

### G4. No DD for Proprioceptive Feedback (Motor Neuron Stretch Receptors)

**What's Missing:**
DD019 line 579: "Proprioceptive feedback via stretch receptors on motor neurons (Wen et al. 2012). Deferred to future DD."

DD019 line 583: "Motor neuron proprioception could be DD020."

**But DD020 is Connectome Data Access**, not proprioception.

**The Gap:**
Proprioceptive feedback is important for undulatory locomotion (Wen et al. 2012 showed B-class motor neurons have stretch-sensitive currents). This is a separate feedback loop from touch (DD019) and likely needed for stable crawling.

**Resolution:**
**Create DD023: Proprioceptive Feedback and Motor Coordination**
(Or DD022 if environment takes DD022)

Scope:
- Stretch-sensitive channels on B-class motor neurons
- Coupling to body deformation (strain readout from DD003)
- Effect on locomotion wave propagation
- Validation against Wen et al. 2012 behavioral data

---

### G5. No DD for Chemosensory / Thermosensory / Other Sensory Modalities

**What's Missing:**
DD019 (Touch Response) is the only mechanistic sensory transduction DD. But it explicitly scopes out:

| Sensory Modality | Neurons | Current State |
|-----------------|---------|---------------|
| **Touch** | ALM, AVM, PLM, PVD | **DD019** (MEC-4 channel model) |
| **Chemosensation (NaCl)** | ASEL, ASER | No DD; DD017 Component 4 (learned model) deferred |
| **Thermosensation** | AFD, AIY, AIZ | No DD; DD017 Component 4 deferred |
| **Olfaction** | AWC, AWA | No DD |
| **Nociception (chemical)** | ASH | No DD |
| **Oxygen sensing** | URX, AQR, PQR | No DD |

DD017 Component 4 proposes a **learned sensory transduction model** (ML-based, black box). But there's no mechanistic DD for any non-touch sensory modality.

**The Gap:**
Closed-loop chemotaxis, thermotaxis, and oxygen avoidance require sensory transduction models. DD019 establishes the **pattern** (stimulus → channel → neuron → behavior), but each modality needs its own DD.

**Resolution:**
**Defer to Phase 3+** but acknowledge the gap. Could create:
- DD024: Chemosensory Transduction (ASEL/ASER, cGMP signaling)
- DD025: Thermosensory Transduction (AFD, cGMP signaling)
- DD026: Olfactory Transduction (AWC/AWA, odorant receptors)

Or create a **single comprehensive DD: Sensory Transduction Suite** covering all modalities.

---

### G6. No DD for Male-Specific Modeling

**What's Missing:**
Cook et al. 2019 mapped the male connectome (385 neurons, +83 male-specific). DD020 includes `Cook2019MaleReader`. But no DD specifies how to model:

- Male-specific neurons (83 cells)
- Mating circuit (ray neurons, spicule muscles, HOB sensory neurons)
- Male tail anatomy (fan, rays, spicules)
- Copulation behavior

DD018 line 538: "Male-specific mating circuit: ray neurons, spicule muscles... This DD covers hermaphrodite egg-laying only."

**The Gap:**
Male modeling is Phase 6+ work, but there's no placeholder DD or even a proposal outline.

**Resolution:**
**Acknowledge in Phase 6 roadmap** (when created) but don't block current work. If a contributor proposes male modeling, they'd write **DD027: Male-Specific Neural Circuits and Copulation Behavior** via DD012 RFC process.

---

### G7. No DD for Developmental Modeling (Beyond Connectome Data)

**What's Scattered Across DDs:**

| DD | Reference | What It Mentions |
|----|-----------|------------------|
| DD004 | Line 227 | "Developmental stage transitions: Cell boundaries change (L1-adult). Adult hermaphrodite reference. Multi-stage support future work." |
| DD005 | Line 397 | "Developmental stage differences: CeNGEN L4 reference. L1, adult, dauer require separate expression datasets." |
| DD020 | Line 424-434 | Witvliet developmental series (8 stages, L1-adult) with 8 different `cect` readers |
| DD018 | Line 675 | "Developmental changes: Body size, shape change (L1-L4-adult). Assumes fixed adult. Phase 6 work." |
| DD007 | Line 280 | "Developmental changes in muscle properties: L1 vs. adult. Phase 6 work." |

**The Gap:**
Developmental connectomes exist (Witvliet 1-8). CeNGEN L1 expression exists. But no DD specifies:
- How to simulate neuron birth/death during development
- Body size scaling (L1 is ~240 µm, adult is ~1000 µm)
- Stage-specific validation targets (L1 locomotion is different from adult)
- Integration with DD001-DD003 (which assume fixed adult)

**Resolution:**
**Create DD (future): Developmental Modeling Framework**

Placeholder entry for Phase 6. Not needed now, but the gap should be acknowledged.

---

### G8. No Master Phase Roadmap Document

**The Problem:**
Phase numbers appear in DDs but there's no master document defining what each phase is:

| DD | Phase | Why Assigned to This Phase |
|----|-------|---------------------------|
| DD005 | Phase 1 | "First DD to produce biologically distinct neurons" |
| DD006 | Phase 2 | "Slow modulation layer" |
| DD007, DD009, DD018 | Phase 3 | "Organ systems" |
| DD004 | Phase 4 | "Mechanical cell identity" |
| DD017 | Phase 3-4 | "Hybrid ML" (unclear — listed as Phase 3-4 in status) |
| DD019 | Phase 2-3 | "Closed-loop touch" (ambiguous) |

DD013 has a roadmap (Phase A-D) but these are **implementation phases** (infrastructure work), not **modeling phases** (science DDs).

**The Gap:**
No single source of truth for "What is Phase 1? Which DDs belong to it? What's the timeline?"

**Resolution:**
**Create `DD_PHASE_ROADMAP.md`** in design_documents/ directory:

```markdown
# OpenWorm Modeling Phase Roadmap

## Phase 0: Foundation (Existing, Accepted)
- DD001 (Neural), DD002 (Muscle), DD003 (Body Physics)
- DD008 (OWMeta partial), DD010 (Validation partial)
- DD020 (Connectome via cect), DD021 (Toolbox — needs revival)

## Phase A: Infrastructure (Weeks 1-4, Parallel with Phase 1)
- DD013 (Simulation Stack)
- DD021 (Toolbox Revival)
- DD012 (RFC Process)
- DD011 (Contributor Progression)

## Phase 1: Cell-Type Differentiation (Months 1-3)
- DD005 (128 neuron classes from CeNGEN)
- DD014 Phase 1 (Post-hoc Trame viewer, organism + tissue scales)

## Phase 2: Slow Modulation + Closed-Loop (Months 4-6)
- DD006 (Neuropeptides — 31,479 interactions)
- DD019 (Touch Response — MEC-4, bidirectional coupling)
- DD014 Phase 2 (Interactive viewer, layers, cell selection)

## Phase 3: Organ Systems (Months 7-12)
- DD007 (Pharynx — 63 cells, pumping)
- DD009 (Intestine — 20 cells, defecation)
- DD018 (Egg-Laying — 28 cells, two-state)
- DD017 (Hybrid ML — differentiable backend, surrogates)

## Phase 4: Mechanical Cell Identity (Months 13-18)
- DD004 (Per-particle cell IDs, 959 cells)
- DD014.2 (Mesh deformation — cage-based, PBD collision)

## Phase 5: Intracellular Signaling (Months 19-24+)
- [To be written] — IP3/cAMP/MAPK cascades, detailed GPCR biochemistry

## Phase 6: Developmental Modeling (Year 2+)
- [To be written] — Multi-stage simulation, neuron birth/death, body growth

## Phase 7: Male-Specific / Advanced (Year 3+)
- [To be written] — Male connectome, mating circuit, copulation
```

---

### G9. No Master Coupling Map / Integration Diagram

**The Problem:**
Every DD has local coupling tables:

```markdown
| I Depend On | DD | What Breaks If They Change |
```

But there's no **global view** of all coupling dependencies.

**Impact:**
- Can't visualize the full coupling graph
- Can't identify bottleneck DDs (which DD is depended on by the most others?)
- Can't plan integration order (which DDs must be implemented first to unblock others?)

**Resolution:**
**Create `INTEGRATION_MAP.md`** with:

1. **Graphviz/Mermaid coupling diagram:**

```mermaid
graph TD
    DD020[DD020: Connectome Data] --> DD001[DD001: Neural]
    DD001 --> DD002[DD002: Muscle]
    DD002 --> DD003[DD003: Body Physics]
    DD001 --> DD005[DD005: Cell Differentiation]
    DD005 --> DD006[DD006: Neuropeptides]
    DD003 --> DD004[DD004: Cell Identity]
    DD001 --> DD007[DD007: Pharynx]
    DD001 --> DD009[DD009: Intestine]
    DD001 --> DD018[DD018: Egg-Laying]
    DD003 --> DD019[DD019: Touch]
    DD001 --> DD019
    DD001 --> DD010[DD010: Validation]
    DD003 --> DD010
    DD021[DD021: Movement Toolbox] --> DD010
    DD001 --> DD013[DD013: Integration]
    DD002 --> DD013
    DD003 --> DD013
    DD001 --> DD014[DD014: Visualization]
    DD002 --> DD014
    DD003 --> DD014
    DD004 --> DD014
    DD005 --> DD014
    DD006 --> DD014
    DD007 --> DD014
    DD009 --> DD014
    DD018 --> DD014
    DD019 --> DD014
    DD014 --> DD014.1[DD014.1: Visual Rendering]
    DD003 --> DD014.2[DD014.2: Mesh Deformation]
    DD001 --> DD017[DD017: Hybrid ML]
    DD002 --> DD017
    DD003 --> DD017
    DD005 --> DD017
```

2. **Bottleneck analysis table:**

| DD | Depended On By (count) | Critical? |
|----|----------------------|-----------|
| DD001 (Neural) | 11 DDs | ✅ CRITICAL — touches everything |
| DD003 (Body Physics) | 7 DDs | ✅ CRITICAL — all mechanical coupling |
| DD020 (Connectome) | 9 DDs | ✅ CRITICAL — data foundation |
| DD021 (Toolbox) | 1 DD (DD010) | ⚠️ BLOCKING — Tier 3 validation impossible without it |
| DD013 (Integration) | 0 DDs | ℹ️ LEAF — consumes all, produces nothing (orchestrator) |
| DD014 (Visualization) | 0 DDs | ℹ️ LEAF — consumes all outputs, no one depends on it |

**Auto-generate this file** from DD Integration Contract tables (parse all DDs, extract coupling dependencies, build graph).

---

### G10. Missing Owner Assignments for Phase A Tasks

**The Gap:**
DD013 and DD021 have detailed task roadmaps with effort estimates, but **many have "Owner: TBD"** or reference vacant roles:

| Task | Stated Owner | Reality |
|------|-------------|---------|
| DD013 Phase A (8 tasks) | "Integration Maintainer" | **Role is vacant** (DD011) |
| DD021 Revival (8 tasks) | "Validation L4" | **Role is vacant** (DD011) |
| DD014 Phase 1 (9 tasks) | "Visualization L4" | **Role is vacant** (DD011) |

**Impact:**
Roadmaps exist but no one owns executing them.

**Resolution:**
1. **Immediate:** Founder assigns Phase A tasks to existing L3+ contributors (even if not L4)
2. **Medium-term:** Recruit L4 maintainers for Integration, Validation, Visualization
3. **Update DD011 Subsystem Ownership Map** when filled

---

### G11. DD005 CeNGEN Calibration Training Data Is Underspecified

**The Gap:**
DD005 line 442-448 lists ~5 neuron types with electrophysiology (ALM, AVM, PLM, AVA, RIM, ASH, AWC). But:
- No table of actual measured conductances
- No data files specified
- No DOIs for source papers beyond general citations

Line 185: "Fit a scaling relationship... using the ~20 neuron types with published patch-clamp"

**But only 5-7 are actually listed.**

**Impact:**
A contributor implementing DD005 doesn't know:
- Where to get the training data
- What the measured conductance values are
- Which 20 neurons (only 5-7 are named)

**Resolution:**
**Update DD005 with:**
1. **Complete training set table:**

```markdown
### Calibration Dataset (Complete List)

| Neuron | Channel | Measured g_max | E_rev | Source Paper | DOI |
|--------|---------|---------------|-------|-------------|-----|
| ALM | MEC-4 | 20 nS | +10 mV | O'Hagan et al. 2005 | 10.1038/nn1356 |
| AVA | Leak | ... | ... | Lockery lab (year?) | ... |
| ...  | ... | ... | ... | ... | ... |
```

2. **Data file location:**
```markdown
Calibration data CSV: `c302/data/electrophysiology_training_set.csv`
Format: neuron_class, channel, measured_g, E_rev, source_doi
```

---

### G12. Missing Integration Between DD015 (AI Contributor Model) and DD011 (Badges)

**The Gap:**
DD015 says "AI agents earn the same badges as human contributors" but doesn't specify:
- Does N2-Whisperer verify AI agent badge completion differently?
- Do AI agents get BadgeList profiles? (human-facing platform)
- Can AI agents earn teach-back badges? (No — those are sponsor-only per DD011)

DD011 extensively covers teach-back badges (for human sponsors) but DD015 mentions them only briefly.

**Resolution:**
**Update DD015 Section 1.3** to cross-reference DD011 §Badge & Recognition System completely:

```markdown
### 1.3 Badge Earning (Cross-Reference to DD011)

AI agents earn badges from the same pool as human contributors, with one exception:

**Badges AI agents CAN earn:** (see DD011 for full definitions)
- Orientation badges (Connected, Simulation Runner, Explorer, Paper Reader)
- Skill badges (Neuron Modeling Foundations, Data Wrangler, GitHub Proficient, etc.)
- Domain badges (Neural Circuit Contributor, Muscle Model Contributor, etc.)
- Milestone badges (First PR, Tenacious, Centurion, etc.)
- Community badges (Reviewer — if agent reviews L1 PRs)

**Badges AI agents CANNOT earn:**
- Teach-Back badges (I Understand Neurons, etc.) — these are **human sponsor only**

See DD011 §Teach-Back Badges (lines 392-410) for complete sponsor learning framework.
```

---

## Part 3: Redundancies (Overlapping or Duplicated Coverage)

### R1. Integration Contract Sections in Every DD (High Maintenance Burden)

**The Pattern:**
DD001-DD021 (21 DDs) all include full Integration Contract sections with 5 required sub-sections (DD012 lines 119-159):
- Inputs / Outputs
- Repository & Packaging
- Configuration
- How to Test
- How to Visualize
- Coupling Dependencies

**The Cost:**
If DD012 adds a 6th required sub-section, **all 21 DDs must be updated**. If `openworm.yml` schema changes (DD013), all DD config sections must be updated.

**Is This Bad?**
**Not necessarily.** The redundancy provides **locality** — a contributor working on DD006 can read everything about DD006 in one place without jumping to DD013 for config schema or DD014 for visualization.

**Trade-off:**
- **Locality (good):** Each DD is self-contained
- **Maintenance burden (bad):** Changes to Integration Contract format ripple across 21 DDs

**Recommendation:**
**Keep the redundancy** but add tooling to reduce maintenance cost:

1. **Auto-generate parts of Integration Contracts:**
   - `versions.lock` entry (extract from DD013)
   - Docker stage (extract from DD013 Dockerfile)
   - Test commands (templated from DD013)

2. **Validation script:**
   ```bash
   # Checks that all DDs' Integration Contracts match DD012 template
   python scripts/validate_integration_contracts.py design_documents/*.md
   # Flags: Missing sub-sections, inconsistent formatting
   ```

---

### R2. Repository URLs Repeated (Minor)

**The Pattern:**
`openworm/c302` is hyperlinked in DD001, DD002, DD005, DD006, DD007, DD009, DD018, DD019 (8 DDs).
`openworm/sibernetic` is hyperlinked in DD002, DD003, DD004, DD007, DD019 (5 DDs).

**Impact:**
If the repo moves (e.g., rename to `openworm/CElegansNeuroML`), must update 8 links.

**Resolution:**
**Use markdown reference-style links** at bottom of each DD or globally:

```markdown
[c302]: https://github.com/openworm/c302
[sibernetic]: https://github.com/openworm/sibernetic

<!-- Then in body -->
Repository: [c302] — issues labeled `dd001`
```

**Benefit:** Change URL once, all references update.

**Recommendation:** **Low priority** — current approach works fine, this is a minor optimization.

---

### R3. Quality Criteria Overlap with DD010

**The Pattern:**
Every science DD (DD001-DD009, DD018-DD019) has a "Quality Criteria" section. DD010 defines global validation tiers. Some overlap:

| DD | Quality Criterion | DD010 Equivalent |
|----|------------------|------------------|
| DD001 line 253 | "Kinematic validation score... within 15%" | Tier 3 acceptance: ±15% |
| DD002 line 237 | "Kinematic validation scores... not degrade" | Tier 3 (same) |
| DD005 line 347 | "Must improve correlation with Randi 2023" | Tier 2 functional connectivity |

**Is This Bad?**
**No, this is good redundancy.** It reinforces that DD-specific criteria align with global validation (DD010). Each DD is explicit about its validation requirements.

**Recommendation:** **Keep it.** The redundancy is intentional and helpful.

---

### R4. Docker/Config Repeated (Acceptable)

**The Pattern:**
Every DD specifies its Docker stage, `openworm.yml` keys, and `versions.lock` entry. This info is also centralized in DD013.

**Is This Bad?**
**No.** Same locality vs. centralization trade-off as R1. The repetition is acceptable because:
- Contributors working on DD006 can see DD006's config without jumping to DD013
- If DD013's schema changes, affected DDs update their local copies
- Validation script can catch inconsistencies

**Recommendation:** **Keep it** + add validation:

```bash
# Verify all DD config sections match DD013's openworm.yml schema
python scripts/validate_dd_configs.py design_documents/*.md
```

---

## Part 4: Better Ordering / Grouping

### Current Organization (from README.md)

The README groups DDs as:

1. **Core Architecture** (DD001-DD003)
2. **Proposed Extensions** (DD004-DD009, DD018)
3. **Infrastructure** (DD008, DD010-DD013, DD020-DD021)
4. **Visualization** (DD014, DD014.1, DD014.2)
5. **AI/ML** (DD015, DD017)
6. **Archived** (DD016)

**Problems with this grouping:**
- Mixes **status** (Accepted vs. Proposed) with **category** (Architecture vs. Infrastructure)
- Phase progression unclear (DD005 is Phase 1, DD006 is Phase 2, but both are in "Proposed Extensions")
- Dependencies not visible (DD020 feeds DD001, but DD020 is in "Infrastructure" while DD001 is in "Core")

---

### Recommended Reorganization Option 1: By Dependency Layer (Data Flow)

This grouping shows **how data flows through the system** from foundational layers up to consumers.

**Layer 0: Governance & Process (Meta)**
- DD012 (Design Document RFC Process)
- DD011 (Contributor Progression Model)
- DD015 (AI-Native Contributor Model)

**Layer 1: Data Providers (Foundation)**
- DD020 (Connectome Data Access — `cect`)
- DD008 (Data Integration Pipeline — OWMeta, Phase 3+)
- DD021 (Movement Analysis Toolbox — WCON, validation data)

**Layer 2: Validation Framework**
- DD010 (3-Tier Validation)

**Layer 3: Core Simulation Chain (The Coupling Backbone)**
- DD001 (Neural Circuit) ← consumes DD020
- DD002 (Muscle Model) ← consumes DD001
- DD003 (Body Physics) ← consumes DD002

**Layer 4: Integration Orchestrator**
- DD013 (Simulation Stack) ← consumes DD001-DD003, DD010

**Layer 5: Extensions to Core**
- DD005 (Cell Differentiation) ← enhances DD001
- DD006 (Neuropeptides) ← adds to DD001
- DD004 (Mechanical Cell Identity) ← enhances DD003
- DD019 (Touch Response) ← closes loop DD003 → DD001

**Layer 6: Organ Systems (Semi-Independent Subsystems)**
- DD007 (Pharyngeal System)
- DD009 (Intestinal Oscillator)
- DD018 (Egg-Laying System)

**Layer 7: Visualization (Consumes All Outputs)**
- DD014 (Dynamic Visualization Architecture)
- DD014.1 (Visual Rendering Specification)
- DD014.2 (Anatomical Mesh Deformation Pipeline)

**Layer 8: Advanced/Hybrid (Future)**
- DD017 (Hybrid Mechanistic-ML Framework)

**Archived:**
- DD016 (Tokenomics)

**Benefits:**
- Shows data flow clearly
- Dependency order visible (implement Layer 1 before Layer 3)
- Integration (DD013) is correctly placed as orchestrator that consumes Layers 1-3

---

### Recommended Reorganization Option 2: By Implementation Phase (Timeline)

This grouping shows **when each DD gets implemented** (matches Phase Roadmap from G8).

**Phase 0: Existing Foundation**
- DD001 (Neural — Accepted, working)
- DD002 (Muscle — Accepted, working)
- DD003 (Body Physics — Accepted, working)
- DD020 (Connectome — `cect` exists, needs pinning)

**Phase A: Infrastructure Bootstrap (Weeks 1-4, Prerequisite for All Phases)**
- DD013 (Simulation Stack — config, Docker, CI)
- DD021 (Toolbox Revival — 8 tasks, 33 hours)
- DD012 (RFC Process — governance)
- DD011 (Contributor Progression — levels, badges)

**Phase 1: Cell Differentiation (Months 1-3)**
- DD005 (128 neuron classes from CeNGEN)
- DD014 Phase 1 (Trame viewer, organism + tissue)
- DD010 Tier 2 validation (functional connectivity)

**Phase 2: Slow Modulation + Closed-Loop (Months 4-6)**
- DD006 (Neuropeptides — 31,479 interactions)
- DD019 (Touch Response — bidirectional coupling)
- DD014 Phase 2 (Interactive layers, cell selection)

**Phase 3: Organ Systems + Hybrid ML (Months 7-12)**
- DD007 (Pharynx — 63 cells)
- DD009 (Intestine — 20 cells)
- DD018 (Egg-Laying — 28 cells)
- DD017 (Differentiable backend, SPH surrogate)

**Phase 4: Mechanical Detail (Months 13-18)**
- DD004 (Cell Identity — 959 cells)
- DD014.2 (Mesh Deformation — cage-based)
- DD014 Phase 3 (Public experience, molecular scale)

**Phase 5-6: Future (Not Yet Specified)**
- Intracellular signaling (IP3/cAMP cascades)
- Developmental modeling (Witvliet series)
- Male-specific modeling

**Governance (Ongoing):**
- DD015 (AI Contributors — can deploy anytime after DD011/DD012)

**Archived:**
- DD016 (Tokenomics — backburner)

**Benefits:**
- Clear implementation order
- Timeline visible
- Phase dependencies explicit (Phase 2 requires Phase 1, etc.)

---

### Recommendation: Use Option 2 (By Phase) in README, Option 1 (By Layer) in INTEGRATION_MAP.md

**README.md:** Timeline-based grouping (what to implement when)
**INTEGRATION_MAP.md:** Dependency-layer grouping (what depends on what)

Both views are useful for different purposes.

---

## Part 5: Detailed Inconsistency Matrix

| # | Inconsistency | DDs Involved | Severity | Proposed Resolution |
|---|---------------|-------------|----------|---------------------|
| I1 | OWMeta (MUST use) vs. cect (MUST use) data access | DD008 vs DD020 | 🔴 Major | Update DD008: acknowledge DD020 phasing (cect Phase 1-2, OWMeta wraps cect Phase 3+) |
| I2 | Toolbox "partial" vs. "completely broken" | DD010 vs DD021 | 🔴 Major | Update DD010: mark Tier 3 as BLOCKED, reference DD021 revival |
| I3 | Backend options (4 listed) vs. reality (1 stable) | DD013 vs DD003 | 🟡 Moderate | Annotate DD013 config: opencl (stable), others (experimental) |
| I4 | Boyle & Cohen used for both neurons and muscles | DD001 vs DD002 | 🟢 Minor | Clarify DD001: muscle params used for neurons due to data scarcity |
| I5 | DD014 Phase 1 scope (molecular scale yes/no?) | DD014 vs DD014.1 | 🟡 Moderate | Clarify DD014 roadmap: molecular is Phase 3 only |
| I6 | DD005 "~20 neuron electrophysiology" but only 5-7 listed | DD005 internal | 🟡 Moderate | Expand training set table with all 20, or correct to "~7" |
| I7 | DD008 "dormant since Jul 2024" but marked Accepted | DD008 status | 🟢 Minor | Update status to "Accepted (with dormant components)" |
| I8 | DD019 says proprioception "could be DD020" but DD020 is connectome | DD019 line 583 | 🟢 Minor | Fix typo: "could be DD023" or "future DD" |

---

## Part 6: Detailed Gap Matrix

| # | Gap | Area | Priority | Proposed Resolution |
|---|-----|------|----------|---------------------|
| G1 | ~50 missing scripts marked `[TO BE CREATED]` with no GitHub issues | DD001-DD009, DD018-DD019, DD021 | 🔴 Critical | Run dd_issue_generator.py, create issues, update DDs with real issue numbers |
| G2 | No DD for Environment / Boundary Conditions / Stimulus Delivery | Multiple DDs reference but none specify | 🟡 Moderate | Create DD022: Environmental Modeling (substrates, gradients, obstacles, food) |
| G3 | No DD for Cuticle Fine Structure (3 layers, anisotropy) | DD003, DD004, DD014.1, DD019 | 🟡 Moderate | Fold into DD004 or create DD023 |
| G4 | No DD for Proprioceptive Feedback (motor neuron stretch receptors) | DD019 scopes out | 🟡 Moderate | Create DD023 or DD024: Proprioceptive Feedback (Wen et al. 2012) |
| G5 | No DDs for Chemosensory / Thermosensory / Olfactory Transduction | DD019 scopes out, DD017 defers | 🟡 Moderate | Phase 3+ work; defer until DD019 mechanistic approach validated |
| G6 | No DD for Male-Specific Modeling (385 neurons, mating circuit) | DD018, DD020 | 🟢 Low (Phase 6+) | Acknowledge in Phase 6 roadmap when created |
| G7 | No DD for Developmental Modeling Framework | DD004, DD005, DD020 | 🟢 Low (Phase 6+) | Create placeholder DD for Phase 6 |
| G8 | No Master Phase Roadmap | Multiple DDs | 🔴 Critical | Create DD_PHASE_ROADMAP.md |
| G9 | No Master Coupling Map / Integration Diagram | All DDs | 🔴 Critical | Create INTEGRATION_MAP.md with dependency graph |
| G10 | Missing owner assignments for Phase A tasks | DD013, DD021, DD014 | 🔴 Critical | Founder assigns tasks to existing contributors or recruits L4 maintainers |
| G11 | DD005 calibration training set underspecified | DD005 | 🟡 Moderate | Add complete table of 20 neurons with measured conductances, DOIs, data file locations |
| G12 | DD015/DD011 badge integration unclear | DD015, DD011 | 🟢 Minor | Cross-reference DD011 §Badge system in DD015 |
| G13 | No DD for Gonad/Reproductive System Mechanics (beyond egg-laying) | DD018 | 🟢 Low (Phase 5+) | Defer; acknowledge in DD018 boundaries |
| G14 | No DD for Sensory-Motor Integration (beyond touch) | DD019 | 🟡 Moderate | Phase 3 work; DD019 establishes pattern |
| G15 | No DD for Multi-Worm Simulation (social behavior, aggregation) | None | 🟢 Low (Phase 7+) | Not on current roadmap |

---

## Part 7: Recommended Master Index Structure

### Proposed: Dual-Index System

**README.md** (Timeline View — For Contributors):
*"What should I implement and when?"*

```markdown
# OpenWorm Design Documents

## How to Navigate This Directory

- **By Phase:** See implementation timeline below
- **By Dependency:** See INTEGRATION_MAP.md for coupling diagram
- **By Topic:** See topical index below
- **Template:** See DD012 (RFC Process) for DD template; DD005 for reference implementation

---

## Implementation Timeline (Phase-Based Organization)

### Phase 0: Existing Foundation (Accepted, Working)

| DD | Title | Status | What It Does |
|----|-------|--------|--------------|
| DD001 | Neural Circuit Architecture | ✅ Accepted | 302 neurons, HH Level C1, graded synapses |
| DD002 | Muscle Model Architecture | ✅ Accepted | 95 muscles, Ca²⁺→force coupling |
| DD003 | Body Physics Architecture | ✅ Accepted | Sibernetic SPH, PCISPH, ~100K particles |
| DD020 | Connectome Data Access | ✅ Accepted (pinning needed) | `cect` API, Cook2019Herm default |

### Phase A: Infrastructure Prerequisites (Weeks 1-4)

**MUST complete before modeling phases can proceed.**

| DD | Title | Status | Blocking | What It Does |
|----|-------|--------|----------|--------------|
| DD013 | Simulation Stack Architecture | ⚠️ Proposed | **CRITICAL** | `openworm.yml`, multi-stage Docker, CI/CD, Integration Maintainer role |
| DD021 | Movement Toolbox & WCON Policy | ⚠️ Proposed (revival plan) | **Tier 3 validation** | Revive analysis toolbox, WCON 1.0 pin, 8 tasks (33 hours) |
| DD012 | Design Document RFC Process | ⚠️ Proposed | Governance | DD template, RFC workflow, Mind-of-a-Worm enforcement |
| DD011 | Contributor Progression Model | ⚠️ Proposed | Governance | L0-L5 levels, badge system, subsystem ownership |

### Phase 1: Cell-Type Differentiation (Months 1-3)

| DD | Title | Dependencies | What It Does |
|----|-------|-------------|--------------|
| DD005 | Cell-Type Differentiation Strategy | DD001, DD008/DD020 | 128 neuron classes from CeNGEN, expression→conductance calibration |
| DD014 (Phase 1) | Post-Hoc Trame Viewer | DD001-DD003, DD005 | Evolve Worm3DViewer to Trame, OME-Zarr export, organism + tissue scales |
| DD010 (Tier 2) | Functional Connectivity Validation | DD005, DD008 | Randi 2023 correlation target, blocking gate |

### Phase 2: Slow Modulation + Closed-Loop (Months 4-6)

| DD | Title | Dependencies | What It Does |
|----|-------|-------------|--------------|
| DD006 | Neuropeptidergic Connectome | DD001, DD005 | 31,479 peptide-receptor interactions, GPCR modulation, seconds timescale |
| DD019 | Closed-Loop Touch Response | DD001, DD003 | MEC-4 mechanotransduction, bidirectional coupling, tap withdrawal |
| DD014 (Phase 2) | Interactive Viewer | DD014 Phase 1 | Layers, time scrubbing, cell selection, validation overlay |

### Phase 3: Organ Systems + Hybrid ML (Months 7-12)

| DD | Title | Dependencies | What It Does |
|----|-------|-------------|--------------|
| DD007 | Pharyngeal System Architecture | DD001, DD002 | 63-cell semi-autonomous organ, 3-4 Hz pumping |
| DD009 | Intestinal Oscillator Model | DD001, DD004 (optional) | 20-cell IP3/Ca oscillator, 50s defecation period |
| DD018 | Egg-Laying System Architecture | DD001, DD002, DD005, DD006 | 28-cell reproductive circuit, HSN serotonergic command, two-state pattern |
| DD017 | Hybrid Mechanistic-ML Framework | DD001-DD005, DD010 | Differentiable backend, SPH surrogate, foundation model→params, learned sensory |

### Phase 4: Mechanical Cell Identity + Mesh Deformation (Months 13-18)

| DD | Title | Dependencies | What It Does |
|----|-------|-------------|--------------|
| DD004 | Mechanical Cell Identity | DD003, DD008 | Per-particle cell IDs, 959 somatic cells, cell-type-specific elasticity |
| DD014.2 | Anatomical Mesh Deformation | DD003, DD014 | GPU skinning, cage-based MVC, PBD collision for ~1.6M vertices |
| DD014 (Phase 3) | Public Experience Viewer | DD014 Phase 2 | Three.js + WebGPU, molecular scale, "Digital Organism In Your Browser" |

### Phase 5-6: Future (Not Yet Specified)

- Intracellular signaling cascades (IP3/cAMP/MAPK, detailed GPCR)
- Developmental modeling (Witvliet series, neuron birth/death)
- Male-specific modeling (385 neurons, mating circuit)
- Advanced sensory modalities (chemo, thermo, proprioception beyond touch)

### Governance & AI (Can Deploy Anytime After DD011/DD012)

| DD | Title | Dependencies | What It Does |
|----|-------|-------------|--------------|
| DD015 | AI-Native Contributor Model | DD011, DD012 | Autonomous AI agents, GitHub bot, Moltbook-inspired, sponsor knowledge profiles + teach-back |

### Archived / Backburner

| DD | Title | Status | Why Archived |
|----|-------|--------|--------------|
| DD016 | Tokenomics and Retroactive Funding | Backburner | WORM token, Base L2, retroactive public goods funding — deferred pending funding strategy decision |

---

## Topical Index (Cross-Reference)

**Neural Modeling:**
DD001 (architecture), DD005 (differentiation), DD006 (neuropeptides), DD007 (pharynx neurons), DD009 (no neurons, intestinal cells), DD018 (HSN, VC neurons)

**Muscle Modeling:**
DD002 (body wall), DD007 (pharyngeal muscles), DD018 (vulval/uterine muscles)

**Body Mechanics:**
DD003 (SPH), DD004 (cell identity), DD014.2 (mesh deformation), DD019 (strain readout)

**Sensory Transduction:**
DD019 (touch — MEC-4), DD017 Component 4 (learned, ML-based)

**Data Access:**
DD008 (OWMeta), DD020 (cect), DD021 (WCON)

**Validation:**
DD010 (framework), DD021 (toolbox)

**Integration:**
DD013 (simulation stack)

**Visualization:**
DD014 (architecture), DD014.1 (visual spec), DD014.2 (mesh deformation)

**Governance:**
DD011 (progression), DD012 (RFC), DD015 (AI)

**Hybrid/Advanced:**
DD017 (ML framework)
```

---

**INTEGRATION_MAP.md** (Dependency View — For Architects):
*"How does the system fit together?"*

```markdown
# OpenWorm Integration Map

## Purpose

This document visualizes **how all Design Documents couple together** — which DDs produce data, which consume it, and what breaks if coupling interfaces change.

Generated from: Integration Contract sections of DD001-DD021
Last updated: 2026-02-19

---

## Dependency Graph

[Insert Mermaid diagram from Part 4, Option 1]

---

## Bottleneck Analysis

| DD | Producers (count) | Consumers (count) | Criticality |
|----|------------------|------------------|-------------|
| **DD001** (Neural) | 1 (DD020) | 11 (DD002, DD005, DD006, DD007, DD009, DD010, DD013, DD014, DD017, DD018, DD019) | 🔴 CRITICAL BOTTLENECK |
| **DD003** (Body Physics) | 1 (DD002) | 7 (DD004, DD007, DD010, DD013, DD014, DD014.2, DD019) | 🔴 CRITICAL |
| **DD020** (Connectome) | 0 (external data) | 9 (DD001, DD002, DD005, DD006, DD007, DD013, DD017, DD018, DD019) | 🔴 CRITICAL FOUNDATION |
| **DD021** (Toolbox) | 0 (external data) | 1 (DD010 Tier 3) | 🟡 BLOCKING (for validation only) |
| **DD013** (Integration) | 10+ (all science DDs) | 0 (orchestrator, no one depends on it) | ℹ️ LEAF NODE |
| **DD014** (Visualization) | 10+ (all science DDs) | 0 (consumer only) | ℹ️ LEAF NODE |

---

## Coupling Chains (Data Flow Sequences)

### Chain 1: Neural → Muscle → Body → Validation (The Core Loop)

```
DD020 (connectome topology)
  ↓
DD001 (neural voltage/calcium)
  ↓
DD002 (muscle calcium → activation)
  ↓
DD003 (SPH forces → movement)
  ↓
DD021 (WCON kinematics)
  ↓
DD010 Tier 3 (behavioral validation)
```

### Chain 2: CeNGEN → Conductances → Functional Connectivity (Phase 1 Validation)

```
DD008/DD020 (CeNGEN expression data)
  ↓
DD005 (expression → conductance calibration)
  ↓
DD001 (differentiated neuron models)
  ↓
DD010 Tier 2 (functional connectivity vs. Randi 2023)
```

### Chain 3: Bidirectional Touch Loop (DD019 Closes the Loop)

```
DD003 (SPH elastic particles)
  ↓ (strain readout)
DD019 (MEC-4 channel on touch neurons)
  ↓
DD001 (neural circuit — touch → AVA → motor)
  ↓
DD002 (muscle activation)
  ↓
DD003 (SPH forces → body moves)
  ↓ (LOOP BACK TO STRAIN READOUT)
```

### Chain 4: All Outputs → Visualization

```
DD001, DD002, DD003, DD004, DD005, DD006, DD007, DD009, DD018, DD019
  ↓ (all export to OME-Zarr)
DD014 (OME-Zarr groups: neural/, muscle/, body/, pharynx/, intestine/, etc.)
  ↓
DD014.1 (color mapping, activity overlays)
  ↓
DD014.2 (mesh deformation from SPH particles)
  ↓
Viewer renders all subsystems in a single 3D scene
```

---

## Integration Interfaces (What Gets Exchanged)

| Producer DD | Consumer DD | Variable | Format | Coupling Script | Breakage Risk |
|------------|-------------|----------|--------|----------------|---------------|
| DD001 (Neural) | DD002 (Muscle) | `V_neuron`, `ca_neuron` | NeuroML state vars | Within same LEMS sim | 🟢 Low (tightly coupled) |
| DD002 (Muscle) | DD003 (Body) | `ca_muscle` → activation | Tab-separated file | `sibernetic_c302.py` | 🟡 Moderate (file format) |
| DD003 (Body) | DD019 (Sensory) | SPH particle positions → strain | Shared memory or file | `sibernetic_c302_closedloop.py` | 🔴 High (new bidirectional) |
| DD003 (Body) | DD021 (Toolbox) | Particle positions → skeleton | WCON file | WCON exporter in `master_openworm.py` | 🟡 Moderate (format compliance) |
| DD020 (Connectome) | DD001 (Neural) | Adjacency matrices | `cect` Python API | `c302` network generation | 🟢 Low (stable API) |
| DD005 (Cell Diff) | DD001 (Neural) | Per-class conductances | 128 `.cell.nml` files | `c302` reads when `differentiated: true` | 🟡 Moderate (file count) |
| DD010 Tier 3 | DD013 (CI) | Pass/fail + metrics | JSON report | CI script reads exit code | 🟡 Moderate (schema changes) |
| All science DDs | DD014 (Viz) | Time-varying state | OME-Zarr groups | `master_openworm.py` Step 4b export | 🔴 High (10+ producers) |

---

## Who Owns Integration? (Responsibility Matrix)

| Integration Boundary | Upstream DD | Downstream DD | Coupling Script Location | Owner |
|---------------------|------------|--------------|------------------------|-------|
| Neural → Muscle | DD001 | DD002 | NeuroML/LEMS (same sim) | Neural L4 (Padraig) |
| Muscle → Body | DD002 | DD003 | `sibernetic_c302.py` | Body Physics L4 (Andrey) + Integration L4 |
| Body → Sensory (new) | DD003 | DD019 | `sibernetic_c302_closedloop.py` | Body Physics L4 + Neural L4 |
| All → Visualization | DD001-DD019 | DD014 | `master_openworm.py` Step 4b | Integration L4 + Visualization L4 |
| Simulation → Validation | DD003 | DD021 | WCON exporter + toolbox | Integration L4 + Validation L4 |
| Connectome → All | DD020 | DD001+ | `cect` API | Data L4 (TBD) |

**Critical Finding:**
5 of 6 coupling boundaries require **Integration L4** — the vacant role identified in Finding #2.

---

## Recommended Actions for Integration Maintainer (When Filled)

### Week 1-2: Audit and Baseline
1. Clone all repos referenced in DDs (c302, Sibernetic, OWMeta, ConnectomeToolbox, Worm3DViewer)
2. Verify current coupling scripts exist and work (run coupled sim end-to-end)
3. Document current state: which couplings work, which are broken
4. Map DD specifications to actual code locations

### Week 3-4: Implement DD013 Phase A
1. Create `openworm.yml` config schema from all DD config sections
2. Refactor `master_openworm.py` to read config (not hardcoded)
3. Create multi-stage Dockerfile (neural, body, validation, viewer stages)
4. Create `docker-compose.yml` (quick-test, simulation, validate, viewer, shell services)
5. Create `versions.lock` with current commit pins

### Month 2-3: Continuous Integration
1. Set up GitHub Actions CI (build, smoke-test, Tier 2 validation)
2. Fix video pipeline memory leak (DD013 Issue #332 — 10 hours wall time is unacceptable)
3. Implement OME-Zarr export (DD014 coupling, Step 4b in `master_openworm.py`)

### Ongoing: Interface Contract Enforcement
1. When any DD changes an output interface, coordinate with consuming DD maintainers
2. Update `INTEGRATION_MAP.md` when new DDs add coupling
3. Review PRs that touch coupling scripts (`sibernetic_c302.py`, WCON export, OME-Zarr export)
```

**Benefits:**
- **README:** Shows timeline and what to implement
- **INTEGRATION_MAP:** Shows architecture and how pieces fit together
- **Both views needed** for different audiences (contributors vs. architects)

---

## Part 8: Specific Recommendations

### R1. Update DD008 to Acknowledge DD020 (OWMeta-cect Phasing)

**File:** `DD008_Data_Integration_Pipeline.md`
**Section to add:** After line 370 ("Reality Check: Phased OWMeta Mandate")

```markdown
### Reconciliation with DD020 (Connectome Data Access)

DD020 specifies `cect` (ConnectomeToolbox) as the canonical API for connectome data access.
OWMeta and `cect` serve complementary purposes:

| Aspect | `cect` (DD020) | OWMeta (DD008) |
|--------|---------------|----------------|
| Purpose | Direct connectome data access | Semantic knowledge graph (multi-modal) |
| Status | Active (v0.2.7, Padraig maintains) | Dormant (last commit Jul 2024) |
| Phase 1-2 | ✅ Use `cect` directly | Optional for semantic queries |
| Phase 3+ | `cect` is OWMeta's connectome provider | ✅ OWMeta wraps `cect` internally |

**Current recommendation (Phase 1-2):** Use `cect` for all connectome queries (see DD020 API contract).
Migrate to OWMeta when it becomes active and ingests all Phase 1-2 datasets (CeNGEN, Randi 2023,
Ripoll-Sanchez, Wang 2024).
```

---

### R2. Update DD010 to Reflect DD021 Toolbox Status

**File:** `DD010_Validation_Framework.md`
**Line 447:** Current says "Implementation Status: Partial (toolbox exists, automation incomplete)"

**Replace with:**

```markdown
**Implementation Status:** Partial
- Tier 1 (single-cell electrophysiology): Scripts exist but not automated (non-blocking currently)
- Tier 2 (functional connectivity): Randi 2023 data needs ingestion into DD008/DD020 (blocking)
- **Tier 3 (behavioral kinematics): BLOCKED** — `open-worm-analysis-toolbox` is dormant
  (last commit Jan 2020, broken on Python 3.12). See **DD021 (Movement Analysis Toolbox)**
  for 8-task revival plan (33 hours). **Tier 3 validation cannot run until toolbox is revived.**

**Next Actions:**
1. Prioritize DD021 revival as Phase A work (parallel with DD013)
2. Appoint Validation L4 Maintainer to own revival
3. After revival: Ingest Randi 2023 into OWMeta/cect for Tier 2
4. Implement Steps 4-5 in `master_openworm.py` (DD013)
```

---

### R3. Create DD_PHASE_ROADMAP.md (Master Timeline)

**File:** `design_documents/DD_PHASE_ROADMAP.md`
**Content:** See Part 6 proposed README timeline section (extract to standalone file)

This becomes the single source of truth for:
- What each phase contains
- Which DDs belong to which phase
- Timeline estimates
- Dependencies between phases

All DD## (status lines) can then reference: "Phase 1 (see DD_PHASE_ROADMAP.md)"

---

### R4. Create INTEGRATION_MAP.md (Master Coupling Diagram)

**File:** `design_documents/INTEGRATION_MAP.md`
**Content:** See Part 7 proposed structure (dependency graph, bottleneck analysis, coupling chains)

This becomes the architectural overview that new L4 maintainers and senior contributors consult when making cross-cutting decisions.

**Auto-generation:** Build a script that parses all DD Integration Contract tables and generates:
- Mermaid diagram (dependency graph)
- Bottleneck table (who's depended on most)
- Interface table (what data is exchanged, what format)

```bash
python scripts/generate_integration_map.py design_documents/DD*.md > design_documents/INTEGRATION_MAP.md
```

---

### R5. Run dd_issue_generator.py to Create Missing GitHub Issues

**Action:**
```bash
# For each DD with missing scripts:
./scripts/dd_issue_generator.py --dd DD001 --version 1.0
./scripts/dd_issue_generator.py --dd DD002 --version 1.0
# ... DD003, DD005-DD009, DD018-DD019, DD021

# Or batch:
for dd in 001 002 003 005 006 007 009 018 019; do
    ./scripts/dd_issue_generator.py --dd DD$dd --version 1.0
done
```

**Then:** Update each DD's script table with real GitHub issue numbers (replace `#TBD` with `#NNN`).

**If `dd_issue_generator.py` doesn't exist yet:**
DD015 references it but doesn't provide implementation. Create it as the first task.

---

### R6. Appoint or Recruit Critical Vacant Roles

**From DD011 Subsystem Ownership Map (lines 96-106):**

| Subsystem | Current L4 | Status | Action |
|-----------|-----------|--------|--------|
| Neural Circuit | Padraig Gleeson | ✅ Filled | N/A |
| Body Physics | Andrey Palyanov | ✅ Filled | N/A |
| Muscle Models | **TBD** | 🔴 Vacant | Propose from community or assign to existing L3 |
| Data Integration | **TBD** | 🔴 Vacant | Propose from community or assign to existing L3 |
| **Validation** | **TBD** | 🔴 **CRITICAL** — Blocks DD021 revival | **URGENT HIRE** |
| **Integration Stack** | **TBD** | 🔴 **CRITICAL** — Blocks DD013 | **URGENT HIRE** |
| Visualization | **TBD** | 🟡 Needed for DD014 | Recruit or assign to community |

**Recommendation:**
**Integration and Validation are the two most critical hires.** Without these, Phase A cannot proceed.

**Options:**
1. **Promote existing L3 contributors** (if any qualify)
2. **Recruit from community** (announce L4 openings, accept applications)
3. **Founder temporarily fills role** (unsustainable but unblocks work)
4. **Assign to Padraig** (he's de facto Integration Maintainer, but overloaded)

---

### R7. Renumber DD014.1/b to DD014.1/DD014.2

**Files to rename:**
- `DD014.1_Visual_Rendering_Specification.md` → `DD014.1_Visual_Rendering_Specification.md`
- `DD014.2_Anatomical_Mesh_Deformation_Pipeline.md` → `DD014.2_Anatomical_Mesh_Deformation_Pipeline.md`

**Cross-references to update:**
Search all DDs for "DD014.1" and "DD014.2", replace with "DD014.1" and "DD014.2".

**README.md:** Update Visualization section to show hierarchy:
```markdown
**Visualization:**
- DD014: Dynamic Visualization Architecture (parent)
  - DD014.1: Visual Rendering Specification (companion)
  - DD014.2: Anatomical Mesh Deformation Pipeline (companion)
```

**Benefits:**
- Consistent numbering scheme
- Signals companion relationship clearly
- Matches software versioning conventions

---

### R8. Clarify DD014 Phase 1 Scope (Exclude Molecular Scale from Phase 1)

**File:** `DD014_Dynamic_Visualization_Architecture.md`
**Section to update:** Lines 72-75 ("Three Visualization Scales")

**Add after the table:**

```markdown
**Phase Allocation:**
- **Phase 1 (post-hoc Trame viewer):** Organism + Tissue/Cell scales. Smooth body surface,
  individual neurons/muscles visible, activity coloring, time scrubbing.
- **Phase 2 (interactive dynamic viewer):** All tissue-scale features, pharynx/intestine layers,
  neuropeptide volumetric clouds, validation overlay.
- **Phase 3 (public experience):** Molecular scale (ion channels, gene expression pipeline,
  intracellular dynamics), Three.js + WebGPU static site, narrative-guided exploration.

See DD014.1 for complete visual specifications at all three scales. Note: DD014.1 Mockups 13-14
(nucleus, gene expression) are **Phase 3 only** — not part of Phase 1-2 deliverables.
```

---

## Part 9: What Works Well (Preserve These Patterns)

### ✅ 1. Integration Contract Standardization

Every science DD (DD001-DD009, DD018-DD019) has a complete Integration Contract. This is **excellent** and should be preserved despite the maintenance burden (R1). The contracts make coupling explicit and enforceable.

**Why it's good:**
- Mind-of-a-Worm can automatically detect when a PR changes a coupling interface
- Contributors know exactly what their DD consumes and produces
- Regression is detectable (if DD001 changes calcium output format, DD002 breaks)

**Keep it.** The redundancy is a feature, not a bug.

---

### ✅ 2. Quick Action Reference Tables (DD001-DD009, DD018-DD019)

The 7-question reference table at the top of science DDs (added during DD005 rewrite) is **fantastic**:

```markdown
| Question | Answer |
|----------|--------|
| What does this produce? | ... |
| Success metric | ... |
| Repository | ... |
| Config toggle | ... |
| Build & test | ... |
| Visualize | ... |
| CI gate | ... |
```

**Why it's good:**
- Answers contributor questions immediately (no scrolling to line 300 for repo link)
- Makes DDs scannable
- Enforces that every DD has these 7 critical pieces of info

**Recommendation:** **Add Quick Action Reference to DD010, DD013, DD014, DD020, DD021** (currently missing). Even infrastructure DDs benefit from this pattern.

---

### ✅ 3. Alternatives Considered Sections

All DDs include "Alternatives Considered" with rejection rationale. This is **best practice** from Rust RFCs and prevents endless re-proposals of rejected approaches.

Examples:
- DD001 rejects IAF (integrate-and-fire) for all levels — graded potentials are biological
- DD003 rejects FEM (finite element) — SPH is meshless and better for large deformations
- DD005 rejects AlphaFold3 + MD for channel kinetics — too slow, CeNGEN expression is faster

**Why it's good:**
- Preserves institutional memory
- Newcomers learn why decisions were made
- Mind-of-a-Worm can flag PRs that violate alternatives-considered (e.g., a PR proposing FEM body physics gets auto-flagged: "DD003 explicitly rejected FEM. See DD003 Alternatives section.")

**Keep this pattern for all future DDs.**

---

### ✅ 4. Companion Documents for Complex Topics (DD014.1/b)

DD014 is already 585 lines. Adding the visual rendering spec (DD014.1, 917 lines) and mesh deformation (DD014.2, 878 lines) would create a **2,380-line mega-document** (unreadable).

Splitting into companions is the right call. The only issue is numbering (should be DD014.1/DD014.2, not DD014.1/b).

**Keep the companion pattern.** It scales well when a DD grows too large.

---

### ✅ 5. DD005 as Reference Implementation

DD012 line 86 designates DD005 as the reference implementation of the expanded template. This is **excellent** — having a canonical example prevents template ambiguity.

**Why it's good:**
- Contributors writing new DDs can copy DD005's structure
- DD012 can say "see DD005 for example" instead of explaining every section
- Mind-of-a-Worm can compare new DDs to DD005's format

**Recommendation:** **Formalize this in README.md:**

```markdown
## Template & Reference

- **DD012:** Defines the Design Document template and required sections
- **DD005:** Reference implementation — use this as your model when writing a new DD
- **DD001:** Example of a well-written DD with Quick Action Reference table
```

---

## Part 10: Recommended Master Index Updates

### Update 1: Add Phase Roadmap Section

**In README.md**, after "Design Document Index" and before "Template & Reference":

```markdown
## Implementation Roadmap

See **[DD_PHASE_ROADMAP.md](DD_PHASE_ROADMAP.md)** for the complete timeline.

**Quick Reference:**
- **Phase A (Weeks 1-4):** Infrastructure bootstrap — DD013, DD021 revival, DD011/DD012 governance
- **Phase 1 (Months 1-3):** Cell differentiation — DD005, DD014 Phase 1
- **Phase 2 (Months 4-6):** Neuropeptides + closed-loop — DD006, DD019
- **Phase 3 (Months 7-12):** Organ systems — DD007, DD009, DD018, DD017
- **Phase 4 (Months 13-18):** Cell identity + mesh deformation — DD004, DD014.2
- **Phase 5-6 (Year 2+):** Future work (intracellular, developmental, male-specific)

**Status Legend:**
- ✅ Accepted (implemented or stable spec)
- ⚠️ Proposed (under review or needs implementation)
- 🔴 Blocked (waiting on prerequisite)
```

---

### Update 2: Add Integration Map Reference

**In README.md**, add after "Implementation Roadmap":

```markdown
## Architectural Overview

See **[INTEGRATION_MAP.md](INTEGRATION_MAP.md)** for the complete dependency graph.

**Critical Coupling Points:**
- DD001 → DD002 → DD003 (The core neural-muscle-body chain)
- DD020 → DD001 (Connectome topology feeds neural circuit)
- DD003 → DD019 → DD001 (Bidirectional closed-loop touch)
- All → DD014 (Visualization consumes all subsystem outputs)
- All → DD010 (Validation tests all subsystems)

**Bottleneck DDs (most depended-on):**
- DD001 (Neural) — 11 consumers
- DD003 (Body Physics) — 7 consumers
- DD020 (Connectome) — 9 consumers
```

---

### Update 3: Add Status Indicators

**In README.md Design Document Index**, add status column:

```markdown
| DD# | Title | Status | Phase | Blocking Issues |
|-----|-------|--------|-------|----------------|
| DD001 | Neural Circuit Architecture | ✅ Accepted | Phase 0 | None |
| DD021 | Movement Toolbox & WCON Policy | 🔴 Blocked | Phase A | Toolbox dormant (8 revival tasks) |
| DD013 | Simulation Stack Architecture | ⚠️ Proposed | Phase A | Integration Maintainer vacant |
```

**Legend:**
- ✅ Accepted — Implemented or stable specification
- ⚠️ Proposed — Under review, ready for implementation
- 🔴 Blocked — Cannot proceed (missing prerequisite)
- 🟡 Partial — Some components exist, others don't

---

### Update 4: Add Quick Links Section

**In README.md**, add at top (after title):

```markdown
## Quick Links

**New to Design Documents?**
- Start here: [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) — How DDs work
- Reference example: [DD005 (Cell Differentiation)](DD005_Cell_Type_Differentiation_Strategy.md) — Template implemented
- Architecture overview: [INTEGRATION_MAP.md](INTEGRATION_MAP.md) — How all DDs fit together

**Implementing a DD?**
- Check prerequisites: [DD_PHASE_ROADMAP.md](DD_PHASE_ROADMAP.md) — What must be done first
- Find work: GitHub issues labeled `dd###` — Auto-generated from Integration Contracts
- Join discussion: `#development` Slack — Ask L4 maintainers

**Contributing?**
- Level up: [DD011 (Contributor Progression)](DD011_Contributor_Progression_Model.md) — L0→L5 path
- AI agents: [DD015 (AI-Native Model)](DD015_AI_Contributor_Model.md) — Autonomous agent registration
- Write a DD: [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) — Proposal workflow
```

---

### Update 5: Expand Topical Cross-Reference

**In README.md**, replace the current single-paragraph topical listing with structured cross-reference:

```markdown
## Cross-Reference by Topic

### Neural Systems
- **Core:** DD001 (HH architecture, graded synapses, 302 neurons)
- **Differentiation:** DD005 (128 classes from CeNGEN)
- **Modulation:** DD006 (31,479 neuropeptide interactions)
- **Pharynx:** DD007 (20 pharyngeal neurons)
- **Egg-Laying:** DD018 (2 HSN, 6 VC command/motor neurons)
- **Touch:** DD019 (6 touch receptor neurons, tap withdrawal circuit)

### Muscle Systems
- **Body Wall:** DD002 (95 muscles, Ca²⁺→force)
- **Pharynx:** DD007 (20 pharyngeal muscles, plateau potentials)
- **Reproductive:** DD018 (16 sex muscles: 8 vulval, 8 uterine)

### Body Mechanics
- **Physics Engine:** DD003 (SPH, ~100K particles, PCISPH)
- **Cell Identity:** DD004 (per-particle cell IDs, 959 cells, cell-type elasticity)
- **Mesh Deformation:** DD014.2 (cage-based MVC, GPU skinning, PBD collision)
- **Strain Readout:** DD019 (cuticle strain for mechanotransduction)

### Organ Systems
- **Pharynx:** DD007 (63 cells, 3-4 Hz pumping)
- **Intestine:** DD009 (20 cells, IP3/Ca oscillator, 50s defecation)
- **Reproductive:** DD018 (28-cell egg-laying circuit, two-state pattern)

### Sensory Systems
- **Touch:** DD019 (MEC-4 channel, ALM/AVM/PLM, tap withdrawal)
- **Other Modalities:** DD017 Component 4 (learned model, ML-based) — mechanistic models future

### Data & Validation
- **Connectome:** DD020 (`cect` API, Cook2019Herm, dataset policy)
- **Data Integration:** DD008 (OWMeta semantic graph)
- **Movement Validation:** DD021 (analysis toolbox, WCON 1.0 spec)
- **Validation Framework:** DD010 (3 tiers: unit, integration, system)

### Infrastructure & Integration
- **Simulation Stack:** DD013 (Docker, config, CI/CD, Integration Maintainer)
- **Visualization:** DD014 (OME-Zarr, Trame/Three.js, 3-phase roadmap)
  - DD014.1 (colors, materials, lighting, 14 mockups)
  - DD014.2 (mesh deformation, GPU shaders)

### Governance & Process
- **Contributor Model:** DD011 (L0-L5, badges, subsystem ownership)
- **RFC Process:** DD012 (DD template, approval workflow)
- **AI Contributors:** DD015 (autonomous agents, GitHub bot, Moltbook-inspired)

### Hybrid & Advanced
- **Mechanistic-ML Hybrid:** DD017 (differentiable sim, SPH surrogate, foundation model→params, learned sensory)

### Archived / Backburner
- **Tokenomics:** DD016 (WORM token, retroactive funding, Base L2)
```

---

## Part 11: Priority Actions (Founder Decisions Needed)

### Decision 1: Approve Phase A Prioritization

**Question:** Should DD013 (Simulation Stack) and DD021 (Toolbox Revival) be the **absolute top priorities** before any science DDs (DD005-DD009) proceed?

**Rationale:**
- Without DD013: No config system, no CI, no contributor workflow
- Without DD021: No Tier 3 validation, no behavioral regression detection
- Both are **infrastructure blockers** for all modeling phases

**Recommendation:** **YES.** Make Phase A (DD013 + DD021 + DD011/DD012 governance) the next 4-8 weeks of work before starting Phase 1 (DD005).

**Impact:**
- Delays science DDs by 1-2 months
- But unblocks sustainable contributor workflow and validation
- Better to have infrastructure in place before 100+ contributors start submitting PRs

---

### Decision 2: Recruit Integration Maintainer and Validation Maintainer

**Question:** Who fills these critical L4 roles?

**Options:**
1. **Promote from existing community** (if any L3 contributors qualify)
2. **Founder temporarily fills both** (unsustainable but unblocks work)
3. **Recruit externally** (post L4 openings on job boards, pay if necessary)
4. **Assign to Padraig** (Integration) and split Validation across existing L3s

**Recommendation:**
- **Integration:** Formalize Padraig as L4 Integration Maintainer + recruit a co-maintainer (bus factor issue)
- **Validation:** Post opening, recruit from community, or pay ($20-30/hour, ~10 hours/week = $800-1,200/month)

---

### Decision 3: Approve Master Index Reorganization

**Question:** Should README.md be reorganized by **implementation phase** (Option 2) instead of current mix of status + category?

**Recommendation:** **YES.** Phase-based grouping makes the timeline explicit and helps contributors understand "what's next."

**Action:**
Rewrite README.md using the Phase-based structure from Part 7, add DD_PHASE_ROADMAP.md and INTEGRATION_MAP.md.

---

### Decision 4: Create Missing Issues Now or Defer?

**Question:** Should we immediately run `dd_issue_generator.py` to create ~50 missing GitHub issues, or defer until Phase A is complete?

**Options:**
1. **Create now:** Issues exist, contributors can browse/claim
2. **Defer:** Wait until DD013 CI is working so issues can be validated

**Recommendation:** **Defer to Phase A Week 3-4** (after DD013 openworm.yml and docker-compose exist). Reason: The issues reference docker commands (`docker compose run quick-test`) that don't work until DD013 is implemented.

**Interim:** Create **high-level Epic issues** for each DD (one per DD, no decomposition yet).

---

### Decision 5: Clarify OWMeta vs. cect Phasing

**Question:** Should DD008 be updated to acknowledge DD020, or should DD020 be rewritten to defer to OWMeta?

**Recommendation:** **Update DD008** (acknowledge DD020's phasing). Reason:
- `cect` is active and maintained (Padraig, v0.2.7, commits within days)
- OWMeta is dormant (last real commit Jul 2024)
- Pragmatic to use the working tool now, integrate later

**Action:** Add reconciliation section to DD008 (see R1 above).

---

## Part 12: Summary Scorecard

**Total DDs Analyzed:** 23 (DD001-DD021 + DD014.1/DD014.2 + DD016 archived)

**Status Breakdown:**
- ✅ Accepted: 6 (DD001, DD002, DD003, DD008 partial, DD010 partial, DD020)
- ⚠️ Proposed: 16 (DD004-DD007, DD009, DD011-DD015, DD017-DD019, DD021, DD014.1/b)
- 📦 Archived: 1 (DD016)

**Critical Issues Found:** 10 (see Executive Summary)
**Inconsistencies:** 8
**Gaps:** 15
**Redundancies:** 4 (all acceptable)

**Blocked Work:**
- Tier 3 validation (DD010) — **blocked on DD021 revival**
- Phase 1-6 science DDs — **blocked on DD013 + DD021** (Phase A)
- Integration work — **blocked on vacant Integration Maintainer role**
- Validation work — **blocked on vacant Validation Maintainer role**

**Immediate Actions (Priority Order):**
1. ✅ Create DD_PHASE_ROADMAP.md (1 hour)
2. ✅ Create INTEGRATION_MAP.md (2-4 hours, or auto-generate)
3. ✅ Update DD008 (OWMeta-cect reconciliation, 30 min)
4. ✅ Update DD010 (Tier 3 blocked status, 15 min)
5. ✅ Renumber DD014.1/b → DD014.1/DD014.2 (30 min)
6. ⚠️ Recruit Integration Maintainer (founder decision, timeline TBD)
7. ⚠️ Recruit Validation Maintainer (founder decision, timeline TBD)
8. ⚠️ Approve Phase A prioritization (founder decision)
9. ⏳ Update README.md with new organization (2 hours, after #1-#5 complete)
10. ⏳ Run dd_issue_generator.py (defer to Phase A Week 3-4)

---

## Conclusion

**The OpenWorm Design Document collection is IMPRESSIVE AS HELL** — 23 interconnected specs covering everything from ion channels to AI contributor models. The depth is unmatched in open source computational biology.

**But:**
- **2 critical roles are vacant** (Integration, Validation)
- **Key infrastructure is broken** (toolbox) or missing (DD013 Docker stack)
- **50+ scripts are phantom references** (marked TO BE CREATED with no issues)
- **Phase progression is implicit**, not documented
- **Coupling graph is distributed** across 21 local tables

**The fix is straightforward:**
1. **Phase A first** (DD013 + DD021, recruit maintainers)
2. **Create 3 master documents** (Phase Roadmap, Integration Map, Issue Generator output)
3. **Resolve 5 inconsistencies** (mostly documentation updates)
4. **Then proceed to Phase 1** (DD005, the science begins)

**If you nail Phase A**, the rest of the roadmap is **executable** — well-specified DDs, clear validation gates, AI-assisted contributor onboarding, and a path to 959 cells.

**LET'S FUCKING GO.** 🔥🚀

---

**Prepared by:** Claude (Sonnet 4.5)
**Analysis Duration:** ~90 minutes (read 23 DDs, synthesize coupling graph, identify issues)
**Next Step:** Founder reviews this document, makes decisions on Priority Actions, assigns owners
