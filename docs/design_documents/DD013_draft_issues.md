# DD013 Draft GitHub Issues

**Epic:** DD013 — Simulation Stack Architecture

**Generated from:** [DD013: Simulation Stack Architecture](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 42 issues (ai-workable: 31 / human-expert: 11 | L1: 17, L2: 15, L3: 9)

---

## Phase A: Foundation (Weeks 1–4)

Target: Contributors can `docker compose run quick-test` with their branch.

---

### Issue 1: Create `openworm.yml` config schema

- **Title:** `[DD013] Create openworm.yml declarative configuration schema`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD013 §1 — Simulation Configuration System](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml)
- **Depends On:** None
- **Files to Modify:**
    - `openworm.yml` (new file — root of repo)
    - `configs/validation_full.yml` (new — full validation preset)
- **Test Commands:**
    - `python3 -c "import yaml; yaml.safe_load(open('openworm.yml'))"`
    - `yamllint openworm.yml`
- **Acceptance Criteria:**
    - [ ] `openworm.yml` exists at repo root with all sections from DD013 §1 (neural, body, muscle, pharynx, intestine, simulation, validation, output, visualization, viewer)
    - [ ] All default values match DD013 spec (e.g., `neural.level: C1`, `simulation.duration: 15.0`)
    - [ ] File is valid YAML (loads without error)
    - [ ] Comments explain every parameter with DD cross-references
    - [ ] `configs/validation_full.yml` enables all validation tiers
- **Sponsor Summary Hint:** This config file is the "control panel" for the entire worm simulation. Each section controls a different biological subsystem — neural circuit, body physics, muscles, pharynx, intestine. Contributors toggle subsystems on/off to test specific changes, just like a lab bench setup.

---

### Issue 2: Write `openworm.yml` validation script

- **Title:** `[DD013] Write Python validation script for openworm.yml`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD013 §1 — Simulation Configuration System](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml)
- **Depends On:** Issue 1
- **Files to Modify:**
    - `scripts/validate_config.py` (new)
    - `tests/test_config.py` (new)
- **Test Commands:**
    - `python3 scripts/validate_config.py openworm.yml`
    - `pytest tests/test_config.py`
- **Acceptance Criteria:**
    - [ ] Script validates YAML structure against expected schema
    - [ ] Detects missing required sections, invalid types, out-of-range values
    - [ ] Validates cross-section constraints (e.g., `muscle.enabled` requires `neural.enabled`)
    - [ ] Returns exit code 0 on valid config, non-zero on invalid
    - [ ] Unit tests cover valid config, missing sections, invalid values, cross-constraints
- **Sponsor Summary Hint:** A guard-rail script that checks the simulation config file before running. Like a preflight checklist — catches typos and invalid settings before wasting 20 minutes on a failed build.

---

### Issue 3: Create multi-stage Dockerfile (6 stages)

- **Title:** `[DD013] Create multi-stage Dockerfile with base, neural, body, validation, full, and viewer stages`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 §2 — Multi-Stage Docker Build](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#2-multi-stage-docker-build-layered-images)
- **Depends On:** Issue 1
- **Files to Modify:**
    - `Dockerfile` (replace existing monolithic Dockerfile)
- **Test Commands:**
    - `docker build --target base -t openworm/base .`
    - `docker build --target neural -t openworm/neural .`
    - `docker build --target full -t openworm/full .`
- **Acceptance Criteria:**
    - [ ] 6 named stages: `base`, `neural`, `body`, `validation`, `full`, `viewer`
    - [ ] `base` installs Ubuntu 24.04, Python 3, NEURON 8.2.6, build tools
    - [ ] `neural` clones c302 at `$C302_REF` build arg
    - [ ] `body` clones Sibernetic at `$SIBERNETIC_REF` build arg, builds with cmake
    - [ ] `full` copies from neural + body + validation stages
    - [ ] `viewer` extends full with Trame/VTK/OME-Zarr deps
    - [ ] Each stage builds independently (`docker build --target <stage>`)
    - [ ] Build args allow contributor override of subsystem branches
- **Sponsor Summary Hint:** The Docker image is how every contributor runs the simulation identically. The multi-stage design means changing one subsystem (e.g., the neural circuit) only rebuilds that layer — 5 min instead of 20 min. Like modular LEGO vs. a single molded block.

---

### Issue 4: Create `docker-compose.yml` (quick-test, simulation, shell)

- **Title:** `[DD013] Create docker-compose.yml with quick-test, simulation, validate, and shell services`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 §3 — Docker Compose for Composable Execution](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#3-docker-compose-for-composable-execution)
- **Depends On:** Issue 3
- **Files to Modify:**
    - `docker-compose.yml` (new file)
- **Test Commands:**
    - `docker compose config` (validates YAML)
    - `docker compose build simulation`
- **Acceptance Criteria:**
    - [ ] Services defined: `quick-test`, `simulation`, `validate`, `shell`
    - [ ] `quick-test` runs 10ms sim with `--no-video`
    - [ ] `simulation` runs default 15ms with 8G memory limit
    - [ ] `validate` runs full validation config with 16G memory limit
    - [ ] `shell` provides interactive bash with volumes mounted
    - [ ] Shared `./output` volume on all services
    - [ ] `docker compose config` validates without errors
- **Sponsor Summary Hint:** Docker Compose lets contributors run different modes with one command: `quick-test` for a 2-minute sanity check, `simulation` for the full run, `validate` for CI-level checks, and `shell` for interactive debugging. Each mode maps to a step in the scientific workflow.

---

### Issue 5: Add viewer service to docker-compose

- **Title:** `[DD013] Add viewer service to docker-compose.yml for DD014 visualization`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 §3 — Docker Compose](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#3-docker-compose-for-composable-execution) (viewer service block) and [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/)
- **Depends On:** Issue 4
- **Files to Modify:**
    - `docker-compose.yml` (add `viewer` service)
- **Test Commands:**
    - `docker compose config`
- **Acceptance Criteria:**
    - [ ] `viewer` service defined targeting `viewer` Docker stage
    - [ ] Exposes port 8501
    - [ ] `depends_on: simulation` with `service_completed_successfully` condition
    - [ ] Mounts `./output` volume for reading OME-Zarr data
    - [ ] Runs `viewer/app.py` pointing at `output/openworm.zarr`
- **Sponsor Summary Hint:** The viewer service launches a 3D visualization of the simulation output (body shape, neural activity, muscle forces) in a web browser. It reads the OME-Zarr data bus — the universal data format that all subsystems write to. See [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/).

---

### Issue 6: Add neural-dev service to docker-compose

- **Title:** `[DD013] Add neural-dev service to docker-compose.yml for neural-only development`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 §3 — Docker Compose](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#3-docker-compose-for-composable-execution) (neural-dev service block)
- **Depends On:** Issue 4
- **Files to Modify:**
    - `docker-compose.yml` (add `neural-dev` service)
- **Test Commands:**
    - `docker compose config`
- **Acceptance Criteria:**
    - [ ] `neural-dev` service targets the `neural` Docker stage
    - [ ] Runs c302 network generation (`generate('C1', 'FW')`)
    - [ ] Mounts `./output` volume
    - [ ] No body physics dependencies required
- **Sponsor Summary Hint:** This lets neural circuit developers test their changes without building the body physics engine (Sibernetic). It's like testing the worm's brain in isolation — faster iteration for anyone working on [DD001](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/) neural architecture.

---

### Issue 7: Create `versions.lock` with pinned commits

- **Title:** `[DD013] Create versions.lock file with pinned dependency commits`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** git, yaml
- **DD Section to Read:** [DD013 §4 — Dependency Pinning](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#4-dependency-pinning-versionslock)
- **Depends On:** None
- **Files to Modify:**
    - `versions.lock` (new file — root of repo)
- **Test Commands:**
    - `python3 -c "import yaml; yaml.safe_load(open('versions.lock'))"`
- **Acceptance Criteria:**
    - [ ] Entries for: c302, sibernetic, connectome_toolbox, neuron, open_worm_analysis_toolbox, tracker_commons, owmeta
    - [ ] Each entry has `repo`, `commit` (actual current hash from each repo's main branch), `tag` (if applicable)
    - [ ] `system` section pins ubuntu, python, java versions
    - [ ] `opencl_sdk` section with URL and sha256 placeholder
    - [ ] Valid YAML
    - [ ] Comments explain that only Integration Maintainer updates this file
- **Sponsor Summary Hint:** Dependency pinning ensures every contributor builds the exact same simulation. Without it, one person might get a newer c302 version that's incompatible with Sibernetic. Like freezing a recipe's ingredient list — reproducible science requires reproducible builds.

---

### Issue 8: Write `build.sh` (reads versions.lock, passes Docker build args)

- **Title:** `[DD013] Write build.sh script that reads versions.lock and passes build args to Docker`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, docker
- **DD Section to Read:** [DD013 §4 — Dependency Pinning](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#4-dependency-pinning-versionslock) (build script section)
- **Depends On:** Issue 7
- **Files to Modify:**
    - `build.sh` (replace existing)
- **Test Commands:**
    - `bash build.sh --dry-run` (prints docker build command without executing)
    - `shellcheck build.sh`
- **Acceptance Criteria:**
    - [ ] Reads `versions.lock` to extract commit hashes for each subsystem
    - [ ] Passes `--build-arg C302_REF=<hash>` and `--build-arg SIBERNETIC_REF=<hash>` to `docker build`
    - [ ] Tags image with version from `VERSION` file
    - [ ] Supports `--dry-run` flag for testing
    - [ ] Supports override args (e.g., `build.sh --c302-ref my-branch`)
    - [ ] Passes shellcheck
- **Sponsor Summary Hint:** This script is the bridge between `versions.lock` (which says what versions to use) and the Docker build (which compiles them). It reads the pinned commits and feeds them to the Dockerfile as build arguments.

---

### Issue 9: Refactor `master_openworm.py` Step 1 — config loading

- **Title:** `[DD013] Refactor master_openworm.py to load and use openworm.yml configuration`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 1) and [DD013 §1 — Config System](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml)
- **Depends On:** Issue 1
- **Files to Modify:**
    - `master_openworm.py`
- **Test Commands:**
    - `python3 master_openworm.py --config openworm.yml --dry-run`
    - `pytest tests/test_master_openworm.py`
- **Acceptance Criteria:**
    - [ ] `master_openworm.py` accepts `--config` argument pointing to `openworm.yml`
    - [ ] Loads config via `yaml.safe_load()`, validates structure
    - [ ] Replaces hardcoded defaults with config values
    - [ ] Falls back to `default_config.yml` if no `--config` specified
    - [ ] Adds `--dry-run` flag that prints config and exits without running simulation
    - [ ] Existing Step 3 behavior unchanged when using default config
- **Sponsor Summary Hint:** The orchestrator script (`master_openworm.py`) currently has simulation parameters hardcoded. This refactor makes it read from `openworm.yml` instead, so contributors can change what the simulation does by editing a config file rather than Python code.

---

### Issue 10: Refactor `master_openworm.py` Step 2 — subsystem init

- **Title:** `[DD013] Implement master_openworm.py Step 2: conditional subsystem initialization`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 2) and [DD001](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/) (c302 network generation)
- **Depends On:** Issue 9
- **Files to Modify:**
    - `master_openworm.py`
- **Test Commands:**
    - `python3 master_openworm.py --config configs/neural_only.yml --dry-run`
    - `docker compose run quick-test`
- **Acceptance Criteria:**
    - [ ] Step 2 initializes each subsystem conditionally based on config `enabled` flags
    - [ ] `neural.enabled: true` → generates c302 network at specified `level` and `reference`
    - [ ] `body.enabled: true` → initializes Sibernetic with specified `backend` and `particle_count`
    - [ ] `pharynx.enabled: false` → skips pharynx initialization (placeholder for future)
    - [ ] `intestine.enabled: false` → skips intestine initialization (placeholder for future)
    - [ ] Error messages if a dependent subsystem is disabled (e.g., muscle without neural)
- **Sponsor Summary Hint:** Step 2 is where the simulation "wakes up" each organ system. If neural is enabled, c302 generates the worm's neural circuit (302 neurons, thousands of synapses). If body is enabled, Sibernetic initializes the fluid dynamics for the worm's physical body. The config file controls which organs are active — like choosing which systems to study in a virtual dissection.

---

### Issue 11: Refactor `master_openworm.py` Step 3 — coupled sim loop

- **Title:** `[DD013] Implement master_openworm.py Step 3: configurable coupled simulation loop`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 3)
- **Depends On:** Issue 10
- **Files to Modify:**
    - `master_openworm.py`
- **Test Commands:**
    - `docker compose run quick-test`
    - `docker compose run simulation`
- **Acceptance Criteria:**
    - [ ] Coupled simulation loop uses config values: `simulation.duration`, `simulation.dt_neuron`, `simulation.dt_coupling`
    - [ ] Each enabled subsystem advances one timestep per loop iteration
    - [ ] Data exchange at coupling boundaries (Ca2+ from neural → forces in muscle → body physics)
    - [ ] Output frames written at `simulation.output_interval` frequency
    - [ ] Simulation runs to configured `duration` and exits cleanly
    - [ ] Quick test (10ms) completes in <5 minutes
- **Sponsor Summary Hint:** This is the actual simulation loop — the "heartbeat" of the virtual worm. Each tick, the neural circuit computes which neurons fire, calcium signals propagate to muscles, muscles generate forces, and the body physics engine moves the virtual worm's particles through fluid. The coupling interval (`dt_coupling`) determines how often these systems exchange data.

---

### Issue 12: Create `scripts/quick-test.sh`

- **Title:** `[DD013] Create scripts/quick-test.sh smoke test for contributors`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker, testing
- **DD Section to Read:** [DD013 §3 — Docker Compose](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#3-docker-compose-for-composable-execution) and [DD013 Quality Criteria](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#quality-criteria) (criterion 2: <5 min)
- **Depends On:** Issue 4
- **Files to Modify:**
    - `scripts/quick-test.sh` (new)
- **Test Commands:**
    - `bash scripts/quick-test.sh`
    - `shellcheck scripts/quick-test.sh`
- **Acceptance Criteria:**
    - [ ] Runs `docker compose run quick-test`
    - [ ] Checks output directory for expected files (PNGs, WCON)
    - [ ] Prints PASS/FAIL summary
    - [ ] Returns exit code 0 on success, non-zero on failure
    - [ ] Completes in <5 minutes total
    - [ ] Passes shellcheck
- **Sponsor Summary Hint:** The contributor smoke test — a 2-minute sanity check that runs a minimal 10ms simulation and verifies outputs exist. Every contributor should run this before submitting a PR. It's the minimum bar: "does it still run?"

---

### Issue 13: CI Gate 1 — Docker build on PR/push

- **Title:** `[DD013] Create GitHub Actions CI Gate 1: Docker build verification`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** ci-cd
- **DD Section to Read:** [DD013 §6 — CI/CD Pipeline](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#6-cicd-pipeline-automated-quality-gates) (Gate 1)
- **Depends On:** Issue 3
- **Files to Modify:**
    - `.github/workflows/integration.yml` (new)
- **Test Commands:**
    - Push to a test branch and verify Actions workflow runs
- **Acceptance Criteria:**
    - [ ] Triggers on `pull_request` to `main`/`dev*` and `push` to `main`
    - [ ] `build` job runs `docker compose build simulation`
    - [ ] 30-minute timeout
    - [ ] Runs on `ubuntu-latest`
    - [ ] Fails if Docker build fails
- **Sponsor Summary Hint:** The first CI gate: does it compile? Every PR automatically builds the Docker image. If a code change breaks the build, the contributor knows immediately — no waiting for human review to discover a syntax error.

---

### Issue 14: CI Gate 2 — smoke test

- **Title:** `[DD013] Create GitHub Actions CI Gate 2: smoke test after build`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** ci-cd
- **DD Section to Read:** [DD013 §6 — CI/CD Pipeline](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#6-cicd-pipeline-automated-quality-gates) (Gate 2)
- **Depends On:** Issue 12, Issue 13
- **Files to Modify:**
    - `.github/workflows/integration.yml` (add `smoke-test` job)
- **Test Commands:**
    - Push to a test branch and verify smoke test job runs after build
- **Acceptance Criteria:**
    - [ ] `smoke-test` job runs after `build` job succeeds
    - [ ] Runs `docker compose run quick-test`
    - [ ] Checks that output PNGs and WCON file exist
    - [ ] 10-minute timeout
    - [ ] Fails if outputs are missing
- **Sponsor Summary Hint:** The second CI gate: does it run? After the build succeeds, CI runs a minimal simulation and checks that outputs (plots, movement data) were actually generated. Catches runtime errors that passed compilation.

---

### Issue 15: Fix video pipeline memory leak

- **Title:** `[DD013] Fix video pipeline memory leak (OOM at >2s simulations)`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, docker
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (video pipeline fix options) and [DD013 Context — Known Issues](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#known-critical-issues)
- **Depends On:** None
- **Files to Modify:**
    - `master_openworm.py` (video recording section)
    - Possibly `sibernetic_c302.py` or related rendering code
- **Test Commands:**
    - `docker compose run simulation` with `simulation.duration: 2000` (2 seconds)
    - Monitor memory: `docker stats` during run
- **Acceptance Criteria:**
    - [ ] 2-second simulation completes without OOM kill on 8GB RAM
    - [ ] 5-second simulation completes without OOM kill on 16GB RAM
    - [ ] Video output generated (or cleanly skipped with `--no-video`)
    - [ ] Fix uses one of: headless rendering (OSMesa/EGL), post-hoc visualization, or streaming to disk
    - [ ] Related issues [#332](https://github.com/openworm/OpenWorm/issues/332), [#341](https://github.com/openworm/OpenWorm/issues/341) resolved
- **Sponsor Summary Hint:** The current simulation records video by capturing screenshots of a virtual display — but it stores ALL frames in memory, causing out-of-memory crashes for simulations longer than 2 seconds. A 5s sim needs 64GB RAM just for video. The fix decouples recording from simulation, either by rendering headlessly or saving positions and creating video afterwards.

---

### Issue 16: Fix Docker GPU passthrough and backend selection

- **Title:** `[DD013] Fix Docker GPU passthrough and backend selection`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 Context — Known Issues](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#known-critical-issues), [DD013 Open Questions](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#open-questions-require-founder-input) (question 2), and [DD003 Backend Stabilization Roadmap](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#backend-stabilization-roadmap)
- **Depends On:** None
- **Files to Modify:**
    - `Dockerfile` (OpenCL/GPU layers + conditional Taichi/PyTorch installation)
    - `docker-compose.yml` (GPU device passthrough)
- **Test Commands:**
    - `docker compose run simulation` with GPU available
    - `clinfo` inside container to verify OpenCL device visible
    - `docker compose run simulation` with `body.backend: pytorch` (verify backend selection works)
- **Acceptance Criteria:**
    - [ ] Sibernetic detects and uses GPU via OpenCL inside Docker container
    - [ ] docker-compose.yml includes GPU device passthrough config (nvidia-docker2 or similar)
    - [ ] Falls back to CPU OpenCL gracefully when no GPU available
    - [ ] `body.backend` config selects between opencl, pytorch, taichi-metal, taichi-cuda
    - [ ] Taichi/PyTorch deps installed conditionally based on selected backend
    - [ ] Performance improvement documented (expect ~10x speedup for GPU backends)
    - [ ] Issue [#320](https://github.com/openworm/OpenWorm/issues/320) resolved
- **Sponsor Summary Hint:** Sibernetic simulates the worm's body as ~100,000 fluid particles — massively parallel computation that GPUs excel at. Currently the Docker image forces CPU-only OpenCL mode (10x slower) and doesn't support alternative backends. This broadens Docker to support GPU passthrough AND conditional installation of Taichi/PyTorch backends per the DD003 Backend Stabilization Roadmap.

---

### Issue 17: Pin apt packages + add virtualenv

- **Title:** `[DD013] Pin apt package versions and add Python virtualenv to Dockerfile`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 Context — Known Issues](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#known-critical-issues) (dependency pinning, virtualenv rows) and [DD013 §4 — Dependency Pinning](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#4-dependency-pinning-versionslock)
- **Depends On:** Issue 3
- **Files to Modify:**
    - `Dockerfile` (base stage)
- **Test Commands:**
    - `docker build --target base .`
    - `docker run openworm/base pip --version` (verify virtualenv active)
- **Acceptance Criteria:**
    - [ ] All `apt-get install` commands use pinned versions (e.g., `python3=3.12.*`)
    - [ ] Python packages installed inside a virtualenv (not `--break-system-packages`)
    - [ ] Virtualenv activated in subsequent stages
    - [ ] Issues [#314](https://github.com/openworm/OpenWorm/issues/314), [#317](https://github.com/openworm/OpenWorm/issues/317) addressed
- **Sponsor Summary Hint:** Without pinned package versions, the exact same Dockerfile can produce different results on different days — a package update could silently break the simulation. Using virtualenv isolates Python dependencies, preventing conflicts with system packages. Both are standard practices for reproducible science.

---

## Phase B: Validation Integration (Weeks 5–8)

Target: PRs to main are automatically validated. JupyterLab available for exploration.

---

### Issue 18: `master_openworm.py` Step 4 — output generation

- **Title:** `[DD013] Implement master_openworm.py Step 4: output generation (plots, WCON, video)`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 4)
- **Depends On:** Issue 11
- **Files to Modify:**
    - `master_openworm.py` (Step 4 implementation)
- **Test Commands:**
    - `docker compose run simulation`
    - `ls output/` (verify PNGs, WCON, optional MP4)
- **Acceptance Criteria:**
    - [ ] Generates membrane potential plots (PNG)
    - [ ] Generates calcium concentration plots (PNG)
    - [ ] Generates movement trajectory plots (PNG)
    - [ ] Exports WCON trajectory file
    - [ ] Generates video if `output.video: true` (and memory leak is fixed)
    - [ ] Respects `output.directory` config setting
    - [ ] All outputs written to the shared output volume
- **Sponsor Summary Hint:** Step 4 turns raw simulation data into human-readable outputs. Membrane potential plots show which neurons fired when (like an EEG for the worm). WCON is a standardized movement data format so other tools can analyze the worm's locomotion. This is where computation becomes science.

---

### Issue 19: `master_openworm.py` Step 4b — OME-Zarr export

- **Title:** `[DD013] Implement master_openworm.py Step 4b: OME-Zarr data export for DD014 viewer`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 4b) and [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/) (OME-Zarr schema)
- **Depends On:** Issue 18
- **Files to Modify:**
    - `master_openworm.py` (Step 4b implementation)
- **Test Commands:**
    - `docker compose run simulation`
    - `python3 -c "import zarr; z = zarr.open('output/openworm.zarr'); print(list(z.keys()))"`
- **Acceptance Criteria:**
    - [ ] Exports `openworm.zarr` with groups: `body/positions`, `body/types`, `neural/voltage`, `neural/calcium`, `muscle/activation`
    - [ ] Writes at `visualization.export_interval` frequency
    - [ ] Runs marching cubes surface reconstruction if `visualization.surface_reconstruction: true`
    - [ ] Only runs if `visualization.enabled: true`
    - [ ] Zarr file readable by [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/) viewer
- **Sponsor Summary Hint:** OME-Zarr is the universal data bus for the whole simulation — every subsystem writes its state to a shared Zarr store. The [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/) viewer reads this to render 3D visualizations. It's like a shared whiteboard where each organ writes its current state, and the viewer reads all of them at once.

---

### Issue 20: `master_openworm.py` Step 5 — DD010 validation

- **Title:** `[DD013] Implement master_openworm.py Step 5: DD010 validation framework integration`
- **Labels:** `DD013`, `human-expert`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD013 §5 — Enhanced master_openworm.py](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 5) and [DD010](https://docs.openworm.org/design_documents/DD010_Validation_Framework/)
- **Depends On:** Issue 18
- **Files to Modify:**
    - `master_openworm.py` (Step 5 implementation)
    - `scripts/check_ci_results.py` (new — parses validation report)
- **Test Commands:**
    - `docker compose run validate`
    - `python3 scripts/check_ci_results.py output/validation_report.json`
- **Acceptance Criteria:**
    - [ ] Runs Tier 1 (electrophysiology) if `validation.tier1_electrophysiology: true`
    - [ ] Runs Tier 2 (functional connectivity) if `validation.tier2_functional_connectivity: true`
    - [ ] Runs Tier 3 (behavioral kinematics) if `validation.tier3_behavioral: true`
    - [ ] Generates `validation_report.json` with pass/fail per tier
    - [ ] Exits with non-zero code if any enabled tier fails
    - [ ] `check_ci_results.py` parses report and prints human-readable summary
- **Sponsor Summary Hint:** Validation is how we know the simulation is scientifically accurate. Tier 1 checks individual neuron behavior against patch-clamp recordings. Tier 2 compares circuit-level activity patterns against [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain imaging data. Tier 3 compares the virtual worm's movement to real worm videos. It's the scientific method applied to simulation.

---

### Issue 21: CI Gate 3 — Tier 2 validation on PRs

- **Title:** `[DD013] Create GitHub Actions CI Gate 3: Tier 2 validation on pull requests`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** ci-cd
- **DD Section to Read:** [DD013 §6 — CI/CD Pipeline](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#6-cicd-pipeline-automated-quality-gates) (Gate 3)
- **Depends On:** Issue 14, Issue 20
- **Files to Modify:**
    - `.github/workflows/integration.yml` (add `tier2-validation` job)
- **Test Commands:**
    - Open a PR and verify Tier 2 validation job runs
- **Acceptance Criteria:**
    - [ ] `tier2-validation` job runs after `smoke-test` succeeds
    - [ ] Only runs on `pull_request` events
    - [ ] Runs `docker compose run validate` with Tier 2 config
    - [ ] Calls `check_ci_results.py` to verify pass/fail
    - [ ] 60-minute timeout
    - [ ] Reports results as PR check
- **Sponsor Summary Hint:** This CI gate runs circuit-level validation (functional connectivity) on every PR. If a code change breaks the neural circuit's behavior relative to real worm brain data, the PR is automatically flagged. No more "merge and hope" — science checks happen before human review.

---

### Issue 22: CI Gate 4 — Tier 3 validation on main

- **Title:** `[DD013] Create GitHub Actions CI Gate 4: Tier 3 behavioral validation on main branch`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** ci-cd
- **DD Section to Read:** [DD013 §6 — CI/CD Pipeline](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#6-cicd-pipeline-automated-quality-gates) (Gate 4)
- **Depends On:** Issue 21
- **Files to Modify:**
    - `.github/workflows/integration.yml` (add `tier3-validation` job)
- **Test Commands:**
    - Merge to main and verify Tier 3 job triggers
- **Acceptance Criteria:**
    - [ ] `tier3-validation` job runs after `smoke-test` succeeds
    - [ ] Only runs on `push` to `main`
    - [ ] Runs 5-second simulation with Tier 3 behavioral validation
    - [ ] Uploads `validation_report.json` as GitHub artifact
    - [ ] 120-minute timeout
    - [ ] Reports results as commit status
- **Sponsor Summary Hint:** The strongest validation gate — only runs when code lands on main. It simulates 5 seconds of worm movement and compares locomotion kinematics (speed, wavelength, amplitude) against real worm videos from the Schafer lab. This is the ultimate test: does the virtual worm move like a real worm?

---

### Issue 23: Add JupyterLab service to docker-compose

- **Title:** `[DD013] Add JupyterLab service to docker-compose.yml for interactive exploration`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 §9 — JupyterLab Interface](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#9-jupyterlab-interface-issue-347)
- **Depends On:** Issue 4
- **Files to Modify:**
    - `docker-compose.yml` (add `jupyter` service)
- **Test Commands:**
    - `docker compose up jupyter`
    - Open `http://localhost:8888` in browser
- **Acceptance Criteria:**
    - [ ] `jupyter` service targets `full` Docker stage
    - [ ] Runs `jupyter lab` on port 8888
    - [ ] Mounts `./output` and `./notebooks` directories
    - [ ] No authentication token (empty token for local use)
    - [ ] JupyterLab accessible at `http://localhost:8888`
- **Sponsor Summary Hint:** JupyterLab gives newcomers an interactive notebook environment inside the simulation container. They can explore the connectome, run simulations, and visualize results — all in a web browser. This directly supports [DD011](https://docs.openworm.org/design_documents/DD011_Contributor_Progression_Model/) L0→L1 onboarding.

---

### Issue 24: Notebook: `02_run_c302_network.ipynb`

- **Title:** `[DD013] Create starter notebook 02_run_c302_network.ipynb`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD013 §9 — JupyterLab Interface](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#9-jupyterlab-interface-issue-347) and [DD001](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/) (c302 framework)
- **Depends On:** Issue 23
- **Existing Code to Reuse:**
    - `c302/examples/test/Comparison.ipynb` — Existing Jupyter notebook comparing c302 configurations (starting point)
- **Files to Modify:**
    - `notebooks/02_run_c302_network.ipynb` (new)
- **Test Commands:**
    - `jupyter nbconvert --execute notebooks/02_run_c302_network.ipynb`
- **Acceptance Criteria:**
    - [ ] Generates a c302 Level C1 network for the forward locomotion reference (FW)
    - [ ] Lists all 302 neurons with their classification (sensory, inter, motor)
    - [ ] Runs a short NEURON simulation (5ms)
    - [ ] Plots membrane potentials for selected neurons (AVBL, DB1, VB1, DD1, VD1)
    - [ ] Plots muscle calcium traces showing alternating dorsoventral activation
    - [ ] Visualizes the forward locomotion subcircuit (AVB → B-type → muscles, cross-inhibition)
    - [ ] Explains c302 levels (A, B, C, C1, C2, D) in markdown cells
    - [ ] Includes markdown explaining the circuit biology at undergraduate level
    - [ ] Runs to completion without errors
- **Sponsor Summary Hint:** An interactive guided tour of the virtual worm's brain. You generate the 302-neuron circuit, zoom into the forward locomotion pathway, and watch how command neurons (AVB) activate motor neurons (DB, VB) that drive muscles — while inhibitory neurons (DD, VD) create the alternating dorsal/ventral pattern needed for undulatory crawling. Different c302 "levels" add more biological detail — from simple connectivity (Level A) to full channel dynamics (Level D).

---

### Issue 25: Notebook: `03_analyze_output.ipynb`

- **Title:** `[DD013] Create starter notebook 03_analyze_output.ipynb`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD013 §9 — JupyterLab Interface](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#9-jupyterlab-interface-issue-347)
- **Depends On:** Issue 23
- **Files to Modify:**
    - `notebooks/03_analyze_output.ipynb` (new)
- **Test Commands:**
    - `jupyter nbconvert --execute notebooks/03_analyze_output.ipynb`
- **Acceptance Criteria:**
    - [ ] Loads simulation output from `./output/` directory
    - [ ] Plots neural activity traces (membrane potentials, calcium)
    - [ ] Plots body movement trajectory from WCON file
    - [ ] Shows energy consumption over time
    - [ ] Includes markdown explaining what each plot means biologically
    - [ ] Runs to completion (requires output from a prior simulation run)
- **Sponsor Summary Hint:** After running a simulation, this notebook helps you understand the results. Each plot tells a biological story: membrane potentials show when neurons fire, calcium traces show muscle activation, and the WCON trajectory shows how the virtual worm actually moved through space.

---

### Issue 26: Notebook: `04_validate_against_data.ipynb`

- **Title:** `[DD013] Create starter notebook 04_validate_against_data.ipynb`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD013 §9 — JupyterLab Interface](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#9-jupyterlab-interface-issue-347) and [DD010](https://docs.openworm.org/design_documents/DD010_Validation_Framework/)
- **Depends On:** Issue 23
- **Files to Modify:**
    - `notebooks/04_validate_against_data.ipynb` (new)
- **Test Commands:**
    - `jupyter nbconvert --execute notebooks/04_validate_against_data.ipynb`
- **Acceptance Criteria:**
    - [ ] Loads simulation output and experimental reference data
    - [ ] Runs Tier 1 validation comparison (simulated vs. recorded electrophysiology)
    - [ ] Plots side-by-side comparison of simulated vs. real worm movement
    - [ ] Computes and displays validation metrics (correlation, error)
    - [ ] Explains what "good" and "bad" validation looks like
    - [ ] Runs to completion (requires output from a prior simulation run)
- **Sponsor Summary Hint:** This notebook compares the virtual worm to the real worm. Does the simulated AVAL neuron fire at the right voltage? Does the virtual worm crawl at the right speed? Validation is how we know the simulation is doing science, not just computing. See [DD010](https://docs.openworm.org/design_documents/DD010_Validation_Framework/).

---

## Phase C: Subsystem Expansion (Weeks 9–16)

Target: New subsystems plug into the stack via config toggles.

---

### Issue 27: DD005 cell-type specialization hooks

- **Title:** `[DD013] Add DD005 cell-type specialization config hooks and subsystem init`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD005](https://docs.openworm.org/design_documents/DD005_Cell_Type_Differentiation_Strategy/) (Integration Contract) and [DD013 §1](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml) (`neural.differentiated` config)
- **Depends On:** Issue 9
- **Files to Modify:**
    - `openworm.yml` (verify `neural.differentiated` flag exists)
    - `master_openworm.py` (add conditional init for cell-type specialization)
- **Test Commands:**
    - `python3 master_openworm.py --config configs/differentiated.yml --dry-run`
- **Acceptance Criteria:**
    - [ ] `neural.differentiated: true` triggers CeNGEN-based cell-type specialization in c302
    - [ ] `neural.differentiated: false` uses current behavior (302 identical neurons)
    - [ ] Placeholder integration code in `master_openworm.py` with clear TODO markers for DD005 implementation
    - [ ] Config documented with reference to DD005
- **Sponsor Summary Hint:** In reality, the worm's 302 neurons aren't identical — they come in 128 distinct types with different gene expression profiles (from the CeNGEN atlas). [DD005](https://docs.openworm.org/design_documents/DD005_Cell_Type_Differentiation_Strategy/) defines how to differentiate them. This issue adds the config toggle and initialization hook so the simulation can switch between "all neurons identical" and "128 types" mode.

---

### Issue 28: DD004 mechanical cell identity

- **Title:** `[DD013] Add DD004 mechanical cell identity integration for Sibernetic particles`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python
- **DD Section to Read:** [DD004](https://docs.openworm.org/design_documents/DD004_Mechanical_Cell_Identity/) (Integration Contract) and [DD013 §5](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 4b, `body/cell_ids` in OME-Zarr)
- **Depends On:** Issue 19
- **Files to Modify:**
    - Sibernetic particle output code (add cell ID tags)
    - `master_openworm.py` (export `body/cell_ids` to OME-Zarr)
- **Test Commands:**
    - `python3 -c "import zarr; z = zarr.open('output/openworm.zarr'); print('cell_ids' in z['body'])"`
- **Acceptance Criteria:**
    - [ ] Sibernetic particles tagged with cell identity (muscle, hypodermis, cuticle, etc.)
    - [ ] `body.cell_identity: true` config flag activates tagging
    - [ ] Cell IDs exported to `body/cell_ids` array in OME-Zarr
    - [ ] Viewer can color-code particles by cell type
- **Sponsor Summary Hint:** The worm's body isn't homogeneous — it has muscles, skin (hypodermis), a tough outer layer (cuticle), and internal organs, each with different mechanical properties. [DD004](https://docs.openworm.org/design_documents/DD004_Mechanical_Cell_Identity/) tags each simulated particle with its cell type. This issue wires that into the OME-Zarr data bus so the viewer can display cells in different colors.

---

### Issue 29: DD006 neuropeptide integration

- **Title:** `[DD013] Add DD006 neuropeptide modulation coupling to simulation loop`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302` + `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD006](https://docs.openworm.org/design_documents/DD006_Neuropeptidergic_Connectome_Integration/) (Integration Contract) and [DD013 §5](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#5-enhanced-master_openwormpy-implement-all-5-steps) (Step 3, coupling)
- **Depends On:** Issue 11
- **Files to Modify:**
    - `master_openworm.py` (neuropeptide coupling in simulation loop)
    - c302 neuropeptide module (GPCR modulation equations)
    - `openworm.yml` (`neural.neuropeptides` section)
- **Test Commands:**
    - `docker compose run simulation` with `neural.neuropeptides: true`
    - `python3 -c "import zarr; z = zarr.open('output/openworm.zarr'); print('concentrations' in z['neuropeptides'])"`
- **Acceptance Criteria:**
    - [ ] Neuropeptide modulation runs in the coupled simulation loop when `neural.neuropeptides: true`
    - [ ] Peptide concentration fields computed and exchanged with neural subsystem each coupling step
    - [ ] GPCR modulation affects synaptic weights per [DD006](https://docs.openworm.org/design_documents/DD006_Neuropeptidergic_Connectome_Integration/) equations
    - [ ] `neuropeptides/concentrations` exported to OME-Zarr
    - [ ] Simulation still runs correctly when `neural.neuropeptides: false`
- **Sponsor Summary Hint:** Beyond fast electrical synapses, worm neurons also communicate via neuropeptides — small signaling molecules that diffuse between cells and modulate behavior over longer timescales. [DD006](https://docs.openworm.org/design_documents/DD006_Neuropeptidergic_Connectome_Integration/) defines 31,479 peptide-receptor interactions. This issue integrates that slow signaling layer into the simulation loop alongside the fast neural circuit.

---

### Issue 30: DD007 pharynx model integration

- **Title:** `[DD013] Add DD007 pharyngeal nervous system integration to simulation stack`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** New pharynx repo + `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD007](https://docs.openworm.org/design_documents/DD007_Pharyngeal_Nervous_System_Architecture/) (Integration Contract) and [DD013 §7](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#7-contributor-development-workflow) (adding new subsystem workflow)
- **Depends On:** Issue 11
- **Files to Modify:**
    - New repo: pharynx model code
    - `Dockerfile` (add pharynx Docker stage)
    - `docker-compose.yml` (pharynx service if needed)
    - `master_openworm.py` (pharynx init + coupling in loop)
    - `openworm.yml` (pharynx section already present as `enabled: false`)
    - `versions.lock` (add pharynx repo entry)
- **Test Commands:**
    - `docker compose run simulation` with `pharynx.enabled: true`
    - Verify pumping frequency ~3.5 Hz in output
- **Acceptance Criteria:**
    - [ ] Pharynx model repo created with basic 20-neuron circuit
    - [ ] Docker stage added for pharynx dependencies
    - [ ] `pharynx.enabled: true` activates pharynx in simulation loop
    - [ ] Pharynx neural activity coupled to main nervous system via RIP interneurons
    - [ ] Pumping events exported to `pharynx/pumping_state` in OME-Zarr
    - [ ] `pharynx.pumping_frequency_target` used for validation
- **Sponsor Summary Hint:** The pharynx is the worm's feeding organ — a muscular pump with its own 20-neuron nervous system that operates semi-independently from the rest of the body. It pumps bacteria at ~3.5 Hz. [DD007](https://docs.openworm.org/design_documents/DD007_Pharyngeal_Nervous_System_Architecture/) specifies its architecture. This issue creates the repo, builds the Docker stage, and wires it into the simulation loop.

---

### Issue 31: DD009 intestine model integration

- **Title:** `[DD013] Add DD009 intestinal oscillator model integration to simulation stack`
- **Labels:** `DD013`, `human-expert`, `L3`
- **Target Repo:** New intestine repo + `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD009](https://docs.openworm.org/design_documents/DD009_Intestinal_Oscillator_Model/) (Integration Contract) and [DD013 §7](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#7-contributor-development-workflow) (adding new subsystem workflow)
- **Depends On:** Issue 11
- **Files to Modify:**
    - New repo: intestine model code
    - `Dockerfile` (add intestine Docker stage)
    - `master_openworm.py` (intestine init + coupling in loop)
    - `openworm.yml` (intestine section already present as `enabled: false`)
    - `versions.lock` (add intestine repo entry)
- **Test Commands:**
    - `docker compose run simulation` with `intestine.enabled: true`
    - Verify oscillation period ~50s in output
- **Acceptance Criteria:**
    - [ ] Intestine model repo created with 20-cell calcium oscillator
    - [ ] Docker stage added for intestine dependencies
    - [ ] `intestine.enabled: true` activates intestine in simulation loop
    - [ ] Calcium wave propagation across 20 intestinal cells
    - [ ] `intestine/calcium` and `intestine/defecation_events` exported to OME-Zarr
    - [ ] `intestine.oscillator_period_target` used for validation
- **Sponsor Summary Hint:** The worm's intestine generates rhythmic calcium waves (~50-second period) that drive the defecation motor program — one of the most regular biological clocks in nature. [DD009](https://docs.openworm.org/design_documents/DD009_Intestinal_Oscillator_Model/) specifies the 20-cell oscillator model. This issue creates the repo, Docker stage, and simulation coupling.

---

## Phase D: Polish & Onboarding (Weeks 17–20)

Target: A newcomer can experience the full simulation in a browser via MyBinder, then progress to local Docker for development.

---

### Issue 32: Write getting-started guide

- **Title:** `[DD013] Write getting-started guide for new contributors`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD013 §7 — Contributor Development Workflow](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#7-contributor-development-workflow) and [DD013 Quality Criteria](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#quality-criteria) (criterion 8: clone-to-simulation in <30 min)
- **Depends On:** Issue 4, Issue 12
- **Files to Modify:**
    - `GETTING_STARTED.md` (new)
    - `README.md` (update to link to getting-started guide)
- **Test Commands:**
    - Follow the guide on a clean machine with only Docker installed
- **Acceptance Criteria:**
    - [ ] Step-by-step instructions from `git clone` to running simulation
    - [ ] Covers: clone repo, `docker compose run quick-test`, inspect output, make a change, re-test
    - [ ] Time estimate <30 minutes (using pre-built Docker image pull)
    - [ ] Troubleshooting section for common issues (Docker not running, port conflicts, etc.)
    - [ ] Links to JupyterLab notebooks for deeper exploration
    - [ ] Links to DD013 for architecture understanding
- **Sponsor Summary Hint:** The first document a new contributor reads. It must get them from zero to running simulation in under 30 minutes. This is the "front door" to OpenWorm — if it's confusing or broken, we lose contributors before they even start.

---

### Issue 33: MyBinder.org integration

- **Title:** `[DD013] Configure MyBinder.org for zero-install browser-based simulation demo`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD013 Phase D](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#phase-d-polish-and-onboarding-weeks-17-20) and [DD013 Open Questions](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#open-questions-require-founder-input) (question 3)
- **Depends On:** Issue 23
- **Files to Modify:**
    - `binder/` directory (new — Binder config files: `Dockerfile`, `postBuild`, `start`)
    - `README.md` (add "Launch on Binder" badge)
- **Test Commands:**
    - Visit `https://mybinder.org/v2/gh/openworm/OpenWorm/main` and verify JupyterLab launches
- **Acceptance Criteria:**
    - [ ] MyBinder configuration in `binder/` directory
    - [ ] Launches JupyterLab with starter notebooks pre-loaded
    - [ ] Can run `02_run_c302_network.ipynb` within Binder resource limits
    - [ ] README.md has "Launch on Binder" badge
    - [ ] Binder environment includes c302, cect, matplotlib, numpy
- **Sponsor Summary Hint:** MyBinder lets anyone experience the simulation in their browser with zero installation — just click a badge in the README. It's how we lower the barrier to entry from "install Docker + clone repo" to "click a link." Perfect for curious scientists, students, and potential contributors who want to explore before committing.

---

### Issue 34: Automate Docker Hub publishing

- **Title:** `[DD013] Create GitHub Actions workflow for automated Docker Hub image publishing`
- **Labels:** `DD013`, `ai-workable`, `L2`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** ci-cd, docker
- **DD Section to Read:** [DD013 §8 — Pre-Built Images](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#8-pre-built-images-on-docker-hub) and [DD013 Phase D](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#phase-d-polish-and-onboarding-weeks-17-20)
- **Depends On:** None
- **Files to Modify:**
    - `.github/workflows/publish.yml` (new)
- **Test Commands:**
    - Create a test release tag and verify image appears on Docker Hub
- **Acceptance Criteria:**
    - [ ] Triggers on GitHub release (tag creation)
    - [ ] Builds multi-stage Dockerfile
    - [ ] Pushes `openworm/openworm:<tag>` and `openworm/openworm:latest` to Docker Hub
    - [ ] Uses GitHub Secrets for Docker Hub credentials
    - [ ] Build cache for faster publishes
    - [ ] Publishes both `full` and `viewer` images
- **Sponsor Summary Hint:** Most users just want to run the simulation, not build it from source. Automated Docker Hub publishing means every release automatically produces a pre-built image. `docker pull openworm/openworm:0.10.0` and you're running in seconds instead of building for 20 minutes.

---

### Issue 35: Update N2-Whisperer orientation tasks

- **Title:** `[DD013] Update N2-Whisperer orientation tasks for new simulation stack`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD013 Phase D](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#phase-d-polish-and-onboarding-weeks-17-20) and [DD011](https://docs.openworm.org/design_documents/DD011_Contributor_Progression_Model/) (L0→L1 orientation tasks)
- **Depends On:** Issue 32
- **Files to Modify:**
    - `n2_whisperer_orientation_tasks.md` (update references to new Docker workflow)
- **Test Commands:**
    - Review that orientation tasks reference `docker compose` commands (not legacy `run.sh`)
- **Acceptance Criteria:**
    - [ ] L0 Task B1 ("Install and run Docker simulation") updated to use `docker compose run quick-test`
    - [ ] References to legacy `run.sh` / `build.sh` replaced with docker-compose commands
    - [ ] JupyterLab notebooks referenced as exploration tasks
    - [ ] Getting-started guide linked
    - [ ] Tasks achievable within the new stack architecture
- **Sponsor Summary Hint:** N2-Whisperer is the AI onboarding assistant that guides new contributors through their first tasks. This issue updates its task list to match the new Docker Compose workflow — so newcomers learn the current way of running simulations, not the legacy shell scripts.

---

## Infrastructure (Cross-Phase)

---

### Issue 36: Survey `sibernetic_config_gen` for reuse

- **Title:** `[DD013] Survey sibernetic_config_gen repo for reusable particle config generation code`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, git
- **DD Section to Read:** [DD013 Existing Code Resources](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#existing-code-resources) (sibernetic_config_gen section)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary comment on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Clone and inspect [openworm/sibernetic_config_gen](https://github.com/openworm/sibernetic_config_gen)
    - [ ] Document: What does it generate? (particle positions, `.ini` config files)
    - [ ] Document: What resolution/body configurations are available?
    - [ ] Document: Is it compatible with current Sibernetic version?
    - [ ] Document: What code can be reused for `openworm.yml` → Sibernetic `.ini` translation?
    - [ ] Estimate time savings if reused vs. rewriting
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** This dormant 2016 repo generates the initial particle positions for Sibernetic — like placing ~100,000 water droplets in the shape of a worm before the simulation starts. If the code still works, it saves 10-20 hours of reimplementation. Surveying before building is good engineering practice.

---

### Issue 37: Survey `skeletonExtraction` for reuse

- **Title:** `[DD013] Survey skeletonExtraction repo for reusable skeleton export code`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, git
- **DD Section to Read:** [DD013 Existing Code Resources](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#existing-code-resources) (skeletonExtraction section) and [DD021](https://docs.openworm.org/design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy/) (WCON export)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary comment on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Clone and inspect [openworm/skeletonExtraction](https://github.com/openworm/skeletonExtraction)
    - [ ] Document: What does it extract? (49-point skeleton/centerline from SPH particles)
    - [ ] Document: Output format (COLLADA, coordinates)
    - [ ] Document: Is it compatible with current Sibernetic output format?
    - [ ] Document: Can the skeleton extraction algorithm be used for SPH → WCON export pipeline?
    - [ ] Estimate time savings if reused vs. rewriting
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** This 2016 repo extracts the worm's centerline (a 49-point skeleton) from the cloud of ~100,000 Sibernetic particles — like finding the backbone inside a blob. This skeleton is essential for converting simulation output to WCON format (the standard for worm movement data) which [DD021](https://docs.openworm.org/design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy/) needs for validation. Saves 15-25 hours if reusable.

---

### Issue 38: Survey `sibernetic_NEURON` for reuse

- **Title:** `[DD013] Survey sibernetic_NEURON repo for Sibernetic-NEURON interface patterns`
- **Labels:** `DD013`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, git
- **DD Section to Read:** [DD013 Existing Code Resources](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#existing-code-resources) (sibernetic_NEURON section) and [DD019](https://docs.openworm.org/design_documents/DD019_Closed_Loop_Touch_Response/) (bidirectional coupling)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary comment on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Clone and inspect [openworm/sibernetic_NEURON](https://github.com/openworm/sibernetic_NEURON)
    - [ ] Document: What interface pattern does it use between Sibernetic and NEURON?
    - [ ] Document: How does it differ from current `sibernetic_c302.py`?
    - [ ] Document: Are there bidirectional coupling patterns applicable to DD019 (closed-loop touch response)?
    - [ ] Document: Is any code directly reusable?
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** Before `sibernetic_c302.py` (the current coupling code), there was `sibernetic_NEURON` — an earlier attempt at connecting the body physics engine to the neural simulator. Reviewing it may reveal useful patterns for implementing bidirectional sensory feedback (touch → neural response → movement change) as specified in [DD019](https://docs.openworm.org/design_documents/DD019_Closed_Loop_Touch_Response/).

---

## Backend Stabilization (Cross-Phase, DD003)

Target: Achieve result parity with OpenCL on PyTorch/Taichi backends before OpenCL becomes unusable.

---

### Issue 39: Create cross-backend parity test suite

- **Title:** `[DD003] Create cross-backend parity test suite against OpenCL baseline`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Cross-Backend Parity Requirements](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#cross-backend-parity-requirements)
- **Depends On:** DD003 Issues 1–2 (stability validation scripts)
- **Files to Modify:**
    - `scripts/backend_parity_test.py` (new)
    - `tests/baseline/` (new — OpenCL baseline metric files)
- **Test Commands:**
    - `python3 scripts/backend_parity_test.py --backend opencl --save-baseline`
    - `python3 scripts/backend_parity_test.py --backend pytorch --compare-baseline tests/baseline/`
- **Acceptance Criteria:**
    - [ ] Runs 4 test scenarios: drop test, elastic deformation, muscle contraction, full worm crawl
    - [ ] Each test produces numeric metrics (position means, velocity stats, curvature)
    - [ ] `--save-baseline` mode saves OpenCL metrics to reference files
    - [ ] `--compare-baseline` mode compares another backend's metrics against saved baseline
    - [ ] Reports per-metric deviation; ±5% = PASS, >5% = FAIL
    - [ ] Summary report shows which tests passed/failed for each backend
- **Sponsor Summary Hint:** This is the automated comparison tool that tells us whether PyTorch or Taichi produce the same physics as OpenCL. It runs four standard simulation scenarios on each backend and compares the numeric outputs. A backend must pass all four within ±5% of OpenCL to graduate from Experimental to Stable.

---

### Issue 40: Fix Taichi elastic coordinate-space bug

- **Title:** `[DD003] Fix Taichi elastic coordinate-space bug`
- **Labels:** `DD003`, `human-expert`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — The Taichi Coordinate-Space Bug](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#the-taichi-coordinate-space-bug)
- **Depends On:** Issue 39
- **Files to Modify:**
    - `taichi_backend/sph_metal.py` (elastic force calculation)
    - `taichi_backend/sph_cuda.py` (elastic force calculation, if separate)
- **Test Commands:**
    - `python3 scripts/backend_parity_test.py --backend taichi-metal --compare-baseline tests/baseline/`
    - Verify elastic body mean Y > 1.0 after 3s floor collision (vs current 0.24)
- **Acceptance Criteria:**
    - [ ] Remove incorrect `/sim_scale` division in elastic force calculation
    - [ ] Add `simulationScaleInv` to the integration step
    - [ ] Use `h_scaled` for kernel coefficients instead of unscaled `h`
    - [ ] Taichi elastic body mean Y > 1.0 after 3s floor collision (currently 0.24)
    - [ ] Taichi elastic deformation test passes parity suite (within ±5% of OpenCL)
    - [ ] No regressions in liquid particle behavior
- **Sponsor Summary Hint:** The Taichi backend has a known bug where elastic forces are computed in the wrong coordinate space — making them ~287x too weak. Elastic bodies (like the worm's skin) flatten to the floor instead of maintaining shape. The fix is documented (3 specific code changes) but hasn't been applied yet. This is the single biggest blocker for Taichi becoming usable.

---

### Issue 41: Audit and fix PyTorch/Taichi result quality gap vs OpenCL

- **Title:** `[DD003] Audit and fix PyTorch/Taichi result quality gap vs OpenCL`
- **Labels:** `DD003`, `human-expert`, `L3`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics, sph
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — The Result Quality Gap](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#the-result-quality-gap)
- **Depends On:** Issue 39, Issue 40
- **Files to Modify:**
    - `taichi_backend/sph_metal.py` (kernel implementations)
    - `pytorch_solver.py` (kernel implementations)
    - Possibly other solver files
- **Test Commands:**
    - `python3 scripts/backend_parity_test.py --backend pytorch --compare-baseline tests/baseline/`
    - `python3 scripts/backend_parity_test.py --backend taichi-metal --compare-baseline tests/baseline/`
- **Acceptance Criteria:**
    - [ ] Line-by-line audit of PyTorch/Taichi kernel implementations against OpenCL `sphFluid.cl`
    - [ ] Documented list of algorithmic differences found
    - [ ] Fixes applied to bring implementations into alignment
    - [ ] Parity test suite passes within ±5% of OpenCL on all 4 test scenarios for at least one Python backend
    - [ ] Audit findings documented in a report (posted on the issue)
- **Sponsor Summary Hint:** Even after fixing the Taichi coordinate bug, neither Python backend produces physics matching the C++/OpenCL reference. This is the detective work — going through ~64KB of OpenCL kernel code line by line to find where PyTorch and Taichi diverge. Could be numerical precision, algorithm differences, or missing terms. This is the hardest issue in the stabilization sequence but also the most impactful.

---

### Issue 42: Graduate backends to Stable/Production and add to Dockerfile

- **Title:** `[DD003] Graduate backends to Stable/Production and add to Dockerfile`
- **Labels:** `DD003`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic` + `openworm/OpenWorm`
- **Required Capabilities:** docker, ci-cd
- **DD Section to Read:** [DD003 Backend Stabilization Roadmap — Backend Graduation Criteria](https://docs.openworm.org/design_documents/DD003_Body_Physics_Architecture/#backend-graduation-criteria)
- **Depends On:** Issue 41
- **Files to Modify:**
    - `Dockerfile` (body stage — add `pip install taichi torch` conditional)
    - `.github/workflows/integration.yml` (add backend-specific CI gates)
    - DD003 Backend Status table (update status based on graduation results)
- **Test Commands:**
    - `docker compose run simulation` with `body.backend: pytorch`
    - `docker compose run simulation` with `body.backend: taichi-metal` (on Apple Silicon)
    - CI passes with multi-backend smoke tests
- **Acceptance Criteria:**
    - [ ] Backends that pass parity tests upgraded to Stable in DD003 status table
    - [ ] `pip install taichi torch` added to Dockerfile body stage (conditional on backend)
    - [ ] CI runs smoke test on at least OpenCL + one Python backend
    - [ ] Performance benchmark results documented for each graduated backend
    - [ ] DD003 Compute Backends table updated with final status
    - [ ] Recommendation updated based on actual benchmark results
- **Sponsor Summary Hint:** The final step in the stabilization sequence — once backends pass the parity tests, they graduate from Experimental to Stable/Production. This means adding them to the Docker image so any contributor can use them, and adding CI gates so regressions are caught automatically. The goal is that Apple Silicon users can run Taichi Metal, NVIDIA users can run CUDA, and everyone has a working backend.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 42 |
| **ai-workable** | 31 |
| **human-expert** | 11 |
| **L1** | 17 |
| **L2** | 15 |
| **L3** | 9 |
| **DD003 label** | 4 |

| Phase | Issues | Target |
|-------|--------|--------|
| **A: Foundation** | 1–17 | `docker compose run quick-test` works |
| **B: Validation** | 18–26 | PRs auto-validated, JupyterLab available |
| **C: Subsystem Expansion** | 27–31 | New organs plug in via config toggles |
| **D: Polish & Onboarding** | 32–35 | Clone-to-simulation in <30 min |
| **Infrastructure** | 36–38 | Dormant repo surveys for reuse |
| **Backend Stabilization** | 39–42 | PyTorch/Taichi match OpenCL result quality |

### Dependency Graph (Critical Path)

```
Issue 1 (config schema)
  ├→ Issue 2 (validation script)
  ├→ Issue 3 (Dockerfile) → Issue 4 (docker-compose)
  │    ├→ Issue 5 (viewer service)
  │    ├→ Issue 6 (neural-dev service)
  │    ├→ Issue 12 (quick-test.sh) → Issue 14 (CI Gate 2)
  │    ├→ Issue 23 (JupyterLab) → Issues 24-26 (notebooks)
  │    │                         → Issue 33 (MyBinder)
  │    └→ Issue 32 (getting-started) → Issue 35 (N2-Whisperer update)
  ├→ Issue 13 (CI Gate 1) → Issue 14 (CI Gate 2)
  ├→ Issue 17 (apt pin + venv)
  └→ Issue 9 (config loading)
       → Issue 10 (subsystem init) → Issue 11 (coupled loop)
            ├→ Issue 18 (output gen) → Issue 19 (OME-Zarr)
            │    └→ Issue 20 (validation) → Issue 21 (CI Gate 3) → Issue 22 (CI Gate 4)
            │                              → Issue 28 (DD004 cell identity)
            ├→ Issue 27 (DD005 cell-type specialization)
            ├→ Issue 29 (DD006 neuropeptides)
            ├→ Issue 30 (DD007 pharynx)
            └→ Issue 31 (DD009 intestine)

Issue 7 (versions.lock) → Issue 8 (build.sh)

Issues 15, 16 (bug fixes) — independent
Issues 34 (Docker Hub) — independent
Issues 36, 37, 38 (surveys) — independent

DD003 Issues 1-2 (stability scripts) → Issue 39 (parity test suite)
  → Issue 40 (Taichi coordinate bug) → Issue 41 (quality gap audit)
    → Issue 42 (graduate backends + Dockerfile)
```
