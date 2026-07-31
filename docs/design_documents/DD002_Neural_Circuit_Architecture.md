---
search:
  exclude: true
---

# DD002: Neural Circuit Architecture and Multi-Level Framework

- **Status:** Accepted
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** [DD003](DD003_Muscle_Model_Architecture.md) (Muscle Model), [DD001](DD001_Body_Physics_Architecture.md) (Body Physics), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization), [DD020](DD020_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition), [DD021](DD021_Protein_Foundation_Model_Pipeline.md) (Foundation Model Channel Kinetics), [DD023](DD023_Multicompartmental_Neuron_Models.md) (Multicompartmental Neuron Models)

---

## TL;DR

OpenWorm models the 302-neuron *C. elegans* nervous system using a multi-level [Hodgkin-Huxley](https://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model) conductance-based framework (c302), with Level C1 ([graded synapses](https://en.wikipedia.org/wiki/Graded_potential)) as the default. Graded synapses match worm biology — these neurons do not fire [action potentials](https://en.wikipedia.org/wiki/Action_potential). Success: kinematic validation of emergent locomotion within ±15% of Schafer lab experimental data.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **Layer** | Core Architecture — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **What does this produce?** | [NeuroML](https://www.neuroml.org) network files: `LEMS_c302_C1_*.xml` with 302 neurons, 95 muscles, graded synapses, [gap junctions](https://en.wikipedia.org/wiki/Gap_junction) |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: kinematic metrics within ±15% of Schafer lab [WCON](https://github.com/openworm/tracker-commons) data |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) — issues labeled `dd002` |
| **Config toggle** | `neural.level: C1` / `neural.enabled: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` (per-PR), `docker compose run validate` (pre-merge) |
| **Visualize** | [DD012](DD012_Dynamic_Visualization_Architecture.md) `neural/` layer — 302 neurons with voltage/calcium traces, color-by-activity |
| **CI gate** | Tier 3 kinematic validation blocks merge; `jnml -validate` blocks PR |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Kinematic validation | Forward speed, wavelength, frequency, amplitude, crawling/swimming classification within ±15% of Schafer lab WCON data | Tier 3 (blocking) |
| **Secondary:** Functional connectivity | Calcium correlation matrix comparable to experimental recordings | Tier 2 (blocking) |
| **Tertiary:** NeuroML compliance | All cell models, channels, synapses pass `jnml -validate` | Tier 0 (blocking per-PR) |

**Before:** No whole-nervous-system simulation — neurons modeled individually or not at all.

**After:** 302 neurons in a single [LEMS](https://docs.neuroml.org/Userdocs/LEMS.html) simulation with graded synaptic and gap junction coupling, producing emergent locomotion when coupled to muscle and body physics.

---

## Deliverables

| Artifact | Path (relative to `openworm/c302`) | Format | Example |
|----------|-------------------------------------|--------|---------|
| Generic neuron cell template (Level C/C1) | `c302/c302_GenericCell.py` | Python → NeuroML 2 XML | `GenericCell` with 4 channels |
| Leak channel definition | `channel_models/leak_chan.channel.nml` | NeuroML 2 XML | `leak_chan` |
| K_slow channel definition | `channel_models/k_slow_chan.channel.nml` | NeuroML 2 XML | `k_slow_chan` |
| K_fast channel definition | `channel_models/k_fast_chan.channel.nml` | NeuroML 2 XML | `k_fast_chan` |
| Ca_boyle channel definition | `channel_models/ca_boyle_chan.channel.nml` | NeuroML 2 XML | `ca_boyle_chan` |
| Graded synapse definition | `synapse_models/GradedSynapse.synapse.nml` | NeuroML 2 XML | Level C1 default |
| Event-driven synapse definition | `synapse_models/EventDrivenSynapse.synapse.nml` | NeuroML 2 XML | Level C |
| LEMS network files | `examples/generated/LEMS_c302_C1_*.xml` | LEMS XML | `LEMS_c302_C1_Muscles.xml` |
| Connectome data | ConnectomeToolbox / `cect` package | Python API / CSV | [Cook2019](https://doi.org/10.1038/s41586-019-1352-7), [Witvliet2021](https://doi.org/10.1038/s41586-021-03778-8), [Varshney2011](https://doi.org/10.1371/journal.pcbi.1001066) |
| Neuron voltage time series (viewer) | [OME-Zarr](https://ngff.openmicroscopy.org): `neural/voltage/`, shape (n_timesteps, 302) | OME-Zarr | mV per neuron per timestep |
| Neuron calcium time series (viewer) | OME-Zarr: `neural/calcium/`, shape (n_timesteps, 302) | OME-Zarr | mol/cm³ per neuron per timestep |
| Neuron 3D positions (viewer) | OME-Zarr: `neural/positions/`, shape (302, 3) | OME-Zarr | µm static coordinates |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd002` |
| **Milestone** | Neural Circuit Architecture |
| **Branch convention** | `dd002/description` (e.g., `dd002/graded-synapse-tuning`) |
| **Example PR title** | `DD002: Tune graded synapse parameters for Level C1` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD011](DD011_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, [pyNeuroML](https://github.com/NeuroML/pyNeuroML), [jnml](https://github.com/NeuroML/jNeuroML), [NEURON](https://www.neuron.yale.edu) 8.2.6, [ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox)/`cect`

### Getting Started (Environment Setup)

There are two paths: **Docker** (simpler, recommended for newcomers) and **native Python** (for development).

**Clone the repositories:**

```bash
git clone https://github.com/openworm/c302.git
git clone https://github.com/openworm/sibernetic.git        # for coupled simulation
git clone https://github.com/openworm/OpenWorm.git           # for docker compose
```

**Path A — Docker (recommended for newcomers):**

```bash
cd OpenWorm
docker compose build                 # builds all subsystems
```

Then skip to Step 7 below (`docker compose run quick-test`).

**Path B — Native Python:**

```bash
cd c302
pip install -e .                     # installs c302 + dependencies
pip install pyneuroml neuron         # NeuroML tools + NEURON simulator
pip install connectometoolbox        # cect for connectome data
```

You also need [jNeuroML](https://github.com/NeuroML/jNeuroML) (`jnml`) on your PATH (requires Java). Steps 1–6 below use this native path. Steps 7–8 use Docker.

### Step-by-step

```bash
# Step 1: Validate NeuroML syntax (must pass before PR)
jnml -validate c302/examples/generated/LEMS_c302_C1_Muscles.xml

# Step 2: Run simulation
jnml LEMS_c302_C1_Muscles.xml -nogui

# Step 3a: Fast trajectory screening (Boyle-Cohen 2D model, seconds, no GPU)
python scripts/boyle_berri_cohen_trajectory.py
# [TO BE CREATED] — Boyle, Berri & Cohen 2012 rod-spring model

# Step 3b: Full-fidelity trajectory (requires Sibernetic SPH output)
python scripts/extract_trajectory.py
# [TO BE CREATED] — extracts centerline from ~100K SPH particles

# Step 5: Compare to Schafer lab data
python open-worm-analysis-toolbox/compare_kinematics.py \
    --simulated trajectory_simulated.wcon \
    --real schafer_baseline.wcon \
    --output validation_report.json
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 6: Check that validation score has not degraded
python scripts/check_regression.py validation_report.json baseline_score.json
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 7: Quick coupled simulation (must pass before PR submission)
docker compose run quick-test
# Green light: output/*.wcon file exists (worm moved)
# Green light: output/*.png shows non-flat voltage traces for neurons AND muscles

# Step 8: Full validation (must pass before merge to main)
docker compose run validate
# Green light: Tier 2 functional connectivity r > 0.5
# Green light: Tier 3 kinematic metrics within ±15% of baseline
```

### Scripts that may not exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/boyle_berri_cohen_trajectory.py` | `[TO BE CREATED]` if not present | openworm/c302#TBD |
| `scripts/extract_trajectory.py` | `[TO BE CREATED]` if not present | openworm/c302#TBD |
| `open-worm-analysis-toolbox/compare_kinematics.py` | `[TO BE CREATED]` if not present | openworm/c302#TBD |
| `scripts/check_regression.py` | `[TO BE CREATED]` if not present | openworm/c302#TBD |

### Green light criteria

- `jnml -validate` passes for all NeuroML/LEMS files
- Simulation completes without NaN or voltage explosions
- `output/*.wcon` file exists (worm moved)
- Tier 3 kinematic metrics within ±15% of Schafer lab baseline across 5 key metrics (speed, wavelength, frequency, amplitude, crawling/swimming classification)

---

## How to Visualize

**[DD012](DD012_Dynamic_Visualization_Architecture.md) viewer layer:** `neural/` — 302 neurons with voltage and calcium trace overlays, color-by-activity.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `neural/` |
| **Color mode** | Color-by-activity: voltage or calcium magnitude mapped to warm colormap |
| **Data source** | OME-Zarr: `neural/voltage/` shape (n_timesteps, 302), `neural/calcium/` shape (n_timesteps, 302), `neural/positions/` shape (302, 3) |
| **What you should SEE** | 302 neurons at their 3D positions, colored by instantaneous voltage or calcium concentration. During simulation playback, motor neurons driving dorsal muscles should activate in antiphase to those driving ventral muscles. Sensory neurons should respond to stimulation with graded depolarization, not spikes. |
| **Trace view** | Clicking a neuron shows its voltage and calcium time series. Traces should be smooth and graded (Level C1), not spiking. |

---

## Technical Approach

OpenWorm implements a **multi-level framework (c302)** offering increasing biophysical detail for the same connectome topology, enabling users to choose the appropriate trade-off between simulation complexity and biological realism.

### Architecture Levels

| Level | Name | Cell Type | Biological Realism | Use Case |
|-------|------|-----------|-------------------|----------|
| **A** | [Integrate-and-Fire](https://en.wikipedia.org/wiki/Biological_neuron_model#Leaky_integrate-and-fire) | IafCell (NeuroML) | Low (inappropriate for *C. elegans*) | Topology testing only |
| **B** | Custom IAF + Activity | IafActivityCell | Low-Medium | Community-contributed extensions |
| **C** | Hodgkin-Huxley Conductance-Based | GenericCell (4 channels) | Medium-High | Default working model |
| **C1** | Graded Synapse HH | GenericCell + graded synapses | **High (recommended)** | Sibernetic coupling |
| **D** | Multicompartmental HH | Multicompartment with soma + processes | Highest | NEURON-only, specialized studies |

### Chosen Default: Level C1

**Rationale:**

- Graded synapses match *C. elegans* biology ([Goodman et al. 1998](https://doi.org/10.1016/S0896-6273(00)81014-4))
- Continuous voltage coupling enables realistic sensorimotor feedback via Sibernetic
- Computationally tractable for whole-circuit simulation
- Validated against movement kinematics

### Cell Model Specification (Level C/C1)

**Membrane dynamics (Hodgkin-Huxley formalism):**

```
C * dV/dt = I_leak + I_Kslow + I_Kfast + I_Ca + I_syn + I_gap + I_ext
```

**Ion channels (derived from [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025) muscle model):**

> **Note:** Neuron channel kinetics are currently borrowed from the Boyle & Cohen 2008 *muscle* model because direct neuronal electrophysiology data was scarce at the time of initial implementation. This is a known approximation. A second muscle model (Johnson & Mailler 2015) with one K⁺ and one Ca²⁺ channel has also been incorporated into c302. Both are based on Jospin et al.'s characterization of K⁺ and Ca²⁺ currents in body wall muscle. See [DD005](DD005_Cell_Type_Differentiation_Strategy.md) for the cell-type specialization strategy that addresses this.

| Channel | Type | Neuron g_max | E_rev | Gating | Kinetics |
|---------|------|-------------|-------|--------|----------|
| **Leak** | Non-gated | 0.005 mS/cm² | -50 mV | None | Ohmic |
| **K_slow** | Voltage-gated K⁺ | 3 mS/cm² | -60 mV | m | tau_m(V) |
| **K_fast** | Voltage-gated K⁺ | 0.0711 mS/cm² | -60 mV | m | tau_m(V) fast |
| **Ca_boyle** | Voltage-gated Ca²⁺ | 3 mS/cm² | +40 mV | m, h | tau_m(V), tau_h(V) |

**Calcium dynamics:**
```
d[Ca]/dt = -rho * I_Ca - [Ca]/tau_Ca
```
Where: rho = 0.000238 mol/(C*cm), tau_Ca = 11.5943 ms

**Membrane properties:**

- Initial voltage: -45 mV
- Specific capacitance: 1 µF/cm²
- Cell diameter: 5 µm (single compartment approximation)
- Total membrane area: ~78.5 µm²

**Synaptic transmission (Level C1 graded synapses):**
```
I_syn = g_syn * s * (V_post - E_rev)
ds/dt = k * sigmoid((V_pre - V_th)/delta) * (1 - s) - s/tau_syn
```
Parameters:

- g_syn = 0.09 nS
- delta = 5 mV (sigmoid slope)
- V_th = 0 mV (threshold)
- k = 0.025 ms⁻¹
- tau_syn (decay time constant, synapse-specific)
- E_rev (excitatory or inhibitory)

**Gap junctions:**
```
I_gap = g_gap * (V_neighbor - V)
```

- g_gap = 0.01 nS

### Validated Forward Locomotion Circuit (Gleeson et al. 2018)

The c302 paper demonstrated a working forward locomotion circuit (Figure 3) that successfully generated head-to-tail traveling waves in all 96 body-wall muscle cells. The circuit comprises:

- **Command interneurons:** AVB (AVBL, AVBR) — kept active during forward movement
- **Excitatory motor neurons:** 18 B-type (DB1–DB7 dorsal, VB1–VB11 ventral) — cholinergic, excite downstream muscles
- **Inhibitory motor neurons:** 19 D-type (DD1–DD6 dorsal, VD1–VD13 ventral) — GABAergic, inhibit muscles
- **96 body-wall muscle cells** in 4 quadrants of 24 (MVL24 receives no connections)

**Circuit topology:**

- AVB → B-type motor neurons via **gap junctions**
- DB/VB → muscles via **excitatory chemical synapses**
- DD/VD → muscles via **inhibitory chemical synapses**
- **Cross-inhibition:** DB excites VD and inhibits DD; VB activates DD and inhibits VD
- **Proprioceptive coupling:** Excitatory connections between neighboring DB/VB neurons approximate stretch receptor feedback (Wen et al. 2012), propagating bends posteriorly along the body
- **CPG input:** Periodic current pulses to DB1 and VB1 (hypothesized central pattern generator)
- **Head muscles:** Directly stimulated by synchronized oscillatory current pulses

This circuit produced alternating dorsoventral muscle activation waves propagating from head to tail — the pattern required for forward crawling. The result validates the c302 Level C1 framework as capable of producing locomotion-relevant network dynamics.

### Known Approximations

The current Level C1 model has three known approximations:

- **Uniform channel kinetics:** All 302 neurons share 4 channels borrowed from the muscle model (Boyle & Cohen 2008). See [DD005](DD005_Cell_Type_Differentiation_Strategy.md).
- **Uniform synaptic weights:** All chemical synapses use `g_syn = 0.09 nS`. See [DD013](DD013_Hybrid_Mechanistic_ML_Framework.md).
- **Single compartment:** All neurons are modeled as isopotential spheres. See [DD023](DD023_Multicompartmental_Neuron_Models.md).

---

## Alternatives Considered

### 1. Pure Integrate-and-Fire for All Levels

**Rejected because:** *C. elegans* neurons do not fire action potentials. IAF models produce biologically incorrect all-or-nothing spiking. [Goodman et al. (1998)](https://doi.org/10.1016/S0896-6273(00)81014-4) electrophysiology shows graded, continuous responses.

### 2. AlphaFold-predicted Channel Structures + MD Simulations

**Rejected (for now) because:** While ESM3 and AlphaFold can predict protein structures, converting structures to Hodgkin-Huxley parameters requires electrophysiology data we don't have for most neurons. See [DD005](DD005_Cell_Type_Differentiation_Strategy.md) for how we address this using CeNGEN transcriptomics.

### 3. Detailed Multicompartmental Models for All 302 Neurons

**Rejected because:** Computationally prohibitive and morphological data (dendritic arbor structure) does not exist for all neurons. Reserve Level D for specialized studies of specific well-characterized neurons.

### 4. Simplified Rate Model (Fire Rate Encoding)

**Rejected because:** Throws away voltage dynamics entirely. Cannot couple to Sibernetic body physics, which requires continuous calcium concentration signals to drive muscle contraction.

---

## Quality Criteria

A contribution to the neural circuit model MUST:

1. **Preserve NeuroML 2 / LEMS Compliance:** All cell models, channels, and synapses must be valid NeuroML 2 XML. Use `jnml -validate` before committing.

2. **Maintain Backward Compatibility Across Levels:** Changes to Level C must not break Levels A, B, or D. Each level is a separate NeuroML cell template.

3. **Biophysical Units:** All parameters must have correct units (mV, nS, ms, µm). NeuroML enforces dimensional analysis.

4. **Connectome Topology Preservation:** The connectome structure (adjacency matrices) is defined by [Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7) data in ConnectomeToolbox. Do not edit synapse existence; only edit synapse properties (weights, time constants).

5. **Validation Against Movement Data:** Any change to the default Level C1 model must not degrade the kinematic validation score vs. Schafer lab WCON data. Run `open-worm-analysis-toolbox` before and after the change.

### Validation Procedure (Quick Reference)

```bash
# 1. Validate NeuroML syntax
jnml -validate c302/examples/generated/LEMS_c302_C1_Muscles.xml

# 2. Run simulation
jnml LEMS_c302_C1_Muscles.xml -nogui

# 3a. Fast trajectory screening (Boyle-Cohen 2D model)
python scripts/boyle_berri_cohen_trajectory.py

# 3b. Full-fidelity trajectory (Sibernetic SPH)
python scripts/extract_trajectory.py

# 5. Compare to Schafer lab data
python open-worm-analysis-toolbox/compare_kinematics.py \
    --simulated trajectory_simulated.wcon \
    --real schafer_baseline.wcon \
    --output validation_report.json

# 6. Check that validation score has not degraded
python scripts/check_regression.py validation_report.json baseline_score.json
```

**Acceptance threshold:** Simulated movement must remain within 15% of baseline across 5 key metrics (speed, wavelength, frequency, amplitude, crawling/swimming classification).

---

## Validation Methodology (Per-Cell → Per-Pair → Per-Network)

Neural-circuit changes touch a three-level hierarchy: a single cell's electrophysiology, the pairwise interaction between two coupled cells, and the network-level emergent dynamics. Each level has its own validation workflow — and each follows the cross-tier [Validation Workflow Pattern](DD010_Validation_Framework.md#validation-workflow-pattern) (predict → reference → inspect → refine → implement → tune → render → compare). PRs that modify cell models, synapses, or network topology must address all three levels affected by the change.

### Level 1 — Per-Cell Electrophysiology Validation

**When to apply:** any change to a NeuroML cell template, ion channel kinetics, conductance density, or resting state.

**Reference:** patch-clamp datasets per neuron class. Primary sources: Goodman et al. 2002 (touch receptors), Lindsay et al. 2011 (AVA command interneuron), Liu et al. 2018 (RIM), Suzuki 2003 / Chalasani 2007 (sensory neurons). See [DD010 §Tier 1 datasets](DD010_Validation_Framework.md#tier-1-single-cell-validation-unit-tests).

**8-phase instantiation:**

| Phase | Per-cell activity |
|-------|-------------------|
| 1. Predict | From CeNGEN gene expression for the neuron class, predict resting potential (V_rest), input resistance (R_in), I-V curve shape, calcium response amplitude. Cite which channels (egl-19, unc-2, shk-1, etc.) drive each prediction. |
| 2. Reference | Pull the patch-clamp or calcium-imaging trace for this neuron class from the curated dataset directory. Cite the exact dataset version (`data/goodman2002_v1.2/`, etc.). |
| 3. Inspect | Measure the reference's V_rest, R_in, I-V curve, time constants, spike threshold if applicable. Note any features your prediction missed. |
| 4. Refine | Update the prediction with measured values; these become the acceptance targets per the Tier 1 thresholds (±5 mV V_rest, ±30% R_in, Pearson r>0.8 on I-V curve). |
| 5. Implement | Encode the cell model in NeuroML 2 / LEMS. Validate XML with `jnml -validate`. |
| 6. Tune | If parameters need adjustment, use grid search or NSGA-II (see neurotune / NeuroTune-jr) over conductance densities. Do NOT hand-sweep. Save the optimization log. |
| 7. Render | Plot model V(t), I_Ca(t) overlaid with the reference trace. Standard protocols: V-clamp step, I-clamp ramp, depolarization-evoked Ca²⁺ response. Commit overlay PNG. |
| 8. Compare | Per-metric pass/fail table at the Tier 1 acceptance thresholds. Commit the table + the trace overlay + the optimization log alongside the cell template change. |

**Expression-consistency shortcut for the ~121 classes without patch-clamp data:** instead of comparing to a reference trace, run the [Expression-Consistency Check](DD010_Validation_Framework.md#tier-1-single-cell-validation-unit-tests) defined in DD010. The 8-phase workflow simplifies: prediction is the CeNGEN-derived expected behavior; reference is the gene-expression profile; comparison is whether the cell's electrical signature matches what its expression predicts.

### Level 2 — Per-Pair Synaptic Validation

**When to apply:** any change to synaptic weight, time constant, gap junction conductance, or addition of a new connection.

**Reference:** NMJ EPSP shapes (Richmond & Jorgensen 1999 for cholinergic, McIntire 1993 for GABAergic), specific pairwise recordings where available. Where not, use the connectome-topology constraint (Cook 2019) as a structural reference.

**8-phase instantiation:**

| Phase | Per-pair activity |
|-------|-------------------|
| 1. Predict | From the synapse type (chemical excitatory, chemical inhibitory, gap junction) + count/weight, predict the post-synaptic response: EPSP/IPSP amplitude, time constant, summation behavior under repeated pre-synaptic spikes. |
| 2. Reference | Patch-clamp NMJ recording or analogous pair data. For gap junctions, the symmetric-current criterion (current injected at A causes proportional V change at B and vice versa) is the structural reference. |
| 3. Inspect | Measure reference EPSP amplitude, rise time, decay time constant, reversal potential. |
| 4. Refine | Update synaptic-weight target; identify whether the gap is in the synapse model or in the pre-synaptic spike generation (often the latter — see Level 1 above first). |
| 5. Implement | Add/modify synapse in NeuroML; verify connectivity matches Cook 2019 topology (do not add or remove synapses). |
| 6. Tune | Grid search over synaptic weight + time constants. Constrain to within Cook 2019's reported synapse counts as a scaling factor. |
| 7. Render | Pre- and post-synaptic voltage trace overlay; comparison to reference EPSP shape. Commit PNG. |
| 8. Compare | EPSP amplitude within ±30%; time constants within ±50%; reversal potential within ±5 mV. Commit measurements + plot + tuning log. |

### Level 3 — Per-Network Functional Validation

**When to apply:** any change with cross-cellular reach — cell-type specialization rollouts (DD005), neuromodulator effects (DD006), large-scale parameter retuning. Per [DD010 §Tier 2a](DD010_Validation_Framework.md#tier-2a-integration-tests), this is a blocking gate for merge.

**Reference:** Randi et al. 2023 whole-brain calcium imaging — pairwise functional correlations across ~189 recorded cells (wild-type for Tier 2a; wt-vs-`unc-31` for Tier 2b once DD006 lands).

**8-phase instantiation:**

| Phase | Per-network activity |
|-------|----------------------|
| 1. Predict | From the connectome topology + your changed parameters, predict which neuron pairs should be more/less correlated, and which functional clusters should emerge. |
| 2. Reference | Randi 2023 pairwise correlation matrix (`data/randi2023_v*/correlations.npy`). |
| 3. Inspect | Compute reference correlation-of-correlations: clusters, hub neurons, distance-from-correlation-zero distribution. |
| 4. Refine | Update the predicted correlation pattern with the actual reference structure (often reveals e.g. "I predicted AVA-AVB anti-correlated; data shows them weakly positive — my synapse-sign assumption is wrong"). |
| 5. Implement | Run the full c302 network simulation. Compute the model's pairwise correlation matrix. |
| 6. Tune | Tier 2 acceptance is r > 0.5 (correlation-of-correlations). If under, identify which neuron classes most contribute to the drop (single-cell ablation analysis) and revisit Levels 1 or 2 for those classes. |
| 7. Render | Side-by-side correlation-matrix heatmap: model vs. Randi 2023. Difference heatmap highlights specific pair divergences. Commit PNGs. |
| 8. Compare | Aggregate correlation-of-correlations score with confidence interval; per-pair difference distribution. Commit the heatmap, the score, and the tuning log alongside the network change. |

### Layer 4 — Round-Trip with the Body (Locomotion-Closing Validation)

**When to apply:** any change that touches the neural-to-muscle output ([DD003](DD003_Muscle_Model_Architecture.md)) or that you expect to change behavior. Even cell-internal changes (e.g., command interneuron tuning) should be checked here because of the closed loop.

**Reference:** Yemini et al. 2013 (Schafer lab) — WCON kinematic recordings of wild-type and mutant animals. See [DD010 §Tier 3](DD010_Validation_Framework.md#tier-3-behavioral-validation-system-tests).

This level uses the body-physics validation tooling described in [DD001 §Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology) — the same `dump_metal_trajectory.py` / SGD / render / compare workflow, but with the neural circuit as the upstream driver rather than a fixed muscle-activation file. The neural-circuit change is the parameter being varied; Sibernetic is the simulator; Schafer-lab WCON metrics are the reference.

**Key cross-DD dependency:** as the body substrate is differentiable end-to-end ([DD001 §Differentiability](DD001_Body_Physics_Architecture.md#differentiability)), kinematic-target loss can in principle backpropagate through the body into the muscle activation timing. Once the neural ODE side is also differentiable (deferred to Phase 5 per [DD013](DD013_Hybrid_Mechanistic_ML_Framework.md)), this enables joint neural↔body parameter fitting via SGD. Until then, this layer uses gradient-free tuning (grid search, NSGA-II).

### Mind-of-a-Worm PR Review Checklist (Neural-Circuit-Specific)

When reviewing a DD002 PR, MoaW must verify:

| # | Check | Pass condition |
|---|-------|---------------|
| 1 | **Level identified** | The PR clearly states which level(s) of validation it touches: per-cell, per-pair, per-network, or round-trip. |
| 2 | **Written prediction filed** | For each level touched, the PR includes a prediction derived from the underlying biology (CeNGEN expression for cells, Cook 2019 topology for synapses, connectome + neuromodulation theory for networks) BEFORE the implementation. |
| 3 | **Reference dataset version** | Each level's reference is cited with explicit dataset version path (`data/goodman2002_v1.2/`, `data/randi2023_v*/`, etc.). |
| 4 | **NeuroML validates** | `jnml -validate` passes on any modified cell template, channel, or synapse XML. |
| 5 | **Tier 1 trace overlays** | For per-cell changes, model V(t)/I_Ca(t) trace overlay PNGs committed alongside the cell template. |
| 6 | **Tier 2 correlation heatmap** | For per-network changes, model-vs-Randi heatmap committed; aggregate correlation-of-correlations score in commit message. |
| 7 | **Tier 3 round-trip if behavior could change** | For changes that could affect movement, side-by-side worm-trajectory MP4 + 5-metric pass/fail table. |
| 8 | **Tuning log if parameters changed** | Grid search or NSGA-II convergence log committed; no hand-sweeping. |
| 9 | **Regression check** | `check_regression.py` shows no degradation vs. baseline validation score. |
| 10 | **Topology preservation** | If the PR touches synapses, no edges added or removed vs. Cook 2019 — only properties changed. |

### Common Gotchas (Neural-Circuit-Specific)

1. **Conflating prediction with simulation output.** "I predicted what NEURON gave me" is not a prediction. Predictions must come from biology (CeNGEN expression, channel kinetics, connectome topology) before the simulator runs.
2. **Tuning a single cell to match traces, then breaking the network.** Per-cell validation passes but Tier 2 correlation drops. Always re-run Level 3 after Level 1 tuning.
3. **Adding "missing" synapses to fix correlations.** Cook 2019 is the structural reference. Adjust weights and time constants; do not add edges.
4. **Ignoring the closed-loop body feedback.** Cell-internal changes that look local often shift the muscle output, which shifts the body, which shifts the proprioceptive feedback (when DD019 lands), which shifts the cell input. Run Layer 4 even for "local" cell changes.
5. **Using NEURON's default thresholds as if they were validation thresholds.** NEURON's numerical tolerances are not biological validation criteria. The acceptance thresholds in DD010 are biology-derived; use those.

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Cell-type-specific specialization:** Covered in [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization Using CeNGEN). This document defines the *generic* cell template.

2. **Neuropeptidergic / extrasynaptic signaling:** Covered in [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptidergic Connectome Integration). This document covers only fast synaptic and gap junction transmission.

3. **Sensory transduction:** How mechanosensors, chemosensors, thermosensors convert stimuli to voltage is out of scope. Currently sensory neurons receive generic current injections.

4. **Muscle actuation:** Covered in [DD003](DD003_Muscle_Model_Architecture.md) (Muscle Model). This document defines neuron-to-muscle signaling interface (calcium concentration) but not the muscle dynamics themselves.

5. **Intracellular signaling cascades:** IP3, cAMP, MAPK cascades are future work (Phases 4-5). This document covers membrane voltage and calcium only.

---

## Context & Background

The *C. elegans* nervous system comprises 302 neurons in the hermaphrodite (385 in the male) organized into a well-characterized connectome. OpenWorm must simulate this neural circuit to produce emergent behavior. The challenge: neurons in *C. elegans* primarily use graded potentials and analog transmission rather than action potentials, making integrate-and-fire models biologically inappropriate.

Robert Rosen's work on causal loops in biological systems guides our design philosophy: biological systems contain looping causal relationships, and the behavior-nervous system loop provides a minimal core onto which additional processes can be layered.

---

## Implementation References

### NeuroML Cell Template Location

```
CElegansNeuroML/CElegans/pythonScripts/c302/
├── c302_IafCell.py                # Level A
├── c302_IafActivityCell.py        # Level B
├── c302_GenericCell.py            # Level C/C1  ← PRIMARY
└── c302_MultiComp.py              # Level D
```

### Channel Definitions

```
CElegansNeuroML/CElegans/pythonScripts/c302/channel_models/
├── leak_chan.channel.nml
├── k_slow_chan.channel.nml
├── k_fast_chan.channel.nml
└── ca_boyle_chan.channel.nml
```

### Synapse Definitions

```
CElegansNeuroML/CElegans/pythonScripts/c302/synapse_models/
├── GradedSynapse.synapse.nml      # Level C1 (default)
└── EventDrivenSynapse.synapse.nml  # Level C
```

### Connectome Data Source

```
openworm.org/ConnectomeToolbox
```
Ingests: [Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7) (both sexes), [Witvliet et al. 2021](https://doi.org/10.1038/s41586-021-03778-8) (developmental), Varshney 2011 (original)

---

### Existing Code Resources

**wormneuroatlas** ([openworm/wormneuroatlas](https://github.com/openworm/wormneuroatlas), PyPI: `pip install wormneuroatlas`, maintained 2025):
Provides connectome data, CeNGEN gene expression, and [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity via a unified Python API. Complements `cect` ([DD016](DD016_Connectome_Data_Access_and_Dataset_Policy.md)) with additional datasets.

---

## References

1. **Boyle JH, Cohen N (2008).** "Caenorhabditis elegans body wall muscles are simple actuators." *Biosystems* 94:170-181.
   *Source of channel kinetics.*

2. **[Goodman MB, Hall DH, Avery L, Bhatt R (1998)](https://doi.org/10.1016/S0896-6273(00)81014-4).** "Active currents regulate sensitivity and dynamic range in *C. elegans* neurons." *Neuron* 20:763-772.
   *Evidence for graded potentials.*

3. **Cook SJ et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *Connectome topology.*

4. **[Gleeson P et al. (2018)](https://doi.org/10.1098/rstb.2017.0379).** "c302: a multiscale framework for modelling the nervous system of *Caenorhabditis elegans*." *Phil Trans R Soc B* 373:20170379.
   *c302 architecture paper.*

5. **Rosen R (1991).** *Life Itself: A Comprehensive Inquiry Into the Nature, Origin, and Fabrication of Life.*
   *Causal loop philosophy.*

6. **[Hendricks M, Ha H, Maffey N, Zhang Y (2012)](https://doi.org/10.1038/nature11081).** "Compartmentalized calcium dynamics in a *C. elegans* interneuron encode head movement." *Nature* 487:99-103.
   *Evidence for spatially compartmentalized signaling within individual neurons.*

7. **[Liu Q, Kidd PB, Dobosiewicz M, Bhatt R (2018)](https://doi.org/10.1016/j.cell.2018.08.018).** "*C. elegans* AWA olfactory neurons fire calcium-mediated all-or-none action potentials." *Cell* 175:57-70.e17.
   *Evidence that some C. elegans neurons use action potentials, not just graded signaling.*

8. **[Cannon RC, Gleeson P, Crook S, et al. (2014)](https://doi.org/10.3389/fninf.2014.00079).** "LEMS: a language for expressing complex biological models in concise and hierarchical form and its use in underpinning NeuroML 2." *Front Neuroinform* 8:79.
   *LEMS/NeuroML 2 specification.*

9. **[Haspel G et al. (2023)](https://arxiv.org/abs/2308.06578).** "To reverse engineer an entire nervous system." *arXiv* [q-bio.NC] 2308.06578.
   *White paper arguing for observational and perturbational completeness in C. elegans neuroscience.*

10. **Zhao M, Wang N, Jiang X, et al. (2024).** "An integrative data-driven model simulating *C. elegans* brain, body and environment interactions." *Nature Computational Science* 4(12):978-990.
    *MetaWorm: 136 multicompartmental neurons with 14 ion channel classes, gradient-descent-optimized synaptic weights, FEM body, closed-loop chemotaxis. Open-source: [github.com/Jessie940611/BAAIWorm](https://github.com/Jessie940611/BAAIWorm) (Apache 2.0). Key benchmark for comparison with OpenWorm.*

11. **Kato S, Kaplan HS, Schrödel T, et al. (2015).** "Global brain dynamics embed the motor command sequence of *Caenorhabditis elegans*." *Cell* 163:656-669.
    *PCA of whole-brain dynamics shows forward/backward neuron groups separate on PC1.*

12. **Wang Z, Bhatt D, et al. (2024).** "Neurotransmitter classification from electron microscopy images at synaptic sites in *C. elegans*." *eLife* 13:RP95402.
    *Experimentally determined neurotransmitter identities for all connectome synapses.*

13. **Bargmann CI, Marder E (2013).** "From the connectome to brain function." *Nature Methods* 10:483-490.
    *Argument that connection topology alone is insufficient — connection properties matter for understanding circuit function.*

18. **Johnson C, Mailler R (2015).** "Modeling action potentials of body wall muscles in *C. elegans*: a biologically founded computational approach." *7th Int. Conf. Bioinformat. Comput. Biol.*
    *Second muscle model incorporated into c302 (one K⁺ + one Ca²⁺ channel). Based on Jospin et al. electrophysiology. See [openworm/JohnsonMailler_MuscleModel](https://github.com/openworm/JohnsonMailler_MuscleModel).*

19. **Wen Q et al. (2012).** "Proprioceptive coupling within motor neurons drives *C. elegans* forward locomotion." *Neuron* 76:750-761.
    *B-type motor neurons have stretch-sensitive properties. Basis for proprioceptive coupling between neighboring DB/VB neurons in c302 forward locomotion circuit. See also [DD019](DD019_Proprioceptive_Feedback_and_Motor_Coordination.md).*

---

## Migration Path (If This Decision Changes)

If future research demonstrates that Level C1 graded synapses are insufficient (e.g., specific neurons require action potentials, or detailed dendritic computation is essential):

1. **Upgrade specific neurons to Level D** rather than modifying C1. Backward compatibility is sacred.
2. **Document the biological justification** for which neurons need multicompartmental treatment.
3. **Provide a conversion script** from C1 to Level D for those neurons.
4. **Re-validate** against all existing benchmarks.

Do NOT modify Level C1 unless a critical bug is found.

### Level D: Multicompartmental Cable Equation Models

For neurons where single-compartment approximation is insufficient, Level D multicompartmental models are specified in [DD023](DD023_Multicompartmental_Neuron_Models.md). Level D neurons must still pass all [DD010](DD010_Validation_Framework.md) tiers.

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source | Variable | Format | Units |
|-------|--------|----------|--------|-------|
| Connectome topology (synapses + gap junctions) | ConnectomeToolbox (`cect` package) | Adjacency matrices | Python API / CSV | Neuron pairs + weights |
| Sensory stimulation (external) | `master_openworm.py` orchestrator | `I_ext` current injection per neuron | NeuroML `<pulseGenerator>` | nA |
| CeNGEN expression (when differentiated) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) pipeline | Per-class conductance densities | NeuroML `<channelDensity>` elements | S/cm² |
| Neuropeptide modulation (when enabled) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | `conductance_modulation` per channel | NeuroML `<peptideReceptor>` exposure | dimensionless multiplier |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units | Timestep |
|--------|------------|----------|--------|-------|----------|
| Neuron membrane voltage | [DD003](DD003_Muscle_Model_Architecture.md) (via NMJ synapses) | `V` per neuron | NeuroML state variable | mV | dt_neuron (0.05 ms) |
| Neuron [Ca²⁺]ᵢ | [DD003](DD003_Muscle_Model_Architecture.md) (muscle activation), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (peptide release trigger) | `ca_internal` per neuron | NeuroML state variable | mol/cm³ | dt_neuron (0.05 ms) |
| Muscle [Ca²⁺]ᵢ (via [DD003](DD003_Muscle_Model_Architecture.md) muscle cells in same LEMS simulation) | [DD001](DD001_Body_Physics_Architecture.md) (Sibernetic, via `sibernetic_c302.py`) | `muscle_ca` per muscle | Tab-separated file: muscle_id, timestep, ca_value | mol/cm³ | dt_coupling (0.005 ms) |
| Network activity recordings | [DD010](DD010_Validation_Framework.md) (Tier 2 validation) | `*_calcium.dat`, `*_voltages.dat` | Tab-separated, neuron_id columns × timestep rows | mV or mol | dt_neuron |
| Neuron voltage time series (for viewer) | **[DD012](DD012_Dynamic_Visualization_Architecture.md)** (visualization) | Per-neuron V over all timesteps | OME-Zarr: `neural/voltage/`, shape (n_timesteps, 302) | mV | output_interval |
| Neuron calcium time series (for viewer) | **[DD012](DD012_Dynamic_Visualization_Architecture.md)** (visualization) | Per-neuron [Ca²⁺] over all timesteps | OME-Zarr: `neural/calcium/`, shape (n_timesteps, 302) | mol/cm³ | output_interval |
| Neuron 3D positions | **[DD012](DD012_Dynamic_Visualization_Architecture.md)** (visualization) | Static 3D coordinates for 302 neurons | OME-Zarr: `neural/positions/`, shape (302, 3) | µm | one-time |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository** | `openworm/c302` |
| **Docker stage** | `neural` in multi-stage Dockerfile |
| **`versions.lock` key** | `c302` |
| **Build dependencies** | NEURON 8.2.6 (pip), ConnectomeToolbox/`cect` (pip), pyNeuroML (pip) |

### Configuration

**`openworm.yml` section:**

```yaml
neural:
  enabled: true
  framework: c302
  level: C1                          # A, B, C, C1, C2, D
  differentiated: false              # Phase 3 ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)): CeNGEN cell-type specialization
  neuropeptides: false               # Phase 4 ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)): peptidergic modulation
  connectome_dataset: "Cook2019"     # Cook2019, Witvliet2021, Varshney2011
  data_reader: "UpdatedSpreadsheetDataReader2"
  reference: "FW"                    # FW (forward crawl), BA (backward), TU (turning)
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `neural.enabled` | `true` | `true`/`false` | Enable neural circuit simulation |
| `neural.framework` | `c302` | `c302` | Neural framework (only c302 currently) |
| `neural.level` | `C1` | `A`, `B`, `C`, `C1`, `C2`, `D` | Biophysical detail level |
| `neural.differentiated` | `false` | `true`/`false` | Enable CeNGEN cell-type specialization ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) |
| `neural.neuropeptides` | `false` | `true`/`false` | Enable peptidergic modulation ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) |
| `neural.connectome_dataset` | `"Cook2019"` | `"Cook2019"`, `"Witvliet2021"`, `"Varshney2011"` | Connectome data source |
| `neural.data_reader` | `"UpdatedSpreadsheetDataReader2"` | String | Data reader class |
| `neural.reference` | `"FW"` | `"FW"`, `"BA"`, `"TU"` | Behavior reference (forward, backward, turning) |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
docker compose run quick-test
# Checks: output/*.wcon file exists (worm moved)
# Checks: output/*.png shows non-flat voltage traces for neurons AND muscles

# Full validation (must pass before merge to main)
docker compose run validate
# Checks:
#   - Tier 2: functional connectivity r > 0.5
#   - Tier 3: kinematic metrics within ±15% of baseline
```

**Per-PR checklist:**

- [ ] `jnml -validate` passes for all modified NeuroML/LEMS files
- [ ] `docker compose run quick-test` passes (worm moves, non-flat traces)
- [ ] `docker compose run validate` passes (Tier 2 + Tier 3)
- [ ] No changes to connectome topology (synapse existence) without explicit justification
- [ ] All parameters have correct biophysical units

### How to Visualize ([DD012](DD012_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `neural/voltage/` (n_timesteps, 302) | Voltage traces | Standard mV colormap |
| `neural/calcium/` (n_timesteps, 302) | Calcium activity | Warm colormap (blue→red) |
| `neural/positions/` (302, 3) | 3D neuron positions | Static spatial layout |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| ConnectomeToolbox data | (external) | Synapse counts or neuron IDs change → network topology changes |
| CeNGEN expression data | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Calibration parameters change → all conductance densities shift |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Muscle activation | [DD003](DD003_Muscle_Model_Architecture.md) | If neuron→muscle synaptic output changes, muscle calcium dynamics change |
| Body physics | [DD001](DD001_Body_Physics_Architecture.md) | If muscle calcium output format/units change, `sibernetic_c302.py` coupling breaks |
| Neuropeptide release | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | If `ca_internal` variable name or units change, peptide release triggers break |
| Tier 2 validation | [DD010](DD010_Validation_Framework.md) | If calcium recording file format changes, validation scripts break |

### Coupling Bridge Ownership

The `sibernetic_c302.py` script (in the Sibernetic repo) implements the [DD002](DD002_Neural_Circuit_Architecture.md)→[DD003](DD003_Muscle_Model_Architecture.md)→[DD001](DD001_Body_Physics_Architecture.md) coupling chain. It reads c302/NEURON calcium output and writes Sibernetic muscle activation input. **Any change to calcium output format or variable naming in c302 must be coordinated with the Sibernetic maintainer ([DD001](DD001_Body_Physics_Architecture.md)) and the Integration Maintainer ([DD011](DD011_Simulation_Stack_Architecture.md)).**

### Joint Neural ↔ Body Parameter Fitting (Forward Reference)

The native Sibernetic substrate is end-to-end differentiable ([DD001 §Differentiability](DD001_Body_Physics_Architecture.md#differentiability)) — gradients on `(spring_K, viscosity, density compliance, …)` are available via `xpbd_full_bwd`. As the c302/NEURON pipeline gains a differentiable substrate of its own (currently future work tracked under [DD013](DD013_Hybrid_Mechanistic_ML_Framework.md)), joint optimization becomes possible: muscle activation timing, calcium-to-force scaling, and per-muscle-unit strength can be tuned end-to-end against kinematic targets ([DD010](DD010_Validation_Framework.md) Tier 3 metrics) rather than via manual sweeps. This is a Phase 5 capability gated on the neural-side substrate, not a current deliverable of this DD.

---

- **Approved by:** OpenWorm Steering
- **Implementation Status:** Complete (c302 Levels A-D exist)
- **Next Review:** After Phase 3 cell-type specialization (see [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
