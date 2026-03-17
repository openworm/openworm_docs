# DD003 Draft GitHub Issues

**Epic:** DD003 — Body Physics Engine (Sibernetic) Architecture

**Generated from:** [DD003: Body Physics Engine Architecture](DD003_Body_Physics_Architecture.md)

**Methodology:** [DD015 §2.2 — DD Issue Generator](DD015_AI_Contributor_Model.md#22-the-dd-issue-generator-automated-issue-creation), [DD015 §2.3 — Reuse-First Methodology](DD015_AI_Contributor_Model.md#23-reuse-first-methodology), [DD015 §2.4 — DD013 Simulation Stack Integration](DD015_AI_Contributor_Model.md#24-dd013-simulation-stack-integration)

**Totals:** 21 issues (ai-workable: 14 / human-expert: 7 | L1: 8, L2: 8, L3: 5)

**Note:** Backend stabilization Issues 40–44 in [DD013_draft_issues](DD013_draft_issues.md) are also labeled `DD003` and are cross-referenced here but not duplicated.

**Roadmap Context:** DD003 is a **Phase 0** DD (existing, working). Its draft issues span multiple roadmap phases:

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Validation Infrastructure (Issues 1-6) | **Phase A1** | 3 `[TO BE CREATED]` scripts + test configs |
| 2. Backend Stabilization (Issues 7-10) | **Phase A1** | OpenCL documentation, CI smoke tests |
| 3. Output Pipeline (Issues 11-13) | **Phase A1/1** | OME-Zarr export (A), surface mesh (1), config (A) |
| 4. Advanced Features (Issues 14-16) | **Phase 2+** | FEM evaluation, Python bindings |
| 5. Documentation (Issues 17-21) | **Any** | Can be addressed independently |

---

## Group 1: Validation Infrastructure (Phase A1)

Target: Scripts and test configurations needed to measure simulation quality and compare backends.

---

### Issue 1: Create `scripts/check_stability.py`

- **Title:** `[DD003] Create check_stability.py — simulation divergence detector`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — How to Build & Test](DD003_Body_Physics_Architecture.md#how-to-build-test) (Step 3) and [DD003 Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) (criterion 1)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/owPhysicTest.cpp`](https://github.com/openworm/sibernetic) — Energy conservation test already exists; validates that total system energy (kinetic + potential) remains bounded across timesteps. Reuse its energy-bounding logic as a stability criterion alongside NaN/escape detection.
    - [`openworm/sibernetic/run_all_tests.sh`](https://github.com/openworm/sibernetic) — 5 bash test configurations that run Sibernetic with different parameters; reference for how tests are invoked.
- **Approach:** Extend — build on the energy conservation logic in `owPhysicTest.cpp` and add NaN/escape/velocity checks as a Python wrapper.
- **DD013 Pipeline Role:** Body-stage validation gate. Runs after Sibernetic simulation completes. Non-zero exit code blocks the pipeline run as failed. Output path configured via `openworm.yml`.
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
- **Sponsor Summary Hint:** The basic health check for any SPH simulation — did the physics blow up? NaN values mean the computation diverged (division by zero, impossible forces). Escaped particles mean the simulation lost containment. This script is listed as a DD003 deliverable but was never created. The existing `owPhysicTest.cpp` already checks energy conservation — this extends that logic into a comprehensive Python stability checker.

---

### Issue 2: Create `scripts/validate_incompressibility.py`

- **Title:** `[DD003] Create validate_incompressibility.py — density deviation checker`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — How to Build & Test](DD003_Body_Physics_Architecture.md#how-to-build-test) (Step 4) and [DD003 Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) (criterion 2)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Defines rest density ρ₀ and other physical constants with extensive inline documentation. Reference for expected density values and particle type classifications.
    - [`openworm/sibernetic/src/sphFluid.cl`](https://github.com/openworm/sibernetic) — The PCISPH pressure solver that enforces incompressibility; reference for understanding what the script validates.
- **Approach:** Create — no existing incompressibility validation script exists, but `owPhysicsConstant.h` provides all physical constants needed.
- **DD013 Pipeline Role:** Body-stage validation gate. Runs after Sibernetic simulation completes. Non-zero exit code blocks the pipeline run as failed.
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

### Issue 3: Document and extend standard test configuration directories

- **Title:** `[DD003] Document existing binary test configurations and create missing scenario directories`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** physics
- **DD Section to Read:** [DD003 Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) (criterion 4) and [DD003 Backend Stabilization Roadmap — Cross-Backend Parity Requirements](DD003_Body_Physics_Architecture.md#cross-backend-parity-requirements)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/configuration/`](https://github.com/openworm/sibernetic) — **12+ binary configuration directories** already exist, including `worm_crawl_*`, `worm_no_water_*`, and demo configurations. Sibernetic uses binary configuration directories (containing particle position/velocity/type buffers), NOT `.ini` text files. Each directory contains binary blobs that initialize particle state.
    - [`openworm/sibernetic/run_all_tests.sh`](https://github.com/openworm/sibernetic) — 5 bash test configurations that exercise different scenarios (drop test, crawl, etc.) with specific command-line flags.
- **Approach:** Adapt — document the existing binary configuration directories and `run_all_tests.sh` scenarios, then create any missing test scenario directories (e.g., isolated elastic deformation, single-quadrant muscle activation) using the existing configurations as templates.
- **Files to Modify:**
    - `configuration/test_elastic_deformation/` (new — binary config directory, generated from existing worm config with liquid particles removed)
    - `configuration/test_muscle_single_quadrant/` (new — binary config directory, generated from existing worm config)
    - `configuration/README.md` (new — documents all configs including existing ones)
- **Test Commands:**
    - `./build/Sibernetic -f configuration/worm_crawl_demo`
    - `./build/Sibernetic -f configuration/test_elastic_deformation`
    - `bash run_all_tests.sh`
- **Acceptance Criteria:**
    - [ ] `README.md` documents ALL existing configuration directories (12+), including what each tests and expected behavior
    - [ ] `README.md` documents the binary configuration format (position/velocity/type buffers per directory)
    - [ ] `test_elastic_deformation/`: Elastic body suspended under gravity (no liquid). Should sag measurably.
    - [ ] `test_muscle_single_quadrant/`: Full worm body with single quadrant (e.g., MDR) activated at constant force. Should bend.
    - [ ] Each new config directory is generated programmatically from existing configs (document the generation script)
    - [ ] All configs run without crash on the OpenCL backend
    - [ ] `run_all_tests.sh` updated to include new test scenarios
- **Sponsor Summary Hint:** Sibernetic already has 12+ binary configuration directories and 5 test scenarios in `run_all_tests.sh`. This issue documents what already exists, fills in missing test scenarios (isolated elastic test, single-quadrant muscle test), and creates a README so contributors know which configuration to use for which purpose. Note: Sibernetic uses binary configuration directories, not `.ini` text files.

---

### Issue 4: Create OpenCL baseline metrics for parity tests

- **Title:** `[DD003] Generate and save OpenCL baseline metrics for cross-backend parity tests`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Cross-Backend Parity Requirements](DD003_Body_Physics_Architecture.md#cross-backend-parity-requirements)
- **Depends On:** Issue 3 (test configs), DD013 Issue 39 (parity test script)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/configuration/`](https://github.com/openworm/sibernetic) — Existing binary configuration directories provide the test scenarios to run.
    - [`openworm/sibernetic/src/owPhysicTest.cpp`](https://github.com/openworm/sibernetic) — Energy conservation test provides a reference for what metrics to capture (energy, position bounds).
- **Approach:** Create — no baseline metrics infrastructure exists, but test configs and energy test provide the foundation.
- **Files to Modify:**
    - `tests/baseline/drop_test_opencl.json` (new)
    - `tests/baseline/elastic_deformation_opencl.json` (new)
    - `tests/baseline/muscle_contraction_opencl.json` (new)
    - `tests/baseline/worm_crawl_opencl.json` (new)
    - `tests/baseline/README.md` (new — documents baseline generation)
- **Test Commands:**
    - `python3 scripts/backend_parity_test.py --backend opencl --save-baseline tests/baseline/`
- **Acceptance Criteria:**
    - [ ] Run all 4 test scenarios on OpenCL backend using existing binary configuration directories
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
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) (criterion 3, 5) and [DD003 — SPH Kernel Functions](DD003_Body_Physics_Architecture.md#sph-kernel-functions)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/sphFluid.cl`](https://github.com/openworm/sibernetic) — The 64KB OpenCL kernel file containing all SPH kernel function implementations (Wpoly6, ∇Wspiky, ∇²Wviscosity, elastic bond forces, PCISPH). These are the reference implementations that PyTorch tests must match.
    - [`openworm/sibernetic/src/owPhysicTest.cpp`](https://github.com/openworm/sibernetic) — Energy conservation test showing how to validate physics output programmatically.
- **Approach:** Create — no PyTorch kernel tests exist. Use `sphFluid.cl` as the reference specification for expected outputs.
- **Note:** The PyTorch backend does not exist on Sibernetic's main branch. This issue targets a feature branch or requires the PyTorch backend to be merged first.
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
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) (criterion 3, 5) and [DD003 — SPH Kernel Functions](DD003_Body_Physics_Architecture.md#sph-kernel-functions)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/sphFluid.cl`](https://github.com/openworm/sibernetic) — The 64KB OpenCL kernel file containing all SPH kernel function implementations. Reference for expected outputs.
    - [`openworm/sibernetic/src/sphFluid_crawling.cl`](https://github.com/openworm/sibernetic) — Crawling-specific kernel variant with agar gel interactions. May have additional kernel functions not in the standard version.
- **Approach:** Create — no Taichi kernel tests exist. Use `sphFluid.cl` and `sphFluid_crawling.cl` as the reference specifications.
- **Note:** The Taichi backend does not exist on Sibernetic's main branch. This issue targets a feature branch or requires the Taichi backend to be merged first.
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

## Group 2: Backend Stabilization (Phase A1)

Target: PyTorch and Taichi backends produce results matching OpenCL within ±5%.

**Note:** The core backend stabilization issues are tracked in [DD013_draft_issues.md](DD013_draft_issues.md) as Issues 39–42 (labeled `DD003`). They cover:

- **DD013 Issue 39:** Create cross-backend parity test suite
- **DD013 Issue 40:** Fix Taichi elastic coordinate-space bug
- **DD013 Issue 41:** Audit and fix PyTorch/Taichi result quality gap
- **DD013 Issue 42:** Graduate backends to Stable/Production

Stability validation scripts (`check_stability.py`, `validate_incompressibility.py`) are DD003 Issues 1–2 above.

The issues below supplement that sequence with DD003-specific work.

---

### Issue 7: Document OpenCL kernel architecture (`sphFluid.cl`)

- **Title:** `[DD003] Document OpenCL kernel architecture for algorithmic audit`
- **Labels:** `DD003`, `human-expert`, `L2`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** opencl, physics, sph
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — The Result Quality Gap](DD003_Body_Physics_Architecture.md#the-result-quality-gap) and [DD003 — Implementation References](DD003_Body_Physics_Architecture.md#implementation-references)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/sphFluid.cl`](https://github.com/openworm/sibernetic) — The 64KB OpenCL kernel file. THIS is the primary subject of this documentation issue.
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Extensive inline documentation of physical constants, particle types, and simulation parameters. Use as companion reference when documenting kernels.
- **Approach:** Create — no kernel architecture documentation exists, but the source files themselves contain significant inline comments.
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
- **Sponsor Summary Hint:** The OpenCL kernel file is the 64KB brain of the physics engine — the actual GPU code that moves 100,000 particles. Nobody has documented what it does at the code level. Before we can audit why PyTorch/Taichi produce different results (DD013 Issue 41), we need to understand what the reference implementation actually computes. This is like creating an annotated blueprint before renovating a building.

---

### Issue 8: Add PyTorch backend to CI smoke test

- **Title:** `[DD003] Add PyTorch backend smoke test to GitHub Actions CI`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** ci-cd, python
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Stabilization Sequence](DD003_Body_Physics_Architecture.md#stabilization-sequence) (step 6)
- **Depends On:** Issue 5 (PyTorch kernel tests)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/run_all_tests.sh`](https://github.com/openworm/sibernetic) — 5 existing bash test configurations. These should be integrated into the CI workflow alongside PyTorch tests.
- **Approach:** Create — Sibernetic currently has NO CI infrastructure at all (no `.github/workflows/` directory on main branch). This issue creates CI from scratch, starting with PyTorch since it's the easiest backend to test without GPU hardware.
- **DD013 Pipeline Role:** Body-stage CI gate. CI must pass before merging PRs to Sibernetic. Integrates with DD013's `docker compose run quick-test` workflow.
- **Note:** Sibernetic currently has NO CI at all — no GitHub Actions workflows exist on the main branch. This issue creates the first CI workflow.
- **Files to Modify:**
    - `.github/workflows/ci.yml` (new — first CI workflow for Sibernetic)
- **Test Commands:**
    - Push to branch and verify CI runs PyTorch tests
- **Acceptance Criteria:**
    - [ ] CI installs `torch` (CPU-only) in addition to OpenCL SDK
    - [ ] Runs PyTorch kernel unit tests (`pytest tests/test_pytorch_kernels.py`)
    - [ ] Runs a 100-step PyTorch simulation (drop test config) and verifies no crash
    - [ ] Runs `check_stability.py` on PyTorch output
    - [ ] CI passes on ubuntu-latest without GPU
    - [ ] Total CI time increase <5 minutes
- **Sponsor Summary Hint:** PyTorch is the easiest backend to test in CI — it's pure Python and runs on CPU. Adding it to CI means every code change is tested against two backends (OpenCL + PyTorch) automatically, catching cross-backend regressions before they land. Note: Sibernetic currently has NO CI at all — this creates it from scratch.

---

### Issue 9: Audit physical parameters in code vs. DD003 spec

- **Title:** `[DD003] Audit physical parameters in Sibernetic code against DD003 specification`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 — Physical Parameters](DD003_Body_Physics_Architecture.md#physical-parameters)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Extensive header file with inline documentation of every physical constant. THIS is the primary file to audit — it documents parameters, their units, and their physical meaning.
- **Approach:** Create — no parameter audit exists, but `owPhysicsConstant.h` is well-documented and provides the code-side values to compare against DD003.
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
- **Sponsor Summary Hint:** DD003 specifies exact physical parameters (rest density 1000 kg/m³, viscosity 4e-6 Pa·s, etc.) but does the code actually use these values? And do all three backends use the same values? Parameter drift is a silent source of cross-backend divergence. This audit finds any mismatches. The good news: `owPhysicsConstant.h` has extensive inline documentation, making the audit tractable.

---

### Issue 10: Benchmark all backends (performance comparison)

- **Title:** `[DD003] Benchmark all backends: OpenCL vs. PyTorch vs. Taichi (Metal/CUDA)`
- **Labels:** `DD003`, `human-expert`, `L2`
- **Roadmap Phase:** Phase A1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, benchmarking
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Stabilization Sequence](DD003_Body_Physics_Architecture.md#stabilization-sequence) (step 7)
- **Depends On:** DD013 Issue 40 (Taichi coordinate fix — must work before meaningful benchmarks)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/run_all_tests.sh`](https://github.com/openworm/sibernetic) — 5 existing test configurations that can serve as benchmark scenarios.
- **Approach:** Create — no benchmark infrastructure exists. Use `run_all_tests.sh` scenarios and existing binary configuration directories as benchmark inputs.
- **Files to Modify:**
    - `scripts/benchmark_backends.py` (new)
    - `docs/benchmark_results.md` (new — in Sibernetic repo)
- **Test Commands:**
    - `python3 scripts/benchmark_backends.py --backend opencl --config configuration/worm_crawl_demo`
    - `python3 scripts/benchmark_backends.py --all --config configuration/worm_crawl_demo`
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

## Group 3: Output Pipeline & Visualization (Phase A1/1)

Target: Sibernetic produces output in formats needed by DD010 (validation), DD013 (simulation stack), DD014 (viewer), and DD021 (movement analysis).

---

### Issue 11: Implement OME-Zarr export for particle data

- **Title:** `[DD003] Implement OME-Zarr export for body/positions and body/types`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A1/1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python
- **DD Section to Read:** [DD003 — Deliverables](DD003_Body_Physics_Architecture.md#deliverables) (OME-Zarr rows) and [DD014](DD014_Dynamic_Visualization_Architecture.md) (OME-Zarr schema)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owVtkExport.h`](https://github.com/openworm/sibernetic) — VTK export already exists for particle data visualization. Reference for how particle data is extracted and formatted for external tools.
    - [`openworm/sibernetic/wcon/generate_wcon.py`](https://github.com/openworm/sibernetic) — Shows how to read Sibernetic output files from Python. Reference for I/O patterns.
- **Approach:** Create — no OME-Zarr export exists. Use `owVtkExport.h` and `generate_wcon.py` as references for how particle data is accessed.
- **DD013 Pipeline Role:** Body-stage post-processing. Runs after Sibernetic simulation completes. Produces Zarr store artifact at path configured via `openworm.yml` for DD014 visualization stage.
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
- **Sponsor Summary Hint:** OME-Zarr is the universal data format connecting simulation to visualization. This script converts Sibernetic's raw binary output into a structured Zarr store that the DD014 3D viewer can read. It's the bridge between physics engine and interactive visualization. The existing `owVtkExport.h` shows how particle data is already extracted for VTK — this creates the OME-Zarr equivalent.

---

### Issue 12: Implement surface mesh reconstruction from SPH particles

- **Title:** `[DD003] Implement marching cubes surface reconstruction from SPH particles`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Roadmap Phase:** Phase A1/1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, 3d-geometry
- **DD Section to Read:** [DD003 — Deliverables](DD003_Body_Physics_Architecture.md#deliverables) (surface mesh row) and [DD003 — How to Visualize](DD003_Body_Physics_Architecture.md#how-to-visualize) (surface mesh description)
- **Depends On:** Issue 11 (OME-Zarr export)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owVtkExport.h`](https://github.com/openworm/sibernetic) — VTK export for particle visualization. Can serve as the input reader for surface reconstruction.
    - [`openworm/skeletonExtraction`](https://github.com/openworm/skeletonExtraction) — C++ skeleton extraction from Sibernetic mesh output (3D graphics skeleton for animation). Different purpose (animation skeleton vs. surface mesh) but related geometry processing on the same particle data.
- **Approach:** Extend — build on `owVtkExport.h` for particle data access and reference `skeletonExtraction` for geometry processing patterns on Sibernetic output.
- **DD013 Pipeline Role:** Body-stage post-processing. Runs after OME-Zarr export. Adds `geometry/body_surface/` group to the Zarr store for DD014 viewer.
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
- **Sponsor Summary Hint:** The raw simulation produces a cloud of 100,000 points. This script turns that cloud into a smooth, solid worm shape using marching cubes — the same algorithm used in medical imaging to reconstruct organs from CT scans. The result is what you see in the 3D viewer: a recognizable worm body, not a spray of dots. The existing `owVtkExport.h` and `skeletonExtraction` repo provide reference implementations for working with Sibernetic's particle data.

---

### Issue 13: Implement configurable output frequency via `openworm.yml`

- **Title:** `[DD003] Implement configurable output frequency from openworm.yml simulation.output_interval`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A1/1
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, c++
- **DD Section to Read:** [DD003 — Integration Contract — Configuration](DD003_Body_Physics_Architecture.md#configuration) and [DD013 §1](DD013_Simulation_Stack_Architecture.md#1-simulation-configuration-system-openwormyml) (`simulation.output_interval`)
- **Depends On:** DD013 Issue 9 (config loading in master_openworm.py)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/owPhysicsFluidSimulator.cpp`](https://github.com/openworm/sibernetic) — Contains the output writing logic. The output frequency is controlled here — this is the file to modify.
- **Approach:** Create — no configurable output frequency exists. Modify the output loop in `owPhysicsFluidSimulator.cpp` to respect an interval parameter.
- **DD013 Pipeline Role:** Body-stage configuration. `master_openworm.py` passes `simulation.output_interval` from `openworm.yml` to Sibernetic via command-line argument.
- **Files to Modify:**
    - `src/owPhysicsFluidSimulator.cpp` (output frequency)
    - Sibernetic command-line argument parsing
- **Test Commands:**
    - `./build/Sibernetic -f configuration/worm_crawl_demo -output_interval 100`
    - `ls output/ | wc -l` (verify expected number of output files)
- **Acceptance Criteria:**
    - [ ] Sibernetic accepts `--output_interval N` command-line argument
    - [ ] Output frames written every N timesteps (default: 100)
    - [ ] `master_openworm.py` passes `simulation.output_interval` from `openworm.yml` to Sibernetic
    - [ ] Reducing output interval does not affect simulation accuracy (only I/O frequency)
    - [ ] Quick-test uses high interval (less output, faster), validation uses low interval (more output, thorough)
- **Sponsor Summary Hint:** How often the simulation saves its state to disk. Writing every timestep generates enormous files (100K particles × 50,000 steps = terabytes). Writing every 100th step is a good balance. This makes output frequency configurable so quick tests save less data and validation runs save more.

---

## Group 4: Advanced Features (Phase 2+)

Target: New backend options, environmental support, and integration improvements.

---

### Issue 14: Evaluate FEM Projective Dynamics backend feasibility

- **Title:** `[DD003] Evaluate Projective Dynamics FEM backend feasibility (Zhao et al. / BAAIWorm / Metaworm)`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 2+
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** physics, c++, cuda
- **DD Section to Read:** [DD003 — Alternatives Considered — FEM](DD003_Body_Physics_Architecture.md#1-finite-element-method-fem) (Update 2026-02 section)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`Jessie940611/BAAIWorm/Metaworm/sim/fem/`](https://github.com/Jessie940611/BAAIWorm) — **Complete FEM Projective Dynamics implementation.** Directory structure includes:
        - `FEMSolver.cpp` / `FEMSolver.h` — Core FEM solver with Projective Dynamics iteration
        - `Constraint.cpp` / `Constraint.h` — Strain, volume, and attachment constraints
        - `Muscle.cpp` / `Muscle.h` — 96-muscle actuator model with per-muscle activation input
        - `World.cpp` / `World.h` — Scene management, collision handling, time integration
    - [`Jessie940611/BAAIWorm/Metaworm/data/worm_mesh_4.obj`](https://github.com/Jessie940611/BAAIWorm) — Worm body mesh: 984 vertices, 3,341 tetrahedrons. Ready-to-use FEM mesh.
    - [`Jessie940611/BAAIWorm/Metaworm/sim/`](https://github.com/Jessie940611/BAAIWorm) — Build system, CUDA/OptiX rendering pipeline, Python bindings via `pybind11`.
- **Approach:** Evaluate — comprehensive feasibility study of the BAAIWorm/Metaworm FEM implementation for integration as an alternative Sibernetic backend.
- **Files to Modify:**
    - None (research issue — output is a feasibility report)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Clone and build BAAIWorm/Metaworm FEM solver (`sim/fem/`)
    - [ ] Document: build requirements — CUDA version (tested: 11.x), OptiX 7.x for rendering, C++17 compiler
    - [ ] Document: mesh format — `data/worm_mesh_4.obj` (984 vertices, 3,341 tetrahedrons)
    - [ ] Document: muscle actuator interface — `Muscle.cpp` implements 96 actuators; verify mapping compatibility with DD002's 96-muscle activation array
    - [ ] Document: constraint system — `Constraint.cpp` implements strain limits, volume preservation, and attachment constraints
    - [ ] Document: performance benchmarks (claimed 30 FPS — verify on available hardware)
    - [ ] Document: physics fidelity — surface hydrodynamics only (no internal fluid simulation, unlike SPH)
    - [ ] Assess: effort to wrap as `body.backend: "fem-projective"` in OpenWorm stack
    - [ ] Assess: CUDA/OptiX dependency — can it run on Apple Silicon? CI? (likely no — CUDA required)
    - [ ] Post feasibility report as issue comment with go/no-go recommendation
- **Sponsor Summary Hint:** Zhao et al. (2024) demonstrated a worm body simulation running at 30 FPS using Projective Dynamics FEM — orders of magnitude faster than our SPH approach. Their code (BAAIWorm/Metaworm) is open source with a complete implementation: FEM solver, 984-vertex mesh, 96-muscle actuator, and constraint system all in `sim/fem/`. This feasibility study determines whether we can add it as a "fast mode" backend for rapid iteration and CI testing.

---

### Issue 15: Create Sibernetic Python bindings for direct API access

- **Title:** `[DD003] Create Python bindings for Sibernetic C++ library`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 2+
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, c++, pybind11
- **DD Section to Read:** [DD003 — Integration Contract](DD003_Body_Physics_Architecture.md#integration-contract) (coupling dependencies)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/owSignalSimulator.cpp`](https://github.com/openworm/sibernetic) — Already contains a CPython API integration layer using direct `PyObject` calls to interface with NEURON/c302. This demonstrates that C++↔Python interop already exists in the codebase — the question is whether to formalize it with pybind11 or extend the existing CPython approach.
- **Approach:** Extend — build on the existing CPython API calls in `owSignalSimulator.cpp`. Two viable paths: (a) formalize with pybind11 for a clean public API, (b) extend the existing CPython embedding for backward compatibility.
- **Note:** Sibernetic uses a Makefile build system, not CMake. Adding pybind11 would require either CMake migration or Makefile-based pybind11 integration.
- **Files to Modify:**
    - `python/sibernetic_bindings.cpp` (new — pybind11 wrapper)
    - `python/sibernetic/__init__.py` (new — Python package)
    - `CMakeLists.txt` or `Makefile` (add pybind11 target)
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
- **Sponsor Summary Hint:** Currently the neural circuit (Python) and body physics (C++) communicate via file I/O. Python bindings would allow direct function calls, dramatically simplifying the coupling code and eliminating file I/O bottlenecks. The existing `owSignalSimulator.cpp` already has CPython API calls — this formalizes that into a proper Python package.

---

### Issue 16: Add gel/agar environment configuration support

- **Title:** `[DD003] Verify and document gel/agar environment support in openworm.yml`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase 2+
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** physics
- **DD Section to Read:** [DD003 — Boundaries](DD003_Body_Physics_Architecture.md#boundaries-explicitly-out-of-scope) (item 3: gel simulation) and Palyanov et al. 2018 (Section 2c, agar gel)
- **Depends On:** DD013 Issue 1 (openworm.yml config schema)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/configuration/worm_crawl_*`](https://github.com/openworm/sibernetic) — Existing crawl configuration directories that may already include gel/agar environment settings.
    - [`openworm/sibernetic/src/sphFluid_crawling.cl`](https://github.com/openworm/sibernetic) — Crawling-specific OpenCL kernel with agar gel particle interactions. This kernel variant handles the gel environment physics.
- **Approach:** Wrap — gel mode already exists in the codebase (`sphFluid_crawling.cl` + `worm_crawl_*` configs). This issue verifies it works, documents it, and wraps it with an `openworm.yml` config option.
- **DD013 Pipeline Role:** Body-stage configuration. `body.environment` in `openworm.yml` selects between liquid (swimming) and gel (crawling) modes.
- **Files to Modify:**
    - `configuration/README.md` (update — document gel vs. liquid configs)
    - Documentation update in DD003 (if gel support is confirmed working)
- **Test Commands:**
    - `./build/Sibernetic -f configuration/worm_crawl_demo`
- **Acceptance Criteria:**
    - [ ] Verify Sibernetic's agar gel mode works with current codebase (elastic matter cubes in 3D grid, using `sphFluid_crawling.cl`)
    - [ ] Verify the existing `worm_crawl_*` configuration directories provide gel environment
    - [ ] Run gel simulation and verify worm produces crawling-like (not swimming) gait
    - [ ] Document environment options in DD003: liquid (swimming, `sphFluid.cl`) vs. gel (crawling, `sphFluid_crawling.cl`)
    - [ ] Propose `body.environment: "liquid" | "gel"` config option for `openworm.yml`
- **Sponsor Summary Hint:** Real worms behave differently on solid surfaces (crawling) vs. in liquid (swimming). Sibernetic already supports both via `sphFluid.cl` (liquid) and `sphFluid_crawling.cl` (gel), with corresponding `worm_crawl_*` configuration directories. This issue verifies gel mode still works and makes it configurable via `openworm.yml`.

---

## Group 5: Documentation & Maintenance (Any)

Target: Comprehensive documentation enabling new contributors to understand and modify Sibernetic.

---

### Issue 17: Create Sibernetic architecture overview documentation

- **Title:** `[DD003] Create Sibernetic architecture overview for contributors`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD003 — Technical Approach](DD003_Body_Physics_Architecture.md#technical-approach) and [DD003 — Implementation References](DD003_Body_Physics_Architecture.md#implementation-references)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/README.md`](https://github.com/openworm/sibernetic) — 17.5KB README with build instructions, usage examples, and project overview. Start from this as the foundation and expand into a structured architecture document.
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Extensive inline documentation of simulation parameters and physics constants. Source material for the architecture overview.
- **Approach:** Extend — the 17.5KB README and well-documented `owPhysicsConstant.h` provide substantial content to build on.
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
- **Sponsor Summary Hint:** New contributors need a map before they can navigate. This document explains what each file does, how data flows through the simulation, and what happens in a single timestep. DD003 is the specification (what should happen); this is the implementation guide (where the code lives and how it works). The existing 17.5KB README and well-documented `owPhysicsConstant.h` provide a strong foundation.

---

### Issue 18: Document muscle cell mapping (96 units to particle indices)

- **Title:** `[DD003] Document muscle cell mapping from 96 units to elastic particle indices`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** docs, physics
- **DD Section to Read:** [DD003 — Muscle Actuation](DD003_Body_Physics_Architecture.md#muscle-actuation-force-injection) and Palyanov et al. 2018 (Section 2b)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/main_sim.py`](https://github.com/openworm/sibernetic) — Python simulation entry point that documents the 96-element muscle array format: `[MDR_0...MDR_23, MVR_0...MVR_23, MVL_0...MVL_23, MDL_0...MDL_23]`.
    - [`openworm/sibernetic/src/owConfigProperty.cpp`](https://github.com/openworm/sibernetic) — Configuration loading code that maps muscle indices to elastic particle subsets.
- **Approach:** Create — no muscle mapping documentation exists, but the code in `main_sim.py` and `owConfigProperty.cpp` contains the mapping.
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

### Issue 19: Create Sibernetic CONTRIBUTING.md with backend development guide

- **Title:** `[DD003] Create CONTRIBUTING.md with backend development workflow and standards`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD003 — Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) and [DD003 — How to Build & Test](DD003_Body_Physics_Architecture.md#how-to-build-test)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/run_all_tests.sh`](https://github.com/openworm/sibernetic) — 5 existing test configurations. Document these as the standard test suite in the contributing guide.
    - [`openworm/sibernetic/README.md`](https://github.com/openworm/sibernetic) — 17.5KB README with build instructions. Reference for build workflow.
- **Approach:** Create — no CONTRIBUTING.md exists. Use `run_all_tests.sh` and README as foundation.
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

### Issue 20: Create Sibernetic changelog from git history

- **Title:** `[DD003] Create annotated changelog documenting Sibernetic's evolution`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** git, docs
- **DD Section to Read:** [DD003 — Validated Kinematic Outputs](DD003_Body_Physics_Architecture.md#validated-kinematic-outputs-palyanov-et-al-2018)
- **Depends On:** None
- **Existing Code to Reuse:**
    - Git history of `openworm/sibernetic` — the primary source material for this changelog.
- **Approach:** Create — no changelog exists. Mine the git history.
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

### Issue 21: Verify and document Sibernetic's existing test suite

- **Title:** `[DD003] Audit existing Sibernetic test suite and document test coverage`
- **Labels:** `DD003`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD003 Quality Criteria](DD003_Body_Physics_Architecture.md#quality-criteria) (criterion 3: unit tests)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/run_all_tests.sh`](https://github.com/openworm/sibernetic) — 5 bash test configurations. THIS is the existing test suite to audit.
    - [`openworm/sibernetic/src/owPhysicTest.cpp`](https://github.com/openworm/sibernetic) — Energy conservation test.
    - [`openworm/sibernetic/wcon/generate_wcon.py`](https://github.com/openworm/sibernetic) — WCON generation with schema validation (has its own test data).
- **Approach:** Create — no test coverage documentation exists. Run and catalog all existing tests.
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
| **Total Issues** | 21 |
| **ai-workable** | 14 |
| **human-expert** | 7 |
| **L1** | 8 |
| **L2** | 8 |
| **L3** | 5 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Validation Infrastructure** | 1–6 | Scripts and test configs to measure quality |
| **2: Backend Stabilization** | 7–10 | Support the DD013 Issues 39–42 stabilization sequence |
| **3: Output Pipeline** | 11–13 | OME-Zarr, surface mesh, configurable output |
| **4: Advanced Features** | 14–16 | FEM evaluation, Python bindings, gel environment |
| **5: Documentation** | 17–21 | Architecture docs, muscle mapping, contributing guide |

### Cross-Reference: DD013 Backend Stabilization Issues (also labeled DD003)

| DD013 Issue | Title | Label | Level |
|-------------|-------|-------|-------|
| 39 | Create cross-backend parity test suite | `DD003`, `ai-workable` | L2 |
| 40 | Fix Taichi elastic coordinate-space bug | `DD003`, `human-expert` | L2 |
| 41 | Audit PyTorch/Taichi result quality gap | `DD003`, `human-expert` | L3 |
| 42 | Graduate backends to Stable/Production | `DD003`, `ai-workable` | L2 |

**Combined DD003 total (this doc + DD013):** 25 issues

### Dependency Graph (Critical Path)

```
Issue 1 (check_stability.py) ─┐
Issue 2 (incompressibility.py)─┤
Issue 3 (test configs) ────────┤
                               ├→ Issue 4 (OpenCL baseline)
                               │     └→ DD013 Issue 39 (parity test suite)
                               │           ├→ DD013 Issue 40 (Taichi coordinate fix)
                               │           │     └→ DD013 Issue 41 (quality gap audit)
                               │           │           └→ DD013 Issue 42 (graduate backends)
                               │           └→ Issue 10 (benchmarks)
                               │
Issue 5 (PyTorch kernel tests) ┤
Issue 6 (Taichi kernel tests)  ├→ Issue 8 (PyTorch CI)
                               │
Issue 7 (OpenCL docs) ─────────┘→ DD013 Issue 41 (quality gap audit)

Issue 11 (OME-Zarr export) → Issue 12 (surface mesh)
Issue 13 (output frequency) — depends on DD013 Issue 9
Issue 14 (FEM evaluation) — independent
Issue 15 (Python bindings) — independent
Issue 16 (gel environment) — depends on DD013 Issue 1

Issues 9, 17–21 (audits/docs) — independent
```
