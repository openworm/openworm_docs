# DD005: Cell-Type Differentiation Strategy Using Single-Cell Transcriptomics

- **Status:** Proposed (Phase 1)
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD008](DD008_Data_Integration_Pipeline.md) (Data Integration Pipeline), [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition)

---

> **Phase:** [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) | **Layer:** Cell Differentiation

## TL;DR

Replace the single generic neuron template used for all 302 neurons with **128 cell-type-specific templates** parameterized from CeNGEN single-cell RNA-seq data. This is Phase 1 work — the first DD to produce biologically distinct neurons. Success metric: **20%+ improvement in functional connectivity correlation** vs. [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) experimental data.

---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Functional connectivity correlation | Improve ≥20% vs. generic model (e.g., r=0.3 → r≥0.36) | Tier 2 (blocking) |
| **Secondary:** Kinematic validation | Within ±15% of Schafer lab baseline | Tier 3 (blocking) |
| **Tertiary:** Single-cell spot-checks | Predicted channel dominance matches electrophysiology for ≥50% of training neurons | Tier 1 (non-blocking) |

**Before:** 302 copies of `GenericCell` — all neurons have identical conductances, dynamics differ only by connectivity.

**After:** 128 distinct cell types (one per CeNGEN neuron class) — each neuron has biologically informed conductance densities derived from transcriptomic expression data.

---

## Deliverables

| Artifact | Path (relative to `openworm/c302`) | Format | Example |
|----------|-------------------------------------|--------|---------|
| 128 cell-type NeuroML files | `cells/{NeuronClass}Cell.cell.nml` | NeuroML 2 XML | `cells/AVALCell.cell.nml` |
| Calibration parameters | `data/expression_to_conductance_calibration.csv` | CSV | `channel,alpha,beta,baseline,R2` |
| CeNGEN expression matrix | `data/CeNGEN_L4_expression.csv` | CSV (128 × 20,500) | `AVAL,unc-2,342.5,...` |
| Gene→channel mapping | `data/gene_to_channel_map.csv` | CSV | `unc-2,ca_boyle_chan,Cav2` |
| Differentiated network | `examples/generated/LEMS_c302_C1_Differentiated.xml` | LEMS XML | (generated, not committed) |
| Neuron class labels (viewer) | OME-Zarr: `neural/neuron_class/`, shape (302,) | string enum | `AVAL`, `AVAR`, `ASH`, ... |

Each `.cell.nml` file includes metadata:
```xml
<notes>
  CeNGEN neuron class: AVAL
  Expression data: CeNGEN L4 (cengen.org, accessed 2026-02-14)
  Calibration method: expression_to_conductance_v1
  Validation status: inferred (no direct electrophysiology)
  Key channels: unc-2 (high), shl-1 (high), twk-18 (medium)
</notes>
```

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd005` |
| **Milestone** | Phase 1: Cell-Type Differentiation |
| **Branch convention** | `dd005/description` (e.g., `dd005/cengen-calibration`) |
| **Example PR title** | `DD005: Generate 128 cell-type NeuroML files from CeNGEN L4` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, pandas, numpy, scipy
- **Recommended:** `pip install wormneuroatlas` (provides CeNGEN API + [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) data, see reuse opportunities below)

### Step-by-step

```bash
# Step 0: Test wormneuroatlas API (RECOMMENDED FIRST)
# This repo provides production-ready CeNGEN + Randi 2023 data access
pip install wormneuroatlas
python -c "
from wormneuroatlas import NeuroAtlas
atlas = NeuroAtlas()
# Test CeNGEN expression query
expr = atlas.get_gene_expression(gene_names=['unc-2', 'egl-19'], neuron_names=['AVAL', 'AVAR'])
print(f'CeNGEN API working: {len(expr)} expression values retrieved')
# Test Randi 2023 functional connectivity (needed for Tier 2 validation)
fc = atlas.get_signal_propagation_atlas(strain='wt')
print(f'Randi 2023 data: {fc.shape} functional connectivity matrix')
"
# If this works, skip Step 1 manual download — use wormneuroatlas API instead

# Step 1: Download CeNGEN data (FALLBACK if wormneuroatlas unavailable)
# Data files go into c302/data/
wget -O data/CeNGEN_L4_expression.csv "https://cengen.org/downloads/L4_expression_matrix.csv"

# Step 1b: (ALTERNATIVE) Use wormneuroatlas API for CeNGEN access
python scripts/fetch_cengen_via_atlas.py \
    --output data/CeNGEN_L4_expression.csv
# [TO BE CREATED] — Wrapper script that uses wormneuroatlas API
# Benefit: Handles neuron ID normalization, versioning, easier than manual download

# Step 2: Fit calibration parameters from electrophysiology training set
python scripts/fit_calibration.py \
    --expression data/CeNGEN_L4_expression.csv \
    --electrophysiology data/electrophysiology_training_set.csv \
    --output data/expression_to_conductance_calibration.csv
# [TO BE CREATED] — GitHub issue: openworm/c302#TBD
# Expected output: CSV with alpha, beta, baseline, R² per channel type

# Step 3: Generate 128 cell-type NeuroML files
python scripts/generate_differentiated_cells.py \
    --expression data/CeNGEN_L4_expression.csv \
    --calibration data/expression_to_conductance_calibration.csv \
    --output cells/
# Expected output: 128 .cell.nml files in cells/ directory

# Step 4: Generate differentiated c302 network
python c302/CElegans.py C1Differentiated
# Expected output: LEMS_c302_C1_Differentiated.xml

# Step 5: Quick validation (must pass before PR)
docker compose run quick-test   # with neural.differentiated: true
# Green light: simulation completes, worm moves, no NaN values

# Step 6: Full validation (must pass before merge)
docker compose run validate
# Green light: Tier 2 functional connectivity r > 0.5
# Green light: Tier 3 kinematic metrics within ±15% of baseline
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/fit_calibration.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/generate_differentiated_cells.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/compute_functional_connectivity.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/compare_to_randi2023.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/benchmark_improvement.py` | `[TO BE CREATED]` | openworm/c302#TBD |

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** Neurons layer with **color-by-class** mode.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `neural/` (same as [DD001](DD001_Neural_Circuit_Architecture.md), but now with class metadata) |
| **Color mode** | Color-by-neuron-class: 128 distinct colors, one per CeNGEN class |
| **Data source** | OME-Zarr: `neural/neuron_class/`, shape (302,) — string enum mapping each of 302 neurons to its class |
| **What you should SEE** | Neurons colored by class. Clicking a neuron shows its CeNGEN class, dominant channels, and calibration status. Calcium traces should show distinct dynamics per class (e.g., sensory neurons with faster kinetics than interneurons). |
| **Comparison view** | Side-by-side: generic model (all same color/dynamics) vs. differentiated model (distinct colors/dynamics) |

---

## Technical Approach

### Use CeNGEN scRNA-seq to Parameterize Cell-Type-Specific Ion Channel Densities

**Approach:** Map gene expression levels → conductance densities via a calibrated scaling relationship.

### Step 1: Extract Ion Channel Expression from CeNGEN

For each of the 128 neuron classes, extract normalized expression (TPM or log-normalized counts) for all ion channel genes. CeNGEN categorizes genes as:

- Voltage-gated K⁺ channels (unc-2, egl-2, shl-1, shk-1, kvs-1, etc.)
- Voltage-gated Ca²⁺ channels (unc-2, egl-19, cca-1)
- Leak/background K⁺ channels (twk, kcnk families)
- Ligand-gated channels (ACh receptors, GABA receptors, glutamate receptors)
- TRP channels (osm-9, ocr-2)

**Data source:** `cengen.org/downloads` → Gene expression matrix (128 neuron classes × 20,500 genes)

### Step 2: Map Genes to NeuroML Channel Models

| *C. elegans* Gene | Channel Family | NeuroML Model | Notes |
|-------------------|---------------|---------------|-------|
| **unc-2** | Cav2 (P/Q-type Ca) | `ca_boyle_chan` | Current default Ca channel |
| **egl-19** | Cav1 (L-type Ca) | `ca_LType_chan` (to be created) | Muscle-dominant |
| **cca-1** | Cav3 (T-type Ca) | `ca_TType_chan` (to be created) | Low-threshold |
| **shl-1** | Kv4 (A-type K) | `k_fast_chan` | Current fast K |
| **shk-1** | Kv1 (delayed rectifier) | `k_slow_chan` | Current slow K |
| **unc-103** | Kir (inward rectifier) | `k_inward_rect_chan` (to be created) | Hyperpolarization-activated |
| **twk-18** | TWIK (two-pore leak) | `leak_chan` | Current leak |
| **unc-49** | GABA-A receptor | `gaba_a_syn` | Inhibitory ligand-gated |

For genes without existing NeuroML models, create new channel models by:

1. Finding published kinetics (activation curves, time constants) if available
2. Using generic kinetics from the channel family if specific data unavailable
3. Flagging as "inferred" in metadata

### Step 3: Calibrate Expression → Conductance Scaling

The relationship between mRNA expression and membrane conductance is **not 1:1** due to:

- Post-transcriptional regulation
- Protein translation efficiency
- Subcellular localization
- Channel trafficking and degradation

**Calibration approach:** Use the ~20 neuron types with published patch-clamp data (Goodman lab, Lockery lab) as a training set.

For each of these neurons:

1. Extract CeNGEN expression for all ion channel genes
2. Extract measured conductances from electrophysiology papers
3. Fit a scaling relationship: `g_channel = alpha * expression^beta + baseline`
4. Alpha, beta, baseline are fit via regression to minimize error across the training set

**Example (hypothetical):**
```
g_Kslow = 0.5 * TPM_shk1^0.7 + 0.001 mS/cm²
```

This calibrated relationship is then applied to the remaining 108 neuron classes lacking electrophysiology.

### Step 4: Generate Cell-Type-Specific NeuroML Templates

```python
# c302/scripts/generate_differentiated_cells.py

import pandas as pd
from pyneuroml import cell_builder

# Load CeNGEN expression
cengen = pd.read_csv("data/CeNGEN_L4_expression.csv", index_col=0)

# Load calibration parameters (fit from training set)
calibration = pd.read_csv("data/expression_to_conductance_calibration.csv")

for neuron_class in cengen.index:
    # Get expression levels
    expr = cengen.loc[neuron_class]

    # Apply calibration for each channel type
    g_kslow = calibrate(expr["shk-1"], "k_slow", calibration)
    g_kfast = calibrate(expr["shl-1"], "k_fast", calibration)
    g_ca = calibrate(expr["unc-2"], "ca_boyle", calibration)
    g_leak = calibrate(expr["twk-18"], "leak", calibration)

    # Create NeuroML cell
    cell = cell_builder.create_cell(
        id=f"{neuron_class}Cell",
        channels=[
            ("leak_chan", g_leak),
            ("k_slow_chan", g_kslow),
            ("k_fast_chan", g_kfast),
            ("ca_boyle_chan", g_ca)
        ],
        C_m=1.0,
        v_init=-45
    )

    # Write to file
    cell_builder.write_neuroml(cell, f"cells/{neuron_class}Cell.cell.nml")
```

### Step 5: Generate Differentiated c302 Network

```python
# c302/CElegans.py
python CElegans.py C1Differentiated
```

This produces `LEMS_c302_C1_Differentiated.xml` with 128 distinct cell types (one per CeNGEN neuron class) instead of 302 copies of GenericCell.

### Step 6: Validate Against Functional Connectivity

**Primary validation:** [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain calcium imaging functional connectivity matrix.

- Compute pairwise correlations in simulated calcium signals
- Compare to experimental pairwise correlations
- Metric: Pearson correlation between simulated and real correlation matrices

**Expected improvement:** The differentiated model should capture cell-type-specific dynamics (e.g., ASH sensory neurons with fast kinetics, interneurons with slower integration) better than the generic model.

---

## Alternatives Considered

### 1. AlphaFold3 + Molecular Dynamics to Predict Channel Kinetics

**Description:** Use AlphaFold to predict 3D structures of all *C. elegans* ion channels, then run molecular dynamics simulations to extract gating kinetics (activation curves, time constants).

**Rejected (for now) because:**

- Computationally expensive (days-weeks per channel)
- MD-to-HH parameter conversion is non-trivial and error-prone
- Published kinetics exist for many channel families; borrow from orthologs
- CeNGEN expression-based scaling is faster and requires only transcriptomic data

**When to reconsider:** If cell-type-specific electrophysiology becomes available for validation, or if a channel has no known ortholog kinetics.

### 2. Direct Electrophysiology for All 128 Neuron Classes

**Description:** Perform patch-clamp recordings for all 128 CeNGEN neuron classes.

**Rejected because:**

- Experimentally infeasible. Each neuron type requires identifying the cell in vivo (NeuroPAL), dissecting, patching, recording across multiple voltage protocols, and analyzing. ~1-2 weeks per neuron type × 128 = years of work.
- Not necessary if scaling relationship from expression works.

**When to reconsider:** Use targeted electrophysiology to validate model predictions for specific high-impact neurons (command interneurons, motor neurons).

### 3. Foundation Model Regression (Learned Expression → Conductance Mapping)

**Description:** Train a neural network (e.g., gradient boosting or transformer) to predict conductance densities from full expression profiles, using the 20 neurons with electrophysiology as training data.

**Deferred (but promising) because:**

- Only 20 training examples (neurons with electrophysiology) may be insufficient
- Requires careful hyperparameter tuning and cross-validation
- Black-box learned mapping is less interpretable than explicit scaling

**When to try:** After the simple scaling approach is tested. If it performs poorly, a learned model may capture nonlinear relationships (e.g., channel subunit co-assembly, trafficking dependencies).

### 4. Manual Curation from Literature

**Description:** Search the literature for each neuron type, extract reported channel expression, manually set conductances.

**Rejected because:**

- Labor-intensive (128 neuron classes × literature search)
- Incomplete (most neurons lack published channel data)
- Not reproducible or updatable as new data arrive

### 5. Uniform Random Variation

**Description:** Keep the generic model but add random ±20% variation to conductances across neurons.

**Rejected because:**

- Biologically meaningless
- Does not improve model accuracy
- Confuses rather than clarifies

### 6. Clustering-Based Parameterization

**Description:** Cluster the 128 CeNGEN neuron classes into 10-20 "super-types" based on expression similarity, then create one model per super-type.

**Rejected because:**

- Arbitrary clustering (how many clusters? which genes to cluster on?)
- Loses biological specificity (ASH nociceptor ≠ AWA olfactory neuron, even if they cluster together)
- The data exist to differentiate all 128 classes, so why reduce resolution?

**When to reconsider:** If 128 cell types prove computationally intractable or if most classes are near-identical.

### 7. Wait for Electrophysiology for All Neurons

**Description:** Do not differentiate until direct patch-clamp data exist for all 128 classes.

**Rejected because:**

- Will never happen (experimentally infeasible)
- Perpetuates the known inaccuracy of the generic model
- CeNGEN data are available now; use them

---

## Quality Criteria

### What Defines a Valid Differentiated Cell Model?

1. **Expression-Based Parameterization:** All conductance densities must be derived from CeNGEN expression data using the documented calibration relationship. Do not manually tune parameters.

2. **NeuroML 2 Compliance:** Each cell type is a separate NeuroML `<cell>` element with unique `id` (e.g., `AVALCell`, `ASHCell`).

3. **Preserve Connectome Topology:** The number of neurons (302 hermaphrodite, 385 male) and their connectivity ([Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7)) must match the biological data. Differentiation changes cell properties, not network structure.

4. **Calibration Transparency:** The `expression_to_conductance_calibration.csv` file must document:
    - Training set (which neurons with electrophysiology)
    - Fit parameters (alpha, beta, baseline for each channel type)
    - Cross-validation R² or error metric
    - Date of calibration and CeNGEN version

5. **Validation Against Functional Data:** The differentiated model must improve the correlation with [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity compared to the generic model.

6. **CeNGEN Expression Data as Ground Truth:** All conductance densities must be traceable to CeNGEN expression values via the documented calibration relationship.

7. **Version Control:** Each cell type file is versioned. If calibration parameters change, create a new version (e.g., `AVALCell_v2.cell.nml`).

### Validation Procedure

```bash
# Generate differentiated network
python c302/CElegans.py C1Differentiated

# Run simulation with calcium recording
jnml LEMS_c302_C1_Differentiated.xml -nogui

# Extract pairwise calcium correlations
python scripts/compute_functional_connectivity.py \
    LEMS_c302_C1_Differentiated_calcium.dat \
    --output simulated_func_conn.npy
# [TO BE CREATED] — GitHub issue: openworm/c302#TBD

# Compare to Randi et al. 2023 experimental data
python scripts/compare_to_randi2023.py \
    simulated_func_conn.npy \
    data/randi2023_functional_connectivity.csv \
    --metric correlation
# [TO BE CREATED] — GitHub issue: openworm/c302#TBD

# Report improvement over generic model
python scripts/benchmark_improvement.py \
    --baseline generic_func_conn.npy \
    --differentiated simulated_func_conn.npy \
    --experimental randi2023_functional_connectivity.csv
# [TO BE CREATED] — GitHub issue: openworm/c302#TBD
```

**Success criteria:**

- Correlation (simulated vs. experimental functional connectivity) improves ≥20% vs. generic model
- At least 50% of neuron classes show expression-predicted channel dominance
- No simulation instabilities (no NaN, no voltage explosions)
- Tier 3 kinematic validation still passes (±15%)

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Non-neural cells:** Muscle, intestine, hypodermis, gonad. This DD applies only to the 302 neurons. Muscle differentiation is a separate effort (Phase 3).

2. **Developmental stage differences:** CeNGEN L4 is the reference stage. L1, adult, dauer require separate expression datasets (CeNGEN L1 is available; others are future work).

3. **Male-specific neurons:** The 83 male-specific neurons ([Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7)) lack CeNGEN data. Use hermaphrodite classes as proxy until male scRNA-seq is available.

4. **Neuropeptide receptors:** Expression is in CeNGEN, but receptor dynamics are covered in [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptidergic Connectome).

5. **Individual genetic variation:** Natural isolates show expression variation (Ben-David et al. 2021 eQTLs). This DD uses population-averaged expression. Individual variation is Phase 6+ work.

6. **Synaptic weight differences:** Expression-based differentiation affects postsynaptic channels but not synaptic weights (connection strengths). Synapse-specific weights from functional data are future work.

7. **Channel post-translational modifications:** Phosphorylation, palmitoylation, etc. are not captured by transcriptomics.

8. **Subcellular / synapse-level molecular localization:** CeNGEN provides cell-class-average transcript counts, not spatial information about where proteins are distributed within a neuron. Emerging techniques — expansion microscopy optimized for *C. elegans* (Shaib et al. 2023) and expansion sequencing (ExSeq) for spatially precise in-situ transcriptomics (Alon et al. 2021) — will eventually provide molecular maps at synaptic resolution, enabling per-synapse channel density assignments. This is future work (Phase 5+) that will complement the class-average approach used here and feed into [DD001](DD001_Neural_Circuit_Architecture.md) Level E multicompartmental models.

---

### Roadmap: From Class-Average to Synapse-Level Resolution

The current power-law expression-to-conductance pipeline is a necessary first step. It uses the best available systematic data (CeNGEN) to move beyond the generic neuron template. Future phases will refine this in stages:

1. **Phase 1 (this DD):** Class-average expression → class-specific conductance densities (128 uniform templates)
2. **Phase 2-3:** Incorporate functional data (Randi et al. 2023 signal propagation) to constrain relative channel weights via data-driven parameter fitting ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) differentiable backend)
3. **Phase 5+:** Subcellular resolution from expansion microscopy (Shaib et al. 2023) and in-situ sequencing (Alon et al. 2021) → per-compartment channel densities for [DD001](DD001_Neural_Circuit_Architecture.md) Level E multicompartmental models

Each stage preserves backward compatibility with earlier stages via the `openworm.yml` configuration system.

---

## Context & Background

The current c302 model uses a **single generic neuron cell template** for all 302 neurons, with identical ion channel types and conductance densities. The only distinguishing feature between neuron types is their connectivity pattern. As stated in the CElegansNeuroML repository: "an accurate representation of the ion channels and their distributions in each neuron has not yet been attempted."

This is biologically inaccurate. Real neurons express distinct complements of ion channels, receptors, and signaling machinery. The CeNGEN database ([Taylor et al. 2021](https://doi.org/10.1016/j.cell.2021.06.023)) provides single-cell RNA-seq for 100,955 neurons across 128 neuron classes at L4 larval stage, making cell-type-specific differentiation feasible for the first time.

John White, in the February 12, 2026 meeting, emphasized: "there's a huge amount of information there" (referring to CeNGEN) and urged integration of this dataset into the modeling framework.

### CeNGEN Data Access

**RECOMMENDED: Use wormneuroatlas Python Package**

- **Repository:** `openworm/wormneuroatlas` (maintained, pip-installable)
- **Docs:** https://francescorandi.github.io/wormneuroatlas/

```python
# Install
pip install wormneuroatlas

# Access CeNGEN expression data
from wormneuroatlas import NeuroAtlas

atlas = NeuroAtlas()
expression_data = atlas.get_gene_expression(
    gene_names=["unc-2", "egl-19", "shl-1", "shk-1", "twk-18"],  # Ion channel genes
    neuron_names=["AVAL", "AVAR", "DA01", ...]  # All 128 CeNGEN classes
)
# Returns: pandas DataFrame with TPM values per gene per neuron class
# Handles neuron ID normalization (AVAL vs AVA_, bilateral merging)
```

**Benefits:**

- ✅ No manual CSV download/parsing
- ✅ Handles neuron ID variants automatically
- ✅ pip-installable (works in Docker)
- ✅ Maintained by Randi lab (Francesco Randi)
- ✅ Also provides [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity for [DD010](DD010_Validation_Framework.md) Tier 2 validation

**Fallback: Manual download from cengen.org**

If wormneuroatlas is unavailable:
```
https://cengen.org/downloads
```

**Files:**

- `CeNGEN_gene_expression_matrix_L4.csv` — 128 neuron classes × 20,500 genes
- `CeNGEN_neuron_class_annotations.csv` — Maps Cook et al. neuron IDs to CeNGEN classes
- `CeNGEN_ion_channel_genes.csv` — Curated list of ion channel genes with functional classifications

### Calibration Dataset (Neurons with Electrophysiology)

| Neuron | Gene Expression Source | Electrophysiology Source | Key Channels Measured |
|--------|----------------------|-------------------------|---------------------|
| Touch neurons (ALM, AVM, PLM) | CeNGEN | Goodman et al. 1998 | mec-4, unc-2 |
| AVA interneuron | CeNGEN | Lockery lab | unc-2, shl-1 |
| RIM motor neuron | CeNGEN | Liu et al. 2018 | egl-19, unc-2 |
| ASH polymodal nociceptor | CeNGEN | Hilliard et al. 2002, **WormsenseLab_ASH repo** | osm-9 |
| AWC olfactory neuron | CeNGEN | [Chalasani et al. 2007](https://doi.org/10.1038/nature06292) | tax-2/tax-4 |

Approximately **20 neuron types** have published electrophysiological recordings suitable for calibration.

**Note:** The calibration training set should be expanded with a complete table listing each neuron, channel, measured conductance, reversal potential, and source DOI. See ChannelWorm ion channel database as a starting point.

**CODE REUSE:** The `openworm/ChannelWorm` repository (dormant since 2018 but complete) contains a curated ion channel database (`data/ion_channel_database.xlsx`) with patch clamp sources, HH parameter fitting tools (`channelworm/fitter.py`), and pre-generated NeuroML2 channel models (`models/*.channel.nml`). **This is 50-70% of [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s calibration pipeline already built.** See "ChannelWorm Reuse" section below for integration plan.

---

## Migration Path

### From Generic to Differentiated (Contributor Workflow)

**Old workflow (generic model):**
```bash
python c302/CElegans.py C1
jnml LEMS_c302_C1.xml
```
Output: 302 identical neurons.

**New workflow (differentiated model):**
```bash
python c302/CElegans.py C1Differentiated
jnml LEMS_c302_C1_Differentiated.xml
```
Output: 128 distinct neuron types.

**Backward compatibility:** The generic model remains available. Existing scripts that depend on `GenericCell` are not broken. Both models coexist.

### Incremental Rollout

Do not switch the entire community to differentiated models on day 1. Rollout plan:

1. **Week 1-2:** Generate differentiated cells, validate locally
2. **Week 3-4:** Publish as experimental branch, invite community testing
3. **Week 5-6:** Present validation results (functional connectivity improvement, no kinematic degradation)
4. **Week 7+:** Make differentiated model the recommended default in documentation; keep generic model for backward compatibility

---

## Code Reuse Opportunities

### ChannelWorm Ion Channel Database (HIGH-IMPACT REUSE)

- **Repository:** `openworm/ChannelWorm` (pushed 2018-08-27, dormant but complete)
- **Status:** Contains curated ion channel database + HH parameter fitting tools

**What It Provides:**
```
ChannelWorm/
├── data/ion_channel_database.xlsx    # Curated ion channels with patch clamp sources
├── models/*.channel.nml               # Pre-generated NeuroML2 channel models
├── channelworm/fitter.py              # HH parameter fitting from experimental data
├── channelworm/digitizer.py           # Digitize patch clamp plots from papers
└── tests/                             # SciUnit validation framework
```

**Reuse Plan:**

1. **Extract ion channel database:** `data/ion_channel_database.xlsx` → Convert to [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s `electrophysiology_training_set.csv`
    - Contains: gene, channel family, measured conductances, patch clamp paper DOIs
    - Covers many of the ~20 neurons needed for calibration training set
2. **Reuse HH fitting code:** `channelworm/fitter.py` → Adapt for [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s `scripts/fit_calibration.py`
    - Already implements least-squares fitting of HH parameters to experimental I-V curves
    - Handles activation/inactivation gate fitting separately
3. **Use pre-generated NeuroML2 models:** `models/unc2_L-type_Ca.channel.nml`, `models/egl19_L-type_Ca.channel.nml`, etc.
    - These can be [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s initial channel definitions (before calibration)
    - Cross-validate: Do ChannelWorm's models match [DD001](DD001_Neural_Circuit_Architecture.md)'s current channels?
4. **Reuse SciUnit validation:** `tests/` directory → [DD010](DD010_Validation_Framework.md) Tier 1 single-cell validation framework

**Estimated Time Savings:** 40-60 hours (no manual channel curation, HH fitter exists, NeuroML2 models already generated)

**Testing:**
```bash
git clone https://github.com/openworm/ChannelWorm.git
cd ChannelWorm
pip install -r requirements.txt  # May need dependency updates for Python 3.12
cd data/
# Convert ion_channel_database.xlsx to CSV
python -c "import pandas as pd; pd.read_excel('ion_channel_database.xlsx').to_csv('ion_channels.csv', index=False)"
# Review: How many channels? How many have measured conductances?
wc -l ion_channels.csv
head -20 ion_channels.csv
```

**Next Actions:**

- [ ] Test ChannelWorm installation on Python 3.12 (may need dependency updates)
- [ ] Extract ion channel database, count coverage (how many of 20 training neurons present?)
- [ ] Compare ChannelWorm's NeuroML2 models to [DD001](DD001_Neural_Circuit_Architecture.md)'s current channel definitions
- [ ] Port `channelworm/fitter.py` algorithm to [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s calibration pipeline
- [ ] Add ChannelWorm to [DD013](DD013_Simulation_Stack_Architecture.md) `versions.lock` if used

---

## Known Issues and Future Work

### Issue 1: Calibration Relies on Limited Training Data

Only ~20 neuron types have electrophysiology. Extrapolating to 128 classes assumes the expression→conductance relationship is conserved. This may fail for highly divergent cell types (e.g., sensory neurons with specialized channels).

**Mitigation:** Flag inferred cell types in metadata. Prioritize experimental validation for high-impact neurons (command interneurons: AVA, AVB, AVD, AVE; motor neurons: DA, DB, VA, VB).

**CODE REUSE:** The `openworm/ChannelWorm` database may expand the training set beyond 20 neurons if it contains additional patch clamp sources not yet incorporated into [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s curated list.

### Issue 2: CeNGEN Is L4 Only

CeNGEN L1 data exist but are less mature. Adult and dauer expression are unavailable. Developmental changes in channel expression are not captured.

**Future work:** Integrate CeNGEN L1 when validated. Use [Packer et al. 2019](https://doi.org/10.1126/science.aax1971) embryonic atlas for earlier stages.

### Issue 3: Post-Transcriptional Regulation

mRNA levels ≠ protein levels ≠ surface channel density. The calibration implicitly absorbs these factors into the scaling relationship, but cell-type-specific regulation is not modeled.

**Future work:** If proteomics data become available (currently scarce), refine calibration using protein abundance instead of transcript abundance.

### Existing Code Resources

**wormneuroatlas** ([openworm/wormneuroatlas](https://github.com/openworm/wormneuroatlas), PyPI: `pip install wormneuroatlas`, maintained 2025):
Provides unified Python API for CeNGEN gene expression (`NeuroAtlas.get_gene_expression(gene_names, neuron_names)`), [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity, neuropeptide/GPCR mapping, and neuron ID normalization. Replaces manual CeNGEN CSV download with a production-ready, pip-installable package. **Estimated time savings: 25 hours.**

**ChannelWorm** ([openworm/ChannelWorm](https://github.com/openworm/ChannelWorm), dormant since 2018 but complete):
Contains curated ion channel database (`data/ion_channel_database.xlsx`), pre-generated NeuroML2 channel models (`models/*.channel.nml`), HH parameter fitting tools (`channelworm/fitter.py`), and SciUnit validation tests. This was designed to feed c302 and provides the exact calibration pipeline DD005 needs. **Estimated time savings: 40-60 hours.**

**WormsenseLab_ASH** ([openworm/WormsenseLab_ASH](https://github.com/openworm/WormsenseLab_ASH), dormant):
Contains ASH neuron patch clamp recordings useful for calibration training set (ASH channel conductances).

**NicolettiEtAl2019_NeuronModels** ([openworm/NicolettiEtAl2019_NeuronModels](https://github.com/openworm/NicolettiEtAl2019_NeuronModels), 2025):
Pre-fitted HH models for AWCon and RMD neurons (Nicoletti et al. 2019). Expands the ~20-neuron calibration training set with published parameter fits that can serve as cross-validation targets for the expression→conductance scaling pipeline.

**NicolettiEtAl2024_MN_IN** ([openworm/NicolettiEtAl2024_MN_IN](https://github.com/openworm/NicolettiEtAl2024_MN_IN), 2025):
Motor neuron and interneuron HH models (Nicoletti et al. 2024). Provides B-class motor neuron templates needed for [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) stretch receptor channels, and additional calibration data for motor neuron cell types.

**NeuroPAL** ([openworm/NeuroPAL](https://github.com/openworm/NeuroPAL), 2025):
Scripts for NeuroPAL dataset analysis and conversion. In-vivo neuron identification datasets for validating that cell-type assignments from CeNGEN expression correctly map to anatomical neuron identities.

---

## References

1. **Taylor SR et al. (2021).** "Molecular topography of an entire nervous system." *Cell* 184:4329-4347.
   *CeNGEN database.*

2. **Goodman MB, Hall DH, Avery L, Bhatt R (1998).** "Active currents regulate sensitivity and dynamic range in *C. elegans* neurons." *Neuron* 20:763-772.
   *Electrophysiology validation data.*

3. **Randi F, Sharma AK, Dvali N, Leifer AM (2023).** "Neural signal propagation atlas of *Caenorhabditis elegans*." *Nature* 623:406-414.
   *Functional connectivity validation target.*

4. **Boyle JH, Cohen N (2008).** "Caenorhabditis elegans body wall muscles are simple actuators." *Biosystems* 94:170-181.
   *Source of generic channel kinetics.*

5. **Yemini E et al. (2021).** "NeuroPAL: A multicolor atlas for whole-brain neuronal identification in *C. elegans*." *Cell* 184:272-288.
   *In vivo neuron identification for validation.*

6. **Alon S et al. (2021).** "Expansion sequencing: spatially precise in situ transcriptomics in intact biological systems." *Science* 371.
   *In-situ sequencing enabling subcellular-resolution gene expression maps — future data source for per-compartment channel densities.*

7. **Shaib AH et al. (2023).** "*C. elegans*-optimized Expansion Microscopy." ExM with 20-fold expansion for nanoscale molecular mapping.
   *Future data source for synapse-level protein localization, enabling refinement beyond class-average expression.*

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source | Variable | Format | Units |
|-------|--------|----------|--------|-------|
| CeNGEN L4 expression matrix | cengen.org / OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) | 128 neuron classes × 20,500 genes | CSV (TPM or log-normalized counts) | TPM |
| Electrophysiology calibration data | Published literature (Goodman, Lockery labs) | ~20 neuron classes with patch-clamp | CSV: neuron_class, channel, measured_g | S/cm² |
| Ion channel gene→NeuroML model mapping | [DD001](DD001_Neural_Circuit_Architecture.md) channel definitions | Gene symbol → NeuroML channel ID | Python dict / CSV | identifiers |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| 128 cell-type-specific NeuroML cell files | [DD001](DD001_Neural_Circuit_Architecture.md) (replaces GenericCell when `differentiated: true`) | `{NeuronClass}Cell.cell.nml` | NeuroML 2 XML | S/cm² (conductances), mV, ms |
| Calibration parameters file | [DD001](DD001_Neural_Circuit_Architecture.md) (reproducibility) | `expression_to_conductance_calibration.csv` | CSV: channel, alpha, beta, baseline, R² | mixed |
| Neuron class labels (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-neuron class identity (128 classes) for color-by-type mode | OME-Zarr: `neural/neuron_class/`, shape (302,) | string enum |

### CRITICAL: Integration Cascade

Changing neuron conductance densities changes calcium dynamics → changes muscle activation magnitudes → changes body forces → changes locomotion. **This is a full-stack cascade.** Any change to the calibration relationship or CeNGEN data version MUST be validated against the complete coupling chain, not just Tier 2 functional connectivity.

Validation sequence after calibration changes:

1. Tier 1: Single-cell electrophysiology spot-checks (non-blocking)
2. Tier 2: Functional connectivity correlation > 0.5 (blocking)
3. **Tier 3: Full coupled simulation kinematic metrics within ±15% (BLOCKING)**

### Repository & Packaging

- **Primary repository:** `openworm/c302`
- **Docker stage:** `neural` (same as [DD001](DD001_Neural_Circuit_Architecture.md))
- **`versions.lock` key:** `c302`
- **Build dependencies:** pyNeuroML (pip), pandas (pip), scipy (pip)
- **Additional data in image:** CeNGEN expression matrix (~50MB CSV), calibration file (~1KB)
- **`versions.lock` note:** CeNGEN data version must be recorded alongside c302 commit

### Configuration

```yaml
neural:
  differentiated: true               # false = generic model ([DD001](DD001_Neural_Circuit_Architecture.md) default)
                                     # true = CeNGEN-differentiated ([DD005](DD005_Cell_Type_Differentiation_Strategy.md))
  cengen_version: "L4_v1.0"         # Pin the CeNGEN data version
  calibration_version: "v1"          # Pin the calibration parameters
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `neural.differentiated` | `false` | `true`/`false` | Enable CeNGEN-based cell differentiation |
| `neural.cengen_version` | `"L4_v1.0"` | String | CeNGEN dataset version pin |
| `neural.calibration_version` | `"v1"` | String | Calibration parameter version pin |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
docker compose run quick-test   # with neural.differentiated: true
# Checks: simulation completes, worm moves, no NaN values

# Full validation (must pass before merge to main)
docker compose run validate
# Checks:
#   - Tier 2: functional connectivity r > 0.5 AND improved vs. generic baseline
#   - Tier 3: kinematic metrics within ±15% of experimental data
#   - If Tier 3 fails: calibration is wrong, do NOT merge
```

**Per-PR checklist:**

- [ ] All 128 `.cell.nml` files generated without error
- [ ] `jnml -validate` passes for each cell file
- [ ] `quick-test` passes with `differentiated: true`
- [ ] `validate` passes (Tier 2 + Tier 3)
- [ ] Calibration CSV committed with metadata (training set, R², CeNGEN version)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `neural/neuron_class/` (302,) | Neurons layer | 128-color palette, one per CeNGEN class |
| `neural/calcium/` (n_timesteps, 302) | Calcium activity | Warm colormap (blue→red), class-specific dynamics visible |
| `neural/voltage/` (n_timesteps, 302) | Voltage traces | Standard mV colormap |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| NeuroML channel model definitions | [DD001](DD001_Neural_Circuit_Architecture.md) | If channel kinetics change, calibration must be redone |
| CeNGEN data (external) | cengen.org | If CeNGEN updates expression values, all cell files must be regenerated |
| Calibration training set (electrophysiology) | Published data | New electrophysiology data should improve calibration |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Neural circuit dynamics | [DD001](DD001_Neural_Circuit_Architecture.md) | Every neuron's voltage/calcium behavior changes |
| Muscle activation | [DD002](DD002_Muscle_Model_Architecture.md) | Motor neuron calcium output drives muscles — different conductances = different force |
| Body locomotion | [DD003](DD003_Body_Physics_Architecture.md) | Changed muscle forces → changed movement |
| Neuropeptide release | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Different calcium dynamics → different peptide release timing |
| Functional connectivity validation | [DD010](DD010_Validation_Framework.md) | Tier 2 baseline changes — must re-establish reference values |

---

- **Approved by:** Pending (Phase 1 work)
- **Implementation Status:** Proposed
- **Next Actions:**

1. Download CeNGEN L4 expression matrix
2. Curate ion channel gene list
3. Collect electrophysiology data for calibration training set (20 neurons)
4. Fit calibration relationship
5. Generate 128 cell-type-specific NeuroML files
6. Validate against [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4)
