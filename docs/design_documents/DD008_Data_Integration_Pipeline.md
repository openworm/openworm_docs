# DD008: Data Integration Pipeline and OWMeta Knowledge Graph

**Status:** Accepted (with proposed extensions)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** None  
**Related:** All other DDs (data layer for entire project)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | Unified data access layer (OWMeta) for connectome, CeNGEN expression, cell positions, neuropeptide interactions — all via Python API |
| **Success metric** | All downstream DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md)) can query data via OWMeta; ID consistency (all neuron/cell IDs map to WBbt ontology) |
| **Repository** | [`openworm/owmeta`](https://github.com/openworm/owmeta) + [`openworm/owmeta-core`](https://github.com/openworm/owmeta-core) — issues labeled `dd008` |
| **Config toggle** | `data.backend: owmeta` (recommended) or `data.backend: direct` (legacy) in `openworm.yml` |
| **Build & test** | `docker compose run shell python -c "import owmeta_core"` (installs?), query 302 neurons (returns correct count?) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `geometry/cell_metadata.json` — cell names, types, lineage for viewer tooltips and search |
| **CI gate** | OWMeta installation + basic query test blocks merge for data-layer changes |

---

## TL;DR

OWMeta is a semantic knowledge graph providing unified programmatic access to 15+ biological data sources (WormBase, CeNGEN, Cook connectome, Ripoll-Sanchez neuropeptides, Randi functional connectivity, etc.). All modeling code should access data through OWMeta, not by parsing raw files. Success: all downstream DDs can query data via a unified API; ID consistency across all datasets with every neuron/cell ID mapping to the WBbt ontology.

---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** ID consistency | All neuron/cell IDs map to WBbt ontology; no orphaned IDs | Tier 1 (blocking) |
| **Secondary:** Dataset ingestion | All Phase 1-3 datasets ingested and queryable via OWMeta | Tier 1 (blocking) |
| **Tertiary:** Downstream migration | c302, Sibernetic init, and validation scripts successfully migrated to OWMeta queries | Tier 2 (blocking) |

**Before:** Each contributor writes custom parsers for CSV/JSON files from different sources; IDs are inconsistent across datasets (Cook uses "AVAL," WormBase uses "WBGene00006748"); data versions drift.

**After:** Single `connect("openworm_data")` call provides unified access to all datasets with normalized IDs, versioned data, and provenance metadata.

---

## Deliverables

| Artifact | Path / Location | Format | Example |
|----------|----------------|--------|---------|
| OWMeta data bundles | `openworm_data` bundle (baked into Docker image or downloaded at build) | RDF graph (OWMeta bundle) | `connect("openworm_data")` |
| Ingestion scripts per dataset | `openworm/owmeta` repo, per-dataset scripts | Python | `ingest_ripoll_sanchez.py`, `ingest_witvliet.py` |
| Python query API | `owmeta-core` + `owmeta` packages | Python package (pip) | `pip install owmeta-core owmeta` |
| Entity types | OWMeta schema | Python classes (RDF-backed) | `Neuron`, `Muscle`, `Connection`, `Gene`, `Channel`, `Cell` |
| Cell metadata for viewer | OME-Zarr: `geometry/cell_metadata.json` | JSON | Cell names, types, lineage, WormAtlas links |
| Configuration schema | `openworm.yml` `data:` section | YAML | `data.backend: owmeta` |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/owmeta`](https://github.com/openworm/owmeta) + [`openworm/owmeta-core`](https://github.com/openworm/owmeta-core) |
| **Issue label** | `dd008` |
| **Milestone** | Phase 1-3: Data Integration |
| **Branch convention** | `dd008/description` (e.g., `dd008/ingest-ripoll-sanchez`) |
| **Example PR title** | `DD008: Ingest Ripoll-Sanchez neuropeptide-receptor pairs into OWMeta` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: Python 3.10+, pip

### Step-by-step

```bash
# Step 1: Install OWMeta packages
pip install owmeta-core owmeta

# Step 2: Verify import works
python -c "import owmeta_core; print(owmeta_core.__version__)"

# Step 3: Verify data queries work
python -c "
from owmeta_core import connect
conn = connect('openworm_data')
# Verify connectome query returns 302 neurons
neurons = list(conn.query(Neuron)())
assert len(neurons) >= 302, f'Expected 302+ neurons, got {len(neurons)}'
print(f'Connectome loaded: {len(neurons)} neurons')
"

# Step 4: Docker-based verification
docker compose run shell python -c "import owmeta_core; print(owmeta_core.__version__)"

# Step 5: Backward compatibility (direct backend)
# When data.backend: "direct", OWMeta is not required
# Modeling code falls back to direct file access
docker compose run quick-test  # with data.backend: "direct"
```

### Scripts that don't exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `ingest_ripoll_sanchez.py` | `[TO BE CREATED]` | openworm/owmeta#TBD |
| `ingest_witvliet.py` | `[TO BE CREATED]` | openworm/owmeta#TBD |
| `ingest_randi.py` | `[TO BE CREATED]` | openworm/owmeta#TBD |

### Green light criteria

- `import owmeta_core` succeeds in Docker
- Query returns >= 302 neurons
- `docker compose run quick-test` passes with `data.backend: "direct"` (backward compatibility)

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** `geometry/cell_metadata.json` for tooltips, search, and cell identification.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `geometry/` (cell metadata overlay) |
| **Data source** | OME-Zarr: `geometry/cell_metadata.json` — cell names, types, lineage, WormAtlas links |
| **What you should SEE** | Clicking any cell in the 3D viewer shows its WBbt ID, cell type, lineage, and links to WormAtlas. Search by cell name returns the correct 3D position. All 302 neurons + non-neural cells are labeled and searchable. |
| **Color mapping** | Cell type color coding: neurons (by class), muscles (by quadrant), intestinal cells, hypodermal cells |

---

## Technical Approach

### Use OWMeta as the Canonical Data Access Layer

All modeling code (c302, Sibernetic initialization, validation scripts) MUST access biological data through OWMeta, not by directly parsing raw files.

**Rationale:**
- **Single source of truth:** WormBase IDs, cell names, gene symbols are normalized
- **Versioned:** OWMeta tracks dataset versions (e.g., WS298, CeNGEN v1.0)
- **Queryable:** Semantic queries like "Get all neurons in the nerve ring expressing unc-2" are one-liners
- **Extensible:** New datasets (Ripoll-Sanchez neuropeptides, Witvliet development) can be added without modifying downstream code

### OWMeta Entity Types

| Entity | Properties | Example |
|--------|-----------|---------|
| **Neuron** | name, WormBase ID, type (sensory/inter/motor), position | `AVAL` (WBbt:0006748) |
| **Muscle** | name, quadrant, row, innervation | `MDR05` |
| **Connection** | pre, post, type (syn/gap/peptide), weight | `AVAL → AVAR` (gap) |
| **Gene** | symbol, WormBase ID, expression by cell | `unc-2` (WBGene00006765) |
| **Channel** | gene, type (Kv/Cav/Cl), NeuroML model | `unc-2` → `ca_boyle_chan` |
| **Cell** | WBbt ID, lineage, anatomy, neighbors | `int5` (WBbt:0005193) |

### Example Queries

**Get all neurons expressing unc-2:**
```python
from owmeta_core import connect
conn = connect("openworm_data")

neurons = conn.query(Neuron)().get_neuron_type_by_expression("unc-2")
for n in neurons:
    print(f"{n.name()}: {n.expression_level('unc-2')} TPM")
```

**Get connectome for AVAL:**
```python
aval = Neuron(name="AVAL")
connections = aval.connection.get()
for c in connections:
    print(f"{c.pre_cell()} -> {c.post_cell()}: {c.connection_type()} weight={c.weight()}")
```

**Get 3D position for all intestinal cells:**
```python
intestine_cells = Cell.query(lineage_contains="E")  # E lineage = intestine
for cell in intestine_cells:
    pos = cell.position_3d()  # From WormAtlas or Witvliet EM
    print(f"{cell.name()}: {pos}")
```

### Data Ingestion Priority

| Dataset | OWMeta Status | Priority | Action |
|---------|--------------|---------|--------|
| Cook 2019 connectome | Integrated | -- | Maintain |
| WormBase WS298 | Integrated | -- | Maintain (archival) |
| WormAtlas anatomy | Partial | High | Complete integration |
| CeNGEN L4 expression | Integrated | -- | Maintain |
| CeNGEN L1 expression | Not yet | Medium | Add in Phase 1 |
| Witvliet 2021 dev. connectomes | Not yet | High | Add for Phase 6 (development) |
| Ripoll-Sanchez neuropeptides | Not yet | High | Add for Phase 2 ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) |
| Randi 2023 functional connectivity | Not yet | High | Add for validation |
| Packer 2019 embryonic scRNA-seq | Not yet | Medium | Add for Phase 6 |
| Ben-David 2021 eQTLs | Not yet | Low | Phase 6+ |

### OWMeta Update Process (For Contributors)

**DO NOT directly edit OWMeta.**  Updates go through a review process:

1. **Propose a dataset addition** via GitHub issue on the OWMeta repository
2. **Provide data source:** DOI, URL, file format, license
3. **Provide mapping:** How identifiers in the new dataset map to WormBase IDs or WBbt ontology
4. **Write an ingestion script** following OWMeta patterns
5. **Submit PR** with ingestion script + documentation + example queries
6. **Maintainer review:** OWMeta maintainers check for ID conflicts, data quality, schema consistency
7. **Merge and version:** New dataset becomes available in next OWMeta release

**Do not:**
- Parse raw CSV/JSON files directly in modeling code
- Hardcode cell IDs or gene names
- Duplicate data across repositories

---

## Alternatives Considered

### 1. Direct File Parsing (No OWMeta)

**Rejected:** Every contributor writing their own CSV parser leads to:
- ID mismatches (Cook uses "AVAL," WormBase uses "WBGene00006748")
- Version drift (contributor uses old WormBase release)
- Code duplication

### 2. SQL Database Instead of Semantic Graph

**Rejected:** Semantic RDF graphs better capture biological relationships (is-a, part-of, expressed-in, connected-to) than rigid SQL schemas. OWMeta uses RDF + SPARQL.

### 3. Use WormBase API Directly

**Partial use:** WormBase REST API is a data source for OWMeta. But WormBase lacks:
- Connectome data (ConnectomeToolbox)
- Single-cell expression (CeNGEN)
- 3D positions (WormAtlas)

OWMeta aggregates WormBase + all other sources.

---

## Quality Criteria

1. **All Data Versioned:** OWMeta must track the version of every source dataset (e.g., "WormBase WS298," "CeNGEN v1.0 L4").

2. **ID Consistency:** All neuron/cell identifiers must map to WBbt ontology. No orphaned IDs.

3. **Provenance Metadata:** Every datum includes source DOI, access date, confidence level (experimental/inferred).

4. **API Stability:** OWMeta query syntax must remain backward-compatible across updates. Deprecate gracefully.

---

## Context & Background

OpenWorm integrates data from 15+ sources: WormBase, WormAtlas, CeNGEN, Cook connectome, Witvliet developmental data, Ripoll-Sanchez neuropeptides, Randi functional connectivity, Schafer kinematics, and more. These datasets use different formats, identifiers, and coordinate systems.

**The challenge:** A contributor implementing [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (cell differentiation) must pull CeNGEN expression, map neuron IDs to CeNGEN classes, extract channel genes, and generate NeuroML. Without a unified data layer, this requires writing custom parsers for each dataset.

**The solution:** **OWMeta** (openworm.org/OWMeta) — a semantic knowledge graph providing unified programmatic access to all OpenWorm-relevant biological data.

---

## References

1. **OWMeta Documentation:** https://pypi.org/project/owmeta-core/
2. **ConnectomeToolbox:** openworm.org/ConnectomeToolbox
3. **WormBase REST API:** https://wormbase.org/about/userguide/for_developers

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source | Variable | Format | Notes |
|-------|--------|----------|--------|-------|
| Cook 2019 connectome | wormwiring.org | Neuron adjacency + weights | CSV/Excel → RDF ingestion | Already integrated |
| CeNGEN L4 scRNA-seq | cengen.org | Per-neuron-class TPM values | CSV → RDF ingestion | Already integrated |
| WormAtlas anatomy | wormatlas.org | Cell positions, morphology, EM images | HTML/images → RDF ingestion | Partial |
| Ripoll-Sanchez neuropeptides | Neuron 111:3570 supplement | Peptide-receptor pairs + expression | CSV → RDF ingestion | **Not yet ingested** (needed for [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) |
| Randi 2023 functional connectivity | Nature 623:406 supplement | 302×302 correlation matrix | NumPy .npy → RDF metadata only | **Not yet ingested** (needed for [DD010](DD010_Validation_Framework.md)) |
| Witvliet 2021 dev. connectomes | Nature 596:257 | Multi-stage connectomes (L1, L4, adult) | CSV → RDF ingestion | **Not yet ingested** (needed for Phase 6) |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Neuron adjacency (connectome) | [DD001](DD001_Neural_Circuit_Architecture.md) | Synapse pairs + weights | OWMeta query → Python objects | synapse count |
| Per-class gene expression | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | TPM per gene per neuron class | OWMeta query → DataFrame | TPM |
| Neuropeptide-receptor pairs | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Peptide ligand → receptor → expressing cells | OWMeta query → edge list | binary (expressed/not) |
| Cell positions (3D) | [DD004](DD004_Mechanical_Cell_Identity.md) | Per-cell x, y, z coordinates | OWMeta query → NumPy array | um |
| Cell ontology IDs | [DD004](DD004_Mechanical_Cell_Identity.md) | Cell name → WBbt ID mapping | OWMeta query → dict | identifiers |
| Cell metadata (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Cell names, types, lineage, WormAtlas links | OME-Zarr: `geometry/cell_metadata.json` | mixed |

### Repository & Packaging

- **Repository:** `openworm/owmeta` + `openworm/owmeta-core`
- **Docker stage:** `data` in multi-stage Dockerfile (new stage)
- **`versions.lock` key:** `owmeta`, `owmeta_core`
- **Build dependencies:** `pip install owmeta-core owmeta`
- **Data bundle:** OWMeta data bundle must be downloaded or baked into the Docker image at build time

```yaml
# versions.lock
owmeta_core:
  pypi_version: "0.14.x"         # Pin to specific minor version
owmeta:
  repo: "https://github.com/openworm/owmeta.git"
  commit: "TBD"                   # Must be updated when OWMeta is revived
```

### Configuration

**`openworm.yml` Section:**

```yaml
data:
  backend: owmeta                    # "owmeta" (recommended) or "direct" (legacy file access)
  owmeta_bundle: "openworm_data"    # OWMeta data bundle name
  connectome_dataset: "Cook2019"     # Cook2019, Witvliet2021, Varshney2011
  cengen_version: "L4_v1.0"         # CeNGEN dataset version
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `data.backend` | `owmeta` | `owmeta` / `direct` | Data access backend; `direct` is legacy fallback |
| `data.owmeta_bundle` | `"openworm_data"` | String | OWMeta data bundle name |
| `data.connectome_dataset` | `"Cook2019"` | `Cook2019`, `Witvliet2021`, `Varshney2011` | Which connectome dataset to use |
| `data.cengen_version` | `"L4_v1.0"` | String | CeNGEN dataset version pin |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test
docker compose run shell python -c "import owmeta_core; print(owmeta_core.__version__)"
# Check: import succeeds, version prints

# Data query test
docker compose run shell python -c "
from owmeta_core import connect
conn = connect('openworm_data')
neurons = list(conn.query(Neuron)())
assert len(neurons) >= 302, f'Expected 302+ neurons, got {len(neurons)}'
print(f'Connectome loaded: {len(neurons)} neurons')
"
# Check: 302+ neurons returned

# Backward compatibility test
docker compose run quick-test  # with data.backend: "direct"
# Check: simulation completes without OWMeta installed
```

**Per-PR checklist:**
- [ ] `import owmeta_core` succeeds in Docker
- [ ] Neuron count query returns >= 302
- [ ] `quick-test` passes with `data.backend: "direct"` (backward compatibility)
- [ ] New ingestion scripts include source DOI, version, and ID mapping documentation
- [ ] No orphaned IDs (all IDs map to WBbt ontology)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `geometry/cell_metadata.json` | Cell metadata overlay | Cell type color coding: neurons (by class), muscles (by quadrant), intestinal, hypodermal |

### Reality Check: Phased OWMeta Mandate

OWMeta is **dormant** (last real commit Jul 2024, `owmeta-core` last updated Mar 2025). The mandate "all code MUST use OWMeta" cannot be enforced immediately. Phased approach:

- **Phase 1:** OWMeta is **optional**. Direct file access is acceptable with documented data provenance (source DOI, version, access date).
- **Phase 2:** OWMeta is **recommended**. New code should use OWMeta where possible. Migration scripts provided for existing direct-access code.
- **Phase 3+:** OWMeta is **required**. All modeling code accesses data through OWMeta. Direct file parsing is prohibited.

**Trigger for Phase 2→3 transition:** OWMeta is installable on Python 3.12, all Phase 1-2 datasets are ingested, and at least 3 downstream consumers (c302, Sibernetic init, validation) have been successfully migrated.

### Reconciliation with [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (Connectome Data Access Policy)

**[DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)** specifies ConnectomeToolbox (`cect`, PyPI v0.2.7) as the canonical API for connectome data access. OWMeta and `cect` serve complementary purposes and should coexist:

| Aspect | `cect` ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) | OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) |
|--------|---------------|----------------|
| **Purpose** | Direct connectome data access | Semantic knowledge graph (multi-modal) |
| **Architecture** | Direct Python API | RDF semantic graph |
| **Query style** | `get_instance()` → `ConnectomeDataset` | `connect("openworm_data")` → SPARQL-like |
| **Data scope** | Connectome topology only (30+ datasets) | Connectome + CeNGEN + WormAtlas + lineage + anatomy |
| **Maintainer** | Padraig Gleeson (active, commits within days) | OWMeta team (dormant since Jul 2024) |
| **Current status** | v0.2.7, preprint pending | Working but under-maintained |
| **Best for** | Direct adjacency matrix access, visualization, cross-dataset comparison | Unified multi-modal biological queries, provenance tracking |

**Current recommendation (Phase 1-2):** Use `cect` directly for all connectome queries (see [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) API contract). This is the actively maintained, stable tool with 30+ dataset readers.

**Future integration (Phase 3+):** When OWMeta becomes active again and ingests all Phase 1-2 datasets (CeNGEN, Randi 2023, Ripoll-Sanchez, Wang 2024), it should call `cect` internally as its connectome data provider. Consuming DDs can then use either `cect` (direct, fast) or OWMeta (semantic, provenance-tracked) depending on their needs.

**Action for OWMeta revival:** Add a `cect` ingestion adapter so OWMeta wraps `cect` readers rather than duplicating connectome parsing logic.

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| WormBase releases | External | New WormBase releases may change gene IDs or annotations |
| CeNGEN updates | External | New expression data may change downstream conductances |
| ConnectomeToolbox | [DD001](DD001_Neural_Circuit_Architecture.md) | If connectome representation changes, OWMeta ingestion scripts must update |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Neural circuit (connectome queries) | [DD001](DD001_Neural_Circuit_Architecture.md) | If neuron adjacency format or ID scheme changes, c302 network generation breaks |
| Cell differentiation (expression data) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | If CeNGEN query format changes, conductance pipeline breaks |
| Neuropeptides (peptide-receptor data) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | If peptide interaction data format changes, neuropeptide layer breaks |
| Mechanical cell identity (cell positions) | [DD004](DD004_Mechanical_Cell_Identity.md) | If cell position queries change, particle tagging breaks |
| Validation (experimental data metadata) | [DD010](DD010_Validation_Framework.md) | If data provenance metadata changes, validation data versioning breaks |

---

**Approved by:** OpenWorm Steering
**Implementation Status:** Partial (core OWMeta exists, extensions proposed)
**Next Actions:**
1. Ingest Ripoll-Sanchez neuropeptides
2. Ingest Witvliet developmental connectomes
3. Ingest Randi functional connectivity
4. Document canonical query patterns for common tasks
