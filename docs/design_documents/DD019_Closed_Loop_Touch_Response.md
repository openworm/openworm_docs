# DD019: Closed-Loop Touch Response and Tap Withdrawal Behavior

**Status:** Proposed (Phase 2-3)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-16  
**Supersedes:** None  
**Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD003](DD003_Body_Physics_Architecture.md) (Body Physics), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation), [DD010](DD010_Validation_Framework.md) (Validation Framework), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Hybrid Mechanistic-ML Framework)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | Closed-loop mechanosensory transduction model: Sibernetic cuticle strain → MEC-4 channel currents on touch neurons (ALM, AVM, PLM, PVD) → tap withdrawal circuit → motor reversal → backward locomotion |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: tap stimulus → reversal onset <1 s, backward locomotion ≥1 body length, return to forward crawling within 10 s |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) (mechanosensory model, circuit) + [`openworm/sibernetic`](https://github.com/openworm/sibernetic) (strain readout, tap stimulus, bidirectional coupling) |
| **Config toggle** | `sensory.mechanotransduction: true` / `behavior.tap_withdrawal: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` (closed-loop runs, reversal occurs), `docker compose run validate` (Tier 3 behavioral) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `sensory/strain/` layer — cuticle strain heatmap; `neural/` layer — touch neuron + command interneuron activation; `body/` layer — body trajectory with reversal event markers |
| **CI gate** | Tier 3 behavioral validation blocks merge; closed-loop stability (no NaN/divergence over 30 s) blocks PR |

---

## TL;DR

Close the sensorimotor loop by reading cuticle mechanical strain from Sibernetic SPH particles, transducing it through a biophysical MEC-4/MEC-10 channel model on touch receptor neurons (ALM, AVM, PLM, PVD), and coupling this into the existing c302 tap withdrawal circuit — producing emergent backward locomotion in response to a simulated tap. This is the first behavior that requires **bidirectional coupling**: body physics → sensory neurons (new) AND neurons → muscles → body physics (existing). Success: a forward-crawling worm reverses direction within 1 second of a tap stimulus, travels ≥1 body length backward, and resumes forward crawling within 10 seconds.

---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Reversal onset latency | Tap stimulus → first backward body bend <1 s (Chalfie et al. 1985: 300-800 ms) | Tier 3 (blocking) |
| **Primary:** Reversal distance | ≥1 body length backward travel | Tier 3 (blocking) |
| **Primary:** Recovery to forward | Resume forward crawling within 10 s of tap | Tier 3 (blocking) |
| **Secondary:** Anterior vs. posterior discrimination | Anterior touch (ALM/AVM activated) → backward; posterior touch (PLM activated) → forward acceleration | Tier 3 (blocking) |
| **Secondary:** Closed-loop stability | 30 s bidirectional simulation without NaN, divergence, or oscillatory instability | Quick-test (blocking per-PR) |
| **Tertiary:** Touch neuron calcium dynamics | MEC-4 channel current onset <50 ms from strain application, decay <500 ms | Tier 1 (non-blocking) |

**Before:** Open-loop simulation — sensory neurons receive artificial current injections or no input at all. The c302_TapWithdrawal circuit exists but "does not produce the correct behavior" (per code header). No body→sensory feedback path.

**After:** Closed-loop simulation — mechanical contact on the cuticle propagates through the mechanosensory transduction chain to produce emergent tap withdrawal behavior with no manual current injection.

---

## Deliverables

| Artifact | Path (relative to repo) | Format | Example |
|----------|------------------------|--------|---------|
| MEC-4 mechanosensory channel model | `openworm/c302` — `channel_models/mec4_chan.channel.nml` | NeuroML 2 XML | DEG/ENaC mechanically-gated cation channel |
| Touch receptor neuron templates | `openworm/c302` — `cells/ALMCell.cell.nml`, `AVMCell.cell.nml`, `PLMCell.cell.nml`, `PVDCell.cell.nml` | NeuroML 2 XML | HH cell with MEC-4 channel + standard channels |
| Updated tap withdrawal circuit | `openworm/c302` — `c302/c302_TapWithdrawal.py` | Python → NeuroML 2 XML | Updated circuit with mechanosensory input |
| Cuticle strain readout module | `openworm/sibernetic` — `coupling/strain_readout.py` | Python | Reads SPH particle positions → computes local strain per body segment |
| Bidirectional coupling script | `openworm/sibernetic` — `sibernetic_c302_closedloop.py` | Python | Extends `sibernetic_c302.py` with body→sensory feedback path |
| Tap stimulus generator | `openworm/sibernetic` — `stimuli/tap_stimulus.py` | Python | Delivers boundary particle displacement at configurable body position |
| Sensory strain time series (viewer) | OME-Zarr: `sensory/strain/`, shape (n_timesteps, n_segments) | OME-Zarr | Per-segment cuticle strain over time |
| Reversal event annotations (viewer) | OME-Zarr: `behavior/events/`, shape (n_events, 3) | OME-Zarr | (onset_time, offset_time, type) per reversal event |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository (mechanosensory model)** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Repository (coupling + stimulus)** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) |
| **Issue label** | `dd019` |
| **Milestone** | Closed-Loop Touch Response |
| **Branch convention** | `dd019/description` (e.g., `dd019/mec4-channel-model`, `dd019/strain-readout`) |
| **Example PR title** | `DD019: MEC-4 mechanosensory channel model for touch receptor neurons` |
| **Related GitHub issues** | [openworm/openworm#223](https://github.com/openworm/openworm/issues/223), [#224](https://github.com/openworm/openworm/issues/224), [#225](https://github.com/openworm/openworm/issues/225), [#227](https://github.com/openworm/openworm/issues/227) |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, NEURON 8.2.6, Sibernetic (with OpenCL or Taichi backend)

### Step-by-step

```bash
# Step 1: Validate MEC-4 channel model
jnml -validate c302/channel_models/mec4_chan.channel.nml

# Step 2: Generate tap withdrawal network with mechanosensory input
cd c302/
python c302/c302_TapWithdrawal.py --mechanosensory
# Expected output: LEMS_c302_C1_TapWithdrawal.xml with MEC-4 channels on touch neurons

# Step 3: Validate NeuroML syntax
jnml -validate LEMS_c302_C1_TapWithdrawal.xml

# Step 4: Unit test — MEC-4 channel responds to strain
python scripts/test_mec4_channel.py
# [TO BE CREATED] — GitHub issue: openworm/c302#TBD
# Expected: channel opens for strain > threshold, current < 100 pA, correct reversal potential

# Step 5: Unit test — strain readout from Sibernetic particles
python scripts/test_strain_readout.py
# [TO BE CREATED] — GitHub issue: openworm/sibernetic#TBD
# Expected: known particle displacement → correct strain value at touch neuron position

# Step 6: Closed-loop quick test (must pass before PR)
docker compose run quick-test --config tap_withdrawal
# Green light: simulation runs 10 s without NaN or divergence
# Green light: at least one reversal event detected after tap stimulus
# Green light: body trajectory file (*.wcon) exists

# Step 7: Full behavioral validation (must pass before merge)
docker compose run validate --config tap_withdrawal
# Green light: reversal onset < 1 s after tap
# Green light: reversal distance ≥ 1 body length
# Green light: return to forward within 10 s
# Green light: anterior touch → backward, posterior touch → forward (direction discrimination)
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `c302/scripts/test_mec4_channel.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `sibernetic/scripts/test_strain_readout.py` | `[TO BE CREATED]` | openworm/sibernetic#TBD |
| `sibernetic/coupling/strain_readout.py` | `[TO BE CREATED]` | openworm/sibernetic#TBD |
| `sibernetic/sibernetic_c302_closedloop.py` | `[TO BE CREATED]` | openworm/sibernetic#TBD |
| `sibernetic/stimuli/tap_stimulus.py` | `[TO BE CREATED]` | openworm/sibernetic#TBD |
| `c302/scripts/validate_tap_withdrawal.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `c302/scripts/detect_reversal_events.py` | `[TO BE CREATED]` | openworm/c302#TBD |

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layers:** Three new overlays for closed-loop touch response.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer 1: Cuticle strain** | `sensory/strain/` — body segments colored by local strain magnitude. Blue (no strain) → red (high strain). Tap stimulus should produce a transient red flash at the contact point. |
| **Layer 2: Touch circuit activity** | `neural/` layer with touch neurons (ALM, AVM, PLM, PVD) and command interneurons (AVA, AVB) highlighted. During tap: touch neurons depolarize (warm) → AVA activates (warm), AVB inhibited (cool) → motor neurons switch. |
| **Layer 3: Reversal events** | `behavior/events/` — body trajectory with event markers. Forward crawling = green path, reversal = red path. Tap onset marked with vertical line on timeline. |
| **Combined view** | Side-by-side: (left) SPH particle view with strain heatmap, (center) circuit diagram with live activation, (right) body trajectory with event timeline. |

---

## Technical Approach

### Overview: Closing the Sensorimotor Loop

The tap withdrawal behavior requires a complete causal loop:

```
Environment → Cuticle deformation → Cuticle strain (SPH)
    → Mechanosensory transduction (MEC-4 channels)
    → Touch receptor neuron depolarization (ALM, AVM, PLM, PVD)
    → Command interneuron decision (AVA backward / AVB forward)
    → Motor neuron pattern switch (DA/VA backward wave vs. DB/VB forward wave)
    → Muscle activation ([DD002](DD002_Muscle_Model_Architecture.md) calcium-force)
    → Body deformation ([DD003](DD003_Body_Physics_Architecture.md) SPH)
    → Movement in environment → (loop)
```

Currently, the **forward path** (neural → muscle → body) is implemented via `sibernetic_c302.py`. [DD019](DD019_Closed_Loop_Touch_Response.md) adds the **reverse path** (body → sensory) and connects them into a single closed loop.

### Component 1: Cuticle Strain Readout from SPH Particles

**Problem:** Sibernetic represents the body wall as ~40,000 elastic SPH particles. When the cuticle is deformed (e.g., by a tap stimulus or contact with a boundary object), particles displace from their rest positions. We need to compute a local strain signal at each touch receptor neuron's anatomical position.

**Approach:** Compute strain as the local deformation of elastic particles relative to their rest configuration, averaged over a receptive field centered at each touch neuron's known anatomical position.

**Touch neuron positions (White et al. 1986, WormAtlas):**

| Neuron | Position (% body length from anterior) | Receptive Field | Touch Modality |
|--------|---------------------------------------|-----------------|----------------|
| ALML | ~30% | Anterior body (10-50%) | Gentle (light) touch |
| ALMR | ~30% | Anterior body (10-50%) | Gentle touch |
| AVM | ~40% | Anterior-mid body (20-55%) | Gentle touch |
| PLML | ~75% | Posterior body (50-90%) | Gentle touch |
| PLMR | ~75% | Posterior body (50-90%) | Gentle touch |
| PVD | ~65% | Full body (overlapping) | Harsh (nociceptive) touch |

**Strain computation:**

```python
# coupling/strain_readout.py

import numpy as np

def compute_local_strain(particle_positions, rest_positions, neuron_position,
                         receptive_field_radius):
    """
    Compute local cuticle strain at a touch neuron's anatomical position.

    Parameters
    ----------
    particle_positions : ndarray, shape (n_elastic, 3)
        Current positions of elastic (body wall) particles.
    rest_positions : ndarray, shape (n_elastic, 3)
        Rest (equilibrium) positions of elastic particles.
    neuron_position : float
        Fractional position along body axis (0 = anterior, 1 = posterior).
    receptive_field_radius : float
        Radius of the neuron's receptive field in particle units.

    Returns
    -------
    strain : float
        Local strain magnitude (dimensionless, 0 = no deformation).
    """
    # Map neuron position to body-axis coordinate
    body_length = np.max(rest_positions[:, 0]) - np.min(rest_positions[:, 0])
    neuron_x = np.min(rest_positions[:, 0]) + neuron_position * body_length

    # Select particles within receptive field
    distances = np.abs(rest_positions[:, 0] - neuron_x)
    mask = distances < receptive_field_radius

    if np.sum(mask) < 10:
        return 0.0  # Not enough particles — no signal

    # Compute local displacement
    displacements = particle_positions[mask] - rest_positions[mask]

    # Strain = RMS displacement magnitude normalized by particle spacing
    particle_spacing = body_length / np.cbrt(len(rest_positions))
    strain = np.sqrt(np.mean(np.sum(displacements**2, axis=1))) / particle_spacing

    return strain
```

**Temporal filtering:** Raw SPH positions are noisy at the particle level. Apply a 1st-order low-pass filter (tau = 5 ms, matching MEC channel kinetics) to produce a smooth strain signal before feeding to the channel model:

```
d(strain_filtered)/dt = (strain_raw - strain_filtered) / tau_filter
```

### Component 2: MEC-4/MEC-10 Mechanosensory Channel Model

**Biology:** The six gentle-touch receptor neurons (ALML/R, AVM, PLML/R, PVD for harsh touch) express the MEC-4/MEC-10 DEG/ENaC mechanically-gated ion channel complex. This channel opens in response to mechanical deformation of the cuticle transmitted through a specialized extracellular matrix (the "mantle") attached via MEC-1/MEC-5/MEC-9 linker proteins.

The MEC-4 channel is a non-selective cation channel with these electrophysiological properties (O'Hagan et al. 2005, Goodman et al. 2002):

| Property | Value | Source |
|----------|-------|--------|
| Reversal potential (E_MEC) | +10 mV | Non-selective cation (Na⁺/K⁺/Ca²⁺) |
| Maximum conductance | 100-150 pS per channel complex | O'Hagan et al. 2005 |
| Total conductance per cell | ~20 nS (estimated, ~130-200 channels) | Goodman lab |
| Activation threshold | ~1-2 µm cuticle indentation | O'Hagan et al. 2005 |
| Activation time constant | ~1-5 ms | Rapid onset |
| Inactivation time constant | ~50-200 ms | Adapts during sustained touch |
| Deactivation time constant | ~5-10 ms | Rapid offset after stimulus removal |

**Channel model (NeuroML):**

We model MEC-4 as a mechanically-gated conductance with activation and inactivation gates:

```
I_MEC = g_MEC * m(strain) * h(strain, t) * (V - E_MEC)
```

Where:

- `m(strain)` = activation gate — opens with cuticle strain (Boltzmann sigmoid)
- `h(strain, t)` = inactivation gate — adapts during sustained strain (slow exponential decay)
- `E_MEC` = +10 mV (cation reversal potential)
- `g_MEC` = 20 nS (total mechanosensory conductance per cell)

**Activation gate (strain-dependent, effectively instantaneous):**

```
m_inf(strain) = 1 / (1 + exp(-(strain - strain_half) / k_strain))
```

- `strain_half` = 0.05 (dimensionless strain at half-activation, ~1-2 µm indentation)
- `k_strain` = 0.015 (sensitivity slope)
- `tau_m` = 2 ms (fast activation)

**Inactivation gate (time-dependent adaptation):**

```
h_inf(strain) = 1 / (1 + exp((strain - strain_half_h) / k_strain_h))
dh/dt = (h_inf - h) / tau_h
```

- `strain_half_h` = 0.08 (adapts at stronger sustained strain)
- `k_strain_h` = 0.02
- `tau_h` = 100 ms (slow inactivation → adaptation to sustained touch)

This produces the experimentally observed response: rapid onset current that adapts over ~100-200 ms during sustained touch, matching O'Hagan et al. 2005 recordings from ALM.

**NeuroML implementation:**

```xml
<!-- channel_models/mec4_chan.channel.nml -->
<neuroml xmlns="http://www.neuroml.org/schema/neuroml2">

  <ionChannelHH id="mec4_chan" conductance="20nS" species="non_specific">
    <notes>
      MEC-4/MEC-10 DEG/ENaC mechanosensory channel.
      Mechanically gated by cuticle strain.
      Source: O'Hagan et al. 2005, Goodman et al. 2002.
      Activation: strain-dependent Boltzmann.
      Inactivation: time-dependent adaptation.
    </notes>

    <gateHHrates id="m" instances="1">
      <!-- Activation depends on strain exposure variable, not voltage -->
      <!-- Uses strain-dependent alpha/beta or tabulated rates -->
      <!-- Strain exposure mapped from Sibernetic via coupling script -->
    </gateHHrates>

    <gateHHrates id="h" instances="1">
      <!-- Inactivation: slow adaptation (~100 ms tau) -->
    </gateHHrates>

  </ionChannelHH>

</neuroml>
```

**Implementation note:** Standard NeuroML channels are voltage-gated. To make a strain-gated channel, we use NeuroML's `<exposure>` mechanism to inject the strain signal as an external variable. The coupling script (`sibernetic_c302_closedloop.py`) computes strain and injects it via NEURON's external variable interface at each coupling timestep. If NeuroML's exposure mechanism is insufficient, implement as a LEMS ComponentType extension:

```xml
<ComponentType name="MEC4Channel" extends="baseIonChannel">
  <Exposure name="strain" dimension="none"/>
  <!-- Strain drives activation gate instead of voltage -->
</ComponentType>
```

### Component 3: Touch Receptor Neuron Cell Templates

Each touch receptor neuron has the standard [DD001](DD001_Neural_Circuit_Architecture.md) channels (leak, K_slow, K_fast, Ca_boyle) PLUS the MEC-4 mechanosensory channel:

```python
# c302/cells/ALMCell.cell.nml (pseudocode)
cell = GenericCell.copy()
cell.id = "ALMCell"
cell.add_channel("mec4_chan", g=20e-9)  # 20 nS mechanosensory
cell.add_exposure("strain", source="sibernetic_strain_readout")
# Standard channels remain at [DD001](DD001_Neural_Circuit_Architecture.md)/DD005 defaults
```

If [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (cell-type differentiation) is enabled, the standard channel densities come from CeNGEN expression for ALM/AVM/PLM/PVD. The MEC-4 channel is additive on top.

### Component 4: Tap Withdrawal Neural Circuit

The existing `c302_TapWithdrawal.py` defines 16 interneurons forming the tap withdrawal circuit. [DD019](DD019_Closed_Loop_Touch_Response.md) integrates mechanosensory input into this existing circuit rather than replacing it.

**Circuit architecture (Chalfie et al. 1985, Wicks et al. 1996):**

```
GENTLE ANTERIOR TOUCH:
  ALM, AVM → (excitatory) → AVD → (excitatory) → AVA → backward command
         → (excitatory) → PVC → (inhibitory on AVB) → suppresses forward

GENTLE POSTERIOR TOUCH:
  PLM → (excitatory) → PVC → (excitatory) → AVB → forward command
      → (inhibitory) → AVD → (suppresses AVA) → suppresses backward

HARSH TOUCH:
  PVD → (excitatory) → AVA → backward command (direct, fast)
      → (excitatory) → PVC → modulates forward/backward balance
```

**Command interneuron output → motor pattern switching:**

The key behavioral switch is controlled by the relative activity of AVA (backward) vs. AVB (forward):

| Command Interneuron | Active State | Motor Pattern | Motor Neurons Driven |
|---------------------|-------------|---------------|---------------------|
| **AVB** (default high) | Forward crawling | Anterograde wave | DB, VB (B-class) |
| **AVA** (activated by touch) | Backward crawling | Retrograde wave | DA, VA (A-class) |

**Motor pattern switching mechanism (per issue #227):**

Rather than sinusoidal input to motor neurons (current approach in c302_TapWithdrawal.py), the motor pattern emerges from the relative activation of A-class vs. B-class motor neurons by command interneurons:

```python
# Motor neuron activation based on command interneuron calcium
# (replaces hardcoded sinusoidal input in current c302_TapWithdrawal.py)

# Forward mode (AVB active, AVA quiet):
#   DB/VB motor neurons receive excitatory drive from AVB
#   DA/VA motor neurons are quiescent
#   → anterograde (head-to-tail) muscle wave → forward locomotion

# Backward mode (AVA active, AVB quiet):
#   DA/VA motor neurons receive excitatory drive from AVA
#   DB/VB motor neurons are quiescent
#   → retrograde (tail-to-head) muscle wave → backward locomotion
```

**Updates to `c302_TapWithdrawal.py`:**

1. **Remove** artificial sinusoidal current injections to VB/DB motor neurons
2. **Add** MEC-4 channel to touch receptor neurons (ALM, AVM, PLM, PVD)
3. **Add** strain input exposure to touch neurons (fed from Sibernetic)
4. **Preserve** existing connection polarity overrides (`conn_polarity_override`) and gap junction weight overrides (`conn_number_override`) from previous circuit tuning work (issues #224, #225)
5. **Add** proprioceptive coupling between adjacent body segments for wave propagation (B-class motor neurons have stretch receptor properties — Wen et al. 2012)

### Component 5: Bidirectional Coupling Script

The closed-loop coupling extends the existing `sibernetic_c302.py` (which handles neural→body) with the new body→sensory path:

```python
# sibernetic_c302_closedloop.py

import numpy as np
from strain_readout import compute_local_strain

# Touch neuron registry
TOUCH_NEURONS = {
    'ALML': {'position': 0.30, 'rf_radius': 40.0, 'modality': 'gentle'},
    'ALMR': {'position': 0.30, 'rf_radius': 40.0, 'modality': 'gentle'},
    'AVM':  {'position': 0.40, 'rf_radius': 35.0, 'modality': 'gentle'},
    'PLML': {'position': 0.75, 'rf_radius': 40.0, 'modality': 'gentle'},
    'PLMR': {'position': 0.75, 'rf_radius': 40.0, 'modality': 'gentle'},
    'PVDL': {'position': 0.65, 'rf_radius': 80.0, 'modality': 'harsh'},
    'PVDR': {'position': 0.65, 'rf_radius': 80.0, 'modality': 'harsh'},
}

class ClosedLoopCoupling:
    """
    Bidirectional coupling between c302 (neural) and Sibernetic (body).

    Forward path (existing): muscle calcium → activation → SPH forces
    Reverse path (new): SPH particle strain → MEC-4 current on touch neurons
    """

    def __init__(self, c302_sim, sibernetic_sim, config):
        self.neural = c302_sim
        self.body = sibernetic_sim
        self.dt_coupling = config['coupling']['timestep']  # 0.005 ms
        self.rest_positions = sibernetic_sim.get_elastic_particle_positions()  # t=0
        self.strain_filters = {n: 0.0 for n in TOUCH_NEURONS}
        self.tau_filter = 5.0  # ms, low-pass filter time constant

    def step(self):
        """One bidirectional coupling step."""

        # === FORWARD PATH (existing) ===
        # Read muscle calcium from c302
        muscle_ca = self.neural.get_muscle_calcium()
        # Convert to activation [0, 1]
        activation = np.minimum(1.0, muscle_ca / 4e-7)
        # Write to Sibernetic
        self.body.set_muscle_activation(activation)

        # === REVERSE PATH (new: [DD019](DD019_Closed_Loop_Touch_Response.md)) ===
        # Read current elastic particle positions from Sibernetic
        current_positions = self.body.get_elastic_particle_positions()

        # Compute strain at each touch neuron
        for neuron_name, props in TOUCH_NEURONS.items():
            raw_strain = compute_local_strain(
                current_positions, self.rest_positions,
                props['position'], props['rf_radius']
            )
            # Low-pass filter
            alpha = self.dt_coupling / (self.tau_filter + self.dt_coupling)
            self.strain_filters[neuron_name] += alpha * (
                raw_strain - self.strain_filters[neuron_name]
            )
            # Inject strain as exposure variable on MEC-4 channel
            self.neural.set_strain_exposure(
                neuron_name, self.strain_filters[neuron_name]
            )

        # Advance both simulators by dt_coupling
        self.neural.advance(self.dt_coupling)
        self.body.advance(self.dt_coupling)
```

### Component 6: Tap Stimulus Model

A tap stimulus is a brief, spatially broad mechanical perturbation of the agar plate surface, transmitted through the plate to the worm's body. In the simulation:

```python
# stimuli/tap_stimulus.py

class TapStimulus:
    """
    Delivers a mechanical tap to the simulated worm.

    A tap is modeled as a transient displacement of boundary particles
    (the agar surface) beneath the worm, simulating plate vibration.
    """

    def __init__(self, config):
        self.onset_time = config['stimulus']['onset']      # s
        self.duration = config['stimulus']['duration']      # 0.01 s (10 ms)
        self.amplitude = config['stimulus']['amplitude']    # µm displacement
        self.position = config['stimulus']['position']      # 'anterior', 'posterior', 'whole'

    def get_boundary_displacement(self, t, boundary_positions):
        """
        Returns displacement vector for boundary particles at time t.
        """
        if t < self.onset_time or t > self.onset_time + self.duration:
            return np.zeros_like(boundary_positions)

        # Half-sine pulse (smooth onset/offset)
        phase = (t - self.onset_time) / self.duration * np.pi
        magnitude = self.amplitude * np.sin(phase)

        # Apply displacement in the dorsal-ventral axis (z)
        displacement = np.zeros_like(boundary_positions)
        if self.position == 'whole':
            displacement[:, 2] = magnitude
        elif self.position == 'anterior':
            # Only displace boundary particles near anterior 50%
            mask = boundary_positions[:, 0] < np.median(boundary_positions[:, 0])
            displacement[mask, 2] = magnitude
        elif self.position == 'posterior':
            mask = boundary_positions[:, 0] > np.median(boundary_positions[:, 0])
            displacement[mask, 2] = magnitude

        return displacement
```

**Stimulus parameters:**

- Duration: 10 ms (brief mechanical impulse, as in Chalfie et al. 1985)
- Amplitude: 5-20 µm (boundary particle displacement — produces cuticle strain above MEC-4 threshold)
- Position: configurable (whole plate, anterior only, posterior only — for testing directional discrimination)

---

## Alternatives Considered

### 1. Direct Current Injection Instead of Mechanotransduction Model

**Description:** Skip the MEC-4 channel model entirely. Inject a fixed current pulse into touch neurons when a "tap" event is triggered.

**Rejected because:**

- Does not close the loop — the stimulus is artificial, not derived from body mechanics
- Cannot produce graded responses to varying touch intensity
- Cannot model adaptation (MEC-4 channels inactivate during sustained touch)
- Cannot distinguish gentle vs. harsh touch (different channel populations)
- The existing c302_TapWithdrawal.py already tried this approach (empty `cells_to_stimulate`) and "does not produce the correct behavior"

**When to reconsider:** Never. The whole point of [DD019](DD019_Closed_Loop_Touch_Response.md) is mechanistically closing this loop.

### 2. Simplified Linear Transduction (Strain → Current, No Channel Model)

**Description:** Use a simple proportional mapping `I_touch = k * strain` without modeling MEC-4 channel kinetics.

**Rejected because:**

- Loses adaptation dynamics (the hallmark of touch receptor neuron responses)
- Cannot reproduce the rapid onset + slow decay profile observed electrophysiologically
- Cannot be validated against O'Hagan et al. 2005 channel recordings
- Minimal complexity savings — the HH-style channel adds only 2 state variables per touch neuron

**When to reconsider:** If MEC-4 channel parameters prove too uncertain and the linear model suffices for behavioral validation.

### 3. Machine-Learned Transduction Model ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4)

**Description:** Train an RNN on calcium imaging data from touch neurons to learn the strain→activity mapping.

**Deferred because:**

- Insufficient training data (calcium imaging during calibrated mechanical stimulation is scarce)
- Black-box model — cannot interpret the transduction mechanism
- Better to start with the biophysical model and compare to ML later

**When to try:** After the biophysical MEC-4 model is validated. If it performs poorly, the learned model from [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 may capture nonlinear dynamics that the HH approximation misses.

### 4. Finite Element Strain Computation Instead of SPH Particle Displacement

**Description:** Compute strain using a finite element mesh overlaid on the SPH body, for more accurate continuum mechanics.

**Rejected because:**

- Adds significant computational cost (FEM mesh + SPH particles in parallel)
- SPH particle displacement provides sufficient strain resolution for the ~6 touch neuron receptive fields
- Maintaining FEM/SPH consistency during large deformations is non-trivial
- FEM was already rejected for body physics in [DD003](DD003_Body_Physics_Architecture.md)

**When to reconsider:** If strain computation from SPH particles proves too noisy or spatially inaccurate for fine mechanosensory discrimination.

### 5. Proprioceptive Feedback via Stretch Receptors on Motor Neurons

**Description:** In addition to touch neurons, model stretch-sensitive channels on B-class motor neurons (Wen et al. 2012) for proprioceptive wave propagation.

**Deferred (but important) because:**

- This is a separate proprioceptive feedback loop, not the touch response loop
- Adding it simultaneously would confound validation of the touch circuit
- Motor neuron proprioception is likely needed for stable undulatory locomotion but is not required for tap withdrawal specifically

**When to add:** Phase 3, after [DD019](DD019_Closed_Loop_Touch_Response.md)'s touch-response closed loop is validated. Proprioceptive feedback could be [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md).

### 6. Detailed Cuticle Layer Mechanics

**Description:** Model the three cuticle layers (cortical, medial, basal) with distinct mechanical properties and the MEC protein complex (MEC-1/MEC-5/MEC-9 extracellular attachment) explicitly.

**Rejected because:**

- [DD003](DD003_Body_Physics_Architecture.md) currently uses homogeneous elastic particles for the body wall
- Adding cuticle microstructure requires [DD004](DD004_Mechanical_Cell_Identity.md) (Mechanical Cell Identity) to tag particles with tissue layers
- Overkill for the behavioral validation target (tap withdrawal doesn't require cuticle layer resolution)
- Insufficient mechanical characterization of individual cuticle layers

**When to reconsider:** If touch sensitivity requires modeling cuticle anisotropy (longitudinal vs. circumferential strain transmission).

---

## Quality Criteria

### What Defines a Valid Closed-Loop Touch Response Implementation?

1. **MEC-4 Channel Electrophysiology:** The channel model must reproduce the key features of O'Hagan et al. 2005 recordings:
   - Rapid onset (<5 ms from strain application)
   - Peak current 50-150 pA for threshold strain
   - Reversal potential near +10 mV
   - Adaptation (current decays to <20% of peak within 200 ms of sustained strain)

2. **Strain Readout Physical Consistency:** Computed strain values must be:
   - Zero when no external force is applied (resting state)
   - Proportional to applied boundary displacement (linear regime)
   - Spatially localized (strain at posterior should not affect anterior touch neurons)
   - Temporally consistent with SPH timestep (no aliasing artifacts)

3. **Closed-Loop Stability:** The bidirectional coupling must not introduce:
   - Oscillatory instability (positive feedback: strain → touch → motor → movement → more strain)
   - Numerical divergence (NaN, infinite voltages, particle escape)
   - Must remain stable for at least 30 seconds of simulated time

4. **Behavioral Correctness:**
   - Anterior touch → backward locomotion (ALM/AVM → AVA pathway)
   - Posterior touch → forward acceleration (PLM → AVB pathway)
   - Whole-plate tap → backward (anterior-dominant response, as in real worms)
   - No response without stimulus (baseline forward crawling preserved)

5. **Preservation of Existing Behavior:** With `sensory.mechanotransduction: false`, the simulation must produce identical results to the existing open-loop model. No regression in forward crawling kinematics.

### Validation Procedure

```bash
# 1. MEC-4 channel unit test
python scripts/test_mec4_channel.py
# Expected: matches O'Hagan et al. 2005 current traces within ±30%

# 2. Strain readout unit test
python scripts/test_strain_readout.py --known_displacement 10.0
# Expected: strain proportional to displacement, correct spatial localization

# 3. Open-loop regression
docker compose run validate --config forward_crawl
# Expected: identical kinematic scores with mechanotransduction disabled

# 4. Closed-loop tap withdrawal
docker compose run validate --config tap_withdrawal
# Expected:
#   - Reversal onset: < 1 s (target: 300-800 ms per Chalfie et al.)
#   - Reversal distance: ≥ 1 body length
#   - Recovery: forward crawling resumes within 10 s
#   - Direction discrimination: anterior → backward, posterior → forward

# 5. Stability test
docker compose run validate --config tap_withdrawal --duration 30
# Expected: no NaN, no divergence, no oscillatory instability
```

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Chemosensory transduction:** Olfactory (AWA, AWC), gustatory (ASE), nociceptive chemical (ASH) neuron responses to chemical stimuli. Each requires a separate channel model and stimulus delivery system. Future DDs.

2. **Thermosensory transduction:** AFD thermosensory neurons and cryophilic/thermophilic navigation. Different transduction mechanism entirely.

3. **Proprioceptive feedback:** Stretch-sensitive channels on B-class motor neurons (Wen et al. 2012). Important for locomotion wave propagation but a separate feedback loop from touch. Deferred to future DD.

4. **Nose touch:** The nose-touch response involves different neurons (OLQ, CEP, FLP, ASH) and likely different mechanosensory channels (TRP family, not DEG/ENaC). Separate behavior circuit.

5. **Habituation and sensitization:** Repeated taps cause habituation (decreased reversal probability). This involves neuromodulatory mechanisms (dopamine, serotonin) not modeled in [DD019](DD019_Closed_Loop_Touch_Response.md). See [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptidergic Connectome) for the modulatory framework.

6. **Male-specific touch neurons:** Males have additional touch-related neurons (e.g., ray neurons for mating). Hermaphrodite only in [DD019](DD019_Closed_Loop_Touch_Response.md).

7. **Environmental mechanics beyond flat agar:** Soil, bacterial lawns, geometric obstacles, microfluidic channels. [DD003](DD003_Body_Physics_Architecture.md) currently supports simple boundary conditions only.

8. **Cuticle fine structure:** Three-layer cuticle mechanics, annuli, alae. Homogeneous elastic particles are sufficient for [DD019](DD019_Closed_Loop_Touch_Response.md).

---

## Code Reuse Opportunities

### CE_locomotion Proprioceptive Feedback Model

**Repository:** `openworm/CE_locomotion` (pushed 2026-02-18, **VERY ACTIVE**)
**Collaboration:** Dr. Erick Olivares & Prof. Randall Beer

This repo contains a **complete neuromechanical C++ model** with a `StretchReceptor` module implementing proprioceptive feedback on motor neurons (Wen et al. 2012). This is the **missing piece** [DD019](DD019_Closed_Loop_Touch_Response.md) scopes out for future work.

**What It Provides:**

- `StretchReceptor.cpp/h` — B-class motor neuron stretch-sensitive currents
- Produces forward + backward locomotion from the same circuit (gait modulation)
- Evolutionary parameter fitting algorithm

**Reuse Plan for [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (Proprioceptive Feedback):**
```bash
# Clone and test
git clone https://github.com/openworm/CE_locomotion.git
cd CE_locomotion
make
./main  # Runs evolutionary optimization (~2 minutes)
python viz.py  # Visualize neural/muscle activity

# Extract StretchReceptor algorithm
# File: StretchReceptor.cpp (lines 1-120, stretch-dependent current model)
# Port: C++ → Python or NeuroML for c302 integration
```

**Next Actions:**

- [ ] Contact authors (still active as of 2026-02-18) — collaborate on proprioception DD?
- [ ] Extract StretchReceptor model, compare to Wen et al. 2012 data
- [ ] Write [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md): Proprioceptive Feedback (references CE_locomotion as source)
- [ ] Integrate with [DD001](DD001_Neural_Circuit_Architecture.md) B-class motor neurons

**Estimated Time Savings:** 30-40 hours (proprioceptive model exists, just needs porting)

---

## Context & Background

### The Longstanding Goal

The tap withdrawal reflex is arguably the most studied mechanosensory behavior in *C. elegans*. Martin Chalfie's pioneering work (Nobel Prize 2008, partly for GFP discovery in touch neuron studies) established the genetic and cellular basis:

- Six touch receptor neurons mediate gentle body touch
- MEC genes encode the mechanosensory channel complex
- The neural circuit for tap withdrawal was mapped by Chalfie et al. 1985 and refined by Wicks et al. 1996

For OpenWorm, implementing closed-loop touch response has been a goal since the project's inception. GitHub issues #223-#227 (openworm/openworm) document multi-year efforts to connect the c302 neural circuit with Sibernetic body physics for this behavior.

### What Exists Today

**c302_TapWithdrawal.py** defines the tap withdrawal circuit with:

- 16 interneurons: AVAL/R, AVBL/R, PVCL/R, AVDL/R, DVA, PVDL/R, PLML/R, AVM, ALML/R
- Motor neuron groups: VA1-12, VB1-11, DA1-9, DB1-7, DD1-6, VD1-13
- 130+ connection polarity overrides (exc/inh assignments, manually curated from Chalfie et al.)
- 60+ gap junction weight overrides
- **But:** sensory neurons have no input (`cells_to_stimulate` is empty)
- **But:** motor output uses artificial sinusoidal inputs to VB/DB rather than command interneuron drive
- **Header note:** "Tap-Withdrawal circuit still under development — it does not produce the correct behavior!"

**sibernetic_c302.py** implements the forward coupling (neural → body):

- Reads muscle calcium from NEURON
- Converts to activation coefficients
- Writes to Sibernetic muscle input file
- **But:** no reverse path (body → sensory)

### What's Missing ([DD019](DD019_Closed_Loop_Touch_Response.md) Fills This)

1. **Mechanosensory transduction model** — converting cuticle strain to neural current
2. **Cuticle strain readout** — computing strain from SPH particle displacements
3. **Bidirectional coupling** — extending `sibernetic_c302.py` with the reverse path
4. **Tap stimulus** — delivering a mechanical perturbation through Sibernetic boundary particles
5. **Command-interneuron-driven motor switching** — replacing artificial sinusoidal inputs with emergent motor pattern selection

### Biological Foundations

The tap withdrawal circuit is one of the best-characterized neural circuits in any organism:

**Chalfie et al. 1985** — defined the gentle touch circuit: ALM/AVM (anterior) and PLM (posterior) touch neurons, AVA/AVD (backward command) and AVB/PVC (forward command) interneurons.

**Wicks et al. 1996** — showed that anterior touch preferentially activates backward locomotion, posterior touch activates forward locomotion, and a whole-plate tap produces a net backward response because the anterior pathway dominates.

**O'Hagan et al. 2005** — first direct electrophysiological recordings from *C. elegans* touch receptor neurons. Showed MEC-4 channel responses with rapid onset, adaptation, and ~100-150 pA peak currents.

**Goodman et al. 2002** — characterized MEC-4/MEC-10 as a DEG/ENaC family channel with non-selective cation permeability (E_rev ≈ +10 mV).

**Wen et al. 2012** — demonstrated proprioceptive feedback in B-class motor neurons, suggesting the locomotion wave is partially driven by stretch-sensitive mechanisms (deferred to future DD, out of scope here).

---

## Implementation References

### Existing Code Locations

```
openworm/c302/
├── c302/c302_TapWithdrawal.py         # Existing circuit definition (to be updated)
├── c302/c302_GenericCell.py            # Generic neuron template ([DD001](DD001_Neural_Circuit_Architecture.md))
├── channel_models/                     # Existing channel models
│   ├── leak_chan.channel.nml
│   ├── k_slow_chan.channel.nml
│   ├── k_fast_chan.channel.nml
│   └── ca_boyle_chan.channel.nml
├── channel_models/mec4_chan.channel.nml  # NEW ([DD019](DD019_Closed_Loop_Touch_Response.md))
└── cells/                              # NEW touch neuron templates ([DD019](DD019_Closed_Loop_Touch_Response.md))
    ├── ALMCell.cell.nml
    ├── AVMCell.cell.nml
    ├── PLMCell.cell.nml
    └── PVDCell.cell.nml

openworm/sibernetic/
├── sibernetic_c302.py                  # Existing forward coupling
├── sibernetic_c302_closedloop.py       # NEW bidirectional ([DD019](DD019_Closed_Loop_Touch_Response.md))
├── coupling/
│   └── strain_readout.py              # NEW ([DD019](DD019_Closed_Loop_Touch_Response.md))
└── stimuli/
    └── tap_stimulus.py                # NEW ([DD019](DD019_Closed_Loop_Touch_Response.md))
```

### Key Data Sources

- **Connectome (NMJ + interneuron):** ConnectomeToolbox / `cect` package (Cook et al. 2019)
- **MEC-4 electrophysiology:** O'Hagan et al. 2005, Goodman et al. 2002
- **Behavioral data:** Chalfie et al. 1985 (reversal latency), Wicks et al. 1996 (direction discrimination)
- **Touch neuron positions:** WormAtlas, White et al. 1986

---

## Migration Path

### If Mechanotransduction Model Needs Updating

1. **Create a new channel model** (e.g., `mec4_v2_chan.channel.nml`) rather than modifying the original
2. **Pin the channel version** in `openworm.yml`: `sensory.mec4_version: "v2"`
3. **Re-validate** all behavioral tests (reversal latency, distance, direction discrimination)
4. **Update coupling script** if strain→channel interface changes

### If Additional Sensory Modalities Are Added

Each new sensory modality (chemosensory, thermosensory, proprioceptive) follows the [DD019](DD019_Closed_Loop_Touch_Response.md) pattern:

1. Define the transduction channel model
2. Create a stimulus readout module (chemical concentration, temperature, stretch)
3. Extend the bidirectional coupling script
4. Validate the emergent behavior

---

## References

1. **Chalfie M, Sulston JE, White JG, Southgate E, Thomson JN, Brenner S (1985).** "The neural circuit for touch sensitivity in *Caenorhabditis elegans*." *J Neurosci* 5:956-964.
   *Foundational touch circuit: touch neurons, command interneurons, reversal behavior.*

2. **Wicks SR, Roehrig CJ, Bhatt R, Rankin CH (1996).** "Tap withdrawal in *Caenorhabditis elegans*: Identification of neural substrates." *J Neurobiol* 31:1-11.
   *Refined circuit diagram. Anterior vs. posterior discrimination.*

3. **O'Hagan R, Bhatt S, Bhatt R, Bhatt R (2005).** "The MEC-4 DEG/ENaC channel of *Caenorhabditis elegans* touch receptor neurons transduces mechanical signals." *Nat Neurosci* 8:43-50.
   *First direct electrophysiology of touch receptor neurons. MEC-4 channel kinetics.*

4. **Goodman MB, Ernstrom GG, Bhatt R, Davis MW, Jones BK (2002).** "MEC-2 regulates *C. elegans* DEG/ENaC channels needed for mechanosensation." *Nature* 415:1039-1042.
   *MEC channel complex characterization. Reversal potential, conductance.*

5. **Wen Q, Po MD, Hulme E, Chen S, Liu X, Kwok SW, Gershow M, Leifer AM, Butler V, Fang-Yen C, Samuel ADT (2012).** "Proprioceptive coupling within motor neurons drives undulatory locomotion in *C. elegans*." *Neuron* 76:750-761.
   *B-class motor neuron proprioception (stretch-sensitive, out of scope for [DD019](DD019_Closed_Loop_Touch_Response.md)).*

6. **Boyle JH, Cohen N (2008).** "Caenorhabditis elegans body wall muscles are simple actuators." *Biosystems* 94:170-181.
   *Muscle model parameters used in [DD002](DD002_Muscle_Model_Architecture.md) calcium-force coupling.*

7. **Cook SJ et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *Connectome topology for circuit definition.*

8. **White JG, Southgate E, Thomson JN, Brenner S (1986).** "The structure of the nervous system of the nematode *Caenorhabditis elegans*." *Phil Trans R Soc Lond B* 314:1-340.
   *Original connectome paper (Mind of a Worm). Touch neuron positions and morphology.*

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units | Timestep |
|-------|----------|----------|--------|-------|----------|
| Elastic particle positions | [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic) | Per-particle (x, y, z) for body wall particles | Sibernetic internal state / shared memory | µm | dt_body (20 µs) |
| Rest particle positions | [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic) | Per-particle (x, y, z) at t=0 | Snapshot at initialization | µm | One-time |
| Boundary particle positions | [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic) | Per-particle (x, y, z) for agar surface | Sibernetic internal state | µm | dt_body |
| Connectome (touch circuit) | [DD001](DD001_Neural_Circuit_Architecture.md) (ConnectomeToolbox) | Touch neuron → interneuron → motor neuron adjacency | ConnectomeToolbox API | neuron pairs + weights | One-time |
| Cell-type channel densities (optional) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | CeNGEN-derived conductances for ALM, AVM, PLM, PVD | NeuroML `<channelDensity>` | S/cm² | One-time |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units | Timestep |
|--------|------------|----------|--------|-------|----------|
| Touch neuron membrane voltage | [DD001](DD001_Neural_Circuit_Architecture.md) (part of network simulation) | `V` per touch neuron | NeuroML state variable | mV | dt_neuron (0.05 ms) |
| Touch neuron [Ca²⁺]ᵢ | [DD001](DD001_Neural_Circuit_Architecture.md) (downstream synaptic output) | `ca_internal` per touch neuron | NeuroML state variable | mol/cm³ | dt_neuron |
| Command interneuron activity (AVA, AVB) | [DD002](DD002_Muscle_Model_Architecture.md) (motor neuron drive) | Calcium/voltage of command interneurons | NeuroML state variable | mV, mol/cm³ | dt_neuron |
| Reversal event log | [DD010](DD010_Validation_Framework.md) (Tier 3 validation) | Event onset/offset/type | JSON or CSV | s (timestamps) | Per-event |
| Cuticle strain time series (viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-body-segment strain magnitude | OME-Zarr: `sensory/strain/`, shape (n_timesteps, n_segments) | dimensionless | output_interval |
| Reversal event annotations (viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Event markers on timeline | OME-Zarr: `behavior/events/`, shape (n_events, 3) | s, enum | Per-event |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository (channel model + circuit)** | `openworm/c302` |
| **Repository (coupling + stimulus)** | `openworm/sibernetic` |
| **Docker stage** | `neural` (c302 changes) + `body` (Sibernetic changes) |
| **`versions.lock` keys** | `c302`, `sibernetic` (both must be pinned together for closed-loop) |
| **Build dependencies** | Same as [DD001](DD001_Neural_Circuit_Architecture.md) + [DD003](DD003_Body_Physics_Architecture.md); no new dependencies |

### Configuration

```yaml
sensory:
  mechanotransduction: true            # Enable MEC-4 channel on touch neurons
  mec4_version: "v1"                   # Pin channel model version
  strain_filter_tau: 5.0               # ms, low-pass filter on strain signal
  strain_readout_method: "sph_displacement"  # Method for computing strain

behavior:
  tap_withdrawal: true                 # Enable closed-loop tap withdrawal
  motor_switching: "command_interneuron"  # "command_interneuron" ([DD019](DD019_Closed_Loop_Touch_Response.md)) or "sinusoidal" (legacy)

stimulus:
  type: "tap"                          # Stimulus type
  onset: 5.0                           # s, time of tap delivery
  duration: 0.01                       # s, tap duration (10 ms impulse)
  amplitude: 10.0                      # µm, boundary particle displacement
  position: "whole"                    # "whole", "anterior", "posterior"
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `sensory.mechanotransduction` | `false` | `true`/`false` | Enable MEC-4 mechanosensory transduction |
| `sensory.mec4_version` | `"v1"` | String | Pin MEC-4 channel model version |
| `sensory.strain_filter_tau` | `5.0` | 1.0-50.0 ms | Low-pass filter time constant for strain signal |
| `sensory.strain_readout_method` | `"sph_displacement"` | `"sph_displacement"` | Strain computation method |
| `behavior.tap_withdrawal` | `false` | `true`/`false` | Enable closed-loop tap withdrawal circuit |
| `behavior.motor_switching` | `"sinusoidal"` | `"sinusoidal"`, `"command_interneuron"` | Motor pattern source |
| `stimulus.type` | `"tap"` | `"tap"`, `"gentle_anterior"`, `"gentle_posterior"` | Stimulus type |
| `stimulus.onset` | `5.0` | Positive float (s) | Stimulus onset time |
| `stimulus.duration` | `0.01` | 0.001-1.0 s | Stimulus duration |
| `stimulus.amplitude` | `10.0` | 1.0-50.0 µm | Boundary displacement amplitude |
| `stimulus.position` | `"whole"` | `"whole"`, `"anterior"`, `"posterior"` | Spatial position of stimulus |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
docker compose run quick-test --config tap_withdrawal
# Checks: 30 s simulation without NaN/divergence
# Checks: reversal event detected after tap
# Checks: forward crawling preserved before tap

# Full validation (must pass before merge to main)
docker compose run validate --config tap_withdrawal
# Checks:
#   - Reversal onset < 1 s (Tier 3, blocking)
#   - Reversal distance ≥ 1 body length (Tier 3, blocking)
#   - Recovery to forward < 10 s (Tier 3, blocking)
#   - Direction discrimination (anterior→backward, posterior→forward) (Tier 3, blocking)
#   - No regression in forward crawling kinematics (Tier 3, blocking)
```

**Per-PR checklist:**

- [ ] `jnml -validate` passes for MEC-4 channel model and touch neuron cell files
- [ ] MEC-4 unit test passes (onset, peak current, adaptation, reversal potential)
- [ ] Strain readout unit test passes (spatial localization, proportionality)
- [ ] `quick-test` passes (closed-loop stable 30 s, reversal event detected)
- [ ] `validate` passes (Tier 3 behavioral + no forward-crawl regression)
- [ ] Existing open-loop simulations produce identical results when mechanotransduction is disabled

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `sensory/strain/` (n_timesteps, n_segments) | Cuticle strain heatmap | Blue (0) → red (>0.1 strain) |
| `neural/calcium/` (n_timesteps, 302) — touch + command neurons highlighted | Touch circuit activation | Warm colormap, touch neurons + AVA/AVB highlighted |
| `behavior/events/` (n_events, 3) | Reversal event markers | Green (forward) → red (backward) on timeline |
| `body/positions/` (existing) | Body trajectory | Path colored by locomotion direction |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Elastic particle positions | [DD003](DD003_Body_Physics_Architecture.md) | If particle count, indexing, or coordinate frame changes, strain readout breaks |
| Muscle activation interface | [DD002](DD002_Muscle_Model_Architecture.md) | Forward coupling path (existing) — if activation format changes, coupling script breaks |
| Touch circuit connectivity | [DD001](DD001_Neural_Circuit_Architecture.md) | If connectome data for touch neurons or command interneurons changes, circuit behavior changes |
| Cell-type conductances (optional) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | If CeNGEN-derived densities for touch neurons change, baseline excitability changes |
| Neuropeptide modulation (optional) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Dopamine/serotonin modulation of touch sensitivity (habituation) — future work |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Behavioral validation | [DD010](DD010_Validation_Framework.md) | Tier 3 behavioral tests are defined by [DD019](DD019_Closed_Loop_Touch_Response.md) success criteria |
| Learned sensory transduction | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 may replace MEC-4 model with learned alternative — interface must match |
| Future sensory DDs | Future | [DD019](DD019_Closed_Loop_Touch_Response.md) establishes the pattern for body→sensory coupling; future modalities follow same architecture |
| Visualization | [DD014](DD014_Dynamic_Visualization_Architecture.md) | New OME-Zarr groups (`sensory/`, `behavior/`) require viewer support |

---

**Approved by:** Pending
**Implementation Status:** Proposed
**Next Actions:**

1. Implement MEC-4 channel model in NeuroML (`mec4_chan.channel.nml`)
2. Implement cuticle strain readout from SPH particles (`strain_readout.py`)
3. Implement tap stimulus delivery (`tap_stimulus.py`)
4. Extend coupling script for bidirectional communication (`sibernetic_c302_closedloop.py`)
5. Update `c302_TapWithdrawal.py`: add MEC-4 to touch neurons, replace sinusoidal input with command interneuron drive
6. Validate: MEC-4 unit test → strain readout unit test → closed-loop stability → behavioral metrics
7. Create GitHub issues for each script and component (track with `dd019` label)
