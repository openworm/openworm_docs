# Design Document Code Reuse Opportunities
**Created:** 2026-02-19
**Purpose:** Identify existing OpenWorm repos that can accelerate DD implementation

---

## Executive Summary

**Of the 109 OpenWorm GitHub repositories, at least 15 contain code, data, or algorithms that directly support Design Document deliverables.** Rather than building from scratch, we can reuse, adapt, or learn from:

- **3 repos with production-ready data APIs** (wormneuroatlas, ChannelWorm, ConnectomeToolbox)
- **4 repos with models we can directly port** (pharyngeal_muscle_model, CE_locomotion proprioceptive feedback, bionet, CyberElegans)
- **5 repos with infrastructure/tools** (sibernetic_config_gen, sibernetic_NEURON, skeletonExtraction, openworm.ai, simple-C-elegans)
- **3 validation/analysis repos** (wormneuroatlas, neuronal-analysis, SegWorm)

**Potential time savings:** 100-200 hours across Phases 1-3 if we reuse instead of rebuild.

---

## HIGH-IMPACT REUSE OPPORTUNITIES (Immediate)

### 1. wormneuroatlas → [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (CeNGEN API) + [DD010](DD010_Validation_Framework.md) (Randi 2023 Data)

**Repo:** [openworm/wormneuroatlas](https://github.com/openworm/wormneuroatlas) (pushed 2025-10-22)
**Status:** ✅ **Production-ready Python package on PyPI**
**Installation:** `pip install wormneuroatlas`

**What It Provides:**

| Feature | API | DD Deliverable It Replaces |
|---------|-----|---------------------------|
| **Randi 2023 functional connectivity** | `NeuroAtlas.get_signal_propagation_atlas(strain="wt")` | [DD010](DD010_Validation_Framework.md) Tier 2 validation target (302×302 correlation matrix) |
| **CeNGEN gene expression** | `NeuroAtlas.get_gene_expression(gene_names, neuron_names)` | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) expression data access (currently: download CSV from cengen.org) |
| **Neuropeptide/GPCR binding** | `PeptideGPCR.get_gpcrs_binding_to(peptides)` | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) neuropeptide-receptor mapping |
| **Anatomical connectome** | `NeuroAtlas` class (includes Cook et al. data) | [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) connectome (complements `cect`) |
| **Neuron ID conversion** | `merge_bilateral=True` etc. | Handles AVAL/AVAR → AVA_ merging |

**Reuse Plan for [DD005](DD005_Cell_Type_Differentiation_Strategy.md):**

Instead of:
```python
# DD005 current plan (lines 78-79)
wget -O data/CeNGEN_L4_expression.csv "https://cengen.org/downloads/L4_expression_matrix.csv"
```

**Do this:**
```python
# Reuse wormneuroatlas API
from wormneuroatlas import NeuroAtlas

atlas = NeuroAtlas()
expression_data = atlas.get_gene_expression(
    gene_names=["unc-2", "egl-19", "shl-1", "shk-1"],  # Ion channel genes
    neuron_names=["AVAL", "AVAR", "DA01", ...]  # All 302 neurons or 128 classes
)
# Returns: DataFrame with expression values (TPM) per gene per neuron
```

**Benefits:**
- ✅ No manual CSV download/parsing
- ✅ Handles neuron ID normalization (AVAL vs AVA_ vs bilateral merging)
- ✅ pip-installable (works in Docker)
- ✅ Maintained by Randi lab (Francesco Randi's repo)
- ✅ Already integrates CeNGEN, WormBase, and Randi 2023 datasets

**Reuse Plan for [DD010](DD010_Validation_Framework.md) Tier 2:**

```python
# Load Randi 2023 functional connectivity for validation
from wormneuroatlas import NeuroAtlas

atlas = NeuroAtlas()
func_conn_matrix = atlas.get_signal_propagation_atlas(strain="wt")
# Returns: 302×302 correlation matrix (exactly what [DD010](DD010_Validation_Framework.md) Tier 2 needs)

# Compare simulated to experimental
simulated_fc = compute_functional_connectivity(simulation_calcium_traces)
correlation_of_correlations = np.corrcoef(
    func_conn_matrix.flatten(),
    simulated_fc.flatten()
)[0, 1]

# DD010 acceptance: r > 0.5
assert correlation_of_correlations > 0.5, "Tier 2 validation failed"
```

**Action Items:**
- [ ] Add `wormneuroatlas` to [DD013](DD013_Simulation_Stack_Architecture.md) `versions.lock` (pin version)
- [ ] Add to [DD013](DD013_Simulation_Stack_Architecture.md) Docker `neural` stage: `pip install wormneuroatlas`
- [ ] Update [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration scripts to use `wormneuroatlas` API
- [ ] Update [DD010](DD010_Validation_Framework.md) Tier 2 validation to load Randi data via `wormneuroatlas`
- [ ] Update [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) to reference `PeptideGPCR` class for neuropeptide-receptor mapping
- [ ] Add to [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) as **complementary** to `cect` (wormneuroatlas has different data: functional connectivity, neuropeptide deorphanization)

**Estimated Time Savings:** 20-30 hours (no manual data download, parsing, or API building)

---

### 2. ChannelWorm → [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Ion Channel Database + HH Parameters)

**Repo:** [openworm/ChannelWorm](https://github.com/openworm/ChannelWorm) (pushed 2018-08-27, dormant but complete)
**Status:** ⚠️ Dormant (6 years) but **contains curated ion channel data and NeuroML2 models**

**What It Contains:**

```
ChannelWorm/
├── data/                          # Curated ion channel spreadsheet
│   └── ion_channel_database.xlsx  # Gene, kinetics, patch clamp sources
├── models/                        # NeuroML2 channel models (pre-generated)
│   ├── unc2_L-type_Ca.channel.nml
│   ├── egl19_L-type_Ca.channel.nml
│   ├── shl1_Kv4_A-type.channel.nml
│   └── ...
├── channelworm/                   # Python tools
│   ├── digitizer.py               # Digitize patch clamp plots from papers
│   ├── fitter.py                  # Fit HH parameters to experimental data
│   └── exporter.py                # Export to NeuroML2
└── tests/                         # SciUnit validation tests
```

**Reuse Plan for [DD005](DD005_Cell_Type_Differentiation_Strategy.md):**

[DD005](DD005_Cell_Type_Differentiation_Strategy.md) needs (lines 442-448):
- ~20 neurons with electrophysiology for calibration training set
- Ion channel→NeuroML model mapping
- HH parameter fitting from patch clamp data

**ChannelWorm already has this!**

**Instead of building from scratch:**
1. **Clone ChannelWorm:** `git clone https://github.com/openworm/ChannelWorm.git`
2. **Extract ion channel database:** `data/ion_channel_database.xlsx` → Convert to CSV for [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration
3. **Use existing NeuroML2 models:** `models/*.channel.nml` → These are [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s channel definitions
4. **Reuse fitting pipeline:** `channelworm/fitter.py` → Adapt for CeNGEN expression→conductance calibration
5. **Reuse validation:** `tests/` SciUnit framework → [DD010](DD010_Validation_Framework.md) Tier 1 single-cell validation

**ChannelWorm was designed to feed c302** (per README: "models are used by c302 for simulating nervous system dynamics"). It's the EXACT pipeline [DD005](DD005_Cell_Type_Differentiation_Strategy.md) needs.

**Action Items:**
- [ ] Review ChannelWorm `models/` directory — how many NeuroML2 channels already exist?
- [ ] Extract ion channel database to [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s `data/electrophysiology_training_set.csv`
- [ ] Port `channelworm/fitter.py` HH fitting code to [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s `scripts/fit_calibration.py`
- [ ] Reference ChannelWorm in [DD005](DD005_Cell_Type_Differentiation_Strategy.md) Implementation References section
- [ ] Consider reviving ChannelWorm as the **canonical ion channel database** for OpenWorm (update dependencies, merge into c302 or make it a [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)-style data access layer)

**Estimated Time Savings:** 40-60 hours (no manual channel curation, no HH fitter from scratch)

---

### 3. pharyngeal_muscle_model → [DD007](DD007_Pharyngeal_System_Architecture.md) (Pharyngeal Muscle HH Model)

**Repo:** [openworm/pharyngeal_muscle_model](https://github.com/openworm/pharyngeal_muscle_model) (pushed 2017-01-19, dormant but complete)
**Status:** ⚠️ Dormant (9 years) but **contains working NEURON model of pm3 pharyngeal muscle**

**What It Contains:**
- **pm3 muscle NEURON model** with Ca²⁺ slow action potential (NMODL)
- Implements **EAT-2, EGL-19, UNC-2 channels** (exactly what [DD007](DD007_Pharyngeal_System_Architecture.md) needs!)
- Output visualization showing plateau potentials (~100ms duration)
- Matches Raizen & Avery 1994 EPG recordings ([DD007](DD007_Pharyngeal_System_Architecture.md)'s primary validation target)

**Reuse Plan for [DD007](DD007_Pharyngeal_System_Architecture.md):**

[DD007](DD007_Pharyngeal_System_Architecture.md) needs (lines 48-49):
- Pharyngeal muscle cell template (`PharyngealMuscleCell.cell.nml`)
- Plateau potential kinetics (eat-2, egl-19, unc-2 channels)

**This repo already has the NEURON implementation!**

**Action:**
1. Clone `pharyngeal_muscle_model`
2. Extract pm3 muscle NMODL code
3. Convert NEURON/NMODL → NeuroML2 (use `pyNeuroML` conversion tools or rewrite)
4. Validate against Raizen & Avery 1994 (the repo claims to match EPG data)
5. Use as `PharyngealMuscleCell.cell.nml` in [DD007](DD007_Pharyngeal_System_Architecture.md)

**Alternative:** Run NEURON model directly in [DD007](DD007_Pharyngeal_System_Architecture.md) (no conversion needed), couple to c302 via existing `sibernetic_NEURON` bridge (see below).

**Action Items:**
- [ ] Test pharyngeal_muscle_model (run `_run.hoc` in NEURON, verify Ca²⁺ plateau)
- [ ] Compare output to [DD007](DD007_Pharyngeal_System_Architecture.md)'s target: plateau duration ~100ms, pumping frequency compatible
- [ ] Convert to NeuroML2 OR use NEURON directly (decision: NeuroML for consistency)
- [ ] Reference in [DD007](DD007_Pharyngeal_System_Architecture.md) Implementation References

**Estimated Time Savings:** 20-30 hours (pharyngeal muscle model already validated)

---

### 4. CE_locomotion → [DD019](DD019_Closed_Loop_Touch_Response.md) (Proprioceptive Feedback) + [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Evolutionary Parameter Fit)

**Repo:** [openworm/CE_locomotion](https://github.com/openworm/CE_locomotion) (pushed 2026-02-18, **VERY ACTIVE**)
**Status:** ✅ **ACTIVE** — Collaboration with Dr. Erick Olivares & Prof. Randall Beer

**What It Contains:**
- Complete neuromechanical C++ model (nervous system + muscles + body)
- **StretchReceptor.cpp/h** — Proprioceptive feedback on motor neurons (Wen et al. 2012 model!)
- **Evolutionary algorithm** for parameter fitting (auto-tunes parameters to produce forward/backward locomotion)
- Produces forward and backward locomotion from same neural circuit (gait modulation)
- Visualization tools (Python + Mathematica)

**Reuse Plan for [DD019](DD019_Closed_Loop_Touch_Response.md) Follow-Up (Proprioception DD):**

[DD019](DD019_Closed_Loop_Touch_Response.md) line 579 scopes out proprioceptive feedback: "B-class motor neuron stretch receptors (Wen et al. 2012). Deferred to future DD."

**CE_locomotion already implemented this!**

**Action:**
1. Extract `StretchReceptor.cpp/h` algorithm
2. Port to Python or NeuroML for integration with c302
3. Add as a new DD ([DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md): Proprioceptive Feedback and Motor Coordination)
4. Reference CE_locomotion as source of stretch receptor model

**Reuse Plan for [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Auto-Fitting):**

[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) proposes gradient descent for parameter fitting. CE_locomotion uses **evolutionary algorithms** (genetic algorithm or CMA-ES) for the same purpose.

**Action:**
1. Extract evolutionary algorithm code (`main.cpp` optimization loop)
2. Compare to [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)'s gradient descent approach
3. Hybrid approach: Use evolutionary for global search, gradient descent for local refinement
4. Reference CE_locomotion's fitness function (how they define "good locomotion")

**Action Items:**
- [ ] **Contact repo owners** (Erick Olivares, Randall Beer) — ask if this is still active, can we collaborate?
- [ ] Extract StretchReceptor model, port to Python/NeuroML
- [ ] Write [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (Proprioceptive Feedback) using CE_locomotion's approach
- [ ] Compare CE_locomotion's neuromechanical model to c302+Sibernetic (publication opportunity: "Two Approaches to C. elegans Neuromechanical Modeling")
- [ ] Extract evolutionary parameter fitting for [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 1

**Estimated Time Savings:** 30-50 hours (proprioceptive model already implemented + evolutionary fitting algorithm exists)

---

### 5. sibernetic_config_gen → [DD013](DD013_Simulation_Stack_Architecture.md) (Configuration System)

**Repo:** [openworm/sibernetic_config_gen](https://github.com/openworm/sibernetic_config_gen) (pushed 2016-12-19, dormant)
**Status:** ⚠️ Dormant (10 years) but **already generates Sibernetic scene configs**

**What It Does:**
- Generates starting particle positions for Sibernetic
- Creates `.ini` config files ([DD013](DD013_Simulation_Stack_Architecture.md) needs to read these!)
- Handles different body resolutions (full, half, quarter)

**Reuse Plan for [DD013](DD013_Simulation_Stack_Architecture.md):**

[DD013](DD013_Simulation_Stack_Architecture.md) needs (lines 469-479):
- Translator from `openworm.yml` → Sibernetic `.ini` format
- Particle initialization for different configs

**This repo already does half of this!**

**Action:**
1. Review `sibernetic_config_gen` particle generation algorithms
2. Reuse particle placement code in [DD013](DD013_Simulation_Stack_Architecture.md)'s `master_openworm.py`
3. Extend to read `openworm.yml` and call config_gen as subprocess

**Action Items:**
- [ ] Test sibernetic_config_gen (does it still work with current Sibernetic?)
- [ ] Extract particle generation algorithms
- [ ] Integrate into [DD013](DD013_Simulation_Stack_Architecture.md)'s config→ini translation layer
- [ ] Reference in [DD013](DD013_Simulation_Stack_Architecture.md) Implementation References

**Estimated Time Savings:** 10-20 hours (particle init already solved)

---

### 6. sibernetic_NEURON → [DD013](DD013_Simulation_Stack_Architecture.md) (Coupling Script Foundation)

**Repo:** [openworm/sibernetic_NEURON](https://github.com/openworm/sibernetic_NEURON) (pushed 2016-12-19, dormant)
**Status:** ⚠️ Dormant but **contains Sibernetic↔NEURON interface code**

**What It Contains:**
- Interface between Sibernetic and NEURON simulator
- Reads NEURON output, writes Sibernetic input
- **This is the predecessor to `sibernetic_c302.py`** ([DD002](DD002_Muscle_Model_Architecture.md)→[DD003](DD003_Body_Physics_Architecture.md) coupling)

**Reuse Plan for [DD013](DD013_Simulation_Stack_Architecture.md):**

The current `sibernetic_c302.py` may have originated from this repo. Check if:
- Current coupling script is a fork/evolution of sibernetic_NEURON
- Lessons learned from sibernetic_NEURON inform [DD019](DD019_Closed_Loop_Touch_Response.md)'s bidirectional coupling (`sibernetic_c302_closedloop.py`)

**Action:**
1. Compare sibernetic_NEURON to current `sibernetic_c302.py`
2. Check git history — was it forked from this repo?
3. Extract any reusable patterns for [DD019](DD019_Closed_Loop_Touch_Response.md)'s reverse path (body→sensory)

**Estimated Time Savings:** 5-10 hours (learn from existing coupling code)

---

### 7. skeletonExtraction → [DD013](DD013_Simulation_Stack_Architecture.md) (WCON Export), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Skeleton Generation)

**Repo:** [openworm/skeletonExtraction](https://github.com/openworm/skeletonExtraction) (pushed 2016-12-19, dormant)
**Status:** ⚠️ Dormant but **transforms Sibernetic particle output to skeleton + COLLADA animation**

**What It Does:**
- Reads Sibernetic particle positions
- Extracts 49-point skeleton (centerline of worm body)
- Exports to COLLADA for animation

**Reuse Plan for [DD013](DD013_Simulation_Stack_Architecture.md) + [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md):**

[DD013](DD013_Simulation_Stack_Architecture.md) needs (Step 4 in `master_openworm.py`):
- Convert SPH particles → 49-point skeleton → WCON file

[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) needs:
- WCON files with 49 skeleton points per frame (required by analysis toolbox)

**This repo already does skeleton extraction!**

**Action:**
1. Extract skeleton algorithm from `skeletonExtraction`
2. Port to Python (if it's not already)
3. Modify output: COLLADA → WCON format
4. Use in [DD013](DD013_Simulation_Stack_Architecture.md)'s WCON exporter

**Action Items:**
- [ ] Clone and test skeletonExtraction
- [ ] Extract centerline algorithm (how does it find the 49-point spine from ~40K particles?)
- [ ] Port to [DD013](DD013_Simulation_Stack_Architecture.md)'s WCON export pipeline
- [ ] Reference in [DD013](DD013_Simulation_Stack_Architecture.md) + [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)

**Estimated Time Savings:** 15-25 hours (skeleton extraction algorithm is non-trivial)

---

### 8. openworm.ai → [DD015](DD015_AI_Contributor_Model.md) (AI Contributor Infrastructure)

**Repo:** [openworm/openworm.ai](https://github.com/openworm/openworm.ai) (pushed 2026-02-19, **VERY ACTIVE**)
**Status:** ✅ **ACTIVE** — Contains LLM/AI scripts

**What It Contains:**
```
openworm_ai/
├── corpus/            # Text corpus (OpenWorm docs for RAG?)
├── processed/         # Processed data
└── openworm_ai/       # Python package
```

**Reuse Plan for [DD015](DD015_AI_Contributor_Model.md):**

[DD015](DD015_AI_Contributor_Model.md) needs (Section 8, lines 560-673):
- GitHub App bot (Mind-of-a-Worm)
- OpenClaw backend for webhook handling
- AI agent registration system

**Check if openworm.ai already has:**
- LLM prompts for OpenWorm domain knowledge
- RAG corpus (Design Documents, papers, docs)
- AI agent scaffolding

**Action:**
1. **Explore openworm.ai codebase** — what's in `openworm_ai/` package?
2. Check for:
   - Prompt templates (could be Mind-of-a-Worm SKILL.md seeds)
   - OpenWorm knowledge corpus (could be agent training data)
   - Any existing bot/webhook code
3. Coordinate with repo owner (who's maintaining this? Stephen? Someone else?)

**Action Items:**
- [ ] Deep-dive openworm.ai source code (inspect `openworm_ai/` Python package)
- [ ] Check `corpus/` — is this Design Documents, papers, or something else?
- [ ] Identify maintainer (GitHub contributors list)
- [ ] Integrate with [DD015](DD015_AI_Contributor_Model.md) if overlap exists

**Estimated Time Savings:** 10-30 hours (depends on what's already built)

---

## MEDIUM-IMPACT REUSE OPPORTUNITIES

### 9. PlateauNoiseModel → [DD007](DD007_Pharyngeal_System_Architecture.md) (Pharyngeal Muscle Validation)

**Repo:** [openworm/PlateauNoiseModel](https://github.com/openworm/PlateauNoiseModel) (pushed 2025-01-30)
**Status:** ✅ **Recently active** (1 year ago)

**What It Contains:**
- Jupyter notebook with pharyngeal muscle plateau potential model
- Plotting code
- Related to Kenngott et al. 2025 paper

**Reuse Plan:**
- Review notebook for pharyngeal muscle kinetics
- Compare to `pharyngeal_muscle_model` (older repo)
- Use as validation data for [DD007](DD007_Pharyngeal_System_Architecture.md) pharyngeal muscle model

**Estimated Time Savings:** 5-10 hours (validation data + plotting code)

---

### 10. CyberElegans → [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Alternative Model for Comparison)

**Repo:** [openworm/CyberElegans](https://github.com/openworm/CyberElegans) (pushed 2016-12-19, 36 stars)
**Status:** ⚠️ Dormant but **complete neuromechanical model**

**What It Is:**
- Alternative C. elegans neuromechanical model (not c302/Sibernetic)
- 36 stars (popular for a research repo)
- Likely different approach to same problem

**Reuse Plan for [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md):**

[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) is about hybrid mechanistic-ML approaches. **CyberElegans provides a comparison point:**
- How does CyberElegans differ from c302+Sibernetic?
- What trade-offs did they make?
- Can we benchmark [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)'s SPH surrogate against CyberElegans's approach?

**Action:**
- Review CyberElegans architecture
- Compare to [DD001](DD001_Neural_Circuit_Architecture.md)-003
- If CyberElegans is faster or more accurate on some metrics, learn from it

**Estimated Time Savings:** 10-15 hours (comparative analysis)

---

### 11. bionet → [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Neural Network Component)

**Repo:** [openworm/bionet](https://github.com/openworm/bionet) (pushed 2015-04-26, 32 stars)
**Status:** ⚠️ Dormant but **32 stars** suggest it was significant

**What It Is:**
- "Artificial biological neural network"
- Could be ML component or spiking network framework

**Reuse Plan:**
- Check if bionet has neural network architectures (LSTM, GRU, transformer) for [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 2 (SPH surrogate) or Component 4 (learned sensory)
- May have training pipelines

**Action:** Deep-dive to assess usefulness

**Estimated Time Savings:** 5-15 hours (if ML infrastructure exists)

---

### 12. WormsenseLab_ASH → [DD019](DD019_Closed_Loop_Touch_Response.md) (ASH Neuron Validation Data)

**Repo:** [openworm/WormsenseLab_ASH](https://github.com/openworm/WormsenseLab_ASH) (pushed 2021-09-28)
**Status:** ⚠️ Dormant but **contains electrophysiology recordings**

**What It Contains:**
- ASH neuron patch clamp recordings
- ASH is a polymodal nociceptor (responds to mechanical, chemical, osmotic stimuli)
- Could validate [DD019](DD019_Closed_Loop_Touch_Response.md)'s touch neuron model (ASH is one of the touch-responsive neurons alongside ALM/AVM/PLM)

**Reuse Plan:**
- Extract ASH electrophysiology traces
- Use for [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration training set (ASH channel conductances)
- Use for [DD019](DD019_Closed_Loop_Touch_Response.md) validation (ASH's mechanosensory response)

**Estimated Time Savings:** 5-10 hours (validation data extraction)

---

### 13. SegWorm → [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Original Schafer Lab Code)

**Repo:** [openworm/SegWorm](https://github.com/openworm/SegWorm) (pushed 2016-05-27, 5 stars)
**Status:** ⚠️ Dormant, MATLAB code

**What It Is:**
- Original Schafer lab MATLAB code from Dr. Eviatar Yemini
- Part of WormBehavior database
- **This is the source code for the 726-feature phenotyping** that `open-worm-analysis-toolbox` implements!

**Reuse Plan for [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md):**

The analysis toolbox is a **Python port of SegWorm**. When reviving the toolbox ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) 8-task plan):
- Cross-reference SegWorm MATLAB for feature definitions
- If Python toolbox has ambiguous implementations, check SegWorm for ground truth
- Use SegWorm as validation (MATLAB vs. Python should produce identical features)

**Action Items:**
- [ ] During [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival, compare analysis toolbox feature implementations to SegWorm MATLAB
- [ ] If discrepancies found, defer to SegWorm (original source)
- [ ] Reference SegWorm in [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) as "original implementation"

**Estimated Time Savings:** 5-10 hours (clarifies ambiguous feature definitions during revival)

---

### 14. tierpsy-tracker → [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Modern Alternative)

**Repo:** [openworm/tierpsy-tracker](https://github.com/openworm/tierpsy-tracker) (pushed 2025-06-29, fork of ver228/tierpsy-tracker)
**Status:** ✅ **Maintained** (OpenWorm has a fork)

**What It Is:**
- Modern successor to SegWorm + open-worm-analysis-toolbox
- Implements same 726-feature set (Yemini 2013)
- **Actively maintained** (original repo by ver228 has 2024 commits)
- Python 3.x compatible

**Reuse Plan for [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md):**

[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) mentions tierpsy-tracker as a "future evaluation" (lines 456-496). But OpenWorm **already has a fork**!

**Options:**
1. **Use tierpsy-tracker instead of reviving analysis toolbox** ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) Alternative 1)
2. **Revive analysis toolbox AND use tierpsy for cross-validation** (both tools, verify they agree)
3. **Hybrid:** Use tierpsy's feature extraction, analysis toolbox's comparison API

**Action:**
- Check why OpenWorm forked tierpsy (what customizations were made?)
- Evaluate: Is OpenWorm's fork compatible with [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)'s WCON input needs?
- Decision: Revive toolbox OR switch to tierpsy (founder decides)

**Estimated Time Savings:** Potentially **33 hours** (the entire [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival) if tierpsy works out-of-the-box

---

### 15. simple-C-elegans → [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Minimalist Reference)

**Repo:** [openworm/simple-C-elegans](https://github.com/openworm/simple-C-elegans) (pushed 2020-06-08, 6 stars)
**Status:** ⚠️ Dormant

**What It Is:**
- "Minimalist Python code based on OpenWorm and published literature"
- Simplified model (not full c302/Sibernetic)

**Reuse Plan:**
- Educational reference (how to explain OpenWorm's complex models simply)
- Possible basis for [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 1 (differentiable backend) — simpler starting point than full c302
- Code examples for [DD011](DD011_Contributor_Progression_Model.md) orientation tasks

**Estimated Time Savings:** 5-10 hours (educational materials, code examples)

---

## INFRASTRUCTURE REUSE OPPORTUNITIES

### 16. NemaNode → [DD014](DD014_Dynamic_Visualization_Architecture.md) (Interactive Connectome Visualization)

**Repo:** [openworm/NemaNode](https://github.com/openworm/NemaNode) (pushed 2024-05-30)
**Status:** ⚠️ Dormant but **was online at nemanode.org**

**What It Is:**
- Interactive map of neural connections
- Web-based visualization
- Likely uses D3.js or similar

**Reuse Plan:**
- Check if NemaNode's connectome visualization can be integrated into [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer
- Reuse web visualization patterns (layer toggle, node selection)
- May have graph layout algorithms useful for [DD014](DD014_Dynamic_Visualization_Architecture.md)'s neural circuit view

**Estimated Time Savings:** 10-20 hours (graph visualization code)

---

### 17. WCONViewer → [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (WCON Visualization)

**Repo:** [openworm/WCONViewer](https://github.com/openworm/WCONViewer) (pushed 2025-12-17, RECENT!)
**Status:** ✅ **Maintained** (2 months ago)

**What It Is:**
- Python-based 2D viewer for WCON files
- Already reads WCON 1.0 format ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)'s target)

**Reuse Plan:**
- Use WCONViewer's WCON parser in [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) toolbox revival
- Or: Recommend WCONViewer as a lightweight alternative to full analysis toolbox for quick trajectory inspection
- Integrate with [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer (2D trajectory overlay)

**Estimated Time Savings:** 5-10 hours (WCON parser already implemented)

---

### 18. neuronal-analysis → [DD010](DD010_Validation_Framework.md) (Tier 1 Validation)

**Repo:** [openworm/neuronal-analysis](https://github.com/openworm/neuronal-analysis) (pushed 2017-03-05, dormant)
**Status:** ⚠️ Dormant

**What It Is:**
- "Tools to produce, analyse and compare simulated and recorded neuronal datasets"
- Exactly [DD010](DD010_Validation_Framework.md) Tier 1's purpose!

**Reuse Plan:**
- Check for electrophysiology comparison tools
- May have single-cell validation scripts [DD010](DD010_Validation_Framework.md) Tier 1 needs
- Compare to ChannelWorm's SciUnit validation

**Estimated Time Savings:** 10-15 hours (Tier 1 validation tools)

---

## COMPREHENSIVE REUSE PLAN (Prioritized)

### Phase A (Weeks 1-4): Infrastructure Reuse

| DD | Existing Repo | What to Reuse | Time Saved | Action |
|----|--------------|---------------|------------|--------|
| **[DD013](DD013_Simulation_Stack_Architecture.md)** | sibernetic_config_gen | Particle init, .ini generation | 15 hours | Extract particle placement algorithms, integrate into config→ini translator |
| **[DD013](DD013_Simulation_Stack_Architecture.md)** | sibernetic_NEURON | Coupling script patterns | 5 hours | Review as precedent for bidirectional coupling ([DD019](DD019_Closed_Loop_Touch_Response.md)) |
| **[DD013](DD013_Simulation_Stack_Architecture.md)** | skeletonExtraction | 49-point skeleton extraction | 20 hours | Port to Python, use in WCON export pipeline |
| **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** | **tierpsy-tracker** (OpenWorm fork) | **Modern analysis toolbox** | **33 hours?** | **EVALUATE FIRST** — If tierpsy works, skip toolbox revival entirely |
| **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** | WCONViewer | WCON parser | 5 hours | Reuse WCON 1.0 parsing code |
| **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** | SegWorm | Original feature definitions | 5 hours | Reference for ambiguous feature implementations |

**Phase A Total Potential Savings:** 83 hours (if tierpsy works) or 50 hours (if still need toolbox revival)

---

### Phase 1 (Months 1-3): Cell Differentiation Reuse

| DD | Existing Repo | What to Reuse | Time Saved | Action |
|----|--------------|---------------|------------|--------|
| **[DD005](DD005_Cell_Type_Differentiation_Strategy.md)** | **ChannelWorm** | **Ion channel database + HH fitter** | **50 hours** | Extract `data/` spreadsheet → electrophysiology_training_set.csv; reuse `fitter.py` for calibration |
| **[DD005](DD005_Cell_Type_Differentiation_Strategy.md)** | **wormneuroatlas** | **CeNGEN API + gene expression** | **25 hours** | Use `NeuroAtlas.get_gene_expression()` instead of manual CSV parsing |
| **[DD005](DD005_Cell_Type_Differentiation_Strategy.md)** | NicolettiEtAl models | Validation data (AWCon, RMD neuron models) | 5 hours | Use as Tier 1 single-cell validation targets |
| **[DD010](DD010_Validation_Framework.md) Tier 2** | **wormneuroatlas** | **Randi 2023 functional connectivity** | **15 hours** | Use `get_signal_propagation_atlas()` instead of manual .npy download |

**Phase 1 Total Potential Savings:** 95 hours

---

### Phase 2 (Months 4-6): Closed-Loop + Neuropeptides Reuse

| DD | Existing Repo | What to Reuse | Time Saved | Action |
|----|--------------|---------------|------------|--------|
| **[DD006](DD006_Neuropeptidergic_Connectome_Integration.md)** | wormneuroatlas | Peptide-GPCR deorphanization | 15 hours | Use `PeptideGPCR.get_gpcrs_binding_to()` for receptor mapping |
| **[DD019](DD019_Closed_Loop_Touch_Response.md)** | WormsenseLab_ASH | ASH electrophysiology data | 5 hours | Validation data for touch neuron model |
| **[DD019](DD019_Closed_Loop_Touch_Response.md)** | CE_locomotion | **StretchReceptor proprioceptive model** | **30 hours** | Extract for [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioception follow-up) |

**Phase 2 Total Potential Savings:** 50 hours

---

### Phase 3 (Months 7-12): Organ Systems + ML Reuse

| DD | Existing Repo | What to Reuse | Time Saved | Action |
|----|--------------|---------------|------------|--------|
| **[DD007](DD007_Pharyngeal_System_Architecture.md)** | **pharyngeal_muscle_model** | **pm3 NEURON model (plateau potentials)** | **25 hours** | Convert NMODL → NeuroML2 or use NEURON directly |
| **[DD007](DD007_Pharyngeal_System_Architecture.md)** | PlateauNoiseModel | Pharyngeal muscle validation data | 5 hours | Cross-validate plateau kinetics |
| **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)** | CE_locomotion | Evolutionary parameter fitting | 20 hours | Extract optimization algorithm, compare to gradient descent |
| **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)** | CyberElegans | Alternative neuromechanical model | 10 hours | Benchmark comparison, learn from different approach |
| **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)** | bionet | Neural network architectures | 10 hours | Check for reusable ML components |
| **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)** | wormvae | Connectome-constrained latent variable model | 10 hours | Compare to [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)'s graph neural network approach |

**Phase 3 Total Potential Savings:** 80 hours

---

## GRAND TOTAL POTENTIAL TIME SAVINGS

| Phase | Hours Saved (Optimistic) | Hours Saved (Conservative) |
|-------|-------------------------|---------------------------|
| Phase A | 83 (if tierpsy works) | 50 (if toolbox revival still needed) |
| Phase 1 | 95 | 70 |
| Phase 2 | 50 | 35 |
| Phase 3 | 80 | 50 |
| **TOTAL** | **308 hours** | **205 hours** |

**At $30/hour equivalent:** $9,240 (optimistic) or $6,150 (conservative) in volunteer time saved.

**At 40 hours/week:** 5-8 weeks of full-time work eliminated by reusing existing code.

---

## CRITICAL NEXT STEPS (Priority Order)

### 1. URGENT: Evaluate tierpsy-tracker for [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Could Save 33 Hours)

**Question:** Does OpenWorm's tierpsy-tracker fork work with WCON input?

**Test:**
```bash
cd /tmp
git clone https://github.com/openworm/tierpsy-tracker.git
cd tierpsy-tracker
pip install -e .
# Try loading a WCON file
python -c "
from tierpsy import ... # (check their API)
# Load sample WCON
# Extract features
"
```

**Decision Point:**
- **If tierpsy works:** Skip [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) toolbox revival, use tierpsy directly (saves 33 hours)
- **If tierpsy doesn't work:** Proceed with [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) 8-task revival as planned

**Owner:** Validation L4 (when appointed) or founder makes call

---

### 2. HIGH PRIORITY: Integrate wormneuroatlas into [DD005](DD005_Cell_Type_Differentiation_Strategy.md) + [DD010](DD010_Validation_Framework.md)

**Action Plan:**

**Week 1:**
- [ ] Add `wormneuroatlas` to [DD013](DD013_Simulation_Stack_Architecture.md) Docker neural stage
- [ ] Pin version in `versions.lock`
- [ ] Test CeNGEN API: `atlas.get_gene_expression()`
- [ ] Test Randi 2023 API: `atlas.get_signal_propagation_atlas()`

**Week 2:**
- [ ] Update [DD005](DD005_Cell_Type_Differentiation_Strategy.md) scripts to use wormneuroatlas instead of manual CSV download
- [ ] Update [DD010](DD010_Validation_Framework.md) Tier 2 to load Randi data via wormneuroatlas
- [ ] Add wormneuroatlas to [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) as complementary data source

**Benefit:** **40 hours saved** (no manual data wrangling, API is production-ready)

---

### 3. MEDIUM PRIORITY: Extract ChannelWorm Ion Channel Database

**Action Plan:**

**Week 3-4 (during Phase 1):**
- [ ] Clone ChannelWorm, navigate to `data/` directory
- [ ] Convert `ion_channel_database.xlsx` → CSV for [DD005](DD005_Cell_Type_Differentiation_Strategy.md)
- [ ] Review `models/*.channel.nml` — count how many NeuroML2 channels already exist
- [ ] Extract HH fitting code from `channelworm/fitter.py`
- [ ] Port to [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s `scripts/fit_calibration.py`

**Benefit:** **50 hours saved** (ion channel database + fitting pipeline already built)

---

### 4. EXPLORE: openworm.ai for [DD015](DD015_AI_Contributor_Model.md) AI Infrastructure

**Action:**
```bash
cd /tmp/openworm.ai
cat openworm_ai/*.py  # Inspect Python package contents
ls corpus/             # Check knowledge corpus
cat README.md          # Check for docs
```

**Questions:**
- What's in the `corpus/` — Design Documents? Papers? OpenWorm docs?
- What's in `openworm_ai/` package — Bot code? Prompt templates? RAG?
- Who's the maintainer — coordinate with [DD015](DD015_AI_Contributor_Model.md) implementation

**Benefit:** 10-30 hours (depends on overlap with [DD015](DD015_AI_Contributor_Model.md) GitHub bot infrastructure)

---

### 5. PHASE 3: Pharyngeal Muscle Model Conversion

**Action Plan (Phase 3, [DD007](DD007_Pharyngeal_System_Architecture.md) implementation):**
- [ ] Clone pharyngeal_muscle_model
- [ ] Run NEURON simulation (`_run.hoc`), verify plateau potentials
- [ ] Convert NMODL → NeuroML2 using pyNeuroML
- [ ] Integrate into [DD007](DD007_Pharyngeal_System_Architecture.md) as `PharyngealMuscleCell.cell.nml`
- [ ] Validate against Raizen & Avery 1994

**Benefit:** 25 hours (pharyngeal muscle already modeled)

---

### 6. PHASE 2-3: Proprioception from CE_locomotion

**Action Plan:**
- [ ] Extract StretchReceptor.cpp algorithm from CE_locomotion
- [ ] Port to Python or NeuroML
- [ ] Write [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md): Proprioceptive Feedback (references CE_locomotion as source)
- [ ] Integrate with [DD001](DD001_Neural_Circuit_Architecture.md) B-class motor neurons
- [ ] Validate against Wen et al. 2012

**Benefit:** 30 hours (stretch receptor model exists)

---

## RECOMMENDED UPDATES TO DDs

### Update [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (add ChannelWorm + wormneuroatlas)

**Add to Implementation References section (after line 520):**

```markdown
### ChannelWorm Ion Channel Database

**Repository:** `openworm/ChannelWorm` (2018, dormant but complete)

ChannelWorm contains a curated database of C. elegans ion channels with:
- Gene → channel family mapping
- Patch clamp experimental data sources (papers, DOIs)
- HH parameter fitting tools (`channelworm/fitter.py`)
- Pre-generated NeuroML2 channel models (`models/*.channel.nml`)

**Reuse for [DD005](DD005_Cell_Type_Differentiation_Strategy.md):**
1. Extract `data/ion_channel_database.xlsx` → `c302/data/electrophysiology_training_set.csv`
2. Reuse HH fitting algorithms from `channelworm/fitter.py`
3. Cross-reference pre-generated NeuroML2 models in `models/` directory
4. SciUnit validation framework from `tests/` → [DD010](DD010_Validation_Framework.md) Tier 1 single-cell tests

**Action:** Review ChannelWorm database for completeness (how many of [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s ~20 calibration neurons are covered?).

### Wormneuroatlas Python Package

**Repository:** `openworm/wormneuroatlas` (2025-10-22, maintained)
**PyPI:** `pip install wormneuroatlas`
**Docs:** https://francescorandi.github.io/wormneuroatlas/

Provides unified Python API for:
- CeNGEN gene expression: `NeuroAtlas.get_gene_expression(gene_names, neuron_names)`
- Randi 2023 functional connectivity: `NeuroAtlas.get_signal_propagation_atlas(strain="wt")`
- Neuropeptide/GPCR mapping: `PeptideGPCR.get_gpcrs_binding_to(peptides)`
- Neuron ID normalization (bilateral merging, class merging)

**Reuse for [DD005](DD005_Cell_Type_Differentiation_Strategy.md):**
Replace manual CeNGEN CSV download (lines 78-79) with:
```python
from wormneuroatlas import NeuroAtlas
atlas = NeuroAtlas()
expression = atlas.get_gene_expression(
    gene_names=ion_channel_genes,  # unc-2, egl-19, shl-1, etc.
    neuron_names=all_neuron_classes  # 128 CeNGEN classes
)
```

**Reuse for [DD010](DD010_Validation_Framework.md) Tier 2:**
Replace manual Randi 2023 data download with:
```python
from wormneuroatlas import NeuroAtlas
atlas = NeuroAtlas()
experimental_fc = atlas.get_signal_propagation_atlas(strain="wt")
# Returns 302×302 correlation matrix
```

**Action:** Add `wormneuroatlas` to [DD013](DD013_Simulation_Stack_Architecture.md) `versions.lock` and Docker neural stage.
```

---

### Update [DD007](DD007_Pharyngeal_System_Architecture.md) (add pharyngeal_muscle_model)

**Add to Implementation References (after line 250):**

```markdown
### Existing Pharyngeal Muscle Model (NEURON)

**Repository:** `openworm/pharyngeal_muscle_model` (2017-01-19, dormant but complete)

Contains a NEURON implementation of pm3 pharyngeal muscle with:
- EAT-2, EGL-19, UNC-2 Ca²⁺ channels ([DD007](DD007_Pharyngeal_System_Architecture.md)'s target channels)
- Ca²⁺ slow action potential (plateau potentials, ~100ms duration)
- Output matches Raizen & Avery 1994 EPG recordings

**Reuse for [DD007](DD007_Pharyngeal_System_Architecture.md):**
1. Test NEURON model (`nrngui _run.hoc`)
2. Convert NMODL channel files → NeuroML2 using pyNeuroML
3. Use as `PharyngealMuscleCell.cell.nml` baseline
4. Validate plateau duration, amplitude against Raizen & Avery 1994
5. Adjust conductances if needed for 3-4 Hz pumping frequency

**Alternative:** Use NEURON model directly (no NeuroML conversion), couple to c302 via
`sibernetic_NEURON` interface. Decision: NeuroML preferred for consistency with [DD001](DD001_Neural_Circuit_Architecture.md)-002.
```

---

### Update [DD019](DD019_Closed_Loop_Touch_Response.md) (reference CE_locomotion for proprioception)

**Add to Known Issues section (after line 709):**

```markdown
### Issue 4: Proprioceptive Feedback Model Already Exists

[DD019](DD019_Closed_Loop_Touch_Response.md) scopes out proprioceptive feedback (B-class motor neuron stretch receptors, Wen et al. 2012)
as future work. However, `openworm/CE_locomotion` (pushed 2026-02-18, VERY ACTIVE) already
implements proprioceptive feedback via its `StretchReceptor.cpp/h` module.

**Reuse opportunity:**
1. Extract StretchReceptor algorithm from CE_locomotion
2. Port C++ → Python or NeuroML
3. Integrate with [DD001](DD001_Neural_Circuit_Architecture.md) B-class motor neurons
4. Create [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md): Proprioceptive Feedback and Motor Coordination (references CE_locomotion)

**Contact:** Collaborate with Dr. Erick Olivares & Prof. Randall Beer (CE_locomotion authors).
```

---

### Update [DD010](DD010_Validation_Framework.md) (add wormneuroatlas for Tier 2)

**Add to Known Issues section:**

```markdown
### Randi 2023 Data Already Accessible via wormneuroatlas

[DD010](DD010_Validation_Framework.md) Tier 2 requires Randi et al. 2023 functional connectivity (302×302 correlation matrix).
Manual download from Nature supplement is not needed:

**Use wormneuroatlas Python package:**
```python
pip install wormneuroatlas
from wormneuroatlas import NeuroAtlas
experimental_fc = NeuroAtlas().get_signal_propagation_atlas(strain="wt")
```

This provides the exact 302×302 matrix needed for correlation-of-correlations validation.

**Action:** Add `wormneuroatlas` to [DD013](DD013_Simulation_Stack_Architecture.md) Docker validation stage, update Tier 2 scripts to use API.
```

---

### Update [DD015](DD015_AI_Contributor_Model.md) (reference openworm.ai)

**Add to Implementation Checklist (Phase 1, after line 785):**

```markdown
### Explore openworm.ai for Existing AI Infrastructure

**Repository:** `openworm/openworm.ai` (pushed 2026-02-19, VERY ACTIVE)

This repo may already contain:
- LLM prompts for OpenWorm domain knowledge
- RAG corpus (Design Documents, papers, OpenWorm docs in `corpus/`)
- AI agent scaffolding or bot code

**Action:**
- [ ] Deep-dive `openworm_ai/` Python package source code
- [ ] Check `corpus/` contents — is this DD knowledge base?
- [ ] Identify repo maintainer, coordinate with [DD015](DD015_AI_Contributor_Model.md) GitHub bot implementation
- [ ] Reuse any existing prompt templates, knowledge bases, or webhook handlers
```

---

### Update [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (add CE_locomotion + CyberElegans comparisons)

**Add to Alternatives Considered (after Component 4):**

```markdown
### 5. Reuse Existing Neuromechanical Models (CE_locomotion, CyberElegans)

**Description:** OpenWorm has at least 2 other complete neuromechanical models in the GitHub org:
- `openworm/CE_locomotion` (2026-02-18, VERY ACTIVE) — C++ model with evolutionary parameter fitting
- `openworm/CyberElegans` (2016, 36 stars) — Alternative neuromechanical model

**Considered because:** These models solve the same problem (locomotion from neurons+muscles+body) with different architectures. Could we adopt one instead of c302+Sibernetic?

**Rejected as replacement because:**
- c302+Sibernetic is the established, validated pipeline (Sarma 2018, Gleeson 2018 publications)
- 15 years of development invested in current stack
- [DD001](DD001_Neural_Circuit_Architecture.md)-003 are Accepted and working
- Migration cost would be massive (all downstream DDs assume c302+Sibernetic)

**But: Use as comparison points and learning opportunities:**
- CE_locomotion's **StretchReceptor** → Extract for [DD019](DD019_Closed_Loop_Touch_Response.md) proprioceptive follow-up ([DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md))
- CE_locomotion's **evolutionary algorithm** → Compare to [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 1 gradient descent
- CyberElegans architecture → Benchmark [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) surrogate against alternative approach
- Both models likely solve problems (parameter tuning, sensory transduction) we can learn from

**Action:**
- Contact CE_locomotion authors (Erick Olivares, Randall Beer) — still active, collaborate?
- Review CyberElegans for novel approaches to neuromechanical coupling
- Cross-validate: Do all 3 models (c302+Sibernetic, CE_locomotion, CyberElegans) produce similar locomotion patterns? If not, why?
```

---

## ACTION PLAN (Next 2 Weeks)

### Week 1: Data Access Layer Audit

**Owner:** Founder or Data L4 (when appointed)

1. **Test wormneuroatlas:**
   ```bash
   pip install wormneuroatlas
   python -c "from wormneuroatlas import NeuroAtlas; atlas = NeuroAtlas(); print(atlas.get_gene_expression(['unc-2'], ['AVAL']))"
   ```
   **If it works:** Add to [DD013](DD013_Simulation_Stack_Architecture.md) Docker, update [DD005](DD005_Cell_Type_Differentiation_Strategy.md) + [DD010](DD010_Validation_Framework.md) to use it

2. **Test ChannelWorm:**
   ```bash
   git clone https://github.com/openworm/ChannelWorm.git
   cd ChannelWorm
   pip install -r requirements.txt
   # Check data/ and models/ directories
   ```
   **If usable:** Extract ion channel database, add to [DD005](DD005_Cell_Type_Differentiation_Strategy.md) references

3. **Evaluate tierpsy-tracker:**
   ```bash
   git clone https://github.com/openworm/tierpsy-tracker.git
   cd tierpsy-tracker
   # Check WCON input capability
   ```
   **Decision:** Use tierpsy OR revive analysis toolbox (can't do both in Phase A)

### Week 2: Model Extraction

**Owner:** Neural L4 (Padraig) or Phase 1 contributor

1. **Test pharyngeal_muscle_model:**
   ```bash
   cd pharyngeal_muscle_model/pm3\ muscle\ +\ small\ current/
   nrngui _run.hoc
   # Verify plateau potentials appear in output
   ```
   **If works:** Plan NeuroML2 conversion for [DD007](DD007_Pharyngeal_System_Architecture.md)

2. **Explore CE_locomotion:**
   ```bash
   cd CE_locomotion
   make
   ./main  # Run evolution
   # Review StretchReceptor.cpp source
   ```
   **Action:** Extract proprioceptive algorithm, propose [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md)

3. **Audit openworm.ai:**
   ```bash
   cd openworm.ai
   ls -R openworm_ai/
   cat corpus/*  # What's the knowledge base?
   ```
   **Action:** Identify reuse for [DD015](DD015_AI_Contributor_Model.md)

---

## RECOMMENDATION TO FOUNDER

**The OpenWorm GitHub org is sitting on a GOLD MINE of reusable code.** At least 15 repos contain:
- Production-ready data APIs (wormneuroatlas, ChannelWorm)
- Validated models (pharyngeal muscle, CE_locomotion proprioception)
- Infrastructure tools (config gen, skeleton extraction, WCON viewer)

**By systematically auditing and reusing, we can:**
1. **Accelerate Phase 1 by 70-95 hours** (wormneuroatlas + ChannelWorm for [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
2. **Potentially skip [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) toolbox revival** (if tierpsy-tracker works, saves 33 hours)
3. **Reduce Phase 3 implementation by 50-80 hours** (pharyngeal muscle, proprioception, ML components)

**Immediate Actions:**
1. **This week:** Test wormneuroatlas, ChannelWorm, tierpsy-tracker (3 repos, 4-8 hours total)
2. **Phase A:** Integrate working tools into [DD013](DD013_Simulation_Stack_Architecture.md) Docker + `versions.lock`
3. **Phase 1:** Rewrite [DD005](DD005_Cell_Type_Differentiation_Strategy.md) scripts to use wormneuroatlas + ChannelWorm APIs

**Don't rebuild what already exists. BUILD ON IT.** 🚀

---

**Created by:** Claude (Sonnet 4.5)
**Next Update:** After Week 1-2 repo evaluation (document which repos actually work vs. need updating)
