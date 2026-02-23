# DD003 Draft GitHub Issues

**Epic:** DD003 — Body Physics Engine (Sibernetic) Architecture

**Generated from:** [DD003: Body Physics Engine Architecture](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 22 issues (ai-workable: 14 / human-expert: 8 | L1: 8, L2: 9, L3: 5)

**Note:** Backend stabilization Issues 40–44 in [DD013_draft_issues](DD013_draft_issues.md) are also labeled `DD003` and are cross-referenced here but not duplicated.

---

## Phase 1: Validation Infrastructure

Target: Scripts and test configurations needed to measure simulation quality and compare backends.

---

### Issue 1: Create `scripts/check_stability.py`

- **Title:** `[DD003] Create check_stability.py — simulation divergence detector`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — How to Build & Test](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#how-to-build-test) (Step 3) and [DD003 Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) (criterion 1)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/check_stability.py` (new)
    - `tests/test_check_stability.py` (new)
- **Test Commands:**
    - `python3 scripts/check_stability.py output.dat`
    - `pytest tests/test_check_stability.py`
- **Acceptance Criteria:**
    - [ ] Reads Sibernetic binary output file (`output.dat`)
    - [ ] Detects NaN values in particle positions or velocities
    - [ ] Detects particles escaping bounding box (configurable box dimensions)
    - [ ] Detects velocity divergence (magnitude exceeding physical threshold)
    - [ ] Verifies simulation ran for at least the expected duration without early termination
    - [ ] Prints PASS/FAIL with diagnostic details (which particles, which timestep, what went wrong)
    - [ ] Returns exit code 0 on pass, non-zero on fail
    - [ ] Unit tests with synthetic data (clean data → PASS, NaN-injected data → FAIL, escaped particle → FAIL)
- **Sponsor Summary Hint:** The basic health check for any SPH simulation — did the physics blow up? NaN values mean the computation diverged (division by zero, impossible forces). Escaped particles mean the simulation lost containment. This script is listed as a DD003 deliverable but was never created.

---

### Issue 2: Create `scripts/validate_incompressibility.py`

- **Title:** `[DD003] Create validate_incompressibility.py — density deviation checker`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — How to Build & Test](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#how-to-build-test) (Step 4) and [DD003 Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) (criterion 2)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/validate_incompressibility.py` (new)
    - `tests/test_validate_incompressibility.py` (new)
- **Test Commands:**
    - `python3 scripts/validate_incompressibility.py output.dat --max_deviation 0.01`
    - `pytest tests/test_validate_incompressibility.py`
- **Acceptance Criteria:**
    - [ ] Reads Sibernetic output and extracts per-particle density values
    - [ ] Filters to liquid-type particles only (elastic and boundary excluded)
    - [ ] Computes density deviation from rest density ρ₀ = 1000 kg/m³
    - [ ] Reports max deviation, mean deviation, and percentage of particles exceeding threshold
    - [ ] `--max_deviation` flag sets the pass/fail threshold (default 0.01 = 1%)
    - [ ] Prints PASS/FAIL with statistics
    - [ ] Returns exit code 0 on pass, non-zero on fail
    - [ ] Unit tests with synthetic density data
- **Sponsor Summary Hint:** PCISPH enforces incompressibility — the virtual fluid shouldn't compress. If density deviates >1% from the rest density (1000 kg/m³), the pressure solver isn't converging properly. This script checks that the core physics invariant holds.

---

### Issue 3: Create standard test configuration files

- **Title:** `[DD003] Create standard .ini test configurations for drop, elastic, muscle, and worm crawl tests`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** physics
- **DD Section to Read:** [DD003 Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) (criterion 4) and [DD003 Backend Stabilization Roadmap — Cross-Backend Parity Requirements](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#cross-backend-parity-requirements)
- **Depends On:** None
- **Files to Modify:**
    - `configurations/test_drop.ini` (new)
    - `configurations/test_elastic_deformation.ini` (new)
    - `configurations/test_muscle_contraction.ini` (new)
    - `configurations/test_worm_crawl.ini` (new)
    - `configurations/README.md` (new — explains each config)
- **Test Commands:**
    - `./build/Sibernetic -config configurations/test_drop.ini -timestep 0.00002 -duration 1.0`
    - `./build/Sibernetic -config configurations/test_elastic_deformation.ini -timestep 0.00002 -duration 3.0`
- **Acceptance Criteria:**
    - [ ] `test_drop.ini`: Sphere of ~5,000 liquid particles under gravity (no elastic, no muscle). Should settle and spread.
    - [ ] `test_elastic_deformation.ini`: Elastic body suspended under gravity (no liquid). Should sag measurably.
    - [ ] `test_muscle_contraction.ini`: Full worm body with single quadrant (e.g., MDR) activated at constant force. Should bend.
    - [ ] `test_worm_crawl.ini`: Standard worm configuration at half resolution (~50K particles), 15ms coupled simulation.
    - [ ] Each config has comments explaining what it tests and expected behavior
    - [ ] `README.md` documents all configs and when to use each
    - [ ] All configs run without crash on the OpenCL backend
- **Sponsor Summary Hint:** Standard test configurations are the physical experiments of our simulation — like a lab protocol. Drop test (does fluid fall?), elastic test (does skin stretch?), muscle test (does activation bend?), crawl test (does the worm move?). Every backend must pass these same tests to be considered valid.

---

### Issue 4: Create OpenCL baseline metrics for parity tests

- **Title:** `[DD003] Generate and save OpenCL baseline metrics for cross-backend parity tests`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Cross-Backend Parity Requirements](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#cross-backend-parity-requirements)
- **Depends On:** Issue 3 (test configs), DD013 Issue 41 (parity test script)
- **Files to Modify:**
    - `tests/baseline/drop_test_opencl.json` (new)
    - `tests/baseline/elastic_deformation_opencl.json` (new)
    - `tests/baseline/muscle_contraction_opencl.json` (new)
    - `tests/baseline/worm_crawl_opencl.json` (new)
    - `tests/baseline/README.md` (new — documents baseline generation)
- **Test Commands:**
    - `python3 scripts/backend_parity_test.py --backend opencl --save-baseline tests/baseline/`
- **Acceptance Criteria:**
    - [ ] Run all 4 test scenarios on OpenCL backend
    - [ ] Save numeric metrics to JSON files (position means, velocity statistics, density stats, curvature)
    - [ ] Each baseline file includes metadata: Sibernetic version, commit hash, OpenCL platform, run date
    - [ ] Metrics are deterministic to ±0.1% across repeated runs on same hardware
    - [ ] README documents how to regenerate baselines and when they should be updated
    - [ ] Baseline files committed to repo (small JSON, not large binary data)
- **Sponsor Summary Hint:** The OpenCL backend is the gold standard — its outputs define "correct." These baseline files capture exactly what OpenCL produces for each test scenario, so we can numerically compare PyTorch and Taichi against them. Like calibrating a lab instrument against a known reference.

---

### Issue 5: Port SPH kernel unit tests to PyTorch backend

- **Title:** `[DD003] Port existing SPH kernel unit tests to run on PyTorch backend`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) (criterion 3, 5) and [DD003 — SPH Kernel Functions](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#sph-kernel-functions)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_pytorch_kernels.py` (new)
- **Test Commands:**
    - `pytest tests/test_pytorch_kernels.py -v`
- **Acceptance Criteria:**
    - [ ] Unit tests for Wpoly6 kernel function (density estimation)
    - [ ] Unit tests for ∇Wspiky kernel function (pressure gradient)
    - [ ] Unit tests for ∇²Wviscosity kernel function (viscous diffusion)
    - [ ] Unit tests for elastic bond force calculation
    - [ ] Unit tests for PCISPH pressure correction iteration
    - [ ] Each test compares PyTorch output against analytical or OpenCL reference values
    - [ ] All tests pass with tolerance ±1e-6 for single-precision floats
    - [ ] Tests can be run without OpenCL installed (pure Python/PyTorch)
- **Sponsor Summary Hint:** The SPH kernel functions are the mathematical heart of the physics engine — they compute how particles interact via density, pressure, and viscosity. Unit tests verify each function produces the correct output for known inputs. Currently these tests only exist for OpenCL. Porting to PyTorch ensures the Python implementation matches the C++ math.

---

### Issue 6: Port SPH kernel unit tests to Taichi backend

- **Title:** `[DD003] Port existing SPH kernel unit tests to run on Taichi backend`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) (criterion 3, 5) and [DD003 — SPH Kernel Functions](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#sph-kernel-functions)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_taichi_kernels.py` (new)
- **Test Commands:**
    - `pytest tests/test_taichi_kernels.py -v`
- **Acceptance Criteria:**
    - [ ] Same kernel unit tests as Issue 5 but targeting Taichi backend
    - [ ] Tests exercise both Metal and CUDA code paths (parameterized by `ti.init(arch=...)`)
    - [ ] Each test compares Taichi output against analytical or OpenCL reference values
    - [ ] All tests pass with tolerance ±1e-6 for single-precision floats
    - [ ] Tests can be run on CPU fallback (`ti.init(arch=ti.cpu)`) for CI without GPU
- **Sponsor Summary Hint:** Same as Issue 5 but for the Taichi backend. Taichi compiles Python to GPU shaders (Metal on Apple Silicon, CUDA on NVIDIA). These unit tests verify the compiled kernels produce the same results as the C++ originals. Especially important given the known coordinate-space bug.

---

## Phase 2: Backend Stabilization

Target: PyTorch and Taichi backends produce results matching OpenCL within ±5%.

**Note:** The core backend stabilization issues are tracked in [DD013_draft_issues.md](DD013_draft_issues.md) as Issues 40–44 (labeled `DD003`). They cover:

- **DD013 Issue 40:** Create stability validation scripts → equivalent to Issues 1–2 above
- **DD013 Issue 41:** Create cross-backend parity test suite
- **DD013 Issue 42:** Fix Taichi elastic coordinate-space bug
- **DD013 Issue 43:** Audit and fix PyTorch/Taichi result quality gap
- **DD013 Issue 44:** Graduate backends to Stable/Production

The issues below supplement that sequence with DD003-specific work.

---

### Issue 7: Document OpenCL kernel architecture (`sphFluid.cl`)

- **Title:** `[DD003] Document OpenCL kernel architecture for algorithmic audit`
- **Labels:** `DD003`, `human-expert`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** opencl, physics, sph
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — The Result Quality Gap](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#the-result-quality-gap) and [DD003 — Implementation References](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#implementation-references)
- **Depends On:** None
- **Files to Modify:**
    - `docs/opencl_kernel_architecture.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Annotated walkthrough of `kernels/sphFluid.cl` (~64KB) — every major function documented
    - [ ] Maps each OpenCL kernel function to its DD003 equation (Wpoly6, ∇Wspiky, ∇²Wviscosity, F_elastic, PCISPH)
    - [ ] Documents coordinate spaces used (world vs. scaled) and where conversions happen
    - [ ] Documents simulation_scale factor and its role in elastic force calculation
    - [ ] Documents the PCISPH iteration loop (predict → correct → converge)
    - [ ] Documents neighbor search data structures
    - [ ] Identifies any undocumented heuristics, magic numbers, or non-standard modifications to PCISPH
    - [ ] Provides a "function call graph" showing the order of kernel invocations per timestep
- **Sponsor Summary Hint:** The OpenCL kernel file is the 64KB brain of the physics engine — the actual GPU code that moves 100,000 particles. Nobody has documented what it does at the code level. Before we can audit why PyTorch/Taichi produce different results (DD013 Issue 43), we need to understand what the reference implementation actually computes. This is like creating an annotated blueprint before renovating a building.

---

### Issue 8: Add PyTorch backend to CI smoke test

- **Title:** `[DD003] Add PyTorch backend smoke test to GitHub Actions CI`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** ci-cd, python
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Stabilization Sequence](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#stabilization-sequence) (step 6)
- **Depends On:** Issue 5 (PyTorch kernel tests)
- **Files to Modify:**
    - `.github/workflows/ci.yml` (modify or create)
- **Test Commands:**
    - Push to branch and verify CI runs PyTorch tests
- **Acceptance Criteria:**
    - [ ] CI installs `torch` (CPU-only) in addition to OpenCL SDK
    - [ ] Runs PyTorch kernel unit tests (`pytest tests/test_pytorch_kernels.py`)
    - [ ] Runs a 100-step PyTorch simulation (drop test config) and verifies no crash
    - [ ] Runs `check_stability.py` on PyTorch output
    - [ ] CI passes on ubuntu-latest without GPU
    - [ ] Total CI time increase <5 minutes
- **Sponsor Summary Hint:** PyTorch is the easiest backend to test in CI — it's pure Python and runs on CPU. Adding it to CI means every code change is tested against two backends (OpenCL + PyTorch) automatically, catching cross-backend regressions before they land.

---

### Issue 9: Audit physical parameters in code vs. DD003 spec

- **Title:** `[DD003] Audit physical parameters in Sibernetic code against DD003 specification`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — Physical Parameters](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#physical-parameters)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary posted on the issue)
- **Test Commands:**
    - N/A (audit task)
- **Acceptance Criteria:**
    - [ ] For each parameter in DD003's Physical Parameters table, find its value in the codebase
    - [ ] Document: file path, line number, variable name, actual value
    - [ ] Flag any discrepancies between DD003 spec and code
    - [ ] Check all three backends (OpenCL, PyTorch, Taichi) use the same parameter values
    - [ ] Post findings as issue comment with a comparison table
    - [ ] If discrepancies found, file follow-up issues for fixes
- **Sponsor Summary Hint:** DD003 specifies exact physical parameters (rest density 1000 kg/m³, viscosity 4e-6 Pa·s, etc.) but does the code actually use these values? And do all three backends use the same values? Parameter drift is a silent source of cross-backend divergence. This audit finds any mismatches.

---

### Issue 10: Benchmark all backends (performance comparison)

- **Title:** `[DD003] Benchmark all backends: OpenCL vs. PyTorch vs. Taichi (Metal/CUDA)`
- **Labels:** `DD003`, `human-expert`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, benchmarking
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Stabilization Sequence](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#stabilization-sequence) (step 7)
- **Depends On:** DD013 Issue 42 (Taichi coordinate fix — must work before meaningful benchmarks)
- **Files to Modify:**
    - `scripts/benchmark_backends.py` (new)
    - `docs/benchmark_results.md` (new — in Sibernetic repo)
- **Test Commands:**
    - `python3 scripts/benchmark_backends.py --backend opencl --config configurations/test_worm_crawl.ini`
    - `python3 scripts/benchmark_backends.py --all --config configurations/test_worm_crawl.ini`
- **Acceptance Criteria:**
    - [ ] Benchmark script runs the same configuration on each available backend
    - [ ] Measures: wall-clock time per timestep, total sim time, memory usage, particle throughput
    - [ ] Runs on at least two particle counts (~25K quick, ~100K standard) to measure scaling
    - [ ] Generates a comparison table in markdown format
    - [ ] Tests on at least 3 platforms: Linux x86 (CI), Apple Silicon (Metal), NVIDIA GPU (CUDA)
    - [ ] Results documented in `docs/benchmark_results.md` with hardware specs
    - [ ] Validates the "~3x faster" (Taichi Metal) and "~5x faster" (Taichi CUDA) claims from DD003
- **Sponsor Summary Hint:** The DD003 backends table claims Taichi is 3-5x faster than OpenCL, but these are target estimates. This issue produces actual measured benchmarks on real hardware — the data needed to decide which backend to recommend for which platform.

---

## Phase 3: Output Pipeline & Visualization

Target: Sibernetic produces output in formats needed by DD010 (validation), DD013 (simulation stack), DD014 (viewer), and DD021 (movement analysis).

---

### Issue 11: Implement OME-Zarr export for particle data

- **Title:** `[DD003] Implement OME-Zarr export for body/positions and body/types`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python
- **DD Section to Read:** [DD003 — Deliverables](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#deliverables) (OME-Zarr rows) and [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/) (OME-Zarr schema)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/export_zarr.py` (new)
- **Test Commands:**
    - `python3 scripts/export_zarr.py output.dat --output output/openworm.zarr`
    - `python3 -c "import zarr; z = zarr.open('output/openworm.zarr'); print(z['body/positions'].shape, z['body/types'].shape)"`
- **Acceptance Criteria:**
    - [ ] Reads Sibernetic binary output and exports to OME-Zarr format
    - [ ] `body/positions/` array: shape (n_timesteps, n_particles, 3), dtype float32
    - [ ] `body/types/` array: shape (n_particles,), dtype int32 (0=liquid, 1=elastic, 2=boundary)
    - [ ] Export interval configurable (every Nth output frame)
    - [ ] Zarr store readable by DD014 viewer
    - [ ] Handles typical simulation sizes (~100K particles × ~500 frames) without OOM
    - [ ] Includes OME-Zarr metadata (axes labels, units)
- **Sponsor Summary Hint:** OME-Zarr is the universal data format connecting simulation to visualization. This script converts Sibernetic's raw binary output into a structured Zarr store that the DD014 3D viewer can read. It's the bridge between physics engine and interactive visualization.

---

### Issue 12: Implement surface mesh reconstruction from SPH particles

- **Title:** `[DD003] Implement marching cubes surface reconstruction from SPH particles`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, 3d-geometry
- **DD Section to Read:** [DD003 — Deliverables](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#deliverables) (surface mesh row) and [DD003 — How to Visualize](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#how-to-visualize) (surface mesh description)
- **Depends On:** Issue 11 (OME-Zarr export)
- **Files to Modify:**
    - `scripts/reconstruct_surface.py` (new)
- **Test Commands:**
    - `python3 scripts/reconstruct_surface.py output/openworm.zarr --output output/openworm.zarr`
    - `python3 -c "import zarr; z = zarr.open('output/openworm.zarr'); print(z['geometry/body_surface'].keys())"`
- **Acceptance Criteria:**
    - [ ] Reads particle positions from OME-Zarr `body/positions/`
    - [ ] Applies marching cubes (via scikit-image or PyVista) to reconstruct smooth body surface
    - [ ] Uses only elastic + boundary particles (not liquid) for surface reconstruction
    - [ ] Outputs vertices and faces arrays to `geometry/body_surface/` in OME-Zarr
    - [ ] Per-frame reconstruction (each timestep gets its own mesh)
    - [ ] Surface is watertight (no holes) and smooth (Laplacian smoothing pass)
    - [ ] Reasonable performance (<1s per frame for 100K particles)
- **Sponsor Summary Hint:** The raw simulation produces a cloud of 100,000 points. This script turns that cloud into a smooth, solid worm shape using marching cubes — the same algorithm used in medical imaging to reconstruct organs from CT scans. The result is what you see in the 3D viewer: a recognizable worm body, not a spray of dots.

---

### Issue 13: Implement WCON trajectory export from SPH output

- **Title:** `[DD003] Implement WCON trajectory export from Sibernetic particle output`
- **Labels:** `DD003`, `human-expert`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — Deliverables](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#deliverables) (WCON row) and [DD021](https://docs.openworm.org/design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy/) (WCON 1.0 spec)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/export_wcon.py` (new)
- **Test Commands:**
    - `python3 scripts/export_wcon.py output.dat --output output/simulation.wcon`
    - `python3 -c "import json; d = json.load(open('output/simulation.wcon')); print(d['units'], len(d['data']))"`
- **Acceptance Criteria:**
    - [ ] Reads Sibernetic particle output and extracts worm centerline (skeleton)
    - [ ] Computes 49-point skeleton from elastic particle positions (anterior→posterior)
    - [ ] Exports WCON 1.0 format with: `units`, `data` (per-frame x/y arrays), `metadata` (Sibernetic version, config)
    - [ ] Skeleton extraction uses PCA or axis-aligned method to find body midline
    - [ ] Output validates against WCON schema (JSON Schema validation)
    - [ ] Compatible with `open-worm-analysis-toolbox` for DD010 Tier 3 validation
- **Sponsor Summary Hint:** WCON (Worm Common Open format) is the standard for sharing worm movement data. To compare our simulation against real worms (DD010 Tier 3 validation), we need to extract the virtual worm's movement trajectory in WCON format. This requires finding the centerline of the worm body from 100,000 SPH particles — essentially asking "where is the worm's spine?"

---

### Issue 14: Implement configurable output frequency via `openworm.yml`

- **Title:** `[DD003] Implement configurable output frequency from openworm.yml simulation.output_interval`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, c++
- **DD Section to Read:** [DD003 — Integration Contract — Configuration](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#configuration) and [DD013 §1](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml) (`simulation.output_interval`)
- **Depends On:** DD013 Issue 9 (config loading in master_openworm.py)
- **Files to Modify:**
    - `src/owPhysicsFluidSimulator.cpp` (output frequency)
    - Sibernetic command-line argument parsing
- **Test Commands:**
    - `./build/Sibernetic -config test.ini -output_interval 100`
    - `ls output/ | wc -l` (verify expected number of output files)
- **Acceptance Criteria:**
    - [ ] Sibernetic accepts `--output_interval N` command-line argument
    - [ ] Output frames written every N timesteps (default: 100)
    - [ ] `master_openworm.py` passes `simulation.output_interval` from `openworm.yml` to Sibernetic
    - [ ] Reducing output interval does not affect simulation accuracy (only I/O frequency)
    - [ ] Quick-test uses high interval (less output, faster), validation uses low interval (more output, thorough)
- **Sponsor Summary Hint:** How often the simulation saves its state to disk. Writing every timestep generates enormous files (100K particles × 50,000 steps = terabytes). Writing every 100th step is a good balance. This makes output frequency configurable so quick tests save less data and validation runs save more.

---

## Phase 4: Advanced Features

Target: New backend options, environmental support, and integration improvements.

---

### Issue 15: Evaluate FEM Projective Dynamics backend feasibility

- **Title:** `[DD003] Evaluate Projective Dynamics FEM backend feasibility (Zhao et al. / BAAIWorm)`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** physics, c++, cuda
- **DD Section to Read:** [DD003 — Alternatives Considered — FEM](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#1-finite-element-method-fem) (Update 2026-02 section)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a feasibility report)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Clone and inspect BAAIWorm repo (github.com/Jessie940611/BAAIWorm)
    - [ ] Document: build requirements (CUDA version, OptiX, compiler)
    - [ ] Document: mesh format and resolution (984 vertices, 3,341 tetrahedrons)
    - [ ] Document: muscle actuator interface (96 actuators — compatible with DD002?)
    - [ ] Document: performance benchmarks (claimed 30 FPS — verify)
    - [ ] Document: physics fidelity (surface hydrodynamics only — no internal fluid)
    - [ ] Assess: effort to wrap as `body.backend: "fem-projective"` in OpenWorm stack
    - [ ] Assess: CUDA/OptiX dependency — can it run on Apple Silicon? CI?
    - [ ] Post feasibility report as issue comment with go/no-go recommendation
- **Sponsor Summary Hint:** Zhao et al. (2024) demonstrated a worm body simulation running at 30 FPS using Projective Dynamics FEM — orders of magnitude faster than our SPH approach. Their code (BAAIWorm) is open source. This feasibility study determines whether we can add it as a "fast mode" backend for rapid iteration and CI testing, complementing the biophysically richer SPH approach.

---

### Issue 16: Create Sibernetic Python bindings for direct API access

- **Title:** `[DD003] Create Python bindings for Sibernetic C++ library`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, c++, pybind11
- **DD Section to Read:** [DD003 — Integration Contract](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#integration-contract) (coupling dependencies)
- **Depends On:** None
- **Files to Modify:**
    - `python/sibernetic_bindings.cpp` (new — pybind11 wrapper)
    - `python/sibernetic/__init__.py` (new — Python package)
    - `CMakeLists.txt` (add pybind11 target)
    - `setup.py` or `pyproject.toml` (new — pip installable)
- **Test Commands:**
    - `pip install -e .`
    - `python3 -c "import sibernetic; sim = sibernetic.Simulation(); sim.step()"`
- **Acceptance Criteria:**
    - [ ] `pip install` produces a `sibernetic` Python package
    - [ ] Python API exposes: `Simulation(config_path)`, `.step()`, `.get_positions()`, `.get_velocities()`, `.get_densities()`
    - [ ] Can inject muscle forces from Python: `sim.set_muscle_activation(quadrant, value)`
    - [ ] Can read particle state without file I/O (direct memory access)
    - [ ] Works with OpenCL backend (C++ core + Python wrapper)
    - [ ] Enables `sibernetic_c302.py` to call Sibernetic directly instead of via subprocess
    - [ ] Pybind11 wraps the existing C++ API, no algorithmic changes needed
- **Sponsor Summary Hint:** Currently the neural circuit (Python) and body physics (C++) communicate via file I/O — muscle forces written to a file, particle positions read from a file. Python bindings would allow direct function calls between them, dramatically simplifying the coupling code and eliminating file I/O bottlenecks. This is how modern scientific Python packages (NumPy, SciPy) wrap C/Fortran backends.

---

### Issue 17: Add gel/agar environment configuration support

- **Title:** `[DD003] Verify and document gel/agar environment support in openworm.yml`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** physics
- **DD Section to Read:** [DD003 — Boundaries](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#boundaries-explicitly-out-of-scope) (item 3: gel simulation) and Palyanov et al. 2018 (Section 2c, agar gel)
- **Depends On:** DD013 Issue 1 (openworm.yml config schema)
- **Files to Modify:**
    - `configurations/worm_crawl_gel.ini` (new or verify existing)
    - Documentation update in DD003 (if gel support is confirmed working)
- **Test Commands:**
    - `./build/Sibernetic -config configurations/worm_crawl_gel.ini -timestep 0.00002 -duration 1.0`
- **Acceptance Criteria:**
    - [ ] Verify Sibernetic's agar gel mode works with current codebase (elastic matter cubes in 3D grid)
    - [ ] Create or locate gel-mode `.ini` configuration file
    - [ ] Run gel simulation and verify worm produces crawling-like (not swimming) gait
    - [ ] Document environment options in DD003: liquid (swimming) vs. gel (crawling)
    - [ ] Propose `body.environment: "liquid" | "gel"` config option for `openworm.yml`
- **Sponsor Summary Hint:** Real worms behave differently on solid surfaces (crawling) vs. in liquid (swimming). Sibernetic supports both via different environments — liquid for swimming and agar gel for crawling. This issue verifies the gel mode still works and makes it configurable via the `openworm.yml` system so contributors can easily switch between environments.

---

## Phase 5: Documentation & Maintenance

Target: Comprehensive documentation enabling new contributors to understand and modify Sibernetic.

---

### Issue 18: Create Sibernetic architecture overview documentation

- **Title:** `[DD003] Create Sibernetic architecture overview for contributors`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD003 — Technical Approach](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#technical-approach) and [DD003 — Implementation References](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#implementation-references)
- **Depends On:** None
- **Files to Modify:**
    - `docs/architecture.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] High-level overview: what Sibernetic is, what it produces, who uses its output
    - [ ] File map: which source files contain which functionality
    - [ ] Data flow diagram: input config → particle init → SPH loop → output
    - [ ] Timestep walkthrough: what happens in one simulation step (neighbor search → density → pressure → forces → integrate)
    - [ ] Backend comparison: when to use OpenCL vs. PyTorch vs. Taichi
    - [ ] References to DD003 for specification details
    - [ ] Aimed at L2 contributors (familiar with physics but new to codebase)
- **Sponsor Summary Hint:** New contributors need a map before they can navigate. This document explains what each file does, how data flows through the simulation, and what happens in a single timestep. DD003 is the specification (what should happen); this is the implementation guide (where the code lives and how it works).

---

### Issue 19: Document muscle cell mapping (96 units to particle indices)

- **Title:** `[DD003] Document muscle cell mapping from 96 units to elastic particle indices`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** docs, physics
- **DD Section to Read:** [DD003 — Muscle Actuation](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#muscle-actuation-force-injection) and Palyanov et al. 2018 (Section 2b)
- **Depends On:** None
- **Files to Modify:**
    - `docs/muscle_mapping.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Explains: how 95 body-wall muscles → 96 independently activable units
    - [ ] Explains: 4 quadrants (VR, VL, DR, DL) × 24 muscles per quadrant
    - [ ] Documents: which elastic particles belong to which muscle unit
    - [ ] Documents: how `sibernetic_c302.py` maps c302 motor neuron output to Sibernetic muscle indices
    - [ ] Includes a diagram or table showing muscle → quadrant → particle index mapping
    - [ ] References WormAtlas microphotograph geometries (Palyanov et al. 2018)
- **Sponsor Summary Hint:** The 96-muscle mapping is one of Sibernetic's most sophisticated features — each muscle unit activates a specific subset of elastic particles based on real worm anatomy. But this mapping is embedded deep in the code with minimal documentation. This makes it accessible, which is critical for anyone working on the muscle-physics coupling (DD002→DD003 interface).

---

### Issue 20: Create Sibernetic CONTRIBUTING.md with backend development guide

- **Title:** `[DD003] Create CONTRIBUTING.md with backend development workflow and standards`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD003 — Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) and [DD003 — How to Build & Test](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#how-to-build-test)
- **Depends On:** None
- **Files to Modify:**
    - `CONTRIBUTING.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Prerequisites: what to install for OpenCL, PyTorch, and Taichi development
    - [ ] Build instructions for each backend
    - [ ] Testing workflow: unit tests → stability check → incompressibility check → parity test
    - [ ] PR checklist from DD003 Quality Criteria (all 6 criteria)
    - [ ] Branch naming convention: `dd003/description`
    - [ ] How to add a new backend (step-by-step guide)
    - [ ] How to run the cross-backend parity test suite
    - [ ] Links to DD003 for specifications and DD013 for Docker integration
- **Sponsor Summary Hint:** A CONTRIBUTING.md is the entry point for any developer. This one specifically guides physics engine contributors through the multi-backend testing workflow — build, test, compare against OpenCL baseline, submit PR. Without it, contributors won't know which tests to run or what quality bar to meet.

---

### Issue 21: Create Sibernetic changelog from git history

- **Title:** `[DD003] Create annotated changelog documenting Sibernetic's evolution`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** git, docs
- **DD Section to Read:** [DD003 — Validated Kinematic Outputs](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#validated-kinematic-outputs-palyanov-et-al-2018)
- **Depends On:** None
- **Files to Modify:**
    - `CHANGELOG.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] List major milestones: initial SPH, PCISPH addition, muscle mapping, PyTorch backend, Taichi backend
    - [ ] Map milestones to publications (Palyanov et al. 2018, etc.)
    - [ ] Note key branch points: `master`, `ow-0.9.7`, `ow-pytorch-0.0.1`
    - [ ] Document current active branches and what they contain
    - [ ] Note deprecated/abandoned experiments
    - [ ] Useful for new contributors understanding how the codebase evolved
- **Sponsor Summary Hint:** Sibernetic has been in development since ~2014 across multiple branches. A changelog helps new contributors understand what exists, what's been tried, and what worked. Without it, they'll stumble over abandoned experiments and wonder why there are multiple solver implementations.

---

### Issue 22: Verify and document Sibernetic's existing test suite

- **Title:** `[DD003] Audit existing Sibernetic test suite and document test coverage`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD003 Quality Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#quality-criteria) (criterion 3: unit tests)
- **Depends On:** None
- **Files to Modify:**
    - `docs/test_coverage.md` (new — in Sibernetic repo)
- **Test Commands:**
    - `pytest tests/ -v --tb=short` (or equivalent for C++ tests)
- **Acceptance Criteria:**
    - [ ] Inventory all existing tests (unit, integration, regression)
    - [ ] Document: which tests exist, what they test, which backend they target
    - [ ] Run all tests and report pass/fail status
    - [ ] Identify gaps: which DD003 Quality Criteria are not covered by existing tests
    - [ ] Document the "76+ tests pass" claim for PyTorch backend — which specific tests?
    - [ ] Recommend: priority test additions to improve coverage
    - [ ] Post findings as `docs/test_coverage.md`
- **Sponsor Summary Hint:** DD003 says "76+ tests pass" on PyTorch, but which tests? Before adding new tests, we need to know what exists. This audit catalogs the current test suite, identifies gaps, and creates a roadmap for improving coverage. You can't improve what you don't measure.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 22 |
| **ai-workable** | 14 |
| **human-expert** | 8 |
| **L1** | 8 |
| **L2** | 9 |
| **L3** | 5 |

| Phase | Issues | Target |
|-------|--------|--------|
| **1: Validation Infrastructure** | 1–6 | Scripts and test configs to measure quality |
| **2: Backend Stabilization** | 7–10 | Support the DD013 Issues 40–44 stabilization sequence |
| **3: Output Pipeline** | 11–14 | OME-Zarr, WCON, surface mesh, configurable output |
| **4: Advanced Features** | 15–17 | FEM evaluation, Python bindings, gel environment |
| **5: Documentation** | 18–22 | Architecture docs, muscle mapping, contributing guide |

### Cross-Reference: DD013 Backend Stabilization Issues (also labeled DD003)

| DD013 Issue | Title | Label | Level |
|-------------|-------|-------|-------|
| 40 | Create stability validation scripts | `DD003`, `ai-workable` | L1 |
| 41 | Create cross-backend parity test suite | `DD003`, `ai-workable` | L2 |
| 42 | Fix Taichi elastic coordinate-space bug | `DD003`, `human-expert` | L2 |
| 43 | Audit PyTorch/Taichi result quality gap | `DD003`, `human-expert` | L3 |
| 44 | Graduate backends to Stable/Production | `DD003`, `ai-workable` | L2 |

**Combined DD003 total (this doc + DD013):** 27 issues

### Dependency Graph (Critical Path)

```
Issue 1 (check_stability.py) ─┐
Issue 2 (incompressibility.py)─┤
                               ├→ DD013 Issue 40 (validation scripts — superset)
Issue 3 (test configs) ────────┤
                               ├→ Issue 4 (OpenCL baseline)
                               │     └→ DD013 Issue 41 (parity test suite)
                               │           ├→ DD013 Issue 42 (Taichi coordinate fix)
                               │           │     └→ DD013 Issue 43 (quality gap audit)
                               │           │           └→ DD013 Issue 44 (graduate backends)
                               │           └→ Issue 10 (benchmarks)
                               │
Issue 5 (PyTorch kernel tests) ┤
Issue 6 (Taichi kernel tests)  ├→ Issue 8 (PyTorch CI)
                               │
Issue 7 (OpenCL docs) ─────────┘→ DD013 Issue 43 (quality gap audit)

Issue 11 (OME-Zarr export) → Issue 12 (surface mesh)
Issue 13 (WCON export) — independent
Issue 14 (output frequency) — depends on DD013 Issue 9
Issue 15 (FEM evaluation) — independent
Issue 16 (Python bindings) — independent
Issue 17 (gel environment) — depends on DD013 Issue 1

Issues 9, 18–22 (audits/docs) — independent
```
