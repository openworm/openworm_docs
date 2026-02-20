# DD018: Egg-Laying System Architecture (Reproductive Behavioral Circuit)

**Status:** Proposed (Phase 3)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-16  
**Supersedes:** None  
**Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD004](DD004_Mechanical_Cell_Identity.md) (Mechanical Cell Identity), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell Differentiation), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptidergic Connectome)

---

## TL;DR

Model the *C. elegans* egg-laying system as a 24-cell circuit comprising 2 serotonergic HSN command neurons, 6 cholinergic VC motor neurons, and 16 non-striated sex muscles (8 vulval + 8 uterine), with uv1 neuroendocrine feedback cells providing tyramine-mediated inhibition. The circuit produces a characteristic two-state behavioral pattern: ~20-minute inactive phases alternating with ~2-minute active bouts of 3-5 eggs each. Success: reproduce the two-state temporal pattern within quantitative bounds of [Collins et al. 2016](https://doi.org/10.7554/eLife.21126) experimental data.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 3](DD_PHASE_ROADMAP.md#phase-3-organ-systems-hybrid-ml-months-7-12) |
| **Layer** | Organ Systems — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-3-organ-systems-hybrid-ml-months-7-12) |
| **What does this produce?** | Egg-laying circuit: 2 HSN neurons + 6 VC neurons + 16 sex muscles (NeuroML), serotonergic/cholinergic signaling, two-state behavioral output |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: egg-laying bout interval 20 +/- 10 min, 3-5 eggs per bout; inactive/active two-state pattern reproduced |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) (`c302_egglaying.py`, `egglaying/` module) — issues labeled `dd018` |
| **Config toggle** | `egglaying.enabled: true` / `egglaying.model: "circuit"` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` with `egglaying.enabled: true` (body still moves?), `scripts/measure_egglaying.py` (two-state pattern?) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `egglaying/muscle_activation/` layer — 16 sex muscles with contraction heatmap; `egglaying/circuit_state/` for active/inactive state timeline |
| **CI gate** | Two-state behavioral validation (Tier 3) blocks merge; backward compatibility with `egglaying.enabled: false` required |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Two-state temporal pattern | Inactive state ~20 +/- 10 min; active state ~2 min; 3-5 eggs per bout | Tier 3 (blocking) |
| **Secondary:** Body locomotion preservation | Within +/-15% of baseline kinematic metrics when egg-laying circuit enabled | Tier 3 (blocking) |
| **Tertiary:** Serotonin-induced egg-laying | Simulated exogenous serotonin produces sustained active state (pharmacological validation) | Tier 1 (non-blocking) |
| **Quaternary:** Mutant phenotype reproduction | egl-1 (no egg-laying), unc-103(lf) (hyperactive), egl-36(gf) (Egl) reproduced qualitatively | Tier 1 (non-blocking) |

**Before:** No egg-laying circuit. HSN and VC neurons exist in the connectome but have no sex-muscle targets. No vulval or uterine muscles modeled. No reproductive behavior.

**After:** A functional egg-laying circuit producing rhythmic two-state behavior. Serotonergic command neurons drive vulval muscle contraction via feed-forward excitation with tyraminergic feedback inhibition. Egg-laying events are visible as synchronized vulval muscle calcium transients in the [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer.

---

## Deliverables

| Artifact | Path (relative to `openworm/c302`) | Format | Example |
|----------|-------------------------------------|--------|---------|
| Vulval muscle cell template (vm1) | `egglaying/VulvalMuscle1Cell.cell.nml` | NeuroML 2 XML | Non-striated HH with EGL-19, UNC-103, EGL-36 channels |
| Vulval muscle cell template (vm2) | `egglaying/VulvalMuscle2Cell.cell.nml` | NeuroML 2 XML | Same channels + postsynaptic nAChR, SER-1 receptor |
| Uterine muscle cell template (um) | `egglaying/UterineMuscleCell.cell.nml` | NeuroML 2 XML | Simplified; gap-junction-coupled to vm2 |
| HSN neuron differentiated template | `cells/HSNCell.cell.nml` | NeuroML 2 XML | Serotonergic; NLP-3 co-release (if [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) enabled) |
| VC neuron differentiated template | `cells/VCCell.cell.nml` | NeuroML 2 XML | Cholinergic; mechanosensitive |
| uv1 neuroendocrine cell template | `egglaying/UV1Cell.cell.nml` | NeuroML 2 XML | Tyraminergic; releases NLP-7, FLP-11 |
| Egg-laying network generator | `c302_egglaying.py` | Python | Generates circuit: 2 HSN + 6 VC + 16 sex muscles + 4 uv1 |
| Serotonergic synapse model | `egglaying/SerotoninSynapse.synapse.nml` | NeuroML 2 XML | Graded serotonin release -> SER-1 GPCR -> Gaq -> DAG |
| Tyramine inhibitory synapse model | `egglaying/TyramineSynapse.synapse.nml` | NeuroML 2 XML | LGC-55 Cl- channel; EC50 = 12.1 uM |
| Egg-laying state time series (viewer) | OME-Zarr: `egglaying/circuit_state/` | Shape (n_timesteps, 1) | Binary: 0 (inactive) / 1 (active) |
| Vulval muscle activation (viewer) | OME-Zarr: `egglaying/muscle_activation/` | Shape (n_timesteps, 16) | Per-muscle [Ca2+] activation [0, 1] |
| Egg event log (viewer) | OME-Zarr: `egglaying/egg_events/` | Event timestamps | Timestamp of each simulated egg-laying event |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd018` |
| **Milestone** | Phase 3: Organ Systems |
| **Branch convention** | `dd018/description` (e.g., `dd018/hsn-serotonin-synapse`) |
| **Example PR title** | `DD018: Add vulval muscle cell templates with EGL-19/UNC-103 channels` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, pandas, numpy, scipy

### Step-by-step

```bash
# Step 1: Generate egg-laying circuit network
cd c302/
python c302_egglaying.py
# Expected output: LEMS_c302_EggLaying.xml with 28 cells
# (2 HSN + 6 VC + 4 vm1 + 4 vm2 + 4 um1 + 4 um2 + 4 uv1)

# Step 2: Validate NeuroML/LEMS files
jnml -validate egglaying/VulvalMuscle2Cell.cell.nml
jnml -validate egglaying/SerotoninSynapse.synapse.nml
jnml -validate LEMS_c302_EggLaying.xml
# Expected: all pass

# Step 3: Quick test — egg-laying circuit only (isolated, no body)
docker compose run quick-test  # with egglaying.enabled: true
# Green light: simulation completes, no NaN values
# Green light: vulval muscle Ca2+ transients observed
# Green light: two-state pattern visible (inactive/active alternation)

# Step 4: Run coupled simulation (egg-laying + locomotion)
docker compose run simulation -- \
  python scripts/run_egglaying_coupled.py \
  --duration 3600000 \
  --output egglaying_results/
# [TO BE CREATED] — 1 hour simulated time (3 full bouts expected)

# Step 5: Measure egg-laying temporal pattern
python scripts/measure_egglaying.py \
  --input egglaying_results/muscle_activation.dat \
  --expected_bout_interval 20 \
  --expected_eggs_per_bout 4 \
  --tolerance_minutes 10
# [TO BE CREATED]

# Step 6: Validate backward compatibility
docker compose run quick-test  # with egglaying.enabled: false
# Must produce identical output to pre-egg-laying baseline

# Step 7: Pharmacological validation (exogenous serotonin)
python scripts/test_serotonin_response.py \
  --serotonin_concentration 10 \
  --expected sustained_active_state
# [TO BE CREATED]
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `c302_egglaying.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/run_egglaying_coupled.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/measure_egglaying.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/test_serotonin_response.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/test_mutant_phenotypes.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/plot_egglaying_raster.py` | `[TO BE CREATED]` | openworm/c302#TBD |

### Green light criteria

- Vulval muscle Ca2+ transients alternate between rare/low-amplitude (inactive) and rhythmic/high-amplitude (active)
- Inactive state duration: 10-30 minutes (mean ~20 min)
- Active state duration: 1-3 minutes (mean ~2 min)
- Eggs per active bout: 3-5
- Body locomotion not degraded (Tier 3 kinematics within +/-15%)
- No NaN values, no voltage explosions

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layers:**

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer 1** | `egglaying/muscle_activation/` — 16 sex muscles with [0, 1] activation heatmap |
| **Layer 2** | `egglaying/circuit_state/` — Binary timeline showing inactive (blue) vs. active (red) states |
| **Layer 3** | `egglaying/egg_events/` — Discrete markers at each egg-laying event timestamp |
| **Color mapping** | Muscles: warm colormap (blue=relaxed, red=contracted). Circuit state: blue/red binary. Egg events: yellow pulse markers. |
| **What you should SEE** | Long blue (inactive) periods of ~20 min punctuated by short red (active) bursts of ~2 min. During active bursts, 8 vulval muscles contract synchronously 3-5 times with ~20 s intervals. HSN calcium trace shows sustained bursts during active state. |
| **Comparison view** | Wild-type vs. egl-1 (no HSN → no active states) vs. unc-103(lf) (no inactive states → constant activity) |

---

## Technical Approach

### Circuit Architecture: Feed-Forward Excitation with Feedback Inhibition

The egg-laying circuit implements a three-component motif (Zhang et al. 2008):

1. **HSN command neurons** (2 cells: HSNL, HSNR) — serotonergic pacemakers that drive active states
2. **VC motor neurons** (6 cells: VC1-VC6) — cholinergic relay; VC4/VC5 are vulva-proximal and synapse on vm2
3. **Vulval muscles** (8 cells: 4 vm1 + 4 vm2) — effectors that contract to open the vulval slit
4. **uv1 neuroendocrine cells** (4 cells) — feedback inhibitors sensing egg passage

**Circuit connectivity:**

```
                    ┌──────────────────────────────┐
                    │         (tyramine inhibition)  │
                    │                                │
                    ▼                                │
    HSN ─────────► VC4/VC5 ─────────► vm2 ─────► egg passage ──► uv1
     │  (serotonin)  │   (ACh/nAChR)    ▲                          │
     │               │                  │                          │
     └───────────────┼──────────────────┘                          │
     (direct NMJ     │   (gap junctions: vm1↔vm2, um↔vm2)         │
      to vm2)        │                                              │
                     └──────────────────────────────────────────────┘
                           (VC inhibits HSN — feedback)
```

### HSN Neuron Model

HSN neurons are serotonergic command neurons that act as the primary driver of egg-laying. They release both serotonin and NLP-3 neuropeptides.

**HSN dynamics:** HSN neurons generate sustained calcium bursts during active states. The burst-to-silence transition is driven by:

1. Intrinsic HSN excitability (modulated by Gaq/EGL-30 signaling)
2. Feedback inhibition from uv1 (tyramine via LGC-55 Cl- channel)
3. Feedback inhibition from VC neurons (during active state)

**HSN channel complement (from CeNGEN, [DD005](DD005_Cell_Type_Differentiation_Strategy.md)):**

- Standard c302 HH channels (leak, K_slow, K_fast, Ca_boyle)
- Cell-type-specific conductance densities from CeNGEN expression
- Additional: serotonin vesicular release mechanism (Ca2+-dependent exocytosis)

**Serotonin release model:**

```
d[5-HT]_released/dt = k_release * max(0, ([Ca2+]_HSN - ca_threshold)) - [5-HT]_released / tau_clearance
```

Where:

- k_release: serotonin release rate (Ca2+-dependent)
- ca_threshold: calcium threshold for vesicle fusion
- tau_clearance: serotonin reuptake/degradation time constant (~1-5 s)

**NLP-3 neuropeptide co-release:**

- Dense core vesicle release, slower than small clear vesicle serotonin
- Either serotonin or NLP-3 alone provides partial drive; both required for full HSN function
- Modeled as [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) `<peptideRelease>` component if neuropeptides are enabled

### VC Neuron Model

VC neurons are cholinergic motor neurons with a dual role: they excite vm2 muscles AND provide feedback inhibition to HSN.

**VC specialization:**

- **VC4, VC5** (vulva-proximal): Make extensive chemical synapses onto vm2 muscles; synapse onto HSN
- **VC1-3, VC6** (distant): Synapse onto ventral body wall muscles; mediate locomotion slowing during egg-laying

**VC4/VC5 are mechanosensitive** (Kopchock et al. 2021):

- Vulval muscle contraction activates VC4/VC5 mechanically
- This creates a positive feedback loop during active state: vm2 contraction -> VC activation -> more vm2 contraction
- Mechanosensory activation modeled as stretch-dependent current injection

**Acetylcholine release from VC4/VC5 -> vm2:**

```
ACh release -> nAChR on vm2 -> Na+ influx -> local depolarization -> EGL-19 activation -> Ca2+ entry
```

### Vulval Muscle Model (vm1 and vm2)

Vulval muscles are non-striated, excitable cells distinct from body wall muscles ([DD002](DD002_Muscle_Model_Architecture.md)). They generate calcium-dependent potentials, not classical action potentials.

**vm2 ion channels (the critical muscle):**

| Channel | Gene | Type | Conductance | Role |
|---------|------|------|-------------|------|
| L-type Ca2+ | `egl-19` | CaV1 voltage-gated | ~0.001 S/cm² | Primary Ca2+ entry; depolarization-activated |
| ERG K+ | `unc-103` | Kir-family K+ | ~0.0005 S/cm² | Repolarization brake; maintains inactive state |
| Shaw K+ | `egl-36` | Kv3 (Shaw-type) | ~0.0003 S/cm² | Regulates excitability threshold |
| Leak | (multiple) | Background | ~5e-7 S/cm² | Resting potential maintenance |
| nAChR | (nicotinic) | Ligand-gated cation | Synapse-dependent | Postsynaptic ACh receptor from VC4/VC5 |

**Note:** vm2 conductance densities are approximate. EGL-19 and UNC-103 are the two most critical channels — EGL-19 drives calcium entry for contraction; UNC-103 (ERG K+) keeps the muscle subthreshold during the inactive state. The balance between these two channels is the primary determinant of the two-state pattern.

**vm1 model:**

- Same channel types as vm2 but **no direct synaptic input**
- Receives rhythmic excitation from VA/VB motor neurons via body wall muscle connections (ACh, every ~10 s during locomotion body bends)
- Gap-junction-coupled to vm2: calcium transients initiate in vm1 and propagate to vm2 ([Brewer et al. 2019](https://doi.org/10.1371/journal.pgen.1007896))

**Calcium dynamics in vulval muscles:**

```
d[Ca2+]/dt = -rho * I_Ca_EGL19 - [Ca2+] / tau_Ca + J_IP3R

Where:
- I_Ca_EGL19 = EGL-19 L-type Ca2+ current (depolarization-activated)
- tau_Ca = calcium clearance time constant (~20 ms)
- J_IP3R = IP3 receptor-mediated ER release (ITR-1; secondary Ca2+ source)
```

**Two-state mechanism (key insight):**

The two-state pattern emerges from the balance between EGL-19 (excitatory) and UNC-103 ERG (inhibitory) channels on vm2:

- **Inactive state:** UNC-103 ERG K+ channels keep vm2 membrane potential below the EGL-19 activation threshold. Body-bend-driven rhythmic depolarization from vm1 (via gap junctions) is subthreshold. Rare, low-amplitude Ca2+ transients.

- **Active state transition:** HSN releases serotonin -> SER-1 -> Gaq (EGL-30) -> Trio RhoGEF -> DAG -> increased EGL-19 open probability and/or decreased UNC-103 activity. Now each body-bend-driven depolarization triggers a full Ca2+ transient -> muscle contraction -> egg-laying event.

- **Active state termination:** Egg passage through vulva -> uv1 cells mechanosensing -> tyramine release -> LGC-55 Cl- channel on HSN -> HSN inhibition -> serotonin withdrawal -> vm2 returns to subthreshold.

### Uterine Muscle Model (um1, um2)

8 uterine muscles encircle the uterus and contract to squeeze eggs toward the vulva.

- Gap-junction-coupled to vm2 muscles
- Contraction is coordinated with vulval muscle opening
- Uterine stretch from accumulated eggs (2-3) provides a permissive mechanical signal for active state entry

**Simplified model:** Uterine muscles receive calcium spread from vm2 via gap junctions. No direct synaptic input modeled in Phase 3.

### uv1 Neuroendocrine Feedback Model

4 uv1 cells sit at the uterine-vulval junction and sense egg passage mechanically.

**uv1 outputs:**

1. **Tyramine** → LGC-55 (Cl- channel, EC50 = 12.1 uM) on HSN → hyperpolarization → HSN silencing
2. **NLP-7 neuropeptide** → inhibits serotonin vesicular release from HSN (if [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) enabled)
3. **FLP-11 neuropeptide** → inhibits circuit activity (if [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) enabled)

**uv1 mechanosensory activation:**

```
I_mechano = g_mechano * max(0, stretch - stretch_threshold)
```

Where stretch is computed from vulval muscle contraction state (vm2 activation). When an egg passes, stretch is maximal, activating uv1.

### Gap Junction Network

Gap junctions are critical for coordinating the 16 sex muscles into synchronized contraction:

| Connection | Innexin | Conductance | Function |
|------------|---------|-------------|----------|
| vm1 ↔ vm1 | inx-? | ~1.0 nS | Synchronize vm1 cells |
| vm2 ↔ vm2 | inx-? | ~1.0 nS | Synchronize vm2 cells (X-pattern) |
| vm1 ↔ vm2 | inx-? | ~0.5 nS | Propagate Ca2+ from vm1 to vm2 |
| um ↔ vm2 | inx-? | ~0.3 nS | Coordinate uterine squeeze with vulval opening |
| HSN ↔ VC4/VC5 | inx-? | ~0.2 nS | Electrical coupling between command and motor neurons |

### Serotonin Receptor Signaling Cascade

The intracellular cascade from serotonin binding to muscle excitability change is critical for the two-state transition:

```
Serotonin (from HSN)
   │
   ▼
SER-1 (Gaq-coupled GPCR on vm2)
   │
   ▼
EGL-30 (Gaq) activation
   │
   ├──► Trio RhoGEF ──► DAG ──► increased EGL-19 open probability
   │                             (and/or decreased UNC-103)
   │
   └──► PLCbeta (EGL-8) ──► IP3 ──► ITR-1 ──► ER Ca2+ release
        [primarily in neurons]       [in muscles: secondary]
```

**Modeling approach:** The full Gaq -> Trio -> DAG cascade is complex (10+ state variables). For Phase 3, use a **phenomenological modulation model**:

```
g_EGL19_effective = g_EGL19_baseline * (1 + serotonin_modulation)
g_UNC103_effective = g_UNC103_baseline * (1 - serotonin_modulation * 0.3)

Where:
  serotonin_modulation = [5-HT]_at_vm2 / ([5-HT]_at_vm2 + K_d_SER1)
  K_d_SER1 = ~1 uM (SER-1 binding affinity, estimated)
```

This captures the net effect: serotonin increases Ca2+ channel conductance and decreases K+ channel conductance, shifting vm2 from subthreshold to suprathreshold.

### Locomotion-Egg-Laying Coupling

Egg-laying is mechanically coupled to locomotion via body bends:

1. VA/VB motor neurons drive body wall muscle contraction every ~10 s (body bend period)
2. vm1 muscles are innervated by ventral cord motor neurons alongside body wall muscles
3. Each body bend delivers a rhythmic depolarizing pulse to vm1 → gap junctions → vm2
4. During inactive state: subthreshold. During active state: each pulse triggers egg-laying Ca2+ transient

**Coupling variable:** Body bend phase (from [DD001](DD001_Neural_Circuit_Architecture.md)/DD003 locomotion circuit) provides periodic current injection to vm1:

```
I_body_bend = A_bend * sin(2*pi*t / T_bend)

Where:
  A_bend = body-bend-driven current amplitude (~0.5 nA, same as NMJ drive)
  T_bend = ~10 s (body bend period, from locomotion simulation)
```

### Egg Event Model

An egg-laying event is triggered when:

1. All 8 vulval muscles are synchronously contracted (vm1 + vm2 calcium above threshold)
2. AND uterine muscles are contracted (squeeze)
3. The egg counter increments; egg passage triggers uv1 feedback

**Egg counter logic:**

```python
if all(vm_calcium[i] > egg_threshold for i in range(8)):
    egg_count += 1
    trigger_uv1_feedback()
    if egg_count >= eggs_in_uterus:
        egg_count = 0  # uterus empty
```

Eggs accumulate in the uterus at ~1 per 10 min per gonad arm. The uterus holds 10-15 eggs at steady state (wild type).

---

## Alternatives Considered

### 1. Ignore Egg-Laying (Locomotion Only)

**Description:** Focus exclusively on locomotion and body wall muscle contraction; do not model the reproductive system.

**Rejected because:**

- Egg-laying is one of the most-studied *C. elegans* behaviors with rich quantitative data
- The circuit is small (28 cells) and well-characterized — ideal for whole-organism modeling
- HSN and VC neurons already exist in the [DD001](DD001_Neural_Circuit_Architecture.md) connectome; their primary function is egg-laying
- Egg-laying provides a distinct behavioral validation target (two-state pattern) orthogonal to locomotion

### 2. Abstract State Machine (No Biophysical Circuit)

**Description:** Model egg-laying as a two-state Markov chain (inactive ↔ active) without biophysical neurons or muscles.

**Rejected because:**

- Throws away the mechanistic causal chain that OpenWorm aims to capture
- Cannot predict mutant phenotypes (egl-1, unc-103, etc.)
- Cannot respond to simulated pharmacology (exogenous serotonin)
- The Sun & Bhatt 2010 circuit model already shows that biophysical modeling is feasible

**When to reconsider:** If computational cost is prohibitive; could use as a fast approximation for parameter sweeps.

### 3. Full Gaq/DAG Biochemical Cascade

**Description:** Explicitly model the Gaq → PLCbeta / Trio RhoGEF → DAG → PKC → channel phosphorylation cascade with 15+ state variables per cell.

**Rejected (for Phase 3) because:**

- Biochemical rate constants are largely unknown for *C. elegans* Gaq signaling in vulval muscles
- Phenomenological conductance modulation captures the net functional effect
- Phase 5 (intracellular signaling) is the appropriate place for detailed biochemical cascades

**When to reconsider:** Phase 5, when IP3/DAG/PKC cascades are added for non-neural cells.

### 4. Treat Vulval Muscles as Identical to Body Wall Muscles

**Description:** Use the same GenericMuscleCell ([DD002](DD002_Muscle_Model_Architecture.md)) with Boyle & Cohen parameters for vulval muscles.

**Rejected because:**

- Vulval muscles are non-striated; body wall muscles are obliquely striated
- Vulval muscles express distinct channel complement: EGL-19 (L-type Ca) dominates rather than ca_boyle, plus UNC-103 ERG K+ channel (absent in body wall)
- The two-state pattern requires the EGL-19/UNC-103 balance, which does not exist in the [DD002](DD002_Muscle_Model_Architecture.md) GenericMuscleCell
- Calcium-to-force coupling is qualitatively different (vulval opening vs. body bending)

### 5. Model Only HSN Without VC Feedback

**Description:** Simplify the circuit to HSN → vm2 only, omitting VC neurons and uv1 feedback.

**Rejected because:**

- The two-state pattern emerges from the balance of excitation (HSN + VC) and inhibition (uv1)
- VC neurons provide the critical feedback inhibition that terminates active bouts
- HSN-only models produce continuous egg-laying, not the observed bursty pattern
- Zhang et al. 2008 demonstrated the feed-forward/feedback architecture is essential

### 6. Wait for Complete Vulval Muscle Electrophysiology

**Description:** Do not model vulval muscles until direct patch-clamp recordings from vm1/vm2 are available.

**Rejected because:**

- Direct recordings from vulval muscles in vivo are extremely difficult (cells are embedded in tissue)
- Calcium imaging data ([Collins et al. 2016](https://doi.org/10.7554/eLife.21126), [Brewer et al. 2019](https://doi.org/10.1371/journal.pgen.1007896)) provide quantitative constraints
- Genetic perturbation data (egl-19, unc-103, egl-36 alleles) constrain the channel model
- Model predictions can guide future experimental priorities

---

## Quality Criteria

### What Defines a Valid Egg-Laying Model?

1. **Two-State Pattern:** Vulval muscle calcium activity must alternate between inactive (~20 min) and active (~2 min) states. Continuous activity or continuous silence are both failures.

2. **Bout Statistics:** During active states, 3-5 egg-laying events must occur with ~20 s inter-event intervals.

3. **Serotonin Dependence:** Removing HSN serotonin release (simulating tph-1 mutation) must reduce or abolish active states.

4. **ERG Channel Function:** Setting UNC-103 conductance to zero (simulating unc-103 null) must produce hyperactive egg-laying (no or shortened inactive states).

5. **EGL-19 Requirement:** Reducing EGL-19 conductance must reduce Ca2+ transient amplitude and egg-laying frequency.

6. **Feedback Inhibition:** Removing uv1 tyramine release must produce prolonged active states with more eggs per bout.

7. **Backward Compatibility:** Simulations with `egglaying.enabled: false` must produce identical output to the pre-egg-laying baseline. HSN and VC neurons still participate in the general neural circuit ([DD001](DD001_Neural_Circuit_Architecture.md)) but without sex muscle targets.

8. **Locomotion Non-Interference:** Adding the egg-laying circuit must not degrade Tier 3 kinematic metrics by more than 15%.

### Validation Procedure

```bash
# Generate egg-laying-enabled network
cd c302/
python c302_egglaying.py

# Run 1-hour simulation (expect ~3 bouts)
jnml LEMS_c302_EggLaying.xml -nogui -reportFile egglaying_report.txt

# Extract egg-laying temporal pattern
python scripts/measure_egglaying.py \
    LEMS_c302_EggLaying_muscles.dat \
    --metrics bout_interval,eggs_per_bout,active_duration \
    --output egglaying_metrics.csv
# [TO BE CREATED]

# Compare to Collins et al. 2016 experimental data
python scripts/validate_egglaying.py \
    --simulated egglaying_metrics.csv \
    --experimental data/collins2016_egg_laying_stats.csv \
    --tolerance 0.5
# [TO BE CREATED]

# Pharmacological test: exogenous serotonin
python scripts/test_serotonin_response.py \
    --serotonin_concentration 10 \
    --expected sustained_active_state
# [TO BE CREATED]
```

**Success criteria:**

- Inactive state: 10-30 min (mean ~20 min)
- Active state: 1-3 min (mean ~2 min)
- Eggs per bout: 3-5
- Serotonin response: sustained active state
- unc-103 null: hyperactive (inactive state absent or < 5 min)
- egl-1 (no HSN): no active states

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Oogenesis and fertilization:** Oocyte maturation, sperm-oocyte interaction, and events in the spermatheca are not modeled. Eggs appear in the uterus at a fixed rate (~1 per 10 min per gonad arm).

2. **Vulval morphogenesis:** The development of the vulval epithelium (vulA-vulF toroids) is not modeled. The vulval structure is assumed to be fully formed (adult hermaphrodite).

3. **Sex myoblast migration and differentiation:** The postembryonic M lineage that produces the 16 sex muscles is not modeled. Sex muscles are assumed present at simulation start.

4. **Male-specific mating circuit:** The male has a different reproductive circuit (ray neurons, spicule muscles, etc.). This DD covers hermaphrodite egg-laying only.

5. **Egg shell formation:** The chitin/lipid/protein layers of the eggshell are not modeled.

6. **Embryonic development in utero:** Embryos are not simulated. Egg production is modeled as a fixed rate counter.

7. **Food-dependent modulation:** Egg-laying rate varies with food availability. This environmental coupling is future work.

8. **Age-dependent changes:** Egg-laying rate declines with age as sperm are depleted. Reproductive senescence is not modeled.

9. **utse (uterine seam cell) mechanics:** The "hymen" broken by the first egg is not modeled mechanically.

10. **Detailed vulval opening mechanics:** The [DD004](DD004_Mechanical_Cell_Identity.md) SPH model does not include vulval epithelial cells or the mechanical forces of vulval slit opening. Egg-laying is modeled as a circuit-level event, not a mechanical simulation of egg passage.

---

## Context & Background

The egg-laying system is one of the best-characterized neural circuits in *C. elegans*. The hermaphrodite lays approximately 300 eggs over its reproductive lifespan, producing them from two gonad arms at ~1 egg per 10 minutes each. Eggs accumulate in the uterus (10-15 at steady state) and are expelled through the vulva by coordinated contraction of 16 non-striated sex muscles.

The behavioral pattern is remarkably stereotyped: ~20 minutes of inactivity followed by ~2-minute bouts of 3-5 egg-laying events, each separated by ~20 seconds. This two-state pattern was first characterized by Waggoner et al. (1998) and quantified in detail by Collins et al. (2016) using simultaneous calcium imaging of all circuit components.

The circuit architecture is a textbook example of feed-forward excitation with feedback inhibition (Zhang et al. 2008): HSN serotonergic neurons excite both VC cholinergic neurons and vm2 muscles directly; VC4/VC5 provide additional excitation to vm2 but also inhibit HSN; uv1 neuroendocrine cells sense egg passage and release tyramine to inhibit HSN, terminating the active bout.

Serotonin is the critical neuromodulator. HSN neurons release serotonin from their vulval presynaptic region, activating SER-1 (Gaq-coupled) receptors on vm2 muscles. The downstream Gaq → Trio RhoGEF → DAG cascade increases vulval muscle excitability by modulating the balance between EGL-19 (L-type Ca2+, excitatory) and UNC-103 (ERG K+, inhibitory) channels.

The circuit is also the foundation for >145 egg-laying defective (egl) mutants identified by Trent et al. (1983), making it one of the most genetically dissected behaviors in any organism.

---

## Implementation References

### WormAtlas Egg-Laying Apparatus

```
https://www.wormatlas.org/hermaphrodite/egglaying%20apparatus/mainframe.htm
```

Detailed anatomical descriptions with electron micrographs of vulval muscles, HSN synapses, uv1 cells, and sex muscle arrangement.

### Connectome Data ([Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7))

```
https://wormwiring.org/pages/adjacency.html
```

Quantitative adjacency matrices for HSN, VC, and sex muscle synaptic connections.

### Egg-Laying Circuit Connectivity (from [Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7) and [White et al. 1986](https://doi.org/10.1098/rstb.1986.0056))

**Chemical synapses (directed):**

| Source | Target | Neurotransmitter | Weight (EM sections) |
|--------|--------|-----------------|---------------------|
| HSNL | vm2 (all 4) | Serotonin | ~15-20 sections |
| HSNR | vm2 (all 4) | Serotonin | ~15-20 sections |
| HSNL | VC4, VC5 | Serotonin | ~5-10 sections |
| HSNR | VC4, VC5 | Serotonin | ~5-10 sections |
| VC4 | vm2 (all 4) | Acetylcholine | ~10-15 sections |
| VC5 | vm2 (all 4) | Acetylcholine | ~10-15 sections |
| VC4 | HSNL, HSNR | (inhibitory) | ~3-5 sections |
| VC5 | HSNL, HSNR | (inhibitory) | ~3-5 sections |

**Gap junctions (undirected):**

| Cell A | Cell B | Innexin | Estimated g |
|--------|--------|---------|------------|
| HSNL | VC4 | inx-? | ~0.2 nS |
| HSNR | VC5 | inx-? | ~0.2 nS |
| vm1 | vm1 | inx-? | ~1.0 nS |
| vm2 | vm2 | inx-? | ~1.0 nS |
| vm1 | vm2 | inx-? | ~0.5 nS |
| um | vm2 | inx-? | ~0.3 nS |

### Sun & Bhatt 2010 Circuit Model

The first computational model of egg-laying temporal pattern generation (BMC Systems Biology 4:81):

- HSN modeled as a NOR gate (active only when both VC and uv1 are silent)
- VC modeled as "single egg counters" providing short-term inhibition after each egg event
- Successfully reproduces the clustered temporal pattern
- Our model extends this with biophysical (HH) rather than Boolean dynamics

### Vulval Muscle Channel Data

**EGL-19 (L-type Ca2+ channel):**

- Activation: V_half ~ -20 mV, slope ~ 7 mV
- Inactivation: V_half ~ -40 mV, slope ~ 5 mV (slow, tau ~ 100-500 ms)
- Permeation: primarily Ca2+ (P_Ca >> P_Na, P_K)

**UNC-103 (ERG K+ channel):**

- Activation: V_half ~ -30 mV (shifted from mammalian hERG)
- Fast inactivation (C-type): tau ~ 50-100 ms
- Recovery from inactivation: tau ~ 200-500 ms
- ERG channels have characteristic resurgent current on repolarization

**EGL-36 (Shaw K+ channel):**

- Fast-activating K+ channel
- egl-36(gf): shift activation to more negative voltages -> hyperpolarized muscles -> Egl
- egl-36(dn): reduced K+ current -> hyperexcitable muscles -> hyperactive egg-laying

---

## Migration Path

### Incremental Integration Strategy

**Stage 1 (Circuit Only — Isolated):**

- Implement HSN + VC4/VC5 + vm2 circuit without coupling to body physics
- Validate two-state pattern in isolation
- ~10 cells; fast simulation

**Stage 2 (Circuit + Locomotion Coupling):**

- Couple vm1 to body-bend-driven rhythmic excitation from [DD001](DD001_Neural_Circuit_Architecture.md)/DD003 locomotion
- Validate that egg-laying does not degrade locomotion
- Validate that body bend coupling provides the ~10 s rhythmic drive

**Stage 3 (Full Integration):**

- Add uterine muscles, uv1 feedback, gap junction network
- Validate full behavioral statistics
- Add mutant simulations (egl-1, unc-103, egl-36)
- Add pharmacological simulations (exogenous serotonin)

### Backward Compatibility

Models without egg-laying remain valid. The extension is **additive**:

```yaml
# Old config (still works)
egglaying:
  enabled: false

# New config
egglaying:
  enabled: true
  model: "circuit"
```

HSN and VC neurons exist in the [DD001](DD001_Neural_Circuit_Architecture.md) connectome regardless of `egglaying.enabled`. When disabled, they participate in general neural dynamics but have no sex muscle targets. When enabled, the sex muscles are instantiated and connected.

---

## Known Issues and Future Work

### Issue 1: Vulval Muscle Electrophysiology Is Indirect

No direct patch-clamp recordings from vm1/vm2 exist. Channel properties are inferred from:

- Genetic perturbation (egl-19, unc-103, egl-36 alleles)
- Calcium imaging ([Collins et al. 2016](https://doi.org/10.7554/eLife.21126), [Brewer et al. 2019](https://doi.org/10.1371/journal.pgen.1007896))
- Heterologous expression studies

**Future work:** If in vivo vulval muscle recordings become available, recalibrate conductance densities.

### Issue 2: Serotonin Receptor Signaling Is Simplified

The Gaq -> DAG cascade is modeled as phenomenological conductance modulation, not biochemical dynamics. This may miss:

- Temporal dynamics of DAG accumulation/degradation
- Cross-talk between SER-1 and SER-7 pathways
- PKC-mediated phosphorylation of specific channels

**Future work:** Phase 5 intracellular signaling (DD to be written).

### Issue 3: Egg Counter Is Abstract

Eggs are not physically modeled as objects. The "egg in uterus" is a counter, not a mechanical entity. Egg passage through the vulva is an event, not a simulated mechanical process.

**Future work:** [DD004](DD004_Mechanical_Cell_Identity.md) mechanical cell identity could tag egg particles in Sibernetic for physical egg passage simulation.

### Issue 4: Missing Modulatory Inputs

Several known modulatory inputs are not included in Phase 3:

- PLM mechanosensory inhibition of HSN (posterior touch suppresses egg-laying)
- Food-dependent modulation (AWC, ASI chemosensory pathways)
- DVA/PVT stretch-sensitive modulation
- Full neuropeptide landscape (26 GPCRs mapped by Ravi et al. 2020)

**Future work:** Add sensory modulation as inputs from other DD subsystems.

---

## References

1. **Waggoner LE, Zhou GT, Schafer RW, Bhatt R (1998).** "Control of alternative behavioral states by serotonin in *Caenorhabditis elegans*." *Neuron* 21:203-214.
   *Two-state model of egg-laying behavior.*

2. **Zhang M, Chung SH, Bhatt R, et al. (2008).** "A self-regulating feed-forward circuit controlling *C. elegans* egg-laying behavior." *Curr Biol* 18:1445-1455.
   *Feed-forward excitation + feedback inhibition circuit motif.*

3. **Collins KM, Koelle MR (2013).** "Postsynaptic ERG potassium channels limit muscle excitability to allow distinct egg-laying behavior states." *J Neurosci* 33:761-775.
   *UNC-103 ERG channel in vm2; two-state mechanism.*

4. **Collins KM, Bode A, Bhatt R, et al. (2016).** "Activity of the *C. elegans* egg-laying behavior circuit is controlled by competing activation and feedback inhibition." *eLife* 5:e21126.
   *Comprehensive calcium imaging of all circuit components.*

5. **Brewer JC, Olson AC, Collins KM, Bhatt R (2019).** "Serotonin and neuropeptides are both released by the HSN command neuron to initiate *C. elegans* egg laying." *PLoS Genet* 15:e1007896.
   *NLP-3 co-transmission from HSN.*

6. **Kopchock RJ, Ravi B, Bode A, Collins KM (2021).** "The sex-specific VC neurons are mechanically activated motor neurons that facilitate serotonin-induced egg laying in *C. elegans*." *J Neurosci* 41:3635-3650.
   *VC mechanosensory function.*

7. **Trent C, Tsuing N, Bhatt R (1983).** "Egg-laying defective mutants of the nematode *Caenorhabditis elegans*." *Genetics* 104:619-647.
   *145 egl mutants, 4 pharmacological classes.*

8. **Cook SJ et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *Updated connectome including egg-laying circuit synapses.*

9. **Schafer WR (2006).** "Egg-laying." *WormBook* (doi: 10.1895/wormbook.1.38.1).
   *Comprehensive review.*

10. **Sun Q, Bhatt R (2010).** "Bhatt lab computational model of egg-laying circuit temporal pattern generation." *BMC Systems Biology* 4:81.
    *First circuit-level computational model; HSN as NOR gate.*

11. **Collins KM, Bhatt R (2022).** "Serotonin signals through postsynaptic Gaq, Trio RhoGEF, and diacylglycerol to promote *C. elegans* egg-laying circuit activity and behavior." *Genetics* 221:iyac084.
    *Gaq -> Trio -> DAG signaling cascade.*

12. **Ravi B, Singhal N, Bhatt R (2020).** "Expression, function, and pharmacological analysis of all 26 neurotransmitter GPCRs as individual transgenes in *C. elegans*." *J Neurosci* 40:7475-7488.
    *Comprehensive GPCR mapping in egg-laying circuit.*

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| HSN neuron voltage/calcium | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (c302 neural circuit) | `V_HSN`, `ca_HSN` | NeuroML state variables | mV, mol/cm³ |
| VC neuron voltage/calcium | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (c302 neural circuit) | `V_VC4`, `V_VC5` | NeuroML state variables | mV, mol/cm³ |
| Body bend phase (locomotion coupling) | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD003](DD003_Body_Physics_Architecture.md) | Periodic motor neuron output on ventral cord | NeuroML coupling | nA (current injection to vm1) |
| CeNGEN expression (HSN, VC classes) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Per-class conductance densities | NeuroML `<channelDensity>` | S/cm² |
| Neuropeptide modulation (if [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) enabled) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | NLP-3 release from HSN; NLP-7/FLP-11 from uv1 | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) `<peptideRelease>` components | mol/cm³ |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Vulval muscle [Ca2+] per cell | [DD014](DD014_Dynamic_Visualization_Architecture.md) (visualization) | Per-muscle calcium time series | OME-Zarr: `egglaying/muscle_activation/`, shape (n_timesteps, 16) | dimensionless [0, 1] |
| Circuit state (active/inactive) | [DD014](DD014_Dynamic_Visualization_Architecture.md) (visualization) | Binary state time series | OME-Zarr: `egglaying/circuit_state/`, shape (n_timesteps, 1) | binary |
| Egg-laying event timestamps | [DD010](DD010_Validation_Framework.md) (validation) | Event log | OME-Zarr: `egglaying/egg_events/` | ms |
| Egg-laying behavioral metrics | [DD010](DD010_Validation_Framework.md) (Tier 3 validation) | bout_interval, eggs_per_bout, active_duration | CSV output from measure_egglaying.py | min, count, min |
| Sex muscle particle forces (Option B, future) | [DD003](DD003_Body_Physics_Architecture.md) / [DD004](DD004_Mechanical_Cell_Identity.md) | Per-particle force for vulval/uterine muscles | Same format as [DD002](DD002_Muscle_Model_Architecture.md) muscle activation | dimensionless [0, 1] |

### Repository & Packaging

- **Primary repository:** `openworm/c302` (same package, new module)
- **Docker stage:** `neural` (same as [DD001](DD001_Neural_Circuit_Architecture.md) — sex muscles use NeuroML/LEMS)
- **`versions.lock` key:** `c302`
- **Build dependencies:** pyNeuroML (pip), numpy (pip)
- **No additional Docker changes** for Phase 3 (circuit-only model)

**Repository structure:**

```
c302/
├── c302_egglaying.py              # NEW: Egg-laying network generation
├── egglaying/
│   ├── VulvalMuscle1Cell.cell.nml # vm1 HH model
│   ├── VulvalMuscle2Cell.cell.nml # vm2 HH model (with nAChR, SER-1)
│   ├── UterineMuscleCell.cell.nml # um model (gap-junction-coupled)
│   ├── UV1Cell.cell.nml           # uv1 neuroendocrine cell
│   ├── SerotoninSynapse.synapse.nml  # 5-HT -> SER-1 -> conductance modulation
│   ├── TyramineSynapse.synapse.nml   # Tyramine -> LGC-55 Cl- channel
│   └── egglaying_coupling.py     # Coupling to locomotion body bends
```

### Configuration

**`openworm.yml` section:**

```yaml
egglaying:
  enabled: false                    # Off by default until validated
  model: "circuit"                  # Only option for Phase 3
  serotonin_modulation: true       # Enable serotonergic conductance modulation on vm2
  uv1_feedback: true               # Enable tyraminergic feedback from uv1
  egg_production_rate: 0.1         # eggs per minute per gonad arm
  uterus_capacity: 15             # max eggs in uterus
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `egglaying.enabled` | `false` | `true`/`false` | Enable egg-laying subsystem |
| `egglaying.model` | `"circuit"` | `"circuit"` | Egg-laying model type (only one for Phase 3) |
| `egglaying.serotonin_modulation` | `true` | `true`/`false` | Enable serotonin -> Gaq -> conductance modulation on vm2 |
| `egglaying.uv1_feedback` | `true` | `true`/`false` | Enable uv1 tyraminergic feedback inhibition |
| `egglaying.egg_production_rate` | `0.1` | `0.05`-`0.2` eggs/min/arm | Egg production rate per gonad arm |
| `egglaying.uterus_capacity` | `15` | `5`-`30` | Maximum eggs held in uterus before mechanical signal |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)

# Step 1: Verify backward compatibility
docker compose run quick-test  # with egglaying.enabled: false
# Must produce identical output to pre-egg-laying baseline

# Step 2: Verify egg-laying-enabled simulation
docker compose run quick-test  # with egglaying.enabled: true
# Verify: simulation completes without error
# Verify: vulval muscle calcium output file exists
# Verify: calcium values show two-state pattern (not flat, not continuous)
# Verify: body still moves (locomotion not destroyed)

# Full validation (nightly, not per-PR — 1 hour sim time)
docker compose run simulation -- \
  python scripts/measure_egglaying.py \
  --duration 3600000 \
  --expected_bout_interval 20 \
  --expected_eggs_per_bout 4 \
  --tolerance_minutes 10
# Check: bout interval = 20 +/- 10 min
# Check: eggs per bout = 3-5
# Check: active state duration ~2 min
# Check: >=3 bouts observed
```

**Per-PR checklist:**

- [ ] `jnml -validate` passes for all egg-laying NeuroML/LEMS files
- [ ] `quick-test` passes with `egglaying.enabled: false` (backward compatibility)
- [ ] `quick-test` passes with `egglaying.enabled: true` (simulation completes)
- [ ] Vulval muscle calcium output shows two-state pattern
- [ ] Body locomotion kinematics within +/-15% of baseline
- [ ] No NaN values in any output variable

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `egglaying/muscle_activation/` (n_timesteps, 16) | Sex muscle activation heatmap | Warm colormap: 0.0 (blue) → 1.0 (red); 16 rows (4 vm1 + 4 vm2 + 4 um1 + 4 um2) |
| `egglaying/circuit_state/` (n_timesteps, 1) | Active/inactive state timeline | Binary: blue (inactive) / red (active) |
| `egglaying/egg_events/` | Egg-laying event markers | Yellow pulse markers at each event timestamp |
| `egglaying/hsn_calcium/` (n_timesteps, 2) | HSN neuron calcium traces | Standard calcium colormap; sustained bursts during active state |

### Compute Budget

| Resource | Without Egg-Laying | With Egg-Laying | Impact |
|----------|-------------------|-----------------|--------|
| Additional cells | 0 | 28 (2 HSN + 6 VC + 16 muscles + 4 uv1) | ~9% more cells (28/302) |
| State variables | ~1,800 | ~2,100 (+300 for sex muscles and uv1) | ~17% increase |
| Memory | ~500 MB | ~550 MB | Negligible |
| Simulation time (15 ms) | ~10 min | ~11 min | ~10% increase |
| **Validation sim (1 hr)** | N/A | ~40 hours wall time | **Nightly build only** |

The egg-laying circuit adds minimal computational cost to short simulations. However, validation requires ~1 hour of simulated time (3+ bouts at ~20 min intervals), which is expensive. Run validation as a nightly build, not per-PR.

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|----------------------------|
| Neural circuit (HSN, VC connectivity) | [DD001](DD001_Neural_Circuit_Architecture.md) | If HSN/VC synaptic weights change, egg-laying drive strength changes |
| CeNGEN differentiation (HSN, VC channel densities) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | If HSN/VC conductances change, circuit dynamics change |
| Body bend locomotion (vm1 rhythmic drive) | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD003](DD003_Body_Physics_Architecture.md) | If body bend period changes, rhythmic vm1 excitation timing changes |
| Neuropeptide signaling (NLP-3, NLP-7, FLP-11) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | If peptide dynamics change, HSN co-transmission and uv1 feedback change |
| Cell identity (future vulval muscle particles) | [DD004](DD004_Mechanical_Cell_Identity.md) | If vulval muscle cell_ids change, wrong particles contract |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|----------------------------|
| Validation (egg-laying behavioral metrics) | [DD010](DD010_Validation_Framework.md) | Egg-laying pattern is a Tier 3 validation target |
| Body physics (future, if vulval muscles are SPH particles) | [DD003](DD003_Body_Physics_Architecture.md) / [DD004](DD004_Mechanical_Cell_Identity.md) | If vm activation format changes, particle forces change |
| Visualization (egg-laying layers) | [DD014](DD014_Dynamic_Visualization_Architecture.md) | If output format changes, viewer layers break |

---

**Approved by:** Pending (Phase 3)
**Implementation Status:** Proposed
**Next Actions:**

1. Extract HSN and VC channel densities from CeNGEN ([DD005](DD005_Cell_Type_Differentiation_Strategy.md))
2. Implement EGL-19 L-type Ca2+ channel model in NeuroML/LEMS
3. Implement UNC-103 ERG K+ channel model in NeuroML/LEMS
4. Create vm2 cell template with EGL-19/UNC-103 balance
5. Implement serotonergic synapse (5-HT -> SER-1 -> conductance modulation)
6. Validate two-state pattern in isolated circuit
7. Couple to locomotion body bend drive
8. Full behavioral validation against [Collins et al. 2016](https://doi.org/10.7554/eLife.21126)
