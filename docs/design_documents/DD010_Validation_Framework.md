# DD010: Validation Framework and Quantitative Benchmarks

- **Status:** Accepted
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** All other DDs (validation applies to all models), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptides — Tier 2b unc-31 validation), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox — Tier 3 validation tool), [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition Pipeline — data sourcing for all tiers)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) |
| **Layer** | Validation — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) |
| **What does this produce?** | Three-tier validation reports: Tier 1 (single-cell electrophysiology), Tier 2 (functional connectivity correlation), Tier 3 (behavioral kinematics via `open-worm-analysis-toolbox` — see [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) |
| **Success metric** | Tier 2a: correlation-of-correlations r > 0.5 vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4); Tier 2b: neuropeptide contribution r > 0.3 (wt-vs-unc-31); Tier 3: 5 kinematic metrics within ±15% of [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) Schafer lab data |
| **Repository** | Validation scripts in `openworm/OpenWorm` meta-repo; Tier 3 tool: [`openworm/open-worm-analysis-toolbox`](https://github.com/openworm/open-worm-analysis-toolbox) ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) |
| **Config toggle** | `validation.run_after_simulation: true`, `validation.tier2_functional_connectivity: true`, `validation.tier2_neuropeptide_unc31: true`, `validation.tier3_behavioral: true` in `openworm.yml` |
| **Build & test** | `docker compose run validate` — runs all enabled tiers, produces `output/validation_report.json` |
| **Visualize** | Validation overlay in [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer: `validation/overlay/` OME-Zarr group shows per-metric pass/fail |
| **CI gate** | Tier 2 blocks PR merge (r < 0.5 = fail); Tier 3 blocks merge to main (>15% deviation = fail) |

---

## Context

OpenWorm's core philosophy, articulated in [Sarma et al. 2016](https://doi.org/10.12688/f1000research.9095.1) "Unit Testing, Model Validation, and Biological Simulation" (*F1000Research*), is that **model validation is a form of testing**. Just as software has unit tests, integration tests, and system tests, biological models must be validated at multiple levels:

- **Single-cell level:** Electrophysiology (voltage, conductance, kinetics)
- **Circuit level:** Functional connectivity (calcium correlations)
- **Behavioral level:** Movement kinematics, pumping, defecation

A simulation that produces movement but fails electrophysiology validation has **passed the behavioral test but failed the mechanistic test**. Both matter.

---

## Decision

### Three-Tier Validation Hierarchy

| Tier | What Is Validated | Validation Data | Acceptance Criteria | Blocking? |
|------|------------------|-----------------|-------------------|-----------|
| **Tier 1: Unit (Single Cell)** | Membrane voltage, conductances, calcium dynamics | [Goodman et al. 2002](https://doi.org/10.1038/4151039a) patch-clamp, [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) single-neuron Ca imaging | Quantitative match within 20% | No (warning) |
| **Tier 2a: Integration (Circuit)** | Functional connectivity, network dynamics | [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain pairwise correlations (wild-type) | Correlation coefficient > 0.5 vs. experimental | Yes (blocks merge) |
| **Tier 2b: Integration (Neuropeptides)** | Neuropeptide modulation effect on functional connectivity | [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) wild-type vs. *unc-31* mutant | Neuropeptide contribution correlation r > 0.3 | Yes (after [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) |
| **Tier 3: System (Behavior)** | Movement kinematics, pumping, defecation | [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) (Schafer lab kinematics), [Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) (pharyngeal EPG), [Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) (defecation) | Statistical match via open-worm-analysis-toolbox | Yes (blocks merge) |
| **Tier 4: Causal (Intervention)** | Perturbation response: ablation, silencing, mutation | Published laser ablation, optogenetics, mutant phenotype data | Direction of effect matches ≥70%; magnitude within ±30% | No (advisory → blocking Phase 3+) |

**Blocking:** A PR that degrades Tier 2 or Tier 3 validation scores cannot be merged without explicit founder approval + justification.

### Tier 1: Single-Cell Validation (Unit Tests)

**For each neuron class with published electrophysiology:**

Run the cell model in isolation (no synaptic inputs, no network effects) with standard voltage-clamp or current-clamp protocols. Compare:

| Property | Measurement | Typical Acceptance Range |
|----------|-------------|-------------------------|
| Resting potential (V_rest) | No current injection | ± 5 mV |
| Input resistance (R_in) | Small current step | ± 30% |
| I-V curve | Voltage ramp | Pearson r > 0.8 |
| Spike threshold | Depolarizing current | ± 10 mV (if applicable) |
| Calcium influx | Depolarization-evoked | ± 40% (noisy measurement) |

**Primary Tier 1 datasets:**

| Neuron(s) | Dataset | What It Provides | Validation Use |
|-----------|---------|------------------|----------------|
| ALM, AVM, PLM (touch receptors) | [Goodman et al. 2002](https://doi.org/10.1038/4151039a), [O'Hagan et al. 2005](https://doi.org/10.1038/nn1362) | Whole-cell patch-clamp: resting potential, I-V curves, MEC-4/DEG-ENaC channel kinetics | Validate touch neuron resting potential, input resistance, mechanoreceptor current amplitude |
| ALM, AVM, PLM (touch receptors) | [Suzuki et al. 2003](https://doi.org/10.1016/S0896-6273(03)00539-7) | In vivo calcium imaging during mechanical stimulation | Validate calcium transient amplitude and kinetics in response to touch |
| AWC (olfactory) | [Chalasani et al. 2007](https://doi.org/10.1038/nature06292) | Calcium imaging with odor presentation, TAX-2/TAX-4 channel characterization | Validate sensory transduction dynamics, OFF-response calcium kinetics |
| ASH (nociceptor) | Hilliard et al. 2004, **WormsenseLab_ASH** repo | Calcium imaging, OSM-9/TRPV channel characterization | Validate polymodal nociceptor response profile |
| AVA (command interneuron) | Lockery lab (Lindsay et al. 2011) | Whole-cell recordings, graded potential dynamics | Validate command interneuron I-V curve, graded (non-spiking) response |
| RIM (motor/modulatory) | Liu et al. 2018 | Calcium imaging + electrophysiology, EGL-19/UNC-2 channels | Validate motor neuron calcium dynamics, channel conductance ratios |
| Pharyngeal neurons (MC, M3) | [Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) | Electropharyngeogram (EPG): extracellular field potentials from pharyngeal muscles and neurons | Validate pharyngeal neuron firing patterns (Phase 3, [DD007](DD007_Pharyngeal_System_Architecture.md)) |

**Coverage:** ~7 neuron classes have direct patch-clamp or detailed calcium imaging data suitable for Tier 1 spot-checks. An additional ~13 classes have partial recordings (single-channel data, calcium responses to specific stimuli) curated in the `openworm/ChannelWorm` ion channel database. See [DD005](DD005_Cell_Type_Differentiation_Strategy.md) Calibration Dataset for the full training set.

**For the ~121 neuron classes without direct electrophysiology:** Tier 1 cannot compare to patch-clamp recordings that don't exist. Instead, we run **expression-consistency checks** — systematic tests that the model's electrical behavior is consistent with its [CeNGEN](https://cengen.org) ([Taylor et al. 2021](https://doi.org/10.1016/j.cell.2021.06.023)) ion channel expression profile. This catches gross errors (e.g., a model with large calcium currents in a neuron that doesn't express calcium channels) without requiring experimental recordings.

**Expression-consistency check: gene → expected electrical property**

For each neuron class, [DD005](DD005_Cell_Type_Differentiation_Strategy.md) maps CeNGEN expression to conductance densities. The following table defines what each major channel gene predicts about the model's electrical behavior:

| CeNGEN Gene | Channel Type | If Highly Expressed (top quartile) | If Not Expressed (<1 TPM) | Model Check |
|-------------|-------------|-----------------------------------|--------------------------|-------------|
| **egl-19** | Cav1 (L-type Ca²⁺) | Large sustained calcium current during depolarization; high resting [Ca²⁺] | No L-type calcium current | Inject +20mV step → measure I_Ca amplitude |
| **unc-2** | Cav2 (P/Q-type Ca²⁺) | Large transient calcium current; fast synaptic release | No P/Q-type current | Voltage ramp → I-V curve shows Ca²⁺ peak |
| **cca-1** | Cav3 (T-type Ca²⁺) | Low-threshold calcium spikes; rebound bursting after hyperpolarization | No rebound activity | Hyperpolarize → release → check for rebound depolarization |
| **shl-1** | Kv4 (A-type K⁺) | Fast transient outward current; delays depolarization onset | No A-type current | Depolarize from -80mV → measure transient K⁺ peak |
| **shk-1** | Kv1 (delayed rectifier K⁺) | Sustained outward current; limits depolarization duration | No sustained K⁺ current | Sustained depolarization → measure steady-state K⁺ current |
| **unc-103** | Kir (inward rectifier) | Inward current at hyperpolarized potentials; stabilizes resting potential | No inward rectification | I-V curve shows inward current below -80mV |
| **twk-18** | TWIK (two-pore leak K⁺) | Low input resistance; hyperpolarized resting potential | High input resistance | Measure R_in and V_rest |
| **osm-9** | TRPV (mechanosensory) | Mechanically-gated inward current (sensory neurons only) | No mechanosensory response | Only in ASH, AWA, etc. — check for presence/absence |

**Systematic validation procedure:**

1. **Rank channels by expression.** For each neuron class, sort its ion channel genes by CeNGEN TPM (transcripts per million). The top 3 expressed channels define the neuron's expected "electrical fingerprint."

2. **Run the model.** Simulate each neuron class in isolation with a standard voltage-clamp protocol (ramp from -100mV to +40mV, 200ms).

3. **Extract current contributions.** Measure the peak current carried by each channel type in the model.

4. **Check rank-order consistency.** The model's current ranking should match the expression ranking:
    - If CeNGEN says `egl-19 >> shl-1 >> unc-2` for neuron X, then the model's L-type Ca²⁺ current should be larger than its A-type K⁺ current, which should be larger than its P/Q-type Ca²⁺ current.
    - Rank-order correlation (Spearman) between expression and model current magnitudes should be positive.

5. **Check qualitative predictions.** Verify the binary checks from the table above:
    - Gene not expressed (<1 TPM) → corresponding current is absent (<1% of total)
    - Gene highly expressed (top quartile) → corresponding current is present and substantial (>10% of total)

**Acceptance criteria (expression-consistency):**

- **Rank-order correlation:** Spearman ρ > 0.5 between CeNGEN expression rank and model current rank, averaged across all 128 neuron classes
- **Absence check:** For genes with <1 TPM expression, the corresponding model current must be <1% of total current in ≥95% of cases
- **Presence check:** For genes in the top quartile of expression, the corresponding model current must be >10% of total current in ≥80% of cases
- **Zero known violations:** No neuron class should have its dominant current type contradicted by CeNGEN (e.g., a neuron dominated by L-type Ca²⁺ current that doesn't express egl-19)

**Testing command:**
```bash
# Run expression-consistency validation across all 128 neuron classes
python scripts/validate_expression_consistency.py \
    --cell_models cells/*.cell.nml \
    --cengen_expression data/CeNGEN_L4_expression.csv \
    --gene_channel_map data/gene_to_channel_map.csv \
    --output validation_report_tier1_consistency.json

# Output: per-neuron rank correlation, absence/presence checks, violations
```

**This is non-blocking** because (a) the expression→conductance calibration ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) is approximate, (b) post-transcriptional regulation means mRNA ≠ protein ≠ membrane conductance, and (c) some channel genes have poorly characterized kinetics. But it catches the most common failure mode: a calibration error that gives a neuron the wrong dominant current type.

**Example (AVA neuron validation — direct electrophysiology):**
```bash
# Run isolated AVA model (one of ~7 neurons with patch-clamp data)
python c302/test_single_cell.py --cell AVACell --protocol voltage_clamp

# Compare to Lockery lab data (Lindsay et al. 2011)
python scripts/validate_single_cell_electrophys.py \
    --simulated AVA_voltage_clamp.csv \
    --experimental data/electrophysiology/AVA_lockery_vclamp.csv \
    --output validation_report_AVA.html
```

**Outcome:** For neurons with electrophysiology: parameter-by-parameter comparison report. If >2 parameters fail (exceed acceptance range), flag for review. For all 128 neurons: expression-consistency report with rank correlations and violation flags.

### Tier 2: Circuit-Level Validation (Integration Tests)

**Primary target:** [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity matrix (pairwise calcium signal correlations for all 302 neurons during spontaneous activity). Available via `wormneuroatlas` API and also integrated into the [ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox) (`cect` package) as one of five connectivity modalities (anatomical, contactome, neurotransmitter, extrasynaptic, **functional**).

#### Tier 2a: Whole-Network Functional Connectivity

**Validation procedure:**

1. Run c302 simulation for 60 seconds (spontaneous activity, no stimulus)
2. Extract calcium time series for all neurons
3. Compute pairwise Pearson correlations → 302×302 matrix
4. Compare to Randi et al. experimental 302×302 matrix
5. Metric: **Correlation of correlations** (Pearson r between simulated and experimental matrices, flattened to vectors)

**Acceptance criterion:**

- **r > 0.5** between simulated and experimental functional connectivity
- At least 70% of neuron pairs have correlation sign agreement (both positive, both negative, or both near-zero)

**Testing command:**
```bash
# Run functional connectivity validation
python scripts/validate_functional_connectivity.py \
    --model c302_C1_Differentiated \
    --duration 60 \
    --experimental_data data/randi2023_functional_connectivity.npy \
    --output func_conn_validation.json

# Check if acceptance criteria pass
python scripts/check_validation_criteria.py func_conn_validation.json
```

**Blocking:** If this test fails (r < 0.5), the PR cannot merge to `main`.

**PCA structure validation (additional Tier 2 metric):** Beyond pairwise correlation matching, the low-dimensional dynamical structure of the neural network should be validated. [Kato et al. (2015)](https://doi.org/10.1016/j.cell.2015.09.034) showed that PCA of whole-brain calcium activity reveals a dominant mode (PC1) that separates forward-locomotion neurons (AVB, PVC, VB, DB classes) from backward-locomotion neurons (AVA, AVD, VA, DA classes). After synaptic weight optimization ([DD001](DD001_Neural_Circuit_Architecture.md)), simulated membrane potential time series should reproduce this PC1 separation. Zhao et al. (2024) demonstrated this validation approach on a 136-neuron circuit; OpenWorm will apply it to the full 302-neuron network.

#### Tier 2b: Neuropeptide Modulation Validation (unc-31 Natural Experiment)

**Purpose:** Validate that [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (neuropeptide modulation) produces the correct effect on functional connectivity.

**The natural experiment:** UNC-31 is the CAPS protein required for dense-core vesicle fusion — the mechanism by which neuropeptides are released. The *unc-31* mutant has intact synaptic transmission but **no neuropeptide signaling**. [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) measured functional connectivity for both wild-type and *unc-31* mutant strains. The **difference** between the two matrices isolates the neuropeptide contribution to neural dynamics.

**Validation procedure:**

| | Experimental (Randi 2023) | Simulated |
|---|---|---|
| **With neuropeptides** | `fc_wt` (wild-type) | `sim_fc_on` (DD006 enabled) |
| **Without neuropeptides** | `fc_unc31` (*unc-31* mutant) | `sim_fc_off` (DD006 disabled) |
| **Neuropeptide contribution** | `fc_diff_exp = fc_wt - fc_unc31` | `sim_fc_diff = sim_fc_on - sim_fc_off` |

**Acceptance criterion:**

- Correlation between `fc_diff_exp` and `sim_fc_diff` (flattened) **r > 0.3**
- This is a weaker threshold than Tier 2a (r > 0.5) because the difference signal is smaller and noisier than the absolute functional connectivity

**Testing command:**
```bash
# Run unc-31 validation (requires two simulation runs)
python scripts/validate_neuropeptide_fc.py \
    --model_with_neuropeptides c302_C1_DD006_enabled \
    --model_without_neuropeptides c302_C1_DD006_disabled \
    --duration 60 \
    --output neuropeptide_fc_validation.json

# Check acceptance
python scripts/check_validation_criteria.py neuropeptide_fc_validation.json
```

**Data access:**
```python
from wormneuroatlas import NeuroAtlas

atlas = NeuroAtlas()
fc_wt = atlas.get_signal_propagation_atlas(strain="wt")
fc_unc31 = atlas.get_signal_propagation_atlas(strain="unc31")
fc_diff_exp = fc_wt - fc_unc31  # Neuropeptide contribution (experimental)
```

**Blocking:** This sub-test becomes blocking after [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) is implemented (Phase 2). Before DD006, it is informational only.

**Cross-reference:** See [DD006 §Validation](DD006_Neuropeptidergic_Connectome_Integration.md#validation-procedure) for the full neuropeptide validation methodology, which uses this same unc-31 comparison as its Tier 1 functional connectivity validation.

### Tier 3: Behavioral Validation (System Tests)

**Primary tool:** `open-worm-analysis-toolbox` (see **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** for toolbox revival plan, WCON format specification, API contract, and version pinning) — compares simulated movement trajectories to [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) Schafer lab experimental data in WCON format.

**Validated metrics:**

1. **Speed:** Mean forward velocity (µm/s)
2. **Wavelength:** Body bend wavelength (µm)
3. **Frequency:** Undulation frequency (Hz)
4. **Amplitude:** Body bend amplitude (degrees)
5. **Crawl/swim classification:** Behavioral mode based on gait

**Acceptance criteria:**

- All 5 metrics within **±15% of experimental mean**
- Movement trajectory visually resembles real worm (qualitative check)

**Testing command:**
```bash
# Run behavioral validation suite
cd open-worm-analysis-toolbox/
python validate_movement.py \
    --simulated ../c302/output/worm_trajectory.wcon \
    --experimental data/schafer_baseline_N2.wcon \
    --output validation_report.json

# Check pass/fail
python check_acceptance.py validation_report.json --tolerance 0.15
```

**Additional behavioral tests:**

1. **Pharyngeal pumping:** 3-4 Hz ([DD007](DD007_Pharyngeal_System_Architecture.md))
2. **Defecation cycle:** 50 ± 10 seconds period ([DD009](DD009_Intestinal_Oscillator_Model.md))
3. **Reversal initiation:** Response to aversive stimulus (<1 second latency)

**Blocking:** If movement validation degrades by >15%, the PR is blocked.

### Tier 4: Causal / Interventional Validation (Non-Blocking, Advisory)

**Rationale:** Tiers 1-3 validate against observational data — recordings from intact, unperturbed animals. However, a model that reproduces normal behavior may do so for the wrong mechanistic reasons (parameter compensation, degenerate solutions). As [Pearl & Mackenzie (2018)](https://www.hachettebookgroup.com/titles/judea-pearl/the-book-of-why/9780465097616/) argue in their framework for causal inference, observational data alone cannot distinguish correlation from causation. To establish that the model captures true causal relationships between neurons, we need to validate against *interventional* data — experiments where specific neurons are ablated, silenced, or activated, and the resulting changes in neural activity and behavior are measured.

**Validation data sources (published):**

| Intervention | Organism Response | Data Source |
|-------------|-------------------|-------------|
| Touch neuron ablation (ALM, AVM, PLM) | Loss of gentle touch response | [Chalfie et al. (1985)](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985), *J Neurosci* 5:956-964 |
| Pharyngeal neuron laser killing | Pumping continues (semi-autonomous organ) | Avery & Horvitz (1989), *Neuron* 3:473-485 |
| Optogenetic activation of specific neurons | Stimulus-specific behavioral responses | Leifer et al. (2011), *Nat Methods* 8:147-152 |
| unc-2 (Cav2) loss of function | Reduced locomotion speed | Schafer lab WCON mutant data |
| egl-1, unc-103 loss of function | Egg-laying phenotypes | Trent et al. (1983), Collins & Koelle (2013) |
| flp peptide knockouts | Altered locomotion patterns | [Rogers et al. (2003)](https://doi.org/10.1038/nn1140), [Li et al. (1999)](https://doi.org/10.1016/S0006-8993(99)01972-1) |

**Validation procedure:** Simulate the specific perturbation (zero out a neuron's output, remove a channel type, delete a peptide gene) and compare the resulting behavioral change to published experimental data. The model should predict the *direction* of the effect (faster/slower, more/fewer reversals) and ideally the *magnitude* within 30%.

**Acceptance criteria:**
- Direction of effect matches experimental observation for ≥70% of tested perturbations
- Magnitude within ±30% for well-characterized perturbations (e.g., touch neuron ablation latency, unc-2 speed reduction)
- Model does not predict catastrophic failure (NaN, divergence) for perturbations that produce viable animals in vivo

**Status:** Non-blocking (advisory) in Phase 1-2. Becomes blocking in Phase 3+ as more subsystems come online and the model makes increasingly specific causal predictions.

**Note:** A growing body of whole-brain perturbation data is being collected by multiple labs using optogenetic stimulation paired with whole-brain imaging across thousands of animals (Randi et al. 2023; Haspel et al. 2023). As these datasets become publicly available, they will provide increasingly powerful Tier 4 validation targets. See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition) for the data sourcing roadmap.

### Standard In-Silico Perturbation Battery

Zhao et al. (2024) demonstrated several informative in-silico perturbation experiments that reveal how network structure shapes dynamics and behavior. OpenWorm should formalize these as a standard perturbation battery that every model version is tested against:

| Perturbation | Expected Effect | Experimental Basis |
|-------------|----------------|-------------------|
| Remove all gap junctions | Greater disruption to correlation matrix than removing chemical synapses | Zhao et al. 2024 Fig. 10D-G; Randi et al. 2023 unc-7 data |
| Remove neurites (soma-only model) | Higher body twisting, degraded forward locomotion | Zhao et al. 2024 Fig. 10B |
| Shuffle synapse locations on neurites | Faster head/tail oscillation, slower forward speed | Zhao et al. 2024 Fig. 10C |
| Ablate AVA bilaterally | Loss of backward locomotion command | [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) |
| Silence all B-class motor neurons | Loss of forward locomotion | Zheng et al. 1999 |
| Block Cav2 (unc-2 null) | Reduced locomotion speed | Schafer lab mutant data |

These perturbation experiments serve dual purposes: (a) validation that the model responds correctly to interventions, and (b) scientific discovery — any unexpected model response identifies a gap in understanding.

### Statistical Grounding for Acceptance Thresholds

The ±15% tolerance used in Tier 3 is grounded in measured inter-animal variability. Yemini et al. (2013) compiled a database of *C. elegans* behavioral phenotypes from thousands of tracked animals and found that wild-type (N2) locomotion metrics typically exhibit coefficients of variation (CV) in the range of 15-25% for speed, body bend amplitude, and wavelength. A model that matches the experimental mean within one CV is performing within the biological noise floor — tighter matching would be overfitting to a specific animal rather than capturing the population behavior.

For Tier 2 (functional connectivity), the r > 0.5 threshold reflects the observation that calcium correlation matrices from independent recording sessions of the same genotype show inter-session correlations in the range of r = 0.6-0.8 (Randi et al. 2023). A model achieving r > 0.5 is thus approaching the reproducibility ceiling of the experimental data itself.

### Behavioral Quantification Methods

Tiers 3 and 4 require robust, unbiased behavioral quantification. The field of computational neuroethology has developed systematic approaches to this challenge:

- **Unsupervised behavioral decomposition** ([Berman et al. 2014](https://doi.org/10.1098/rsif.2014.0672)) identifies stereotyped behavioral motifs from continuous recordings without pre-defined categories, enabling discovery of behavioral states that the model should reproduce
- **Deep learning-based pose estimation** (Pereira et al. 2022, SLEAP) provides sub-pixel body posture tracking that can extract kinematic features more precisely than centroid-only approaches
- **Computational neuroethology frameworks** ([Datta et al. 2019](https://doi.org/10.1016/j.neuron.2019.09.038)) advocate for treating behavior as a high-dimensional continuous signal rather than a set of discrete categories, which aligns with how our simulation outputs movement data

As the validation toolbox ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) is revived, it should incorporate or interface with these modern approaches rather than relying solely on the classic 5-metric kinematic comparison.

---

## Alternatives Considered

### 1. No Quantitative Validation (Visual Inspection Only)

**Rejected:** "It looks right" is subjective. Quantitative metrics enable regression detection and objective comparison between models.

### 2. Single Validation Level (Behavior Only)

**Rejected:** A model can produce correct movement for the wrong reasons (parameter compensation). Multi-level validation (electrophysiology + connectivity + behavior) ensures mechanistic correctness.

### 3. Strict Thresholds (Must Match Exactly)

**Rejected:** Biological data have measurement noise and animal-to-animal variability. ±15-20% tolerance accounts for this. Exact matches are neither achievable nor necessary.

---

## Quality Criteria

1. **Automated Test Suite:** All validation tests must be runnable via CI/CD without manual intervention.

2. **Regression Detection:** Every PR that modifies cell models, connectome, or physics must run the validation suite. Report before/after comparison.

3. **Versioned Experimental Data:** Validation datasets must be versioned and archived (e.g., `data/randi2023_v1.0/`). Do not overwrite.

4. **Pass/Fail Criteria Documented:** Each test must have explicit acceptance criteria (e.g., "r > 0.5," "period = 50 ± 10 s") in the test script, not tribal knowledge.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Neuron calcium time series | [DD001](DD001_Neural_Circuit_Architecture.md) | Per-neuron [Ca²⁺] over time | Tab-separated `*_calcium.dat` | mol/cm³ |
| Single-cell electrophysiology | [DD001](DD001_Neural_Circuit_Architecture.md) | V, I_Ca, I_K per cell | Tab-separated from NEURON | mV, nA |
| Movement trajectory | [DD003](DD003_Body_Physics_Architecture.md) | Body centroid + posture over time | WCON file | µm, frames |
| Pharyngeal pumping state | [DD007](DD007_Pharyngeal_System_Architecture.md) | Per-section contraction time series | Tab-separated | binary or [0,1] |
| Defecation motor program | [DD009](DD009_Intestinal_Oscillator_Model.md) | pBoc/aBoc/Exp timestamps | Event log | ms |
| Experimental data (electrophysiology) | [DD008](DD008_Data_Integration_Pipeline.md) / published papers | Patch-clamp recordings | CSV | mV, nA |
| Experimental data (functional connectivity, wild-type) | `wormneuroatlas` API / [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) | 302×302 correlation matrix | NumPy `.npy` | dimensionless |
| Experimental data (functional connectivity, *unc-31*) | `wormneuroatlas` API / [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) | 302×302 correlation matrix (no neuropeptide release) | NumPy `.npy` | dimensionless |
| Neuropeptide-on/off simulation outputs | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Per-neuron [Ca²⁺] with DD006 enabled vs. disabled | Tab-separated `*_calcium.dat` | mol/cm³ |
| Experimental data (kinematics) | [DD008](DD008_Data_Integration_Pipeline.md) / [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) (Schafer lab) | Movement trajectories | WCON | µm |
| Experimental data (defecation) | [DD008](DD008_Data_Integration_Pipeline.md) / [Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) | Defecation cycle periods | CSV | seconds |
| Experimental data (pumping) | [DD008](DD008_Data_Integration_Pipeline.md) / [Raizen 1994](https://doi.org/10.1016/0896-6273(94)90207-0) | EPG recordings | CSV | mV |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Tier 1 validation report | [DD012](DD012_Design_Document_RFC_Process.md) (PR review) | Per-cell pass/fail + metrics | JSON | mixed |
| Tier 2 validation report | [DD012](DD012_Design_Document_RFC_Process.md) (PR review), [DD013](DD013_Simulation_Stack_Architecture.md) (CI gate) | Correlation-of-correlations score | JSON | dimensionless (r value) |
| Tier 3 validation report | [DD012](DD012_Design_Document_RFC_Process.md) (PR review), [DD013](DD013_Simulation_Stack_Architecture.md) (CI gate) | Per-metric pass/fail (speed, wavelength, frequency, amplitude, gait) | JSON | mixed |
| Regression alert | [DD013](DD013_Simulation_Stack_Architecture.md) (CI pipeline) | Pass/fail + diff from baseline | JSON + exit code | boolean |
| Validation dashboard | Mad-Worm-Scientist (daily digest) | Summary metrics for all tiers | JSON | mixed |
| Validation overlay data (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-metric pass/fail + experimental comparison traces | OME-Zarr: `validation/overlay/` (tier results + reference data) | mixed |

### CI/CD Ownership Split ([DD010](DD010_Validation_Framework.md) vs. [DD013](DD013_Simulation_Stack_Architecture.md))

**[DD010](DD010_Validation_Framework.md) defines WHAT to validate.** [DD013](DD013_Simulation_Stack_Architecture.md) defines HOW to run it in Docker and CI.

| Responsibility | Owned By |
|---------------|----------|
| Validation metrics, acceptance criteria, test scripts | [DD010](DD010_Validation_Framework.md) |
| Docker compose services (`quick-test`, `validate`) | [DD013](DD013_Simulation_Stack_Architecture.md) |
| CI/CD pipeline (GitHub Actions workflow) | [DD013](DD013_Simulation_Stack_Architecture.md) |
| Validation data packaging in Docker image | [DD010](DD010_Validation_Framework.md) + [DD013](DD013_Simulation_Stack_Architecture.md) (shared) |
| Pass/fail decision logic (blocking PRs) | [DD010](DD010_Validation_Framework.md) (criteria) + [DD013](DD013_Simulation_Stack_Architecture.md) (enforcement) |

**Reconciliation:** The `docker compose run validate` service ([DD013](DD013_Simulation_Stack_Architecture.md)) runs the validation scripts defined by [DD010](DD010_Validation_Framework.md). The scripts produce JSON reports. [DD013](DD013_Simulation_Stack_Architecture.md)'s CI pipeline reads those reports and applies [DD010](DD010_Validation_Framework.md)'s acceptance criteria to determine pass/fail.

### Configuration (`openworm.yml` Section)

```yaml
validation:
  run_after_simulation: false         # Set true for CI; false for interactive use
  tier1_electrophysiology: false      # Single-cell validation (requires specific cell models)
  tier2_functional_connectivity: false  # Tier 2a: Circuit-level (requires 60s sim)
  tier2_neuropeptide_unc31: false       # Tier 2b: unc-31 comparison (requires 2×60s sim, DD006)
  tier3_behavioral: false             # Movement kinematics (requires ~5s sim)
  tier3_pumping: false                # Pharyngeal pumping (requires pharynx.enabled + ~5s sim)
  tier3_defecation: false             # Defecation cycle (requires intestine.enabled + ~200s sim)
  acceptance_criteria:
    tier2_min_correlation: 0.5        # Minimum r for functional connectivity
    tier3_max_deviation: 0.15         # Maximum deviation from experimental mean (±15%)
    tier3_pumping_range: [3.0, 4.0]   # Hz
    tier3_defecation_range: [40, 60]  # seconds
```

**Default vs. CI configuration:**

```yaml
# configs/validation_full.yml (used by CI)
validation:
  run_after_simulation: true
  tier2_functional_connectivity: true
  tier3_behavioral: true
```

### Docker Build

- **Repository:** `openworm/open-worm-analysis-toolbox` (movement validation, see [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) + `openworm/tracker-commons` (WCON spec, see [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) + validation scripts in `openworm/OpenWorm` meta-repo
- **Docker stage:** `validation` in multi-stage Dockerfile
- **`versions.lock` keys:** `open_worm_analysis_toolbox`, `tracker_commons` (both managed per [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md))
- **Build dependencies:** `pip install open-worm-analysis-toolbox` + validation data files

### Validation Data Location

All validation datasets are **baked into the Docker image at build time** (not downloaded at runtime):

```
/opt/openworm/validation/data/
├── electrophysiology/
│   ├── goodman1998_touch_neurons.csv
│   ├── lockery_AVA_recordings.csv
│   └── README.md (sources, DOIs, licenses)
├── functional_connectivity/
│   ├── randi2023_wt_matrix.npy
│   ├── randi2023_unc31_matrix.npy
│   ├── randi2023_metadata.json
│   └── README.md
├── kinematics/
│   ├── schafer_N2_baseline.wcon
│   ├── schafer_unc2_mutant.wcon
│   └── README.md
└── behavioral/
    ├── thomas1990_defecation.csv
    ├── raizen1994_pumping_EPG.csv
    └── README.md
```

**Licensing requirement:** All validation data must be openly accessible (CC-BY or equivalent). Each directory includes a README with source DOIs and licenses.

### Code Reuse: wormneuroatlas and ConnectomeToolbox for Tier 2 Validation

Two existing OpenWorm packages provide all the experimental data needed for Tier 2 validation — no manual data extraction required:

**1. wormneuroatlas** — Functional connectivity matrices from [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4)

- **Repository:** `openworm/wormneuroatlas` (pushed 2025-10-22, maintained)
- **Installation:** `pip install wormneuroatlas`

```python
from wormneuroatlas import NeuroAtlas

atlas = NeuroAtlas()

# Tier 2a: Wild-type functional connectivity
fc_wt = atlas.get_signal_propagation_atlas(strain="wt")
# Returns: 302×302 correlation matrix (exactly what Tier 2a needs)

# Tier 2b: unc-31 mutant functional connectivity (no neuropeptide release)
fc_unc31 = atlas.get_signal_propagation_atlas(strain="unc31")
# Returns: 302×302 correlation matrix without neuropeptide modulation

# Tier 2b: Neuropeptide contribution = difference
fc_neuropeptide_contribution = fc_wt - fc_unc31
```

Both wild-type and *unc-31* datasets are production-ready. No manual download from Nature supplement needed — the package handles data access, versioning, and neuron ID normalization.

**2. ConnectomeToolbox (`cect`)** — Unified connectivity data across five modalities

- **Repository:** `openworm/ConnectomeToolbox` ([Gleeson et al., in preparation](https://github.com/openworm/ConnectomeToolbox))
- **Installation:** `pip install cect`

The ConnectomeToolbox aggregates C. elegans connectivity data into a unified API with five modalities: anatomical, contactome, neurotransmitter atlases, extrasynaptic (neuropeptidergic — [Ripoll-Sánchez 2023](https://doi.org/10.1016/j.neuron.2023.09.043), [Bentley 2016](https://doi.org/10.1371/journal.pcbi.1005283), [Pereira 2015](https://doi.org/10.7554/eLife.12432), [Beets 2022](https://doi.org/10.1101/2022.10.30.514428)), and functional ([Randi 2023](https://doi.org/10.1038/s41586-023-06683-4)). For Tier 2 validation, the functional connectivity modality provides an alternative access path to the same Randi 2023 data:

```python
from cect import ConnectomeDataset

# Access functional connectivity via cect
functional = ConnectomeDataset("Randi2023")
```

**Recommendation:** Use `wormneuroatlas` directly for Tier 2 validation (more mature API for functional connectivity matrices, strain-specific access). Use `cect` when you need structural + functional connectivity together (e.g., comparing structural predictions to functional observations).

**Testing:**
```bash
pip install wormneuroatlas
python -c "
from wormneuroatlas import NeuroAtlas
atlas = NeuroAtlas()
fc_wt = atlas.get_signal_propagation_atlas(strain='wt')
fc_unc31 = atlas.get_signal_propagation_atlas(strain='unc31')
print(f'Wild-type FC: {fc_wt.shape}')
print(f'unc-31 FC: {fc_unc31.shape}')
print(f'Neuropeptide contribution matrix: {(fc_wt - fc_unc31).shape}')
"
# Expected: (302, 302) for all three
```

**Action Items:**

- [ ] Add `wormneuroatlas` to [DD013](DD013_Simulation_Stack_Architecture.md) Docker validation stage
- [ ] Add `cect` to [DD013](DD013_Simulation_Stack_Architecture.md) Docker validation stage
- [ ] Pin versions for both in `versions.lock`
- [ ] Update Tier 2a validation scripts to use wormneuroatlas API
- [ ] Implement Tier 2b (unc-31 comparison) validation script after [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)

**Estimated Time Savings:** 15-20 hours (no manual data extraction, both APIs are production-ready)

---

### `open-worm-analysis-toolbox` Revival ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md))

This repo is **dormant** (last commit Jan 2020). **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox and WCON Policy)** owns the full revival plan, including:

- 8-task revival roadmap with owners, effort estimates, and dependencies (~33 hours total)
- Python 3.12 compatibility, dependency updates, test suite fixes
- WCON 1.0 format pinning from `tracker-commons`
- Docker `validation` stage and `versions.lock` entries
- API contract for `NormalizedWorm` and `WormFeatures` classes
- Relationship to Tierpsy Tracker (modern successor)

**See [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) for the complete revival plan.** This is a Phase A ([DD013](DD013_Simulation_Stack_Architecture.md) roadmap) task. Without a working analysis toolbox, Tier 3 validation is impossible.

Note: The archived predecessor repo `openworm/movement_validation` should not be used — it was superseded by the analysis toolbox.

### Integration Test

```bash
# Step 1: Verify validation tools install
docker compose run shell python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
print('Analysis toolbox loaded successfully')
"

# Step 2: Verify validation data is present
docker compose run shell ls /opt/openworm/validation/data/
# Must show: electrophysiology/, functional_connectivity/, kinematics/, behavioral/

# Step 3: Run validation suite (after simulation)
docker compose run validate
# Verify: output/validation_report.json exists
# Verify: report contains tier2 and tier3 sections
# Verify: CI exit code = 0 if all tiers pass, non-zero if any blocking tier fails

# Step 4: Test regression detection
# Modify a parameter known to degrade locomotion
# Run validation
# Verify: Tier 3 fails with specific metric(s) identified
```

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Neural output format | [DD001](DD001_Neural_Circuit_Architecture.md) | If calcium time series format changes, Tier 1 and Tier 2 validators can't read data |
| Neuropeptide on/off toggle | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | If DD006 enable/disable mechanism changes, Tier 2b (unc-31) validation can't run paired simulations |
| Movement output format | [DD003](DD003_Body_Physics_Architecture.md) | If WCON format or particle output changes, Tier 3 movement validator breaks |
| Pharyngeal output format | [DD007](DD007_Pharyngeal_System_Architecture.md) | If pumping state format changes, pumping validation breaks |
| Intestinal output format | [DD009](DD009_Intestinal_Oscillator_Model.md) | If defecation event format changes, defecation validation breaks |
| Experimental data (OWMeta) | [DD008](DD008_Data_Integration_Pipeline.md) | If data provenance or versioning changes, validation baselines may shift |
| Docker compose services | [DD013](DD013_Simulation_Stack_Architecture.md) | If `validate` service configuration changes, validation pipeline breaks |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| CI pipeline (blocking gates) | [DD013](DD013_Simulation_Stack_Architecture.md) | If acceptance criteria change, CI may pass/fail differently |
| PR review (Mind-of-a-Worm) | [DD012](DD012_Design_Document_RFC_Process.md) | Mind-of-a-Worm references [DD010](DD010_Validation_Framework.md) criteria when checking PR compliance |
| Founder digest (Mad-Worm-Scientist) | AI Agents | If validation report format changes, Mad-Worm-Scientist can't parse regression alerts |
| All subsystem DDs | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md) | If a tier's acceptance criteria tighten, previously-passing subsystems may now fail |

---

## Implementation References

### Open-Worm-Analysis-Toolbox

**Repository:**
```
https://github.com/openworm/open-worm-analysis-toolbox
```

> **Note:** The predecessor repo `openworm/movement_validation` is **archived** and should not be used. The analysis toolbox is the current, canonical implementation. See [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) for full repository landscape and revival plan.

**Key modules:**

- `movement_validation/` — Statistical feature extraction from WCON files
- `comparison/` — Compare simulated vs. real
- `wcon_parser/` — WCON format handling

**Usage:**
```python
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures

# Load experimental data
exp_worm = NormalizedWorm.from_schafer_file("schafer_N2_baseline.wcon")
exp_features = WormFeatures(exp_worm)

# Load simulated data
sim_worm = NormalizedWorm.from_simulation("c302_output.wcon")
sim_features = WormFeatures(sim_worm)

# Compare
comparison = exp_features.compare(sim_features)
print(comparison.summary())  # Pass/fail report
```

### Validation Data Repository

```
openworm/validation_data/
├── electrophysiology/
│   ├── goodman1998_touch_neurons.csv
│   ├── lockery_AVA_recordings.csv
│   └── ...
├── functional_connectivity/
│   ├── randi2023_wt_matrix.npy
│   ├── randi2023_unc31_matrix.npy
│   ├── randi2023_metadata.json
│   └── ...
├── kinematics/
│   ├── schafer_N2_baseline.wcon
│   ├── schafer_unc2_mutant.wcon  # Calcium channel mutant
│   └── ...
└── behavioral/
    ├── thomas1990_defecation.csv
    ├── raizen1994_pumping_EPG.csv
    └── ...
```

**Licensing:** All validation data must be openly accessible (CC-BY or equivalent). Cite original publications.

---

## Migration Path

### From Manual Validation to Automated CI

**Current state:** Validation is run manually before major releases.

**Target state (Phase 1):** GitHub Actions CI runs validation suite on every PR to `main`.

**Implementation:**
```yaml
# .github/workflows/validation.yml
name: Model Validation
on: [pull_request]
jobs:
  tier2_functional_connectivity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate c302 network
        run: python c302/CElegans.py C1Differentiated
      - name: Run simulation
        run: jnml LEMS_c302_C1_Differentiated.xml -nogui
      - name: Validate vs. Randi 2023
        run: python scripts/validate_functional_connectivity.py
      - name: Check acceptance
        run: python scripts/check_criteria.py --min_correlation 0.5

  tier3_behavioral:
    runs-on: ubuntu-latest
    steps:
      - name: Run movement validation
        run: cd open-worm-analysis-toolbox && python validate_movement.py
      - name: Check acceptance
        run: python scripts/check_criteria.py --max_deviation 0.15
```

---

## Boundaries (Out of Scope)

1. **Developmental validation:** Validating stage-specific models (L1, dauer, male) is Phase 6 work.
2. **Genetic variation:** Validating against natural isolates (Ben-David eQTLs) is Phase 6+ work.
3. **Pharmacological validation:** Drug effects (aldicarb, levamisole) are future work.

---

### Existing Code Resources

**wormneuroatlas** ([openworm/wormneuroatlas](https://github.com/openworm/wormneuroatlas), PyPI: `pip install wormneuroatlas`, maintained 2025):
Provides direct API access to [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity via `NeuroAtlas.get_signal_propagation_atlas(strain="wt")`, returning the exact 302x302 correlation matrix needed for Tier 2 validation. No manual data download required. **Estimated time savings: 15 hours.**

**neuronal-analysis** ([openworm/neuronal-analysis](https://github.com/openworm/neuronal-analysis), 2017, dormant):
Tools to produce, analyse and compare simulated and recorded neuronal datasets — directly relevant to Tier 1 electrophysiology validation. May contain reusable single-cell comparison scripts.

**owmeta-sciunit** ([openworm/owmeta-sciunit](https://github.com/openworm/owmeta-sciunit), 2021):
OWMeta-integrated SciUnit types providing formalized Tier 1 single-cell validation test classes with Z-scores, pass/fail, and goodness-of-fit metrics. Recommended tooling for automating Tier 1 electrophysiology validation in CI ([DD013](DD013_Simulation_Stack_Architecture.md)).

**worm-functional-connectivity** ([openworm/worm-functional-connectivity](https://github.com/openworm/worm-functional-connectivity), 2023):
Alternative/supplementary source for Tier 2 functional connectivity matrices. Check if it includes unc-31 neuropeptide-deficient mutant data alongside wild-type.

**NicolettiEtAl2024_MN_IN** + **NicolettiEtAl2019_NeuronModels** ([openworm/NicolettiEtAl2024_MN_IN](https://github.com/openworm/NicolettiEtAl2024_MN_IN), [openworm/NicolettiEtAl2019_NeuronModels](https://github.com/openworm/NicolettiEtAl2019_NeuronModels)):
Published HH parameter fits for motor neurons, interneurons, AWCon, and RMD. Expand the Tier 1 calibration set beyond the current ~20 neurons.

---

## References

1. **[Sarma et al. 2016](https://doi.org/10.12688/f1000research.9095.1)** — "Unit testing, model validation, and biological simulation." *F1000Research* 5:1946.
2. **[Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4)** — "Neural signal propagation atlas of *Caenorhabditis elegans*." *Nature* 623:406-414.
3. **[Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560)** — "A database of *Caenorhabditis elegans* behavioral phenotypes." *Nature Methods* 10:877-879.
4. **[Goodman et al. 2002](https://doi.org/10.1038/4151039a)** — "Active currents regulate sensitivity and dynamic range in *C. elegans* neurons." *Nature* 415:1039-1042.
5. **[Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0)** — "Electrical activity and behavior in the pharynx of *Caenorhabditis elegans*." *Neuron* 12:483-495.
6. **[Thomas 1990](https://doi.org/10.1093/genetics/124.4.855)** — "The defecation motor program of *Caenorhabditis elegans*." *Genetics* 124:855-872.
7. **[Gleeson et al., in preparation](https://github.com/openworm/ConnectomeToolbox)** — "ConnectomeToolbox: a unified software framework for *C. elegans* connectivity data." (Manuscript in preparation; `cect` Python package published.)
8. **[Ripoll-Sánchez et al. 2023](https://doi.org/10.1016/j.neuron.2023.09.043)** — "The neuropeptidergic connectome of *C. elegans*." *Neuron* 111:3570-3589. (Extrasynaptic connectivity data in ConnectomeToolbox.)
9. **[Pereira et al. 2015](https://doi.org/10.7554/eLife.12432)** — "A cellular and regulatory map of the cholinergic nervous system of *C. elegans*." *eLife* 4:e12432. (Peptide co-expression data in ConnectomeToolbox.)
10. **Pearl J, Mackenzie D (2018).** [*The Book of Why: The New Science of Cause and Effect.*](https://www.hachettebookgroup.com/titles/judea-pearl/the-book-of-why/9780465097616/) Basic Books (ISBN: 978-0465097609). *Theoretical framework for causal inference — observational data is insufficient for validating causal models; interventional data (perturbations) is required.*
11. **[Berman GJ, Choi DM, Bialek W, Shaevitz JW (2014).](https://doi.org/10.1098/rsif.2014.0672)** "Mapping the stereotyped behaviour of freely moving fruit flies." *J R Soc Interface* 11:20140672. *Unsupervised behavioral decomposition — systematic approach to identifying behavioral motifs from continuous recordings.*
12. **[Pereira TD et al. 2022](https://doi.org/10.1038/s41592-022-01426-1)** — "SLEAP: A deep learning system for multi-animal pose estimation." *Nature Methods* 19:486-495. *Deep learning pose estimation for high-precision behavioral quantification.*
13. **[Datta SR, Anderson DJ, Branson K, Perona P, Leifer A (2019).](https://doi.org/10.1016/j.neuron.2019.09.038)** "Computational neuroethology: a call to action." *Neuron* 104:11-24. *Framework for treating behavior as a high-dimensional continuous signal — relevant to how we quantify simulated vs. real movement.*
14. **[Chalfie M, Sulston JE, White JG, Southgate E, Thomson JN, Brenner S (1985)](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985).** "The neural circuit for touch sensitivity in *Caenorhabditis elegans*." *J Neurosci* 5:956-964. *Foundational touch neuron ablation data — Tier 4 causal validation target.*
15. **Haspel G et al. (2023).** "To reverse engineer an entire nervous system." *arXiv* [q-bio.NC] 2308.06578. *White paper on observational and perturbational completeness in C. elegans neuroscience — motivates Tier 4 validation.*
16. **[Kato S, Kaplan HS, Schrodel T, Skora S, Lindsay TH, Yemini E, Lockery S, Zimmer M (2015).](https://doi.org/10.1016/j.cell.2015.09.034)** "Global brain dynamics embed the motor command sequence of *Caenorhabditis elegans*." *Cell* 163:656-669. *Whole-brain calcium imaging showing PCA structure of neural dynamics — PC1 separates forward vs. backward locomotion command neurons.*
17. **Zhao M, Wang N, Jiang X, et al. (2024).** "An integrative data-driven model simulating *C. elegans* brain, body and environment interactions." *Nature Computational Science* 4(12):978-990. *MetaWorm model — 136-neuron circuit with neurite-level spatial detail, demonstrates PCA validation, gap junction perturbation, and closed-loop chemotaxis.*

---

- **Approved by:** OpenWorm Steering
- **Implementation Status:** Partial

- **Tier 1** (single-cell electrophysiology): Scripts exist but not automated (non-blocking currently)
- **Tier 2a** (functional connectivity): [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) data accessible via `wormneuroatlas` API — no manual ingestion needed (blocking)
- **Tier 2b** (neuropeptide unc-31 comparison): [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) *unc-31* data also in `wormneuroatlas` — blocked on [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) implementation (Phase 2)
- **Tier 3** (behavioral kinematics): **BLOCKED** — `open-worm-analysis-toolbox` is dormant (last commit Jan 2020, broken on Python 3.12)

**See [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox and WCON Policy)** for the complete toolbox revival plan (8 tasks, ~33 hours). Tier 3 validation cannot run until the toolbox is revived and installable on Python 3.12.

**Next Actions:**

1. **URGENT:** Prioritize [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) toolbox revival as Phase A work (parallel with [DD013](DD013_Simulation_Stack_Architecture.md))
2. Appoint Validation L4 Maintainer to own revival (see ClickUp task 868hjdzqy)
3. Add `wormneuroatlas` + `cect` to Docker validation stage — [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) data is already accessible via API (no manual ingestion needed)
4. After [DD006](DD006_Neuropeptidergic_Connectome_Integration.md): Implement Tier 2b (unc-31 comparison) validation script
5. After [DD013](DD013_Simulation_Stack_Architecture.md): Implement Steps 4-5 in `master_openworm.py` (validation pipeline)
6. Set up GitHub Actions CI with Tier 2a+2b+3 blocking gates
