# DD013: Simulation Stack Architecture (The Integration Backbone)

- **Status:** Proposed
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-15
- **Supersedes:** Informal Docker meta-repo approach
- **Related:** [DD001](DD001_Neural_Circuit_Architecture.md)–[DD010](DD010_Validation_Framework.md) (all technical subsystems), [DD011](DD011_Contributor_Progression_Model.md) (Contributor Progression), [DD012](DD012_Design_Document_RFC_Process.md) (RFC Process)

---

> **Phase:** [Infrastructure Bootstrap](DD_PHASE_ROADMAP.md#phase-a-infrastructure-bootstrap-weeks-1-4) | **Layer:** Integration

## TL;DR

The OpenWorm simulation stack uses Docker Compose to orchestrate five containerized subsystems (neural, muscle, body physics, sensory, visualization) with a shared OME-Zarr data bus. Every contributor runs the same environment via `docker compose up`, ensuring reproducibility from laptop to CI server. This DD replaces the current monolithic Dockerfile and shell-script approach with a multi-stage Docker build, a declarative `openworm.yml` configuration system, dependency pinning via `versions.lock`, and automated CI/CD validation gates.

## Context

### The Gap Between Vision and Execution

Design Documents [DD001](DD001_Neural_Circuit_Architecture.md)-[DD012](DD012_Design_Document_RFC_Process.md) specify a rich, multi-tissue, multi-scale organism simulation:

| Subsystem | DD | Primary Repo | Integration Status |
|-----------|----|--------------|--------------------|
| Neural circuit (c302) | [DD001](DD001_Neural_Circuit_Architecture.md) | `openworm/c302` | **Working** — runs via NEURON |
| Muscle model | [DD002](DD002_Muscle_Model_Architecture.md) | `openworm/c302` + `openworm/muscle_model` | **Working** — coupled to c302 |
| Body physics (Sibernetic) | [DD003](DD003_Body_Physics_Architecture.md) | `openworm/sibernetic` | **Working** — coupled to c302 via `sibernetic_c302.py` |
| Mechanical cell identity | [DD004](DD004_Mechanical_Cell_Identity.md) | `openworm/sibernetic` (future) | **Not started** |
| Cell-type specialization | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | `openworm/c302` (future) | **Not started** |
| Neuropeptides | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | `openworm/c302` (future) | **Not started** |
| Pharynx | [DD007](DD007_Pharyngeal_System_Architecture.md) | New repo TBD | **Not started** |
| Data integration (OWMeta) | [DD008](DD008_Data_Integration_Pipeline.md) | `openworm/owmeta` | **Dormant** (last real commit Jul 2024) |
| Intestinal oscillator | [DD009](DD009_Intestinal_Oscillator_Model.md) | New repo TBD | **Not started** |
| Validation framework | [DD010](DD010_Validation_Framework.md), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | `openworm/open-worm-analysis-toolbox` + `openworm/tracker-commons` | **Dormant** (last commit Jan 2020) — [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival plan |

The `openworm/OpenWorm` meta-repository is the only place where these subsystems come together as a runnable simulation. **It is the architectural backbone of the entire project.** And right now, it consists of:

- One Dockerfile
- One Python script (`master_openworm.py`) with 3 of 5 steps unimplemented
- Four shell scripts (`build.sh`, `run.sh`, `run-quick.sh`, `stop.sh`)
- No configuration system
- No dependency pinning beyond branch names
- No automated validation
- No docker-compose
- One active maintainer (Neural Circuit L4)

### What Actually Runs Today

The current simulation pipeline (v0.9.7) executes Step 3 of `master_openworm.py`:

```
1. Build Docker image (ubuntu:24.04 + NEURON 8.2.6 + c302 @ ow-0.9.7 + Sibernetic @ ow-0.9.7 + AMD OpenCL SDK)
2. Launch container with X11 forwarding and GPU passthrough
3. Execute sibernetic_c302.py:
   a. c302 generates NeuroML network (Level C2, "FW" reference)
   b. NEURON simulates neural activity
   c. Sibernetic simulates body physics driven by neural output
   d. Both run in a coupled loop for 15ms (default)
4. Record video via xvfb + tmux + ffmpeg screen capture
5. Copy outputs (PNGs, WCON, MP4) to shared volume
```

Steps 1, 2, 4, and 5 of `master_openworm.py` are stubs ("Not yet implemented"):

- Step 1: Rebuild c302 from latest OWMeta
- Step 2: Execute unit tests
- Step 4: Movement analysis
- Step 5: Report on movement analysis fit

### Known Critical Issues

| Issue | Impact | GitHub # | Status |
|-------|--------|----------|--------|
| **Memory leak in plotting/video** | OOM kills simulations >2s; 5s sim needs 64GB RAM | #332, #341 | Unfixed |
| **No GPU in Docker** | OpenCL runs on CPU only; 10× slower than necessary | #320 | Open since 2021 |
| **External dependency downloads** | AMD SDK from SourceForge; build can break any time | — | Fragile |
| **No dependency pinning** | apt packages unpinned; c302/Sibernetic pinned to branch name, not commit | #317 | Open since 2021 |
| **No virtualenv** | `pip install --break-system-packages` | #314 | Open since 2021 |
| **Fragile video pipeline** | xvfb + tmux + ffmpeg screen capture chain | #315, #268 | Open |
| **No docker-compose** | Raw `docker run` in shell scripts | — | Never addressed |

### The Contributor Experience Today

A contributor who wants to test a change against the full simulation must:

1. Fork the relevant repo (e.g., `c302`)
2. Make their change
3. Modify the Dockerfile to point `git clone` at their fork/branch
4. Build the entire Docker image from scratch (~20 minutes)
5. Run the simulation (~10 minutes for 15ms)
6. Manually inspect output (PNGs, video)
7. No automated validation — must visually compare

**This is why most contributors work on subsystems in isolation and never see how their work affects the whole organism.**

### The Scale of What's Coming

The [Whole-Organism Modeling Proposal](DD_PHASE_ROADMAP.md) (Phases 1-6) will expand the simulation from:

- **302 identical neurons + body wall muscles + fluid body** →
- **128 differentiated neuron types + neuropeptides + pharynx (63 cells) + intestine (20 cells) + mechanical cell identity + intercellular signaling**

This means:

- More repos to integrate (pharynx model, intestinal oscillator, neuropeptide layer)
- More configuration knobs (which tissues enabled, which c302 level, which backend)
- More validation targets (Tier 1, 2, 3 across multiple tissues)
- More contributors touching different subsystems simultaneously
- More compute requirements (longer simulations, more particles, more neurons)

**The current meta-repo architecture cannot support this growth.**

---

## Deliverables

- `docker-compose.yml` — orchestration of all simulation containers (quick-test, simulation, validate, viewer, shell services)
- `Dockerfile` (multi-stage) — per-subsystem container definitions (base, neural, body, validation, full, viewer stages)
- `versions.lock` — pinned dependency versions (exact commit hashes) across all subsystems
- `openworm.yml` — unified declarative configuration file for simulation parameters
- `master_openworm.py` (enhanced) — orchestrator implementing all 5 pipeline steps driven by config
- `.github/workflows/integration.yml` — CI/CD pipeline with build, smoke test, and validation gates
- `scripts/quick-test.sh` — contributor smoke test `[TO BE CREATED]`
- Starter Jupyter notebooks (4) — orientation and exploration notebooks for newcomers `[TO BE CREATED]`

---

## Decision

### 1. Simulation Configuration System (`openworm.yml`)

Replace hardcoded defaults in `master_openworm.py` with a declarative YAML configuration file that specifies exactly what to simulate.

```yaml
# openworm.yml — Simulation Configuration
# This file lives in the OpenWorm meta-repo root.
# Contributors copy and modify for their experiments.

version: "0.10.0"

# === Neural Subsystem ([DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) ===
neural:
  enabled: true
  framework: c302
  level: C1                          # A, B, C, C1, C2, D
  differentiated: false              # Phase 1: CeNGEN cell-type specialization ([DD005](DD005_Cell_Type_Differentiation_Strategy.md))
  neuropeptides: false               # Phase 2: peptidergic modulation ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md))
  connectome_dataset: "Cook2019"     # Cook2019, Witvliet2021, Varshney2011
  data_reader: "UpdatedSpreadsheetDataReader2"
  reference: "FW"                    # FW (forward crawl), BA (backward), TU (turning)

# === Body Physics ([DD003](DD003_Body_Physics_Architecture.md), [DD004](DD004_Mechanical_Cell_Identity.md)) ===
body:
  enabled: true
  engine: sibernetic
  backend: opencl                    # opencl (production), pytorch (testing), taichi-metal (experimental), taichi-cuda (experimental)
  configuration: "worm_crawl_half_resolution"
  particle_count: 100000             # ~100K for standard, ~25K for quick
  cell_identity: false               # Phase 4: tagged particles ([DD004](DD004_Mechanical_Cell_Identity.md))
  timestep: 0.00002                  # seconds

# === Muscle Model ([DD002](DD002_Muscle_Model_Architecture.md)) ===
muscle:
  enabled: true                      # Requires neural.enabled
  calcium_coupling: true             # Ca²⁺ → force pipeline

# === Pharynx ([DD007](DD007_Pharyngeal_System_Architecture.md)) — Phase 3 ===
pharynx:
  enabled: false
  pumping_frequency_target: 3.5      # Hz

# === Intestine ([DD009](DD009_Intestinal_Oscillator_Model.md)) — Phase 3 ===
intestine:
  enabled: false
  oscillator_period_target: 50.0     # seconds

# === Simulation Parameters ===
simulation:
  duration: 15.0                     # milliseconds
  dt_neuron: 0.05                    # ms (NEURON timestep)
  dt_coupling: 0.005                 # ms (neural↔body coupling interval)
  output_interval: 100               # steps between output frames

# === Validation ([DD010](DD010_Validation_Framework.md)) ===
validation:
  run_after_simulation: false        # Set true for CI
  tier1_electrophysiology: false     # Single-cell validation
  tier2_functional_connectivity: false  # Circuit-level (requires 60s sim)
  tier3_behavioral: false            # Movement kinematics (requires ~5s sim)

# === Output ===
output:
  directory: "./output"
  video: true
  plots: true
  wcon: true                         # WCON movement file
  raw_data: false                    # Full simulation state dumps

# === Visualization ([DD014](DD014_Dynamic_Visualization_Architecture.md)) ===
visualization:
  enabled: true                      # Export OME-Zarr for viewer
  export_format: "zarr"              # "zarr" (OME-Zarr, recommended) or "legacy" (position_buffer.txt)
  surface_reconstruction: true       # Marching cubes → smooth body surface mesh
  export_interval: 10                # Timesteps between Zarr frames (every 10th output frame)

viewer:
  enabled: false                     # Launch Trame viewer after simulation
  port: 8501                         # Viewer port
  backend: "trame"                   # "trame" (Phase 1) or "threejs" (Phase 2+)
  default_layers:                    # Layers visible on startup
    - body_surface
    - muscles
```

**Why this matters:**

- Contributors can toggle subsystems on/off to test specific changes
- CI can run different configurations (quick smoke test vs. full validation)
- New subsystems (pharynx, intestine) plug in by adding a config section
- The configuration file is self-documenting (comments explain every option)
- Experiment reproducibility: commit the config file alongside results

### 2. Multi-Stage Docker Build (Layered Images)

Replace the monolithic Dockerfile with a multi-stage build that separates concerns:

```dockerfile
# === Stage 0: Base Environment ===
# System packages, Python, NEURON, build tools
# Rebuilt rarely (only when system deps change)
FROM ubuntu:24.04 AS base
# ... system packages, Python 3, pip, virtualenv ...
RUN pip install neuron==8.2.6

# === Stage 1: Subsystem — c302 (Neural Circuit) ===
FROM base AS neural
ARG C302_REF=ow-0.10.0
RUN git clone --branch $C302_REF --depth 1 \
    https://github.com/openworm/c302.git /opt/openworm/c302
RUN pip install -e /opt/openworm/c302

# === Stage 2: Subsystem — Sibernetic (Body Physics) ===
FROM base AS body
ARG SIBERNETIC_REF=ow-0.10.0
RUN git clone --branch $SIBERNETIC_REF --depth 1 \
    https://github.com/openworm/sibernetic.git /opt/openworm/sibernetic
# OpenCL SDK + build
RUN cd /opt/openworm/sibernetic && mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)
# NOTE: Taichi/PyTorch backends require additional dependencies:
#   pip install taichi torch
# These should be installed conditionally based on body.backend config.
# See DD003 Backend Stabilization Roadmap for when Taichi will be Dockerfile-ready.

# === Stage 3: Subsystem — Validation Tools ([DD010](DD010_Validation_Framework.md)) ===
FROM base AS validation
RUN git clone --depth 1 \
    https://github.com/openworm/open-worm-analysis-toolbox.git \
    /opt/openworm/validation
RUN pip install -e /opt/openworm/validation

# === Stage 4: Integration (Full Stack) ===
FROM base AS full
COPY --from=neural /opt/openworm/c302 /opt/openworm/c302
COPY --from=body /opt/openworm/sibernetic /opt/openworm/sibernetic
COPY --from=validation /opt/openworm/validation /opt/openworm/validation
# Copy orchestration
COPY master_openworm.py /opt/openworm/
COPY openworm.yml /opt/openworm/default_config.yml

# === Stage 5: Viewer ([DD014](DD014_Dynamic_Visualization_Architecture.md) Dynamic Visualization) ===
FROM full AS viewer
ARG WORM3DVIEWER_REF=main
RUN git clone --branch $WORM3DVIEWER_REF --depth 1 \
    https://github.com/openworm/Worm3DViewer.git /opt/openworm/viewer
RUN pip install trame trame-vtk trame-vuetify pyvista zarr ome-zarr
# Surface reconstruction + OME-Zarr export utilities
COPY viewer/ /opt/openworm/viewer/
EXPOSE 8501
```

**Benefits:**

- **Build caching:** Changing c302 code only rebuilds Stage 1 + Stage 4 (not Sibernetic)
- **Contributor override:** `docker build --build-arg C302_REF=my-feature-branch .` swaps in a custom c302
- **Modular images:** Can run just c302 (Stage 1) for neural-only development
- **Smaller rebuild time:** ~5 minutes for a single-subsystem change vs. ~20 minutes for full rebuild

### 3. Docker Compose for Composable Execution

Add a `docker-compose.yml` that defines services for different use cases:

```yaml
# docker-compose.yml
version: "3.8"

services:
  # === Quick smoke test (CI, contributor sanity check) ===
  quick-test:
    build:
      context: .
      target: full
    command: >
      python3 /opt/openworm/master_openworm.py
        --config /opt/openworm/default_config.yml
        --duration 10
        --no-video
    volumes:
      - ./output:/opt/openworm/output

  # === Standard simulation (default 15ms) ===
  simulation:
    build:
      context: .
      target: full
    command: >
      python3 /opt/openworm/master_openworm.py
        --config /opt/openworm/default_config.yml
    volumes:
      - ./output:/opt/openworm/output
    deploy:
      resources:
        limits:
          memory: 8G

  # === Full validation suite (CI blocking check) ===
  validate:
    build:
      context: .
      target: full
    command: >
      python3 /opt/openworm/master_openworm.py
        --config configs/validation_full.yml
    volumes:
      - ./output:/opt/openworm/output
    deploy:
      resources:
        limits:
          memory: 16G

  # === Viewer — Dynamic visualization ([DD014](DD014_Dynamic_Visualization_Architecture.md)) ===
  viewer:
    build:
      context: .
      target: viewer                 # New Docker stage (see below)
    command: >
      python3 /opt/openworm/viewer/app.py
        --data /opt/openworm/output/openworm.zarr
        --port 8501
    ports:
      - "8501:8501"
    volumes:
      - ./output:/opt/openworm/output
    depends_on:
      simulation:
        condition: service_completed_successfully

  # === Neural-only development (no body physics) ===
  neural-dev:
    build:
      context: .
      target: neural
    command: >
      python3 -c "from c302 import generate; generate('C1', 'FW')"
    volumes:
      - ./output:/opt/openworm/output

  # === Interactive shell (contributor debugging) ===
  shell:
    build:
      context: .
      target: full
    command: /bin/bash
    stdin_open: true
    tty: true
    volumes:
      - ./output:/opt/openworm/output
      - .:/opt/openworm/workspace
```

**Usage for contributors:**
```bash
# Quick sanity check (2 minutes)
docker compose run quick-test

# Standard simulation
docker compose run simulation

# Full validation (for PRs to main)
docker compose run validate

# Interactive debugging
docker compose run shell

# Test with your branch of c302
docker compose build --build-arg C302_REF=my-feature-branch simulation
docker compose run simulation
```

### 4. Dependency Pinning (`versions.lock`)

Replace branch-name dependencies with a lockfile that pins exact commits:

```yaml
# versions.lock — Pinned dependency versions
# Updated by the Integration Maintainer for each release.
# Contributors should NOT modify this file.

c302:
  repo: "https://github.com/openworm/c302.git"
  commit: "a1b2c3d4e5f6"  # Exact commit hash
  tag: "ow-0.10.0"
  pypi_version: null        # If published to PyPI

sibernetic:
  repo: "https://github.com/openworm/sibernetic.git"
  commit: "f6e5d4c3b2a1"
  tag: "ow-0.10.0"

connectome_toolbox:
  repo: "https://github.com/openworm/ConnectomeToolbox.git"
  commit: "1a2b3c4d5e6f"
  pypi_version: "0.2.7"    # Also pinned via pip

neuron:
  pypi_version: "8.2.6"

open_worm_analysis_toolbox:
  repo: "https://github.com/openworm/open-worm-analysis-toolbox.git"
  commit: "6f5e4d3c2b1a"  # [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival — pin after Python 3.12 update

tracker_commons:
  repo: "https://github.com/openworm/tracker-commons.git"
  commit: "a1b2c3d4e5f6"  # [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) — WCON 1.0 spec pin
  wcon_version: "1.0"

owmeta:
  repo: "https://github.com/openworm/owmeta.git"
  commit: "deadbeef1234"

# System dependencies (Dockerfile apt-get)
system:
  ubuntu: "24.04"
  python: "3.12"
  java: "8"

# External SDKs (with checksum for integrity)
opencl_sdk:
  url: "https://github.com/openworm/sibernetic/releases/download/v1.0/AMD-APP-SDK-3.0.tar.bz2"
  sha256: "abc123..."  # Verify download integrity
```

**Build script reads `versions.lock`:**
```bash
# build.sh (enhanced)
C302_COMMIT=$(python3 -c "import yaml; print(yaml.safe_load(open('versions.lock'))['c302']['commit'])")
docker build \
  --build-arg C302_REF=$C302_COMMIT \
  --build-arg SIBERNETIC_REF=$(get_version sibernetic) \
  -t openworm/openworm:$(cat VERSION) .
```

### 5. Enhanced `master_openworm.py` (Implement All 5 Steps)

The orchestrator must implement the full pipeline, driven by `openworm.yml`:

```
Step 1: Load configuration (openworm.yml)
Step 2: Initialize subsystems based on config
         - If neural.enabled: generate c302 network at specified level
         - If body.enabled: initialize Sibernetic with specified backend
         - If pharynx.enabled: initialize pharyngeal circuit
         - If intestine.enabled: initialize intestinal oscillator
Step 3: Run coupled simulation
         - Time-step loop with configurable coupling intervals
         - Each enabled subsystem advances one step
         - Data exchange at coupling boundaries (Ca²⁺ → forces, etc.)
Step 4: Generate outputs
         - Plots (membrane potentials, calcium, movement)
         - WCON trajectory file
         - Video (if enabled — fix the memory leak first)
Step 4b: Export OME-Zarr ([DD014](DD014_Dynamic_Visualization_Architecture.md), if visualization.enabled)
         - Collect all subsystem outputs into openworm.zarr
         - body/positions, body/types, body/cell_ids ([DD003](DD003_Body_Physics_Architecture.md), [DD004](DD004_Mechanical_Cell_Identity.md))
         - neural/voltage, neural/calcium, neural/positions ([DD001](DD001_Neural_Circuit_Architecture.md))
         - muscle/activation, muscle/calcium ([DD002](DD002_Muscle_Model_Architecture.md))
         - pharynx/pumping_state ([DD007](DD007_Pharyngeal_System_Architecture.md), if pharynx.enabled)
         - intestine/calcium, intestine/defecation_events ([DD009](DD009_Intestinal_Oscillator_Model.md), if intestine.enabled)
         - neuropeptides/concentrations ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md), if neural.neuropeptides)
         - validation/overlay ([DD010](DD010_Validation_Framework.md), if validation.run_after_simulation)
         - geometry/ (cell metadata, VirtualWorm meshes)
         - Run surface reconstruction (marching cubes) if visualization.surface_reconstruction
Step 5: Run validation (if enabled)
         - Tier 1: Single-cell electrophysiology checks
         - Tier 2: Functional connectivity vs. Randi 2023
         - Tier 3: Behavioral kinematics vs. Schafer lab
         - Generate pass/fail report
         - Exit with non-zero code if blocking tiers fail
```

**Critical fix needed:** The video generation pipeline (xvfb + tmux + ffmpeg screen capture) must be replaced. Options:

1. **Headless rendering** via OSMesa or EGL (no X server needed)
2. **Post-hoc visualization** from saved particle positions (decouple recording from simulation)
3. **Skip video in CI** (validation doesn't need video, only data)

### 6. CI/CD Pipeline (Automated Quality Gates)

```yaml
# .github/workflows/integration.yml
name: Integration Test Suite
on:
  pull_request:
    branches: [main, dev*]
  push:
    branches: [main]

jobs:
  # === Gate 1: Build (does it compile?) ===
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker compose build simulation

  # === Gate 2: Smoke test (does it run?) ===
  smoke-test:
    needs: build
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - name: Run 10ms simulation (no video)
        run: docker compose run quick-test
      - name: Check outputs exist
        run: |
          test -f output/*.png && echo "Plots: OK"
          test -f output/*.wcon && echo "WCON: OK"

  # === Gate 3: Tier 2 validation (circuit-level, BLOCKING) ===
  tier2-validation:
    needs: smoke-test
    runs-on: ubuntu-latest
    timeout-minutes: 60
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - name: Run functional connectivity validation
        run: docker compose run validate
      - name: Check pass/fail
        run: python3 scripts/check_ci_results.py output/validation_report.json

  # === Gate 4: Tier 3 validation (behavioral, BLOCKING for main) ===
  tier3-validation:
    needs: smoke-test
    runs-on: ubuntu-latest
    timeout-minutes: 120
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Run behavioral validation (5s sim)
        run: >
          docker compose run -e DURATION=5000 validate
      - name: Upload validation report
        uses: actions/upload-artifact@v4
        with:
          name: validation-report
          path: output/validation_report.json

  # NOTE: Once Taichi graduates to Production (see DD003 Backend Stabilization Roadmap),
  # CI should run smoke tests on multiple backends (at minimum OpenCL + one Python backend)
  # to catch backend-specific regressions.
```

### 7. Contributor Development Workflow

#### For contributors working on a specific subsystem:

```bash
# 1. Fork the subsystem repo (e.g., c302)
gh repo fork openworm/c302

# 2. Clone the meta-repo (for integration testing)
git clone https://github.com/openworm/OpenWorm.git
cd OpenWorm

# 3. Build with your branch of c302
docker compose build --build-arg C302_REF=my-feature-branch simulation

# 4. Run quick test
docker compose run quick-test

# 5. Check results
ls output/   # PNGs, WCON files

# 6. Run validation before submitting PR
docker compose run validate

# 7. If validation passes, submit PR to c302 repo
# CI on the meta-repo will automatically test the integration
```

#### For contributors adding a new subsystem (e.g., [DD007](DD007_Pharyngeal_System_Architecture.md) pharynx):

```bash
# 1. Create new repo (L4 maintainer action)
gh repo create openworm/pharynx-model --public

# 2. Add to versions.lock
# pharynx:
#   repo: "https://github.com/openworm/pharynx-model.git"
#   commit: "initial"

# 3. Add Docker stage to Dockerfile
# FROM base AS pharynx
# RUN git clone ... /opt/openworm/pharynx

# 4. Add config section to openworm.yml
# pharynx:
#   enabled: false  # Off by default until validated

# 5. Add coupling code to master_openworm.py
# if config['pharynx']['enabled']:
#     pharynx.step(dt)

# 6. Add validation targets
# validation:
#   pharynx_pumping: true  # 3-4 Hz check

# 7. Submit PR to meta-repo with all of the above
```

### 8. Pre-Built Images on Docker Hub

For users who just want to run the simulation without building:

```bash
# Pull and run (no build required)
docker pull openworm/openworm:0.10.0
docker run -v $(pwd)/output:/opt/openworm/output openworm/openworm:0.10.0

# Or with docker compose
docker compose pull simulation
docker compose run simulation
```

**Automated publishing:** GitHub Actions builds and pushes tagged images to Docker Hub on every release.

### 9. JupyterLab Interface (Issue #347)

Add an optional JupyterLab service for interactive exploration:

```yaml
# docker-compose.yml (additional service)
  jupyter:
    build:
      context: .
      target: full
    command: >
      jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
      --NotebookApp.token=''
      --notebook-dir=/opt/openworm/notebooks
    ports:
      - "8888:8888"
    volumes:
      - ./output:/opt/openworm/output
      - ./notebooks:/opt/openworm/notebooks
```

**Include starter notebooks:**

- `01_explore_connectome.ipynb` — Load and visualize the connectome
- `02_run_c302_network.ipynb` — Generate and simulate a neural circuit
- `03_analyze_output.ipynb` — Plot simulation results
- `04_validate_against_data.ipynb` — Run validation comparisons

This directly addresses newcomer onboarding ([DD011](DD011_Contributor_Progression_Model.md) L0→L1 tasks) and makes orientation tasks executable in a browser.

---

## Alternatives Considered

### 1. Monorepo (All Subsystems in One Repository)

**Advantages:** Single clone, atomic commits across subsystems, simple CI.

**Rejected because:**

- OpenWorm already has 109 repos with established histories
- Different subsystems have different maintainers and release cadences
- Monorepo migration would be massively disruptive
- The current multi-repo approach is standard for scientific projects

**When to reconsider:** Never. The multi-repo approach with a meta-repo integrator is the right pattern for this project.

### 2. Git Submodules

**Advantages:** Built-in Git feature, pins exact commits.

**Rejected because:**

- Submodules are notoriously confusing for contributors (`git clone --recursive`, detached HEAD, update commands)
- OpenWorm tried this before (the meta-repo once had submodules — they were removed)
- The `versions.lock` + build-arg approach gives the same pinning benefits without submodule pain

### 3. Nix / Guix for Reproducible Builds

**Advantages:** Perfectly reproducible, content-addressed, covers system deps.

**Rejected because:**

- Extremely steep learning curve (most contributors won't know Nix)
- Docker is already the standard in this project and the broader scientific computing community
- Nix inside Docker is possible but adds complexity without clear benefit for this project size

### 4. Kubernetes / Microservices (One Container Per Subsystem)

**Advantages:** Clean separation, independent scaling, true composability.

**Rejected because:**

- Massive operational overhead for a volunteer-run open source project
- The subsystems communicate via shared memory and files, not network APIs
- Latency between containers would harm the tight neural↔body coupling loop
- Nobody would maintain a Kubernetes cluster

### 5. Keep Current Approach (Single Dockerfile, Shell Scripts)

**Rejected because:**

- Cannot support adding new subsystems without growing a monolithic Dockerfile
- No contributor workflow for testing changes against the full stack
- No automated validation
- Memory leak and video pipeline issues remain unaddressed
- Single maintainer is a bus factor risk

---

## Quality Criteria

### For the Simulation Stack Itself

1. **Build succeeds in CI on every push to main.** Zero tolerance for broken builds.

2. **Quick test completes in <5 minutes.** This is the contributor feedback loop — if it takes longer, people won't run it.

3. **Full validation suite completes in <2 hours.** This runs on PRs to main. Must be fast enough to not block contributor workflow.

4. **Pre-built Docker images published for every tagged release.** Users should never need to build from source unless developing.

5. **Configuration file is the single source of truth.** No simulation parameters hardcoded in Python scripts, Dockerfiles, or shell scripts.

6. **Every subsystem can be disabled independently.** A contributor working on c302 should be able to run neural-only simulations without building Sibernetic.

7. **`versions.lock` is updated atomically with releases.** When we release 0.10.0, all component commits are pinned together.

### For Contributors

8. **A new contributor can go from `git clone` to running simulation in <30 minutes** (including Docker image pull, not build).

9. **Testing a change to one subsystem requires rebuilding only that subsystem's Docker stage** (~5 minutes, not 20).

10. **Validation results are automatically reported on PRs.** Contributors see pass/fail before human review.

---

## Boundaries (Out of Scope)

### This Design Document Does NOT Cover:

1. **Cloud execution.** Running simulations on AWS/GCP/Azure is out of scope. The stack runs locally in Docker. Cloud deployment can be a future DD.

2. **Real-time visualization.** Geppetto (the web-based viewer) is dormant and not part of this architecture. Post-hoc visualization via Jupyter notebooks is in scope.

3. **Multi-node / HPC distribution.** The simulation runs on a single machine. Distributing across nodes (MPI) is future work.

4. **Specific subsystem implementations.** This DD covers how subsystems plug together, not what they compute internally (that's [DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md)).

5. **AI agent deployment.** N2-Whisperer/Mind-of-a-Worm/Mad-Worm-Scientist are separate infrastructure (see [AI Agents for Community Scaling](../Community/ai_agents.md)).

---

## Ownership and Maintenance

### Integration Is a Shared Responsibility

**Integration is not solely the Integration Maintainer's job.** The INTEGRATION_AUDIT.md (produced alongside this DD) identified that every Design Document was originally written in isolation — specifying what each subsystem does but not how it composes with the rest of the organism.

The fix: **every DD now has an Integration Contract section** (inputs, outputs, config, Docker, integration test, coupling dependencies). This distributes integration responsibility:

| Role | Integration Responsibility |
|------|---------------------------|
| **Integration Maintainer (L4)** | Owns Docker build, CI pipeline, `openworm.yml` schema, `versions.lock`, `master_openworm.py` orchestrator |
| **Subsystem Maintainer (L4)** | Owns their DD's Integration Contract. Ensures changes to their subsystem don't break downstream consumers. Updates consuming DDs' input specs when outputs change. |
| **Committer (L3)** | When reviewing PRs, checks the DD's Integration Contract section. If a PR changes a coupling interface, coordinates with consuming subsystem maintainers before merging. |
| **Contributor (L2)** | Runs `docker compose run quick-test` before submitting PRs. Includes integration test results in PR description. |
| **Mind-of-a-Worm (AI)** | Automatically identifies coupling interface changes, tags affected maintainers, verifies integration test evidence in PR description. |
| **Mad-Worm-Scientist (AI)** | Escalates integration CI failures on `main` as **IMMEDIATE** priority to founder. |

**The through-line:** The Integration Maintainer owns the infrastructure that makes integration possible. But every contributor, reviewer, and maintainer is responsible for keeping their piece integratable. Mind-of-a-Worm automates what it can; human judgment handles the rest.

### New Role: L4 Integration Maintainer

This Design Document introduces a new entry in the Subsystem Ownership Map ([DD011](DD011_Contributor_Progression_Model.md)):

| Subsystem | Design Documents | L4 Maintainer | Primary Repository |
|-----------|-----------------|---------------|-------------------|
| **Integration Stack** | **[DD013](DD013_Simulation_Stack_Architecture.md)** (this), [DD010](DD010_Validation_Framework.md) | **TBD — Critical hire** | `openworm/OpenWorm` |

The Integration Maintainer is responsible for:

| Responsibility | Frequency | Effort |
|---------------|-----------|--------|
| Merge PRs to meta-repo | As needed | 1-2 hrs/week |
| Update `versions.lock` for releases | Monthly | 2-4 hrs/month |
| Maintain Dockerfile and docker-compose | As needed | 1-2 hrs/month |
| Maintain CI/CD pipeline | As needed | 1-2 hrs/month |
| Review subsystem integration PRs | As needed | 2-3 hrs/week |
| Triage integration issues | Weekly | 1 hr/week |
| Coordinate with subsystem L4 maintainers | Bi-weekly | 30 min |
| Update getting-started documentation | Per release | 2-4 hrs/release |

**Total estimated effort: 5-10 hrs/week.**

**Who should fill this role:**

- Currently the Neural Circuit L4 Maintainer is doing this de facto but it's not formalized or sustainable alongside their Neural Circuit role
- Ideal candidate: Someone with strong DevOps/Docker experience who also understands the science
- Alternative: An L3 contributor who can be mentored into this role
- Mind-of-a-Worm AI can assist with routine tasks (dependency updates, CI triage) but cannot own architectural decisions

**Founder involvement:** Approve L4 appointment, review major architectural changes (per [DD011](DD011_Contributor_Progression_Model.md)). This role should **reduce** founder time, not increase it.

### Mind-of-a-Worm Support for Integration

Mind-of-a-Worm (AI agent) can automate routine integration tasks:

1. **Dependency staleness alerts:** Weekly check if any pinned commit in `versions.lock` is >30 days behind the subsystem repo's main branch. Post alert to `#development`.

2. **CI failure triage:** When CI fails, Mind-of-a-Worm reads the logs, identifies which subsystem broke, and tags the relevant L4 maintainer.

3. **PR integration checklist:** When a PR modifies `openworm.yml`, `versions.lock`, or `Dockerfile`, Mind-of-a-Worm verifies:
    - Config schema is valid
    - All referenced repos/commits exist
    - No subsystem accidentally disabled
    - Version numbers are consistent

4. **Onboarding verification:** For L0→L1 Task B1 ("Install and run Docker simulation"), Mind-of-a-Worm can verify the output screenshot includes the correct version string.

---

## Implementation Roadmap

For the granular task breakdown of DD013 implementation, see the [DD013 Draft Issues](DD013_draft_issues.md) (42 issues organized into Phases A–D, Infrastructure, and Backend Stabilization). For project-wide phasing and timeline, see the [DD Phase Roadmap](DD_PHASE_ROADMAP.md) — DD013 is assigned to **Phase A: Infrastructure Bootstrap (Weeks 1–4)**.

---

## The Contributor → Simulation Feedback Loop

This is the critical path that makes the whole system work:

```
Contributor makes a change
        │
        ▼
Pushes to their fork of a subsystem repo (e.g., c302)
        │
        ▼
Runs locally: docker compose build --build-arg C302_REF=my-branch simulation
              docker compose run quick-test     (~2 min)
              docker compose run validate       (~30 min)
        │
        ▼
Opens PR to subsystem repo
        │
        ▼
Subsystem CI runs (unit tests for that repo)
        │
        ▼
Integration CI triggered (runs full stack with PR branch)
  ├── Build: Does it compile with the rest of the stack?
  ├── Smoke test: Does it produce output?
  ├── Tier 2: Does functional connectivity hold?
  └── Tier 3: Does movement still look right?
        │
        ▼
Mind-of-a-Worm pre-review:
  ├── Design Document compliance check
  ├── Code style and test coverage
  └── Validation results summary
        │
        ▼
Human review (L3/L4)
        │
        ▼
Merge → versions.lock updated → next release includes change
        │
        ▼
Docker Hub image published
        │
        ▼
Next newcomer who runs the Docker image sees the improvement
```

**This is the through-line:** Every contributor's work flows through a path that ends with the next newcomer experiencing a better simulation. The Docker image is the product. The configuration system is the interface. The validation framework is the quality gate. The meta-repo is the integration point.

---

## Open Questions (Require Founder Input)

1. **Who is the L4 Integration Maintainer?** The Neural Circuit L4 Maintainer is the de facto integration maintainer but this should be formalized and ideally shared with someone else to reduce bus factor.

2. **GPU support priority:** Should we invest in fixing Docker GPU passthrough (issue #320) now, or wait for Phase 1 to be further along? GPU would make longer simulations practical.

3. **MyBinder vs. Google Colab:** For zero-install demos, MyBinder is fully open but resource-limited. Google Colab has GPU but requires Google account. Which aligns better with open science values?

4. **OpenCL SDK hosting:** The AMD SDK is currently downloaded from SourceForge at build time. Should we host it in the OpenWorm org (GitHub Releases on the sibernetic repo) for reliability?

5. **Release cadence target:** Current cadence is roughly quarterly. Should we aim for monthly releases once the new stack is in place?

---

### Existing Code Resources

**sibernetic_config_gen** ([openworm/sibernetic_config_gen](https://github.com/openworm/sibernetic_config_gen), 2016, dormant):
Generates starting particle positions and `.ini` config files for Sibernetic. Contains particle placement algorithms for different body resolutions. Reusable for DD013's `openworm.yml` → Sibernetic `.ini` translation layer. **Estimated time savings: 10-20 hours.**

**sibernetic_NEURON** ([openworm/sibernetic_NEURON](https://github.com/openworm/sibernetic_NEURON), 2016, dormant):
Predecessor to `sibernetic_c302.py` — contains Sibernetic-NEURON interface code. Review for patterns applicable to [DD019](DD019_Closed_Loop_Touch_Response.md)'s bidirectional coupling.

**skeletonExtraction** ([openworm/skeletonExtraction](https://github.com/openworm/skeletonExtraction), 2016, dormant):
Extracts 49-point skeleton (centerline) from Sibernetic particle output, exports to COLLADA. The skeleton extraction algorithm is directly needed for DD013's SPH → WCON export pipeline and [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)'s analysis toolbox input. **Estimated time savings: 15-25 hours.**

---

## References

1. **Docker multi-stage builds.** https://docs.docker.com/build/building/multi-stage/
2. **Docker Compose specification.** https://docs.docker.com/compose/compose-file/
3. **GitHub Actions for Docker.** https://docs.docker.com/build/ci/github-actions/
4. **MyBinder.org.** https://mybinder.org/ — Zero-install reproducible environments
5. **[Sarma et al. (2016)](https://doi.org/10.12688/f1000research.9095.1).** "Unit testing, model validation, and biological simulation." *F1000Research* 5:1946.
6. **OpenWorm/OpenWorm repository.** https://github.com/openworm/OpenWorm

---

## Migration Path

### From v0.9.x to v0.10.0 (This DD)

1. **v0.9.7 remains available.** The current Dockerfile and scripts are preserved in the `legacy-0.9.x` branch.
2. **v0.10.0 introduces the new architecture** (`openworm.yml`, multi-stage Docker, docker-compose, `versions.lock`).
3. **Backward compatibility:** `run.sh` continues to work but prints a deprecation notice pointing to `docker compose run simulation`.
4. **No behavioral change:** The default `openworm.yml` produces the same simulation output as v0.9.7 (c302 Level C2, Sibernetic half-res, 15ms).
5. **Phased introduction:** New subsystems (pharynx, intestine, neuropeptides) are added as `enabled: false` config options. Contributors opt in.

---

## Integration Contract

### Inputs / Outputs

The simulation stack is the **integration layer** — it consumes and routes outputs from all science DDs:

| Direction | DD | Data | Format |
|-----------|------|------|--------|
| Consumes | [DD001](DD001_Neural_Circuit_Architecture.md) | Neural state | OME-Zarr `/neural/` |
| Consumes | [DD002](DD002_Muscle_Model_Architecture.md) | Muscle forces | OME-Zarr `/muscle/` |
| Consumes | [DD003](DD003_Body_Physics_Architecture.md) | Body geometry | OME-Zarr `/physics/` |
| Produces | All | Unified simulation state | OME-Zarr `/simulation/` |

### Repository & Packaging

- Primary repository: `openworm/OpenWorm`
- Docker multi-stage build: orchestrator layer
- `versions.lock` key: `openworm`

### Configuration

- `openworm.yml` root section: `simulation:`
- Key parameters: `timestep`, `duration`, `output_format`, `subsystems[]`

### How to Test (Contributor Workflow)

- `docker compose run quick-test` — verifies all containers start and communicate
- `docker compose run validate` — runs [DD010](DD010_Validation_Framework.md) Tier 2 correlation check

### Coupling Dependencies

- **Upstream:** DD001, DD002, DD003, DD005, DD006, DD007, DD009 (all science subsystems)
- **Downstream:** DD014 (visualization), DD010 (validation)

---

- **Approved by:** Pending (requires founder + Integration Maintainer appointment)
- **Implementation Status:** Proposed
- **Next Actions:**

1. Appoint or recruit L4 Integration Maintainer
2. Begin Phase A (config system + multi-stage Docker)
3. Fix the video pipeline memory leak (critical for any serious use)
4. Set up CI with docker-compose-based test suite
