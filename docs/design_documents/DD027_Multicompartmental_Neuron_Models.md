# DD027: Multicompartmental Neuron Models

- **Status:** Proposed
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-24
- **Supersedes:** None
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit Architecture), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization), [DD010](DD010_Validation_Framework.md) (Validation Framework), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Hybrid ML), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (Connectome Data Access), [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition)

---

## TL;DR

Some *C. elegans* neurons require multicompartmental cable equation models — single-compartment (isopotential) approximations miss compartmentalized calcium signals (RIA) and all-or-none action potentials (AWA). This DD specifies how to build Level D multicompartmental models for a subset of neurons, starting with 5 representative neurons (AWC, AIY, AVA, RIM, VD5) and scaling to all 302, using existing NeuroML morphologies and ion channel libraries.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 2](DD_PHASE_ROADMAP.md) (Stage 1: 5 neurons), Phase 4-5 (Stage 2: all 302) |
| **Layer** | Neural Architecture Extension |
| **What does this produce?** | Multicompartmental NeuroML neuron models with per-segment channel densities and spatially resolved synapses |
| **Success metric** | Level D neurons reproduce published I-V curves and compartmentalized calcium dynamics (Hendricks 2012, Nicoletti 2019) |
| **Where is the code?** | `openworm/c302` (parameters_D.py framework, morphologies/, channel_models/) |
| **Quick start** | See [Getting Started](#getting-started) below |

---

## Biological Motivation

Experimental evidence shows that single-compartment (isopotential) models are insufficient for a subset of *C. elegans* neurons:

1. **Compartmentalized calcium dynamics (RIA).** [Hendricks et al. (2012)](https://doi.org/10.1038/nature11081) demonstrated that calcium dynamics in the RIA interneuron are compartmentalized across distinct segments of the neurite, encoding head movement direction through spatially separated signals within a single cell.

2. **All-or-none action potentials (AWA).** [Liu et al. (2018)](https://doi.org/10.1016/j.cell.2018.08.018) showed that AWA olfactory neurons fire calcium-mediated all-or-none action potentials — a fundamentally different signaling mode from the graded potentials assumed by Level C1.

These findings indicate that model complexity must vary among neurons: some are well-described by the single-compartment approximation, while others require multicompartmental representations that capture signal propagation along neurites.

---

## Technical Approach

### NeuroML Multicompartmental Support

**NeuroML 2 natively supports multicompartmental morphologies.** The `<cell>` element can contain a `<morphology>` with multiple `<segment>` elements organized into `<segmentGroup>` definitions, with per-segment channel density assignments. This means Level D can be implemented within the existing NeuroML/LEMS framework without a new file format — the same `jnml -validate` pipeline applies, and the same NEURON simulator backend can execute multicompartmental cells alongside single-compartment ones in the same network simulation ([Cannon et al. 2014](https://doi.org/10.3389/fninf.2014.00079); [Gleeson et al. 2018](https://doi.org/10.1098/rstb.2017.0379)).

### Feasibility (Zhao et al. 2024)

Zhao et al. (2024) showed that the "representative neuron" strategy makes multicompartmental modeling tractable at scale: build detailed models for a small set of representative neurons (one per functional group), fit them to published electrophysiology, then propagate fitted parameters to all neurons in the same functional class. Using this approach with 5 representative neurons (AWC, AIY, AVA, RIM, VD5), they produced 136 multicompartmental neurons whose I-V curves matched experimental recordings. Nicoletti et al. (2019) earlier demonstrated a similar multicompartmental approach for AWCon with multiple ion channel types. This establishes that Level D is achievable with current data — it does not require waiting for new experimental techniques.

### Code Reuse Opportunity

The BAAIWorm repository ([github.com/Jessie940611/BAAIWorm](https://github.com/Jessie940611/BAAIWorm), Apache 2.0 license) contains NMODL ion channel files and SWC neuron morphology reconstructions. These can be converted to NeuroML format using pyNeuroML's NMODL→NeuroML converter, providing a head start on the channel library expansion and morphological models.

---

## Implementation Pathway

### Stage 1 (Phase 2 — Proof of Concept)

1. Select 5 representative neurons with published morphological reconstructions AND published electrophysiology: AWC (sensory), AIY (interneuron), AVA (command interneuron), RIM (interneuron), VD5 (motor neuron) — the same set validated by Zhao et al. (2024)
2. Obtain morphologies from EM reconstructions (Witvliet et al. 2021; Cook et al. 2019) or from BAAIWorm SWC files; convert to NeuroML `<morphology>` elements with segments < 2 μm
3. Assign per-segment channel densities from the Extended Channel Library (14 classes), guided by CeNGEN expression profiles ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) and functional group membership
4. Optimize passive parameters (axial resistance, membrane capacitance) and channel densities using automated fitting ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) differentiable backend or NEURON's built-in optimizer) to match published I-V curves and current-clamp responses
5. Propagate fitted parameters to all neurons in the same CeNGEN functional class, scaling channel densities by expression level ([DD005](DD005_Cell_Type_Differentiation_Strategy.md))

### Stage 2 (Phase 4-5 — Scale to Full Circuit)

1. Extend to all 302 neurons using the representative-neuron approach
2. Incorporate subcellular molecular data from expansion microscopy (Alon et al. 2021; [Shaib et al. 2023](https://doi.org/10.1038/s41587-024-02431-9)) as it becomes available
3. Apply spatially resolved synapse placement (see section below)
4. Infer parameters using data-constrained fitting methods including RNN-based approaches ([Linka et al. 2023](https://doi.org/10.1016/j.actbio.2023.01.055))

### OpenWorm Extensions Beyond Zhao et al.

(a) We target all 302 neurons, not 136; (b) we use NeuroML standard format enabling multi-simulator support and community sharing; (c) we integrate with CeNGEN transcriptomics for principled parameter propagation rather than purely functional-group-based assignment; (d) our models include neuropeptidergic modulation ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) and organ systems ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)) that the locomotion-only circuit does not capture.

---

## Spatially Resolved Synapse Placement

For the single-compartment models (Levels A-C, C1), synapses are abstract neuron-to-neuron connections with no spatial structure — all inputs sum at the single compartment. However, for multicompartmental neurons (Level D), the location of synapses along neurites matters because it determines signal propagation delays, spatial input integration, and the degree to which nearby synapses interact nonlinearly.

Zhao et al. (2024) demonstrated a practical approach: for each connection in the Cook et al. (2019) adjacency matrix, assign a distance along the neurite drawn from an inverse Gaussian distribution fitted to experimental synapse centroid distance measurements from serial-section EM (Witvliet et al. 2021). Each synapse is then placed on the neurite segment closest to the assigned distance. This produces spatially realistic clustering of synapses along neurites, matching the biological organization observed in EM.

OpenWorm will adopt this approach with one improvement: quantitative validation that the constructed distributions match the experimental distributions (as in Zhao et al. Fig. 4B-C), integrated into [DD010](DD010_Validation_Framework.md) Tier 1 as a non-blocking structural validation.

**Applies only when:** `neural.level: D` and `neural.spatial_synapses: true`. For Level C1, synapse placement is irrelevant and this feature is disabled.

**Data requirement:** Synapse centroid distances from Witvliet et al. 2021, to be acquired per [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data Acquisition Pipeline). See also [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) for ConnectomeToolbox data access.

---

## Quality Criteria

1. **Backward compatibility:** Level D neurons must coexist with Level C1 single-compartment neurons in the same network simulation
2. **Biological fidelity:** Per-neuron I-V curves reproduce published electrophysiology within ±15%
3. **Compartmentalized dynamics:** RIA model shows spatially separated calcium signals matching [Hendricks et al. 2012](https://doi.org/10.1038/nature11081)
4. **Structural validation:** Synapse placement distributions match Witvliet et al. 2021 EM measurements ([DD010](DD010_Validation_Framework.md) Tier 1)
5. **Standard format:** All models in NeuroML2 format, passing `jnml -validate`

---

## Validation

Level D neurons must pass all [DD010](DD010_Validation_Framework.md) tiers. Individual cell models should additionally reproduce published I-V curves and compartmentalized calcium dynamics where available (e.g., RIA spatial signals per [Hendricks et al. 2012](https://doi.org/10.1038/nature11081), AWC responses per Nicoletti et al. 2019).

---

## Getting Started

**Prerequisites:** Familiarity with [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit Architecture) — especially the c302 framework, Level C1 baseline, and the Hodgkin-Huxley formulation.

**Key resources:**

1. **c302 Level D framework:** `c302/parameters_D.py` — existing Level D infrastructure with `ChannelDensity` support and `Species` (Ca); currently uses placeholder channels
2. **Existing morphologies:** `CElegansNeuroML/CElegans/generatedNeuroML2/` — all 302 neurons as multicompartmental NeuroML2 cells (also copied into `c302/NeuroML2/`)
3. **Ion channel library:** Nicoletti et al. 2019 NeuroML2 channels at `openworm/NicolettiEtAl2019_NeuronModels/NeuroML2/` (31 channels, validated)
4. **EM morphology data:** Witvliet et al. 2021 and Cook et al. 2019 for synapse centroid distances
5. **BAAIWorm reference:** Per-neuron conductance JSONs at `eworm/components/param/cell/*.json`

**First contribution:** Start with [DD027 Draft Issues](DD027_draft_issues.md) — Issue 14 (evaluate existing morphologies) is the entry point.

---

## Existing Code Resources

| Resource | Repository | What It Provides |
|----------|-----------|-----------------|
| Level D framework | `openworm/c302` (`parameters_D.py`) | Multicompartmental infrastructure, `ChannelDensity`, placeholder channels |
| 302 neuron morphologies | `openworm/CElegansNeuroML` | All neurons as multicompartmental NeuroML2 |
| 31 ion channels (NeuroML2) | `openworm/NicolettiEtAl2019_NeuronModels` | AWCon (16 ch) + RMD (15 ch), validated |
| 22 NMODL channel files | `openworm/NicolettiEtAl2024_MN_IN` | Motor neurons + interneurons |
| 17+ NMODL channels + per-neuron conductances | `Jessie940611/BAAIWorm` | Full channel library + JSON conductance params |
| Morphology data (SWC) | `Jessie940611/BAAIWorm` | HOC files for every neuron |

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source | Variable | Format | Units |
|-------|--------|----------|--------|-------|
| Single-compartment neuron models | [DD001](DD001_Neural_Circuit_Architecture.md) | Level C1 network | NeuroML | — |
| Cell-type-specific conductances | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Per-class channel expression | CSV | TPM → g_max |
| Neuron morphologies (EM) | [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) / Witvliet 2021 | 3D segment coordinates | NeuroML `<morphology>` | µm |
| Synapse centroid distances | [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) / Witvliet 2021 | Distance distributions | CSV | µm |
| Differentiable fitting backend | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) | Parameter optimizer | Python API | — |

**Outputs (What This Subsystem Produces)**

| Output | Consumer | Variable | Format | Units |
|--------|----------|----------|--------|-------|
| Multicompartmental neuron models | [DD001](DD001_Neural_Circuit_Architecture.md) network | Level D cells | NeuroML `<cell>` | — |
| Fitted channel densities | [DD010](DD010_Validation_Framework.md) Tier 1 | Per-segment g_max | NeuroML `<channelDensity>` | S/cm² |
| Spatially placed synapses | [DD001](DD001_Neural_Circuit_Architecture.md) network | Synapse locations | NeuroML `<connection>` with segment refs | µm |
| Validation metrics | [DD010](DD010_Validation_Framework.md) | I-V curve fits | JSON | — |

---

## References

1. Hendricks, M., et al. (2012). "Compartmentalized calcium dynamics in a C. elegans interneuron encode head movement." *Nature*, 487:99-103. [doi:10.1038/nature11081](https://doi.org/10.1038/nature11081)
2. Liu, Q., et al. (2018). "C. elegans AWA olfactory neurons fire calcium-mediated all-or-none action potentials." *Cell*, 175:57-70. [doi:10.1016/j.cell.2018.08.018](https://doi.org/10.1016/j.cell.2018.08.018)
3. Nicoletti, M., et al. (2019). "Biophysical modeling of C. elegans neurons: Single ion currents and whole-cell dynamics of AWCon and RMD." *PLoS ONE*, 14:e0218738. [doi:10.1371/journal.pone.0218738](https://doi.org/10.1371/journal.pone.0218738)
4. Zhao, B., et al. (2024). "MetaWorm: an integrative data-driven model of C. elegans." *Nature Computational Science*, 4:978-990. [doi:10.1038/s43588-024-00738-w](https://doi.org/10.1038/s43588-024-00738-w)
5. Cannon, R. C., et al. (2014). "LEMS: a language for expressing complex biological models in concise and hierarchical form." *Frontiers in Neuroinformatics*, 8:79. [doi:10.3389/fninf.2014.00079](https://doi.org/10.3389/fninf.2014.00079)
6. Gleeson, P., et al. (2018). "c302: a multiscale framework for modelling the nervous system of C. elegans." *Phil. Trans. R. Soc. B*, 373:20170379. [doi:10.1098/rstb.2017.0379](https://doi.org/10.1098/rstb.2017.0379)
7. Witvliet, D., et al. (2021). "Connectomes across development reveal principles of brain maturation." *Nature*, 596:257-261. [doi:10.1038/s41586-021-03778-8](https://doi.org/10.1038/s41586-021-03778-8)
8. Shaib, A. H., et al. (2023). "Expansion microscopy at the nanoscale." *Nature Biotechnology*. [doi:10.1038/s41587-024-02431-9](https://doi.org/10.1038/s41587-024-02431-9)
9. Linka, K., et al. (2023). "A new family of constitutive artificial neural networks towards automated model discovery." *Acta Biomaterialia*. [doi:10.1016/j.actbio.2023.01.055](https://doi.org/10.1016/j.actbio.2023.01.055)

---

- **Approved by:** Pending (awaiting founder review)
- **Implementation Status:** Not started
- **Next Review:** After Phase 2 kickoff
