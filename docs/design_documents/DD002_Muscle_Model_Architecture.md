# DD002: Muscle Model Architecture and Calcium-Force Coupling

**Status:** Accepted  
**Author:** OpenWorm Core Team (based on Boyle & Cohen 2008)  
**Date:** 2026-02-14  
**Supersedes:** None  
**Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD003](DD003_Body_Physics_Architecture.md) (Body Physics)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | `GenericMuscleCell` NeuroML template (95 body wall muscles), muscle [Ca²⁺]→activation coupling via `sibernetic_c302.py` |
| **Success metric** | DD010 Tier 3: forward speed and body bend amplitude within ±15% of baseline |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) (muscle templates) + [`openworm/sibernetic`](https://github.com/openworm/sibernetic) (coupling script) — issues labeled `dd002` |
| **Config toggle** | `muscle.enabled: true` / `muscle.calcium_coupling: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` (activation in [0,1]?), `docker compose run validate` (Tier 3 kinematics) |
| **Visualize** | DD014 `muscle/activation/` layer — 95 muscles with [0,1] activation heatmap, warm colormap |
| **CI gate** | Tier 3 kinematic validation blocks merge |

---

## TL;DR

The muscle model uses Hodgkin-Huxley muscle cells with Ca²⁺-to-force coupling, bridging the neural voltage domain (mV, milliseconds) to the Sibernetic body physics domain (forces, mechanical strain). 95 body wall muscles in 4 quadrants convert intracellular calcium concentration to a linear activation coefficient [0, 1] consumed by Sibernetic. Success: forward speed and body bend amplitude within ±15% of Schafer lab experimental data.

---

## Goal & Success Criteria

| Criterion | Target | DD010 Tier |
|-----------|--------|------------|
| **Primary:** Forward speed | Within ±15% of Schafer lab WCON baseline | Tier 3 (blocking) |
| **Primary:** Body bend amplitude | Within ±15% of Schafer lab WCON baseline | Tier 3 (blocking) |
| **Secondary:** Muscle activation range | All activations in [0, 1], peak > 0.3 during neural drive | Quick-test (blocking per-PR) |
| **Tertiary:** Calcium decay dynamics | Decay time constant ~12 ms, consistent with Boyle & Cohen 2008 | Tier 1 (non-blocking) |

**Before:** No electrophysiological muscle model — neurons could not drive body physics through a biophysically realistic pathway.

**After:** 95 body wall muscles receive motor neuron input via NMJ synapses, depolarize via HH channels, accumulate intracellular calcium, and produce a [0, 1] activation coefficient that Sibernetic converts to contractile force.

---

## Deliverables

| Artifact | Path (relative to repo) | Format | Example |
|----------|------------------------|--------|---------|
| Generic muscle cell template | `openworm/c302` — `c302/c302_Muscles.py` | Python → NeuroML 2 XML | `GenericMuscleCell` with 4 channels (muscle-specific densities) |
| Muscle list (95 cells) | `CElegansNeuroML/CElegans/generatedNeuroML2/muscles.csv` | CSV | `muscle_id, quadrant, row_number, anterior_position, synaptic_partners` |
| Coupling script | `openworm/sibernetic` — `sibernetic_c302.py` | Python | Reads muscle [Ca²⁺]ᵢ, writes activation to Sibernetic |
| Muscle activation time series (viewer) | OME-Zarr: `muscle/activation/`, shape (n_timesteps, 95) | OME-Zarr | dimensionless [0, 1] per muscle per timestep |
| Muscle calcium time series (viewer) | OME-Zarr: `muscle/calcium/`, shape (n_timesteps, 95) | OME-Zarr | mol/cm³ per muscle per timestep |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository (templates)** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Repository (coupling)** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) |
| **Issue label** | `dd002` |
| **Milestone** | Muscle Model Architecture |
| **Branch convention** | `dd002/description` (e.g., `dd002/tune-nmj-conductance`) |
| **Example PR title** | `DD002: Adjust muscle conductance densities for locomotion fidelity` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` (DD013 simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, NEURON 8.2.6

### Step-by-step

```bash
# Step 1: Generate muscle network
cd c302/
python CElegans.py C1Muscles

# Step 2: Validate NeuroML syntax
jnml -validate LEMS_c302_C1_Muscles.xml

# Step 3: Run simulation
jnml LEMS_c302_C1_Muscles.xml -nogui

# Step 4: Check muscle activation outputs
python scripts/plot_muscle_activation.py LEMS_c302_C1_Muscles_muscles.dat
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 5: Verify activation ranges and calcium dynamics
python scripts/validate_muscle_calcium.py
# [TO BE CREATED] if not present — GitHub issue: openworm/c302#TBD

# Step 6: Quick test via Docker (must pass before PR)
docker compose run quick-test
# Green light: output plots show muscle activation in [0, 1] range
# Green light: peak activation during neural drive > 0.3

# Step 7: Full validation via Docker (must pass before merge)
docker compose run validate
# Green light: Tier 3 kinematic metrics within ±15% of baseline
# Green light: forward speed and body bend amplitude specifically checked
```

### Scripts that may not exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/plot_muscle_activation.py` | `[TO BE CREATED]` if not present | openworm/c302#TBD |
| `scripts/validate_muscle_calcium.py` | `[TO BE CREATED]` if not present | openworm/c302#TBD |

### Green light criteria

- Muscle activation range: [0, 1]
- Peak activation during neural drive: >0.5 (>0.3 minimum)
- Calcium decay time constant: ~12 ms
- No negative voltages below -60 mV, no positive voltages above +20 mV
- Tier 3 kinematic metrics within ±15% of baseline

---

## How to Visualize

**DD014 viewer layer:** `muscle/activation/` — 95 body wall muscles with [0, 1] activation heatmap, warm colormap.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `muscle/activation/` |
| **Color mode** | Warm colormap: 0 (blue/cool) → 1 (red/hot) representing activation coefficient |
| **Data source** | OME-Zarr: `muscle/activation/` shape (n_timesteps, 95), `muscle/calcium/` shape (n_timesteps, 95) |
| **What you should SEE** | 95 body wall muscles arranged in 4 quadrants (MDR, MVR, MVL, MDL). During forward locomotion, dorsal and ventral muscles should activate in alternating waves propagating anterior-to-posterior. Activation values should range [0, 1] with smooth transitions (no flickering or binary on/off). |
| **Trace view** | Clicking a muscle shows its calcium concentration and activation coefficient time series. Calcium decay should be ~12 ms. |

---

## Technical Approach

### Muscle Cells Use the Same Hodgkin-Huxley Framework as Neurons

Muscles are modeled as single-compartment conductance-based cells using the **same ion channel types** (leak, K_slow, K_fast, Ca_boyle) with **muscle-specific conductance densities** tuned to produce slower, sustained depolarizations rather than sharp action potentials.

**Muscle conductance densities (from Boyle & Cohen 2008):**

| Channel | Muscle g_max | E_rev | Notes |
|---------|-------------|-------|-------|
| Leak | 5e-7 S/cm² | -50 mV | 100x smaller than neurons → slower dynamics |
| K_slow | 0.0006 S/cm² | -60 mV | 5000x smaller than neurons |
| K_fast | 0.0001 S/cm² | -60 mV | 711x smaller than neurons |
| Ca_boyle | 0.0007 S/cm² | +40 mV | ~4300x smaller than neurons |

**Membrane properties:**
- Specific capacitance: 1 µF/cm²
- Cell diameter: larger than neurons (varies by muscle, ~5-10 µm)
- Initial voltage: -45 mV

### Calcium-to-Force Coupling (The Bridge to Sibernetic)

Intracellular calcium concentration ([Ca²⁺]ᵢ) is the coupling variable between the electrophysiological model (NeuroML/NEURON) and the body physics model (Sibernetic/SPH).

**Calcium dynamics:**
```
d[Ca]/dt = -rho * I_Ca - [Ca]/tau_Ca
```
- rho = 0.000238 mol/(C·cm)
- tau_Ca = 11.5943 ms

**Activation coefficient (linear scaling):**
```
activation = min(1.0, [Ca²⁺]ᵢ / [Ca²⁺]_max)
```
- [Ca²⁺]_max = 4e-7 mol (maximum calcium for full contraction)

**Force generation:**
```
F_muscle = activation * max_muscle_force
```
- max_muscle_force = 4000 (Sibernetic units)

This linear scaling is a **simplification**. Real muscle involves crossbridge dynamics (actin-myosin binding), cooperative activation, length-tension relationships, and force-velocity curves. But Boyle & Cohen (2008) showed that "*Caenorhabditis elegans* body wall muscles are simple actuators" -- they behave as direct transducers of calcium to force without complex mechanical nonlinearities.

### Neural-to-Muscle Coupling

Neurons communicate to muscles via **neuromuscular junctions (NMJs)** modeled as excitatory chemical synapses:

- Neuron releases synaptic current proportional to presynaptic voltage (graded release)
- Muscle receives depolarizing current
- Muscle voltage rises → Ca channels open → [Ca²⁺]ᵢ increases → contraction

**Critical parameter:** NMJ conductance is higher than neuron-neuron synapses to produce strong muscle depolarization. Typical values: 0.5-1.0 nS (vs. 0.09 nS for inter-neuron synapses).

---

## Alternatives Considered

### 1. Hill-Type Muscle Model with Crossbridge Dynamics

**Description:** Explicitly model actin-myosin binding, ADP/ATP cycling, length-tension curves, force-velocity relationships.

**Rejected because:**
- Boyle & Cohen (2008) demonstrated that simple linear activation is sufficient to reproduce *C. elegans* locomotion
- Adds significant computational cost (6+ additional state variables per muscle)
- Lacks experimental data to parameterize crossbridge kinetics in *C. elegans* muscles
- Violates YAGNI (You Aren't Gonna Need It) principle

**When to reconsider:** If simulations fail to reproduce detailed muscle mechanics (e.g., tetanic contraction during egg-laying, rapid twitches during defecation, isometric force-length relationships).

### 2. Direct Neural Activation Without Electrophysiology

**Description:** Skip the muscle HH model entirely. Let neurons directly control Sibernetic particle forces.

**Rejected because:**
- Throws away the biophysical realism that is OpenWorm's core strength
- Loses the voltage-to-calcium-to-force causal chain, making the model less interpretable
- Cannot capture muscle dynamics like refractory periods, fatigue, or calcium-dependent force modulation

### 3. FitzHugh-Nagumo Simplified Excitable Dynamics

**Description:** Use a 2-variable reduced model (V, recovery variable) instead of full HH.

**Rejected because:**
- FHN does not explicitly model calcium, which is the critical coupling variable to Sibernetic
- Parameters are abstract (not directly tied to conductances and ion channels)
- Loses the modularity of being able to add/remove specific channels

---

## Quality Criteria

A contribution to the muscle model MUST:

1. **Preserve the Calcium Interface:** The output of the muscle model to Sibernetic is [Ca²⁺]ᵢ. Any change must maintain this interface or provide a migration path for Sibernetic.

2. **Validate Against Movement Data:** Changes must not degrade kinematic validation scores. The Boyle & Cohen parameter set has been validated against real worm movement via open-worm-analysis-toolbox.

3. **NeuroML 2 Compliance:** Muscle cell definitions must be valid NeuroML 2.

4. **Biophysical Units:** Conductances in S/cm² or mS/cm², voltages in mV, time constants in ms, calcium in mol or mM.

5. **Muscle-Neuron Distinction:** Muscle conductance densities are 10-1000x smaller than neuron densities. Do not copy neuron parameters to muscles.

### Testing Procedure

```bash
# Generate muscle network
cd c302/
python CElegans.py C1Muscles

# Run simulation
jnml LEMS_c302_C1_Muscles.xml -nogui

# Check muscle activation outputs
python scripts/plot_muscle_activation.py LEMS_c302_C1_Muscles_muscles.dat

# Verify activation ranges are [0, 1] and follow calcium dynamics
python scripts/validate_muscle_calcium.py
```

**Expected results:**
- Muscle activation range: [0, 1]
- Peak activation during neural drive: >0.5
- Calcium decay time constant: ~12 ms
- No negative voltages below -60 mV, no positive voltages above +20 mV

---

## Boundaries (Explicitly Out of Scope)

### This Design Document Does NOT Cover:

1. **Pharyngeal muscles:** Modeled separately (see DD007: Pharyngeal System). Pharyngeal muscle is nonstriated and functionally distinct from body wall muscle.

2. **Specialized muscles (vulval, uterine, anal, intestinal):** Future work. These may require different channel complements or calcium-to-force relationships.

3. **Muscle cell geometry:** Currently single-compartment. Multicompartmental muscle with spindle morphology is future work.

4. **Developmental changes:** Muscle properties change during development (L1 vs. adult). Phase 6 work.

5. **Myosin isoform diversity:** *C. elegans* expresses multiple myosin heavy chain genes. Current model uses generic contractility.

---

## Context & Background

*C. elegans* body wall muscles enable locomotion by generating contractile forces that deform the elastic body against the fluid-filled pseudocoelom. The worm has 95 body wall muscles arranged in 4 quadrants (MDR, MVR, MVL, MDL) of 24 rows each, extending along the anterior-posterior axis. These muscles are excitable membranes innervated by motor neurons.

The coupling challenge: neurons operate in the voltage domain (mV, milliseconds), body physics operates in the force domain (Newtons, mechanical strain). The muscle model bridges these domains.

---

## Implementation References

### Muscle Cell Template

```python
# c302/c302_Muscles.py
def create_generic_muscle_cell():
    muscle_cell = NeuroMLCell(id="GenericMuscleCell")
    muscle_cell.add_channel("leak_chan", density="5e-7 S_per_cm2")
    muscle_cell.add_channel("k_slow_chan", density="0.0006 S_per_cm2")
    muscle_cell.add_channel("k_fast_chan", density="0.0001 S_per_cm2")
    muscle_cell.add_channel("ca_boyle_chan", density="0.0007 S_per_cm2")
    muscle_cell.C = 1.0  # uF_per_cm2
    muscle_cell.v_init = -45  # mV
    return muscle_cell
```

### Muscle List (95 Cells)

```
CElegansNeuroML/CElegans/generatedNeuroML2/muscles.csv
```

Each muscle row: `muscle_id, quadrant (MDR/MVR/MVL/MDL), row_number (1-24), anterior_position, synaptic_partners`

### Coupling to Sibernetic

The `c302_Sibernetic` integration script:
1. Reads muscle [Ca²⁺]ᵢ time series from NEURON simulation
2. Converts to activation coefficients via `activation = min(1, ca/max_ca)`
3. Writes to Sibernetic-readable muscle activation file
4. Sibernetic reads and applies forces to elastic particle connections representing each muscle

---

## Migration Path

### If Detailed Crossbridge Mechanics Become Necessary:

1. **Create a new Level E cell type** with crossbridge state variables (attached, detached, power stroke, etc.).
2. **Implement as a LEMS ComponentType extension** rather than modifying the base GenericMuscleCell.
3. **Provide [Ca²⁺]ᵢ → force mapping** that preserves the Sibernetic interface.
4. **Validate against isometric force recordings** if such data become available for *C. elegans*.

### If Muscle-Type Diversity Is Required (Phase 3):

See DD007 (Pharyngeal System) for an example of creating a distinct muscle cell type. The general pattern:
- Create a new LEMS cell template (e.g., `PharyngealMuscleCell`)
- Adjust channel densities based on transcriptomic or electrophysiological data
- Adjust calcium-to-force parameters if pharyngeal contraction dynamics differ
- Validate against tissue-specific behavior (pumping rate, not crawling)

---

## Known Issues and Future Work

### Issue 1: Single Muscle Compartment

Real *C. elegans* body wall muscles are spindle-shaped with ~60 µm length. Voltage may not be uniform along the length. Multicompartmental muscle models (Level D equivalent for muscle) would require:
- Morphological reconstructions (EM data exists but not yet digitized in cable-equation-compatible format)
- Axial resistance parameters
- Increased compute cost (24 compartments/muscle × 95 muscles = 2,280 compartments)

**When to address:** If single-compartment fails to reproduce localized muscle responses or wave propagation.

### Issue 2: Lack of Direct Muscle Electrophysiology

Most validation is indirect (via movement). Direct patch-clamp recordings from *C. elegans* muscle are rare. We validate via the emergent behavior (crawling), not the muscle voltage directly.

**When to address:** If muscle-specific electrophysiology data become available, recalibrate conductance densities.

### Issue 3: MVL24 Muscle Does Not Exist

The simulation includes MVL24 for symmetry (4 quadrants × 24 rows = 96 muscles), but the real worm has only 95 (MVL24 is absent). This is a minor biological inaccuracy preserved for code simplicity.

**Fix:** Set MVL24 conductances to zero or remove from the simulation. Low priority.

---

## References

1. **Boyle JH, Cohen N (2008).** "Caenorhabditis elegans body wall muscles are simple actuators." *Biosystems* 94:170-181.
   *Source of muscle conductance densities and calcium-to-force coupling.*

2. **Goodman MB, Hall DH, Avery L, Bhatt R (1998).** "Active currents regulate sensitivity and dynamic range in *C. elegans* neurons." *Neuron* 20:763-772.
   *Evidence for graded potentials in the nervous system that drives these muscles.*

3. **Cook SJ et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *NMJ connectivity (which motor neurons innervate which muscles).*

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Motor neuron synaptic current | DD001 (via NMJ graded synapses) | `I_syn` on each muscle cell | NeuroML synapse coupling (within same LEMS simulation) | nA |
| Motor neuron identity | DD001 connectome | NMJ adjacency (which neurons innervate which muscles) | ConnectomeToolbox | neuron-muscle pairs |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units | Timestep |
|--------|------------|----------|--------|-------|----------|
| Muscle [Ca²⁺]ᵢ | DD003 (Sibernetic) | `ca_internal` per muscle | Read by `sibernetic_c302.py` from NEURON state | mol/cm³ | dt_coupling (0.005 ms) |
| Muscle activation coefficient | DD003 (Sibernetic) | `activation = min(1.0, [Ca²⁺]ᵢ / 4e-7)` | Computed in `sibernetic_c302.py`, written to Sibernetic muscle activation input | dimensionless [0, 1] | dt_coupling |
| Muscle activation time series (for viewer) | **DD014** (visualization) | Per-muscle activation over all timesteps | OME-Zarr: `muscle/activation/`, shape (n_timesteps, 95) | dimensionless [0, 1] | output_interval |
| Muscle calcium time series (for viewer) | **DD014** (visualization) | Per-muscle [Ca²⁺] over all timesteps | OME-Zarr: `muscle/calcium/`, shape (n_timesteps, 95) | mol/cm³ | output_interval |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository (templates)** | `openworm/c302` (muscle cells are NeuroML templates within c302) |
| **Repository (coupling)** | `openworm/sibernetic` (`sibernetic_c302.py`) |
| **Docker stage** | Same as DD001 (`neural` stage) |
| **`versions.lock` key** | No separate pin — muscles are part of the c302 package |
| **Build dependencies** | Same as DD001 (NEURON 8.2.6, pyNeuroML) |

### Configuration

**`openworm.yml` section:**

```yaml
muscle:
  enabled: true                      # Requires neural.enabled
  calcium_coupling: true             # Ca²⁺ → force pipeline
  max_muscle_force: 4000             # Sibernetic force units
  max_ca: 4e-7                       # mol; calcium for full contraction
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `muscle.enabled` | `true` | `true`/`false` | Enable muscle simulation (requires `neural.enabled`) |
| `muscle.calcium_coupling` | `true` | `true`/`false` | Enable Ca²⁺ → force coupling pipeline |
| `muscle.max_muscle_force` | `4000` | Positive float | Maximum muscle force in Sibernetic units |
| `muscle.max_ca` | `4e-7` | Positive float (mol) | Calcium concentration for full contraction (activation = 1.0) |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
docker compose run quick-test
# Checks: output plots show muscle activation in [0, 1] range
# Checks: peak activation during neural drive > 0.3

# Full validation (must pass before merge to main)
docker compose run validate
# Checks:
#   - Tier 3: kinematic metrics within ±15% of baseline
#   - Specifically: forward speed and body bend amplitude are most sensitive to muscle changes
```

**Per-PR checklist:**
- [ ] `jnml -validate` passes for muscle NeuroML/LEMS files
- [ ] `docker compose run quick-test` passes (activation in [0, 1], peak > 0.3)
- [ ] `docker compose run validate` passes (Tier 3 kinematics)
- [ ] Muscle conductance densities are 10-1000x smaller than neuron densities (no copy-paste from neuron params)
- [ ] Calcium interface to Sibernetic is preserved (variable name, units)

### How to Visualize (DD014 Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `muscle/activation/` (n_timesteps, 95) | Muscle activation heatmap | Warm colormap: 0.0 (blue) → 1.0 (red) |
| `muscle/calcium/` (n_timesteps, 95) | Muscle calcium concentration | mol/cm³ colormap |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Neuron→muscle synaptic conductance | DD001 | NMJ weight changes → muscle depolarization amplitude changes |
| c302 HH framework | DD001 | If channel model equations change, muscle dynamics change (same framework) |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Body physics forces | DD003 | If calcium→activation mapping changes (max_ca, activation formula), Sibernetic locomotion behavior changes |
| Kinematic validation | DD010 | Muscle force directly determines movement — any change affects Tier 3 |

### Coupling Bridge Ownership

**The `sibernetic_c302.py` coupling script** (lives in `openworm/sibernetic` repo) reads muscle calcium from NEURON and writes activation to Sibernetic. This script is the single point where DD002 output format matters. Changes to:
- Muscle calcium variable name → must update `sibernetic_c302.py`
- Activation formula → must update `sibernetic_c302.py`
- Number of muscles (e.g., adding pharyngeal muscles per DD007) → must update muscle mapping in `sibernetic_c302.py`

**Coordination required:** Muscle model maintainer + Body Physics maintainer (DD003) + Integration Maintainer (DD013)

---

**Approved by:** OpenWorm Steering
**Implementation Status:** Complete (GenericMuscleCell in c302)
**Next Actions:**
1. Differentiate into muscle-type-specific models using transcriptomics (Phase 3)
2. Add pharyngeal muscles (DD007)
3. Model specialized muscles (vulval, uterine, enteric) as needed
