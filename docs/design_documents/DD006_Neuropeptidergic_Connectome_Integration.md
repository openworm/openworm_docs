# DD006: Neuropeptidergic Connectome Integration (Extrasynaptic Signaling Layer)

**Status:** Proposed (Phase 2)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** None  
**Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell Differentiation)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | NeuroML `<peptideRelease>` + `<peptideReceptor>` components for 31,479 peptide-receptor interactions; conductance modulation layer |
| **Success metric** | ≥3 peptide knockout phenotypes reproduced within 30% error ([DD010](DD010_Validation_Framework.md) Tier 3); wild-type kinematics not degraded |
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) — issues labeled `dd006` |
| **Config toggle** | `neural.neuropeptides: true` / `neural.peptide_dataset: "RipollSanchez2023"` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` with `neuropeptides: false` (backward compat), then `neuropeptides: true` |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `neuropeptides/concentrations/` layer — volumetric peptide concentration fields; `neuropeptides/release_events/` for per-neuron release timing |
| **CI gate** | Tier 3 kinematic validation blocks merge; conductance modulation must stay in [0.5, 3.0] range |

---

## TL;DR

Add 31,479 neuropeptide-receptor interactions (Ripoll-Sanchez 2023) as a slow modulatory layer on top of fast synaptic transmission. Only 5% overlap with the synaptic connectome — this is an orthogonal signaling network that governs slow behavioral states (arousal, stress, dwelling/roaming). Success: at least 3 peptide knockout phenotypes reproduced within 30% error.

---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Peptide knockout phenotype reproduction | ≥3 known knockouts within 30% quantitative error | Tier 3 (blocking) |
| **Secondary:** Wild-type kinematic preservation | Within ±15% of baseline (peptides modulate, not destroy, locomotion) | Tier 3 (blocking) |
| **Tertiary:** Conductance modulation range | All modulation factors in [0.5, 3.0] | Tier 1 (non-blocking) |

**Before:** 302 neurons connected only by ~5,000 chemical synapses and ~900 gap junctions — fast transmission only, no slow modulatory layer.

**After:** 31,479 neuropeptide-receptor interactions layered on top, providing seconds-timescale conductance modulation via GPCR-mediated signaling. Each neuron class expresses ~23 peptide genes and ~36 receptors.

---

## Deliverables

| Artifact | Path (relative to `openworm/c302`) | Format | Example |
|----------|-------------------------------------|--------|---------|
| PeptideRelease LEMS component type | `lems/PeptideReleaseDynamics.xml` | NeuroML 2 / LEMS XML | `<ComponentType name="peptideRelease">` |
| PeptideReceptor LEMS component type | `lems/PeptideReceptorDynamics.xml` | NeuroML 2 / LEMS XML | `<ComponentType name="peptideReceptor">` |
| Neuropeptidergic adjacency CSV | `data/neuropeptidergic_connectome.csv` | CSV (31,479 rows) | `AVAL,AVAR,flp-1,npr-1,short,excitatory,8.2` |
| Extended c302 cell templates | `cells/{NeuronClass}Cell.cell.nml` | NeuroML 2 XML | `<peptideRelease id="flp1_release" .../>` added to cell |
| Differentiated network with peptides | `examples/generated/LEMS_c302_C1_DifferentiatedWithPeptides.xml` | LEMS XML | (generated, not committed) |
| Peptide concentration fields (viewer) | OME-Zarr: `neuropeptides/concentrations/`, shape (n_timesteps, n_peptides, n_spatial_bins) | OME-Zarr volumetric | Per-peptide concentration over time |
| Peptide release events (viewer) | OME-Zarr: `neuropeptides/release_events/` | OME-Zarr event series | Per-neuron release timestamps (ms) |

Each LEMS extension includes metadata:
```xml
<notes>
  Data source: Ripoll-Sanchez et al. 2023, Neuron 111:3570-3589
  DOI: 10.1016/j.neuron.2023.07.002
  Interaction count: 31,479
  Distance categories: short (<10 um), mid (10-50 um), long (>50 um)
</notes>
```

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/c302`](https://github.com/openworm/c302) |
| **Issue label** | `dd006` |
| **Milestone** | Phase 2: Neuropeptidergic Signaling |
| **Branch convention** | `dd006/description` (e.g., `dd006/flp-proof-of-concept`) |
| **Example PR title** | `DD006: Add FLP peptide release/receptor LEMS components (Stage 1)` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pyNeuroML, jnml, pandas, numpy
- Ripoll-Sanchez Table S1 data (downloaded to `data/`)

### Step-by-step

```bash
# Step 1: Download Ripoll-Sanchez Table S1 and convert to CSV
# Data goes into c302/data/neuropeptidergic_connectome.csv
# [MANUAL] — download from Neuron journal supplementary data

# Step 2: Generate network with neuropeptides
python c302/CElegans.py C1DifferentiatedWithPeptides
# Expected output: LEMS_c302_C1_DifferentiatedWithPeptides.xml

# Step 3: Run simulation
jnml LEMS_c302_C1_DifferentiatedWithPeptides.xml -nogui

# Step 4: Quick validation — backward compatibility (must pass before PR)
docker compose run quick-test   # with neuropeptides: false
# Green light: identical output to pre-peptide baseline

# Step 5: Quick validation — peptide-enabled (must pass before PR)
# (set neural.neuropeptides: true in openworm.yml)
docker compose run quick-test
# Green light: simulation completes within 2.5x baseline time
# Green light: no NaN values in peptide concentration variables
# Green light: conductance modulation factors in [0.5, 3.0] range

# Step 6: Full validation (must pass before merge)
docker compose run validate
# Green light: Tier 3 kinematic metrics within ±15%
# Green light: ≥3 peptide knockout phenotypes within 30% error

# Step 7: Peptide knockout validation
python c302/CElegans.py C1DifferentiatedWithPeptides --knockout flp-1,flp-2,flp-3
jnml LEMS_c302_C1_DifferentiatedWithPeptides_flp_knockout.xml -nogui
python scripts/validate_knockout.py \
    --simulated flp_knockout_behavior.csv \
    --experimental data/flp_knockout_phenotypes.csv \
    --metrics speed,reversal_frequency \
    --tolerance 0.3
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/extract_behavior.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/validate_peptide_effects.py` | `[TO BE CREATED]` | openworm/c302#TBD |
| `scripts/validate_knockout.py` | `[TO BE CREATED]` | openworm/c302#TBD |

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layers:** Neuropeptide concentration fields and release events.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer 1** | `neuropeptides/concentrations/` — volumetric peptide concentration fields |
| **Layer 2** | `neuropeptides/release_events/` — per-neuron release timing markers |
| **Color mapping** | Concentrations: cool-to-warm colormap (blue=low → red=high peptide concentration); Release events: discrete pulse markers |
| **Data source** | OME-Zarr: `neuropeptides/concentrations/`, shape (n_timesteps, n_peptides, n_spatial_bins); `neuropeptides/release_events/` for per-neuron timestamps |
| **What you should SEE** | Slow waves of peptide concentration building over seconds (not milliseconds). Release events correlated with calcium spikes but with longer temporal footprint. Short-range peptides visible only near source; long-range peptides spread across body regions. |
| **Comparison view** | Side-by-side: synaptic-only model (fast, sparse activity) vs. synaptic+peptide model (slow modulatory waves overlaid on fast dynamics) |

---

## Technical Approach

### Add Neuropeptidergic Signaling as a Second Coupling Layer

Layer the extrasynaptic connectome on top of the synaptic connectome without replacing or modifying the existing fast synaptic transmission ([DD001](DD001_Neural_Circuit_Architecture.md)). Each neuron will have:

1. **Fast synaptic inputs** ([DD001](DD001_Neural_Circuit_Architecture.md): graded synapses, ~ms timescale)
2. **Gap junction inputs** ([DD001](DD001_Neural_Circuit_Architecture.md): electrical coupling)
3. **Neuropeptide inputs** (this DD: slow modulatory, ~seconds timescale)

### Modeling Framework

**Peptide release (presynaptic):**
```
d[peptide]_released/dt = k_release * H([Ca²⁺]ᵢ - threshold) - [peptide]_released / tau_release
```

Where:

- H(x) = Heaviside step function (1 if x > 0, else 0)
- k_release = release rate constant
- threshold = [Ca²⁺]ᵢ level that triggers release (~2x baseline, matching synaptic vesicle release)
- tau_release = peptide clearance time constant (~10-100 seconds, slow compared to synaptic transmission)

**Spatial diffusion (simplified):**

Rather than solving full 3D diffusion PDEs (computationally expensive), use **distance-dependent attenuation** based on the Ripoll-Sanchez distance categories:

```
[peptide]_at_target = [peptide]_released * exp(-distance / lambda)
```

Where:

- distance = Euclidean distance between source and target cell (from WormAtlas 3D positions)
- lambda = diffusion length constant:
  - Short-range: lambda = 5 um (steep decay)
  - Mid-range: lambda = 20 um (moderate decay)
  - Long-range: lambda = 100 um (slow decay)

**Receptor activation (postsynaptic):**

Neuropeptide receptors are **G-protein coupled receptors (GPCRs)** that modulate ion channel conductances via second messengers (cAMP, IP3, DAG). Full biochemical modeling is complex. Use a **simplified phenomenological model**:

```
d[receptor]_active/dt = k_on * [peptide]_at_target * (1 - [receptor]_active) - k_off * [receptor]_active
```

Where:

- k_on = binding rate constant (~10^3 M^-1 s^-1, typical for GPCRs)
- k_off = unbinding rate constant (~0.1-1 s^-1, giving seconds-to-minutes timescale)

**Conductance modulation:**

Activated receptors modulate existing ion channels:

```
g_effective = g_baseline * (1 + modulation_factor * [receptor]_active)
```

Where:

- modulation_factor is receptor-specific:
  - Excitatory peptides (e.g., FLP neuropeptides): increase g_Ca or decrease g_K -> depolarization
  - Inhibitory peptides: increase g_K -> hyperpolarization
  - Values: typically +/-0.2 to +/-2.0 (20% to 200% modulation)

### Data Structure: Neuropeptidergic Adjacency Matrix

Extend the ConnectomeToolbox to include a third connection type:

| Connection Type | Matrix Dimensions | Entries | Timescale |
|----------------|------------------|---------|-----------|
| Chemical synapses | 302 x 302 | ~5,000 | Milliseconds |
| Gap junctions | 302 x 302 | ~900 | Instantaneous |
| **Neuropeptides** | 302 x 302 | **31,479** | Seconds |

Each neuropeptidergic connection stores:

- Source neuron ID
- Target neuron ID
- Peptide ID (e.g., FLP-1, INS-3, NLP-12)
- Receptor ID (e.g., NPR-1, DAF-2, TYRA-2)
- Distance category (short/mid/long)
- Modulation type (excitatory/inhibitory/unknown)

**File format (CSV):**
```
source_neuron,target_neuron,peptide_gene,receptor_gene,distance_category,modulation_type,distance_um
AVAL,AVAR,flp-1,npr-1,short,excitatory,8.2
RIM,AVA,nlp-12,ckr-2,mid,excitatory,25.4
...
```

---

## Alternatives Considered

### 1. Full 3D Diffusion PDE

**Description:** Solve the diffusion equation `dC/dt = D nabla^2 C` in 3D space for each peptide species.

**Rejected because:**

- Computationally prohibitive (31 peptide species x 3D grid x seconds-long timescales)
- Requires meshing the extracellular space
- Diffusion coefficients for neuropeptides in worm tissue are not well-characterized
- The Ripoll-Sanchez data provide distance categories, not continuous concentration fields
- Distance-dependent attenuation (exp(-distance/lambda)) captures the key effect (nearby cells receive more signal) without full PDE solve

**When to reconsider:** If spatial peptide gradients prove critical (e.g., for chemotaxis-like behaviors driven by local peptide concentration, or for directed migration/localized modulation).

### 2. Binary On/Off Modulation

**Description:** Peptide present -> receptor fully active. Peptide absent -> receptor inactive. No dynamics.

**Rejected because:**

- Ignores temporal dynamics (seconds timescale is biologically important)
- Oversimplifies dose-response relationships
- Cannot capture graded modulation

### 3. Wait for Experimental Validation of All 31,479 Interactions

**Description:** Do not model any peptide-receptor interaction until experimentally validated in vivo.

**Rejected because:**

- The Ripoll-Sanchez map is based on spatial proximity + expression, not direct functional validation. But it is the best available whole-organism dataset.
- Most interactions will never be individually validated (infeasible to test 31K interactions)
- Modeling predictions can guide experimental prioritization

**Mitigation:** Flag interactions as "predicted" vs. "validated" in metadata. Prioritize validation of high-impact interactions (e.g., FLP peptides modulating locomotion).

### 4. Collapse All Peptides into Generic "Excitatory" and "Inhibitory" Classes

**Description:** Ignore peptide diversity. Model two generic peptide types.

**Rejected because:**

- Throws away biological specificity
- The Ripoll-Sanchez data provide peptide-receptor specificity; use it
- Peptide diversity is functionally important (different peptides have different spatiotemporal profiles)

### 5. Full Biochemical GPCR Cascade Model

**Description:** Explicitly model G-protein activation, PLC/adenylyl cyclase, IP3/cAMP production, PKA/PKC, and downstream channel phosphorylation.

**Rejected (for Phase 2) because:**

- Adds 10-20 state variables per receptor per cell (x36 receptors x 302 neurons = ~200,000 additional variables)
- Biochemical rate constants are largely unknown for *C. elegans* GPCRs
- Phenomenological modulation (direct conductance scaling) captures the functional effect without mechanistic detail
- Phase 5 (intracellular signaling cascades) is the appropriate place for detailed GPCR modeling

**When to reconsider:** Phase 5, when IP3/cAMP/MAPK cascades are added for intestinal and other non-neural cells.

### 6. Ignore Neuropeptides Entirely

**Description:** Stick with synaptic + gap junction connectome only.

**Rejected because:**

- 31,479 interactions is >5x the synaptic connectome (5,000 synapses)
- Only 5% overlap means peptides provide orthogonal information
- Known behavioral phenotypes (arousal, feeding, stress) depend on neuropeptides
- The data exist and are well-curated (Ripoll-Sanchez et al. 2023)

---

## Quality Criteria

### What Defines a Valid Neuropeptidergic Model?

1. **Data Provenance:** Every modeled interaction must trace to the Ripoll-Sanchez et al. 2023 dataset. Include source DOI in metadata.

2. **NeuroML 2 Extensions:** Neuropeptide signaling requires extending NeuroML to include:
   - `<peptideRelease>` component type
   - `<peptideReceptor>` component type
   - `<modulatorySynapse>` (GPCR-mediated modulation)

   These extensions must follow LEMS syntax and be backward-compatible (i.e., simulations without peptides still run).

3. **Timescale Separation:** Neuropeptide dynamics (seconds) must be numerically stable when coupled with fast synaptic dynamics (milliseconds). Use appropriate timestep or multi-rate integration.

4. **Distance Calculation:** Requires 3D cell positions. Source: WormAtlas 3D atlases, Long et al. 2009 nuclear positions, or Witvliet et al. 2021 EM reconstructions. Do not hardcode distances; compute from spatial data.

5. **Modulation Magnitude Constraints:** Conductance modulation factors must be biophysically plausible:
   - Minimum: 0.5x (50% reduction)
   - Maximum: 3.0x (300% increase)
   - Do not allow negative conductances or voltage flips (E_rev changes)

### What Defines a Valid Implementation?

6. **All 31,479 Interactions Included:** The Ripoll-Sanchez dataset is complete. Do not cherry-pick. If a peptide-receptor pair is in the dataset, it must be in the model (or explicitly flagged as excluded with justification).

7. **NeuroML Extensions Validated:** The new `peptideRelease` and `peptideReceptor` component types must:
   - Pass `jnml -validate`
   - Be documented in a LEMS schema file
   - Include example usage in a standalone test case

8. **Timescale Validation:** Neuropeptide effects should:
   - Onset: seconds (not milliseconds like synapses)
   - Duration: tens of seconds to minutes
   - Clearance: exponential decay with tau ~ 10-100 seconds

9. **Behavioral Phenotype Reproduction:** At least **3 known peptide knockout phenotypes** must be reproduced:
   - FLP peptides -> locomotion changes
   - NLP-12 -> reversal defects
   - PDF-1 -> arousal modulation

10. **Computational Performance:** Adding neuropeptides must not increase simulation time by >50% compared to synaptic-only model. Profile and optimize if needed.

### Validation Procedure

**Primary validation target:** Behavioral assays showing neuropeptide effects.

| Peptide | Knockout Phenotype | Modeling Prediction | Data Source |
|---------|-------------------|---------------------|-------------|
| **FLP peptides** | Altered locomotion speed and reversal frequency | Modulation of motor circuit excitability | Li et al. 1999, Rogers et al. 2003 |
| **NLP-12** (RIM neurons) | Reduced reversal initiation | Reduced excitability of backward command circuit | Ripoll-Sanchez supp data |
| **INS-1** (ASI neurons) | Dauer decision, lifespan | Modulation of DAF-2 pathway (out of scope for Phase 2) | Future |
| **PDF-1** (DVA neuron) | Arousal state | Modulation of global excitability | Choi et al. 2013 |

**Testing workflow:**

```bash
# Generate network with neuropeptides
python c302/CElegans.py C1DifferentiatedWithPeptides

# Run simulation
jnml LEMS_c302_C1_DifferentiatedWithPeptides.xml

# Extract behavioral metrics
python scripts/extract_behavior.py \
    --input LEMS_c302_C1_DifferentiatedWithPeptides.dat \
    --metrics speed,reversal_frequency,dwelling_time

# Compare to wild-type and peptide knockout data
python scripts/validate_peptide_effects.py \
    --simulated behavioral_metrics.csv \
    --experimental data/flp_knockout_phenotypes.csv
```

**Full validation procedure:**

```bash
# Generate network with peptides
cd c302/
python CElegans.py C1DifferentiatedWithPeptides

# Run baseline simulation (wild-type)
jnml LEMS_c302_C1_DifferentiatedWithPeptides.xml -nogui -reportFile baseline_report.txt

# Measure baseline behavior
python scripts/extract_behavior.py \
    LEMS_c302_C1_DifferentiatedWithPeptides.dat \
    --output baseline_behavior.csv

# Simulate FLP knockout (zero FLP release rate)
python c302/CElegans.py C1DifferentiatedWithPeptides --knockout flp-1,flp-2,flp-3
jnml LEMS_c302_C1_DifferentiatedWithPeptides_flp_knockout.xml -nogui

# Measure knockout behavior
python scripts/extract_behavior.py \
    LEMS_c302_C1_DifferentiatedWithPeptides_flp_knockout.dat \
    --output flp_knockout_behavior.csv

# Compare to experimental knockout data
python scripts/validate_knockout.py \
    --simulated flp_knockout_behavior.csv \
    --experimental data/flp_knockout_phenotypes.csv \
    --metrics speed,reversal_frequency \
    --tolerance 0.3  # 30% error allowed
```

**Success criteria:**

- At least 3 peptide knockouts reproduce known phenotypes within 30% error
- Wild-type simulation does not degrade (kinematic validation still passes)
- Peptide modulation onset time is >1 second (slower than synapses)

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Peptide synthesis and trafficking:** Neuropeptides are produced in the soma, packaged into dense-core vesicles, and trafficked to release sites. This trafficking is not modeled. Assume peptides are available for release when [Ca2+]i is high.

2. **Peptide degradation enzymes:** Extracellular peptidases (e.g., neprilysins) degrade peptides. Captured phenomenologically in tau_release, not mechanistically.

3. **Non-neuronal peptide signaling:** Intestinal cells, hypodermis, and other tissues release peptides (e.g., insulin-like peptides from intestine). Phase 5 work.

4. **GPCR signaling cascades:** The full Gq/Gs/Gi cascade (PLC, adenylyl cyclase, IP3, cAMP, PKA, PKC) is not modeled. Captured as direct conductance modulation.

5. **Behavioral state models:** Arousal, stress, satiety are emergent network properties. No explicit "state variable" for arousal. These emerge from peptide modulation of circuit excitability.

6. **Monoaminergic signaling:** Serotonin, dopamine, octopamine, tyramine are small-molecule transmitters, not peptides. Already partially in ConnectomeToolbox (Bentley et al. 2016). Separate from peptide signaling.

7. **Endocrine signaling:** Insulin, TGF-beta, steroids released from non-neural tissues (intestine, hypodermis) into the pseudocoelom. Phase 5 (inter-tissue signaling).

8. **Synaptic co-transmission:** Some neurons co-release peptides and classical transmitters (e.g., GLU + NLP). Modeling the interaction is Phase 5 work.

9. **Receptor desensitization:** GPCRs undergo desensitization (beta-arrestin binding, receptor internalization) on prolonged activation. Not modeled in Phase 2. If needed, add desensitization term to receptor dynamics.

10. **Peptide isoform diversity:** Some peptide genes encode multiple bioactive peptides (e.g., FLP-1 encodes 8 peptides). Current model treats each gene as a single peptide. Isoform-specific modeling is future work if functional differences are demonstrated.

---

## Context & Background

The classical *C. elegans* connectome (White et al. 1986, Cook et al. 2019) describes **synaptic** (chemical) and **gap junction** (electrical) connections. But neurons also communicate via **neuropeptides** — small signaling molecules released into the extracellular space that diffuse to receptors on distant cells. This "wireless" signaling layer was recently mapped at whole-organism scale:

**Ripoll-Sanchez et al. (2023), *Neuron*:** "The neuropeptidergic connectome of *C. elegans*"

- **31,479 peptide-receptor interactions** across all 302 neurons
- Each neuron class expresses ~23 neuropeptide genes and ~36 neuropeptide receptors
- **Only 5% overlap** with the synaptic connectome
- Three distance categories: short-range (<10 um), mid-range (10-50 um), long-range (>50 um)

This extrasynaptic layer likely governs slow behavioral states (arousal, stress, feeding motivation, dwelling/roaming transitions) that the fast synaptic connectome alone cannot explain.

---

## Implementation References

### Neuropeptidergic Connectome Data Source

**Primary:**
```
Ripoll-Sanchez et al. (2023) Supplementary Data Table S1
```
Download from *Neuron* journal website or request from authors.

**Integrated into ConnectomeToolbox:**
```
openworm.org/ConnectomeToolbox
```
Add as new connection type alongside chemical synapses and gap junctions.

### NeuroML Extension Proposal

Create new LEMS component types:

**PeptideReleaseDynamics.xml:**
```xml
<ComponentType name="peptideRelease">
    <Parameter name="k_release" dimension="per_time"/>
    <Parameter name="ca_threshold" dimension="concentration"/>
    <Parameter name="tau_release" dimension="time"/>
    <Exposure name="peptide_concentration" dimension="concentration"/>
    <Dynamics>
        <StateVariable name="P" dimension="concentration"/>
        <DerivedVariable name="release_trigger"
            value="(ca_internal - ca_threshold) / ca_threshold"/>
        <ConditionalDerivedVariable name="release_rate">
            <Case condition="release_trigger .gt. 0"
                  value="k_release * release_trigger"/>
            <Case value="0"/>
        </ConditionalDerivedVariable>
        <TimeDerivative variable="P"
            value="release_rate - P / tau_release"/>
    </Dynamics>
</ComponentType>
```

**PeptideReceptorDynamics.xml:**
```xml
<ComponentType name="peptideReceptor">
    <Parameter name="k_on" dimension="per_concentration_per_time"/>
    <Parameter name="k_off" dimension="per_time"/>
    <Parameter name="modulation_factor" dimension="none"/>
    <Parameter name="target_channel" dimension="none"/>
    <Requirement name="peptide_concentration" dimension="concentration"/>
    <Exposure name="conductance_modulation" dimension="none"/>
    <Dynamics>
        <StateVariable name="R_active" dimension="none"/>
        <TimeDerivative variable="R_active"
            value="k_on * peptide_concentration * (1 - R_active) - k_off * R_active"/>
        <DerivedVariable name="conductance_modulation"
            value="1 + modulation_factor * R_active"/>
    </Dynamics>
</ComponentType>
```

### Integration into c302 Cell Models

Each neuron cell template extends to include:

```xml
<cell id="AVALCell">
    <!-- Existing membrane dynamics, channels, synapses -->

    <!-- Peptide release -->
    <peptideRelease id="flp1_release"
        k_release="0.001 per_ms"
        ca_threshold="2e-7 mol_per_cm3"
        tau_release="30000 ms"/>  <!-- 30 seconds -->

    <!-- Peptide receptors -->
    <peptideReceptor id="npr1_receptor"
        k_on="1e6 per_M_per_s"
        k_off="0.1 per_s"
        modulation_factor="0.5"      <!-- 50% increase in target conductance -->
        target_channel="k_slow_chan"  <!-- NPR-1 increases K+ conductance -->
        peptide_concentration="$flp1_from_RIM"/>  <!-- Pointer to RIM's FLP-1 release -->
</cell>
```

### Connectome Data Structure

Extend the c302 network generation to read peptide-receptor adjacency matrix:

```python
# c302/neuroml/CeNGENConnectome.py

def add_neuropeptide_connections(network, peptide_data):
    for _, row in peptide_data.iterrows():
        source = row['source_neuron']
        target = row['target_neuron']
        peptide = row['peptide_gene']
        receptor = row['receptor_gene']
        distance = row['distance_um']
        mod_type = row['modulation_type']  # excitatory/inhibitory

        # Create peptide release in source neuron
        network.add_component(
            source,
            "peptideRelease",
            id=f"{peptide}_release",
            tau_release=infer_tau_from_distance(distance)
        )

        # Create receptor in target neuron
        mod_factor = 0.5 if mod_type == "excitatory" else -0.3
        network.add_component(
            target,
            "peptideReceptor",
            id=f"{receptor}_receptor",
            modulation_factor=mod_factor,
            target_channel=infer_target_channel(receptor)
        )

        # Link source release to target receptor
        network.link_peptide(source, peptide, target, receptor, distance)
```

### Ripoll-Sanchez Dataset

**Publication:**
```
Ripoll-Sanchez L, Watteyne J, Sun H, et al. (2023).
"The neuropeptidergic connectome of C. elegans."
Neuron 111:3570-3589.
DOI: 10.1016/j.neuron.2023.07.002
```

**Supplementary data:**

- Table S1: All 31,479 peptide-receptor interactions
- Table S2: Neuron-by-neuron peptide expression
- Table S3: Receptor expression
- Table S4: Distance categories

**Integration:**
Download Table S1, convert to CSV, add to:
```
openworm.org/ConnectomeToolbox/data/neuropeptidergic_connectome.csv
```

### WormBase Neuropeptide Annotations

```
https://wormbase.org/
```

Gene classes:

- FLP peptides: flp-1 through flp-34
- NLP peptides: nlp-1 through nlp-50
- INS insulin-like: ins-1 through ins-39
- Receptors: npr-1 through npr-38, dmsr-1, tyra-2, etc.

### Existing Partial Implementation

The **Bentley et al. 2016 monoaminergic/peptidergic connectome** is already in ConnectomeToolbox:
```
https://github.com/openworm/ConnectomeToolbox
```

The Ripoll-Sanchez 2023 dataset is a comprehensive update. Bentley data can serve as a validation subset (check that Ripoll-Sanchez reproduces Bentley's interactions).

---

## Migration Path

### Incremental Integration Strategy

Do not add all 31,479 interactions at once. Rollout:

**Stage 1 (Proof of Concept):**

- FLP peptides only (~5,000 interactions)
- Validate against FLP knockout behavioral phenotypes
- Confirm NeuroML extensions work

**Stage 2 (Core Neuropeptides):**

- Add NLP, INS, PDF peptides (~15,000 interactions)
- Validate against published knockout/overexpression studies

**Stage 3 (Complete Dataset):**

- Add remaining peptides (full 31,479 interactions)
- Full validation suite

### Backward Compatibility

Models without peptides remain valid. The NeuroML extension is **additive**:

```xml
<!-- Old model (still works) -->
<cell id="AVALCell">
    <membraneProperties>...</membraneProperties>
</cell>

<!-- New model (backward compatible) -->
<cell id="AVALCell">
    <membraneProperties>...</membraneProperties>
    <peptideRelease id="flp1_release">...</peptideRelease>  <!-- Added -->
</cell>
```

Simulations without `<peptideRelease>` components run as before.

---

## Known Issues and Future Work

### Issue 1: Modulation Type (Excitatory vs. Inhibitory) Often Unknown

The Ripoll-Sanchez dataset includes spatial proximity and expression but not always functional validation. For many peptide-receptor pairs, whether the effect is excitatory or inhibitory is unknown.

**Mitigation:**

- Use WormBase phenotype data (e.g., "increased activity" suggests excitatory)
- Use mammalian ortholog data (e.g., NPY receptors are typically inhibitory)
- Flag as "inferred" in metadata

**Validation:** Test both excitatory and inhibitory hypotheses, compare to experimental knockout behavior.

### Issue 2: Spatial Positions May Vary Across Individuals

3D cell positions are from EM reconstructions of specific animals. Different animals have slight positional variation. Distance calculations are approximate.

**Mitigation:** Use population-averaged positions from multiple EM datasets (Witvliet et al. 2021 has 8 animals). Report mean +/- SD for distances.

### Issue 3: Developmental Changes in Peptide Expression

The neuropeptidergic connectome likely changes across L1, L4, adult, dauer stages. Ripoll-Sanchez data are primarily adult.

**Future work:** Integrate with CeNGEN L1 and Packer et al. embryonic data to model stage-specific peptide signaling.

---

## References

1. **Ripoll-Sanchez L, Watteyne J, Sun H, et al. (2023).** "The neuropeptidergic connectome of *C. elegans*." *Neuron* 111:3570-3589.
   *31,479 interactions dataset.*

2. **Bentley B, Branicky R, Barnes CL, et al. (2016).** "The multilayer connectome of *Caenorhabditis elegans*." *PLoS Comput Biol* 12:e1005283.
   *Earlier monoaminergic/peptidergic map.*

3. **Li C, Kim K, Nelson LS (1999).** "FMRFamide-related neuropeptide gene family in *Caenorhabditis elegans*." *Brain Res* 848:26-34.
   *FLP peptide family.*

4. **Choi S, Taylor KP, Chatzigeorgiou M, et al. (2013).** "Analysis of NPR-1 reveals a circuit mechanism for behavioral quiescence in *C. elegans*." *Neuron* 78:869-880.
   *NPR-1 receptor function.*

5. **Taylor SR et al. (2021).** "Molecular topography of an entire nervous system." *Cell* 184:4329-4347.
   *CeNGEN provides receptor expression data.*

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Neuron [Ca2+]i (triggers peptide release) | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | `ca_internal` per neuron | NeuroML state variable | mol/cm3 |
| 3D cell positions (distance calculation) | [DD008](DD008_Data_Integration_Pipeline.md) / WormAtlas | Per-neuron (x, y, z) | OWMeta query or CSV | um |
| Ripoll-Sanchez peptide-receptor dataset | External / OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) | 31,479 interaction table | CSV: source, target, peptide, receptor, distance, modulation_type | mixed |
| Ion channel conductance baselines | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | `g_baseline` per channel per neuron | NeuroML `<channelDensity>` | S/cm2 |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Conductance modulation factors | [DD001](DD001_Neural_Circuit_Architecture.md) (modifies channel conductances in real-time) | `g_effective = g_baseline * conductance_modulation` | NeuroML `<peptideReceptor>` exposure | dimensionless multiplier [0.5, 3.0] |
| Peptide concentration fields | Internal (receptor activation) | Per-source peptide concentration | NeuroML state variable | mol/cm3 |
| Neuropeptide concentration fields (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-peptide volumetric concentration over time | OME-Zarr: `neuropeptides/concentrations/`, shape (n_timesteps, n_peptides, n_spatial_bins) | mol/cm3 |
| Peptide release events (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-neuron peptide release timestamps | OME-Zarr: `neuropeptides/release_events/` | ms |

### Repository & Packaging

- **Primary repository:** `openworm/c302` (NeuroML extensions for peptides)
- **Docker stage:** `neural` (same as [DD001](DD001_Neural_Circuit_Architecture.md))
- **`versions.lock` key:** `c302`
- **Build dependencies:** pyNeuroML (pip), pandas (pip), numpy (pip)
- **Additional data in image:** Ripoll-Sanchez Table S1 (~5MB CSV), 3D neuron positions (~100KB)
- **`versions.lock` note:** Pin Ripoll-Sanchez data version

### Configuration

```yaml
neural:
  neuropeptides: true                # false = synaptic-only (backward compatible)
  peptide_dataset: "RipollSanchez2023"
  peptide_dt: 1.0                   # ms (slow dynamics timestep)
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `neural.neuropeptides` | `false` | `true`/`false` | Enable neuropeptide modulatory layer |
| `neural.peptide_dataset` | `"RipollSanchez2023"` | String | Peptide-receptor dataset version pin |
| `neural.peptide_dt` | `1.0` | `0.1`-`10.0` ms | Slow dynamics timestep for multi-rate integration |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)

# Step 1: Verify backward compatibility
docker compose run quick-test  # with neuropeptides: false
# Must produce identical output to pre-peptide baseline

# Step 2: Verify peptide-enabled simulation
# (set neural.neuropeptides: true in openworm.yml)
docker compose run quick-test
# Verify: simulation completes within 2.5x baseline time
# Verify: no NaN values in peptide concentration variables
# Verify: conductance modulation factors in [0.5, 3.0] range

# Full validation (must pass before merge to main)
docker compose run validate
# Tier 3 kinematic metrics within +/-15% (peptides should modulate, not destroy, locomotion)
```

**Per-PR checklist:**

- [ ] `jnml -validate` passes for peptideRelease and peptideReceptor LEMS types
- [ ] `quick-test` passes with `neuropeptides: false` (backward compatibility)
- [ ] `quick-test` passes with `neuropeptides: true` (peptide-enabled)
- [ ] No NaN values in peptide concentration variables
- [ ] Conductance modulation factors in [0.5, 3.0] range
- [ ] `validate` passes (Tier 3 kinematic metrics within +/-15%)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `neuropeptides/concentrations/` (n_timesteps, n_peptides, n_spatial_bins) | Volumetric peptide concentration | Cool-to-warm colormap (blue=low, red=high concentration) |
| `neuropeptides/release_events/` | Release event markers | Discrete pulse markers per neuron |

### Computational Budget

| Resource | Without Neuropeptides | With Neuropeptides | Impact |
|----------|----------------------|-------------------|--------|
| State variables | ~1,800 (302 neurons x ~6 vars) | ~65,000 (+31,479 peptide release + receptor states) | ~36x more state variables |
| Memory | ~500 MB | ~2 GB | Docker memory limit must increase |
| Simulation time (15ms) | ~10 min | ~15-25 min | 50-150% increase |

**Docker memory limit:** When `neural.neuropeptides: true`, the `docker-compose.yml` simulation service must set `deploy.resources.limits.memory: 16G` (up from 8G).

### Multi-Rate Integration Requirement

Neuropeptides operate on seconds timescale, synapses on milliseconds. The `master_openworm.py` orchestrator ([DD013](DD013_Simulation_Stack_Architecture.md)) must support multi-rate stepping:

```python
# Pseudocode for multi-rate coupling in master_openworm.py
dt_fast = 0.05    # ms (synaptic, gap junction dynamics)
dt_slow = 1.0     # ms (peptide release, receptor activation)

for t in range(0, duration, dt_fast):
    step_fast_dynamics(dt_fast)       # Synapses, gap junctions, membrane voltage
    if t % dt_slow == 0:
        step_slow_dynamics(dt_slow)   # Peptide release, diffusion, receptor binding
```

**This is a change to the orchestrator ([DD013](DD013_Simulation_Stack_Architecture.md)), not just to c302.** The Integration Maintainer must implement multi-rate stepping support.

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Neuron calcium dynamics | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Peptide release is triggered by [Ca2+]i — if calcium dynamics change, release timing shifts |
| 3D positions | [DD008](DD008_Data_Integration_Pipeline.md) | Distance-dependent attenuation uses cell positions — if atlas data updates, all distances recalculate |
| Channel conductance baselines | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Modulation is multiplicative on baseline g — if baselines change, effective g changes |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Neural circuit dynamics | [DD001](DD001_Neural_Circuit_Architecture.md) | Conductance modulation changes every neuron's excitability |
| Muscle activation | [DD002](DD002_Muscle_Model_Architecture.md) | Changed neuron excitability -> changed motor output |
| Locomotion | [DD003](DD003_Body_Physics_Architecture.md) | Changed motor output -> changed movement |
| Behavioral validation | [DD010](DD010_Validation_Framework.md) | Peptide modulation shifts behavioral metrics |
| Orchestrator | [DD013](DD013_Simulation_Stack_Architecture.md) | Multi-rate stepping requirement — if peptide dt changes, orchestrator must adapt |

---

**Approved by:** Pending (Phase 2 proposal)
**Implementation Status:** Proposed
**Next Actions:**

1. Download Ripoll-Sanchez Table S1
2. Design NeuroML peptide extension schema
3. Implement proof-of-concept with FLP peptides only
4. Validate against FLP knockout behavioral data
5. Extend to full dataset if validation succeeds
