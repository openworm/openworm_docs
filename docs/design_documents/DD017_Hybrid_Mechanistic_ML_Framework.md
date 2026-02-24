# DD017: Hybrid Mechanistic-ML Framework

- **Status:** Proposed (Phase 3-4)
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-16
- **Supersedes:** None
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD003](DD003_Body_Physics_Architecture.md) (Body Physics), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization), [DD009](DD009_Intestinal_Oscillator_Model.md) (Intestinal Oscillator), [DD010](DD010_Validation_Framework.md) (Validation Framework), [DD013](DD013_Simulation_Stack_Architecture.md) (Simulation Stack)

---

> **Phase:** [Phase 3: Organ Integration & Behavior](DD_PHASE_ROADMAP.md#phase-3-organ-integration--behavior-months-13-18) | **Layer:** ML Framework

## TL;DR

When mechanistic models hit data gaps (unknown ion channel kinetics, unmeasured synaptic weights), this framework provides a disciplined way to use machine learning as a gap-filler — constrained by known biology so ML components can be replaced as experimental data becomes available. The remaining three components are: (1) a differentiable simulation backend for automatic parameter fitting, (2) a neural surrogate for SPH to achieve 1000x speedup, and (4) learned sensory transduction to close the stimulus-response loop. Component 3 (foundation model → ODE parameters) has been extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md) and promoted to Phase A/Phase 1.

## Goal & Success Criteria

**Goal:** Provide a principled framework for combining mechanistic models with ML where experimental data is insufficient, while preserving OpenWorm's core commitment to mechanistic interpretability.

**Success Criteria:**

- ML-augmented models match or exceed pure-mechanistic validation scores ([DD010](DD010_Validation_Framework.md) Tier 2 correlation r > 0.5)
- Differentiable backend reproduces NEURON/jNML reference within +/-5% on all state variables
- SPH surrogate achieves at least 100x speedup (target 1000x) with < 5% trajectory error
- Auto-fitted parameters outperform hand-tuned parameters on [DD010](DD010_Validation_Framework.md) metrics
- Every ML component has a documented replacement pathway for when experimental data becomes available

## Deliverables

- Framework specification document (this DD)
- Differentiable simulation backend (`openworm/openworm-ml/differentiable/`) — PyTorch reimplementation of [DD001](DD001_Neural_Circuit_Architecture.md)+[DD002](DD002_Muscle_Model_Architecture.md)+[DD009](DD009_Intestinal_Oscillator_Model.md) ODEs
- Neural surrogate for SPH body physics (`openworm/openworm-ml/surrogate/`)
- Foundation model parameter pipeline (`openworm/openworm-ml/foundation_params/`) — **Extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md)**
- Learned sensory transduction module (`openworm/openworm-ml/sensory/`)
- ML component registry tracking which model parameters use ML vs. mechanistic values `[TO BE CREATED]`
- Benchmark comparison scripts (ML-augmented vs. pure mechanistic) `[TO BE CREATED]`

## Repository & Issues

- **Repository:** `openworm/openworm-ml` (new repo) `[TO BE CREATED]`
- **Issue label:** `dd017`
- **Milestone:** Phase 3 — Hybrid ML Framework
- **Example PR title:** `dd017: differentiable HH backend matches NEURON reference within ±5%`

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 3](DD_PHASE_ROADMAP.md#phase-3-organ-systems-hybrid-ml-months-7-12) |
| **Layer** | Hybrid ML — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-3-organ-systems-hybrid-ml-months-7-12) |
| **What does this produce?** | (1) Differentiable c302 neural circuit in PyTorch/JAX, (2) Neural surrogate for Sibernetic SPH, (4) Learned sensory transduction module. Component 3 (foundation model → ODE parameters) extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md) |
| **Success metric** | Differentiable model matches [DD010](DD010_Validation_Framework.md) Tier 2+3 validation within ±5% of reference NEURON/jNML; SPH surrogate achieves 1000x speedup with <5% trajectory error; auto-fitted parameters outperform hand-tuned on [DD010](DD010_Validation_Framework.md) metrics |
| **Repository** | `openworm/openworm-ml` (new repo) — issues labeled `dd017` |
| **Config toggle** | `ml.differentiable_backend: true`, `ml.sph_surrogate: true`, `ml.sensory_model: learned` in `openworm.yml` |
| **Build & test** | `docker compose run ml-test` (differentiable model matches reference), `docker compose run surrogate-validate` (surrogate vs. full SPH) |
| **CI gate** | Differentiable model must reproduce [DD010](DD010_Validation_Framework.md) Tier 2+3 scores within ±5% of NEURON reference |

---

## How to Build & Test

### Prerequisites

- Simulation stack ([DD013](DD013_Simulation_Stack_Architecture.md)) running
- Training datasets from [DD010](DD010_Validation_Framework.md)/[DD024](DD024_Validation_Data_Acquisition_Pipeline.md)

### Getting Started (Environment Setup)

This DD shares the `openworm-ml` repository with [DD025](DD025_Protein_Foundation_Model_Pipeline.md). Follow [DD025 Getting Started](DD025_Protein_Foundation_Model_Pipeline.md#getting-started-environment-setup) to clone the repo and install base dependencies.

**Path A — Docker (recommended):**

```bash
# From the OpenWorm meta-repo (see DD013 Simulation Stack Architecture)
docker compose build ml
# Then use the docker compose run commands below for each component
```

Cross-reference: [DD013](DD013_Simulation_Stack_Architecture.md) for the full Docker Compose stack setup.

**Path B — Native:**

```bash
git clone https://github.com/openworm/openworm-ml.git
cd openworm-ml
pip install -e ".[dev]"  # includes PyTorch, torchdiffeq, ESM dependencies
```

Additional dependency for differentiable ODE solvers:

```bash
pip install torchdiffeq  # ODE solver integration for differentiable simulation
```

!!! note "GPU Support"
    PyTorch with GPU support (CUDA on Linux, MPS on macOS) is strongly recommended for differentiable simulation and neural surrogates. CPU-only mode works but training will be significantly slower.

### Step-by-step

1. **Differentiable backend:** `docker compose run ml-test` — verifies PyTorch ODE solver matches NEURON/jNML reference within +/-5%
2. **Auto-fitting:** `docker compose run ml-autofit` — runs gradient descent against [DD010](DD010_Validation_Framework.md) validation targets
3. **SPH surrogate:** `docker compose run surrogate-validate` — compares surrogate predictions against full SPH on held-out test set
4. **Foundation model pipeline:** `docker compose run foundation-params` — generates per-neuron-class HH parameters from gene sequences
5. **Sensory model:** `docker compose run sensory-test` — validates learned sensory responses against published calcium imaging data

**Quick start for a single component:**

```bash
# Clone and set up
git clone https://github.com/openworm/openworm-ml.git
cd openworm-ml
pip install -r requirements.txt  # torch, torchdiffeq, neuraloperator, esm

# Run equivalence test for differentiable backend
python differentiable/test_equivalence.py --reference data/neuron_reference.h5

# Train SPH surrogate (requires training data)
python surrogate/train.py --data data/sph_training/ --epochs 100
```

Detailed commands: `[TO BE DEVELOPED as components are implemented]`

## How to Visualize

- In the [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer, ML-augmented components should be visually distinguished (e.g., dashed outlines or a distinct color) from fully mechanistic components, so users can see where ML is filling gaps.
- ML uncertainty estimates should be displayable as confidence intervals or heatmaps overlaid on the simulation.
- The ML component registry should provide a dashboard view showing which parameters are ML-derived vs. mechanistic vs. experimentally measured.
- Auto-fitting convergence curves (loss vs. epoch) should be plottable for debugging and reporting.

## Context & Background

### The Current Approach Works — But Has Real Limitations

OpenWorm's simulation stack ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md)) uses coupled ordinary differential equations (ODEs) with Hodgkin-Huxley (HH) conductance-based neuron models, calcium-force muscle coupling, and Smoothed Particle Hydrodynamics (SPH) for body physics. This approach is:

- **Mechanistically interpretable:** Every parameter has a physical meaning (conductances in mS/cm², time constants in ms, calcium concentrations in µM)
- **Compositionally modular:** New subsystems (neuropeptides [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), intestine [DD009](DD009_Intestinal_Oscillator_Model.md), pharynx [DD007](DD007_Pharyngeal_System_Architecture.md)) plug in via clean Integration Contracts
- **Causally explanatory:** You can trace why behavior emerges through the causal chain (sensory input → neural voltage → muscle calcium → body force → movement)

This is OpenWorm's core differentiator vs. Virtual Cell Foundation Models (CZI's ESM3, Arc's Virtual Cell Challenge). Those approaches are data-driven black boxes. OpenWorm is a mechanistic, causally interpretable model. **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) does not replace that foundation — it enhances it.**

### Four Pain Points That ML Can Address

**1. Speed:** [DD009](DD009_Intestinal_Oscillator_Model.md) notes that 200 seconds of simulated time takes ~10 hours wall clock. [DD003](DD003_Body_Physics_Architecture.md)'s SPH with ~100K particles is the bottleneck. This makes iteration brutal — a researcher adjusting one parameter waits half a day for feedback.

**2. Parameter gaps:** [DD001](DD001_Neural_Circuit_Architecture.md) uses the *same* generic HH parameters for all 302 neurons (from [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025) muscle electrophysiology). [DD005](DD005_Cell_Type_Differentiation_Strategy.md) proposes specializing via CeNGEN transcriptomics, but the mapping from transcript counts to conductance densities is hand-crafted and unvalidated. Most neurons lack direct electrophysiology data.

**3. Manual parameter fitting:** [DD009](DD009_Intestinal_Oscillator_Model.md) states parameters were "fit to match ~50 second period." [DD002](DD002_Muscle_Model_Architecture.md)'s `max_ca = 4e-7` and `muscle_strength = 4000` were manually tuned. [DD001](DD001_Neural_Circuit_Architecture.md)'s synaptic conductance `g_syn = 0.09 nS` was hand-set. With hundreds of parameters across [DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md), manual tuning doesn't scale.

**4. Missing sensory front-end:** [DD001](DD001_Neural_Circuit_Architecture.md) explicitly scopes out sensory transduction: "Currently sensory neurons receive generic current injections." The worm can't sense its environment, making closed-loop behavior impossible.

### The Hybrid Principle

**Core rule: ML operates at the boundaries of the mechanistic model, never replacing the causal core.**

```
┌──────────────────────────────────────────────────────────┐
│                    ML BOUNDARY LAYER                      │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ Foundation   │   │ Learned      │   │ Learned      │  │
│  │ Model → ODE  │   │ Sensory      │   │ Validation   │  │
│  │ Parameters   │   │ Transduction │   │ Metrics      │  │
│  └──────┬──────┘   └──────┬───────┘   └──────────────┘  │
│         │                  │                              │
│  ┌──────▼──────────────────▼──────────────────────────┐  │
│  │          MECHANISTIC CORE (unchanged)               │  │
│  │  [DD001](DD001_Neural_Circuit_Architecture.md): HH Neural Circuit (302 neurons, ODEs)       │  │
│  │  [DD002](DD002_Muscle_Model_Architecture.md): Muscle Ca²⁺-Force Coupling (95 muscles)     │  │
│  │  [DD003](DD003_Body_Physics_Architecture.md): SPH Body Physics (100K particles)           │  │
│  │  [DD006](DD006_Neuropeptidergic_Connectome_Integration.md): Neuropeptide Modulation                     │  │
│  │  [DD007](DD007_Pharyngeal_System_Architecture.md): Pharyngeal System                           │  │
│  │  [DD009](DD009_Intestinal_Oscillator_Model.md): Intestinal Oscillator                       │  │
│  └──────────────────────┬─────────────────────────────┘  │
│                         │                                 │
│  ┌──────────────────────▼─────────────────────────────┐  │
│  │           ML ACCELERATION LAYER                     │  │
│  │  ┌─────────────────┐   ┌────────────────────────┐  │  │
│  │  │ Neural Surrogate │   │ Differentiable Backend │  │  │
│  │  │ for SPH (fast)   │   │ (auto parameter fit)   │  │  │
│  │  └─────────────────┘   └────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

The mechanistic ODEs remain the source of truth. ML is used for:

1. **Speeding up** the simulation (surrogate models)
2. **Parameterizing** the simulation (foundation models → ODE parameters)
3. **Fitting** the simulation to data (differentiable simulation + gradient descent)
4. **Extending** the simulation where mechanistic models don't exist yet (sensory transduction)

---

## Technical Approach

### Component 1: Differentiable Simulation Backend

#### What It Means (The Deep Explanation)

Today, when a parameter in the simulation is wrong, the workflow is manual trial and error:

1. Pick initial parameter values from literature
2. Run the simulation (takes hours)
3. Measure the output — e.g., defecation period is 38 seconds (target: 50)
4. Manually adjust `v_release` from 10 to 8 µM/s
5. Run the simulation again — period is now 62 seconds (overshot)
6. Adjust again... repeat 20-50 times
7. Eventually land on values that produce ~50 seconds

This is how [DD009](DD009_Intestinal_Oscillator_Model.md)'s parameters were fit ("fit to match ~50 second period"). [DD001](DD001_Neural_Circuit_Architecture.md)'s `g_syn = 0.09 nS` and [DD002](DD002_Muscle_Model_Architecture.md)'s `max_ca = 4e-7 mol` were similarly hand-tuned.

**"Differentiable" means the simulator can automatically answer: "If I increase `g_max_Kslow` by 0.001 mS/cm², how much does the worm's forward speed change?"**

That quantity — `∂(speed) / ∂(g_max_Kslow)` — is a **gradient**. It tells you the sensitivity of any output to any parameter. Once you have gradients for all parameters simultaneously, you can use gradient descent (the same algorithm that trains neural networks) to automatically find the parameter values that make the simulation match experimental data.

#### What Changes (And What Doesn't)

The equations do not change at all. Same HH formalism, same IP3 receptor model, same calcium dynamics. The only difference is what software runs them.

| | Today ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md)) | Differentiable Backend |
|---|---|---|
| **Equations** | `C * dV/dt = I_leak + I_K + I_Ca + ...` | Identical |
| **Parameters** | Physical meaning (conductances, time constants) | Same physical meaning |
| **Solver** | NEURON / jNML (C/C++, not differentiable) | JAX or PyTorch ODE solver (Python, differentiable) |
| **Parameter fitting** | Manual trial and error | Automatic gradient descent |
| **Output** | Voltage traces, calcium, kinematics | Identical outputs + gradients |

In practice, the ODE right-hand side is rewritten in PyTorch/JAX instead of NeuroML XML:

```python
import torch
from torchdiffeq import odeint

class CelegansNeuron(torch.nn.Module):
    """Same HH equations as [DD001](DD001_Neural_Circuit_Architecture.md), rewritten in PyTorch.

    The key difference: every parameter is a torch.nn.Parameter,
    which means PyTorch automatically tracks how the output
    depends on each parameter (the gradient).
    """
    def __init__(self):
        super().__init__()
        # These are now differentiable parameters.
        # Same values as [DD001](DD001_Neural_Circuit_Architecture.md), same physical meaning.
        self.g_leak = torch.nn.Parameter(torch.tensor(0.005))   # mS/cm²
        self.g_Kslow = torch.nn.Parameter(torch.tensor(3.0))    # mS/cm²
        self.g_Kfast = torch.nn.Parameter(torch.tensor(0.0711)) # mS/cm²
        self.g_Ca = torch.nn.Parameter(torch.tensor(3.0))       # mS/cm²

    def forward(self, t, state):
        V, Ca = state[0], state[1]

        # Same equations as [DD001](DD001_Neural_Circuit_Architecture.md) line 60-76, verbatim
        I_leak = self.g_leak * (V - (-50.0))          # E_leak = -50 mV
        I_K = self.g_Kslow * m_inf(V) * (V - (-60.0)) # E_K = -60 mV
        I_Ca = self.g_Ca * m_Ca(V) * h_Ca(V) * (V - 40.0)  # E_Ca = +40 mV

        dVdt = -(I_leak + I_K + I_Ca) / 1.0  # C_m = 1 µF/cm²
        dCadt = -0.000238 * I_Ca - Ca / 11.5943  # rho, tau_Ca from [DD001](DD001_Neural_Circuit_Architecture.md)

        return torch.stack([dVdt, dCadt])

# Create the model (same parameters as today)
neuron = CelegansNeuron()

# Solve the ODE forward in time (same math as NEURON, just in PyTorch)
initial_state = torch.tensor([-45.0, 0.0])  # V_init, Ca_init
time_points = torch.linspace(0, 1000, 10000)  # 1 second, 0.1ms steps
solution = odeint(neuron, initial_state, time_points)

# Compare to experimental data (e.g., Randi 2023 calcium imaging)
simulated_calcium = solution[:, 1]
experimental_calcium = load_randi_data("AVAL")
loss = torch.mean((simulated_calcium - experimental_calcium) ** 2)

# THIS IS THE KEY LINE:
# Compute ∂loss/∂g_leak, ∂loss/∂g_Kslow, ∂loss/∂g_Ca automatically.
# This tells you exactly which parameters to adjust and by how much.
loss.backward()

# Now neuron.g_Kslow.grad contains the gradient.
# If it's positive: decreasing g_Kslow would reduce the error.
# If it's negative: increasing g_Kslow would reduce the error.
print(f"g_Kslow gradient: {neuron.g_Kslow.grad}")
print(f"g_Ca gradient: {neuron.g_Ca.grad}")
```

#### Why This Matters for OpenWorm Specifically

The system has a **302-neuron, 95-muscle, 20-intestinal-cell model** where:

- [DD001](DD001_Neural_Circuit_Architecture.md) uses the *same* generic conductances for all 302 neurons
- [DD005](DD005_Cell_Type_Differentiation_Strategy.md) proposes specializing them via CeNGEN, but the mapping from transcript levels → conductances is unknown
- [DD009](DD009_Intestinal_Oscillator_Model.md) has 4+ parameters that were manually fit to a 50-second target
- [DD002](DD002_Muscle_Model_Architecture.md)'s `max_ca = 4e-7` and `muscle_strength = 4000` were manually tuned
- [DD010](DD010_Validation_Framework.md) has quantitative validation targets (speed ±15%, period 50±10s, functional connectivity r > 0.5)

A differentiable simulation enables:

1. Start with the current generic [DD001](DD001_Neural_Circuit_Architecture.md) parameters
2. Define the loss as the sum of all [DD010](DD010_Validation_Framework.md) validation criteria:
   ```python
   loss = (
       weight_speed * (sim_speed - exp_speed)**2 +
       weight_period * (sim_defecation_period - 50.0)**2 +
       weight_connectivity * (1.0 - correlation(sim_fc_matrix, randi_fc_matrix)) +
       weight_wavelength * (sim_wavelength - exp_wavelength)**2
   )
   ```

3. Automatically find **per-neuron-class** conductances that satisfy ALL validation tiers simultaneously
4. Do this in hours of compute instead of months of manual tuning

The result is still a mechanistic HH model with physically meaningful parameters — you just found the right parameter values automatically instead of by hand. Every parameter still means something: `g_Kslow = 2.7 mS/cm² for AVAL, 3.4 mS/cm² for AWCL` is still a measurable, falsifiable prediction about ion channel conductance.

#### First Application: Synaptic Weight and Polarity Optimization

The most impactful near-term application of the differentiable backend is automated optimization of synaptic connection weights and excitatory/inhibitory polarities. Zhao et al. (2024) demonstrated this approach on a 136-neuron locomotion circuit, achieving an MSE of 0.076 between simulated and experimental Pearson correlation matrices of membrane potentials. OpenWorm's differentiable backend will enable the same approach on the full 302-neuron network.

Concrete loss function:
```
loss_fc = MSE(simulated_correlation_matrix, randi2023_experimental_matrix)
loss_nt = neurotransmitter_consistency_penalty(polarities, wang2024_identities)
total_loss = loss_fc + lambda_nt * loss_nt
```

The neurotransmitter consistency term constrains the optimizer to respect experimentally determined transmitter identities (Wang et al. 2024, eLife), preventing biologically implausible polarity assignments. This is an improvement over unconstrained optimization.

#### The Existing Starting Point

[DD003](DD003_Body_Physics_Architecture.md)'s compute backends already include a PyTorch solver (`pytorch_solver.py` in Sibernetic). This is the body physics side. The neural circuit side (c302) is locked in NEURON/jNML. Bridging that gap — getting the full [DD001](DD001_Neural_Circuit_Architecture.md)→[DD002](DD002_Muscle_Model_Architecture.md)→[DD003](DD003_Body_Physics_Architecture.md) chain into a single differentiable framework — is the core engineering work.

#### Implementation

**Language/Framework:** PyTorch with `torchdiffeq` (Neural ODE solver). PyTorch chosen over JAX because:

- Sibernetic PyTorch backend already exists
- Larger community, more accessible to contributors
- `torchdiffeq` is mature and well-tested for ODE systems

**Scope:** Reimplement [DD001](DD001_Neural_Circuit_Architecture.md) (neural circuit) + [DD002](DD002_Muscle_Model_Architecture.md) (muscle model) + [DD009](DD009_Intestinal_Oscillator_Model.md) (intestinal oscillator) in PyTorch. [DD003](DD003_Body_Physics_Architecture.md) (SPH body physics) uses the existing PyTorch backend. [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (neuropeptides) and [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx) follow the same pattern when ready.

**Architecture:**

```python
class DifferentiableWorm(torch.nn.Module):
    """Full OpenWorm simulation as a differentiable PyTorch module."""

    def __init__(self, connectome, config):
        super().__init__()
        # [DD001](DD001_Neural_Circuit_Architecture.md): 302 neurons, each with differentiable HH parameters
        self.neurons = NeuralCircuit(
            n_neurons=302,
            connectome=connectome,        # Cook 2019 topology (fixed)
            channel_params=per_class_params,  # Differentiable
            synapse_params=synapse_params,    # Differentiable
        )
        # [DD002](DD002_Muscle_Model_Architecture.md): 95 muscles with calcium-force coupling
        self.muscles = MuscleModel(
            n_muscles=95,
            coupling_params=muscle_params,  # Differentiable
        )
        # [DD009](DD009_Intestinal_Oscillator_Model.md): 20 intestinal cells with IP3/Ca oscillator
        self.intestine = IntestinalOscillator(
            n_cells=20,
            oscillator_params=intestine_params,  # Differentiable
        )

    def forward(self, t, state):
        """ODE right-hand side: same equations as [DD001](DD001_Neural_Circuit_Architecture.md)+[DD002](DD002_Muscle_Model_Architecture.md)+[DD009](DD009_Intestinal_Oscillator_Model.md)."""
        neuron_state, muscle_state, intestine_state = split_state(state)

        d_neuron = self.neurons(t, neuron_state, muscle_state)
        d_muscle = self.muscles(t, muscle_state, neuron_state)
        d_intestine = self.intestine(t, intestine_state, neuron_state)

        return concat(d_neuron, d_muscle, d_intestine)

# Automatic parameter fitting against [DD010](DD010_Validation_Framework.md) validation targets
optimizer = torch.optim.Adam(worm.parameters(), lr=1e-4)
for epoch in range(1000):
    trajectory = odeint(worm, initial_state, time_points)
    loss = dd010_validation_loss(trajectory, experimental_data)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

**Validation criterion:** The differentiable backend must reproduce the reference NEURON/jNML simulation within ±5% on all [DD010](DD010_Validation_Framework.md) metrics when using identical parameters. Only after this equivalence is established can auto-fitting diverge from hand-tuned values.

**Repository location:** `openworm/openworm-ml/differentiable/`

---

### Component 2: Neural Surrogate for SPH Body Physics

#### Problem

[DD003](DD003_Body_Physics_Architecture.md)'s SPH simulation is the speed bottleneck. With ~100K particles and a timestep of 20µs, simulating 200 seconds of biological time takes ~10 hours. This makes:

- CI validation painfully slow ([DD010](DD010_Validation_Framework.md) Tier 3)
- Parameter sweeps impractical (exploring 10 parameter combinations = 100 hours)
- Interactive exploration impossible

#### Solution: Learned Surrogate Model

Train a neural operator (Fourier Neural Operator or DeepONet) that learns the mapping:

```
Input:  Muscle activation time series (95 muscles × T timesteps)
Output: Body trajectory (centroid position + posture angles × T timesteps)
```

The surrogate learns this mapping from a dataset of full SPH simulations. Once trained, it replaces SPH during exploration and parameter sweeps:

```
Full pipeline (today):
  Neural ODEs → Muscle Ca²⁺ → SPH (10 hours) → kinematics
                                ^^^^^^^^^^^
                                bottleneck

Surrogate pipeline:
  Neural ODEs → Muscle Ca²⁺ → Learned Surrogate (30 seconds) → kinematics
                                ^^^^^^^^^^^^^^^^^^
                                1000x faster

Validation pipeline (ground truth):
  Neural ODEs → Muscle Ca²⁺ → Full SPH → kinematics → [DD010](DD010_Validation_Framework.md) Tier 3
```

The full SPH simulation is NEVER discarded — it remains the ground truth for final validation. The surrogate is used for fast iteration.

#### Training Data Generation

Generate a diverse dataset of (muscle_activation, body_trajectory) pairs by running full SPH simulations with:

1. **Nominal activations** from current c302 C1 model (baseline)
2. **Perturbed activations** — scale individual muscle groups by 0.5x-2.0x
3. **Random activations** — sinusoidal patterns at varying frequencies
4. **Single-muscle activations** — one muscle at a time (captures individual muscle contributions)

Target: 500-1000 simulation runs × 5 seconds each = 2,500-5,000 hours of SPH compute (parallelizable across GPUs).

#### Architecture

**Fourier Neural Operator (FNO)** is the recommended architecture:

- Naturally handles time-series → time-series mapping
- Resolution-independent (can train on coarse timesteps, evaluate on fine)
- Well-validated in fluid dynamics applications (weather prediction, turbulence)

```python
from neuraloperator import FNO

surrogate = FNO(
    n_modes=(64,),           # Fourier modes
    in_channels=95,          # 95 muscle activations
    out_channels=7,          # x, y, z centroid + 4 posture angles
    hidden_channels=128,
    n_layers=4,
)

# Train on SPH simulation dataset
for activations, trajectories in training_data:
    predicted = surrogate(activations)
    loss = F.mse_loss(predicted, trajectories)
    loss.backward()
    optimizer.step()
```

#### Accuracy Requirements

| Metric | Requirement | Rationale |
|--------|-------------|-----------|
| Trajectory RMSE | < 5% of body length | Smaller than [DD010](DD010_Validation_Framework.md)'s ±15% acceptance |
| Speed prediction error | < 10% | Must not dominate [DD010](DD010_Validation_Framework.md) error budget |
| Wavelength prediction error | < 10% | Same |
| Generalization to unseen activations | < 15% error | Must handle novel parameter regimes |

**If the surrogate exceeds these error bounds, fall back to full SPH.** The surrogate is advisory, not authoritative.

#### Repository location

`openworm/openworm-ml/surrogate/`

---

### Component 3: Foundation Model → ODE Parameter Pipeline

**Extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (Protein Foundation Model Pipeline for Ion Channel Kinetics).**

Component 3 was promoted from DD017 Phase 3 to a standalone DD in Phase A/Phase 1 because: (1) it derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s uncertain expression→conductance mapping, (2) BioEmu-1 invalidated the original "computationally expensive" objection, and (3) its inputs (WormBase sequences, literature kinetics) have no infrastructure dependencies.

See [DD025](DD025_Protein_Foundation_Model_Pipeline.md) for the full specification including the foundation model table, training data, validation criteria, and implementation roadmap.

**Repository location:** `openworm/openworm-ml/foundation_params/` (unchanged)

---

### Component 4: Learned Sensory Transduction

#### Problem

[DD001](DD001_Neural_Circuit_Architecture.md) explicitly scopes out sensory transduction:

> "Sensory transduction: How mechanosensors, chemosensors, thermosensors convert stimuli to voltage is out of scope. Currently sensory neurons receive generic current injections." ([DD001](DD001_Neural_Circuit_Architecture.md), Boundaries)

This means the worm is "open-loop" — it generates movement but cannot sense or respond to its environment. Without sensory input, behaviors like chemotaxis (navigating toward food), thermotaxis (navigating toward preferred temperature), and touch avoidance are impossible.

Building mechanistic models of the full transduction cascade (stimulus → receptor → G-protein → second messenger → ion channel modulation → voltage) for all sensory modalities would require years of work and data that largely doesn't exist.

#### Solution: Learned Sensory Front-End

Train a model on published sensory neuron calcium imaging data to learn the mapping from stimulus → sensory neuron response, without modeling the intermediate biochemistry:

```
Environment stimulus → Learned Sensory Model → Current injection on sensory neurons → [DD001](DD001_Neural_Circuit_Architecture.md) ODE circuit
```

This is a **learned boundary condition** — a standard technique in hybrid modeling. The rest of the circuit ([DD001](DD001_Neural_Circuit_Architecture.md) interneurons, [DD002](DD002_Muscle_Model_Architecture.md) muscles, [DD003](DD003_Body_Physics_Architecture.md) body physics) remains mechanistic.

#### Available Training Data

| Sensory Modality | Neurons | Data Source | Format |
|-----------------|---------|-------------|--------|
| Mechanosensation (touch) | ALM, AVM, PLM, PVD | Chalfie lab, Suzuki 2003 | Ca²⁺ traces in response to calibrated touch |
| Chemosensation (NaCl) | ASEL, ASER | Suzuki 2008, Luo 2014 | Ca²⁺ traces in response to concentration steps |
| Thermosensation | AFD, AIY, AIZ | Mori & Ohshima 1995, Clark 2006 | Ca²⁺ traces in response to temperature ramps |
| Olfaction | AWC, AWA | Chalasani 2007 | Ca²⁺ traces in response to odor pulses |
| Nociception | ASH, PVD | Hilliard 2005 | Ca²⁺ traces in response to harsh stimuli |

#### Architecture

A small recurrent network (GRU or LSTM) per sensory modality:

```python
class SensoryTransducer(torch.nn.Module):
    """Learns stimulus → sensory neuron current injection."""

    def __init__(self, n_sensory_neurons, stimulus_dim):
        super().__init__()
        self.rnn = torch.nn.GRU(
            input_size=stimulus_dim,
            hidden_size=64,
            num_layers=2,
            batch_first=True,
        )
        self.output = torch.nn.Linear(64, n_sensory_neurons)

    def forward(self, stimulus_timeseries):
        """
        Input:  stimulus (batch, time, stimulus_dim)
                e.g., temperature at worm's head over time
        Output: current injection per sensory neuron (batch, time, n_neurons)
                e.g., I_ext for AFD, AIY, AIZ at each timestep
        """
        hidden, _ = self.rnn(stimulus_timeseries)
        I_ext = self.output(hidden)
        return I_ext

# Example: thermotaxis
thermo_transducer = SensoryTransducer(n_sensory_neurons=3, stimulus_dim=1)
# Train on Clark 2006 data: temperature ramp → AFD/AIY/AIZ calcium
# Output feeds into [DD001](DD001_Neural_Circuit_Architecture.md) as I_ext on sensory neurons
```

#### Closed-Loop Integration

With learned sensory transduction, the simulation becomes closed-loop:

```
1. SPH body physics computes worm position in environment
2. Environment model computes local stimulus at worm's position
   (e.g., temperature gradient, chemical concentration)
3. Learned sensory model converts stimulus → I_ext on sensory neurons
4. [DD001](DD001_Neural_Circuit_Architecture.md) neural circuit processes sensory input → motor output
5. [DD002](DD002_Muscle_Model_Architecture.md) muscles contract → [DD003](DD003_Body_Physics_Architecture.md) body moves → back to step 1
```

This enables emergent behaviors: chemotaxis, thermotaxis, and touch avoidance arise from the interaction of learned sensory input with the mechanistic circuit.

#### Validation

- **Stimulus-response curves:** Predicted sensory neuron responses must match published dose-response curves (e.g., ASER response to NaCl step decreases)
- **Emergent behavior:** With thermosensory model enabled, the simulated worm should perform thermotaxis (navigate toward cultivation temperature). Compare to Mori & Ohshima 1995 behavioral data.
- **Ablation consistency:** Ablating (silencing) a sensory neuron in the model should reproduce the behavioral deficit observed experimentally

#### Repository location

`openworm/openworm-ml/sensory/`

---

## Alternatives Considered

### 1. Replace ODEs Entirely with a Data-Driven Transformer

**Description:** Train a large transformer on tokenized neural activity and behavioral data to directly predict whole-nervous-system dynamics, bypassing biophysical ODEs entirely. Recent work shows this approach can predict *C. elegans* behavior from whole-brain activity with near-zero error when trained on sufficient data (Azabou et al. 2023). Digital twin approaches have shown promise in simulating individual neuron responses in other systems (Cobos et al. 2022).

**Rejected because:**

- Destroys mechanistic interpretability — OpenWorm's core value. A transformer can predict *what* will happen but cannot explain *why* in terms of biophysical mechanisms
- Would match [DD010](DD010_Validation_Framework.md) Tier 3 (behavior) but fail Tier 1, 2, and 4 (electrophysiology, connectivity, causal intervention predictions)
- Cannot predict behavior under truly novel perturbations (new mutations, new drug targets) that fall outside the training distribution. Mechanistic models generalize by construction to any condition expressible in the ODE system
- The training data requirements (thousands of whole-brain recordings during perturbation) are not yet publicly available, though they are being collected by multiple labs (Haspel et al. 2023)
- Would make OpenWorm a black-box prediction engine, eliminating its unique positioning as a causally interpretable whole-organism model

**Complementary role:** Pure data-driven models will be powerful tools for benchmarking. If a transformer trained on perturbation data makes predictions that disagree with our mechanistic model, the disagreement itself identifies where the mechanistic model needs improvement. OpenWorm's hybrid approach (this DD) and a pure data-driven model are complementary, not competing.

### 2. Physics-Informed Neural Networks (PINNs) as Primary Solver

**Description:** Use neural networks constrained by the ODE residuals to approximate solutions, rather than traditional ODE solvers.

**Rejected (for now) because:**

- PINNs struggle with stiff ODE systems (which HH equations are — fast channel kinetics + slow calcium dynamics)
- Training stability is poor for coupled multi-scale systems
- Traditional ODE solvers (CVODE, RK45) are fast and reliable for our system size
- PINNs shine for PDEs in high dimensions, not for our ~1000-variable ODE system

**When to reconsider:** If the differentiable ODE solver approach proves too slow for the full 302-neuron system.

### 3. Graph Neural Networks for the Connectome

**Description:** Replace the explicit ODE-per-neuron approach with a GNN that operates on the connectome graph structure.

**Deferred because:**

- Promising research direction (Bhatt et al. 2024 applied GNNs to C. elegans connectome)
- Could be more parameter-efficient than 302 separate ODE systems
- But loses per-neuron biophysical interpretability
- Better suited as a future Component 5 if Components 1-4 prove insufficient

### 4. Do Nothing (Stay Pure ODE)

**Rejected because:**

- Manual parameter fitting will not scale to 959 cells (the whole-organism goal)
- Simulation speed is already a bottleneck blocking CI and iteration
- The sensory front-end gap prevents closed-loop behavior
- Competing projects (CZI, Arc) are using ML — OpenWorm needs to engage with these tools, not ignore them

---

## Quality Criteria

### For the Differentiable Backend (Component 1)

1. **Equivalence test:** With identical parameters, the differentiable backend must match the NEURON/jNML reference simulation within ±5% on all state variables (V, Ca, activation) at all timesteps.

2. **Gradient correctness:** Gradients must be verified against finite-difference approximations for a subset of parameters. Relative error < 1%.

3. **Auto-fitted parameters must be physical:** After gradient-descent fitting, all parameters must remain within biologically plausible ranges:
    - Conductances: 0 < g < 100 mS/cm²
    - Reversal potentials: -100 < E_rev < +80 mV
    - Time constants: 0.01 < tau < 10,000 ms
    - Calcium concentrations: > 0

4. **[DD010](DD010_Validation_Framework.md) validation improvement:** Auto-fitted parameters must produce [DD010](DD010_Validation_Framework.md) scores equal to or better than hand-tuned parameters.

### For the SPH Surrogate (Component 2)

1. **Speed:** Surrogate must be at least 100x faster than full SPH. Target: 1000x.
2. **Accuracy:** Trajectory prediction error < 5% of body length on held-out test set.
3. **Fail-safe:** If surrogate error exceeds 15% on any metric, automatically fall back to full SPH with a warning.

### For the Foundation Model Pipeline (Component 3)

**Extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md).** See DD025 Quality Criteria for cross-validation and end-to-end validation requirements.

### For the Sensory Model (Component 4)

1. **Stimulus-response match:** Predicted sensory neuron responses within ±20% of published calcium imaging data.
2. **Behavioral emergence:** At least one emergent behavior (chemotaxis, thermotaxis, or touch avoidance) must qualitatively match experimental observations when sensory model is enabled.

### DCell Validation: Visible Neural Networks as Independent Check

**[DCell](https://github.com/idekerlab/DCell)** (Ideker Lab, UCSD) is a "visible neural network" that embeds the Gene Ontology hierarchy into its architecture — each node in the network corresponds to a biological subsystem, and the connections mirror known biological relationships. It predicts yeast cell growth phenotypes from genotype with interpretable intermediate states.

This is conceptually the same approach OpenWorm takes: making the computational structure mirror biological structure, so internal states are interpretable as biological quantities. DCell provides a key validation strategy for the hybrid ML framework:

#### The DCell Cross-Validation Protocol

1. **Build a *C. elegans* DCell:** Adapt DCell's architecture to use the *C. elegans* Gene Ontology (or a simplified version using the 128 neuron classes from [DD005](DD005_Cell_Type_Differentiation_Strategy.md) as nodes). Train on genotype → behavioral phenotype data (e.g., mutant locomotion phenotypes from WormBase)

2. **Compare predictions:** For each genetic perturbation (ablation, RNAi knockdown, gain-of-function):
   - Run the OpenWorm mechanistic simulation → predict behavioral change
   - Run the *C. elegans* DCell → predict behavioral change
   - Compare both against experimental data

3. **Interpret disagreements:**
   - **Both agree with experiment:** Mutual validation — the mechanism is captured by both approaches
   - **OpenWorm correct, DCell wrong:** The mechanistic detail adds value that a data-driven model misses
   - **DCell correct, OpenWorm wrong:** The mechanistic model has a structural error (wrong connectivity, missing pathway) that DCell's data-driven approach bypasses
   - **Both wrong:** Missing biology in both models

This provides a fundamentally different validation signal from [DD010](DD010_Validation_Framework.md)'s tier-based approach. DD010 checks "does the output match data?" DCell cross-validation checks "does the *structure* of the model match the *structure* of the biology?" — a deeper test of mechanistic correctness.

#### Why This Matters for the Hybrid Framework

When DD017's ML components fill mechanistic gaps (e.g., learned sensory transduction, surrogate body physics), DCell cross-validation can detect whether the ML component has learned the *right* biological structure or just fitted the training data. If a surrogate model gets the right behavioral output but DCell reveals the wrong intermediate pathway is active, the surrogate has overfit.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| HH equations and parameters (reference) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md) | All ODE parameters | NeuroML XML (parsed) | mixed |
| Connectome topology | [DD001](DD001_Neural_Circuit_Architecture.md) (ConnectomeToolbox) | Adjacency matrices | Python API / CSV | Neuron pairs + weights |
| CeNGEN expression data | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Per-class transcript levels | CSV | TPM |
| Ion channel gene sequences | WormBase — see [DD025](DD025_Protein_Foundation_Model_Pipeline.md) | Protein sequences | FASTA | amino acids |
| SPH simulation dataset (for surrogate training) | [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic) | (muscle_activation, trajectory) pairs | HDF5 | mixed |
| Sensory neuron calcium imaging data | [DD008](DD008_Data_Integration_Pipeline.md) / published papers | (stimulus, calcium_response) pairs | CSV | µM, °C, mM |
| [DD010](DD010_Validation_Framework.md) validation targets | [DD010](DD010_Validation_Framework.md) | Experimental baselines | NumPy / CSV | mixed |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Auto-fitted ODE parameters | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md) | Per-neuron-class conductances, time constants | YAML / JSON parameter file | mixed |
| SPH surrogate predictions | [DD010](DD010_Validation_Framework.md) (fast validation) | Body trajectory | WCON-compatible | µm |
| Predicted channel kinetics | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Per-channel HH parameters — see [DD025](DD025_Protein_Foundation_Model_Pipeline.md) | YAML | mV, ms, mS/cm² |
| Sensory current injections | [DD001](DD001_Neural_Circuit_Architecture.md) | Per-sensory-neuron I_ext(t) | Time series (PyTorch tensor) | nA |
| Gradient information | Internal | ∂(validation_loss) / ∂(parameter) | PyTorch .grad tensors | mixed |

### Configuration (`openworm.yml` Section)

```yaml
ml:
  # Component 1: Differentiable backend
  differentiable_backend: false    # Use PyTorch ODE solver instead of NEURON
  auto_fit:
    enabled: false                 # Run gradient descent parameter fitting
    target_metrics:                # [DD010](DD010_Validation_Framework.md) validation targets to optimize
      - tier2_functional_connectivity
      - tier3_speed
      - tier3_wavelength
      - tier3_defecation_period
    max_epochs: 1000
    learning_rate: 1e-4
    parameter_bounds: "configs/parameter_bounds.yml"  # Physical constraints

  # Component 2: SPH surrogate
  sph_surrogate: false             # Use learned surrogate instead of full SPH
  surrogate_model: "models/sph_surrogate_v1.pt"
  surrogate_fallback_threshold: 0.15  # Fall back to SPH if error > 15%

  # Component 3: Foundation model parameters — see DD025 for full specification
  foundation_params: false         # Use ESM/AlphaFold-predicted channel kinetics (DD025)
  esm_model: "esm2_t33_650M"      # DD025
  kinetics_predictor: "models/channel_kinetics_v1.pt"  # DD025

  # Component 4: Learned sensory model
  sensory_model: "generic"         # "generic" (current I_ext injection), "learned"
  sensory_checkpoint: "models/sensory_transducer_v1.pt"
  sensory_modalities:
    - thermosensation
    - mechanosensation
    - chemosensation_nacl
```

### Docker Build

- **Repository:** `openworm/openworm-ml` (new)
- **Docker stage:** `ml` in multi-stage Dockerfile (extends `neural` stage)
- **Build dependencies:** `pip install torch torchdiffeq neuraloperator esm`
- **GPU requirement:** NVIDIA GPU strongly recommended for surrogate training and auto-fitting. CPU fallback available but 10-50x slower.
- **Model checkpoints:** Pre-trained models stored in GitHub Releases or Hugging Face Hub (too large for git)

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| HH equations | [DD001](DD001_Neural_Circuit_Architecture.md) | If channel model equations change, differentiable backend must be updated to match |
| Muscle model | [DD002](DD002_Muscle_Model_Architecture.md) | If calcium-force coupling changes, differentiable chain breaks |
| SPH output format | [DD003](DD003_Body_Physics_Architecture.md) | If trajectory format changes, surrogate training data pipeline breaks |
| CeNGEN data | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | If expression data versioning changes, foundation model predictions change |
| Validation criteria | [DD010](DD010_Validation_Framework.md) | If acceptance criteria change, auto-fitting loss function must be updated |
| Simulation stack (Docker) | [DD013](DD013_Simulation_Stack_Architecture.md) | If Docker compose structure changes, `ml-test` service must be updated |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Neural circuit (if using auto-fit params) | [DD001](DD001_Neural_Circuit_Architecture.md) | If auto-fitted parameters change (retrained model), simulation behavior changes |
| Cell-type specialization (if using foundation params) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | If predicted conductances change, per-class models change |
| Validation (if using surrogate for fast validation) | [DD010](DD010_Validation_Framework.md) | If surrogate accuracy degrades, false-positive validation passes possible |
| All subsystems (if sensory model changes) | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md) | Sensory input changes → neural dynamics change → everything downstream changes |

---

## Implementation Roadmap

### Phase A: Differentiable Backend (Weeks 1-8)

1. **Week 1-2:** Port [DD001](DD001_Neural_Circuit_Architecture.md) HH equations to PyTorch (single neuron)
2. **Week 3-4:** Port [DD002](DD002_Muscle_Model_Architecture.md) muscle model, couple to neural circuit
3. **Week 5-6:** Port [DD009](DD009_Intestinal_Oscillator_Model.md) intestinal oscillator
4. **Week 7-8:** Equivalence testing against NEURON/jNML reference. Must match within ±5%.

**Milestone:** `DifferentiableWorm` module passes all [DD010](DD010_Validation_Framework.md) validation tests.

### Phase B: Auto-Fitting (Weeks 9-12)

1. **Week 9-10:** Implement [DD010](DD010_Validation_Framework.md) validation loss function in PyTorch
2. **Week 11-12:** Run gradient descent to find per-neuron-class parameters
3. **Deliverable:** New parameter set that equals or improves on hand-tuned [DD010](DD010_Validation_Framework.md) scores

### Phase C: SPH Surrogate (Weeks 9-16, parallel with Phase B)

1. **Week 9-12:** Generate training dataset (500+ SPH simulation runs)
2. **Week 13-14:** Train FNO surrogate
3. **Week 15-16:** Validate surrogate accuracy, integrate into pipeline

**Milestone:** Full simulation loop with surrogate runs in < 1 minute.

### Phase D: Foundation Model Pipeline

**Extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md) and moved to Phase A/Phase 1.** See DD025 Implementation Roadmap for the detailed timeline (~20 hours Phase A, ~12 hours Phase 1).

### Phase E: Sensory Transduction (Weeks 25-32)

1. **Week 25-28:** Curate training data from published calcium imaging
2. **Week 29-30:** Train sensory transduction models (one per modality)
3. **Week 31-32:** Close the loop — demonstrate emergent chemotaxis or thermotaxis

---

## Boundaries (Explicitly Out of Scope)

1. **Replacing the mechanistic core:** ML is used at boundaries, not as the primary model. The HH ODEs, SPH physics, and calcium dynamics remain the source of truth.

2. **Whole-organism foundation model:** We are not building a foundation model for C. elegans. We are building a mechanistic model that uses existing foundation models (ESM3, AlphaFold) as tools.

3. **Real-time simulation:** The surrogate enables fast iteration but not real-time interactive simulation (which would require <16ms per frame). That is a separate engineering project.

4. **Generative models:** We are not generating synthetic worm behavior or synthetic electrophysiology data. All ML outputs serve the mechanistic simulation.

5. **Hardware-specific optimization:** This DD specifies the ML architecture and algorithms. GPU kernel optimization, distributed training, and hardware-specific tuning are implementation details.

### Existing Code Resources

**CE_locomotion** ([openworm/CE_locomotion](https://github.com/openworm/CE_locomotion), active 2026, collaboration with Olivares & Beer):
Complete C++ neuromechanical model with evolutionary algorithm for parameter fitting (auto-tunes parameters to produce forward/backward locomotion). Compare to DD017 Component 1's gradient descent approach; a hybrid strategy (evolutionary global search + gradient local refinement) may be optimal.

**CyberElegans** ([openworm/CyberElegans](https://github.com/openworm/CyberElegans), 2016, 36 stars):
Alternative neuromechanical model. Useful as a benchmark comparison for DD017's SPH surrogate and for learning from different architectural trade-offs.

**bionet** ([openworm/bionet](https://github.com/openworm/bionet), 2015, 32 stars):
"Artificial biological neural network" — check for reusable neural network architectures or training pipelines applicable to DD017 Component 2 (SPH surrogate) or Component 4 (learned sensory transduction).

**simple-C-elegans** ([openworm/simple-C-elegans](https://github.com/openworm/simple-C-elegans), 2020):
Minimalist Python model based on OpenWorm and published literature. Possible starting point for DD017 Component 1 (differentiable backend) — simpler than full c302 for initial prototyping.

**wormvae** ([openworm/wormvae](https://github.com/openworm/wormvae), 2022):
Connectome-constrained Variational Autoencoder (ICLR 2022). Directly relevant to Component 2 (SPH surrogate) and Component 4 (sensory transduction) as a pre-trained latent representation of worm dynamics.

**wormpose** ([openworm/wormpose](https://github.com/openworm/wormpose), 2025):
Image synthesis and CNNs for *C. elegans* pose estimation. Provides labeled (stimulus, posture) pairs that could augment sensory transduction training data for Component 4.

**CelegansNeuromechanicalGaitModulation** ([openworm/CelegansNeuromechanicalGaitModulation](https://github.com/openworm/CelegansNeuromechanicalGaitModulation), 2025):
Neuromechanical gait modulation model with muscle activation patterns. Training data source for Component 2 (SPH surrogate) or benchmark for Component 1 (differentiable backend).

**multi-dev-sibernetic** ([openworm/multi-dev-sibernetic](https://github.com/openworm/multi-dev-sibernetic), 2023):
Multi-device Sibernetic engine. Useful for bulk generation of the 500-1000 SPH simulation runs needed for Component 2 surrogate training.

---

## References

1. **Chen RT, Rubanova Y, Bettencourt J, Duvenaud D (2018).** "Neural Ordinary Differential Equations." *NeurIPS 2018.*
   *Foundational paper on differentiable ODE solvers.*

2. **Li Z, Kovachki N, Azizzadenesheli K, et al. (2020).** "Fourier Neural Operator for Parametric Partial Differential Equations." *ICLR 2021.*
   *FNO architecture for surrogate models.*

3. **Lin Z, Akin H, Rao R, et al. (2023).** "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science* 379:1123-1130.
   *ESM2/ESM3 protein language model.*

4. **Randi F et al. (2023).** "Neural signal propagation atlas." *Nature* 623:406-414.
   *Whole-brain calcium imaging data for circuit validation.*

5. **Jumper J et al. (2021).** "Highly accurate protein structure prediction with AlphaFold." *Nature* 596:583-589.
   *Structure prediction for channel kinetics pipeline.*

6. **Bhatt D et al. (2024).** "Graph Neural Networks for C. elegans Connectome Modeling." *Preprint.*
   *GNN approach to connectome-based neural simulation.*

7. **Rackauckas C et al. (2020).** "Universal Differential Equations for Scientific Machine Learning." *arXiv:2001.04385.*
   *Hybrid mechanistic-ML framework theory.*

8. **Kidger P (2022).** "On Neural Differential Equations." *PhD Thesis, University of Oxford.*
   *Comprehensive treatment of neural ODEs and differentiable simulation.*

9. **Kochkov D et al. (2024).** "Neural General Circulation Models for Weather and Climate." *Nature* 632:1060-1066.
   *Precedent for learned surrogates in physical simulation (Google DeepMind).*

10. **Azabou M, Arora V, Ganesh V, et al. (2023).** "A Unified, Scalable Framework for Neural Population Decoding." *arXiv*.
    *Demonstrates transformer-based prediction of behavior from whole-brain neural activity — relevant as a benchmark for the mechanistic approach and as evidence that data-driven digital twins are feasible for C. elegans.*

11. **Cobos E, Muhammad T, Fahey PG, et al. (2022).** "It takes neurons to understand neurons: Digital twins of visual cortex synthesize neural metamers." *bioRxiv*:2022.12.09.519708.
    *Data-driven digital twin approach — complementary to (not replacing) mechanistic modeling.*

12. **Haspel G et al. (2023).** "To reverse engineer an entire nervous system." *arXiv* [q-bio.NC] 2308.06578.
    *White paper arguing for observational and perturbational completeness — the scale of data collection proposed would enable both mechanistic and data-driven approaches to C. elegans neural simulation.*

13. **Zhao M et al. (2024).** *Nat Comp Sci* 4:978-990.
    *Demonstrated differentiable optimization of synaptic weights and polarities for a 136-neuron C. elegans locomotion circuit.*

---

- **Approved by:** Pending
- **Implementation Status:** Proposed
- **Next Actions:**

1. Create `openworm/openworm-ml` repository
2. Port [DD001](DD001_Neural_Circuit_Architecture.md) single-neuron HH model to PyTorch (Phase A, Week 1)
3. Verify equivalence against NEURON/jNML reference
4. Begin SPH surrogate training data generation (Phase C, can start in parallel)
