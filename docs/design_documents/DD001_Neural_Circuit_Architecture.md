# DD001: Neural Circuit Architecture and Multi-Level Framework

- **Status:** Accepted
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD003](DD003_Body_Physics_Architecture.md) (Body Physics), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation), [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition), [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (Foundation Model Channel Kinetics)

---

## TL;DR

OpenWorm models the 302-neuron *C. elegans* nervous system using a multi-level Hodgkin-Huxley conductance-based framework (c302), with Level C1 (graded synapses) as the default. Graded synapses match worm biology — these neurons do not fire action potentials. Success: kinematic validation of emergent locomotion within ±15% of Schafer lab experimental data.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **Layer** | Core Architecture — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **What does this produce?** | NeuroML network files: `LEMS_c302_C1_*.xml` with 302 neurons, 95 muscles, graded synapses, gap junctions |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: kinematic metrics within ±15% of Schafer lab WCON data |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) — issues labeled `dd001` |
| **Config toggle** | `neural.level: C1` / `neural.enabled: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` (per-PR), `docker compose run validate` (pre-merge) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `neural/` layer — 302 neurons with voltage/calcium traces, color-by-activity |
| **CI gate** | Tier 3 kinematic validation blocks merge; `jnml -validate` blocks PR |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Kinematic validation | Forward speed, wavelength, frequency, amplitude, crawling/swimming classification within ±15% of Schafer lab WCON data | Tier 3 (blocking) |
| **Secondary:** Functional connectivity | Calcium correlation matrix comparable to experimental recordings | Tier 2 (blocking) |
| **Tertiary:** NeuroML compliance | All cell models, channels, synapses pass `jnml -validate` | Tier 0 (blocking per-PR) |

**Before:** No whole-nervous-system simulation — neurons modeled individually or not at all.

**After:** 302 neurons in a single LEMS simulation with graded synaptic and gap junction coupling, producing emergent locomotion when coupled to muscle and body physics.

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
| Neuron voltage time series (viewer) | OME-Zarr: `neural/voltage/`, shape (n_timesteps, 302) | OME-Zarr | mV per neuron per timestep |
| Neuron calcium time series (viewer) | OME-Zarr: `neural/calcium/`, shape (n_timesteps, 302) | OME-Zarr | mol/cm³ per neuron per timestep |
| Neuron 3D positions (viewer) | OME-Zarr: `neural/positions/`, shape (302, 3) | OME-Zarr | µm static coordinates |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd001` |
| **Milestone** | Neural Circuit Architecture |
| **Branch convention** | `dd001/description` (e.g., `dd001/graded-synapse-tuning`) |
| **Example PR title** | `DD001: Tune graded synapse parameters for Level C1` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, NEURON 8.2.6, ConnectomeToolbox/`cect`

### Step-by-step

```bash
# Step 1: Validate NeuroML syntax (must pass before PR)
jnml -validate c302/examples/generated/LEMS_c302_C1_Muscles.xml

# Step 2: Run simulation
jnml LEMS_c302_C1_Muscles.xml -nogui

# Step 3: Extract movement trajectory
python scripts/extract_trajectory.py
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 4: Compare to Schafer lab data
python open-worm-analysis-toolbox/compare_kinematics.py \
    --simulated trajectory_simulated.wcon \
    --real schafer_baseline.wcon \
    --output validation_report.json
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 5: Check that validation score has not degraded
python scripts/check_regression.py validation_report.json baseline_score.json
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 6: Quick coupled simulation (must pass before PR submission)
docker compose run quick-test
# Green light: output/*.wcon file exists (worm moved)
# Green light: output/*.png shows non-flat voltage traces for neurons AND muscles

# Step 7: Full validation (must pass before merge to main)
docker compose run validate
# Green light: Tier 2 functional connectivity r > 0.5
# Green light: Tier 3 kinematic metrics within ±15% of baseline
```

### Scripts that may not exist yet

| Script | Status | Tracking |
|--------|--------|----------|
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

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** `neural/` — 302 neurons with voltage and calcium trace overlays, color-by-activity.

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
| **A** | Integrate-and-Fire | IafCell (NeuroML) | Low (inappropriate for *C. elegans*) | Topology testing only |
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

> **Note:** Neuron channel kinetics are currently borrowed from the Boyle & Cohen 2008 *muscle* model because direct neuronal electrophysiology data was scarce at the time of initial implementation. This is a known approximation. A second muscle model (Johnson & Mailler 2015) with one K⁺ and one Ca²⁺ channel has also been incorporated into c302. Both are based on Jospin et al.'s characterization of K⁺ and Ca²⁺ currents in body wall muscle. [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation) will replace these generic parameters with neuron-class-specific conductances derived from CeNGEN expression data and the ChannelWorm ion channel database.

### Protein Foundation Model Pathway for Channel Kinetics

The ~4 generic channels above are a starting point. [DD005](DD005_Cell_Type_Differentiation_Strategy.md) replaces them with cell-type-specific conductances from CeNGEN transcriptomics, but the mapping from transcript → conductance remains approximate. A complementary approach uses protein foundation models to predict channel kinetics directly from sequence:

1. **Protein structure prediction:** [AlphaFold 3](https://github.com/google-deepmind/alphafold3) or [Boltz-2](https://github.com/jwohlwend/boltz) predict 3D structures of *C. elegans* ion channels (EGL-19, UNC-2, SHL-1, etc.) from amino acid sequence alone, including bound ions and lipids
2. **Conformational dynamics:** [BioEmu-1](https://github.com/microsoft/BioEmu) (Microsoft) simulates ion channel conformational ensembles at 100,000x the speed of molecular dynamics, enabling prediction of gating transitions (open ↔ closed) from which V_half, slope factor, and tau can be extracted
3. **Sequence embeddings:** [ESM Cambrian](https://github.com/evolutionaryscale/esm) protein language models encode channel sequences into representations that capture functional properties across homologous channel families, enabling transfer from well-characterized mammalian channels to *C. elegans* orthologs

This pipeline is specified in detail in [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (Protein Foundation Model Pipeline for Ion Channel Kinetics). If successful, it would expand the number of neuron classes with predicted kinetics from ~7 (limited by patch-clamp data) to all 128 (limited only by sequence availability).

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

### Synaptic Weight and Polarity Optimization

The uniform `g_syn = 0.09 nS` used above is a baseline placeholder for the undifferentiated model. Zhao et al. (2024) demonstrated that per-synapse conductances and excitatory/inhibitory polarity assignments can be optimized via gradient descent to match the experimentally measured whole-brain functional connectivity matrix. Targeting the Pearson correlation matrix of 65 identified neurons from whole-brain calcium imaging, they achieved a mean squared error of 0.076 between simulated and experimental correlation maps — far better than hand-tuned uniform weights.

OpenWorm will adopt this optimization approach using the differentiable simulation backend ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 1), with two key improvements over the Zhao et al. approach:

1. **Neurotransmitter identity constraints.** Rather than allowing the optimizer to freely assign excitatory/inhibitory polarities, we will constrain synapse signs using experimentally determined neurotransmitter identities. Wang et al. (2024) classified neurotransmitter usage for every neuron in the connectome from EM images — known glutamatergic, cholinergic, and GABAergic identities should not be overridden by the optimizer. This produces a biologically grounded optimization that explains *why* a synapse is excitatory or inhibitory, not just that it is.

2. **Full 302-neuron optimization.** Zhao et al. optimized a 136-neuron locomotion subcircuit. OpenWorm will optimize the complete 302-neuron network, leveraging the full Randi et al. (2023) functional connectivity matrix (accessible via `wormneuroatlas`). This captures circuit interactions that the locomotion-only subcircuit cannot.

**Validation:** After optimization, principal component analysis (PCA) of simulated membrane potential time series should show forward-locomotion neurons (AVB, PVC, VB, DB classes) and backward-locomotion neurons (AVA, AVD, VA, DA classes) separating on PC1, matching the low-dimensional dynamical structure observed in whole-brain calcium imaging (Kato et al. 2015).

**Configuration:** `neural.synapse_optimization: true/false` in `openworm.yml`. When `false`, the baseline uniform `g_syn` is used (backward compatible). When `true`, per-synapse fitted values from the optimization are loaded.

**Phase:** 1-2 (requires [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) differentiable backend as prerequisite).

### Extended Ion Channel Library (Phase 1-2)

The current 4-channel model (leak, K_slow, K_fast, Ca_boyle) is derived from muscle electrophysiology (Boyle &amp; Cohen 2008) and does not capture the diversity of neuronal ion channel kinetics. Zhao et al. (2024) demonstrated that 14 ion channel classes, when combined in neuron-class-specific ratios, produce substantially better fits to published single-neuron electrophysiology. Their open-source NMODL channel files ([BAAIWorm `eworm/` directory](https://github.com/Jessie940611/BAAIWorm), Apache 2.0 license) can potentially be converted to NeuroML channel definitions using pyNeuroML's NMODL converter, saving significant development effort.

**Target channel library (Phase 1-2):**

| Channel | C. elegans Gene(s) | Family | Type | Priority | BAAIWorm NMODL? |
|---------|-------------------|--------|------|----------|----------------|
| Leak | generic | Passive | Leak | ✅ Exists | ✅ |
| K_slow | shk-1 | Kv | Outward | ✅ Exists | ✅ SHK-1 |
| K_fast | shl-1 | Kv | Outward | ✅ Exists | ✅ SHL-1 |
| Ca_boyle | generic Ca²⁺ | Cav | Inward | ✅ Exists | ✅ UNC2 |
| **Cav1 (L-type)** | egl-19 | Cav | Inward | HIGH | ✅ EGL19 |
| **Cav3 (T-type)** | cca-1 | Cav | Inward | MEDIUM | ✅ CCA1 |
| **Kv (Shaker)** | kvs-1 | Kv | Outward | HIGH | ✅ KVS-1 |
| **Kv (EAG)** | egl-2 | Kv | Outward | MEDIUM | ✅ EGL-2 |
| **Kv (KCNQ)** | kqt-3 | Kv | Outward | MEDIUM | ✅ KQT-3 |
| **ERG** | egl-36 | Kv | Outward | HIGH | ✅ EGL-36 |
| **BK (Ca²⁺-activated K⁺)** | slo-1 | KCa | Outward | HIGH | ✅ SLO1 |
| **SK (Ca²⁺-activated K⁺)** | slo-2 | KCa | Outward | MEDIUM | ✅ SLO2 |
| **SK (KCNL)** | kcnl-2 | KCa | Outward | MEDIUM | ✅ KCNL |
| **IRK (inward rectifier)** | irk-1, irk-3 | Kir | Inward | MEDIUM | ✅ IRK1/3 |
| **NCA (Na⁺ leak)** | nca-1, nca-2 | Na | Inward | MEDIUM | ✅ NCA |

**Code reuse plan:** (1) Download BAAIWorm NMODL channel files from `eworm/` directory → (2) Convert to NeuroML using `pyNeuroML` NMODL→NeuroML converter → (3) Validate each channel with `jnml -validate` → (4) Integrate into c302 channel library at `channel_models/` → (5) Map each channel to CeNGEN genes for [DD005](DD005_Cell_Type_Differentiation_Strategy.md) expression-based calibration.

**OpenWorm extends beyond Zhao et al.:** We assign channels to neuron classes via CeNGEN single-cell transcriptomics ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)), not just by functional group membership. This is more biologically grounded — two neurons in the same functional group (e.g., interneurons) may express very different channel complements based on their transcriptomic profiles.

### Spatially Resolved Synapse Placement (Phase 2, with Level E)

For the single-compartment models (Levels A-D, C1), synapses are abstract neuron-to-neuron connections with no spatial structure — all inputs sum at the single compartment. However, for multicompartmental neurons (Level E), the location of synapses along neurites matters because it determines signal propagation delays, spatial input integration, and the degree to which nearby synapses interact nonlinearly.

Zhao et al. (2024) demonstrated a practical approach: for each connection in the Cook et al. (2019) adjacency matrix, assign a distance along the neurite drawn from an inverse Gaussian distribution fitted to experimental synapse centroid distance measurements from serial-section EM (Witvliet et al. 2021). Each synapse is then placed on the neurite segment closest to the assigned distance. This produces spatially realistic clustering of synapses along neurites, matching the biological organization observed in EM.

OpenWorm will adopt this approach with one improvement: quantitative validation that the constructed distributions match the experimental distributions (as in Zhao et al. Fig. 4B-C), integrated into [DD010](DD010_Validation_Framework.md) Tier 1 as a non-blocking structural validation.

**Applies only when:** `neural.level: E` and `neural.spatial_synapses: true`. For Level C1, synapse placement is irrelevant and this feature is disabled.

**Data requirement:** Synapse centroid distances from Witvliet et al. 2021, to be acquired per [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition Pipeline). See also [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) for ConnectomeToolbox data access.

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

### Validation Procedure

```bash
# 1. Validate NeuroML syntax
jnml -validate c302/examples/generated/LEMS_c302_C1_Muscles.xml

# 2. Run simulation
jnml LEMS_c302_C1_Muscles.xml -nogui

# 3. Extract movement trajectory
python scripts/extract_trajectory.py

# 4. Compare to Schafer lab data
python open-worm-analysis-toolbox/compare_kinematics.py \
    --simulated trajectory_simulated.wcon \
    --real schafer_baseline.wcon \
    --output validation_report.json

# 5. Check that validation score has not degraded
python scripts/check_regression.py validation_report.json baseline_score.json
```

**Acceptance threshold:** Simulated movement must remain within 15% of baseline across 5 key metrics (speed, wavelength, frequency, amplitude, crawling/swimming classification).

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Cell-type-specific differentiation:** Covered in [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation Using CeNGEN). This document defines the *generic* cell template.

2. **Neuropeptidergic / extrasynaptic signaling:** Covered in [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptidergic Connectome Integration). This document covers only fast synaptic and gap junction transmission.

3. **Sensory transduction:** How mechanosensors, chemosensors, thermosensors convert stimuli to voltage is out of scope. Currently sensory neurons receive generic current injections.

4. **Muscle actuation:** Covered in [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model). This document defines neuron-to-muscle signaling interface (calcium concentration) but not the muscle dynamics themselves.

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
Provides connectome data, CeNGEN gene expression, and [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity via a unified Python API. Complements `cect` ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) with additional datasets.

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
   *Evidence for spatially compartmentalized signaling within individual neurons — motivates multicompartmental Level E.*

7. **[Liu Q, Kidd PB, Dobosiewicz M, Bhatt R (2018)](https://doi.org/10.1016/j.cell.2018.08.018).** "*C. elegans* AWA olfactory neurons fire calcium-mediated all-or-none action potentials." *Cell* 175:57-70.e17.
   *Evidence that some C. elegans neurons use action potentials, not just graded signaling — motivates neuron-class-specific model complexity.*

8. **[Cannon RC, Gleeson P, Crook S, et al. (2014)](https://doi.org/10.3389/fninf.2014.00079).** "LEMS: a language for expressing complex biological models in concise and hierarchical form and its use in underpinning NeuroML 2." *Front Neuroinform* 8:79.
   *LEMS/NeuroML 2 specification — supports multicompartmental morphologies natively.*

9. **[Linka K, Pierre SRS, Kuhl E (2023)](https://doi.org/10.1016/j.actbio.2023.01.055).** "Automated model discovery for human brain using Constitutive Artificial Neural Networks." *Acta Biomater*.
   *RNN-based approach for inferring biophysical parameters from experimental recordings — applicable to cable equation fitting.*

10. **Alon S et al. (2021).** "Expansion sequencing: spatially precise in situ transcriptomics in intact biological systems." *Science* 371.
    *In-situ sequencing at subcellular resolution — future data source for spatially resolved channel densities in Level E models.*

11. **[Shaib AH et al. (2023)](https://doi.org/10.1038/s41587-024-02431-9).** "*C. elegans*-optimized Expansion Microscopy." ExM with 20-fold expansion for nanoscale molecular mapping.
    *Future data source for synapse-level molecular identity and subcellular protein localization.*

12. **[Haspel G et al. (2023)](https://arxiv.org/abs/2308.06578).** "To reverse engineer an entire nervous system." *arXiv* [q-bio.NC] 2308.06578.
    *White paper arguing for observational and perturbational completeness in C. elegans neuroscience — conceptual alignment with OpenWorm's whole-organism approach.*

13. **Zhao M, Wang N, Jiang X, et al. (2024).** "An integrative data-driven model simulating *C. elegans* brain, body and environment interactions." *Nature Computational Science* 4(12):978-990.
    *MetaWorm: 136 multicompartmental neurons with 14 ion channel classes, gradient-descent-optimized synaptic weights (MSE 0.076 vs experiment), FEM body at 30 FPS, closed-loop chemotaxis. Open-source: [github.com/Jessie940611/BAAIWorm](https://github.com/Jessie940611/BAAIWorm) (Apache 2.0). Key benchmark for OpenWorm — we extend beyond MetaWorm with 302 neurons, organ systems, neuropeptidergic signaling, and NeuroML standard format.*

14. **Kato S, Kaplan HS, Schrödel T, et al. (2015).** "Global brain dynamics embed the motor command sequence of *Caenorhabditis elegans*." *Cell* 163:656-669.
    *PCA of whole-brain dynamics shows forward/backward neuron groups separate on PC1 — validation target for synapse optimization.*

15. **Wang Z, Bhatt D, et al. (2024).** "Neurotransmitter classification from electron microscopy images at synaptic sites in *C. elegans*." *eLife* 13:RP95402.
    *Experimentally determined neurotransmitter identities for all connectome synapses — constrains synapse polarity optimization.*

16. **Nicoletti M et al. (2019).** "Biophysical modeling of *C. elegans* neurons: Single ion currents and whole-cell dynamics of AWCon and RMD." *PLoS ONE* 14:e0218738.
    *Multicompartmental AWC model with multiple ion channel types — precedent for Level E single-neuron models.*

17. **Bargmann CI, Marder E (2013).** "From the connectome to brain function." *Nature Methods* 10:483-490.
    *Argument that connection topology alone is insufficient — connection properties including spatial location and strength matter for understanding circuit function.*

18. **Johnson C, Mailler R (2015).** "Modeling action potentials of body wall muscles in *C. elegans*: a biologically founded computational approach." *7th Int. Conf. Bioinformat. Comput. Biol.*
    *Second muscle model incorporated into c302 (one K⁺ + one Ca²⁺ channel). Based on Jospin et al. electrophysiology. See [openworm/JohnsonMailler_MuscleModel](https://github.com/openworm/JohnsonMailler_MuscleModel).*

19. **Wen Q et al. (2012).** "Proprioceptive coupling within motor neurons drives *C. elegans* forward locomotion." *Neuron* 76:750-761.
    *B-type motor neurons have stretch-sensitive properties. Basis for proprioceptive coupling between neighboring DB/VB neurons in c302 forward locomotion circuit. See also [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md).*

---

## Migration Path (If This Decision Changes)

If future research demonstrates that Level C1 graded synapses are insufficient (e.g., specific neurons require action potentials, or detailed dendritic computation is essential):

1. **Add a new level (e.g., Level E)** rather than modifying C1. Backward compatibility is sacred.
2. **Document the biological justification** in a new DD.
3. **Provide a conversion script** from C1 to the new level.
4. **Re-validate** against all existing benchmarks.

Do NOT modify Level C1 unless a critical bug is found.

### Level E: Multicompartmental Cable Equation Models

Experimental evidence shows that single-compartment (isopotential) models are insufficient for a subset of *C. elegans* neurons. [Hendricks et al. (2012)](https://doi.org/10.1038/nature11081) demonstrated that calcium dynamics in the RIA interneuron are compartmentalized across distinct segments of the neurite, encoding head movement direction through spatially separated signals within a single cell. [Liu et al. (2018)](https://doi.org/10.1016/j.cell.2018.08.018) showed that AWA olfactory neurons fire calcium-mediated all-or-none action potentials — a fundamentally different signaling mode from the graded potentials assumed by Level C1. These findings indicate that model complexity must vary among neurons: some are well-described by the single-compartment approximation, while others require multicompartmental representations that capture signal propagation along neurites.

**NeuroML 2 natively supports multicompartmental morphologies.** The `<cell>` element can contain a `<morphology>` with multiple `<segment>` elements organized into `<segmentGroup>` definitions, with per-segment channel density assignments. This means Level E can be implemented within the existing NeuroML/LEMS framework without a new file format — the same `jnml -validate` pipeline applies, and the same NEURON simulator backend can execute multicompartmental cells alongside single-compartment ones in the same network simulation ([Cannon et al. 2014](https://doi.org/10.3389/fninf.2014.00079); [Gleeson et al. 2018](https://doi.org/10.1098/rstb.2017.0379)).

**Feasibility demonstrated.** Zhao et al. (2024) showed that the "representative neuron" strategy makes multicompartmental modeling tractable at scale: build detailed models for a small set of representative neurons (one per functional group), fit them to published electrophysiology, then propagate fitted parameters to all neurons in the same functional class. Using this approach with 5 representative neurons (AWC, AIY, AVA, RIM, VD5), they produced 136 multicompartmental neurons whose I-V curves matched experimental recordings. Nicoletti et al. (2019) earlier demonstrated a similar multicompartmental approach for AWCon with multiple ion channel types. This establishes that Level E is achievable with current data — it does not require waiting for new experimental techniques.

**Code reuse opportunity.** The BAAIWorm repository ([github.com/Jessie940611/BAAIWorm](https://github.com/Jessie940611/BAAIWorm), Apache 2.0 license) contains NMODL ion channel files and SWC neuron morphology reconstructions. These can be converted to NeuroML format using pyNeuroML's NMODL→NeuroML converter, providing a head start on the channel library expansion and morphological models.

**Implementation pathway (two stages):**

**Stage 1 (Phase 2 — Proof of Concept):**

1. Select 5 representative neurons with published morphological reconstructions AND published electrophysiology: AWC (sensory), AIY (interneuron), AVA (command interneuron), RIM (interneuron), VD5 (motor neuron) — the same set validated by Zhao et al. (2024)
2. Obtain morphologies from EM reconstructions (Witvliet et al. 2021; Cook et al. 2019) or from BAAIWorm SWC files; convert to NeuroML `<morphology>` elements with segments < 2 μm
3. Assign per-segment channel densities from the Extended Channel Library (14 classes), guided by CeNGEN expression profiles ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) and functional group membership
4. Optimize passive parameters (axial resistance, membrane capacitance) and channel densities using automated fitting ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) differentiable backend or NEURON's built-in optimizer) to match published I-V curves and current-clamp responses
5. Propagate fitted parameters to all neurons in the same CeNGEN functional class, scaling channel densities by expression level ([DD005](DD005_Cell_Type_Differentiation_Strategy.md))

**Stage 2 (Phase 4-5 — Scale to Full Circuit):**

1. Extend to all 302 neurons using the representative-neuron approach
2. Incorporate subcellular molecular data from expansion microscopy (Alon et al. 2021; [Shaib et al. 2023](https://doi.org/10.1038/s41587-024-02431-9)) as it becomes available
3. Apply spatially resolved synapse placement (see section above)
4. Infer parameters using data-constrained fitting methods including RNN-based approaches ([Linka et al. 2023](https://doi.org/10.1016/j.actbio.2023.01.055))

**OpenWorm extends beyond Zhao et al.:** (a) We target all 302 neurons, not 136; (b) we use NeuroML standard format enabling multi-simulator support and community sharing; (c) we integrate with CeNGEN transcriptomics for principled parameter propagation rather than purely functional-group-based assignment; (d) our models include neuropeptidergic modulation ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) and organ systems ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)) that the locomotion-only circuit does not capture.

**Validation:** Level E neurons must still pass all [DD010](DD010_Validation_Framework.md) tiers. Individual cell models should additionally reproduce published I-V curves and compartmentalized calcium dynamics where available (e.g., RIA spatial signals per [Hendricks et al. 2012](https://doi.org/10.1038/nature11081), AWC responses per Nicoletti et al. 2019).

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
| Neuron membrane voltage | [DD002](DD002_Muscle_Model_Architecture.md) (via NMJ synapses) | `V` per neuron | NeuroML state variable | mV | dt_neuron (0.05 ms) |
| Neuron [Ca²⁺]ᵢ | [DD002](DD002_Muscle_Model_Architecture.md) (muscle activation), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (peptide release trigger) | `ca_internal` per neuron | NeuroML state variable | mol/cm³ | dt_neuron (0.05 ms) |
| Muscle [Ca²⁺]ᵢ (via [DD002](DD002_Muscle_Model_Architecture.md) muscle cells in same LEMS simulation) | [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic, via `sibernetic_c302.py`) | `muscle_ca` per muscle | Tab-separated file: muscle_id, timestep, ca_value | mol/cm³ | dt_coupling (0.005 ms) |
| Network activity recordings | [DD010](DD010_Validation_Framework.md) (Tier 2 validation) | `*_calcium.dat`, `*_voltages.dat` | Tab-separated, neuron_id columns × timestep rows | mV or mol | dt_neuron |
| Neuron voltage time series (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-neuron V over all timesteps | OME-Zarr: `neural/voltage/`, shape (n_timesteps, 302) | mV | output_interval |
| Neuron calcium time series (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-neuron [Ca²⁺] over all timesteps | OME-Zarr: `neural/calcium/`, shape (n_timesteps, 302) | mol/cm³ | output_interval |
| Neuron 3D positions | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Static 3D coordinates for 302 neurons | OME-Zarr: `neural/positions/`, shape (302, 3) | µm | one-time |

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
  differentiated: false              # Phase 1 ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)): CeNGEN cell-type differentiation
  neuropeptides: false               # Phase 2 ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)): peptidergic modulation
  connectome_dataset: "Cook2019"     # Cook2019, Witvliet2021, Varshney2011
  data_reader: "UpdatedSpreadsheetDataReader2"
  reference: "FW"                    # FW (forward crawl), BA (backward), TU (turning)
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `neural.enabled` | `true` | `true`/`false` | Enable neural circuit simulation |
| `neural.framework` | `c302` | `c302` | Neural framework (only c302 currently) |
| `neural.level` | `C1` | `A`, `B`, `C`, `C1`, `C2`, `D` | Biophysical detail level |
| `neural.differentiated` | `false` | `true`/`false` | Enable CeNGEN cell-type differentiation ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) |
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

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

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
| Muscle activation | [DD002](DD002_Muscle_Model_Architecture.md) | If neuron→muscle synaptic output changes, muscle calcium dynamics change |
| Body physics | [DD003](DD003_Body_Physics_Architecture.md) | If muscle calcium output format/units change, `sibernetic_c302.py` coupling breaks |
| Neuropeptide release | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | If `ca_internal` variable name or units change, peptide release triggers break |
| Tier 2 validation | [DD010](DD010_Validation_Framework.md) | If calcium recording file format changes, validation scripts break |

### Coupling Bridge Ownership

The `sibernetic_c302.py` script (in the Sibernetic repo) implements the [DD001](DD001_Neural_Circuit_Architecture.md)→[DD002](DD002_Muscle_Model_Architecture.md)→[DD003](DD003_Body_Physics_Architecture.md) coupling chain. It reads c302/NEURON calcium output and writes Sibernetic muscle activation input. **Any change to calcium output format or variable naming in c302 must be coordinated with the Sibernetic maintainer ([DD003](DD003_Body_Physics_Architecture.md)) and the Integration Maintainer ([DD013](DD013_Simulation_Stack_Architecture.md)).**

---

- **Approved by:** OpenWorm Steering
- **Implementation Status:** Complete (c302 Levels A-D exist)
- **Next Review:** After Phase 1 cell-type differentiation (see [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
