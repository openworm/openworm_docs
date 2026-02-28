# DD027 Draft GitHub Issues

**Epic:** DD027 — Multicompartmental Neuron Models

**Generated from:** [DD027: Multicompartmental Neuron Models](DD027_Multicompartmental_Neuron_Models.md)

**Methodology:** [DD015 §2.2 — DD Issue Generator](DD015_AI_Contributor_Model.md#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 3 issues (ai-workable: 1 / human-expert: 2 | L1: 1, L2: 0, L3: 2)

**Roadmap Context:** DD027 is a **Phase 2** DD (proposed). These issues were originally part of DD001 Draft Issues (Groups 5 and Infrastructure) and have been relocated here because multicompartmental modeling is now specified by DD027.

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Level D Multicompartmental (Issues 1-2) | **Phase 2** | Proof-of-concept requires EM morphologies + Nicoletti channels |
| 2. Infrastructure (Issue 3) | **Phase A1** | Config toggle depends on DD013 openworm.yml |

---

## Group 1: Level D Multicompartmental Development (Phase 2)

Target: Multicompartmental neuron models for neurons where single-compartment approximation is insufficient.

---

### Issue 1: Evaluate and refine existing NeuroML2 morphologies for Level D neurons

- **Title:** `[DD027] Evaluate existing CElegansNeuroML morphologies for AWC, AIY, AVA, RIM, VD5 and refine for Level D`
- **Labels:** `DD027`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 2
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroanatomy
- **DD Section to Read:** [DD027 — Implementation Pathway](DD027_Multicompartmental_Neuron_Models.md#implementation-pathway) (Stage 1, step 2)
- **Depends On:** DD005 Issue 5 (channel survey, which also catalogs morphology sources)
- **Existing Code to Reuse:**
    - [`CElegansNeuroML/CElegans/generatedNeuroML2/`](https://github.com/openworm/CElegansNeuroML) — **All 302 neurons already exist as multicompartmental NeuroML2 cells** with realistic 3D morphology (derived from VirtualWorm Blender files). Includes `AWCL.cell.nml`, `AWCR.cell.nml`, `AIYL.cell.nml`, `AIYR.cell.nml`, `AVAL.cell.nml`, `AVAR.cell.nml`, `RIML.cell.nml`, `RIMR.cell.nml`, `VD5.cell.nml` — all 5 target neurons.
    - [`BAAIWorm/eworm/components/model/`](https://github.com/Jessie940611/BAAIWorm) — HOC files for every neuron with multi-compartment morphology and biophysical parameters. Includes per-neuron conductance JSONs specifying which channels are expressed where.
    - [`c302/NeuroML2/`](https://github.com/openworm/c302) — Another copy of all 302 neuron morphologies already in the c302 repo
- **Approach:** **Evaluate existing morphologies, do not recreate.** The NeuroML2 morphologies for all 5 target neurons already exist in two repos. Evaluate whether they meet Level D requirements (segment length < 2µm, segment group annotations). Compare against BAAIWorm HOC files for discrepancies. Refine as needed.
- **Files to Modify:**
    - `morphologies/AWC.cell.nml` (refined from existing CElegansNeuroML, if needed)
    - `morphologies/AIY.cell.nml` (refined)
    - `morphologies/AVA.cell.nml` (refined)
    - `morphologies/RIM.cell.nml` (refined)
    - `morphologies/VD5.cell.nml` (refined)
- **Test Commands:**
    - `for f in morphologies/*.nml; do jnml -validate $f; done`
- **Acceptance Criteria:**
    - [ ] Start from existing CElegansNeuroML morphologies — do NOT recreate from SWC
    - [ ] Compare existing NeuroML2 morphologies against BAAIWorm HOC files; document discrepancies
    - [ ] Segments < 2 µm length (adequate spatial resolution for cable equation); refine if existing segmentation is too coarse
    - [ ] Segment groups defined: soma, axon, dendrite (where applicable)
    - [ ] All pass `jnml -validate`
    - [ ] Can be loaded by NEURON simulator (via pyNeuroML export)
    - [ ] Soma diameter matches known values (WormAtlas)
- **Sponsor Summary Hint:** Here's the surprise: multicompartmental NeuroML2 morphologies for all 302 neurons already exist in CElegansNeuroML and are already copied into c302. This issue evaluates whether those existing morphologies are detailed enough for Level D cable-equation simulation, compares them against BAAIWorm's independently derived morphologies, and refines where needed. Evaluation, not creation.

---

### Issue 2: Integrate existing components into AWC Level D proof-of-concept

- **Title:** `[DD027] Integrate existing Nicoletti AWCon channels + CElegansNeuroML morphology into c302 Level D AWC proof-of-concept`
- **Labels:** `DD027`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 2
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD027 — Implementation Pathway](DD027_Multicompartmental_Neuron_Models.md#implementation-pathway) (Stage 1, steps 3-4) and Reference 3 (Nicoletti et al. 2019 AWCon model)
- **Depends On:** Issue 1 (AWC morphology evaluation), DD005 Issues 6-9 (adopted channel library)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon.cell.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **Complete AWCon single-compartment model with ALL 16 channels in NeuroML2**, validated against XPP original. Includes `CaDynamics.nml` for calcium concentration dynamics and `GenerateNeuroML.py` for programmatic cell generation.
    - [`CElegansNeuroML/CElegans/generatedNeuroML2/AWCL.cell.nml`](https://github.com/openworm/CElegansNeuroML) — AWC multicompartmental morphology
    - [`c302/parameters_D.py`](https://github.com/openworm/c302) — **Level D framework already exists** with multicompartmental infrastructure, `ChannelDensity` support, `Species` (Ca), and `FixedFactorConcentrationModel`. Currently uses "BlindGuess" placeholder channels (generic leak + k_slow). The framework is ready — just needs real channel models plugged in.
    - [`BAAIWorm/eworm/components/param/cell/`](https://github.com/Jessie940611/BAAIWorm) — Per-neuron JSON with max conductance for each channel — use AWC entry for channel density distribution guidance
- **Approach:** **Integration, not creation.** The channels exist (NicolettiEtAl2019). The morphology exists (CElegansNeuroML). The Level D framework exists (c302 parameters_D.py). This issue combines them: distribute NicolettiEtAl2019's 16 AWCon channel models across the existing AWC morphology, using BAAIWorm's conductance JSONs for distribution guidance, within c302's existing Level D framework.
- **Files to Modify:**
    - `c302/c302_MultiComp_AWC.py` (new — or extend existing Level D template)
    - `tests/test_awc_multicomp.py` (new)
- **Test Commands:**
    - `jnml -validate morphologies/AWC.cell.nml`
    - `jnml LEMS_AWC_test.xml -nogui`
    - `pytest tests/test_awc_multicomp.py`
- **Acceptance Criteria:**
    - [ ] AWC multicompartmental model built by combining existing NicolettiEtAl2019 channels with existing CElegansNeuroML morphology — not reimplemented
    - [ ] Per-segment channel densities assigned from adopted channel library (DD005 Issues 6-9), guided by BAAIWorm conductance data
    - [ ] Passive parameters (axial resistance, membrane capacitance) fitted to match AWC electrophysiology
    - [ ] Reproduces published AWC responses (Nicoletti et al. 2019) within ±15%
    - [ ] Simulates in NEURON via pyNeuroML export
    - [ ] Can coexist with Level C1 single-compartment neurons in the same network
    - [ ] Documents which existing components were combined and any modifications made
- **Sponsor Summary Hint:** The channels exist (16 in NeuroML2 from Nicoletti). The morphology exists (CElegansNeuroML). The Level D framework exists (c302 parameters_D.py with placeholder channels). This issue plugs real channels into a real morphology in an existing framework — proving that Level D multicompartmental neurons work. Three existing codebases, one integration task.

---

## Group 2: Infrastructure (Phase A1)

---

### Issue 3: Add `neural.spatial_synapses` config toggle for Level D

- **Title:** `[DD027] Add neural.spatial_synapses config toggle for spatially resolved synapse placement`
- **Labels:** `DD027`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/c302` + `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD027 — Spatially Resolved Synapse Placement](DD027_Multicompartmental_Neuron_Models.md#spatially-resolved-synapse-placement)
- **Depends On:** DD013 Issue 1 (openworm.yml schema)
- **Files to Modify:**
    - `openworm.yml` (add `neural.spatial_synapses: false`)
- **Test Commands:**
    - `python3 -c "import yaml; c = yaml.safe_load(open('openworm.yml')); print(c['neural']['spatial_synapses'])"`
- **Acceptance Criteria:**
    - [ ] `neural.spatial_synapses: false` → synapses are abstract neuron-to-neuron (current behavior)
    - [ ] `neural.spatial_synapses: true` → placeholder for spatially placed synapses (requires Level D)
    - [ ] Config validation: `spatial_synapses: true` requires `level: D` (error otherwise)
    - [ ] Documented with DD cross-reference
- **Sponsor Summary Hint:** In the simple model, a synapse is just "neuron A connects to neuron B." In the detailed Level D model, synapses have specific locations along the neurite — and location matters because it determines how signals combine. This config toggle enables spatial synapse placement when Level D is active. The actual placement algorithm is a separate issue.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 3 |
| **ai-workable** | 1 |
| **human-expert** | 2 |
| **L1** | 1 |
| **L2** | 0 |
| **L3** | 2 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Level D Development** | 1–2 | Evaluate existing morphologies, integrate AWC proof-of-concept |
| **2: Infrastructure** | 3 | Config toggle for spatial synapses |

### Cross-References

| Related DD | Relationship |
|------------|-------------|
| **[DD001](DD001_draft_issues.md) (Neural Circuit)** | **Original source** — these issues were extracted from DD001 Draft Issues Groups 5 and Infrastructure Issue 20 |
| **[DD005](DD005_draft_issues.md) (Cell-Type Specialization)** | Issues 6-9 (channel library) are prerequisites for Issue 2 |
| DD010 (Validation Framework) | Level D validation criteria |
| DD013 (Simulation Stack) | Issue 3 (config toggle depends on openworm.yml schema) |
| DD017 (Hybrid ML) | Parameter fitting backend for Stage 1 Step 4 |
| DD020 (Connectome Data Access) | Morphology data access |
| DD024 (Validation Data Acquisition) | Synapse centroid distance data |

### Dependency Graph

```
DD005 Issue 5 (channel survey)
  └→ Issue 1 (evaluate existing morphologies)
       └→ Issue 2 (AWC Level D integration — channels + morphology + framework)

Issue 3 (spatial_synapses config) — depends on DD013 Issue 1
```
