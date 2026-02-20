# DD009: Intestinal Calcium Oscillator and Defecation Motor Program

**Status:** Proposed (Phase 3)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** None  
**Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD004](DD004_Mechanical_Cell_Identity.md) (Mechanical Cell Identity), [DD008](DD008_Data_Integration_Pipeline.md) (Data Integration)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | 20 intestinal cell models (IP3/Ca2+ oscillator in NeuroML/LEMS), defecation trigger signal, per-cell calcium time series |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: defecation cycle period 50 +/- 10 seconds; posterior-to-anterior wave; >=3 consecutive cycles |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) (`c302_intestine.py`, `intestine/` module) — issues labeled `dd009` |
| **Config toggle** | `intestine.enabled: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` with `intestine.enabled: true` (5s partial cycle), nightly: `measure_defecation_period.py` (200s full validation) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `intestine/calcium/` layer — 20-cell calcium heatmap (posterior-to-anterior wave visible); `intestine/defecation_events/` for pBoc/aBoc/Exp markers |
| **CI gate** | Per-PR: 5s quick-test (no crash); nightly: full 200s period validation (Tier 3) blocks merge |

---

## TL;DR

Model 20 intestinal cells with IP3/Ca2+ oscillator dynamics to reproduce the defecation motor program (~50s period). Calcium waves propagate posterior-to-anterior through gap-junction-coupled intestinal cells and trigger the pBoc, aBoc, Exp behavioral sequence via enteric muscle innervation. Success: oscillation period 50+/-10 seconds, correct wave direction, and >=3 consecutive cycles without damping.

---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Defecation cycle period | 50 +/- 10 seconds (Thomas 1990) | Tier 3 (blocking) |
| **Secondary:** Wave direction | Posterior-to-anterior (int20 -> int1) | Tier 3 (blocking) |
| **Tertiary:** Motor program sequence | pBoc -> aBoc -> Exp in correct temporal order | Tier 3 (blocking) |
| **Quaternary:** Cycle stability | >=3 consecutive cycles without damping | Tier 3 (blocking) |

**Before:** No intestinal model exists. Defecation motor program is absent from the simulation. The organism model has no internal organ dynamics.

**After:** 20 intestinal cells with autonomous IP3/Ca2+ oscillations, gap-junction-coupled to produce posterior-to-anterior calcium waves, triggering the full pBoc -> aBoc -> Exp defecation sequence via DVB/AVL enteric neurons.

---

## Deliverables

| Artifact | Path (relative to `openworm/c302`) | Format | Example |
|----------|-------------------------------------|--------|---------|
| Intestinal cell template | `intestine/IntestinalCell.cell.nml` | NeuroML 2 XML | IP3R + Ca dynamics cell |
| IP3 receptor model | `intestine/IP3Receptor.channel.nml` | NeuroML 2 / LEMS XML | Li-Rinzel IP3R model |
| Intestinal network generator | `c302_intestine.py` | Python script | Generates `LEMS_IntestineOscillator.xml` |
| Enteric muscle coupling | `intestine/intestine_coupling.py` | Python | Couples Ca peaks to DVB/AVL neurons |
| Per-cell calcium time series | Output: `LEMS_IntestineOscillator_calcium.dat` | Tab-separated | `cell_id, timestep, [Ca2+]` |
| Calcium heatmap (viewer) | OME-Zarr: `intestine/calcium/`, shape (n_timesteps, 20) | OME-Zarr array | 20-cell posterior-to-anterior heatmap |
| Defecation event markers (viewer) | OME-Zarr: `intestine/defecation_events/` | OME-Zarr event list | pBoc/aBoc/Exp timestamps |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd009` |
| **Milestone** | Phase 3: Intestinal Oscillator |
| **Branch convention** | `dd009/description` (e.g., `dd009/ip3r-lems-model`) |
| **Example PR title** | `DD009: Implement Li-Rinzel IP3R model in LEMS for intestinal cells` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml

### Step-by-step

```bash
# Step 1: Generate intestinal model
python c302/c302_intestine.py
# Expected output: LEMS_IntestineOscillator.xml

# Step 2: Quick oscillation check (5 seconds sim — one partial cycle)
docker compose run quick-test  # with intestine.enabled: true
# Green light: simulation completes without error
# Green light: intestinal calcium output file exists
# Green light: calcium values are non-zero and oscillatory

# Step 3: Full validation (nightly, not per-PR — 200s sim, ~10 hours wall time)
jnml LEMS_IntestineOscillator.xml -nogui -run 200000  # ms

# Step 4: Extract and measure
python scripts/extract_intestinal_calcium.py LEMS_IntestineOscillator_calcium.dat
python scripts/measure_defecation_period.py intestinal_calcium.csv
python scripts/validate_wave_direction.py intestinal_calcium.csv

# Step 5: Compare to experimental data
python scripts/compare_to_thomas1990.py \
    --simulated defecation_metrics.csv \
    --experimental data/thomas1990_defecation.csv

# Step 6: Verify backward compatibility
docker compose run quick-test  # with intestine.enabled: false
# Must produce identical output to pre-intestine baseline
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `c302_intestine.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `intestine/IntestinalCell.cell.nml` | `[TO BE CREATED]` | openworm/c302#TBD |
| `intestine/IP3Receptor.channel.nml` | `[TO BE CREATED]` | openworm/c302#TBD |
| `intestine/intestine_coupling.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/extract_intestinal_calcium.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/measure_defecation_period.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/validate_wave_direction.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/compare_to_thomas1990.py` | `[TO BE CREATED]` | openworm/c302#TBD |

### Green light criteria

- `c302_intestine.py` generates `LEMS_IntestineOscillator.xml` without error
- 5s quick-test completes, calcium output file exists, values are non-zero
- Full 200s validation: period = 40-60 seconds, wave = posterior-to-anterior, >=3 consecutive cycles

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** `intestine/calcium/` for 20-cell calcium heatmap; `intestine/defecation_events/` for motor program markers.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `intestine/` (new layer group for intestinal dynamics) |
| **Calcium heatmap** | OME-Zarr: `intestine/calcium/`, shape (n_timesteps, 20) — 20 cells ordered posterior-to-anterior |
| **Color mapping** | Warm colormap (blue=low Ca2+ -> red=high Ca2+); posterior-to-anterior wave should be visible as a diagonal stripe |
| **Event markers** | `intestine/defecation_events/` — pBoc (red), aBoc (orange), Exp (yellow) vertical markers on timeline |
| **What you should SEE** | Rhythmic calcium waves sweeping from int20 (posterior) to int1 (anterior) every ~50 seconds. Each wave peak is followed by pBoc/aBoc/Exp event markers. At least 3 complete cycles visible in a 200s simulation. |

---

## Technical Approach

### Model the 20 Intestinal Cells with IP3/Calcium Oscillator Dynamics

Each intestinal cell has:
- **Membrane voltage** (HH framework as in [DD001](DD001_Neural_Circuit_Architecture.md)/DD002, but with intestine-specific channels)
- **Cytoplasmic [Ca2+]**
- **ER luminal [Ca2+]_ER**
- **[IP3]** (inositol 1,4,5-trisphosphate)

**Coupled ODEs:**

```
(1) Membrane voltage (simplified HH):
C * dV/dt = I_leak + I_K + I_Ca + I_gap

(2) Cytoplasmic calcium:
d[Ca]/dt = J_release - J_pump - J_leak_ER + J_influx

Where:
- J_release = IP3 receptor flux from ER (IP3-gated, Ca-activated)
- J_pump = SERCA pump (Ca back into ER)
- J_leak_ER = passive ER leak
- J_influx = voltage-gated Ca channels on plasma membrane

(3) ER calcium:
d[Ca]_ER/dt = (J_pump - J_release - J_leak_ER) * (V_cyto / V_ER)

(4) IP3 dynamics:
d[IP3]/dt = k_production - k_degradation * [IP3]
```

### IP3 Receptor Model (ITR-1)

Use a **simplified Li-Rinzel model** (reduction of the DeYoung-Keizer IP3R model):

```
J_release = v_release * m_inf^3 * n * h * ([Ca]_ER - [Ca])

Where:
- m_inf = [IP3] / ([IP3] + K_IP3)  # IP3 binding (instantaneous)
- dn/dt = (n_inf - n) / tau_n      # Ca activation gate (slow, ~seconds)
- dh/dt = (h_inf - h) / tau_h      # Ca inactivation gate (slow)
- n_inf, h_inf depend on [Ca] and [IP3]
```

Parameters (fit to match ~50 second period):
- v_release (max release rate): ~10 uM/s
- K_IP3 (IP3 half-activation): ~0.3 uM
- Ca activation threshold: ~0.2 uM
- Ca inactivation threshold: ~0.4 uM

### Gap Junction Coupling (Inter-Intestinal Cell Synchronization)

Intestinal cells are electrically coupled via **gap junctions** (innexins: inx-3, inx-16). This synchronizes the calcium oscillations.

```
I_gap = g_gap * sum (V_neighbor - V)
```

Where g_gap = 0.5-1.0 nS (higher than neuronal gap junctions to ensure synchrony).

**Cell topology:** Linear chain (int1 <-> int2 <-> int3 ... <-> int20) with additional anterior-posterior skip connections.

### Coupling to Enteric Muscles (Defecation Motor Program)

The intestinal calcium wave triggers the **defecation motor program** via innervation of 4 enteric muscles:

| Muscle | Innervation | Function | Contraction Trigger |
|--------|-------------|----------|-------------------|
| Anal depressor | DVB, AVL neurons | Opens anus | Intestinal Ca wave -> neuron activation |
| Anal sphincter | AVL | Controls expulsion | |
| Enteric muscles (posterior) | DVB | pBoc (posterior body contraction) | |
| Enteric muscles (anterior) | AVL | aBoc (anterior body contraction) | |

**Coupling:** When intestinal [Ca2+] peaks (oscillator peak), release signal to DVB/AVL neurons -> activate enteric muscles -> trigger pBoc/aBoc/Exp sequence.

---

## Alternatives Considered

### 1. Neural Pacemaker Model (Not Intrinsic Intestinal Oscillations)

**Hypothesis:** Defecation is driven by a neural pacemaker circuit, not intestinal oscillations.

**Rejected:** Experiments show intestinal calcium oscillations are **cell-autonomous** (Thomas 1990, Dal Santo et al. 1999). Isolated intestinal cells oscillate in culture. Neurons modulate but do not generate.

### 2. Detailed ER Geometry and Diffusion

**Description:** Explicitly model ER tubules and cisternae with 3D geometry, solve Ca2+ diffusion within ER lumen.

**Rejected (Phase 3):** Simplified lumped-pool ER model (single [Ca]_ER variable) is sufficient to produce oscillations. Detailed ER geometry is future work if spatial Ca2+ gradients within cells prove essential.

### 3. Mitochondrial Calcium Buffering

**Description:** Add mitochondria as a third calcium pool (cytoplasm, ER, mitochondria).

**Deferred:** Mitochondria buffer calcium but likely do not drive the oscillations. Add if simple IP3R + ER model fails to match ~50s period.

---

## Quality Criteria

1. **Oscillation Period:** Simulated defecation cycle period must be 50 +/- 10 seconds (Thomas 1990 experimental data).

2. **Wave Direction:** Calcium wave must propagate **posterior-to-anterior** (int20 -> int1).

3. **Cell Autonomy:** Individual intestinal cells must oscillate when uncoupled (zero gap junction conductance). Coupling synchronizes but does not create oscillations.

4. **Motor Program Sequence:** Must reproduce pBoc -> aBoc -> Exp in correct temporal order.

---

## Boundaries (Explicitly Out of Scope)

1. **Food particle transport:** Bacteria flowing through pharyngeal-intestinal lumen not modeled.
2. **Intestinal gene regulation:** Transcription factor dynamics, metabolic state out of scope.
3. **Developmental changes:** Focus on adult L4/adult. Larval stages future work.

---

## Context & Background

The *C. elegans* intestine is a 20-cell tube (int1-int9 in anterior, int10-int20 in posterior) that comprises approximately one-third of the organism's somatic mass. It is the **pacemaker for the defecation motor program**, a stereotyped behavioral sequence with ~50 second period:

1. **Posterior body contraction (pBoc):** Muscles in posterior compress intestine
2. **Anterior body contraction (aBoc):** Wave propagates forward
3. **Expulsion step (Exp):** Anal depressor and sphincter muscles contract, expelling contents

The intestinal oscillator is driven by **IP3 receptor (ITR-1) mediated calcium waves** that propagate posterior-to-anterior through the 20 intestinal cells via gap junction coupling. Calcium oscillations are **cell-autonomous** (persist in isolated intestinal cells) and require endoplasmic reticulum (ER) calcium stores.

---

## References

1. **Thomas JH (1990).** "Genetic analysis of defecation in *Caenorhabditis elegans*." *Genetics* 124:855-872.
2. **Dal Santo P, Logan MA, Chisholm AD, Jorgensen EM (1999).** "The inositol trisphosphate receptor regulates a 50-second behavioral rhythm in *C. elegans*." *Cell* 98:757-767.
3. **Teramoto T, Iwasaki K (2006).** "Intestinal calcium waves coordinate a behavioral motor program in *C. elegans*." *Cell Calcium* 40:319-327.

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| IP3 production rate | Internal (cell-autonomous) | `k_production` | Scalar parameter per cell | uM/s |
| Gap junction conductances | [DD001](DD001_Neural_Circuit_Architecture.md) framework (innexin expression) | `g_gap` per innexin pair | NeuroML `<gapJunction>` | nS |
| CeNGEN expression (intestinal cells) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Per-cell channel densities | NeuroML `<channelDensity>` | S/cm2 |
| Intestinal cell positions | [DD004](DD004_Mechanical_Cell_Identity.md) (when cell_identity enabled) | 3D coordinates for int1-int20 | Cell-to-particle mapping JSON | um |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Intestinal [Ca2+] per cell | [DD004](DD004_Mechanical_Cell_Identity.md) (drives intestinal particle mechanics) | Per-cell calcium time series | Tab-separated: cell_id, timestep, [Ca2+] | uM |
| Defecation trigger signal | [DD001](DD001_Neural_Circuit_Architecture.md) (DVB/AVL neuron activation) | Binary trigger when Ca peaks in int1 | Event file: timestamp of each peak | ms |
| Defecation motor program state | [DD010](DD010_Validation_Framework.md) (Tier 3 validation) | pBoc/aBoc/Exp occurrence timestamps | Tab-separated event log | ms |
| ER [Ca2+] per cell | Internal (diagnostics) | Per-cell ER calcium time series | Tab-separated | uM |
| Intestinal calcium time series (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-cell [Ca2+] over all timesteps | OME-Zarr: `intestine/calcium/`, shape (n_timesteps, 20) | uM |
| Defecation event markers (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | pBoc/aBoc/Exp event timestamps | OME-Zarr: `intestine/defecation_events/` | ms |

### Repository & Packaging

- **Repository:** `openworm/c302` (same package, new module)
- **Docker stage:** `neural` (same as [DD001](DD001_Neural_Circuit_Architecture.md) — intestinal models use NeuroML/LEMS)
- **No additional Docker changes** for the intestinal oscillator itself
- **Coupling to [DD004](DD004_Mechanical_Cell_Identity.md) particles** (future): requires `body` stage to have cell_identity enabled

**Repository structure:**
```
c302/
├── c302_intestine.py              # NEW: Intestinal network generation
├── intestine/
│   ├── IntestinalCell.cell.nml    # IP3R + Ca dynamics cell template
│   ├── IP3Receptor.channel.nml    # Li-Rinzel IP3R model in LEMS
│   └── intestine_coupling.py     # Coupling to enteric muscles ([DD001](DD001_Neural_Circuit_Architecture.md) neurons DVB/AVL)
```

### Configuration

**`openworm.yml` Section:**

```yaml
intestine:
  enabled: false                    # Off by default until validated
  model: "ip3_calcium"             # Only option for now
  oscillator_period_target: 50.0   # seconds (validation target, not simulation parameter)
  gap_junction_conductance: 0.75   # nS (default, tunable)
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `intestine.enabled` | `false` | `true`/`false` | Enable intestinal oscillator module |
| `intestine.model` | `"ip3_calcium"` | `"ip3_calcium"` | Oscillator model type (only one for now) |
| `intestine.oscillator_period_target` | `50.0` | 30-70 seconds | Validation target period (not a simulation parameter) |
| `intestine.gap_junction_conductance` | `0.75` | 0.1-2.0 nS | Gap junction conductance between adjacent intestinal cells |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (5 seconds sim — must pass before submission)
docker compose run shell python c302/c302_intestine.py
# Check: LEMS_IntestineOscillator.xml created without error

docker compose run quick-test  # with intestine.enabled: true
# Check: simulation completes without error
# Check: intestinal calcium output file exists
# Check: calcium values are non-zero and oscillatory

# Full validation (nightly, not per-PR — 200s sim)
docker compose run simulation -- \
  python scripts/measure_defecation_period.py \
  --duration 200000 \
  --expected_period 50 \
  --tolerance 10
# Check: period = 50 +/- 10 seconds
# Check: wave direction = posterior-to-anterior
# Check: >=3 consecutive cycles without damping

# Backward compatibility (must pass)
docker compose run quick-test  # with intestine.enabled: false
# Check: identical output to pre-intestine baseline
```

**Per-PR checklist:**
- [ ] `c302_intestine.py` generates LEMS XML without error
- [ ] `jnml -validate` passes on generated XML
- [ ] `quick-test` passes with `intestine.enabled: true`
- [ ] `quick-test` passes with `intestine.enabled: false` (backward compat)
- [ ] No NaN values in calcium output
- [ ] Calcium values are oscillatory (not flat, not diverging)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `intestine/calcium/` (n_timesteps, 20) | Intestinal calcium heatmap | Warm colormap (blue=low -> red=high Ca2+), posterior-to-anterior wave visible as diagonal stripe |
| `intestine/defecation_events/` | Defecation event markers | pBoc (red), aBoc (orange), Exp (yellow) vertical markers on timeline |

### Compute Budget Warning

**Validation requires 200 seconds of simulated time** (4 defecation cycles at ~50s each). At current performance:

| Metric | Value | Implication |
|--------|-------|-------------|
| Simulation wall time | ~10 hours for 200s sim | Not practical for CI (use nightly builds) |
| Memory (with video pipeline) | >64 GB (OOM) | **Video pipeline memory leak ([DD013](DD013_Simulation_Stack_Architecture.md) Issue #332) MUST be fixed first** |
| Memory (no video) | ~4 GB | Feasible if video is disabled |
| CI strategy | Nightly validation job, not per-PR | Per-PR tests run 5s (one partial cycle), nightly runs 200s |

**The memory leak in the video/plotting pipeline is a BLOCKING dependency for intestinal validation.** Until fixed, intestinal validation can only run with `output.video: false` and `output.plots: false`.

### Coupling to Enteric Muscles (Defecation Motor Program)

The intestinal calcium wave must trigger enteric muscle contraction via the neural circuit. **Interface:**

1. Intestinal oscillator produces per-cell [Ca2+] time series
2. When int1 [Ca2+] peaks (anterior cell), a **trigger signal** is sent to DVB and AVL neurons in the [DD001](DD001_Neural_Circuit_Architecture.md) neural circuit
3. DVB/AVL activate enteric muscles via standard NMJ synapses ([DD002](DD002_Muscle_Model_Architecture.md) framework)
4. Enteric muscles contract -> pBoc -> aBoc -> Exp sequence

**Coupling mechanism:** A new coupling script (`intestine_coupling.py`) translates intestinal calcium peaks into current injection on DVB/AVL neurons. This is analogous to how `sibernetic_c302.py` couples neural output to body physics.

### Coupling to [DD004](DD004_Mechanical_Cell_Identity.md) (Mechanical Identity)

When `body.cell_identity: true`, intestinal cells are represented by tagged SPH particles. The coupling works as:

1. [DD009](DD009_Intestinal_Oscillator_Model.md) outputs per-cell activation (from [Ca2+])
2. [DD004](DD004_Mechanical_Cell_Identity.md)'s cell-to-particle mapping translates cell_id -> list of particle indices
3. Intestinal particle elasticity is modulated: `k_particle = k_baseline * (1 + activation * peristalsis_strength)`
4. This produces peristaltic waves in the SPH simulation

**This coupling is Phase 4 work** (requires [DD004](DD004_Mechanical_Cell_Identity.md) to be implemented first).

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| NeuroML/LEMS framework | [DD001](DD001_Neural_Circuit_Architecture.md) | Intestinal cells use same framework — solver or channel model changes propagate |
| CeNGEN expression (intestinal cells) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | If intestinal cell expression data changes, channel densities change, period may shift |
| Cell identity (for mechanical coupling) | [DD004](DD004_Mechanical_Cell_Identity.md) | If intestinal cell_ids change, wrong particles contract |
| Video pipeline fix | [DD013](DD013_Simulation_Stack_Architecture.md) (Issue #332) | Until fixed, cannot run 200s validation with video/plots enabled |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Validation (defecation cycle) | [DD010](DD010_Validation_Framework.md) | Defecation period is a Tier 3 validation target; if oscillator dynamics change, validation criteria may need updating |
| Neural circuit (DVB/AVL activation) | [DD001](DD001_Neural_Circuit_Architecture.md) | If trigger signal timing or format changes, enteric muscle activation breaks |
| Mechanical identity (peristalsis) | [DD004](DD004_Mechanical_Cell_Identity.md) | If per-cell activation format changes, particle force modulation breaks |
| Pharynx (food transport, future) | [DD007](DD007_Pharyngeal_System_Architecture.md) | Eventually pharynx pumps food to intestine; if intestinal acceptance changes, food arrival modeling is affected |

---

**Approved by:** Pending (Phase 3)
**Implementation Status:** Proposed
**Next Actions:**
1. Implement IP3R dynamics in LEMS
2. Add intestinal cell-specific HH models from CeNGEN
3. Couple to enteric muscles
4. Validate against 50s period
