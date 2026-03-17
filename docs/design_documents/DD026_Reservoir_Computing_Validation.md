# DD026: Reservoir Computing Validation of the C. elegans Nervous System

- **Status:** Proposed (Phase 2)
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-23
- **Supersedes:** None
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization), [DD010](DD010_Validation_Framework.md) (Validation Framework), [DD019](DD019_Closed_Loop_Touch_Response.md) (Touch Response), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (Connectome Data Access), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) (Environment)

---

> **Phase:** [Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6) (Months 4-6) | **Layer:** Analysis / Validation

## TL;DR

Tests whether the 302-neuron *C. elegans* connectome functions as a **reservoir computer** — a fixed recurrent network where only a linear output readout is trained — by measuring 5 key RC properties across 4 neuron partitioning schemes. Defines **falsifiable predictions**: if any RC property fails measurably, the reservoir computing framing is rejected. Either outcome (confirmed or falsified) is scientifically valuable and advances understanding of how the connectome transforms sensory input into motor output.

---

## Goal & Success Criteria

**Goal:** Determine whether the simulated *C. elegans* nervous system can be formally characterized as a reservoir computer by measuring five quantitative RC properties and training linear readouts across four neuron partitioning schemes.

| Criterion | Target | Phase | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|-------|------------|
| **Primary:** Linear readout R² | R² ≥ 0.5 predicting motor output from reservoir state under at least one partition | Phase 2 | Tier 2a (advisory, non-blocking) |
| **Secondary:** All 5 RC properties tested | Quantitative results for all 5 predictions × 4 partitions (20 tests total) | Phase 2 | Non-blocking |
| **Tertiary:** Cross-partition robustness | RC framing holds (or fails) consistently across ≥3 of 4 partitions | Phase 2 | Non-blocking |

**Success = all 5 predictions tested across all 4 partitions with quantitative results documented.** The DD succeeds whether it confirms or falsifies the RC framing. A clear falsification is as valuable as confirmation — it constrains what computational framework *does* apply.

---

## Motivation

### Why Reservoir Computing?

The *C. elegans* connectome has properties suggestive of a reservoir computer:

1. **Fixed recurrent connectivity:** The synaptic wiring diagram is genetically determined and does not change during the animal's lifetime (no synaptic plasticity in the mammalian sense)
2. **High recurrence:** Dense recurrent connections among interneurons — the connectome is far from feedforward
3. **Sensory→motor transformation:** 80 sensory neurons project through ~100 interneurons to ~113 motor neurons — a natural input→reservoir→readout architecture
4. **Nonlinear dynamics:** Hodgkin-Huxley neurons with graded potentials provide the nonlinear transformation RC requires

### Why Falsifiable Predictions?

RC is a *framework*, not a fact. The connectome might not satisfy RC requirements — and that would be equally informative. We define 5 quantitative predictions that, if violated, reject the RC framing. This avoids the trap of fitting an RC model post hoc and claiming success.

### Key Reference

[Yan et al. 2024](https://doi.org/10.1038/s41467-024-49498-x) demonstrated reservoir computing in biological neural networks, showing that fixed recurrent networks can perform computation through their transient dynamics. DD026 tests whether this framework applies to the specific case of the *C. elegans* connectome as simulated by OpenWorm.

---

## Background: Reservoir Computing Primer

A **reservoir computer** consists of three components:

```
Input (u) ──→ Reservoir (x) ──→ Readout (y)
   W_in          W_res (fixed)       W_out (trained)
```

1. **Input layer (W_in):** Projects external signals into the reservoir. Not trained.
2. **Reservoir (W_res):** A fixed, recurrent nonlinear dynamical system. Not trained. Its role is to project input into a high-dimensional state space where different inputs become linearly separable.
3. **Readout (W_out):** A linear mapping from reservoir state to output. **This is the only trained component.**

**Key insight:** If a network is a good reservoir, a simple linear readout suffices to extract computation. If a nonlinear readout dramatically outperforms a linear one, the computation is *not* being done by the reservoir — the readout is doing the heavy lifting, and the RC framing is wrong.

### Five Properties of a Good Reservoir

1. **Echo State Property (ESP):** The reservoir's state depends only on recent input history, not on initial conditions. Two trajectories starting from different states must converge.

2. **Fading Memory:** The reservoir retains information about past inputs for a finite time, then forgets. Memory capacity (MC) quantifies how many past timesteps can be linearly decoded.

3. **Separation Property:** Different input patterns produce distinguishable reservoir states. If two distinct inputs map to the same reservoir state, the reservoir cannot separate them.

4. **Linear Readout Sufficiency:** A linear mapping from reservoir state to desired output achieves good performance. This is the whole point — the reservoir does the nonlinear computation, the readout is linear.

5. **Nonlinear Readout Non-Superiority:** A nonlinear readout should not *dramatically* outperform the linear one. If it does, the reservoir is not performing the computation — the readout is.

---

## Neuron Partitioning Schemes

The RC framework requires partitioning neurons into input, reservoir, and readout. For *C. elegans*, the "correct" partition is unknown — so we test 4 schemes as a sensitivity analysis.

### Partition A: Canonical (Anatomical Classification)

| Role | Neurons | Count | Rationale |
|------|---------|-------|-----------|
| **Input** | Sensory neurons (amphid, phasmid, etc.) | ~80 | Natural sensory layer |
| **Reservoir** | Interneurons | ~100 | Recurrent processing layer |
| **Readout** (trained W_out) | Motor neurons (body wall, head, pharyngeal) | ~113 | Natural output layer |

**Rationale:** Follows standard anatomical classification from [Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7). Uses `cect` API ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) neuron classification.

### Partition B: Whole-Nervous-System Reservoir

| Role | Neurons | Count | Rationale |
|------|---------|-------|-----------|
| **Input** | External stimuli only (not neurons) | 0 neurons | Sidesteps partition problem |
| **Reservoir** | ALL 302 neurons | 302 | Entire nervous system as reservoir |
| **Readout** (trained W_out) | Motor neuron subset (linear decoder) | ~113 (decoded, not partitioned out) | Trained to predict motor activation |

**Rationale:** Avoids the arbitrary neuron classification problem. Treats the entire nervous system as the reservoir, with external stimuli (touch, chemical gradients) as input. The readout is a trained linear decoder applied to all 302 neuron states.

### Partition C: Minimal Readout (Ventral Cord Only)

| Role | Neurons | Count | Rationale |
|------|---------|-------|-----------|
| **Input** | Sensory neurons | ~80 | Natural sensory layer |
| **Reservoir** | Interneurons | ~100 | Recurrent processing layer |
| **Readout** (trained W_out) | Ventral cord motor neurons (VA/VB/DA/DB/DD/VD classes) | ~23 | Cleanest motor output |

**Rationale:** Excludes head and pharyngeal motor neurons, which have complex local circuits. Ventral cord motor neurons are the most direct drivers of locomotion — the cleanest readout layer.

### Partition D: Command Neuron Bottleneck

| Role | Neurons | Count | Rationale |
|------|---------|-------|-----------|
| **Input** | Sensory neurons | ~80 | Natural sensory layer |
| **Reservoir** | Non-command interneurons | ~90 | Bulk processing layer |
| **Readout** (trained W_out) | Command interneurons (AVA, AVB, AVD, AVE, PVC) | 5 | Natural bottleneck |

**Rationale:** The 5 command interneurons form a well-known decision bottleneck between sensory processing and motor execution. If the nervous system is an RC, the command neurons might be the natural readout layer — they compress the reservoir state into a forward/reverse decision.

### Cross-Partition Analysis

All 5 RC properties are tested under each partition. Results are reported in a 5×4 matrix:

|  | Partition A | Partition B | Partition C | Partition D |
|--|-------------|-------------|-------------|-------------|
| ESP | pass/fail | pass/fail | pass/fail | pass/fail |
| Memory Capacity | MC value | MC value | MC value | MC value |
| Separation | ratio | ratio | ratio | ratio |
| Linear R² | value | value | value | value |
| Nonlinear ratio | ratio | ratio | ratio | ratio |

**Interpretation:**

- **RC holds across all 4 partitions:** Strong evidence the connectome is a reservoir computer. The framing is robust to partition choice.
- **RC holds under some but not all:** The framing is fragile — it depends on how you carve up the network. Itself an interesting finding.
- **RC fails under all 4:** The connectome is not a reservoir computer. The computation is distributed in a way that RC does not capture.

---

## Five Falsifiable Predictions

Each prediction defines a **quantitative threshold**. If the threshold is violated, the prediction is falsified. All predictions are tested per partition.

### Prediction 1: Echo State Property (ESP)

**Claim:** The reservoir forgets initial conditions — two trajectories starting from different states converge to the same trajectory when driven by the same input.

**Test Protocol:**

1. Initialize the reservoir in state **x₀** (resting state)
2. Drive with input sequence **u(t)** for 10 seconds of simulated time
3. Record reservoir state trajectory **x₁(t)**
4. Re-initialize in a different state **x₀'** (random perturbation, ±50% of resting values)
5. Drive with the *same* input sequence **u(t)** for 10 seconds
6. Record trajectory **x₂(t)**
7. Compute normalized distance: `d(t) = ||x₁(t) - x₂(t)|| / ||x₁(0) - x₂(0)||`

**Falsification criterion:** If `d(10s) > 0.10` (distance remains above 10% of initial distance after 10 seconds), ESP fails. The reservoir retains memory of initial conditions — it is not a proper echo state network.

**Repeat:** 10 random initial perturbations; report mean and std of `d(10s)`.

### Prediction 2: Fading Memory Capacity

**Claim:** The reservoir retains information about past inputs and this information can be linearly decoded.

**Test Protocol:**

1. Drive reservoir with white noise input **u(t)** for 100 seconds
2. Record reservoir state **x(t)** at each timestep
3. For each delay τ = 1, 2, ..., 100 timesteps:
    - Train a ridge regression from **x(t)** to **u(t-τ)**
    - Compute R²(τ) = correlation² between predicted and actual past input
4. Memory capacity: `MC = Σ_τ R²(τ)`

**Falsification criterion:** If MC < 5 (less than 2% of network size for the ~100-neuron interneuron reservoir, or ~1.7% for 302 neurons), the reservoir has negligible memory. It cannot hold enough past information for meaningful computation.

**Context:** Theoretical maximum MC equals reservoir size (N neurons → MC ≤ N). Good reservoirs achieve MC ≈ 0.1N to 0.5N. MC < 5 indicates the network is either too chaotic (forgets instantly) or too stable (doesn't respond to input).

### Prediction 3: Separation Property

**Claim:** Different input patterns produce distinguishable reservoir states.

**Test Protocol:**

1. Generate 100 pairs of input patterns:
    - **Similar pairs:** Two Gaussian noise sequences correlated at r=0.9
    - **Different pairs:** Two uncorrelated Gaussian noise sequences
2. For each pair, drive the reservoir and record final state vectors
3. Compute within-pair distances for similar and different inputs
4. Separation ratio: `SR = mean_distance(different) / mean_distance(similar)`

**Falsification criterion:** If SR < 2.0, the reservoir does not meaningfully separate different inputs. Similar and different inputs produce nearly indistinguishable states — the reservoir is not expanding the input space.

### Prediction 4: Linear Readout Adequacy

**Claim:** A linear mapping from reservoir state to motor output achieves reasonable performance.

**Test Protocol:**

1. Run simulation with naturalistic input (e.g., [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) gradient + [DD019](DD019_Closed_Loop_Touch_Response.md) touch stimuli) for 60 seconds
2. Record reservoir neuron states **X** (time × reservoir neurons matrix)
3. Record readout neuron states **Y** (time × readout neurons matrix) — this is the ground truth
4. Train ridge regression: **Y_pred = X · W_out** (with cross-validation for regularization)
5. Compute R² = 1 - ||Y - Y_pred||² / ||Y - mean(Y)||²

**Falsification criterion:** If R² < 0.3, the linear readout cannot predict motor output from reservoir state. The reservoir is not projecting input into a space where output is linearly accessible.

**Note:** R² ≥ 0.5 is the primary success criterion. R² between 0.3 and 0.5 is a "weak RC" — the framing partially holds but is not strong.

### Prediction 5: Nonlinear Readout Non-Superiority

**Claim:** A nonlinear readout does not dramatically outperform the linear one. The computation is in the reservoir, not the readout.

**Test Protocol:**

1. Using the same data from Prediction 4
2. Train a 2-layer MLP (64 hidden units, ReLU) from reservoir states to readout states
3. Compute R²_MLP
4. Compute ratio: `R²_MLP / R²_linear`

**Falsification criterion:** If `R²_MLP / R²_linear > 2.0`, the nonlinear readout is dramatically better. This means the reservoir is *not* doing the computation — a nonlinear decoder is needed to extract the mapping, which contradicts the RC framework.

**Context:** In a good reservoir, R²_MLP / R²_linear should be close to 1.0 (≤1.5). If the ratio exceeds 2.0, the reservoir is not creating a linearly separable representation.

---

## Deliverables

| Artifact | Path | Format | Status |
|----------|------|--------|--------|
| RC analysis orchestrator | `validation/reservoir_computing/rc_analysis.py` | Python | `[TO BE CREATED]` |
| RC metrics library | `validation/reservoir_computing/rc_metrics.py` | Python | `[TO BE CREATED]` |
| Linear/nonlinear readout training | `validation/reservoir_computing/rc_readout.py` | Python | `[TO BE CREATED]` |
| Neuron partition definitions | `validation/reservoir_computing/rc_partitions.py` | Python | `[TO BE CREATED]` |
| Jupyter notebook (analysis + figures) | `validation/reservoir_computing/RC_Validation.ipynb` | Jupyter | `[TO BE CREATED]` |
| JSON validation report | `validation/reservoir_computing/rc_validation_report.json` | JSON | `[TO BE CREATED]` |
| openworm.yml config section | (within `openworm.yml`) | YAML | `[TO BE CREATED]` |

### Report Schema (`rc_validation_report.json`)

```json
{
  "dd026_version": "1.0",
  "timestamp": "2026-09-XX",
  "simulation_config": {
    "duration_seconds": 60,
    "input_type": "naturalistic",
    "connectome_dataset": "Cook2019"
  },
  "partitions": {
    "A_canonical": {
      "input_count": 80,
      "reservoir_count": 100,
      "readout_count": 113,
      "results": {
        "echo_state_property": {
          "mean_d_10s": 0.0,
          "std_d_10s": 0.0,
          "n_trials": 10,
          "passed": true
        },
        "memory_capacity": {
          "MC": 0.0,
          "MC_over_N": 0.0,
          "passed": true
        },
        "separation_ratio": {
          "SR": 0.0,
          "passed": true
        },
        "linear_readout": {
          "R2_ridge": 0.0,
          "regularization_alpha": 0.0,
          "passed": true
        },
        "nonlinear_superiority": {
          "R2_mlp": 0.0,
          "R2_ridge": 0.0,
          "ratio": 0.0,
          "passed": true
        }
      },
      "rc_confirmed": true
    },
    "B_whole_ns": { "...": "same structure" },
    "C_minimal_readout": { "...": "same structure" },
    "D_command_bottleneck": { "...": "same structure" }
  },
  "cross_partition_summary": {
    "partitions_confirming_rc": 0,
    "partitions_falsifying_rc": 0,
    "robustness": "robust|fragile|falsified"
  }
}
```

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | `openworm/OpenWorm` (validation scripts) `[TO BE CREATED]` |
| **Subdirectory** | `validation/reservoir_computing/` |
| **Issue label** | `dd026` |
| **Milestone** | Phase 2 — Reservoir Computing Validation |
| **Example PR title** | `DD026: echo state property test across 4 partitions` |

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6) (Months 4-6) |
| **Layer** | Analysis / Validation — pure analysis of simulation output, no simulation changes |
| **What does this produce?** | Quantitative assessment of whether the connectome functions as a reservoir computer |
| **Success metric** | All 5 predictions × 4 partitions tested; linear readout R² ≥ 0.5 under ≥1 partition |
| **Repository** | `openworm/OpenWorm/validation/reservoir_computing/` — issues labeled `dd026` |
| **Config toggle** | `validation.reservoir_computing: true` in `openworm.yml` |
| **Build & test** | `python validation/reservoir_computing/rc_analysis.py --config openworm.yml` |

---

## How to Build & Test

### Prerequisites

- Python 3.10+, NumPy, SciPy, scikit-learn, PyTorch (for MLP readout), matplotlib
- `cect` ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) for connectome neuron classification
- Simulation output from [DD001](DD001_Neural_Circuit_Architecture.md) (neural state HDF5) and [DD002](DD002_Muscle_Model_Architecture.md) (motor activation HDF5)

### Getting Started (Environment Setup)

This DD builds on the **c302** neural circuit framework ([DD001](DD001_Neural_Circuit_Architecture.md)) and also requires the **open-worm-analysis-toolbox** ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) for behavioral analysis of simulation output.

If you have already completed [DD001 Getting Started](DD001_Neural_Circuit_Architecture.md#getting-started-environment-setup), you have the simulation infrastructure ready. DD026 is a **pure analysis** DD — it does not modify the simulation, only analyzes its output.

If starting fresh, follow [DD001 Getting Started](DD001_Neural_Circuit_Architecture.md#getting-started-environment-setup) first to set up the simulation stack, then return here.

**Path A — Docker (recommended for newcomers):**

```bash
cd OpenWorm
docker compose build
```

Then run the simulation to produce HDF5 output, and proceed to [Step 1](#step-by-step) below.

**Path B — Native (for development):**

Complete [DD001 native setup](DD001_Neural_Circuit_Architecture.md#getting-started-environment-setup), then install the RC analysis dependencies:

```bash
# Core RC analysis dependencies
pip install scikit-learn torch matplotlib

# Connectome neuron classification (sensory/inter/motor partition definitions)
pip install cect

# Movement analysis toolbox for behavioral output analysis
pip install open-worm-analysis-toolbox
```

Verify the analysis toolchain is available:

```bash
python -c "
from sklearn.linear_model import RidgeCV
from cect import Cook2019DataReader
import torch
print('RC analysis dependencies OK')
"
```

### Step-by-step

```bash
# Run after simulation has produced neural state data (DD001 HDF5 output)
cd openworm/OpenWorm

# Step 1: Run full RC analysis across all 4 partitions
python validation/reservoir_computing/rc_analysis.py \
    --neural-states output/neural_states.h5 \
    --motor-activation output/motor_activation.h5 \
    --connectome Cook2019 \
    --output validation/reservoir_computing/rc_validation_report.json

# Step 2: Generate figures
jupyter nbconvert --execute \
    validation/reservoir_computing/RC_Validation.ipynb

# Step 3: Check results
python -c "
import json
report = json.load(open('validation/reservoir_computing/rc_validation_report.json'))
summary = report['cross_partition_summary']
print(f'RC confirmed under {summary[\"partitions_confirming_rc\"]}/4 partitions')
print(f'Robustness: {summary[\"robustness\"]}')
"
```

### Scripts that don't exist yet

| Script | Status | Phase |
|--------|--------|-------|
| `validation/reservoir_computing/rc_analysis.py` | `[TO BE CREATED]` | Phase 2 |
| `validation/reservoir_computing/rc_metrics.py` | `[TO BE CREATED]` | Phase 2 |
| `validation/reservoir_computing/rc_readout.py` | `[TO BE CREATED]` | Phase 2 |
| `validation/reservoir_computing/rc_partitions.py` | `[TO BE CREATED]` | Phase 2 |
| `validation/reservoir_computing/RC_Validation.ipynb` | `[TO BE CREATED]` | Phase 2 |

---

## Technical Approach

### Data Flow

```
DD001 neural states (HDF5) ──→ rc_analysis.py ──→ rc_validation_report.json
DD002 motor activation ────────┤                         │
DD019/DD022 sensory input ─────┤                         ▼
DD020 connectome (cect) ───────┘                   DD010 (advisory)
```

1. **Load neural states** from [DD001](DD001_Neural_Circuit_Architecture.md) simulation output (HDF5: 302 neurons × T timesteps, voltage + calcium)
2. **Load motor activation** from [DD002](DD002_Muscle_Model_Architecture.md) output (95 muscles × T timesteps)
3. **Load sensory input** from [DD019](DD019_Closed_Loop_Touch_Response.md)/[DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) stimulus logs
4. **Classify neurons** using `cect` API ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) into sensory/interneuron/motor for each partition
5. **Run 5 tests per partition** (see Falsifiable Predictions section)
6. **Produce JSON report** consumed by [DD010](DD010_Validation_Framework.md) as advisory (non-blocking)

### Neuron Classification via cect

```python
from cect import Cook2019DataReader

reader = Cook2019DataReader()
sensory_neurons = reader.get_sensory_neurons()
interneurons = reader.get_interneurons()
motor_neurons = reader.get_motor_neurons()

# Partition A: canonical
partition_a = {
    'input': sensory_neurons,
    'reservoir': interneurons,
    'readout': motor_neurons
}

# Partition D: command bottleneck
command_neurons = ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'AVDL', 'AVDR', 'AVEL', 'AVER', 'PVCL', 'PVCR']
partition_d = {
    'input': sensory_neurons,
    'reservoir': [n for n in interneurons if n not in command_neurons],
    'readout': command_neurons
}
```

### Ridge Regression Readout

```python
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import TimeSeriesSplit

# X: reservoir states (T x N_reservoir)
# Y: readout states (T x N_readout)

ridge = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0, 100.0],
                cv=TimeSeriesSplit(n_splits=5))
ridge.fit(X_train, Y_train)
R2_linear = ridge.score(X_test, Y_test)
```

### MLP Readout (for Prediction 5)

```python
import torch
import torch.nn as nn

class MLPReadout(nn.Module):
    def __init__(self, n_reservoir, n_readout):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_reservoir, 64),
            nn.ReLU(),
            nn.Linear(64, n_readout)
        )

    def forward(self, x):
        return self.net(x)

# Train MLP, compute R2_mlp
# Compare: ratio = R2_mlp / R2_linear
```

### Configuration (`openworm.yml` Section)

```yaml
validation:
  # DD026: Reservoir Computing Validation
  reservoir_computing: false     # Enable RC analysis
  rc_partitions: ["A", "B", "C", "D"]  # Which partitions to test
  rc_esp_trials: 10              # Number of ESP perturbation trials
  rc_esp_perturbation: 0.5      # ±50% of resting values
  rc_esp_duration: 10.0          # Seconds of simulated time
  rc_memory_input_duration: 100.0  # Seconds of white noise input
  rc_memory_max_delay: 100       # Max delay τ for memory capacity
  rc_separation_n_pairs: 100    # Number of input pairs
  rc_readout_duration: 60.0     # Seconds for readout training
  rc_mlp_hidden: 64             # MLP hidden layer size
  rc_ridge_alphas: [0.01, 0.1, 1.0, 10.0, 100.0]
```

---

## Validation

DD026 is itself a validation document — it validates a *computational framework* rather than a biophysical parameter. Results feed into [DD010](DD010_Validation_Framework.md) as **Tier 2a advisory** (non-blocking):

| Metric | Threshold | Blocking? | Rationale |
|--------|-----------|-----------|-----------|
| Linear readout R² | ≥ 0.5 | Advisory | Confirms motor output is linearly decodable from reservoir state |
| ESP convergence | d(10s) < 0.10 | Advisory | Confirms initial-condition independence |
| Memory capacity | MC ≥ 5 | Advisory | Confirms non-trivial temporal memory |
| Separation ratio | SR ≥ 2.0 | Advisory | Confirms input discrimination |
| Nonlinear ratio | ≤ 2.0 | Advisory | Confirms computation is in reservoir, not readout |

**Advisory means:** Results are reported in `rc_validation_report.json` and displayed in the validation dashboard, but they do not block PRs or releases. The RC framing is a scientific hypothesis, not a correctness requirement.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source | Variable | Format | Units |
|-------|--------|----------|--------|-------|
| Neural states (302 neurons) | [DD001](DD001_Neural_Circuit_Architecture.md) | Voltage, calcium traces | HDF5 | mV, µM |
| Motor activation (95 muscles) | [DD002](DD002_Muscle_Model_Architecture.md) | Muscle activation | HDF5 | dimensionless [0,1] |
| Sensory input log | [DD019](DD019_Closed_Loop_Touch_Response.md), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | Stimulus time series | HDF5/CSV | mixed |
| Connectome topology + neuron classification | [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | `cect` API (sensory/inter/motor labels) | Python API | categorical |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| RC validation report | [DD010](DD010_Validation_Framework.md) | Per-partition RC metrics | JSON | mixed |
| Cross-partition summary | [DD010](DD010_Validation_Framework.md) | Robustness assessment | JSON | categorical |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Neural state output format | [DD001](DD001_Neural_Circuit_Architecture.md) | If HDF5 schema changes, `rc_analysis.py` must update parser |
| Motor activation format | [DD002](DD002_Muscle_Model_Architecture.md) | If activation file format changes, readout training breaks |
| Neuron classification | [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | If `cect` changes neuron labels, partition definitions break |
| Sensory input format | [DD019](DD019_Closed_Loop_Touch_Response.md), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | If stimulus log format changes, input reconstruction breaks |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Validation report format | [DD010](DD010_Validation_Framework.md) | If JSON schema changes, dashboard parser must update (advisory only) |

---

## Boundaries (Explicitly Out of Scope)

1. **Modifying the simulation:** DD026 is pure *analysis* of simulation output. No changes to [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), or [DD003](DD003_Body_Physics_Architecture.md) models.
2. **Training the reservoir:** In standard RC, the reservoir is fixed. DD026 does not train or optimize the connectome weights.
3. **Online/real-time RC:** All analysis is post-hoc on recorded simulation data. No real-time readout during simulation.
4. **Comparing to other computational frameworks:** DD026 tests RC specifically. Testing attractor networks, Bayesian inference, or other frameworks would be separate DDs.
5. **Biological RC experiments:** DD026 tests the *simulated* connectome, not the biological worm. Wet-lab RC experiments are out of scope.

---

## Implementation Roadmap

### Phase 2 Implementation (~20 hours)

| Step | Task | Hours | Dependencies |
|------|------|-------|-------------|
| 1 | Implement `rc_partitions.py` with 4 partition definitions using `cect` | 2 | [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| 2 | Implement `rc_metrics.py` (ESP, memory capacity, separation ratio) | 4 | None |
| 3 | Implement `rc_readout.py` (ridge regression + MLP training) | 4 | scikit-learn, PyTorch |
| 4 | Implement `rc_analysis.py` (orchestrator: load data → run tests → produce report) | 4 | [DD001](DD001_Neural_Circuit_Architecture.md) HDF5 output |
| 5 | Create `RC_Validation.ipynb` with visualization and interpretation | 4 | Steps 1-4 |
| 6 | Integration test with Phase 2 simulation output | 2 | Phase 2 simulation running |

**Parallelization:** DD026 can be implemented in parallel with [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD019](DD019_Closed_Loop_Touch_Response.md), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md), and [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md). It only requires Phase 1 specialized neurons ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) and simulation output — no changes to the simulation itself.

---

## Quality Criteria

1. **Reproducibility:** All analysis scripts produce identical results given the same simulation output (seeded random states, deterministic ridge regression).
2. **Falsifiability:** Every prediction has a pre-registered numerical threshold. No post-hoc threshold adjustment.
3. **Cross-partition consistency:** Results are reported for all 4 partitions. Cherry-picking a single partition is not allowed.
4. **Statistical rigor:** ESP uses 10 trials with mean/std. Memory capacity uses cross-validated R². Readout uses time-series cross-validation.
5. **Interpretability:** The Jupyter notebook includes visualizations of each metric, not just pass/fail numbers.

---

## Possible Outcomes and Their Implications

### Outcome 1: RC Confirmed (≥3 partitions pass all 5 tests)

**Implication:** The *C. elegans* connectome functions as a reservoir computer. This means:

- Motor output is a linear transformation of the interneuron/reservoir state
- The recurrent dynamics of the connectome perform the nonlinear sensory→motor computation
- The network's computational power comes from its fixed topology, not from learning
- This constrains what kind of plasticity is needed (only readout weights, not internal weights)

**Publication target:** "The *C. elegans* nervous system functions as a biological reservoir computer" — *PLoS Computational Biology* or *Nature Communications*.

### Outcome 2: RC Partially Confirmed (1-2 partitions pass)

**Implication:** The RC framing is partition-dependent — fragile. This means:

- The "correct" computational decomposition of the connectome matters
- Some neuron groupings support RC, others don't
- The command neuron bottleneck (Partition D) may be particularly informative

**Publication target:** "Partition-dependent reservoir computing in the *C. elegans* connectome" — *eLife* or *PLoS Computational Biology*.

### Outcome 3: RC Falsified (0 partitions pass all 5 tests)

**Implication:** The *C. elegans* connectome is NOT a reservoir computer. This constrains what framework *does* apply:

- If ESP fails: The network has long-term state dependence (attractor dynamics?)
- If memory capacity is low: The network is too chaotic or too stable
- If separation fails: The network compresses rather than expands input space
- If linear readout fails but nonlinear works: Computation is distributed, not reservoir-style

**Publication target:** "The *C. elegans* nervous system is not a reservoir computer: implications for connectome computation" — *Nature Communications* or *eLife*.

---

## References

1. **Yan B, Raby-Smith B, Bhaskara S, et al. (2024).** "Reservoir computing in biological neural networks." *Nature Communications* 15:5765.
   *Primary motivation — demonstrates RC in biological networks.*

2. **Jaeger H (2001).** "The 'echo state' approach to analysing and training recurrent neural networks." GMD Report 148.
   *Original echo state network paper — defines ESP and RC framework.*

3. **Maass W, Natschlager T, Markram H (2002).** "Real-time computing without stable states: a new framework for neural computation based on perturbations." *Neural Computation* 14:2531-2560.
   *Liquid state machines — RC framework for biological spiking networks.*

4. **Lukoševičius M, Jaeger H (2009).** "Reservoir computing approaches to recurrent neural network training." *Computer Science Review* 3:127-149.
   *Comprehensive RC review — defines memory capacity, separation property.*

5. **Cook SJ, Jarrell TA, Brittin CA, et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *Connectome data for neuron classification (sensory/inter/motor).*

6. **Taylor SR, Santpere G, Weinreb A, et al. (2021).** "Molecular topography of an entire nervous system." *Cell* 184:4329-4347.
   *CeNGEN — cell-type classification supporting partition definitions.*

7. **Randi F, Sharma AK, Dvali S, Leifer AM (2023).** "Neural signal propagation atlas of *Caenorhabditis elegans*." *Nature* 623:406-414.
   *Functional connectivity data — independent validation of RC predictions.*

---

- **Approved by:** Pending
- **Implementation Status:** Proposed
- **Next Actions:**

1. Implement `rc_partitions.py` using `cect` neuron classification
2. Implement `rc_metrics.py` (ESP, memory capacity, separation tests)
3. Implement `rc_readout.py` (ridge + MLP readout training)
4. Run on Phase 2 simulation output
5. Produce `rc_validation_report.json` and Jupyter notebook with figures
