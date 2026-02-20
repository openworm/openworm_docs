# DD020: Connectome Data Access and Dataset Policy

**Status:** Proposed  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-16  
**Supersedes:** None  
**Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Differentiation), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptidergic Connectome), [DD007](DD007_Pharyngeal_System_Architecture.md) (Pharyngeal System), [DD008](DD008_Data_Integration_Pipeline.md) (Data Integration Pipeline), [DD013](DD013_Simulation_Stack_Architecture.md) (Simulation Stack), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Hybrid Mechanistic-ML), [DD019](DD019_Closed_Loop_Touch_Response.md) (Closed-Loop Touch Response)

---

## TL;DR

The ConnectomeToolbox (`cect`, PyPI v0.2.7) is OpenWorm's canonical package for accessing *C. elegans* connectome data. It provides 30+ dataset readers spanning 1976-2024 (White, Varshney, Cook, Witvliet developmental series, Randi functional, Ripoll-Sanchez neuropeptidergic, Wang 2024 neurotransmitter atlas), cell classification, neurotransmitter identity, and bilateral symmetry analysis. This DD specifies: (1) the default dataset for each modeling use case, (2) version pinning policy, (3) canonical API patterns all consuming DDs must follow, and (4) multi-dataset validation strategy. **Never parse raw CSV/Excel connectome files directly — always use `cect`.**

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **Layer** | Core Architecture — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **What does this produce?** | Standardized connectome data access via `cect` Python API: adjacency matrices, `ConnectionInfo` objects, cell classification, neurotransmitter identities, bilateral symmetry metrics |
| **Success metric** | All consuming DDs ([DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md), [DD019](DD019_Closed_Loop_Touch_Response.md)) obtain connectome data exclusively through `cect`; dataset selection is explicit and reproducible |
| **Repository** | [`openworm/ConnectomeToolbox`](https://github.com/openworm/ConnectomeToolbox) — issues labeled `dd020` |
| **Config toggle** | `data.connectome.dataset: "Cook2019Herm"` / `data.connectome.cect_version: "0.2.7"` in `openworm.yml` |
| **Build & test** | `pip install cect==0.2.7` then `python -c "from cect.Cook2019HermReader import get_instance; cds = get_instance(); cds.summary()"` |
| **Visualize** | `cect` built-in: `cds.to_plotly_matrix_fig(synclass, view)`, `cds.to_plotly_graph_fig(synclass, view)`, `cds.to_plotly_hive_plot_fig(synclass, view)` |
| **CI gate** | `cect` import + default dataset query returns expected neuron count; version matches `versions.lock` |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Unified data access | All 9 consuming DDs obtain connectome data via `cect` API, not raw file parsing | Tier 1 (blocking) |
| **Secondary:** Reproducibility | Dataset selection and `cect` version pinned in `openworm.yml` + `versions.lock`; any two runs with same config produce identical adjacency matrices | Tier 1 (blocking) |
| **Tertiary:** Multi-dataset validation | Simulation results compared against ≥2 independent connectome datasets (e.g., Cook2019Herm primary, Witvliet8 cross-validation) | Tier 2 (non-blocking initially, blocking Phase 3+) |

**Before:** Each consuming DD independently decides which connectome dataset to use, how to parse it, and how to handle cell name variants. [DD001](DD001_Neural_Circuit_Architecture.md) uses `UpdatedSpreadsheetDataReader2`, [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) uses Ripoll-Sanchez data, [DD007](DD007_Pharyngeal_System_Architecture.md) may use Cook2019 pharyngeal subset — no coordination, no version pinning, no comparison.

**After:** A single DD (this one) specifies dataset selection, version pinning, API contract, and validation strategy. Consuming DDs reference [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) for connectome access. Changes to default dataset or `cect` version are reviewed centrally.

---

## Deliverables

| Artifact | Path / Location | Format | Example |
|----------|----------------|--------|---------|
| `cect` package (external) | PyPI: `pip install cect` / GitHub: `openworm/ConnectomeToolbox` | Python package | `from cect.Cook2019HermReader import get_instance` |
| Dataset selection policy | This DD (Section: Dataset Selection Policy) | Markdown specification | "Default adult hermaphrodite: Cook2019Herm" |
| `openworm.yml` connectome config | `data.connectome.*` keys | YAML | `dataset: "Cook2019Herm"`, `cect_version: "0.2.7"` |
| `versions.lock` entry | `cect` key in `versions.lock` ([DD013](DD013_Simulation_Stack_Architecture.md)) | Lock file | `cect: "0.2.7"` |
| Connectome adjacency matrices | In-memory via `cect` API | `numpy.ndarray` per synclass | `cds.connections["Generic_CS"]` shape (N, N) |
| Cell classification metadata | `cect.Cells` module | Python API | `get_SIM_class("AVAL")` → `"Interneuron"` |
| Bilateral symmetry metrics | `cect.Analysis.convert_to_symmetry_array()` | `(ndarray, float, str)` | `(array, 56.25, "Of 441 possible edges...")` |
| Neurotransmitter identity | `cect.Neurotransmitters` module | Python constants | `ACETYLCHOLINE`, `GABA`, `GLUTAMATE`, `SEROTONIN` |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/ConnectomeToolbox`](https://github.com/openworm/ConnectomeToolbox) |
| **Issue label** | `dd020` |
| **Milestone** | Connectome Data Access Policy |
| **Branch convention** | `dd020/description` (e.g., `dd020/pin-cook2019-default`) |
| **Example PR title** | `DD020: Pin cect 0.2.7 in versions.lock, update openworm.yml` |
| **De facto maintainer** | Padraig Gleeson (p.gleeson@ucl.ac.uk) |
| **PyPI** | https://pypi.org/project/cect/ |

---

## How to Build & Test

### Prerequisites

- Python 3.8+ (tested on 3.8-3.12)
- pip

### Step-by-step

```bash
# Step 1: Install cect at pinned version
pip install cect==0.2.7

# Step 2: Verify default dataset loads
python -c "
from cect.Cook2019HermReader import get_instance
cds = get_instance()
cds.summary()
# Expected: ~302 neurons, chemical + electrical connections
"

# Step 3: Verify ConnectionInfo API
python -c "
from cect.Cook2019HermReader import get_instance
cds = get_instance()
for ci in cds.original_connection_infos[:5]:
    print(f'{ci.pre_cell} -> {ci.post_cell}: {ci.number} ({ci.syntype}, {ci.synclass})')
"

# Step 4: Verify cell classification
python -c "
from cect.Cells import get_SIM_class, SENSORY_NEURONS_COOK, INTERNEURONS_COOK, MOTORNEURONS_COOK
print(f'Sensory: {len(SENSORY_NEURONS_COOK)}')
print(f'Interneurons: {len(INTERNEURONS_COOK)}')
print(f'Motor: {len(MOTORNEURONS_COOK)}')
print(f'AVAL class: {get_SIM_class(\"AVAL\")}')
print(f'DA01 class: {get_SIM_class(\"DA01\")}')
"

# Step 5: Verify bilateral symmetry analysis
python -c "
from cect.Cook2019HermReader import get_instance
from cect.Analysis import convert_to_symmetry_array
cds = get_instance()
arr, pct, info = convert_to_symmetry_array(cds, ['Generic_CS'])
print(f'Symmetry: {pct:.1f}%')
print(info)
"

# Step 6: Docker-based verification ([DD013](DD013_Simulation_Stack_Architecture.md) stack)
docker compose run shell python -c "import cect; print(cect.__version__)"
```

---

## How to Visualize

**`cect` built-in visualization:** The package generates publication-quality Plotly figures directly.

| Viewer Feature | Specification |
|---------------|---------------|
| **Matrix view** | `cds.to_plotly_matrix_fig(synclass="Generic_CS", view="Neurons")` — heatmap of connectivity matrix |
| **Graph view** | `cds.to_plotly_graph_fig(synclass="Generic_CS", view="Neurons")` — network graph |
| **Hive plot** | `cds.to_plotly_hive_plot_fig(synclass="Generic_CS", view="Neurons")` — hive plot visualization |
| **Symmetry view** | `cds.to_plotly_matrix_fig(synclass="Generic_CS", view="Neurons", symmetry=True)` — bilateral symmetry overlay (red=asymmetric, blue=symmetric) |
| **Filtering** | Views: `"Neurons"`, `"Full"`, `"Pharynx"`, `"MotorMuscle"`, custom via `get_connectome_view()` |

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer connection:** Connectome topology exported as part of `neural/` OME-Zarr group. The [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer reads connectivity from the simulation output, not directly from `cect` — but `cect` is the upstream source of truth.

---

## Dataset Selection Policy

### Default Datasets by Use Case

| Use Case | Default Dataset | `cect` Reader | Rationale |
|----------|----------------|---------------|-----------|
| **Adult hermaphrodite somatic connectome** | Cook et al. 2019 (hermaphrodite) | `Cook2019HermReader` | Gold standard whole-animal EM reconstruction; corrects White 1986 errors; includes both chemical and electrical synapses |
| **Adult male connectome** | Cook et al. 2019 (male) | `Cook2019MaleReader` | Only complete male connectome; 385 neurons including male-specific |
| **Pharyngeal nervous system** | Cook et al. 2019 (pharyngeal subset) | `Cook2019HermReader` with pharynx view filter | Same dataset, filtered via `cds.get_connectome_view("Pharynx")` |
| **Developmental series** | Witvliet et al. 2021 (stages 1-8) | `WitvlietDataReader1` through `WitvlietDataReader8` | Only developmental connectome series; L1 through adult |
| **Functional connectivity validation** | Randi et al. 2023 | `WormNeuroAtlasFuncReader` | Whole-brain calcium imaging functional connectivity; primary validation target for [DD005](DD005_Cell_Type_Differentiation_Strategy.md) |
| **Neuropeptidergic network** | Ripoll-Sanchez et al. 2023 | `RipollSanchezShortRangeReader`, `RipollSanchezMidRangeReader`, `RipollSanchezLongRangeReader` | Extrasynaptic neuropeptide signaling; [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) primary data source |
| **Neurotransmitter identity** | Wang et al. 2024 | `Wang2024HermReader`, `Wang2024MaleReader` | CRISPR/Cas9 fluorescent reporter atlas; 16 neurotransmitter systems; reveals co-transmission |
| **OpenWorm unified (experimental)** | Wang 2024 hermaphrodite base | `OpenWormUnifiedReader` | WIP — subject to change; currently wraps Wang2024Reader with electrical connections. Use for forward-looking development, not production simulations |
| **Legacy / backward compatibility** | Varshney et al. 2011 | `VarshneyDataReader` | Historical dataset; use only for comparing to pre-2019 publications |
| **Cross-validation** | Witvliet stage 8 (adult) | `WitvlietDataReader8` | Independent adult reconstruction for comparing against Cook2019Herm |

### Dataset Selection Rules

1. **Default to Cook2019Herm** unless your DD explicitly requires a different dataset. Cook2019 corrects the ~150 errors found in White 1986 and includes both sexes.

2. **Never parse raw files.** All connectome data access MUST go through `cect` readers. The readers handle:
   - Cell name normalization (e.g., `DB1/3` → `DB1`, `DB3`)
   - Synapse type classification
   - Consistent `ConnectionInfo` format
   - Caching for fast repeated access

3. **Specify the dataset explicitly.** Do not rely on `cect` defaults. Every consuming DD must name the dataset in its configuration or code:
   ```python
   # GOOD: Explicit dataset
   from cect.Cook2019HermReader import get_instance
   cds = get_instance()

   # BAD: Implicit/unnamed dataset
   from cect import load_some_connectome  # What dataset is this?
   ```

4. **Use `from_cache=True` in CI and Docker.** Reader instances can load from pre-cached JSON files for reproducibility and speed:
   ```python
   cds = get_instance(from_cache=True)  # Fast, deterministic
   ```

5. **Record the `cect` version** in `versions.lock` ([DD013](DD013_Simulation_Stack_Architecture.md)). Dataset reader behavior may change across versions.

### Policy for Adopting New Datasets

When a new connectome dataset is published (e.g., a future revision or new species):

1. **Padraig adds a reader** to ConnectomeToolbox (he typically does this within days of publication)
2. **Bump `cect` version** in `versions.lock` after reviewing the changelog
3. **Run regression tests** — ensure existing simulations produce equivalent results with the new version
4. **Do NOT change the default dataset** without an RFC ([DD012](DD012_Design_Document_RFC_Process.md) process). Changing from Cook2019Herm to a new default affects all consuming DDs
5. **New datasets can be used for cross-validation** without changing defaults — add them as comparison targets in [DD010](DD010_Validation_Framework.md)

---

## API Contract for Consumers

### Core Data Types

```python
# ConnectionInfo — single synaptic connection
from cect.ConnectomeReader import ConnectionInfo

ci = ConnectionInfo(
    pre_cell="AVAL",       # Presynaptic cell name (str)
    post_cell="DA01",      # Postsynaptic cell name (str)
    number=3.0,            # Connection weight/count (float)
    syntype="Chemical",    # "Chemical" or "Electrical" (str)
    synclass="Acetylcholine"  # Neurotransmitter class (str)
)
```

```python
# ConnectomeDataset — full connectome
from cect.ConnectomeDataset import ConnectomeDataset

cds: ConnectomeDataset
cds.nodes                    # list[str] — all cell names
cds.connections              # dict[str, np.ndarray] — synclass → adjacency matrix
cds.original_connection_infos  # list[ConnectionInfo] — raw connection list
```

### Canonical Query Patterns

**Pattern 1: Load the default adult hermaphrodite connectome**
```python
from cect.Cook2019HermReader import get_instance

cds = get_instance(from_cache=True)
print(f"Nodes: {len(cds.nodes)}")
print(f"Connections: {len(cds.original_connection_infos)}")
```

**Pattern 2: Get neuron-to-neuron connections only**
```python
nn_conns = cds.get_neuron_to_neuron_conns()
for ci in nn_conns:
    print(f"{ci.pre_cell} -> {ci.post_cell}: {ci.number} ({ci.synclass})")
```

**Pattern 3: Get neuron-to-muscle connections (for [DD002](DD002_Muscle_Model_Architecture.md))**
```python
nm_conns = cds.get_neuron_to_muscle_conns()
```

**Pattern 4: Filter to pharyngeal view (for [DD007](DD007_Pharyngeal_System_Architecture.md))**
```python
pharynx_cds = cds.get_connectome_view("Pharynx")
pharynx_cds.summary()
```

**Pattern 5: Convert to NetworkX graph (for graph analysis)**
```python
G = cds.to_networkx_graph(synclass="Generic_CS", view="Neurons")
print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
```

**Pattern 6: Cell classification lookup**
```python
from cect.Cells import (
    get_SIM_class,         # "Sensory" / "Interneuron" / "Motorneuron" / "Other"
    is_any_neuron,         # bool
    is_known_muscle,       # bool
    is_pharyngeal_cell,    # bool
    get_cell_notes,        # descriptive string
    get_standard_color,    # hex color for visualization
    SENSORY_NEURONS_COOK,  # list of sensory neuron names
    INTERNEURONS_COOK,     # list of interneuron names
    MOTORNEURONS_COOK,     # list of motor neuron names
    BODY_WALL_MUSCLE_NAMES,
    PHARYNGEAL_MUSCLE_NAMES,
)
```

**Pattern 7: Bilateral symmetry analysis**
```python
from cect.Cells import (
    is_bilateral_left,
    is_bilateral_right,
    are_bilateral_pair,
    get_contralateral_cell,
)
from cect.Analysis import convert_to_symmetry_array

# Check if cells are bilateral pair
assert are_bilateral_pair("AVAL", "AVAR")
assert get_contralateral_cell("AVAL") == "AVAR"

# Compute symmetry metric for a connectome
arr, symmetry_pct, info = convert_to_symmetry_array(cds, ["Generic_CS"])
print(f"Bilateral symmetry: {symmetry_pct:.1f}%")
```

**Pattern 8: Neurotransmitter-specific queries (for [DD006](DD006_Neuropeptidergic_Connectome_Integration.md))**
```python
from cect.Neurotransmitters import (
    ACETYLCHOLINE, GABA, GLUTAMATE, SEROTONIN, DOPAMINE,
    GENERIC_CHEM_SYN, GENERIC_ELEC_SYN,
    PEPTIDERGIC_SYN_CLASS,
)

# Get acetylcholine-specific connectivity matrix
ach_matrix = cds.connections.get(ACETYLCHOLINE)

# Get neuropeptidergic connections (Ripoll-Sanchez data)
from cect.RipollSanchezShortRangeReader import get_instance as get_rs_short
rs_cds = get_rs_short(from_cache=True)
```

**Pattern 9: Wang 2024 neurotransmitter atlas**
```python
from cect.Wang2024HermReader import get_instance as get_wang2024

wang_cds = get_wang2024(from_cache=True)
# Access 16 neurotransmitter systems with co-transmission data
wang_cds.summary()
```

### Cell ID Normalization

`cect` handles cell name variants internally. Consumers should use the names as returned by `cect` and never apply their own normalization. Key conventions:

| Convention | Example | Notes |
|------------|---------|-------|
| Neuron names | `AVAL`, `AVAR`, `DA01` | Uppercase, left/right suffix L/R |
| Body wall muscles | `MDL01`, `MVR24` | Dorsal/ventral, left/right, numbered |
| Pharyngeal muscles | `pm1DL`, `pm3VR` | Lowercase prefix |
| Pharyngeal neurons | `I1L`, `M3L`, `NSML` | Mixed conventions |

**Rule:** Do not build cell name parsers. Use `cect.Cells` functions:
```python
from cect.Cells import is_known_cell, is_any_neuron, is_known_muscle
assert is_known_cell("AVAL")
assert is_any_neuron("AVAL")
assert is_known_muscle("MDL01")
```

---

## Version Pinning & Update Procedure

### Pinning

```yaml
# versions.lock ([DD013](DD013_Simulation_Stack_Architecture.md))
cect: "0.2.7"  # ConnectomeToolbox — pinned per [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)
```

```yaml
# openworm.yml
data:
  connectome:
    dataset: "Cook2019Herm"          # Default dataset for this simulation run
    cect_version: "0.2.7"           # Must match versions.lock
    pharyngeal_dataset: "Cook2019Herm"  # Pharynx subset (view filter)
    developmental_dataset: null      # Set to "Witvliet1" through "Witvliet8" for developmental
    functional_dataset: "Randi2023"  # Functional connectivity validation target
    neuropeptide_dataset: "RipollSanchezShortRange"  # [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) neuropeptide data
    use_cache: true                  # Load from cached JSON (recommended for CI)
```

### Update Procedure

When a new `cect` version is released:

1. **Review the changelog** on GitHub/PyPI for breaking changes
2. **Install new version locally:** `pip install cect==X.Y.Z`
3. **Run dataset load test:** Verify default dataset returns same neuron count and connection count as previous version
4. **Run full simulation regression:** `docker compose run validate` with new `cect` version
5. **If regression passes:** Update `versions.lock` and `openworm.yml`, open PR referencing [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)
6. **If regression fails:** Investigate which dataset reader changed, report issue on `openworm/ConnectomeToolbox`

**Breaking change policy:** If a `cect` update changes the default dataset's adjacency matrix (e.g., corrected connection counts), this is a **simulation-affecting change** requiring:

- Re-running all [DD010](DD010_Validation_Framework.md) validation tiers
- Documenting the delta (which connections changed, why)
- Approval from the Integration Maintainer ([DD013](DD013_Simulation_Stack_Architecture.md))

---

## Multi-Dataset Validation

### Strategy

Biological connectome data are noisy — different labs, different animals, different EM reconstruction methods yield different connection counts. A robust simulation should produce qualitatively similar behavior across multiple connectome datasets.

### Validation Protocol

| Validation Level | Datasets | What to Compare | Acceptance Criterion |
|-----------------|----------|-----------------|---------------------|
| **Primary** | Cook2019Herm (default) | Full simulation kinematic metrics | [DD010](DD010_Validation_Framework.md) Tier 3: ±15% of Schafer lab data |
| **Cross-validation** | Witvliet8 (independent adult) | Same simulation, different connectome | Locomotion pattern preserved (forward crawling); speed within ±30% of Cook2019 result |
| **Sensitivity analysis** | Cook2019 + Varshney2011 | Compare which connections are critical | Identify connections present in both datasets that most affect behavior |
| **Bilateral symmetry** | All datasets | `convert_to_symmetry_array()` metric | Datasets should show >40% bilateral symmetry for chemical synapses (biological expectation) |

### Bilateral Symmetry as a Validation Metric

The worm's nervous system is largely bilaterally symmetric — left and right neuron pairs (e.g., AVAL/AVAR) receive similar inputs and produce similar outputs. `cect` v0.2.7 includes bilateral symmetry analysis (added Feb 2026):

```python
from cect.Analysis import convert_to_symmetry_array

# Compute symmetry for each dataset
for dataset_name, reader_module in [("Cook2019Herm", "Cook2019HermReader"), ...]:
    cds = get_instance(from_cache=True)
    arr, pct, info = convert_to_symmetry_array(cds, ["Generic_CS"])
    print(f"{dataset_name}: {pct:.1f}% bilateral symmetry")
```

**Use case:** If the simulation produces asymmetric behavior (e.g., the worm always turns left), compare against the bilateral symmetry metric. A highly symmetric connectome should produce roughly symmetric behavior.

---

## Developmental Connectome Support

### Witvliet Developmental Series

Witvliet et al. (2021) published 8 connectome reconstructions spanning L1 larval stage through adult:

| Stage | Reader | Neurons | Notes |
|-------|--------|---------|-------|
| Witvliet 1 | `WitvlietDataReader1` | ~180 | L1 early |
| Witvliet 2 | `WitvlietDataReader2` | ~180 | L1 |
| Witvliet 3 | `WitvlietDataReader3` | ~180 | L1 late |
| Witvliet 4 | `WitvlietDataReader4` | ~240 | L2 |
| Witvliet 5 | `WitvlietDataReader5` | ~270 | L3 |
| Witvliet 6 | `WitvlietDataReader6` | ~270 | L3/L4 |
| Witvliet 7 | `WitvlietDataReader7` | ~280 | L4 |
| Witvliet 8 | `WitvlietDataReader8` | ~300 | Adult |

### Interaction with [DD001](DD001_Neural_Circuit_Architecture.md)

[DD001](DD001_Neural_Circuit_Architecture.md) assumes a single adult hermaphrodite connectome (302 neurons). Developmental connectome support requires:

1. **Neuron birth/death:** Not all 302 neurons exist at all stages. `cect` handles this — each stage reader returns only the neurons present at that stage.
2. **Connection strength changes:** Synapse counts change during development. The `number` field in `ConnectionInfo` reflects the stage-specific count.
3. **Simulation implication:** To simulate a developmental stage, set `data.connectome.dataset: "WitvlietN"` in `openworm.yml`. [DD001](DD001_Neural_Circuit_Architecture.md)'s c302 framework handles variable neuron counts.
4. **Validation caveat:** [DD010](DD010_Validation_Framework.md) kinematic benchmarks are from adult worms. Developmental stage simulations require stage-specific behavioral data for validation (limited availability).

**Current recommendation:** Use Witvliet stages for cross-validation and sensitivity analysis, not as primary simulation input. [DD001](DD001_Neural_Circuit_Architecture.md)'s default remains Cook2019Herm (adult).

---

## Alternatives Considered

### 1. Use OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) as the Sole Connectome Data Access Layer

**Description:** Route all connectome queries through OWMeta's RDF knowledge graph.

**Deferred (not rejected) because:**

- OWMeta wraps connectome data in a semantic layer (RDF triples, SPARQL-like queries) that adds complexity without clear benefit for adjacency matrix access
- OWMeta's `owmeta` package is dormant (last real commit Jul 2024); `cect` is actively maintained (commits within days)
- `cect` provides direct Python API access to 30+ datasets; OWMeta has ingestion scripts for fewer datasets
- `cect` already has caching, cell classification, neurotransmitter identity, and visualization built in

**When to reconsider:** In Phase 3+, when OWMeta integrates CeNGEN, WormAtlas, and other non-connectome data sources, `cect` data should flow *through* OWMeta to provide a unified semantic layer. At that point, [DD008](DD008_Data_Integration_Pipeline.md)'s OWMeta would call `cect` internally, and consuming DDs could use either API. See "Relationship to [DD008](DD008_Data_Integration_Pipeline.md)" below.

### 2. Parse Raw Published Data Files Directly

**Description:** Each consuming DD downloads CSV/Excel files from journal supplementary materials and parses them with custom scripts.

**Rejected because:**

- Cell name inconsistencies across publications (Cook uses "AVAL", some papers use "AVA(L)", White uses different conventions)
- No shared cell classification or neurotransmitter identity
- Each DD reinvents parsing logic; bugs are not shared/fixed centrally
- No version pinning; source URLs can change
- `cect` already solves all these problems

### 3. Maintain a Static Adjacency Matrix in the OpenWorm Meta-Repo

**Description:** Export Cook2019Herm as a static CSV/NumPy file, commit to `openworm/OpenWorm`, and have all DDs read from that file.

**Rejected because:**

- Loses dataset metadata (neurotransmitter identity, synapse types, cell classification)
- Cannot easily switch datasets for cross-validation
- Must manually update when corrections are published
- Cannot leverage `cect`'s growing dataset collection

### 4. Build a Custom Connectome Access Library

**Description:** Write an OpenWorm-specific connectome library separate from `cect`.

**Rejected because:**

- `cect` already exists, is actively maintained by Padraig, and is approaching preprint publication
- Duplicating effort; `cect` has ~4 years of development and 30+ dataset readers
- OpenWorm should contribute to `cect`, not compete with it

### 5. Default to OpenWormUnifiedReader Instead of Cook2019Herm

**Description:** Use the "unified" reader as the default for all simulations.

**Deferred because:**

- OpenWormUnifiedReader is explicitly marked "WIP — subject to change without notice" (as of Feb 2026)
- Currently wraps Wang2024Reader, which is based on neurotransmitter reporter data, not EM reconstruction — different methodology than Cook2019
- The unified reader's connection counts and topology may change as it evolves
- Use for forward-looking development, not production simulations

**When to reconsider:** When OpenWormUnifiedReader stabilizes and Padraig removes the WIP designation.

---

## Quality Criteria

### What Defines Valid Connectome Data Access?

1. **API-only access:** All connectome data loaded via `cect` reader's `get_instance()` function. No raw file parsing.

2. **Explicit dataset naming:** Every consuming DD's code or config must name the dataset reader (e.g., `Cook2019HermReader`). No unnamed/default datasets.

3. **Version pinning:** `cect` version pinned in `versions.lock`. `openworm.yml` records dataset name.

4. **Cell name consistency:** Use cell names as returned by `cect`. Do not apply custom normalization or renaming.

5. **Reproducible queries:** Running the same query with the same `cect` version and `from_cache=True` must return identical results.

6. **Cache usage in CI:** CI builds use `from_cache=True` to ensure deterministic results independent of external data availability.

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **OWMeta/RDF knowledge graph:** [DD008](DD008_Data_Integration_Pipeline.md) owns the semantic data layer. This DD owns the direct Python API layer (`cect`). See "Relationship to [DD008](DD008_Data_Integration_Pipeline.md)" for the boundary.

2. **Neural circuit modeling:** [DD001](DD001_Neural_Circuit_Architecture.md) owns how connectome topology is translated into NeuroML network files. This DD provides the topology; [DD001](DD001_Neural_Circuit_Architecture.md) consumes it.

3. **Neuropeptidergic modeling:** [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) owns the biological interpretation of Ripoll-Sanchez neuropeptide data. This DD provides access to the data.

4. **Cell-type differentiation:** [DD005](DD005_Cell_Type_Differentiation_Strategy.md) owns CeNGEN expression-to-conductance mapping. This DD does not cover transcriptomic data access.

5. **Pharyngeal system modeling:** [DD007](DD007_Pharyngeal_System_Architecture.md) owns the pharyngeal oscillator model. This DD provides the pharyngeal subset of the connectome.

6. **Visualization rendering:** [DD014](DD014_Dynamic_Visualization_Architecture.md)/DD014.1 own the viewer. This DD's visualization is for data exploration via `cect`'s built-in Plotly figures, not for the simulation viewer.

7. **Individual connectome variation:** Natural genetic variation affecting synaptic connectivity is out of scope. This DD uses population-representative published reconstructions.

---

## Context & Background

### ConnectomeToolbox History

The *C. elegans* connectome — the complete wiring diagram of the nervous system — has been the foundation of the OpenWorm project since its inception. The original dataset (White et al. 1986) was manually compiled from electron micrographs. Over four decades, multiple groups have re-analyzed, corrected, and extended this data:

| Year | Dataset | Key Contribution | `cect` Reader |
|------|---------|------------------|---------------|
| 1986 | White et al. | Original 302-neuron hermaphrodite connectome | `WhiteDataReader` |
| 2011 | Varshney et al. | Digital re-analysis of White's EM data | `VarshneyDataReader` |
| 2016 | Bentley et al. | Monoamine network mapping | Via `WormNeuroAtlas` |
| 2019 | Cook et al. | Whole-animal EM reconstruction, both sexes, corrects ~150 errors | `Cook2019HermReader`, `Cook2019MaleReader` |
| 2020 | Cook et al. | Updated analysis | `Cook2020DataReader` |
| 2021 | Witvliet et al. | 8-stage developmental series (L1 through adult) | `WitvlietDataReader1-8` |
| 2021 | Brittin et al. | Contact area-based adjacency | `BrittinDataReader` |
| 2023 | Randi et al. | Whole-brain calcium imaging functional connectivity | `WormNeuroAtlasFuncReader` |
| 2023 | Ripoll-Sanchez et al. | Neuropeptide-receptor network (31,479 interactions) | `RipollSanchezShortRangeReader` etc. |
| 2024 | Wang et al. | Neurotransmitter atlas (16 systems, CRISPR/Cas9 reporters) | `Wang2024HermReader`, `Wang2024MaleReader` |
| 2024 | Yim et al. | Updated connectivity analysis | `Yim2024DataReader` |

Padraig Gleeson created the ConnectomeToolbox (`cect`) to provide unified access to all these datasets through a consistent Python API. As of v0.2.7 (Feb 2026), it includes 30+ dataset readers, cell classification, neurotransmitter identity, bilateral symmetry analysis, and multiple visualization modes.

### Recent Activity (Feb 2026)

- **Feb 10:** Bilateral symmetry analysis notebook added
- **Feb 10:** OpenWormUnifiedReader switched to Wang2024Reader base
- **Feb 11:** Electrical connections added to OpenWormUnifiedReader
- **Feb 12 meeting:** Padraig reported the preprint is "nearly finished"
- **Feb 13:** Merge of latest updates to main branch

### Why This DD Is Needed Now

ConnectomeToolbox is already referenced as a dependency in 9 existing DDs ([DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md), [DD013](DD013_Simulation_Stack_Architecture.md), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md), [DD019](DD019_Closed_Loop_Touch_Response.md)), yet no DD specifies *how* it should be used, *which* dataset to default to, or *how* to pin versions. Key risks without [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md):

1. **Dataset drift:** [DD001](DD001_Neural_Circuit_Architecture.md) uses `Cook2019Herm` while [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) uses `RipollSanchezShortRange` — both valid, but no policy coordinates them
2. **Version skew:** One consumer pins `cect==0.2.5`, another installs latest; connection counts differ silently
3. **API inconsistency:** Some consumers parse `original_connection_infos`, others use `connections` matrices; no canonical pattern
4. **Update risk:** `cect` updates break simulations because no regression testing policy exists

---

## Relationship to [DD008](DD008_Data_Integration_Pipeline.md) (OWMeta)

**Clear boundary:** `cect` and OWMeta serve different purposes and should coexist:

| Aspect | `cect` ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) | OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) |
|--------|----------------|----------------|
| **Architecture** | Direct Python API | RDF semantic graph |
| **Query style** | `get_instance()` → `ConnectomeDataset` | `connect("openworm_data")` → SPARQL-like |
| **Data scope** | Connectome topology only | Connectome + CeNGEN + WormAtlas + lineage + ... |
| **Maintainer** | Padraig Gleeson (active) | OWMeta team (dormant since Jul 2024) |
| **Current status** | v0.2.7, 30+ datasets, preprint pending | Working but under-maintained |
| **Best for** | Direct adjacency matrix access, visualization, cross-dataset comparison | Unified multi-modal biological queries, provenance tracking |

**Phase 1-2 (now):** Use `cect` directly. It's actively maintained, has the datasets we need, and provides the API patterns consuming DDs require.

**Phase 3+ (future):** When OWMeta becomes active again, it should call `cect` internally as its connectome data provider. Consuming DDs could then use either `cect` (direct) or OWMeta (semantic) depending on their needs. [DD008](DD008_Data_Integration_Pipeline.md) should add a `cect` ingestion adapter:

```python
# Future [DD008](DD008_Data_Integration_Pipeline.md) integration (Phase 3+)
# OWMeta calls cect internally
from owmeta_core import connect
conn = connect("openworm_data")
# Under the hood: OWMeta uses cect.Cook2019HermReader
neurons = list(conn.query(Neuron)())
```

---

## Configuration

### `openworm.yml` Section

```yaml
data:
  connectome:
    # Primary structural connectome
    dataset: "Cook2019Herm"             # Required. Reader name from cect.
    cect_version: "0.2.7"              # Required. Must match versions.lock.
    use_cache: true                     # Recommended. Use cached JSON for speed/reproducibility.

    # Pharyngeal subset ([DD007](DD007_Pharyngeal_System_Architecture.md))
    pharyngeal_dataset: "Cook2019Herm"  # Same dataset, different view filter
    pharyngeal_view: "Pharynx"          # View filter name

    # Developmental (optional, null = disabled)
    developmental_dataset: null         # "Witvliet1" through "Witvliet8"

    # Functional connectivity validation target ([DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md))
    functional_dataset: "Randi2023"     # WormNeuroAtlasFuncReader

    # Neuropeptidergic ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md))
    neuropeptide_dataset: "RipollSanchezShortRange"

    # Neurotransmitter identity ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md), experimental)
    neurotransmitter_dataset: "Wang2024Herm"

    # Cross-validation dataset ([DD010](DD010_Validation_Framework.md))
    cross_validation_dataset: "Witvliet8"
```

| Key | Default | Valid Values | Description |
|-----|---------|-------------|-------------|
| `data.connectome.dataset` | `"Cook2019Herm"` | Any `cect` reader name | Primary structural connectome dataset |
| `data.connectome.cect_version` | `"0.2.7"` | Semver string | `cect` package version pin |
| `data.connectome.use_cache` | `true` | `true`/`false` | Load from cached JSON (recommended) |
| `data.connectome.pharyngeal_dataset` | `"Cook2019Herm"` | Reader name | Dataset for pharyngeal subset |
| `data.connectome.pharyngeal_view` | `"Pharynx"` | View filter name | `cect` view filter for pharynx |
| `data.connectome.developmental_dataset` | `null` | `"Witvliet1"` - `"Witvliet8"` / `null` | Developmental series dataset |
| `data.connectome.functional_dataset` | `"Randi2023"` | Reader name | Functional connectivity target |
| `data.connectome.neuropeptide_dataset` | `"RipollSanchezShortRange"` | Ripoll-Sanchez reader name | Neuropeptide network dataset |
| `data.connectome.neurotransmitter_dataset` | `"Wang2024Herm"` | Wang2024 reader name | Neurotransmitter identity dataset |
| `data.connectome.cross_validation_dataset` | `"Witvliet8"` | Reader name | Independent dataset for cross-validation |

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source | Variable | Format | Units |
|-------|--------|----------|--------|-------|
| Published connectome datasets (external) | Journal supplementary materials | EM reconstructions, neurotransmitter atlases | Excel, CSV, TSV | Connection counts |
| `openworm.yml` connectome config | [DD013](DD013_Simulation_Stack_Architecture.md) config system | Dataset selection, version pin | YAML | config keys |
| `versions.lock` cect version | [DD013](DD013_Simulation_Stack_Architecture.md) build system | `cect` package version | Lock file | semver |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Structural adjacency matrices (chemical + electrical) | [DD001](DD001_Neural_Circuit_Architecture.md) (neural circuit topology) | `ConnectomeDataset.connections` dict | `dict[str, np.ndarray]` | Connection counts |
| `ConnectionInfo` list | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md) (neuron→muscle mapping) | `ConnectomeDataset.original_connection_infos` | `list[ConnectionInfo]` | pre_cell, post_cell, number, syntype, synclass |
| Neuron-to-neuron connections | [DD001](DD001_Neural_Circuit_Architecture.md) (synapse generation) | `get_neuron_to_neuron_conns()` | `list[ConnectionInfo]` | Connection counts |
| Neuron-to-muscle connections | [DD002](DD002_Muscle_Model_Architecture.md) (NMJ coupling) | `get_neuron_to_muscle_conns()` | `list[ConnectionInfo]` | Connection counts |
| Pharyngeal connectome view | [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx circuit) | `get_connectome_view("Pharynx")` | `ConnectomeDataset` (filtered) | Connection counts |
| Cell classification | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD014](DD014_Dynamic_Visualization_Architecture.md) (neuron type labeling) | `get_SIM_class()`, cell lists | Python API | Category strings |
| Neuropeptide network | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (peptidergic modulation) | Ripoll-Sanchez readers | `ConnectomeDataset` | Interaction scores |
| Neurotransmitter identity | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (synapse type assignment) | Wang2024Reader | `ConnectionInfo.synclass` | NT names |
| Bilateral symmetry metrics | [DD010](DD010_Validation_Framework.md) (validation), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (ML targets) | `convert_to_symmetry_array()` | `(ndarray, float, str)` | Percentage |
| Developmental connectome series | [DD019](DD019_Closed_Loop_Touch_Response.md) (developmental validation) | Witvliet 1-8 readers | `ConnectomeDataset` per stage | Connection counts |
| Functional connectivity matrix | [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) (validation target) | `WormNeuroAtlasFuncReader` | `ConnectomeDataset` | Correlation values |
| NetworkX graph | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (graph neural networks) | `to_networkx_graph()` | `networkx.DiGraph` | Weighted edges |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository** | `openworm/ConnectomeToolbox` |
| **Docker stage** | `data` (installed via pip in neural/body/pharynx stages) |
| **`versions.lock` key** | `cect` |
| **Build dependencies** | numpy <2.4, xlrd, openpyxl, wormneuroatlas, networkx, hiveplotlib <=0.25.1, webcolors, pyneuroml |
| **Data in image** | Cached JSON files from `cect/cache/` (~5MB total) |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
python -c "
from cect.Cook2019HermReader import get_instance
cds = get_instance(from_cache=True)
assert len(cds.nodes) >= 300, f'Expected 300+ nodes, got {len(cds.nodes)}'
assert len(cds.original_connection_infos) > 0, 'No connections loaded'
print('[DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) quick test: PASS')
"

# Full validation (must pass before merge)
python -c "
import cect
assert cect.__version__ == '0.2.7', f'Version mismatch: {cect.__version__}'

from cect.Cook2019HermReader import get_instance
cds = get_instance(from_cache=True)

# Verify neuron count
from cect.Cells import SENSORY_NEURONS_COOK, INTERNEURONS_COOK, MOTORNEURONS_COOK
total_neurons = len(SENSORY_NEURONS_COOK) + len(INTERNEURONS_COOK) + len(MOTORNEURONS_COOK)
assert total_neurons > 280, f'Expected 280+ neurons, got {total_neurons}'

# Verify cell classification
from cect.Cells import get_SIM_class
assert get_SIM_class('AVAL') == 'Interneuron'
assert get_SIM_class('DA01') == 'Motorneuron'

# Verify bilateral symmetry works
from cect.Analysis import convert_to_symmetry_array
arr, pct, info = convert_to_symmetry_array(cds, ['Generic_CS'])
assert 0 < pct < 100, f'Symmetry percentage out of range: {pct}'

print('[DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) full validation: PASS')
"
```

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| Data Flow | Description |
|-----------|-------------|
| `cect` → [DD001](DD001_Neural_Circuit_Architecture.md) → OME-Zarr → [DD014](DD014_Dynamic_Visualization_Architecture.md) | Connectome topology flows through c302 into simulation output; [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer displays neuron connectivity as part of the neural layer |
| `cect` → Plotly (direct) | `cect`'s built-in `to_plotly_*` methods for data exploration and publication figures |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Published connectome datasets (external) | None | If Cook et al. publish corrections, `cect` readers must be updated by Padraig |
| `cect` Python package (external) | None | If `cect` API changes, all consuming DDs must update imports |
| [DD013](DD013_Simulation_Stack_Architecture.md) config system | [DD013](DD013_Simulation_Stack_Architecture.md) | If `openworm.yml` schema changes, `data.connectome` keys must be updated |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Neural circuit topology | [DD001](DD001_Neural_Circuit_Architecture.md) | Changing default dataset changes every synapse in the simulation |
| Muscle innervation | [DD002](DD002_Muscle_Model_Architecture.md) | Neuron-to-muscle connection list drives NMJ coupling |
| Cell-type differentiation | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Cook2019 neuron list defines which cells to differentiate |
| Neuropeptidergic network | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Ripoll-Sanchez data defines peptide-receptor interactions |
| Pharyngeal circuit | [DD007](DD007_Pharyngeal_System_Architecture.md) | Pharyngeal view filter defines pharynx neuron connectivity |
| Data integration | [DD008](DD008_Data_Integration_Pipeline.md) | OWMeta ingests connectome data from `cect` (Phase 3+) |
| Simulation stack | [DD013](DD013_Simulation_Stack_Architecture.md) | `cect` version pinned in `versions.lock` |
| Hybrid ML framework | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) | Graph structure (via NetworkX) used for graph neural networks |
| Closed-loop touch response | [DD019](DD019_Closed_Loop_Touch_Response.md) | Touch neuron connectivity (MEC-4 neurons) from `cect` |

---

## Known Issues and Future Work

### Issue 1: OpenWormUnifiedReader Is WIP

The "unified" reader is intended to become the single best-estimate connectome, but as of Feb 2026 it wraps Wang2024Reader and is marked "subject to change without notice." Using it as a default would introduce instability.

**Mitigation:** Default to Cook2019Herm. Monitor OpenWormUnifiedReader stability. Adopt as default only after WIP designation is removed and regression tests pass.

### Issue 2: Cell Name Variants Across Datasets

Different datasets use slightly different cell naming conventions. `cect` handles this internally via `map_cell_name()` methods in each reader, but edge cases may remain.

**Mitigation:** Always use cell names as returned by `cect`. Report naming inconsistencies as issues on `openworm/ConnectomeToolbox`.

### Issue 3: Connection Count Discrepancies Between Datasets

Cook2019 and Witvliet8 are both adult hermaphrodite connectomes but report different connection counts for some neuron pairs. This is expected (different animals, different EM volumes) but can confuse validation.

**Mitigation:** Use Cook2019Herm as primary, Witvliet8 as cross-validation. Document expected discrepancy ranges.

### Issue 4: Preprint Not Yet Published

The ConnectomeToolbox preprint (Gleeson et al., in preparation) is not yet available. Once published, this DD should be updated with the citation and DOI.

**Future action:** Add citation when preprint appears on bioRxiv.

---

## References

1. **White JG, Southgate E, Thomson JN, Brenner S (1986).** "The structure of the nervous system of the nematode *Caenorhabditis elegans*." *Phil Trans R Soc B* 314:1-340.
   *Original connectome.*

2. **Varshney LR, Chen BL, Paniagua E, Hall DH, Chklovskii DB (2011).** "Structural properties of the *Caenorhabditis elegans* neuronal network." *PLoS Comput Biol* 7:e1001066.
   *Digital re-analysis.*

3. **Cook SJ, Jarrell TA, Brittin CA, Wang Y, Bloniarz AE, Yaber MA, et al. (2019).** "Whole-animal connectomes of both *Caenorhabditis elegans* sexes." *Nature* 571:63-71.
   *Gold standard whole-animal EM reconstruction.*

4. **Witvliet D, Mulcahy B, Mitchell JK, Meiber Y, Anber R, Bhatia A, et al. (2021).** "Connectomes across development reveal principles of brain maturation." *Nature* 596:257-261.
   *Developmental connectome series (8 stages).*

5. **Randi F, Sharma AK, Dvali N, Leifer AM (2023).** "Neural signal propagation atlas of *Caenorhabditis elegans*." *Nature* 623:406-414.
   *Functional connectivity.*

6. **Ripoll-Sanchez L, Watteyne J, Sun H, Fernandez R, Taylor SR, Weinreb A, et al. (2023).** "The neuropeptidergic connectome of *C. elegans*." *Neuron* 111:3570-3589.
   *Neuropeptide-receptor interaction network.*

7. **Wang C, et al. (2024).** "A neurotransmitter atlas of *C. elegans* males and hermaphrodites." *eLife* 13:RP95402.
   *CRISPR/Cas9 neurotransmitter reporter atlas.*

8. **Gleeson P et al. (in preparation).** "ConnectomeToolbox: a unified Python toolkit for *C. elegans* connectome data."
   *`cect` package preprint.*

---

**Approved by:** Pending (Dataset Policy)
**Implementation Status:** Proposed
**Next Actions:**

1. Pin `cect==0.2.7` in `versions.lock`
2. Add `data.connectome` section to `openworm.yml` schema
3. Update [DD001](DD001_Neural_Circuit_Architecture.md) coupling table: `ConnectomeToolbox (external)` → `DD020`
4. Update [DD008](DD008_Data_Integration_Pipeline.md) coupling table: add [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) as connectome data source
5. Create CI test for `cect` version and default dataset load
6. Monitor OpenWormUnifiedReader stability for future default adoption
