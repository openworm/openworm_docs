# DD001: Neural Circuit Architecture and Multi-Level Framework

**Status:** Accepted  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** None  
**Related:** [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD003](DD003_Body_Physics_Architecture.md) (Body Physics), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation)

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

## TL;DR

OpenWorm models the 302-neuron *C. elegans* nervous system using a multi-level Hodgkin-Huxley conductance-based framework (c302), with Level C1 (graded synapses) as the default. Graded synapses match worm biology — these neurons do not fire action potentials. Success: kinematic validation of emergent locomotion within ±15% of Schafer lab experimental data.

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
| Connectome data | ConnectomeToolbox / `cect` package | Python API / CSV | Cook2019, Witvliet2021, Varshney2011 |
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

- Graded synapses match *C. elegans* biology (Goodman et al. 1998)
- Continuous voltage coupling enables realistic sensorimotor feedback via Sibernetic
- Computationally tractable for whole-circuit simulation
- Validated against movement kinematics

### Cell Model Specification (Level C/C1)

**Membrane dynamics (Hodgkin-Huxley formalism):**

```
C * dV/dt = I_leak + I_Kslow + I_Kfast + I_Ca + I_syn + I_gap + I_ext
```

**Ion channels (derived from Boyle & Cohen 2008 muscle model):**

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

---

## Alternatives Considered

### 1. Pure Integrate-and-Fire for All Levels

**Rejected because:** *C. elegans* neurons do not fire action potentials. IAF models produce biologically incorrect all-or-nothing spiking. Goodman et al. (1998) electrophysiology shows graded, continuous responses.

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

4. **Connectome Topology Preservation:** The connectome structure (adjacency matrices) is defined by Cook et al. 2019 data in ConnectomeToolbox. Do not edit synapse existence; only edit synapse properties (weights, time constants).

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
Ingests: Cook et al. 2019 (both sexes), Witvliet et al. 2021 (developmental), Varshney 2011 (original)

---

## References

1. **Boyle JH, Cohen N (2008).** "Caenorhabditis elegans body wall muscles are simple actuators." *Biosystems* 94:170-181.
   *Source of channel kinetics.*

2. **Goodman MB, Hall DH, Avery L, Bhatt R (1998).** "Active currents regulate sensitivity and dynamic range in *C. elegans* neurons." *Neuron* 20:763-772.
   *Evidence for graded potentials.*

3. **Cook SJ et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *Connectome topology.*

4. **Gleeson P et al. (2018).** "c302: a multiscale framework for modelling the nervous system of *Caenorhabditis elegans*." *Phil Trans R Soc B* 373:20170379.
   *c302 architecture paper.*

5. **Rosen R (1991).** *Life Itself: A Comprehensive Inquiry Into the Nature, Origin, and Fabrication of Life.*
   *Causal loop philosophy.*

---

## Migration Path (If This Decision Changes)

If future research demonstrates that Level C1 graded synapses are insufficient (e.g., specific neurons require action potentials, or detailed dendritic computation is essential):

1. **Add a new level (e.g., Level E)** rather than modifying C1. Backward compatibility is sacred.
2. **Document the biological justification** in a new DD (e.g., [DD015](DD015_AI_Contributor_Model.md): Action Potential Mechanisms in Specific Neurons).
3. **Provide a conversion script** from C1 to the new level.
4. **Re-validate** against all existing benchmarks.

Do NOT modify Level C1 unless a critical bug is found.

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

**Approved by:** OpenWorm Steering
**Implementation Status:** Complete (c302 Levels A-D exist)
**Next Review:** After Phase 1 cell-type differentiation (see [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
