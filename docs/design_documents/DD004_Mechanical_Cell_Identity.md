# DD004: Mechanical Cell Identity in Sibernetic (Per-Cell Physics)

- **Status:** Proposed (Phase 4)
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** [DD003](DD003_Body_Physics_Architecture.md) (Body Physics), [DD007](DD007_Pharyngeal_System_Architecture.md) (Pharyngeal System), [DD009](DD009_Intestinal_Oscillator_Model.md) (Intestinal Model)

---

## TL;DR

Tag every SPH particle with a WBbt cell ID from EM reconstructions, enabling cell-type-specific mechanics (intestinal peristalsis, cuticle stiffness, hypodermal compliance). Extends the particle struct from 32 to 44 bytes. Success: all 959 somatic cells represented, Tier 3 kinematics within ±15%.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 4](DD_PHASE_ROADMAP.md#phase-4-mechanical-cell-identity-high-fidelity-visualization-months-13-18) |
| **Layer** | Complete Organism — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-4-mechanical-cell-identity-high-fidelity-visualization-months-13-18) |
| **What does this produce?** | Tagged particle file: each of ~100K SPH particles gets a WBbt cell ID + cell-type-specific elasticity/adhesion |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: kinematic metrics within ±15% with `cell_identity: true`; all 959 somatic cells mapped |
| **Repository** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) — issues labeled `dd004` |
| **Config toggle** | `body.cell_identity: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` with `cell_identity: false` (backward compat), then `cell_identity: true` (tagged sim) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `body/cell_ids/` layer — particles colored by cell type (muscle=red, intestine=yellow, cuticle=gray) |
| **CI gate** | Tier 3 kinematic validation blocks merge; backward compatibility with `cell_identity: false` required |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Kinematic metrics | Within ±15% of Schafer lab baseline with `cell_identity: true` | Tier 3 (blocking) |
| **Secondary:** Cell coverage | All 959 somatic cells mapped to at least one SPH particle | Required (blocking) |
| **Tertiary:** Backward compatibility | `cell_identity: false` produces identical output to unmodified Sibernetic | Required (blocking) |

**Before:** ~100K SPH particles with bulk elastic/liquid properties — all elastic particles have identical stiffness and adhesion. No cell boundaries, no per-cell mechanics.

**After:** Each SPH particle tagged with a WBbt cell ID and cell-type-specific elasticity/adhesion multipliers. 959 somatic cells represented. Intestinal, cuticle, hypodermal, and gonad sheath mechanics are cell-type-specific.

---

## Deliverables

| Artifact | Path (relative to `openworm/sibernetic`) | Format | Example |
|----------|------------------------------------------|--------|---------|
| Extended SPH_Particle_v2 struct | `src/` (C++ header) | C struct definition | 44-byte struct with `cell_id`, `elasticity_mult`, `adhesion` |
| Tagged particle initialization file | `data/particles_tagged.csv` | CSV | `particle_id,x,y,z,type,cell_id,elasticity,adhesion` |
| Cell-to-particle mapping | `data/cell_to_particle_map.json` | JSON | `{"WBbt:0005189": [0, 1, 2, ...], ...}` |
| Cell boundary meshes | `data/cell_boundaries/` | OBJ or STL per cell | `data/cell_boundaries/int1.obj` |
| Cell identity labels (viewer) | OME-Zarr: `body/cell_ids/`, shape (n_particles,) | OME-Zarr | Integer cell ID per particle |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) |
| **Issue label** | `dd004` |
| **Milestone** | Phase 4: Mechanical Cell Identity |
| **Branch convention** | `dd004/description` (e.g., `dd004/particle-tagging`) |
| **Example PR title** | `DD004: Implement per-particle cell ID tagging from Witvliet EM data` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: OpenCL SDK, CMake, C++ compiler (same as [DD003](DD003_Body_Physics_Architecture.md))
- Cell boundary mesh data from [Witvliet et al. 2021](https://doi.org/10.1038/s41586-021-03778-8) (included in Docker image or downloaded at build time)

### Step-by-step

```bash
# Step 1: Verify backward compatibility (cell_identity: false)
docker compose run quick-test  # with cell_identity: false in openworm.yml
# Green light: produces identical output to unmodified Sibernetic
# Green light: simulation completes without NaN, segfault, or SIGKILL

# Step 2: Run tagged simulation (cell_identity: true)
# (modify openworm.yml: body.cell_identity: true)
docker compose run quick-test
# Green light: simulation completes without crash
# Green light: all particle cell_ids are valid WBbt identifiers
# Green light: locomotion still occurs (body still moves)

# Step 3: Validate mechanics
docker compose run validate
# Green light: Tier 3 kinematic metrics within ±15% with cell_identity enabled
# Green light: all 959 somatic cells mapped to at least one particle
```

### Scripts that may not exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/generate_tagged_particles.py` | `[TO BE CREATED]` | openworm/sibernetic — label `dd004` |
| `scripts/validate_cell_coverage.py` | `[TO BE CREATED]` | openworm/sibernetic — label `dd004` |
| `scripts/extract_cell_boundaries.py` | `[TO BE CREATED]` | openworm/sibernetic — label `dd004` |

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** `body/cell_ids/` — particles colored by cell type.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `body/cell_ids/` |
| **Color mode** | Particles colored by cell type: muscle=red, intestine=yellow, cuticle=gray, hypodermis=cyan, gonad=magenta, seam cells=orange |
| **Data source** | OME-Zarr: `body/cell_ids/`, shape (n_particles,) — integer ID mapping each particle to its WBbt cell |
| **What you should SEE** | The worm body with distinct cell boundaries visible as color transitions. Intestinal cells should form a tube along the body axis. Muscle quadrants (MDR, MVR, MVL, MDL) should be visible as four colored bands. Cuticle should form the outermost shell. Clicking a particle shows its WBbt cell ID and cell-type-specific mechanical properties. |
| **Comparison view** | Side-by-side: bulk tissue (all elastic=green, [DD003](DD003_Body_Physics_Architecture.md) default) vs. cell-tagged (distinct colors per cell type) |

---

## Technical Approach

### Tag Every SPH Particle with a Cell ID from the WBbt Ontology

Use the [Witvliet et al. 2021](https://doi.org/10.1038/s41586-021-03778-8) full-body EM reconstructions (8 animals, L1 through adult) to define 3D cell boundaries at multiple developmental stages. Assign each SPH particle a cell ID (WBbt identifier, e.g., `WBbt:0005189` for intestinal cell int1).

**Data structure:**
```c
typedef struct {
    float pos[3];        // Position (x, y, z)
    float vel[3];        // Velocity
    float density;       // Local density
    int particle_type;   // LIQUID, ELASTIC, BOUNDARY
    int cell_id;         // NEW: WBbt cell identifier
} SPH_Particle;
```

### Cell-Type-Specific Mechanical Properties

| Cell Type | WBbt Count | Elasticity Multiplier | Adhesion Strength | Contractile? | Notes |
|-----------|------------|----------------------|------------------|--------------|-------|
| **Body wall muscle** | 95 | 1.5x baseline | High | Yes (HH-driven) | Current default |
| **Intestinal** | 20 | 0.8x (compliant) | Medium | No (peristaltic waves) | Phase 3 target |
| **Hyp7 syncytium** | 1 (covers body) | 0.5x (soft) | Very high | No | Largest cell |
| **Cuticle (basal)** | -- | 5x (stiff) | N/A (acellular) | No | Protective shell |
| **Cuticle (medial)** | -- | 3x | N/A | No | Layered structure |
| **Cuticle (cortical)** | -- | 10x (rigid) | N/A | No | Outermost |
| **Gonad sheath** | 2 | 1.0x | Medium | Yes (cAMP-driven) | Oocyte transport |
| **Pharyngeal muscle** | 20 | 2x | High | Yes (pumping) | See [DD007](DD007_Pharyngeal_System_Architecture.md) |
| **Seam cells** | 10 | 1.2x | Medium | No | Lateral epidermis |

**Elasticity coefficient per particle:**
```
k_particle = k_baseline * cell_type_elasticity_multiplier
```

**Adhesion between adjacent cells:**
```
F_adhesion = adhesion_strength * overlap_area
```

Where `adhesion_strength` depends on both source and target cell types (e.g., muscle-muscle > muscle-intestine).

### Spatial Initialization (Cell Boundaries)

**Data sources:**

1. **[Witvliet et al. 2021](https://doi.org/10.1038/s41586-021-03778-8):** 3D cell volumes at L1, L4, adult (choose adult hermaphrodite as reference)
2. **WormAtlas Slidable Worm:** Consecutive TEM sections with hand-annotated cell boundaries
3. **[Long et al. 2009](https://doi.org/10.1038/nmeth.1366):** 3D nuclear positions for L1 (357 nuclei)

**Initialization algorithm:**

1. Load cell boundary meshes from Witvliet EM data (3D surface reconstruction)
2. For each cell, fill its 3D volume with SPH particles at spacing = smoothing radius h
3. Tag particles with the cell's WBbt ID
4. Assign cell-type-specific mechanical properties from the table above

**File format:**
```
particle_id,x,y,z,type,cell_id,elasticity,adhesion
0,10.2,5.3,100.1,ELASTIC,WBbt:0005189,0.8,0.5
1,10.5,5.3,100.1,ELASTIC,WBbt:0005189,0.8,0.5
...
```

---

## Alternatives Considered

### 1. Keep Bulk Tissue Representation (No Cell Identity)

**Rejected:** Cannot model cell-type-specific mechanics (intestinal peristalsis, cuticle layers, syncytium compliance). Limits biological realism.

### 2. Finite Element Mesh with Explicit Cell Boundaries

**Rejected:** FEM mesh generation is harder than SPH particle tagging. SPH is already implemented. Tagging is a data structure change, not an algorithmic change.

### 3. Coarse-Grain: Group Cells into Tissue Types Only

**Description:** Tag particles as "muscle," "intestine," "hypodermis" without individual cell identity.

**Rejected:** The data exist for single-cell resolution (959 cells). Why reduce? Individual cell identity enables:

- Per-cell state tracking (e.g., intestinal cell 1 vs. cell 20 calcium)
- Cell division / death during development
- Fine-grained validation

---

## Quality Criteria

1. **All 959 Somatic Cells Represented:** Every cell in the WBbt cell list must map to at least one SPH particle.

2. **Spatial Accuracy:** Cell boundaries must match EM data within ±2 µm (SPH smoothing radius is ~3 µm).

3. **Mechanical Realism:** Cell-type-specific elasticity must be justified by literature (e.g., cuticle is stiffer than intestine) or default to baseline.

4. **Validation:** Intestinal peristalsis (Phase 3), hypodermal compliance during body bending, cuticle rigidity should be qualitatively correct.

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **Neural cell identity:** Neurons are covered by [DD001](DD001_Neural_Circuit_Architecture.md) and [DD005](DD005_Cell_Type_Differentiation_Strategy.md). This DD covers non-neural somatic cells only (muscle, intestine, hypodermis, cuticle, gonad, seam cells, pharyngeal muscle).

2. **Developmental stage transitions:** Cell boundaries change during development (L1 through adult). This DD uses adult hermaphrodite as the reference stage. Multi-stage support is future work.

3. **Cell division and death:** Programmed cell death (131 cells die during development) and cell division are not modeled. Fixed adult cell count (959 somatic cells).

4. **Sub-cellular structure:** Organelles, cytoskeletal networks, and intracellular compartments are not represented. Each cell is a homogeneous collection of SPH particles.

5. **Cadherin-specific adhesion dynamics:** Adhesion is parameterized as a scalar strength per cell-type pair. Molecular-level cadherin binding/unbinding kinetics are out of scope.

---

## Context & Background

Current Sibernetic represents the worm body as **bulk elastic and liquid particles** without cell boundaries. All elastic particles have identical mechanical properties (stiffness, adhesion). This is sufficient for basic locomotion but cannot capture:

- Intestinal peristalsis (requires distinct intestinal cell mechanics)
- Cuticle layering (basal, medial, cortical zones)
- Hypodermal syncytium (hyp7) covering most of the body
- Gonad sheath contraction for oocyte transport
- Cell-cell adhesion specificity (cadherin-mediated)

---

## References

1. **Witvliet D et al. (2021).** "Connectomes across development." *Nature* 596:257-261. 3D EM reconstructions.
2. **Long F et al. (2009).** "A 3D digital atlas of *C. elegans*." *Nature Methods* 6:667-672.
3. **WormAtlas.** wormatlas.org. Slidable Worm, cell lists, anatomy handbooks.

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Cell boundary meshes | OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) / [Witvliet 2021](https://doi.org/10.1038/s41586-021-03778-8) EM | 3D surface reconstruction per cell | OBJ or STL mesh files | µm |
| WBbt cell ontology IDs | OWMeta ([DD008](DD008_Data_Integration_Pipeline.md)) / WormBase | Cell name → WBbt ID mapping | CSV or OWMeta query | identifiers |
| Baseline SPH particle layout | [DD003](DD003_Body_Physics_Architecture.md) | Current particle initialization | Binary particle file | µm (positions) |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Tagged particle file | [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic initialization) | Per-particle: position, type, cell_id, elasticity, adhesion | Extended binary or CSV (see struct below) | mixed |
| Cell-to-particle mapping | [DD009](DD009_Intestinal_Oscillator_Model.md) (intestinal oscillator) | Lookup: cell_id → list of particle indices | JSON or Python dict | indices |
| Cell-to-particle mapping | [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx) | Lookup: cell_id → list of particle indices | JSON or Python dict | indices |
| Cell identity labels (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-particle cell_id for cell-based coloring/selection | OME-Zarr: `body/cell_ids/`, shape (n_particles,) | integer ID |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository** | `openworm/sibernetic` (particle initialization is part of Sibernetic) |
| **Docker stage** | `body` (same as [DD003](DD003_Body_Physics_Architecture.md)) |
| **`versions.lock` key** | `sibernetic` |
| **Build dependencies** | Same as [DD003](DD003_Body_Physics_Architecture.md) + cell boundary mesh data from [Witvliet 2021](https://doi.org/10.1038/s41586-021-03778-8) |
| **Additional data** | Cell boundary meshes must be included in the Docker image (or downloaded at build time from a pinned release) |

### Configuration

```yaml
body:
  cell_identity: false               # false = bulk tissue (backward compatible)
                                     # true = per-particle cell IDs ([DD004](DD004_Mechanical_Cell_Identity.md))
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `body.cell_identity` | `false` | `true`/`false` | Enable per-particle cell IDs from WBbt ontology |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test: backward compatibility (must pass before submission)
docker compose run quick-test  # with cell_identity: false
# Checks: produces identical output to unmodified Sibernetic

# Per-PR quick test: tagged simulation (must pass before submission)
# (set body.cell_identity: true in openworm.yml)
docker compose run quick-test
# Checks: simulation completes without crash
# Checks: all particle cell_ids are valid WBbt identifiers
# Checks: locomotion still occurs (body still moves)

# Full validation (must pass before merge to main)
docker compose run validate
# Checks:
#   - Tier 3 kinematic metrics within ±15% with cell_identity enabled
#   - All 959 somatic cells mapped to at least one particle
```

**Per-PR checklist:**

- [ ] `quick-test` passes with `cell_identity: false` (backward compat)
- [ ] `quick-test` passes with `cell_identity: true` (tagged sim)
- [ ] `validate` passes (Tier 3 kinematics with cell identity)
- [ ] All 959 somatic cells mapped to at least one particle
- [ ] Particle file version header present (first 4 bytes = format version)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `body/cell_ids/` (n_particles,) | Cell identity overlay | Cell type → color: muscle=red, intestine=yellow, cuticle=gray, hypodermis=cyan, gonad=magenta |
| `body/positions/` (n_timesteps, n_particles, 3) | Body particles (from [DD003](DD003_Body_Physics_Architecture.md)) | Combined with cell_ids for cell-aware particle rendering |

### Breaking Change: Particle Data Structure

Adding `cell_id` to the SPH particle struct is a **breaking change** to the Sibernetic binary format. Migration plan:

```c
// Old struct ([DD003](DD003_Body_Physics_Architecture.md) current)
typedef struct {
    float pos[3];
    float vel[3];
    float density;
    int particle_type;     // LIQUID, ELASTIC, BOUNDARY
} SPH_Particle;            // 32 bytes

// New struct ([DD004](DD004_Mechanical_Cell_Identity.md))
typedef struct {
    float pos[3];
    float vel[3];
    float density;
    int particle_type;
    int cell_id;           // NEW: WBbt cell identifier (0 = untagged)
    float elasticity_mult; // NEW: cell-type-specific multiplier (1.0 = default)
    float adhesion;        // NEW: cell-type-specific adhesion strength
} SPH_Particle_v2;        // 44 bytes
```

**Backward compatibility:** When `body.cell_identity: false` in `openworm.yml`:

- Use the old struct (32 bytes)
- Sibernetic reads old-format particle files
- All existing tools continue to work

When `body.cell_identity: true`:

- Use new struct (44 bytes)
- Particle file includes a **version header** (first 4 bytes = format version number)
- All downstream tools must check the version header before reading

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| SPH particle struct | [DD003](DD003_Body_Physics_Architecture.md) | If [DD003](DD003_Body_Physics_Architecture.md) changes the base struct, [DD004](DD004_Mechanical_Cell_Identity.md) extension must match |
| EM cell boundary data | [DD008](DD008_Data_Integration_Pipeline.md)/OWMeta | If cell boundary meshes are updated (new EM data), particle tagging must be regenerated |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Intestinal oscillator | [DD009](DD009_Intestinal_Oscillator_Model.md) | [DD009](DD009_Intestinal_Oscillator_Model.md) drives intestinal-tagged particles; if cell_id assignment changes, wrong particles contract |
| Pharynx mechanics | [DD007](DD007_Pharyngeal_System_Architecture.md) (Option B) | Pharyngeal-tagged particles need correct cell_ids for pumping |
| Cuticle mechanics | [DD003](DD003_Body_Physics_Architecture.md) (future) | Cuticle stiffness multiplier affects body bending — changes affect locomotion |

---

- **Approved by:** Pending (Phase 4)
- **Implementation Status:** Proposed
- **Next Actions:**

1. Extract cell boundaries from Witvliet EM data
2. Implement particle tagging in Sibernetic data structures
3. Assign cell-type-specific mechanical properties
4. Validate with intestinal model ([DD009](DD009_Intestinal_Oscillator_Model.md))
