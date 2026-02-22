# DD003: Body Physics Engine (Sibernetic) Architecture

- **Status:** Accepted
- **Author:** Andrey Palyanov, Sergey Khayrulin, OpenWorm Core Team
- **Date:** 2026-02-14
- **Supersedes:** None
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD002](DD002_Muscle_Model_Architecture.md) (Muscle Model), [DD004](DD004_Mechanical_Cell_Identity.md) (Mechanical Cell Identity)

---

## TL;DR

PCISPH SPH framework (Sibernetic) simulating the worm as ~100K particles — liquid (pseudocoelom), elastic (body wall), boundary (environment). Muscle forces from [DD002](DD002_Muscle_Model_Architecture.md) calcium drive body deformation and locomotion. Success: kinematic validation within ±15%, density deviation <1%.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **Layer** | Core Architecture — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **What does this produce?** | Particle position time series (~100K SPH particles), WCON trajectory files, rendered body frames |
| **Success metric** | [DD010](DD010_Validation_Framework.md) Tier 3: kinematic metrics within ±15%; density deviation <1% for liquid particles |
| **Repository** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) — issues labeled `dd003` |
| **Config toggle** | `body.enabled: true` / `body.backend: opencl` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` (no NaN/segfault, *.wcon exists), `docker compose run validate` (Tier 3) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `body/positions/` layer — SPH particles colored by type (liquid=blue, elastic=green, boundary=gray) |
| **CI gate** | Tier 3 kinematic validation + physical stability (no particle escape) blocks merge |
---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Kinematic metrics | Within ±15% of Schafer lab baseline | Tier 3 (blocking) |
| **Secondary:** Physical stability | No particle escape, no NaN, no divergence over 10 s simulation | Tier 3 (blocking) |
| **Tertiary:** Density deviation | <1% for liquid particles after PCISPH convergence | Tier 3 (blocking) |

**Before:** No fluid-structure interaction — rigid body or mass-spring models that cannot capture pseudocoelomic pressure or hydrostatic skeleton mechanics.

**After:** ~100K SPH particles (liquid + elastic + boundary) with PCISPH pressure solver, enabling coupled fluid-solid locomotion driven by muscle forces from [DD002](DD002_Muscle_Model_Architecture.md).

---

## Deliverables

| Artifact | Path (relative to `openworm/sibernetic`) | Format | Example |
|----------|------------------------------------------|--------|---------|
| Particle position time series | `output/` (per-run) | Binary state dump or WCON trajectory | `output.dat`, `output.wcon` |
| WCON trajectory files | `output/*.wcon` | WCON JSON | Worm centroid + posture over time |
| Rendered frames / video | `output/frames/` | PNG (per-frame) | `frame_00001.png` |
| Sibernetic binary (C++/OpenCL) | `build/Sibernetic` | Compiled executable | `./Sibernetic -config ...` |
| Taichi backends | `taichi_backend/` | Python/Taichi scripts | `taichi_backend/sph_metal.py` |
| Particle positions (viewer) | OME-Zarr: `body/positions/`, shape (n_timesteps, n_particles, 3) | OME-Zarr | Per-particle (x, y, z) over all output timesteps |
| Particle types (viewer) | OME-Zarr: `body/types/`, shape (n_particles,) | OME-Zarr | Enum: liquid/elastic/boundary |
| Surface mesh (viewer) | OME-Zarr: `geometry/body_surface/` (per-frame OBJ or vertices+faces arrays) | OME-Zarr | Reconstructed smooth body surface per timestep |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) |
| **Issue label** | `dd003` |
| **Milestone** | Body Physics Engine |
| **Branch convention** | `dd003/description` (e.g., `dd003/pcisph-stability-fix`) |
| **Example PR title** | `DD003: Fix density deviation in PCISPH pressure solver` |

---

## How to Build & Test

### Prerequisites

- Docker with `docker compose` ([DD013](DD013_Simulation_Stack_Architecture.md) simulation stack)
- OR: OpenCL SDK (AMD or Intel), CMake, C++ compiler
- Optional: `pip install taichi` for Taichi Metal/CUDA backends

### Step-by-step

```bash
# Step 1: Build Sibernetic (C++/OpenCL)
cd Sibernetic/
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j8

# Step 2: Run standard test configuration
./Sibernetic -config ../configurations/worm_body_test.ini -timestep 0.00002 -duration 1.0

# Step 3: Check for divergence
python ../scripts/check_stability.py output.dat
# [TO BE CREATED] if not present — verify existence in repo

# Step 4: Validate density constraint
python ../scripts/validate_incompressibility.py output.dat --max_deviation 0.01
# [TO BE CREATED] if not present — verify existence in repo

# Step 5: Quick validation via Docker (must pass before PR)
docker compose run quick-test
# Green light: simulation completes without NaN, segfault, or SIGKILL
# Green light: output/*.wcon exists

# Step 6: Full validation via Docker (must pass before merge)
docker compose run validate
# Green light: density deviation < 1% for liquid particles
# Green light: Tier 3 kinematic metrics within ±15% of baseline
# Green light: no particle escape (all positions within bounding box)
```

### Scripts that may not exist yet

| Script | Status | Tracking |
|--------|--------|----------|
| `scripts/check_stability.py` | Verify in repo | openworm/sibernetic — label `dd003` |
| `scripts/validate_incompressibility.py` | Verify in repo | openworm/sibernetic — label `dd003` |

---

## How to Visualize

**[DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer:** `body/positions/` — SPH particles colored by type.

| Viewer Feature | Specification |
|---------------|---------------|
| **Layer** | `body/positions/` |
| **Color mode** | Particles colored by type: liquid=blue, elastic=green, boundary=gray |
| **Type data** | OME-Zarr: `body/types/`, shape (n_particles,) — enum mapping each particle to its type |
| **Surface mesh** | OME-Zarr: `geometry/body_surface/` — reconstructed smooth body surface per timestep |
| **What you should SEE** | A worm-shaped particle cloud deforming over time. Blue liquid particles filling the interior (pseudocoelom), green elastic particles forming the body wall, gray boundary particles defining the environment. Muscle activation should produce visible bending. Surface mesh should show smooth locomotion. |
| **Comparison view** | Side-by-side: particle view (raw SPH) vs. surface mesh (reconstructed body shape) |

---

## Technical Approach

### Smoothed Particle Hydrodynamics (SPH) as the Body Physics Framework

OpenWorm uses **Predictive-Corrective Incompressible SPH (PCISPH)** to simulate the worm as a deformable body embedded in a viscous fluid. SPH represents continuous fields (density, velocity, pressure) as weighted sums over discrete particles, making it naturally suited for coupled fluid-solid systems.

### Three Particle Types

| Type | Represents | Count | Dynamics | Color (Viz) |
|------|-----------|-------|----------|-------------|
| **Liquid** | Pseudocoelom fluid | ~50,000 | Navier-Stokes via SPH | Blue |
| **Elastic** | Body wall structure | ~40,000 | Spring-bonded network | Green |
| **Boundary** | Environmental surfaces | ~10,000 | Fixed or moving constraints | Gray |

**Total particle count:** ~100,000 for an adult hermaphrodite.

### Physical Parameters

| Parameter | Value | Units | Biological Basis |
|-----------|-------|-------|------------------|
| Rest density (ρ₀) | 1000 | kg/m³ | Aqueous tissue |
| Viscosity (µ) | 4e-6 | Pa·s | Low Reynolds number (Re ≤ 0.05) |
| Smoothing radius (h) | 3.34 | Particle units | Determines neighbor interaction range |
| Timestep (dt) | 2.0e-5 | s | Stability for explicit integration |
| Simulation length | ~311 | Particles | Adult body length (~1 mm) |
| Adult worm mass | 3.25e-9 | kg | Mapped to total particle mass |
| Elasticity coefficient | 4 × 1.5e-4 / mass | -- | Spring stiffness for elastic bonds |
| Max muscle contraction force | 2.7 × 10⁻⁹ | N | Experimental range: (1.4–9.6) × 10⁻⁹ N |
| Number of muscle units | 96 | -- | 95 body-wall muscles, 24 per quadrant × 4 |

### Validated Kinematic Outputs (Palyanov et al. 2018)

| Metric | Simulated | Experimental | Source |
|--------|-----------|-------------|--------|
| Crawling velocity | 0.13–0.15 mm/s | 0.1–0.3 mm/s | Table 1 |
| Crawling frequency | 0.36–0.37 Hz | 0.3–0.8 Hz | Table 1 |
| Crawling wavelength | 0.62–0.72 mm | 0.65 mm | Table 1 |
| Swimming velocity | 0.26–0.41 mm/s | 0.29 ± 0.03 mm/s | Table 1 |
| Swimming frequency | 1.76–1.83 Hz | 1.74 ± 0.16 Hz | Table 1 |
| Swimming wavelength | 0.43–0.47 mm | 0.46 mm | Table 1 |
| Freq–wavelength slope | 0.59 | 0.64 (Boyle et al.) | Figure 5 |
| Freq–wavelength intercept | 0.48 | 0.42 (Boyle et al.) | Figure 5 |

**Validated behaviors:** Forward crawling, swimming, omega turns, body shortening, two-frequency undulation (head vs. body).

### SPH Kernel Functions

Following [Müller, Charypar & Gross (2003)](https://doi.org/10.2312/SCA03/154-159):

**Density estimation (Wpoly6):**
```
ρᵢ = Σⱼ mⱼ * Wpoly6(rᵢⱼ, h)
Wpoly6(r, h) = (315 / (64πh⁹)) * (h² - r²)³  if r < h, else 0
```

**Pressure gradient (∇Wspiky):**
```
∇pᵢ = Σⱼ mⱼ * ((pᵢ + pⱼ) / (2ρⱼ)) * ∇Wspiky(rᵢⱼ, h)
∇Wspiky(r, h) = -(45 / (πh⁶)) * (h - r)² * (r / |r|)  if r < h, else 0
```

**Viscous diffusion (∇²Wviscosity):**
```
Fᵢ^viscosity = µ * Σⱼ mⱼ * ((vⱼ - vᵢ) / ρⱼ) * ∇²Wviscosity(rᵢⱼ, h)
∇²Wviscosity(r, h) = (45 / (πh⁶)) * (h - r)  if r < h, else 0
```

### Elastic Bonds (Body Wall Structure)

Elastic particles are connected by spring-like bonds with rest lengths:

```
F_elastic = k * (|rᵢⱼ| - L₀) * (rᵢⱼ / |rᵢⱼ|)
```

- k = elasticity coefficient (see table above)
- L₀ = rest length (initial inter-particle distance)

Bonds are created during initialization based on spatial proximity. Particles within the smoothing radius are bonded if they are both elastic-type.

### Muscle Actuation (Force Injection)

**Muscle cell mapping (Palyanov et al. 2018):** The elastic shell is mapped into 4 longitudinal muscle bundles (VR, VL, DR, DL), and each bundle is subdivided into 24 areas representing **individual muscle cells** with geometries based on WormAtlas microphotographs. This gives 95 body-wall muscles (96 independently activable units). Muscle naming follows the DL side convention and is mirrored for DR, VR, and VL quadrants.

Muscle forces from the calcium-force coupling ([DD002](DD002_Muscle_Model_Architecture.md)) are injected by modulating elastic bond stiffness:

```
k_muscle(t) = k_baseline * (1 + activation(t) * muscle_strength_multiplier)
```

Where `activation(t)` comes from the [Ca²⁺]ᵢ time series of each muscle cell. Bonds tagged as muscle bonds (MDR, MVR, MVL, MDL in 4 quadrants) receive this time-varying stiffness. Each of the 96 muscle units can be activated independently, enabling the full range of body postures observed in *C. elegans*.

### Predictive-Corrective Pressure Solver

Standard SPH suffers from density fluctuations causing artificial pressure waves. PCISPH ([Solenthaler & Pajarola 2009](https://doi.org/10.1145/1531326.1531346)) adds a predictive-corrective iteration:

1. **Predict:** Estimate particle positions at t + dt using current forces
2. **Correct:** Iteratively adjust pressure forces to maintain incompressibility (ρ ≈ ρ₀)
3. **Update:** Advance to the next timestep once density error < threshold

This stabilizes the simulation at the cost of ~3-7 iterations per timestep.

---

## Alternatives Considered

### 1. Finite Element Method (FEM)

**Advantages:** Higher accuracy for solid mechanics, well-established in biomechanics.

**Rejected because:**

- Mesh generation for complex morphology is labor-intensive
- Large deformations (bending during crawling) cause mesh distortion
- Fluid-structure coupling in FEM+CFD is computationally expensive
- SPH is meshless, naturally handles topology changes, and couples fluid-solid seamlessly

**When to reconsider:** If future work requires extremely accurate stress/strain fields (e.g., modeling cuticle fracture, cell rupture). Not needed for behavior simulation.

**Update (2026-02):** Zhao et al. (2024) demonstrated that modern Projective Dynamics FEM solvers ([Bouaziz et al. 2014](https://doi.org/10.1145/2601097.2601116)) address the mesh distortion and speed concerns listed above. Their implementation used a tetrahedral mesh of 984 vertices and 3,341 tetrahedrons with 96 muscle actuators and achieved real-time simulation at 30 frames per second — orders of magnitude faster than the current Sibernetic SPH approach (~100K particles). The key insight is that a Projective Dynamics solver uses a local-global optimization that is unconditionally stable under large deformations, eliminating the traditional FEM mesh distortion problem.

However, Zhao et al.'s FEM approach uses simplified surface hydrodynamics (thrust and drag forces on the body surface) rather than solving full fluid dynamics. This is a valid approximation at the low Reynolds number of *C. elegans* locomotion (Re ~ 0.01) but sacrifices the internal pseudocoelomic fluid pressure dynamics that Sibernetic's SPH naturally captures.

**OpenWorm's position:** Sibernetic SPH remains the biophysically richer model and the default backend. A Projective Dynamics FEM backend should be added as a **fast alternative** for rapid iteration, CI testing, and parameter sweeps — similar in philosophy to [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)'s learned surrogate but using first-principles physics rather than machine learning. The BAAIWorm repository (github.com/Jessie940611/BAAIWorm, Apache 2.0) contains a C++/CUDA FEM implementation that could serve as a starting point, though its CUDA/OptiX dependencies would need evaluation for compatibility.

Configuration: `body.backend: "fem-projective"` alongside existing `opencl`, `taichi-metal`, `taichi-cuda`, `pytorch`.

Reference: [Bouaziz S et al. (2014)](https://doi.org/10.1145/2601097.2601116). "Projective Dynamics: Fusing constraint projections for fast simulation." *ACM Trans Graphics* 33:154.

### 2. Mass-Spring System (Simple Elastic Network)

**Advantages:** Extremely fast, simple to implement.

**Rejected because:**

- No fluid mechanics (pseudocoelom is critical for worm locomotion)
- Difficult to enforce incompressibility
- No pressure dynamics

This was tried in early OpenWorm prototypes and abandoned because crawling requires fluid pressure to antagonize muscle contraction.

### 3. Lattice Boltzmann Method (LBM)

**Advantages:** Good for fluid flow, naturally parallelizes.

**Rejected because:**

- Fixed Cartesian grid poorly represents complex worm morphology
- Deformable solid modeling in LBM is cumbersome
- SPH is more natural for moving, deforming boundaries

### 4. Position-Based Dynamics (PBD)

**Advantages:** Unconditionally stable, used in real-time graphics/games.

**Rejected because:**

- Sacrifices physical accuracy for stability (violates momentum conservation in general)
- Not suited for quantitative biophysical validation
- OpenWorm prioritizes biological accuracy over simulation speed

---

## Quality Criteria

A contribution to Sibernetic MUST:

1. **Preserve Physical Stability:** Simulations must not explode (density < 0, particles escaping to infinity, NaN values). Run at least 10 seconds of simulation time without divergence.

2. **Maintain Incompressibility:** Density deviation from ρ₀ should be < 1% for liquid particles after PCISPH convergence.

3. **Pass Unit Tests:** Sibernetic repository contains unit tests for kernel functions, neighbor search, and pressure solver. All must pass.

4. **Validate Against Known Cases:**
    - Drop test: Sphere of liquid particles under gravity should settle and spread
    - Elastic deformation: A suspended elastic body under gravity should sag
    - Muscle contraction: Activating one muscle quadrant should bend the body

5. **GPU Backend Compatibility:** Changes to core SPH algorithms must work across OpenCL (original C++), Taichi Metal (Apple Silicon), Taichi CUDA (NVIDIA), and PyTorch (CPU reference). Test on at least two backends.

---

## Boundaries (Explicitly Out of Scope)

### This Design Document Does NOT Cover:

1. **Per-cell mechanical identity beyond muscles:** Sibernetic already maps 95 body-wall muscles into 96 independently activable units (24 per quadrant × 4 quadrants: VR, VL, DR, DL), with geometries based on WormAtlas microphotographs (Palyanov et al. 2018, Section 2b). However, non-muscle cells (hypodermis, seam cells, neurons) are still represented as bulk elastic/liquid without cell boundaries. See [DD004](DD004_Mechanical_Cell_Identity.md) (Mechanical Cell Identity) for the proposal to extend per-particle cell IDs to all tissue types.

2. **Cuticle fine structure:** The cuticle has three layers (basal, medial, cortical) with distinct mechanical properties. Current model uses homogeneous elastic particles. Phase 4 work.

3. **Environmental complexity beyond liquid/gel:** Sibernetic already supports both liquid and agar gel environments — gel is modeled as elastic matter cubes in a 3D grid (Palyanov et al. 2018, Section 2c). Realistic soil mechanics, bacterial food, and geometric obstacles remain out of scope.

4. **Thermodynamics:** No temperature, no heat diffusion, no thermal expansion. *C. elegans* is studied at 20°C but temperature effects are not modeled.

5. **Growth and molting:** Body size changes during development. Current model assumes fixed adult size. Phase 6 work.

---

## Context & Background

*C. elegans* is a soft-bodied organism. Locomotion emerges from the interaction between:

- Muscle contractile forces (internal)
- Body wall elasticity (structural)
- Pseudocoelomic fluid pressure (hydrostatic skeleton)
- Environmental resistance (viscous drag, surface contact)

Classical rigid-body physics engines (used in robotics) cannot capture this fluid-structure interaction. Finite element methods (FEM) are accurate but computationally expensive and poorly suited for large deformations and topological changes.

---

## Implementation References

### Repository

```
https://github.com/openworm/Sibernetic
```

**Key files:**

- `src/owPhysicsFluidSimulator.cpp` — Main SPH loop
- `src/owWorldSimulation.cpp` — Particle initialization, boundary conditions
- `kernels/sph_cl.cl` — OpenCL kernel for GPU acceleration
- `taichi_backend/` — Taichi Metal/CUDA implementations

### Configuration Format

Sibernetic reads `.ini` files specifying:

- Particle counts (liquid, elastic, boundary)
- Initial positions (from pre-generated `.obj` 3D mesh or procedural)
- Muscle activation input file
- Simulation duration, timestep, output frequency

Example:
```ini
[simulation]
timestep = 0.00002
duration = 10.0
output_interval = 0.01

[particles]
liquid_count = 50000
elastic_count = 40000
boundary_count = 10000

[physics]
rest_density = 1000.0
viscosity = 4e-6
elasticity = 0.0006
```

### Compute Backends

| Backend | Language | Hardware | Speed | Status |
|---------|----------|----------|-------|--------|
| OpenCL | C++ | CPU/GPU (cross-platform) | Baseline | Stable |
| Taichi Metal | Python/Taichi | Apple Silicon GPU | ~3x faster | Experimental |
| Taichi CUDA | Python/Taichi | NVIDIA GPU | ~5x faster | Experimental |
| PyTorch | Python | CPU | Slow (reference only) | Stable |

**Recommendation:** Use Taichi Metal for Apple Silicon, Taichi CUDA for NVIDIA GPUs. OpenCL for maximum portability.

---

## References

1. **[Müller M, Charypar D, Gross M (2003)](https://doi.org/10.2312/SCA03/154-159).** "Particle-based fluid simulation for interactive applications." *Proc. ACM SIGGRAPH/Eurographics Symp. Computer Animation*, pp. 154-159.
   *SPH kernel functions.*

2. **[Solenthaler B, Pajarola R (2009)](https://doi.org/10.1145/1531326.1531346).** "Predictive-Corrective Incompressible SPH." *ACM Trans. Graphics* 28(3):40.
   *PCISPH pressure solver.*

3. **Boyle JH, Cohen N (2008).** "Caenorhabditis elegans body wall muscles are simple actuators." *Biosystems* 94:170-181.
   *Muscle-to-physics coupling validation.*

4. **[Palyanov A, Khayrulin S, Larson SD (2018)](https://doi.org/10.1098/rstb.2017.0376).** "Three-dimensional simulation of the *Caenorhabditis elegans* body and muscle cells in liquid and gel environments for behavioural analysis." *Phil. Trans. R. Soc. B* 373:20170376.
   *Primary Sibernetic publication. Describes muscle cell mapping (96 units), validated kinematics (Table 1), force–velocity/force–length relationships, omega turns, and agar gel simulation.*

5. **Zhao M et al. (2024).** *Nat Comp Sci* 4:978-990.
   *Demonstrated real-time FEM body simulation of C. elegans at 30 FPS.*

6. **[Bouaziz S et al. (2014)](https://doi.org/10.1145/2601097.2601116).** *ACM Trans Graphics* 33:154.
   *Projective Dynamics FEM solver.*

---

## Integration Contract

### Inputs / Outputs

**Inputs (What This Subsystem Consumes)**

| Input | Source DD | Variable | Format | Units | Timestep |
|-------|----------|----------|--------|-------|----------|
| Muscle activation coefficients | [DD002](DD002_Muscle_Model_Architecture.md) (via `sibernetic_c302.py`) | Per-muscle activation [0, 1] | Written to muscle activation file by coupling script | dimensionless | dt_coupling (0.005 ms from neural side) |
| Particle initialization geometry | [DD004](DD004_Mechanical_Cell_Identity.md) (when cell_identity enabled) | Per-particle position, type, cell_id | Binary or CSV particle file | µm (positions), enum (type) | One-time at sim start |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Particle position time series | [DD010](DD010_Validation_Framework.md) (Tier 3 validation) | All particle positions per output frame | Binary state dump or WCON trajectory | µm |
| Rendered frames / video | [DD013](DD013_Simulation_Stack_Architecture.md) (output pipeline) | Visual frames of worm body | PNG or direct framebuffer | pixels |
| Body deformation state | [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx, if Option B) | Anterior attachment point displacement | Shared memory or file | µm |
| Particle positions (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-particle (x, y, z) over all output timesteps | OME-Zarr: `body/positions/`, shape (n_timesteps, n_particles, 3) | µm |
| Particle types (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-particle type (liquid/elastic/boundary) | OME-Zarr: `body/types/`, shape (n_particles,) | enum |
| Surface mesh (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Reconstructed smooth body surface per timestep | OME-Zarr: `geometry/body_surface/` (per-frame OBJ or vertices+faces arrays) | µm |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository** | `openworm/sibernetic` |
| **Docker stage** | `body` in multi-stage Dockerfile |
| **`versions.lock` key** | `sibernetic` |
| **Build dependencies** | OpenCL SDK (AMD or Intel), CMake, C++ compiler |
| **Backend note** | Taichi backends require `pip install taichi` (not currently in Dockerfile) |

### Configuration

```yaml
body:
  enabled: true
  engine: sibernetic
  backend: opencl                    # opencl, taichi-metal, taichi-cuda, pytorch
  configuration: "worm_crawl_half_resolution"
  particle_count: 100000
  cell_identity: muscle              # "muscle" = 96 muscle units mapped (default). "all" = Phase 4 ([DD004](DD004_Mechanical_Cell_Identity.md)): extend to all tissue types. "false" = bulk elastic only.
  timestep: 0.00002                  # seconds
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `body.enabled` | `true` | `true`/`false` | Enable body physics simulation |
| `body.engine` | `sibernetic` | `sibernetic` | Physics engine selection |
| `body.backend` | `opencl` | `opencl`, `taichi-metal`, `taichi-cuda`, `pytorch` | Compute backend |
| `body.configuration` | `"worm_crawl_half_resolution"` | String | Simulation configuration name |
| `body.particle_count` | `100000` | Integer | Total particle count |
| `body.cell_identity` | `muscle` | `false`/`muscle`/`all` | `muscle` = 96 muscle units mapped (existing). `all` = extend to all tissue types ([DD004](DD004_Mechanical_Cell_Identity.md), Phase 4). `false` = bulk elastic only. |
| `body.timestep` | `0.00002` | Float (seconds) | Simulation timestep |

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
docker compose run quick-test
# Checks: simulation completes without NaN, segfault, or SIGKILL
# Checks: output/*.wcon exists

# Full validation (must pass before merge to main)
docker compose run validate
# Checks:
#   - Density deviation < 1% for liquid particles
#   - Tier 3 kinematic metrics within ±15% of baseline
#   - No particle escape (all positions within bounding box)
```

**Per-PR checklist:**

- [ ] Build succeeds (`cmake .. && make -j8`)
- [ ] `quick-test` passes (no NaN, no segfault, *.wcon exists)
- [ ] `validate` passes (Tier 3 kinematics + density constraint)
- [ ] Tested on at least two backends if core SPH algorithms changed
- [ ] No particle escape (all positions within bounding box)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `body/positions/` (n_timesteps, n_particles, 3) | Body particles | Liquid=blue, elastic=green, boundary=gray |
| `body/types/` (n_particles,) | Particle type overlay | Type enum → color mapping |
| `geometry/body_surface/` (per-frame) | Reconstructed mesh | Smooth surface rendering |

### Backend-Config Translation

Sibernetic internally reads `.ini` configuration files. The `master_openworm.py` orchestrator ([DD013](DD013_Simulation_Stack_Architecture.md)) is responsible for translating `openworm.yml` body section to Sibernetic `.ini` format at runtime:

```python
# master_openworm.py (pseudocode)
def write_sibernetic_config(openworm_config):
    ini = configparser.ConfigParser()
    ini['simulation']['timestep'] = str(openworm_config['body']['timestep'])
    ini['particles']['total'] = str(openworm_config['body']['particle_count'])
    # ... etc
    ini.write(open('sibernetic_config.ini', 'w'))
```

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Muscle activation format | [DD002](DD002_Muscle_Model_Architecture.md) | If activation value range, file format, or muscle count changes, Sibernetic reads wrong data |
| `sibernetic_c302.py` script | [DD001](DD001_Neural_Circuit_Architecture.md)/DD002 | This script bridges neural→body; changes to it affect coupling timing |
| Cell boundary data | [DD004](DD004_Mechanical_Cell_Identity.md) | If particle initialization changes (cell-tagged particles), body geometry changes |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Movement validation | [DD010](DD010_Validation_Framework.md) | If particle output format changes, validation toolbox can't read trajectory data |
| Mechanical cell identity | [DD004](DD004_Mechanical_Cell_Identity.md) | If particle struct changes (adding/removing fields), [DD004](DD004_Mechanical_Cell_Identity.md) initialization must match |
| Pharynx attachment | [DD007](DD007_Pharyngeal_System_Architecture.md) | If body geometry changes at anterior, pharynx coupling point shifts |

---

- **Approved by:** OpenWorm Steering
- **Implementation Status:** Complete (Sibernetic v1.0+)
- **Next Actions:**

1. Extend per-particle cell IDs beyond muscles to all tissue types — hypodermis, seam cells, neurons ([DD004](DD004_Mechanical_Cell_Identity.md), Phase 4). Muscle cell IDs (96 units) are already mapped.
2. Add cell-type-specific mechanical properties for non-muscle tissues
3. Optimize Taichi backends for production use
