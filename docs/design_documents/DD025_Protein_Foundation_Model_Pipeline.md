# DD025: Protein Foundation Model Pipeline for Ion Channel Kinetics

- **Status:** Proposed (Phase A / Phase 1)
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-22
- **Supersedes:** None (extracted from [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 3)
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Hybrid ML Framework), [DD010](DD010_Validation_Framework.md) (Validation Framework)

---

> **Phase:** [Phase A](DD_PHASE_ROADMAP.md#phase-a-infrastructure-bootstrap-weeks-1-4) (cross-validation) / [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) (integration) | **Layer:** ML/Structural Biology

## TL;DR

Predict ion channel kinetics (HH parameters: V_half, slope, tau) from amino acid sequences using protein foundation models (AlphaFold 3, BioEmu-1, ESM Cambrian). This expands the calibration set for [DD005](DD005_Cell_Type_Differentiation_Strategy.md) from ~20 neurons (limited by patch-clamp electrophysiology) toward all 128 neuron classes (limited only by sequence availability). Cross-validation against known channels begins in Phase A; predictions feed into [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration as structure-informed priors in Phase 1.

---

## Goal & Success Criteria

**Goal:** Build a computational pipeline that predicts Hodgkin-Huxley kinetic parameters for *C. elegans* ion channels from protein sequence, validated against channels with experimentally measured kinetics.

| Criterion | Target | Phase | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|-------|------------|
| **Primary:** Cross-validation on known channels | < 30% relative error on HH parameters (V_half, slope, tau) | Phase A | Tier 1 (non-blocking) |
| **Secondary:** End-to-end simulation improvement | Predicted parameters inserted into simulation do not degrade [DD010](DD010_Validation_Framework.md) Tier 2 or Tier 3 scores below acceptance thresholds | Phase 1 | Tier 2/3 (blocking) |
| **Tertiary:** Coverage expansion | Predictions available for ≥80% of ion channel genes expressed in CeNGEN | Phase 1 | Non-blocking |

**Before:** [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibrates expression→conductance using ~20 neurons with patch-clamp data. Remaining 108 classes extrapolate from this small training set.

**After:** Structure-based kinetics predictions available for most *C. elegans* ion channels. [DD005](DD005_Cell_Type_Differentiation_Strategy.md) uses these as calibration priors where electrophysiology is unavailable.

---

## Deliverables

| Artifact | Path | Format | Phase |
|----------|------|--------|-------|
| Channel kinetics predictions | `foundation_params/output/channel_kinetics_predictions.csv` | CSV (channel, V_half_m, k_m, tau_m, V_half_h, k_h, tau_h, g_max_scale, E_rev, confidence) | Phase A |
| Cross-validation report | `foundation_params/output/cross_validation_report.json` | JSON (per-channel predicted vs. measured, error metrics) | Phase A |
| Foundation model inference scripts | `foundation_params/scripts/` | Python | Phase A |
| Per-neuron-class HH parameters | `foundation_params/output/per_class_hh_params.csv` | CSV (128 neuron classes × channel parameters) | Phase 1 |
| Integration adapter for DD005 | `foundation_params/scripts/generate_dd005_priors.py` | Python | Phase 1 |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | `openworm/openworm-ml` (new repo, shared with [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)) `[TO BE CREATED]` |
| **Subdirectory** | `foundation_params/` |
| **Issue label** | `dd025` |
| **Milestone** | Phase A — Foundation Model Channel Kinetics |
| **Example PR title** | `DD025: cross-validation of BioEmu-1 kinetics predictions on 50 channels` |

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase A](DD_PHASE_ROADMAP.md#phase-a-infrastructure-bootstrap-weeks-1-4) (cross-validation), [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) (integration) |
| **Layer** | ML/Structural Biology — parallel track derisking [DD005](DD005_Cell_Type_Differentiation_Strategy.md) |
| **What does this produce?** | Predicted HH kinetic parameters for *C. elegans* ion channels from protein sequence + structure |
| **Success metric** | Cross-validation <30% relative error on known channels; end-to-end [DD010](DD010_Validation_Framework.md) Tier 2 scores not degraded |
| **Repository** | `openworm/openworm-ml/foundation_params/` — issues labeled `dd025` |
| **Config toggle** | `ml.foundation_params: true` in `openworm.yml` |
| **Build & test** | `python foundation_params/scripts/run_cross_validation.py` |

---

## How to Build & Test

**Prerequisites:** Python 3.10+, PyTorch, ESM library, internet access for model downloads.

```bash
# Clone and set up
git clone https://github.com/openworm/openworm-ml.git
cd openworm-ml/foundation_params

# Install dependencies
pip install -r requirements.txt  # torch, esm, biopython, pandas, numpy

# Step 1: Download C. elegans ion channel sequences from WormBase
python scripts/fetch_channel_sequences.py \
    --output data/celegans_channel_sequences.fasta

# Step 2: Run structure prediction (or download from AlphaFold DB)
python scripts/predict_structures.py \
    --sequences data/celegans_channel_sequences.fasta \
    --output data/predicted_structures/

# Step 3: Run kinetics prediction pipeline
python scripts/predict_kinetics.py \
    --structures data/predicted_structures/ \
    --output output/channel_kinetics_predictions.csv

# Step 4: Cross-validate against known channels
python scripts/run_cross_validation.py \
    --predictions output/channel_kinetics_predictions.csv \
    --ground_truth data/known_channel_kinetics.csv \
    --output output/cross_validation_report.json
# Green light: relative error < 30% on HH parameters

# Step 5 (Phase 1): Generate DD005 calibration priors
python scripts/generate_dd005_priors.py \
    --predictions output/channel_kinetics_predictions.csv \
    --cengen data/CeNGEN_L4_expression.csv \
    --output output/per_class_hh_params.csv
```

### Scripts that don't exist yet

| Script | Status | Phase |
|--------|--------|-------|
| `scripts/fetch_channel_sequences.py` | `[TO BE CREATED]` | Phase A |
| `scripts/predict_structures.py` | `[TO BE CREATED]` | Phase A |
| `scripts/predict_kinetics.py` | `[TO BE CREATED]` | Phase A |
| `scripts/run_cross_validation.py` | `[TO BE CREATED]` | Phase A |
| `scripts/generate_dd005_priors.py` | `[TO BE CREATED]` | Phase 1 |

---

## Context & Background

### The Problem: Limited Electrophysiology Data

[DD001](DD001_Neural_Circuit_Architecture.md) uses the same generic HH parameters for all 302 neurons. [DD005](DD005_Cell_Type_Differentiation_Strategy.md) proposes specializing via CeNGEN single-cell transcriptomics, but the mapping from mRNA transcript counts to functional conductance densities is a hard, unsolved problem. The current plan ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) proposes a hand-crafted scaling:

```
g_max(neuron_class, channel) = baseline_g * expression_level(neuron_class, channel) / max_expression(channel)
```

This is biologically naive — mRNA levels don't linearly predict protein abundance, protein abundance doesn't linearly predict functional conductance, and post-translational modification, trafficking, and localization all intervene. Only ~20 neuron types have patch-clamp electrophysiology for calibration.

### The Solution: Protein Foundation Models

A rapidly expanding ecosystem of protein foundation models now enables prediction of ion channel kinetics directly from sequence:

```
Step 1: Gene sequence → Protein structure
        Tool: AlphaFold 3, Boltz-2, or Protenix
        Input: C. elegans ion channel gene sequences (from WormBase)
        Output: Predicted 3D protein structures

Step 2: Protein structure → Conformational dynamics
        Tool: BioEmu-1 (Microsoft, 100,000x MD speed)
        Input: Predicted structures
        Output: Gating transition ensembles (open ↔ closed states)

Step 3: Conformational dynamics → HH kinetics
        Tool: ML predictor (trained on channels with known kinetics)
        Input: Conformational landscape + known electrophysiology database
        Output: Predicted HH parameters (V_half, k, tau for each gate)

Step 4: Feed into DD001/DD005 HH ODEs
        Output parameters go directly into NeuroML (or differentiable backend)
```

### Why This Changed: BioEmu-1

[DD005](DD005_Cell_Type_Differentiation_Strategy.md) Alternative #1 originally rejected this approach because molecular dynamics was "computationally expensive (days-weeks per channel)." [BioEmu-1](https://github.com/microsoft/BioEmu) (Microsoft, 2025) changed this calculus: conformational ensembles at 100,000x MD speed make gating parameter prediction feasible for all *C. elegans* channels.

### Why Phase A (Not Phase 3)

This pipeline was originally specified as [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 3 in Phase 3 (months 7-12). It belongs in Phase A because:

1. **Derisks DD005:** If [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s power-law expression→conductance scaling fails for certain neuron classes, DD025 predictions are ready immediately as a fallback
2. **No infrastructure dependencies:** Inputs (WormBase sequences, literature kinetics) are available today. No Docker stack, no simulation infrastructure needed
3. **Available tools:** AlphaFold 3, BioEmu-1, ESM Cambrian are all publicly available with open-source code
4. **Independent scope:** Distinct inputs/outputs, timeline, and validation criteria from [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Components 1, 2, and 4

---

## Technical Approach

### Foundation Models for Each Pipeline Step

| Step | Model | What It Provides | Advantage Over Generic Tools |
|------|-------|-----------------|------------------------------|
| 1 (Structure) | [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | Protein-ion complex structures | Predicts bound ions/lipids critical for channel selectivity |
| 1 (Structure) | [Boltz-2](https://github.com/jwohlwend/boltz) | Open-source, single-GPU | Matches AF3 accuracy without cloud dependency |
| 1 (Structure) | [Protenix](https://github.com/bytedance/protenix) | Apache 2.0 AF3 reproduction | No licensing restrictions for integration |
| 1→2 (Dynamics) | [BioEmu-1](https://github.com/microsoft/BioEmu) | Conformational ensembles at 100,000x MD speed | Directly predicts gating transitions (open ↔ closed states) |
| 2 (Embeddings) | [ESM Cambrian](https://github.com/evolutionaryscale/esm) | Protein language model (300M-6B params) | Outperforms ESM-2; captures functional properties from sequence alone |
| 2 (Embeddings) | [SaProt](https://github.com/westlake-repl/saprot) | Structure-aware protein LM | Combines sequence + 3Di structural tokens; better for mutation effects |

**BioEmu-1 is particularly significant** for Step 2: instead of training a separate ML predictor on the small dataset of ~50-100 channels with known kinetics, BioEmu-1 can directly simulate the gating dynamics of any predicted channel structure and extract V_half, slope, and tau from the conformational landscape. This converts the problem from "learn kinetics from sparse data" to "simulate kinetics from abundant structures."

### Implementation

```python
import esm  # Meta/CZI protein language model

class ChannelKineticsPredictor(torch.nn.Module):
    """Predicts HH parameters from protein sequence embedding."""

    def __init__(self):
        super().__init__()
        self.esm_model = esm.pretrained.esm2_t33_650M_UR50D()
        self.predictor = torch.nn.Sequential(
            torch.nn.Linear(1280, 256),  # ESM2 embedding dim
            torch.nn.ReLU(),
            torch.nn.Linear(256, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 8),  # V_half_m, k_m, tau_m, V_half_h, k_h, tau_h, g_max_scale, E_rev
        )

    def forward(self, protein_sequence):
        embedding = self.esm_model(protein_sequence)
        hh_params = self.predictor(embedding.mean(dim=1))  # Pool over residues
        return hh_params

# Predict kinetics for C. elegans K_slow channel (egl-36)
egl36_sequence = load_wormbase_sequence("egl-36")
predicted_params = predictor(egl36_sequence)
# → V_half_m=-22mV, k_m=5.3, tau_m=12ms, ...
# Feed directly into DD001 HH model
```

### Training Data for Kinetics Prediction

Approximately 50-100 ion channels across species have both:

- Known 3D structures (from X-ray crystallography or cryo-EM)
- Known HH kinetic parameters (from patch-clamp electrophysiology)

This is a small dataset but focused. Transfer learning from protein language model representations helps. The key channels to get right:

| Channel Family | C. elegans Gene | Mammalian Homolog | Known Kinetics? |
|---------------|-----------------|-------------------|-----------------|
| Voltage-gated K+ (Kv) | egl-36, kvs-1, shk-1 | Kv1-Kv12 | Yes (mammalian) |
| Voltage-gated Ca2+ (Cav) | egl-19, unc-2, cca-1 | Cav1-Cav3 | Yes (mammalian) |
| Ca-activated K+ (KCa) | slo-1, slo-2 | BK, SK | Yes |
| Leak (K2P) | twk-* family | TASK, TREK | Partial |
| TRP channels | osm-9, ocr-* | TRPV, TRPA | Partial |

### Strategic Importance

This pipeline creates a direct dependency on CZI's ESM and DeepMind's AlphaFold. The pitch to funders becomes:

> "We don't compete with your foundation models — we *consume* them. Your ESM3 predicts our channel kinetics. Our mechanistic simulation is the testbed that validates whether your predictions produce real organism behavior. Fund us, and we provide the multi-scale benchmark that proves your models work."

---

## Validation

Predicted parameters are validated in two ways:

1. **Cross-validation on known channels (Phase A):** Leave-one-out cross-validation on ~50-100 channels with known kinetics. Train on 80%, predict on 20%, compare predicted vs. measured HH parameters. Target: <30% relative error.

2. **End-to-end validation (Phase 1):** Insert predicted per-neuron-class parameters into the full simulation. Run [DD010](DD010_Validation_Framework.md) validation. If Tier 2 functional connectivity is not degraded below acceptance thresholds, the pipeline is adding value.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source | Variable | Format | Units |
|-------|--------|----------|--------|-------|
| Ion channel gene sequences | WormBase | Protein sequences for *C. elegans* ion channels | FASTA | amino acids |
| CeNGEN expression data | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Per-class transcript levels | CSV | TPM |
| Known channel kinetics (training set) | Published electrophysiology + PDB | ~50-100 channels with measured HH params | CSV | mV, ms, mS/cm² |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Predicted channel kinetics | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Per-channel HH parameters (V_half, k, tau) | CSV | mV, ms, mS/cm² |
| Per-neuron-class HH parameters | [DD001](DD001_Neural_Circuit_Architecture.md) | Per-class conductances from sequence + expression | CSV / YAML | mS/cm², mV, ms |
| Cross-validation report | Internal | Predicted vs. measured, error metrics | JSON | mixed |

### Configuration (`openworm.yml` Section)

```yaml
ml:
  # DD025: Foundation model parameters
  foundation_params: false         # Use structure-predicted channel kinetics
  esm_model: "esm2_t33_650M"
  kinetics_predictor: "models/channel_kinetics_v1.pt"
```

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| CeNGEN data | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) / [DD008](DD008_Data_Integration_Pipeline.md) | If expression data versioning changes, per-class predictions change |
| HH equations | [DD001](DD001_Neural_Circuit_Architecture.md) | If channel model equations change, predicted parameters must be remapped |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Cell-type specialization (if using predicted kinetics) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | If predicted conductances change, per-class models change |
| Neural circuit (if using per-class params) | [DD001](DD001_Neural_Circuit_Architecture.md) | If per-class parameters change, simulation behavior changes |

---

## Boundaries (Explicitly Out of Scope)

1. **Differentiable simulation backend:** That is [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 1 (Phase 3).
2. **SPH surrogate model:** That is [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 2 (Phase 3).
3. **Learned sensory transduction:** That is [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 (Phase 3).
4. **Replacing DD005's CeNGEN approach:** DD025 runs in parallel. If DD005's power-law scaling works, DD025 predictions serve as independent validation. If DD005 fails for certain neuron classes, DD025 predictions substitute immediately.
5. **Neuropeptide-GPCR binding affinity:** That is [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)'s use of foundation models for a different application.

---

## Implementation Roadmap

### Phase A: Cross-Validation (~20 hours)

1. **Curate training data:** Collect ~50-100 channels with both known structure (PDB) and known HH kinetics (electrophysiology literature)
2. **Set up inference pipeline:** ESM embeddings + BioEmu-1 conformational sampling for *C. elegans* channel sequences
3. **Run cross-validation:** Leave-one-out on known channels, report relative error on V_half, slope, tau
4. **Deliverable:** `channel_kinetics_predictions.csv` + `cross_validation_report.json`

### Phase 1: Integration with DD005 (~12 hours)

1. **Generate per-neuron-class parameters:** Combine DD025 kinetics predictions with CeNGEN expression to produce per-class HH parameter sets
2. **Feed into DD005 calibration:** DD025 predictions serve as structure-informed priors where electrophysiology is unavailable
3. **End-to-end validation:** Insert predicted parameters into simulation, run [DD010](DD010_Validation_Framework.md) Tier 2 + Tier 3
4. **Deliverable:** `per_class_hh_params.csv` integrated into DD005 pipeline

---

## Quality Criteria

1. **Cross-validation:** Leave-one-out cross-validation on known channels must achieve < 30% relative error on HH parameters.
2. **End-to-end:** Predicted parameters inserted into the full simulation must not degrade [DD010](DD010_Validation_Framework.md) Tier 2 or Tier 3 scores below acceptance thresholds.
3. **Reproducibility:** All predictions must be reproducible from sequence input alone (no manual tuning).
4. **Provenance:** Each predicted parameter must track which foundation model and version produced it.

---

## Relationship to DD005 and DD017

**DD005 (Cell-Type Specialization):** DD025 does not replace the CeNGEN expression-based approach — it runs in parallel. If DD005's power-law scaling works, DD025 predictions serve as independent validation. If DD005 fails for certain neuron classes, DD025 predictions substitute immediately.

**DD017 (Hybrid ML Framework):** DD025 was originally DD017 Component 3. Components 1 (differentiable backend), 2 (SPH surrogate), and 4 (learned sensory) remain in DD017 as Phase 3 work. DD025 was extracted because it has no infrastructure dependencies and derisks DD005's uncertain mapping.

---

## References

1. **Jumper J et al. (2021).** "Highly accurate protein structure prediction with AlphaFold." *Nature* 596:583-589.
   *Structure prediction for channel kinetics pipeline.*

2. **Lin Z, Akin H, Rao R, et al. (2023).** "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science* 379:1123-1130.
   *ESM2/ESM3 protein language model.*

3. **Wohlwend J et al. (2025).** "Boltz-2: Open-source, single-GPU protein structure prediction." *GitHub.*
   *Open-source alternative to AlphaFold 3.*

4. **Zheng S et al. (2025).** "BioEmu-1: Protein conformational ensembles at 100,000x MD speed." *Microsoft Research.*
   *Key enabler — makes channel dynamics prediction feasible at scale.*

5. **Taylor SR et al. (2021).** "Molecular topography of an entire nervous system." *Cell* 184:4329-4347.
   *CeNGEN database — source of ion channel expression data.*

---

- **Approved by:** Pending
- **Implementation Status:** Proposed
- **Next Actions:**

1. Curate training dataset: ~50-100 channels with known structure + kinetics
2. Download *C. elegans* ion channel sequences from WormBase
3. Set up ESM + BioEmu-1 inference pipeline
4. Run cross-validation, assess error rates
5. If <30% error: generate per-neuron-class predictions for DD005 integration
