# DD007: Pharyngeal System Architecture (Semi-Autonomous Organ)

- **Status:** Proposed (Phase 3)
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD009](DD009_Intestinal_Oscillator_Model.md) (Intestinal Model)

---

## TL;DR

Model the 63-cell pharynx as a semi-autonomous subsystem with 20 neurons (Level C1 Hodgkin-Huxley), 20 nonstriated muscles (plateau potentials), and a 1D pumping oscillator. The pharynx is functionally isolated from the body circuit. Success: pumping frequency 3-4 Hz, with body locomotion not degraded when the pharynx is enabled.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 3](DD_PHASE_ROADMAP.md#phase-3-organ-systems-hybrid-ml-months-7-12) |
| **Layer** | Organ Systems — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-3-organ-systems-hybrid-ml-months-7-12) |
| **What does this produce?** | Pharyngeal network: 20 neurons + 20 muscles (NeuroML), 1D pumping oscillator module, pumping state time series |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: pumping frequency 3-4 Hz; body locomotion not degraded when pharynx enabled |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) (`c302_pharynx.py`, `pharynx/` module) — issues labeled `dd007` |
| **Config toggle** | `pharynx.enabled: true` / `pharynx.model: "1d_oscillator"` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` with `pharynx.enabled: true` (body still moves?), `scripts/measure_pumping.py` (3-4 Hz?) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `pharynx/pumping_state/` layer — 3-section contraction animation (corpus, isthmus, terminal bulb), [0,1] heatmap |
| **CI gate** | Pumping frequency validation (Tier 3) blocks merge; backward compatibility with `pharynx.enabled: false` required |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Pumping frequency | 3-4 Hz (0.25-0.33 s period) under feeding conditions | Tier 3 (blocking) |
| **Secondary:** Body locomotion preservation | Within +/-15% of baseline kinematic metrics when pharynx enabled | Tier 3 (blocking) |
| **Tertiary:** Electropharyngeogram match | Simulated pharyngeal muscle voltage qualitatively matches [Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) EPG plateau potentials | Tier 1 (non-blocking) |

**Before:** No pharyngeal model. The 20 pharyngeal neurons and 20 pharyngeal muscles are absent from simulation. Pumping is not modeled.

**After:** A semi-autonomous pharyngeal subsystem producing 3-4 Hz pumping oscillations via coordinated contraction of corpus, isthmus, and terminal bulb sections. Functionally isolated from body circuit (except rare RIP -> I2 connection).

---

## Deliverables

| Artifact | Path (relative to `openworm/c302`) | Format | Example |
|----------|-------------------------------------|--------|---------|
| Pharyngeal muscle cell template | `pharynx/PharyngealMuscleCell.cell.nml` | NeuroML 2 XML | Nonstriated HH model with plateau potential kinetics |
| Pharyngeal network generator | `c302_pharynx.py` | Python | Generates 20 neurons + 20 muscles + connectivity |
| 1D pumping oscillator | `pharynx/pumping_oscillator.py` | Python | 3-section contraction/relaxation model |
| Pharynx coupling module (future) | `pharynx/pharynx_coupling.py` | Python | Option B SPH coupling `[TO BE CREATED — Phase 4+]` |
| Pumping state time series | Output: `pharynx_pumping_state.dat` | Tab-separated | Per-section contraction [0,1] over time |
| Pumping state for viewer | OME-Zarr: `pharynx/pumping_state/`, shape (n_timesteps, 3) | OME-Zarr | Continuous [0,1] per section |

Each pharyngeal NeuroML file includes metadata:
```xml
<notes>
  Cell type: pharyngeal muscle (nonstriated)
  Electrophysiology reference: Raizen & Avery 1994, Neuron 12:483-495
  Key channels: eat-2 (pharynx-specific Ca2+), egl-19 (L-type Ca2+), unc-2 (P/Q-type Ca2+)
  Gap junction innexins: inx-2, inx-3, inx-7
  Validation target: plateau potentials, ~100 ms duration
</notes>
```

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd007` |
| **Milestone** | Phase 3: Pharyngeal System |
| **Branch convention** | `dd007/description` (e.g., `dd007/pharyngeal-muscle-model`) |
| **Example PR title** | `DD007: Add PharyngealMuscleCell with plateau potential kinetics` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, pandas, numpy

### Step-by-step

```bash
# Step 1: Generate pharyngeal network
python c302/c302_pharynx.py
# Expected output: LEMS_c302_pharynx.xml with 20 neurons + 20 muscles

# Step 2: Quick validation — backward compatibility (must pass before PR)
docker compose run quick-test   # with pharynx.enabled: false
# Green light: identical output to pre-pharynx baseline

# Step 3: Quick validation — pharynx enabled (must pass before PR)
# (set pharynx.enabled: true in openworm.yml)
docker compose run quick-test
# Green light: body still moves (pharynx must not destabilize simulation)
# Green light: pharyngeal output file is generated

# Step 4: Validate pumping frequency
docker compose run simulation -- python scripts/measure_pumping.py
# [TO BE CREATED] — GitHub issue: openworm/c302#TBD
# Green light: pumping rate is 3-4 Hz

# Step 5: Full validation (must pass before merge)
docker compose run validate
# Green light: Tier 3 pumping frequency 3-4 Hz
# Green light: Tier 3 body kinematic metrics within +/-15%
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `c302_pharynx.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `pharynx/PharyngealMuscleCell.cell.nml` | `[TO BE CREATED]` | openworm/c302#TBD |
| `pharynx/pumping_oscillator.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/measure_pumping.py` | `[TO BE CREATED]` | openworm/c302#TBD |

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** Pharyngeal pumping state as a 3-section contraction heatmap.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `pharynx/pumping_state/` — 3-section contraction animation |
| **Color mapping** | Per-section contraction heatmap: blue (0 = relaxed) to red (1 = fully contracted) |
| **Data source** | OME-Zarr: `pharynx/pumping_state/`, shape (n_timesteps, 3) — columns: corpus, isthmus, terminal bulb |
| **What you should SEE** | Rhythmic contraction waves at 3-4 Hz. Corpus contracts first, isthmus follows, terminal bulb last — a peristaltic-like wave moving posterior. Relaxation in reverse order. Clear ~250-330 ms cycle period. |
| **Comparison view** | Overlay pharyngeal pumping trace with body locomotion trace — the two should be independent (no phase-locking, no interference). |

---

## Technical Approach

### Model the Pharynx as a Separate Subsystem

**Rationale:**

- Functional isolation allows independent modeling
- Pharyngeal muscle is **nonstriated** with distinct electrophysiology from body wall muscle
- Pumping behavior (3-4 Hz oscillation) is a clear validation target
- WormAtlas provides complete anatomical descriptions

### Pharyngeal Neuron Models

Use the **same Level C1 framework** (Hodgkin-Huxley conductance-based) as body neurons, but with pharynx-specific:

- Connectome topology (pharyngeal neuron -> pharyngeal neuron connections only)
- Cell-type-specific differentiation using CeNGEN expression (128 neuron classes include pharyngeal neurons)

**Already partially implemented:** c302 Level B includes pharyngeal neurons with integrate-and-fire dynamics. Phase 3 upgrades to Level C1 HH.

### Pharyngeal Muscle Models

**Key difference from body wall muscle:** Pharyngeal muscles are **nonstriated**, electrically coupled via gap junctions, and pump synchronously.

**Electrophysiology:**

- Raizen & Avery (1994): pharyngeal muscles show **plateau potentials** (~100 ms duration) synchronized across the pharynx
- Eat-2 Ca2+ channel is pharynx-specific (egl-19 and unc-2 also expressed)
- Strong gap junction coupling (inx-2, inx-3, inx-7 innexins)

**Modeling approach:**

- Same HH framework as body muscles ([DD002](DD002_Muscle_Model_Architecture.md)) but with:
  - Higher gap junction conductance (0.1-0.5 nS vs. 0.01 nS for neurons)
  - Adjusted Ca2+ channel kinetics for plateau potentials
  - Coupling to pharyngeal body mechanics (separate from main body SPH)

### Pharyngeal Pumping Mechanics

**Option A (Simplified):** Model pharyngeal pumping as a **1D oscillator** with three sections (corpus, isthmus, terminal bulb) undergoing coordinated contraction/relaxation. Do not couple to full Sibernetic SPH.

**Option B (Integrated):** Create a **separate SPH pharyngeal body** with ~5,000 particles representing pharyngeal muscle, lumen, and marginal cells. Couple to the main body via mechanical attachment at the anterior.

**Decision:** Start with **Option A** (1D oscillator) for Phase 3. Upgrade to Option B if detailed pharyngeal-body mechanical coupling is needed (e.g., modeling egg-laying, which requires vulva-uterus-pharynx coordination).

**Validation target:** Reproduce the **3-4 Hz pumping frequency** observed in feeding worms.

---

## Alternatives Considered

### 1. Ignore the Pharynx (Focus on Locomotion Only)

**Rejected:** Pharyngeal pumping is one of the best-characterized behaviors. It provides an independent validation target. Omitting it leaves a major gap in whole-organism modeling.

### 2. Treat Pharyngeal Muscles as Identical to Body Wall Muscles

**Rejected:** Pharyngeal muscle is functionally and structurally distinct (nonstriated, plateau potentials, gap-junction-synchronized). Biological accuracy requires separate parameterization.

### 3. Fully Detailed SPH Pharynx with Food Particle Transport

**Description:** Model individual bacteria as SPH particles flowing through the pharyngeal lumen, grinder crushing bacteria, pharyngeal glands secreting enzymes.

**Deferred (too complex for Phase 3):** Start with muscle contraction dynamics and pumping frequency. Add lumen fluid flow and food transport if needed for validation.

---

## Quality Criteria

1. **Pumping Frequency:** Simulated pumping rate must be 3-4 Hz (0.25-0.33 s period) under feeding conditions.

2. **Electropharyngeogram Validation:** If possible, compare simulated pharyngeal muscle voltage to Raizen & Avery (1994) EPG recordings (plateau potentials, spike duration).

3. **Anatomical Accuracy:** All 63 pharyngeal cells included with correct spatial positions from WormAtlas.

4. **Functional Isolation:** Pharyngeal circuit operates independently from body circuit. No synapses between pharyngeal and body neurons (except RIP -> I2, which is rare).

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Food particle transport:** Individual bacteria moving through the pharyngeal lumen are not modeled. Phase 4+ work if mechanical food processing is needed.

2. **Pharyngeal gland secretion:** The 4 gland cells (g1, g2L, g2R, gl) secrete digestive enzymes. Not modeled in Phase 3.

3. **Grinder mechanics:** The terminal bulb grinder crushes bacteria. Not modeled until Option B SPH pharynx is implemented.

4. **Pharynx-intestine coupling:** Food transfer from pharynx to intestine is the interface with [DD009](DD009_Intestinal_Oscillator_Model.md). Only the pumping state output is provided; actual material flow is future work.

5. **Egg-laying coordination:** Vulva-uterus-pharynx coordination requires Option B (SPH pharynx) and is Phase 4+ work.

6. **Pharyngeal epithelial and marginal cells:** The 9 epithelial and 9 marginal cells provide structural support. They are included in cell count but not actively modeled in Phase 3.

---

## Context & Background

The pharynx is a **semi-autonomous neuromuscular organ** comprising 63 cells:

- **20 pharyngeal neurons** (M1-M5, I1-I6, MC, MI, NSM, RIP)
- **20 pharyngeal muscles** (pm1-pm8 in corpus, pm3-pm5 in isthmus, pm6-pm8 in terminal bulb)
- **9 epithelial cells** (e1-e3 per section)
- **9 marginal cells** (mc1-mc3 per section)
- **4 gland cells** (g1, g2L, g2R, gl)
- **1 valve cell (vpi1)**

The pharynx pumps bacterial food from the mouth to the intestine at **~3-4 Hz** during feeding, with distinct electrophysiological dynamics ([Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) electropharyngeogram recordings). It is functionally isolated from the body circuit — pharyngeal neurons do not synapse onto body neurons and vice versa (with rare exceptions: RIP -> I2).

---

## Code Reuse Opportunities

### Existing Pharyngeal Muscle Models (NEURON + Jupyter)

**Repository 1:** `openworm/pharyngeal_muscle_model` (pushed 2017-01-19, dormant but complete)

Contains a **NEURON implementation of pm3 pharyngeal muscle** with:

- EAT-2, EGL-19, UNC-2 Ca²⁺ channels (exactly [DD007](DD007_Pharyngeal_System_Architecture.md)'s target channels)
- Ca²⁺ slow action potential (plateau potentials, ~100ms duration)
- Output matches [Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) EPG recordings ([DD007](DD007_Pharyngeal_System_Architecture.md)'s validation target)

**Reuse Plan:**
```bash
# Test existing NEURON model
git clone https://github.com/openworm/pharyngeal_muscle_model.git
cd pharyngeal_muscle_model/pm3\ muscle\ +\ small\ current/
nrngui _run.hoc
# Verify: Plateau potentials in output, ~100ms duration
```

**Integration:**

1. Convert NMODL → NeuroML2 using pyNeuroML OR
2. Use NEURON model directly, couple via `sibernetic_NEURON` interface

**Estimated Time Savings:** 20-30 hours (pharyngeal muscle dynamics already validated)

**Repository 2:** `openworm/PlateauNoiseModel` (pushed 2025-01-30, recently active)

Jupyter notebook with pharyngeal muscle plateau model (Kenngott et al. 2025).

- Use for cross-validation of [DD007](DD007_Pharyngeal_System_Architecture.md) muscle model
- Plotting code for EPG-style output

**Next Actions:**

- [ ] Test pharyngeal_muscle_model on modern NEURON (version compatibility?)
- [ ] Extract channel kinetics (eat-2, egl-19, unc-2 conductances)
- [ ] Compare to PlateauNoiseModel (two independent implementations → cross-validate)
- [ ] Convert to NeuroML2 for [DD007](DD007_Pharyngeal_System_Architecture.md)'s `PharyngealMuscleCell.cell.nml`

---

### Existing Code Resources

**pharyngeal_muscle_model** ([openworm/pharyngeal_muscle_model](https://github.com/openworm/pharyngeal_muscle_model), 2017, dormant but complete):
Contains a NEURON implementation of pm3 pharyngeal muscle with EAT-2, EGL-19, UNC-2 Ca2+ channels — exactly the channels DD007 needs. Produces Ca2+ slow action potentials (plateau potentials, ~100ms duration) matching Raizen & Avery 1994 EPG recordings. Can be converted to NeuroML2 via pyNeuroML or used directly via NEURON. **Estimated time savings: 20-30 hours.**

**PlateauNoiseModel** ([openworm/PlateauNoiseModel](https://github.com/openworm/PlateauNoiseModel), active 2025):
Jupyter notebook with pharyngeal muscle plateau potential model and plotting code, related to Kenngott et al. 2025 paper. Provides validation data and reference kinetics for pharyngeal muscle models.

**JohnsonMailler_MuscleModel** ([openworm/JohnsonMailler_MuscleModel](https://github.com/openworm/JohnsonMailler_MuscleModel), 2025):
Ca²⁺-force coupling mechanics from Johnson & Mailler 2015. Evaluate whether the Ca²⁺ dynamics portion is separable from body wall muscle assumptions and adaptable for nonstriated pharyngeal muscle.

**NicolettiEtAl2019_NeuronModels** / **NicolettiEtAl2024_MN_IN** ([openworm/NicolettiEtAl2019_NeuronModels](https://github.com/openworm/NicolettiEtAl2019_NeuronModels), [openworm/NicolettiEtAl2024_MN_IN](https://github.com/openworm/NicolettiEtAl2024_MN_IN)):
May contain HH parameter fits for pharyngeal neurons (I1, M3, MC, NSM) that could initialize `c302_pharynx.py` neuron templates.

---

## References

1. **Raizen DM, Avery L (1994).** "Electrical activity and behavior in the pharynx of *Caenorhabditis elegans*." *Neuron* 12:483-495.
2. **Avery L, Horvitz HR (1989).** "Pharyngeal pumping continues after laser killing of the pharyngeal nervous system." *Neuron* 3:473-485.
3. **WormAtlas Pharynx Handbook.** wormatlas.org/hermaphrodite/pharynx/mainframe.htm
4. **OpenWorm pharyngeal_muscle_model repository.** github.com/openworm/pharyngeal_muscle_model — NEURON model of pm3 muscle with plateau potentials

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Pharyngeal neuron connectome | ConnectomeToolbox / [DD001](DD001_Neural_Circuit_Architecture.md) | Pharyngeal neuron adjacency (20 neurons) | Same format as body connectome | synapse pairs + weights |
| CeNGEN expression (pharyngeal neurons) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Per-class conductance densities | NeuroML `<channelDensity>` | S/cm2 |
| RIP->I2 synaptic input (rare body<->pharynx connection) | [DD001](DD001_Neural_Circuit_Architecture.md) | RIP neuron voltage | NeuroML coupling | mV |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Pumping state (contracted/relaxed per section) | [DD010](DD010_Validation_Framework.md) (pumping frequency validation) | Per-section contraction time series | Tab-separated file | binary (0/1) or continuous [0,1] |
| Pharyngeal particle forces (Option B only) | [DD003](DD003_Body_Physics_Architecture.md) | Per-particle force for pharyngeal muscles | Same format as body muscle activation | dimensionless [0,1] |
| Food transport rate (future) | [DD009](DD009_Intestinal_Oscillator_Model.md) | Rate of material entering intestine | Scalar time series | um3/s |
| Pumping state time series (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-section contraction state over all timesteps | OME-Zarr: `pharynx/pumping_state/`, shape (n_timesteps, 3) | continuous [0, 1] |

### Repository & Packaging

- **Primary repository:** `openworm/c302` (same package, new module)
- **Docker stage:** `neural` (same as [DD001](DD001_Neural_Circuit_Architecture.md))
- **`versions.lock` key:** `c302`
- **Build dependencies:** pyNeuroML (pip), numpy (pip)
- **No additional Docker changes** for Option A (1D oscillator is pure Python/NeuroML)
- **Option B would require:** Additional ~5K particles in Sibernetic initialization, changes to [DD003](DD003_Body_Physics_Architecture.md) Docker stage

### Configuration

```yaml
pharynx:
  enabled: false                     # Off by default until validated
  model: "1d_oscillator"            # "1d_oscillator" (Option A) or "sph" (Option B, future)
  pumping_frequency_target: 3.5     # Hz (validation target, not a simulation parameter)
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `pharynx.enabled` | `false` | `true`/`false` | Enable pharyngeal subsystem |
| `pharynx.model` | `"1d_oscillator"` | `"1d_oscillator"`, `"sph"` | Pumping mechanics model selection |
| `pharynx.pumping_frequency_target` | `3.5` | `1.0`-`10.0` Hz | Validation target (not a simulation parameter) |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)

# Step 1: Verify pharynx doesn't break locomotion
docker compose run quick-test  # with pharynx.enabled: true
# Verify: body still moves (pharynx must not destabilize simulation)
# Verify: pharyngeal output file is generated

# Step 2: Validate pumping frequency
docker compose run simulation -- python scripts/measure_pumping.py
# Verify: pumping rate is 3-4 Hz

# Step 3: Verify backward compatibility
docker compose run quick-test  # with pharynx.enabled: false
# Must produce identical output to pre-pharynx baseline

# Full validation (must pass before merge to main)
docker compose run validate
# Checks:
#   - Tier 3: pumping frequency 3-4 Hz
#   - Tier 3: body kinematic metrics within +/-15%
```

**Per-PR checklist:**

- [ ] `jnml -validate` passes for PharyngealMuscleCell.cell.nml
- [ ] `quick-test` passes with `pharynx.enabled: false` (backward compatibility)
- [ ] `quick-test` passes with `pharynx.enabled: true` (body still moves)
- [ ] Pharyngeal output file generated with contraction values in [0, 1]
- [ ] `measure_pumping.py` reports 3-4 Hz pumping frequency
- [ ] `validate` passes (Tier 3 body kinematics within +/-15%)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `pharynx/pumping_state/` (n_timesteps, 3) | 3-section contraction heatmap | Blue (0 = relaxed) to red (1 = contracted), per section |
| `pharynx/neuron_voltage/` (n_timesteps, 20) | Pharyngeal neuron traces | Standard mV colormap |
| `pharynx/muscle_voltage/` (n_timesteps, 20) | Pharyngeal muscle plateau potentials | Standard mV colormap, plateau visible as sustained red |

### Mechanical Coupling (Option A -> Option B Migration)

**Option A (current):** The 1D oscillator runs independently. No coupling to Sibernetic. Pharynx behavior is output as a time series but does not mechanically affect the body.

**Option B (future):** Requires:

1. ~5,000 additional SPH particles tagged as pharyngeal cells ([DD004](DD004_Mechanical_Cell_Identity.md) cell_identity)
2. Pharyngeal muscle activation -> pharyngeal particle forces (same coupling pattern as [DD002](DD002_Muscle_Model_Architecture.md)->[DD003](DD003_Body_Physics_Architecture.md))
3. Anterior attachment: pharyngeal particles mechanically connected to body wall particles at lips
4. **This changes total particle count** (100K -> 105K), affecting simulation time and memory

**Migration trigger:** Option B is needed only when pharynx-body mechanical interaction matters (e.g., egg-laying, food grinding effects on body movement).

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| c302 HH framework | [DD001](DD001_Neural_Circuit_Architecture.md) | Pharyngeal neurons use same framework — channel model changes propagate |
| CeNGEN differentiation | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Pharyngeal neuron conductances come from CeNGEN |
| Cell identity (Option B) | [DD004](DD004_Mechanical_Cell_Identity.md) | Pharyngeal particle tagging uses [DD004](DD004_Mechanical_Cell_Identity.md)'s cell_id system |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Intestinal input | [DD009](DD009_Intestinal_Oscillator_Model.md) | Eventually pharynx pumps food to intestine — if pumping dynamics change, food arrival rate changes |
| Behavioral validation | [DD010](DD010_Validation_Framework.md) | Pumping frequency is a Tier 3 validation target |
| Body physics (Option B) | [DD003](DD003_Body_Physics_Architecture.md) | Additional particles change total count and body initialization |

---

- **Approved by:** Pending (Phase 3)
- **Implementation Status:** Proposed
- **Next Actions:**

1. Extract pharyngeal neuron expression from CeNGEN
2. Implement pharyngeal muscle HH models with plateau kinetics
3. Create 1D pumping oscillator
4. Validate against pumping frequency
