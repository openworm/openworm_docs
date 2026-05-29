# DD001: Body Physics Engine (Sibernetic) Architecture

- **Status:** Accepted
- **Author:** Andrey Palyanov, Sergey Khayrulin, OpenWorm Core Team
- **Date:** 2026-05-27
- **Supersedes:** None
- **Related:** DD002 (Neural Circuit), DD003 (Muscle Model), DD004 (Mechanical Cell Identity)

---

## TL;DR

[PCISPH](https://doi.org/10.1145/1531326.1531346) [SPH](https://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics) framework (Sibernetic) simulating the worm as ~100K particles — liquid (pseudocoelom), elastic (body wall), boundary (environment). Muscle forces from DD003 calcium drive body deformation and locomotion. Success: kinematic validation within ±15%, density deviation <1%.

**Architecturally differentiable.** The native Metal substrate (`src/metal_diff/`) implements every forward kernel with a paired analytic backward kernel, validated against finite-difference. End-to-end reverse-mode differentiation through multi-step XPBD integration produces gradients on initial conditions and all physical parameters (rest density, spring stiffness, viscosity, density-constraint compliance, floor restitution, membrane mechanics). This is a structural property of the substrate — not an optional layer — and is the design requirement that the in-progress CUDA port inherits.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **Layer** | Core Architecture — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-0-existing-foundation-accepted-working) |
| **What does this produce?** | Particle position time series (~100K SPH particles), [WCON](https://github.com/openworm/tracker-commons) trajectory files, rendered body frames, **gradients on physical parameters via reverse-mode AD** |
| **Success metric** | DD010 Tier 3: kinematic metrics within ±15%; density deviation <1% for liquid particles; **every gradient kernel within ±5% rel-err of finite-difference** |
| **Differentiability** | Native Metal substrate (`src/metal_diff/`) is end-to-end differentiable. Multi-step `xpbd_full_bwd` produces gradients on `(x_init, v_init, ρ_rest, spring_K, viscosity, α_density, floor_y, restitution)`. See [Differentiability](#differentiability) below. |
| **Validation methodology** | Every physics change in Sibernetic should follow the 8-phase **predict → reference → inspect → refine → implement → SGD-tune → render → compare** workflow. [Mind-of-a-Worm](../contributing/ai-contributors.md) — when available — surfaces a checklist on PRs against the [Validation Methodology](#validation-methodology) section; human reviewers remain the canonical approvers. |
| **Repository** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) — issues labeled `dd001` |
| **Config toggle** | `body.enabled: true` / `body.backend: opencl` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test` (no NaN/segfault, *.wcon exists), `docker compose run validate` (Tier 3) |
| **Visualize** | DD012 `body/positions/` layer — SPH particles colored by type (liquid=blue, elastic=green, boundary=gray) |
| **CI gate** | Tier 3 kinematic validation + physical stability (no particle escape) blocks merge |
---

## Implementation Status & Roadmap

DD001 is the architectural specification. Implementation work is tracked outside the spec:

- **Active issues:** filter by [`label:dd001`](https://github.com/openworm/sibernetic/labels/dd001) on the [`openworm/sibernetic`](https://github.com/openworm/sibernetic) repo
- **Release milestones:** see [openworm/sibernetic milestones](https://github.com/openworm/sibernetic/milestones) — milestone names carry the [project Phase](DD_PHASE_ROADMAP.md) they serve (e.g., `Phase 0 — Stabilization`, `Phase A1 — Validation Infrastructure`), so the sibernetic release schedule lines up directly with the larger OpenWorm phase plan

Build & test commands, parameter values, validation criteria, and the substrate architecture all live in this document. *What* gets built, *which phase it serves*, and *who's working on it* live in GitHub.

---

## Goal & Success Criteria

| Criterion | Target | DD010 Tier |
|-----------|--------|------------|
| **Primary:** Kinematic metrics | Within ±15% of Schafer lab baseline | Tier 3 (blocking) |
| **Secondary:** Physical stability | No particle escape, no NaN, no divergence over 10 s simulation | Tier 3 (blocking) |
| **Tertiary:** Density deviation | <1% for liquid particles after PCISPH convergence | Tier 3 (blocking) |

**Before:** No fluid-structure interaction — rigid body or mass-spring models that cannot capture pseudocoelomic pressure or hydrostatic skeleton mechanics.

**After:** ~100K SPH particles (liquid + elastic + boundary) with PCISPH pressure solver, enabling coupled fluid-solid locomotion driven by muscle forces from DD003.

---

## Deliverables

| Artifact | Path (relative to `openworm/sibernetic`) | Format | Example |
|----------|------------------------------------------|--------|---------|
| Particle position time series | `output/` (per-run) | Binary state dump or WCON trajectory | `output.dat`, `output.wcon` |
| WCON trajectory files | `output/*.wcon` | WCON JSON | Worm centroid + posture over time |
| Rendered frames / video | `output/frames/` | PNG (per-frame) | `frame_00001.png` |
| Sibernetic binary (C++/OpenCL) | `build/Sibernetic` | Compiled executable | `./Sibernetic -config ...` |
| Native Metal substrate | `src/metal_diff/` | C++/Objective-C++/Metal shaders | `src/metal_diff/sib_metal`, `src/metal_diff/shaders.metal` |
| Native CUDA substrate | `src/cuda/` | C++/CUDA | `src/cuda/sib_cuda` (PR #229, in review) |
| Particle positions (viewer) | [OME-Zarr](https://ngff.openmicroscopy.org): `body/positions/`, shape (n_timesteps, n_particles, 3) | OME-Zarr | Per-particle (x, y, z) over all output timesteps |
| Particle types (viewer) | OME-Zarr: `body/types/`, shape (n_particles,) | OME-Zarr | Enum: liquid/elastic/boundary |
| Surface mesh (viewer) | OME-Zarr: `geometry/body_surface/` (per-frame OBJ or vertices+faces arrays) | OME-Zarr | Reconstructed smooth body surface per timestep |
| Stability checker | `scripts/check_stability.py` | Python script | Verify no NaN, no particle escape, no divergence `[TO BE CREATED]` |
| Incompressibility validator | `scripts/validate_incompressibility.py` | Python script | Verify density deviation <1% `[TO BE CREATED]` |
| Backend parity test suite | `scripts/backend_parity_test.py` | Python script | Cross-backend kinematic comparison `[TO BE CREATED]` |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | [`openworm/sibernetic`](https://github.com/openworm/sibernetic) |
| **Issue label** | `dd001` |
| **Milestone** | Body Physics Engine |
| **Branch convention** | `dd001/description` (e.g., `dd001/pcisph-stability-fix`) |
| **Example PR title** | `DD001: Fix density deviation in PCISPH pressure solver` |

---

## How to Build & Test

Build and run instructions live with the code, in the [**Sibernetic README**](https://github.com/openworm/sibernetic/blob/master/README.md). That's the canonical source — it tracks the actual build system as it evolves (Docker stages, CMake flags, supported platforms, GPU SDK setup, demo configurations) and is updated more frequently than this design document.

What this design document *does* specify is the **acceptance criteria** for whether a build is correct (below), and the **validation workflow** any contributor must follow when changing the physics (see [Validation Methodology](#validation-methodology)).

### Acceptance Criteria (Green-Light Definitions)

A working build must satisfy, on at least one of the [Compute Backends](#compute-backends):

| Gate | What it proves | How it's run |
|------|----------------|--------------|
| **quick-test** | Simulation completes without NaN, segfault, SIGKILL; `output/*.wcon` exists | `docker compose run quick-test` (or the equivalent native path documented in the Sibernetic README) |
| **validate** | Density deviation < 1% for liquid particles; kinematic metrics within ±15% of baseline; no particle escape | `docker compose run validate` |
| **parity** (native substrates) | Per-demo kinematic match against OpenCL reference within ±5% — see [Cross-Backend Parity Requirements](#cross-backend-parity-requirements) | `python3 tests/test_demo*_backend_parity.py` |
| **differentiability** (native substrates) | Every paired backward kernel within ±5% relative error of finite-difference | `python3 src/metal_diff/test_*.py` (and equivalent for `src/cuda/`) |

---

## How to Visualize

**DD012 viewer layer:** `body/positions/` — SPH particles colored by type.

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

### Validated Kinematic Outputs ([Palyanov et al. 2018](https://doi.org/10.1098/rstb.2017.0376))

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

**Muscle cell mapping ([Palyanov et al. 2018](https://doi.org/10.1098/rstb.2017.0376)):** The elastic shell is mapped into 4 longitudinal muscle bundles (VR, VL, DR, DL), and each bundle is subdivided into 24 areas representing **individual muscle cells** with geometries based on WormAtlas microphotographs. This gives 95 body-wall muscles (96 independently activable units). Muscle naming follows the DL side convention and is mirrored for DR, VR, and VL quadrants.

Muscle forces from the calcium-force coupling (DD003) are injected by modulating elastic bond stiffness:

```
k_muscle(t) = k_baseline * (1 + activation(t) * muscle_strength_multiplier)
```

Where `activation(t)` comes from the [Ca²⁺]ᵢ time series of each muscle cell. Bonds tagged as muscle bonds (MDR, MVR, MVL, MDL in 4 quadrants) receive this time-varying stiffness. Each of the 96 muscle units can be activated independently, enabling the full range of body postures observed in *C. elegans*.

### Predictive-Corrective Pressure Solver (PCISPH — OpenCL Reference)

Standard SPH suffers from density fluctuations causing artificial pressure waves. PCISPH ([Solenthaler & Pajarola 2009](https://doi.org/10.1145/1531326.1531346)) adds a predictive-corrective iteration:

1. **Predict:** Estimate particle positions at t + dt using current forces
2. **Correct:** Iteratively adjust pressure forces to maintain incompressibility (ρ ≈ ρ₀)
3. **Update:** Advance to the next timestep once density error < threshold

This stabilizes the simulation at the cost of ~3-7 iterations per timestep. PCISPH is the approach used by the OpenCL reference implementation (`sphFluid.cl`) and is the validated kinematic baseline against which all newer substrates are measured.

### Extended Position-Based Dynamics (XPBD — Native Metal / CUDA Substrates)

The native Metal substrate (and the in-progress CUDA substrate) uses [eXtended Position-Based Dynamics (XPBD)](https://matthias-research.github.io/pages/publications/XPBD.pdf) ([Macklin, Müller & Chentanez 2016](https://matthias-research.github.io/pages/publications/XPBD.pdf)) as the constraint-projection framework. XPBD generalizes Position-Based Dynamics by introducing a per-constraint compliance parameter `α`, which is the *inverse stiffness*: small α ⇒ stiff (hard) constraint, large α ⇒ compliant (soft) constraint. Each constraint contributes a Lagrange-multiplier update that, when iterated K times per timestep, drives the simulation toward the constrained manifold.

The Sibernetic native substrate expresses each physical phenomenon as an XPBD constraint and projects them sequentially per timestep:

1. **Predict:** `predict_positions` advances positions using gravity, external forces, prior velocity (one shader pass)
2. **Constrain:** K projection passes, each solving one constraint kind in turn:
    - **Density constraint** (`solve_density_constraint`) — particles within smoothing radius `h` project toward target density `ρ_rest` with compliance `α_density`. This is the XPBD equivalent of PCISPH's iterative pressure correction.
    - **Distance constraints** (`solve_distance_constraints_seq`) — elastic bonds (springs + anchors) project toward rest length.
    - **Floor / box-clamp constraints** (`solve_floor_constraint`, `clamp_to_box`) — boundary collision with restitution.
    - **Membrane constraints** (`membrane_apply`) — plane-projection through Ihmsen 2014 membrane mechanism (M10 kernels).
3. **Update velocities:** `update_velocities` derives new velocities from position deltas (one shader pass)

For phenomena that don't fit cleanly as constraints — viscous pair forces, surface tension, SPH pressure-gradient buoyancy needed for water-on-worm dynamics — additional force kernels (`pair_forces_grid`, `pair_forces_pressure_grid`) are interleaved within the same XPBD loop, contributing impulses that the constraint projection then resolves against.

#### Why XPBD for the Native Substrate

The XPBD choice is what makes the substrate differentiable end-to-end:

1. **Each constraint has a closed-form Jacobian.** Every projection step's gradient `∂x_new / ∂x_old` can be derived analytically. The substrate exploits this: every forward constraint kernel (`solve_density_constraint`, `solve_distance_constraints_seq`, etc.) has a paired backward kernel that walks the Jacobian, FD-validated to ±5% relative error. PCISPH's iterative pressure-force loop produces gradients in principle too, but autodiff through the iteration is memory-expensive and analytic backwards through iterative implicit methods are harder to derive. XPBD's per-constraint structure is the cleanest match for analytic backward-mode AD. See [Differentiability](#differentiability).

2. **Per-step state is bounded and saveable.** Each XPBD constraint kernel reads a fixed set of inputs and writes a fixed set of outputs. The substrate persists per-step state (positions, velocities, density, ∇C, denominator helpers, per-kernel auxiliaries) so `xpbd_full_bwd` can walk K constraint iterations in reverse. The state's bounded shape per kernel makes this practical at the worm-scale particle counts (~100K particles × multiple kernels × tens of timesteps).

3. **Unconditional stability (PBD heritage).** XPBD doesn't have the CFL-like stiffness constraint that PCISPH inherits from explicit pressure-force integration. Stiffer constraints don't require smaller timesteps — they require lower compliance α. This means kinematic parameter tuning via SGD can vary stiffness across orders of magnitude without restabilizing the integration loop.

#### Cross-Approach Parity

PCISPH and XPBD are mathematically distinct, but the validation methodology requires the native (XPBD) substrate to reproduce the OpenCL (PCISPH) reference's *kinematic outputs* — the per-demo trajectory parity gates ensure equivalent behavior at the observable level even though the inner numerical scheme differs. Where pure XPBD with constraint projection alone produced wrong kinematics (e.g., a worm sinking because there was no upward SPH pressure-gradient force from surrounding liquid), the substrate added the missing force kernel (`pair_forces_pressure_grid`, ported from `sphFluid.cl`) rather than abandoning the XPBD framework. The substrate is thus a *hybrid*: XPBD as the constraint-projection backbone with SPH force kernels interleaved where projection alone is insufficient. This hybrid is what reaches forward parity on the five validated demos; see [Cross-Backend Parity Requirements](#cross-backend-parity-requirements).

The choice is also a Position-Based Dynamics revisitation. PBD itself was rejected for Sibernetic's original architecture as too inaccurate (see [Alternatives Considered §4](#4-position-based-dynamics-pbd)). XPBD's per-constraint compliance restores the physical accuracy that vanilla PBD lacked while keeping PBD's stability and differentiability properties — making it a fit for biophysical validation that vanilla PBD never was.

---

## Alternatives Considered

### 1. [Finite Element Method](https://en.wikipedia.org/wiki/Finite_element_method) (FEM)

**Advantages:** Higher accuracy for solid mechanics, well-established in biomechanics.

**Rejected because:**

- Mesh generation for complex morphology is labor-intensive
- Large deformations (bending during crawling) cause mesh distortion
- Fluid-structure coupling in FEM+CFD is computationally expensive
- SPH is meshless, naturally handles topology changes, and couples fluid-solid seamlessly

**When to reconsider:** If future work requires extremely accurate stress/strain fields (e.g., modeling cuticle fracture, cell rupture). Not needed for behavior simulation.

**Update (2026-02):** Zhao et al. (2024) demonstrated that modern Projective Dynamics FEM solvers ([Bouaziz et al. 2014](https://doi.org/10.1145/2601097.2601116)) address the mesh distortion and speed concerns listed above. Their implementation used a tetrahedral mesh of 984 vertices and 3,341 tetrahedrons with 96 muscle actuators and achieved real-time simulation at 30 frames per second — orders of magnitude faster than the current Sibernetic SPH approach (~100K particles). The key insight is that a Projective Dynamics solver uses a local-global optimization that is unconditionally stable under large deformations, eliminating the traditional FEM mesh distortion problem.

However, Zhao et al.'s FEM approach uses simplified surface hydrodynamics (thrust and drag forces on the body surface) rather than solving full fluid dynamics. This is a valid approximation at the low Reynolds number of *C. elegans* locomotion (Re ~ 0.01) but sacrifices the internal pseudocoelomic fluid pressure dynamics that Sibernetic's SPH naturally captures.

**OpenWorm's position:** Sibernetic SPH remains the biophysically richer model and the default backend. A Projective Dynamics FEM backend should be added as a **fast alternative** for rapid iteration, CI testing, and parameter sweeps — similar in philosophy to DD013's learned surrogate but using first-principles physics rather than machine learning. The BAAIWorm repository (github.com/Jessie940611/BAAIWorm, Apache 2.0) contains a C++/CUDA FEM implementation that could serve as a starting point, though its CUDA/OptiX dependencies would need evaluation for compatibility.

Configuration: `body.backend: "fem-projective"` alongside existing `opencl`, `metal-native`, `cuda-native`.

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

### 5. Boyle-Berri-Cohen 2D Rod-Spring Model

**Advantages:** Extremely fast (~seconds on single CPU), published and validated ([Boyle, Berri & Cohen 2012](https://doi.org/10.3389/fncom.2012.00010)), already implemented in three OpenWorm repos ([CE_locomotion](https://github.com/openworm/CE_locomotion), [Worm2D](https://github.com/openworm/Worm2D), [CelegansNeuromechanicalGaitModulation](https://github.com/openworm/CelegansNeuromechanicalGaitModulation)), ~150 state variables, produces WCON output directly, has c302 integration and proprioception support.

**Not a replacement for Sibernetic because:**

- 2D only — no dorsal-ventral body mechanics, omega turns, or body roll
- No fluid dynamics — uses drag coefficients (Resistive Force Theory), not solved Navier-Stokes
- No internal body volume — cannot support DD004 (cell identity), DD012.2 (mesh deformation), or Phase 3+ organs
- No fluid-structure interaction — DD015 touch mechanotransduction requires 3D particle strain

**Role in OpenWorm:** Fast validation screening tool (`scripts/boyle_berri_cohen_trajectory.py` in c302 repo). Takes c302 muscle calcium output, runs the 2D body model, produces WCON in seconds. Enables rapid iteration on neural circuit parameters and CI quick-test gates. Also useful for generating DD013 surrogate training data. Sibernetic SPH remains the mission-critical body physics engine.

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

5. **GPU Backend Compatibility:** Changes to core SPH algorithms must work across OpenCL (original C++ reference), Native Metal (Apple Silicon), and Native CUDA (NVIDIA). Test on at least two backends.

6. **Cross-Backend Parity:** Core SPH algorithms must produce kinematic outputs within ±5% across all stable backends on the same configuration. The parity test suite (see [Backend Stabilization Roadmap](#backend-stabilization-roadmap)) must pass before any backend is marked Production.

7. **Paired Backward Per Forward (Native Substrates):** Every new forward kernel added to the native Metal or native CUDA substrate MUST ship with a paired analytic backward kernel, validated against finite-difference to within ±5% relative error. This is the architectural contract of the substrate; see [Differentiability](#differentiability). New kernels without a paired backward break the end-to-end differentiability guarantee and must not land.

8. **Validation Methodology Followed:** Every physics change should follow the 8-phase predict → reference → inspect → refine → implement → SGD-tune → render → compare workflow documented in [Validation Methodology](#validation-methodology). PRs that ship a Metal/CUDA implementation are strongly encouraged to include (a) a benchmark config, (b) an OpenCL reference trajectory, (c) a Metal/CUDA trajectory dump, (d) a side-by-side comparison movie, and (e) visual + quantitative parity evidence — these dramatically reduce review time. SGD-based parameter tuning with a saved convergence history is preferred over hand-swept parameters. Human reviewers exercise judgment on which items are necessary for a given PR.

---

## Validation Methodology

**Every physics change in Sibernetic — new kernel, parameter retuning, optimization PR that perturbs numerical output, backend port — should follow the 8-phase workflow below.** The 10-item checklist at the end of this section is the recommended self-review for contributors and the reviewer's reference. [Mind-of-a-Worm](../contributing/ai-contributors.md) — when the bot is in service — surfaces the checklist on the PR as a courtesy; it does not block merges on its own. Human reviewers remain the canonical approvers and use the checklist to guide their review.

The methodology emerged from the native-Metal port (consolidated on the `ow-native-gpu-0.1.0` branch) and is now baked into the repo's tooling. It is the substrate-correctness story: hand-derived backward kernels per [Differentiability](#differentiability) prove the *math* is right; this workflow proves the *physics* is right.

### Why This Is Horizontal

Earlier OpenCL-only Sibernetic relied on "build the kernel, eyeball the demo, ship it." That worked when there was one reference implementation. With three substrates now (OpenCL gold-standard reference, native Metal, native CUDA in scaffolding) and a differentiable pipeline that can be SGD-tuned, the cost of an incorrect kernel landing is now multi-platform divergence that's expensive to retroactively diagnose. The 8-phase workflow front-loads the cost of being right: predict before measuring, measure before implementing, tune via gradient descent not manual sweeps, prove parity visually frame-by-frame.

This applies horizontally to every PR. There is no "small physics change" exemption — even a parameter default tweak goes through the workflow because the trajectory is what matters, not the change-set size.

### The 8-Phase Workflow

#### Phase 1 — Predict Correct Behavior (Before Running Anything)

Read the benchmark configuration file (typically under `configuration/<demo>` or `configuration/test/<demo>`). Extract the physics setup: simulation box bounds, particle positions and types, velocities, spring bond topology (rest length, connection type), membranes if present, boundary anchor locations.

For analytically tractable scenarios (single elastic + anchor, simple oscillators, cube under gravity), calculate expected equilibrium positions, oscillation periods, settling times, displacements *by hand* using the documented formulas (e.g., for elastic-on-anchor: `T = 2π / √(K_eff / m_eff)` where `K_eff = elasticityCoefficient × 0.25 × sim_scale` for non-worm-body elastic pairs — the 0.25 factor is a frequent gotcha).

Write down the prediction with units BEFORE touching OpenCL or Metal. This written prediction becomes the SGD target in Phase 5 and the parity benchmark in Phase 7. The act of writing the prediction first surfaces assumptions and identifies where intuition is wrong.

#### Phase 2 — Run OpenCL Gold-Standard Reference

Run the benchmark config on the OpenCL backend (the validated ±15%-against-Schafer-lab reference). This produces a reference trajectory: per-particle position time series, typically saved as `<demo>_opencl_position.txt` or equivalent.

The OpenCL trajectory is the ground truth for what the Metal (and future CUDA) implementations must match. Commit it to the repo alongside the new physics change so reviewers can re-run parity checks.

#### Phase 3 — Inspect & Refine Prediction Against OpenCL

Parse the OpenCL trajectory and measure observed behavior: actual oscillation period (zero-crossing analysis), amplitude, equilibrium, drift, damping, settling time. Compare against the Phase 1 prediction.

```python
zero_crossings = np.where(np.diff(np.sign(y_centered)) > 0)[0]
observed_period_ms = np.diff(zero_crossings).mean() * frame_dt_ms
```

Surprises are common and informative:
- Period off by 2× → forgot the 0.25 factor on non-worm-body elastic pairs
- Particle drift when stationary → ε guards differ between paths
- Faster fall than expected → buoyancy from SPH pressure gradients
- Unexpected damping → viscous coupling through neighbor particles

Update the written prediction with the measured values. These updated targets are what Phase 5 SGD will optimize against. A correct Metal port must reproduce *what OpenCL actually does*, not what we thought it would do.

#### Phase 4 — Implement on Metal (or CUDA)

Build the native substrate (`./build.sh` in `src/metal_diff/`; analogous for `src/cuda/` once it lands). Implement the new kernel or change. Run the benchmark via `dump_metal_trajectory.py` (or the equivalent CUDA dumper) with the same duration as the OpenCL reference:

```bash
python3 src/metal_diff/dump_metal_trajectory.py \
    --scenario <demo_name> \
    --steps 2500 --chunk 5 \
    --rho-rest 1.0 \
    --spring-k <initial-guess> --anchor-k <initial-guess> \
    --out /tmp/<demo>_metal.txt
```

Sanity-check immediately: trajectory range should match the OpenCL prediction within a few percent. Massive divergence (>50%) means there's a kernel-level physics error to fix before parameter tuning is meaningful. Per [Quality Criteria #7](#quality-criteria), the new kernel must ship with a paired analytic backward and FD test.

#### Phase 5 — SGD-Tune Parameters (Mandatory; Hand-Sweeps Forbidden)

Use the SGD harness (`src/metal_diff/sgd_*.py`; `sgd_one_sprig.py` for single-spring scenarios, `sgd_true.py` for multi-parameter tuning, `sgd_worm.py` for worm-scale, plus demo-specific scripts). Each iteration:

1. Run the simulation with current parameters via `dump_metal_trajectory.py`
2. Measure trajectory features (period, amplitude, final position, kinematic metrics)
3. Compute scalar loss against the Phase 3 measured targets
4. Compute gradients — finite-difference over the CLI for measurement-based losses; analytic backward kernels via `xpbd_full_bwd` for learned parameters
5. Update in log-space for stiffness-like params, linear-space (`--linear-trainable`) for bounded params like `floor_y`

Save the convergence history to `/tmp/sgd_<demo>_history.json` and commit it alongside the parity artifacts. This is the evidence that parameters were not hand-fitted.

If SGD plateaus on a loss that's worse than OpenCL by a wide margin, the problem is missing physics (a kernel), not bad parameter tuning. Port the missing OpenCL kernel — do not ship with caveats. (Example: worm sinking because no buoyancy → port the SPH pressure-force kernel. Example: water exploding → port the PCISPH iterative density correction.)

#### Phase 6 — Render Comparison Movies

Render OpenCL and Metal trajectories as separate panels using the per-scenario renderer (`render_one_sprig.py`, `render_worm.py`, etc. under `src/metal_diff/`), then stack horizontally with ffmpeg:

```bash
python3 src/metal_diff/render_one_sprig.py \
    /tmp/<demo>_opencl_position.txt /tmp/<demo>_opencl_panel.mp4 \
    --title "OpenCL <demo>"
python3 src/metal_diff/render_one_sprig.py \
    /tmp/<demo>_metal.txt /tmp/<demo>_metal_panel.mp4 \
    --title "Native Metal <demo>" --max-frames 250

ffmpeg -y -i /tmp/<demo>_opencl_panel.mp4 -i /tmp/<demo>_metal_panel.mp4 \
    -filter_complex "[0:v]pad=920:900:0:0:color=white[left];[left][1:v]hstack[v]" \
    -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p \
    docs/<demo>_opencl_vs_metal.mp4
```

The renderer auto-detects trajectory format (OpenCL and Metal frame structures differ — OpenCL includes boundary particles only in frame 0; Metal includes them in every frame). Hard-code identical camera bounds and distance in both panels so visual differences reflect physics, not viewport.

#### Phase 7 — Examine Frame-by-Frame for Visual Parity

Extract sample frames at multiple time points from the side-by-side MP4:

```bash
ffmpeg -y -i docs/<demo>_opencl_vs_metal.mp4 \
    -vf "select=between(n\,0\,0)+between(n\,15\,15)+between(n\,100\,100)+between(n\,200\,200)" \
    -vsync vfr /tmp/check_frames/sxs_%d.png
```

Verify at each sample:
- Frame 0 — correct initial positions on both sides
- Mid-trajectory — particle positions, deformation patterns, flow lines match
- Late frames — equilibrium / settling matches
- No render bugs (particle missing, mis-labeled, anchor-spring topology wrong)

Quantitative spot-check: at each sample frame, log the y-coordinate (or equivalent scalar metric — wave amplitude, sheet curvature, worm midline) for both sides. Δ < 5% of the OpenCL scale is the parity threshold.

If visually rendered values don't match the trajectory file's numbers, it's a parser bug (re-check the auto-detect logic in the render script). If trajectory numbers diverge between OpenCL and Metal despite SGD convergence, it's a kernel-physics mismatch — return to Phase 4.

#### Phase 8 — Commit, Document, Publish

One commit per benchmark / per substrate port, containing:

- New / modified kernel code + paired backward + FD test
- The benchmark config file (if new)
- The OpenCL reference trajectory
- The Metal trajectory
- The side-by-side MP4 under `docs/`
- The SGD convergence history (`/tmp/sgd_<demo>_history.json` copied to a tracked location)
- Spot-check frame images (at minimum 3-4 sampled timepoints) showing labeled y-values
- A commit message summarizing: parity at sample frames, tuned parameters, substrate work landed

Cross-link the PR to the relevant `dd001` GitHub label and the demo's parity artifact in `docs/`.

### Worked Example: `one_sprig_test`

**Scenario:** Single elastic particle suspended by a vertical anchor spring; no other forces. Tests anchor-spring kernel correctness in isolation.

| Phase | Activity | Result |
|-------|----------|--------|
| 1. Predict | Config: anchor at (x, 32.565, z), elastic at (x, 16.91, z), rest_length = 15.655. Equilibrium y = 16.91. K = elasticityCoefficient × 0.25 × sim_scale = 307,500 (Metal units). Predicted T ≈ 0.36 ms. | Written prediction filed |
| 2. Reference | Ran OpenCL gold standard, saved `/tmp/one_sprig_opencl_position.txt` | Reference trajectory captured |
| 3. Inspect & refine | Zero-crossing analysis: actual period = 0.725 ms (1379 Hz); half-amplitude = 1.694 units. **Surprise: period is 2× expected — likely the 0.25 factor.** | Targets updated: T=0.725 ms, A=1.694 units |
| 4. Implement Metal | Built Metal substrate, ran `dump_metal_trajectory.py --anchor-k 555`. Initial: y oscillates at 0.36 ms (2× too fast). | Kernel works; needs parameter tuning |
| 5. SGD-tune | `sgd_one_sprig.py` with loss `L = (period_err/0.725)² + 0.25·(amplitude_err/1.694)²`. Init K=300, lr=0.5 log-space. Converged in 7 iterations to K=555. | History saved; T, A match within <1% |
| 6. Render | `render_one_sprig.py` for both panels; ffmpeg hstack to `docs/one_sprig_opencl_vs_metal.mp4` | Side-by-side MP4 produced |
| 7. Frame check | Samples at t=0, 10, 50, 100 ms: y = 18.606 ± 0.001 across both panels; x, z constant; spring topology correct | Visual parity confirmed |
| 8. Commit | Squashed commit containing: kernel cleanup (M11), SGD history, MP4, frame samples, commit-message parity table | PR ready for review |

### Mind-of-a-Worm PR Review Checklist

Human reviewers (with MoaW assistance when available) walk through this checklist when reviewing a PR that touches Sibernetic physics. Items 1, 4, 5, 6 are the most consequential; items 7–10 are reporting hygiene that can be added in-PR.

| # | Check | Pass condition |
|---|-------|---------------|
| 1 | **Written prediction filed** | PR includes a comment, commit-message section, or doc file showing the expected behavior (period, amplitude, equilibrium, settling time, etc.) derived from the config *before* the implementation was written. |
| 2 | **OpenCL reference trajectory committed** | An `<demo>_opencl_position.txt` (or equivalent) artifact exists in the repo or PR diff, with metadata identifying which OpenCL build produced it. |
| 3 | **Metal/CUDA trajectory committed** | An equivalent Metal/CUDA trajectory dump exists, same scenario, same duration. |
| 4 | **Side-by-side comparison MP4 in `docs/`** | `docs/<demo>_opencl_vs_metal.mp4` (or `_vs_cuda`) exists, OpenCL on left, native on right, identical camera. |
| 5 | **Visual parity verified at sample frames** | PR includes at least 3-4 extracted frame images at distinct time points, with labeled y-values (or scalar metric) showing Δ < 5% of OpenCL scale. |
| 6 | **SGD convergence history** | If any parameter was tuned, the PR includes the SGD harness output (loss-per-iteration JSON or similar) demonstrating systematic optimization, not hand-sweeping. |
| 7 | **Paired backward kernel + FD test** | Per [Quality Criteria #7](#quality-criteria), any new forward kernel has a paired analytic backward and a `test_*.py` FD validator passing at <5% rel-err. |
| 8 | **Tuned parameter values documented** | Final values for `rho_rest`, `spring_k`, `visc_pair_coef`, `alpha_dens`, etc., recorded in the commit message and/or the demo's README. |
| 9 | **Substrate work itemized** | The commit message lists what substrate-level changes landed (new kernels, harness extensions, validator tests, render-script updates). |
| 10 | **Phase 1 prediction reconciled against Phase 3 measurement** | If the OpenCL measurement surprised the predictor, the PR documents the gap and the root cause (e.g., "predicted 2× faster because forgot the 0.25 factor"). This is a learning artifact for future contributors. |

As a rule of thumb: items 1, 4, 5, 6 carry the most weight (without them the PR is hand-fitted or unverified); items 7–10 are reporting hygiene that can usually be added in-PR; items 2 and 3 (the OpenCL reference + the candidate trajectory) are what make parity checkable at all, so they're worth pushing for early.

### Common Gotchas (Distilled from the Native-Metal Port)

These are the recurring failure modes seen during the native-Metal port. Reviewers (and MoaW, when available) keep an eye out for them in new PRs:

1. **0.25 factor on non-worm-body elastic springs.** `sphFluid.cl` applies `elasticityCoefficient × 0.25` only to non-worm-body elastic pairs. Forgetting this in Metal makes the oscillation period 2× too short. The Phase 1 prediction must account for it.
2. **`rho_rest = 0` causes NaN.** The density solver divides by `rho_rest`. Always use `1.0` for vacuum scenarios where SPH coupling is irrelevant; use the config's `rho0` explicitly for liquid scenarios.
3. **CLI argv off-by-one cascades.** `dump_metal_trajectory.py` uses positional arguments. Skipping a slot doesn't skip the C++ side's argv index — you must emit placeholder `'0'` strings. When adding a new flag, verify subsequent indices are still aligned.
4. **Hand-sweeping parameters instead of SGD.** If a PR runs 3-5 variants of `dump_metal_trajectory.py` with guessed values, stop and use the harness. SGD converges in 5-10 iterations; hand-sweeping takes 20+ and produces less defensible results.
5. **Physics gap vs parameter gap.** If SGD plateaus on a loss that's clearly worse than OpenCL (worm sinking with no buoyancy, water exploding with no PCISPH), the issue is a missing kernel, not bad tuning. Port the missing OpenCL kernel — do not ship with caveats.
6. **Bounded parameters in log-space blow up.** Linear parameters like `floor_y` can't use log-space updates (`floor_y = 2 × exp(0.5 × 10) = 296`). Use `--linear-trainable` with `--linear-lr 0.05-0.15` and bounded step sizes.
7. **Oscillation around optimum on linear params.** A limit cycle (parameter bouncing between two values every iteration) means the step size is too coarse. The harness auto-halves on sign-flip + L-increase; if you still see it, drop `--linear-lr` further.
8. **Frame-format mismatch between backends.** OpenCL and Metal trajectories differ in frame structure (boundary particles in frame 0 vs every frame). The render script auto-detects by divisibility check. Symptoms of a broken parser: elastic particle visually missing, or labeled with a boundary-particle y-value.
9. **Frame count mismatch desyncs the side-by-side.** Use `--max-frames` on the longer trajectory to cap it to the shorter one, or both panels will end at different simulation times.
10. **Convergence threshold too tight.** Chasing `L < 1e-6` wastes finite-difference evaluations. `L < 1e-4` is tight enough for frame-by-frame visual parity; stop there.

### Validation Tooling Reference

Operational scripts that implement this workflow (all in `src/metal_diff/`):

- **`dump_metal_trajectory.py`** — runs a scenario on the Metal substrate; emits trajectory text file matching the OpenCL output format
- **`render_one_sprig.py`** — renders a single trajectory as an MP4 panel; auto-detects OpenCL vs Metal frame structure
- **`render_worm.py`** — same for worm-scale demos with iso/closeup/cross views, zoom controls, edge rendering, liquid opacity
- **`sgd_one_sprig.py`** — single-parameter SGD harness for anchor-spring scenarios
- **`sgd_true.py`** — multi-parameter SGD harness using analytic gradients via `xpbd_full_bwd` (the canonical reference; TBPTT + gradient clipping)
- **`sgd_worm.py`** — worm-scale parameter tuning
- **`sgd_demo2_membrane.py`** / **`sgd_demo2_permeability.py`** — membrane-specific tuning harnesses
- **`tests/test_demo1_backend_parity.py`** — automated parity gate for the cube-drop demo (runs both backends, compares trajectories, reports per-metric pass/fail)
- **`test_*.py`** in `src/metal_diff/` — 19 finite-difference validators for individual kernel backwards

The matching cuda substrate (when it lands per `src/cuda/README.md`) must include the same workflow tools — `dump_cuda_trajectory.py`, `sgd_*` scripts, and FD validators.

---

## Boundaries (Explicitly Out of Scope)

### This Design Document Does NOT Cover:

1. **Per-cell mechanical identity beyond muscles:** Sibernetic already maps 95 body-wall muscles into 96 independently activable units (24 per quadrant × 4 quadrants: VR, VL, DR, DL), with geometries based on WormAtlas microphotographs ([Palyanov et al. 2018](https://doi.org/10.1098/rstb.2017.0376), Section 2b). However, non-muscle cells (hypodermis, seam cells, neurons) are still represented as bulk elastic/liquid without cell boundaries. See DD004 (Mechanical Cell Identity) for the proposal to extend per-particle cell IDs to all tissue types.

2. **Cuticle fine structure:** The cuticle has three layers (basal, medial, cortical) with distinct mechanical properties. Current model uses homogeneous elastic particles. Phase 4 work.

3. **Environmental complexity beyond liquid/gel:** Sibernetic already supports both liquid and agar gel environments — gel is modeled as elastic matter cubes in a 3D grid ([Palyanov et al. 2018](https://doi.org/10.1098/rstb.2017.0376), Section 2c). Realistic soil mechanics, bacterial food, and geometric obstacles remain out of scope.

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

- `src/owPhysicsFluidSimulator.cpp` — Main SPH loop (OpenCL reference)
- `src/owWorldSimulation.cpp` — Particle initialization, boundary conditions
- `src/sphFluid.cl` — OpenCL kernel for GPU acceleration (the canonical reference; ~64KB)
- `src/metal_diff/` — Native Metal substrate (Apple Silicon): `sib_metal` binary, `shaders.metal`, per-op test suite
- `src/cuda/` — Native CUDA substrate (NVIDIA): scaffolding awaiting PR #229
- `taichi_backend/` — Historical Taichi prototyping path (superseded by the native substrates above)

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

| Backend | Language | Hardware | Speed | Differentiable | Result Quality | Status |
|---------|----------|----------|-------|----------------|---------------|--------|
| OpenCL | C++ | CPU/GPU (Linux, Intel Mac) | Baseline | ❌ forward only | **Gold standard** — validated ±15% | **Production** (but losing driver support) |
| Native Metal | C++/Metal shaders | Apple Silicon GPU | First-pass ~2.7 ms/step on M-series | ✅ **end-to-end** — 19 paired backward kernels, multi-step `xpbd_full_bwd`, FD-validated, 4 demos SGD-tuned | Forward parity in progress; 5+ demos working (cube drop, membrane, worm_alone, worm_swim) | **Experimental → Stable** — consolidated on `ow-native-gpu-0.1.0` branch; PR #230 in flight |
| Native CUDA | C++/CUDA | NVIDIA GPU | Target ~5x OpenCL | 🟡 **structural mandate** — `src/cuda/README.md` requires mirroring Metal's paired-backward architecture | Scaffolding stage | **Scaffolding** — PR #229 (sib_cuda) in review |
| Taichi Metal / CUDA | Python/Taichi | Apple Silicon / NVIDIA | n/a | n/a | n/a | **Superseded** — earlier prototyping path; supplanted by the native ports above |

**Recommendation:** OpenCL remains the only backend producing validated simulation results today. However, OpenCL driver support is shrinking across platforms (Apple removed OpenCL on Apple Silicon; AMD/NVIDIA deprioritizing). The path forward is **native** Metal and CUDA substrates — hand-written GPU kernels that target each platform's first-class API directly, rather than Taichi abstractions that introduced their own divergence from the OpenCL reference. See [Backend Stabilization Roadmap](#backend-stabilization-roadmap) below.

---

## Backend Stabilization Roadmap

### Why OpenCL Must Be Replaced

The OpenCL backend is the **only** backend producing validated simulation results (kinematic metrics within ±15% of Schafer lab baseline). However, OpenCL driver support is shrinking across all major platforms:

- **Apple** dropped OpenCL entirely (deprecated since macOS 10.14, removed from Apple Silicon native support)
- **AMD** is deprioritizing OpenCL in favor of ROCm/HIP
- **NVIDIA** is deprioritizing OpenCL in favor of CUDA
- **Docker** — OpenCL runs CPU-only in Docker (GPU passthrough broken, issue #320)

The core challenge: the only backend producing good simulation results is losing the platforms it runs on. The goal is to achieve OpenCL-equivalent result quality on **native** Metal (Apple Silicon) and **native** CUDA (NVIDIA) substrates **before** OpenCL becomes unusable.

### Why Native Ports, Not Taichi

An earlier prototyping path used [Taichi](https://www.taichi-lang.org/) as an intermediate language to target Metal and CUDA from a single Python codebase. Taichi simplified bring-up but introduced a coordinate-space divergence from the OpenCL reference (elastic forces ~287× too weak — see historical note in [Cross-Backend Parity Requirements](#cross-backend-parity-requirements) below) that proved harder to debug than implementing the GPU kernels natively.

The current strategy is **hand-written kernels per platform**: a Metal shader implementation for Apple Silicon (`src/metal_diff/`), a CUDA kernel implementation for NVIDIA (`src/cuda/`). Each substrate mirrors the OpenCL `sphFluid.cl` reference line-by-line, giving direct algorithmic correspondence without an intermediate abstraction layer. This is the strategy consolidated on the `ow-native-gpu-0.1.0` branch (see PR #230) and is the active direction for the project.

### The Result Quality Gap

The native Metal substrate is the most mature of the modernization paths and reaches forward parity on five demos so far:

- **demo1** (cube drop) — forward parity within ±5%; cross-backend parity test passes 5/5 metrics
- **demo2** (membrane permeability) — membrane mechanism ported (M10 kernels) with FD-validated backward; sheet-scale parameter tuning in progress
- **one_sprig_test** — active muscle contraction extension to anchor-spring kernel; OpenCL reference + Metal port both validated
- **worm_alone_half_resolution** — gravity drop + cylindrical-diameter retention matched to OpenCL
- **worm_swim_half_resolution** — basic swim locomotion validated; SPH pressure force kernel implemented (replaces XPBD-only density solver) for accurate water-on-worm dynamics

**Cross-backend parity status:**

| Backend | Demo1 | Demo2 | one_sprig | worm_alone | worm_swim |
|---------|-------|-------|-----------|------------|-----------|
| OpenCL | reference | reference | reference | reference | reference |
| Native Metal | ✅ ±5% | 🟡 in tuning | ✅ ±5% | ✅ visual parity | 🟡 swim parity in progress |
| Native CUDA | scaffolding | scaffolding | scaffolding | scaffolding | scaffolding |

**Root cause analysis approach:** The OpenCL C++ kernels (`sphFluid.cl`, ~64KB) are the reference implementation. Each native substrate (Metal, CUDA) implements the kernels per-platform with direct OpenCL-line correspondence rather than via an intermediate abstraction. The historical Taichi divergence (elastic forces ~287× too weak from a coordinate-space mismatch — `sim_scale` division applied inconsistently between SPH and elastic force paths) is not present in the native ports because the OpenCL reference's coordinate handling is preserved verbatim.

### Cross-Backend Parity Requirements

Replacement backends must produce kinematic outputs matching OpenCL within ±5% on the same configuration. The parity test suite consists of:

| Test | What It Measures | Pass Criterion |
|------|-----------------|----------------|
| Drop test | Liquid sphere under gravity settles and spreads | Position/velocity metrics within ±5% of OpenCL |
| Elastic deformation | Suspended elastic body sags under gravity | Mean displacement within ±5% of OpenCL |
| Muscle contraction | Single quadrant activation bends body | Curvature within ±5% of OpenCL |
| Full worm crawling | 15ms coupled simulation | WCON trajectory metrics within ±5% of OpenCL |

Each test produces numeric metrics; the parity suite compares against OpenCL baseline values stored in a reference file.

### Backend Graduation Criteria (Exit Conditions)

A backend transitions levels by satisfying the **exit conditions** below. These are *gating* — a substrate stays at its current level until every condition in the next row is met. This mirrors the Kubernetes alpha/beta/GA graduation-criteria pattern, where each maturity stage has a defined contract for what closes it out.

| To exit... | ...into | Exit conditions (all must hold) |
|------------|---------|--------------------------------|
| (initial) | **Experimental** | Compiles on the target platform. Runs an end-to-end simulation. Produces an output artifact (trajectory dump, frame, or whatever the substrate's analog is) without segfault, NaN, or SIGKILL. |
| **Experimental** | **Stable** | Runs 10s of simulated time without divergence. Passes the cross-backend parity test suite (Issue [#235](https://github.com/openworm/sibernetic/issues/235), milestone Phase 0 — Modernization) within ±5% of the OpenCL reference on every working demo. For native substrates: every new forward kernel ships with a paired analytic backward, FD-validated within ±5% (see [Quality Criteria #7](#quality-criteria)). |
| **Stable** | **Production** | All Stable conditions hold. Substrate integrated into the Sibernetic Docker image. CI gate active on the platform (macOS runner for Metal, Linux+NVIDIA runner for CUDA). Performance benchmarked on at least three platforms and the result documented. |

**Current status:**

| Backend | Level | What's holding the next transition |
|---------|-------|------------------------------------|
| OpenCL | **Production** | (Production today. Losing platform support is a separate, non-graduation concern — the goal is to maintain the gold standard until native substrates reach Production.) |
| Native Metal | **Experimental → Stable** | Forward parity on 5+ demos; demo2 sheet-scale and worm_swim parity tuning in progress. Closes when those two parity gates go green (milestone Phase 0 — Modernization). Differentiable end-to-end: 19 paired backward kernels (FD-validated), multi-step `xpbd_full_bwd`, 4 demos already SGD-tuned. See [Differentiability](#differentiability). |
| Native CUDA | **Scaffolding → Experimental** | Awaiting kernel implementation. PR #229 introduces the substrate skeleton; first wave of forward kernels + paired backwards needed to clear Experimental (milestone Phase 0 — Modernization). |
| Taichi Metal / CUDA | **Superseded** | Earlier prototyping path; the native ports above are the replacement direction. Not on a graduation path. |

### Community Contributions to Modernization

Substantial portions of the native-port modernization have been driven by community contributions. Specific contributor acknowledgments are tracked in GitHub issues on `openworm/sibernetic` rather than in this design document — see the `contributor-acknowledgment` label for the current list. The framing of "OpenCL is losing platform support, native Metal + CUDA is the modernization path" emerged directly from community-filed issues; see the `native-gpu` label for the current set.

---

## Differentiability

The native Metal substrate is **architecturally differentiable**. This is not a bolt-on or a future framework: every physical kernel was implemented from day one with a paired analytic backward kernel, and the multi-step integration loop walks K iterations in reverse to produce gradients on initial conditions and physical parameters. The same architecture is the design requirement for the in-progress CUDA port.

### Why Differentiability Is a Substrate Property, Not a Framework Layer

The native substrate derives analytic backwards alongside each forward kernel rather than relying on an autodiff layer over a separate reimplementation. This produces three structural advantages:

1. **No re-implementation drift.** A separate autodiff reimplementation in a host-language framework would have to track the reference's behavior over time as physics changes; an in-substrate backward is the same code path as the forward.
2. **GPU-native gradients.** Backward kernels run on the same Metal command queue as the forwards — no host round-trip, no autodiff graph overhead.
3. **Parameter gradients arrive for free.** Once each forward kernel has an analytic backward, every physical parameter (stiffness, viscosity, rest density, compliance) is differentiable end-to-end without explicit `requires_grad` plumbing.

The CUDA scaffolding at `src/cuda/README.md` makes this explicit: the CUDA substrate must mirror `src/metal_diff/` file-for-file, including paired backward kernels per forward kernel. Differentiability is the *architectural contract* the substrate exposes — not an optional feature flag.

The ML-augmentation framework that consumes this substrate (surrogate models, learned sensory transduction) is the scope of DD013.

### What's Differentiable Today

| Forward kernel | Backward kernel | Status | FD validation |
|----------------|-----------------|--------|---------------|
| `dist_active_static` / `_active_active` (pairwise distance) | `*_backward` | Implemented | <1% rel-err |
| `wpoly6_inplace` (Müller poly6 SPH kernel) | `wpoly6_inplace_backward` | Implemented | <1% rel-err |
| `rowsum_density` (SPH density via threadgroup reduction) | `rowsum_density_backward` | Implemented | <1% rel-err |
| `density_grad_combined` (fused density + ∇W + denom) | `density_constraint_grad_backward` | Implemented | <5% rel-err |
| `solve_density_constraint` (XPBD density correction) | `solve_density_constraint_backward` | Implemented | <5% rel-err |
| `predict_positions` (XPBD predictive step) | `predict_positions_backward` | Implemented | end-to-end via `xpbd_full_bwd` |
| `solve_distance_constraints_seq` (iterative constraint projection) | `*_backward` | Implemented | end-to-end via `xpbd_full_bwd` |
| `pair_forces_grid` (viscosity + surface tension) | `pair_forces_grid_backward` | Implemented | <1% rel-err |
| `apply_ext_accel` (external acceleration) | `apply_ext_accel_backward` | Implemented | end-to-end via `xpbd_full_bwd` |
| `spring_bonds_force` (Hooke spring bonds) | `spring_bonds_force_backward` | Implemented | <1% rel-err |
| `spring_anchor_force` (boundary anchor springs) | `spring_anchor_force_backward` | Implemented | end-to-end via `xpbd_full_bwd` |
| `solve_floor_constraint` (floor collision + restitution) | `solve_floor_constraint_backward` | Implemented | end-to-end via `xpbd_full_bwd` |
| `update_velocities` (verlet velocity update) | `update_velocities_backward` | Implemented | end-to-end via `xpbd_full_bwd` |
| `membrane_clear` / `_accumulate` / `_apply` (Ihmsen 2014 M10) | analytic backward through plane projection | Implemented | <7e-4 rel-err (test_xpbd_full_membrane.py, K ∈ {1,2,3,5}) |

**19 forward kernels, 19 paired backward kernels.** All analytic, hand-derived from the physics. All validated against finite-difference at ε = 1e-3 to within 1–5% relative error (membrane: <7e-4).

### Multi-Step Reverse-Mode AD: `xpbd_full_fwd` / `xpbd_full_bwd`

The substrate exposes an end-to-end forward + backward pair (`ops_xpbd_full.mm`):

- **`run_xpbd_full_fwd(argc, argv)`** — runs K XPBD constraint-projection steps, persisting per-step state (positions, velocities, density, ∇C, denominator helpers, per-kernel auxiliaries) to disk for the backward walk.
- **`run_xpbd_full_bwd(argc, argv)`** — consumes the saved state + a ∂L/∂x_final seed gradient, walks K steps in reverse, and outputs:
  - `∂L/∂x_init`, `∂L/∂v_init` (initial-condition gradients)
  - `∂L/∂ρ_rest`, `∂L/∂spring_K`, `∂L/∂visc_coef`, `∂L/∂α_density`, `∂L/∂floor_y`, `∂L/∂restitution` (scalar parameter gradients)
  - Per-particle parameter gradients where applicable

Per-step gradient clipping (env: `BWD_CLIP_NORM`) keeps long sequences numerically stable; TBPTT support lets training scripts trade memory for trajectory length.

### Gradient-Tuned Demos (SGD Already Applied)

Four of the five working demos have been tuned via gradient descent against OpenCL reference trajectories:

| Demo | Parameters tuned | SGD script | Status |
|------|-----------------|------------|--------|
| **demo1** (cube drop) | `ρ_rest`, `spring_K`, `visc_coef` | `sgd_true.py` (TBPTT + grad clipping) | tuned to OpenCL parity (commit `bf6b333` series) |
| **demo2** (membrane permeability) | membrane elasticity, permeability | `sgd_demo2_membrane.py`, `sgd_demo2_permeability.py` | tuned to OpenCL parity |
| **one_sprig_test** | `spring_K` (single anchor spring) | `sgd_one_sprig.py` | reference oscillator validated |
| **worm_alone_half_resolution** | `spring_K`, `visc` on worm elastic particles | `sgd_worm.py` | tuned to OpenCL trajectory |
| **worm_swim_half_resolution** | (in progress) | — | forward parity demonstrated; SGD pending |

SGD harness lives at `src/metal_diff/sgd_*.py` (8 scripts total, see repo). The pattern is reusable for any new demo or parameter sweep.

### Implications for Downstream Subsystems

Because the substrate exposes a differentiable contract, downstream subsystems that couple to body physics can now ask gradient-based questions of it:

- **Neural ↔ body coupling (DD002, DD003)** — muscle activation timing, calcium-to-force scaling, and per-muscle-unit strength can be jointly optimized against kinematic targets. The muscle force injection path (Sibernetic's modulation of elastic bond stiffness via `k_muscle(t) = k_baseline × (1 + activation(t) × strength_multiplier)`) is differentiable through `xpbd_full_bwd`; activation traces can be backpropagated to neural circuit parameters when those are also expressed in a differentiable form.
- **Validation framework (DD010)** — kinematic-metric mismatches against Schafer-lab baselines (speed, wavelength, frequency, gait) can directly drive parameter updates rather than requiring manual sweeps. Tier 3 validation becomes a loss function the substrate can be optimized against.
- **Simulation stack (DD011)** — the `body.backend: metal-native` configuration should expose a differentiable interface alongside the forward-only interface, so other subsystems can opt into gradient-based parameter fitting via `openworm.yml`.
- **Hybrid ML framework (DD013)** — now narrows to its remaining scope: neural surrogates for SPH (1000× speedup target) and learned sensory transduction. The "differentiable simulation backend" component of DD013 is delivered here, in DD001.

### What's Not (Yet) Differentiable

- **OpenCL backend** — the reference implementation remains forward-only. Validated as the kinematic ground truth; not a differentiation target.
- **CUDA substrate** — scaffolding stage; PR #229 introduces the substrate skeleton. The architectural contract (paired backward per forward) is mandated by the CUDA README but not yet implemented.

### How to Use the Differentiable Interface

```bash
# Forward pass: run K steps, save state
./sib_metal xpbd_full_fwd <args> --save-state /tmp/sim_state.bin

# Backward pass: seed gradient + retrieve parameter gradients
./sib_metal xpbd_full_bwd /tmp/sim_state.bin /tmp/grad_seed.bin \
    --out-grads /tmp/param_grads.bin
```

For a worked example with SGD harness, see `src/metal_diff/sgd_true.py` (the canonical reference implementation that tunes `(ρ_rest, spring_K, visc_coef, α_density, floor_y)` against an OpenCL target trajectory using TBPTT + gradient clipping).

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
| Muscle activation coefficients | DD003 (via `sibernetic_c302.py`) | Per-muscle activation [0, 1] | Written to muscle activation file by coupling script | dimensionless | dt_coupling (0.005 ms from neural side) |
| Particle initialization geometry | DD004 (when cell_identity enabled) | Per-particle position, type, cell_id | Binary or CSV particle file | µm (positions), enum (type) | One-time at sim start |

**Outputs (What This Subsystem Produces)**

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Particle position time series | DD010 (Tier 3 validation) | All particle positions per output frame | Binary state dump or WCON trajectory | µm |
| Rendered frames / video | DD011 (output pipeline) | Visual frames of worm body | PNG or direct framebuffer | pixels |
| Body deformation state | DD007 (pharynx, if Option B) | Anterior attachment point displacement | Shared memory or file | µm |
| Particle positions (for viewer) | **DD012** (visualization) | Per-particle (x, y, z) over all output timesteps | OME-Zarr: `body/positions/`, shape (n_timesteps, n_particles, 3) | µm |
| Particle types (for viewer) | **DD012** (visualization) | Per-particle type (liquid/elastic/boundary) | OME-Zarr: `body/types/`, shape (n_particles,) | enum |
| Surface mesh (for viewer) | **DD012** (visualization) | Reconstructed smooth body surface per timestep | OME-Zarr: `geometry/body_surface/` (per-frame OBJ or vertices+faces arrays) | µm |
| **Parameter gradients** (native substrates only) | DD002 (joint neural↔body fitting), DD003 (muscle parameter fitting), DD010 (gradient-based validation loop) | `∂L/∂(x_init, v_init, ρ_rest, spring_K, viscosity, α_density, floor_y, restitution)` via `xpbd_full_bwd` | Binary float32 buffers per parameter | mixed (per-particle position grads, scalar parameter grads) |

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
  backend: opencl                    # opencl, metal-native, cuda-native
  configuration: "worm_crawl_half_resolution"
  particle_count: 100000
  cell_identity: muscle              # "muscle" = 96 muscle units mapped (default). "all" = Phase 4 (DD004): extend to all tissue types. "false" = bulk elastic only.
  timestep: 0.00002                  # seconds
```

| Key | Default | Valid Range | Description |
|-----|---------|-------------|-------------|
| `body.enabled` | `true` | `true`/`false` | Enable body physics simulation |
| `body.engine` | `sibernetic` | `sibernetic` | Physics engine selection |
| `body.backend` | `opencl` | `opencl`, `metal-native`, `cuda-native` | Compute backend. `metal-native` targets Apple Silicon via hand-written Metal shaders; `cuda-native` targets NVIDIA via hand-written CUDA kernels. The earlier `taichi-metal` / `taichi-cuda` options are superseded by the native ports. |
| `body.configuration` | `"worm_crawl_half_resolution"` | String | Simulation configuration name |
| `body.particle_count` | `100000` | Integer | Total particle count |
| `body.cell_identity` | `muscle` | `false`/`muscle`/`all` | `muscle` = 96 muscle units mapped (existing). `all` = extend to all tissue types (DD004, Phase 4). `false` = bulk elastic only. |
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

### How to Visualize (DD012 Connection)

| OME-Zarr Group | Viewer Layer | Color Mapping |
|----------------|-------------|---------------|
| `body/positions/` (n_timesteps, n_particles, 3) | Body particles | Liquid=blue, elastic=green, boundary=gray |
| `body/types/` (n_particles,) | Particle type overlay | Type enum → color mapping |
| `geometry/body_surface/` (per-frame) | Reconstructed mesh | Smooth surface rendering |

### Backend-Config Translation

Sibernetic internally reads `.ini` configuration files. The `master_openworm.py` orchestrator (DD011) is responsible for translating `openworm.yml` body section to Sibernetic `.ini` format at runtime:

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
| Muscle activation format | DD003 | If activation value range, file format, or muscle count changes, Sibernetic reads wrong data |
| `sibernetic_c302.py` script | DD002/DD003 | This script bridges neural→body; changes to it affect coupling timing |
| Cell boundary data | DD004 | If particle initialization changes (cell-tagged particles), body geometry changes |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Movement validation | DD010 | If particle output format changes, validation toolbox can't read trajectory data |
| Mechanical cell identity | DD004 | If particle struct changes (adding/removing fields), DD004 initialization must match |
| Pharynx attachment | DD007 | If body geometry changes at anterior, pharynx coupling point shifts |

---

- **Approved by:** OpenWorm Steering
- **Implementation Status:** Complete (OpenCL production but losing platform support; native Metal substrate experimental→stable with 5+ demos working and **end-to-end differentiable** — 19 paired backward kernels, 4 demos already SGD-tuned; native CUDA substrate in scaffolding with paired-backward architecture mandated. See [Backend Stabilization Roadmap](#backend-stabilization-roadmap) and [Differentiability](#differentiability))
