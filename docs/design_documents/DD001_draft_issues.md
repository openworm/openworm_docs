# DD001 Draft GitHub Issues

!!! warning "Internal planning document — to be deleted before master merge"
    This file exists to plan the openworm/sibernetic GitHub issues that will derive from DD001. Once the issues are filed on GitHub, **this entire document is to be deleted** and removed from the mkdocs nav. It is not part of the public design-document set. The canonical source of truth for implementation work is the issue tracker itself ([`label:dd001`](https://github.com/openworm/sibernetic/labels/dd001)) and the [release milestones](https://github.com/openworm/sibernetic/milestones).

**Epic:** DD001 — Body Physics Engine (Sibernetic) Architecture

**Generated from:** [DD001: Body Physics Engine Architecture](DD001_Body_Physics_Architecture.md)

**Methodology:** [§2.2 — DD Issue Generator](../contributing/ai-contributors.md#22-the-dd-issue-generator-automated-issue-creation), [§2.3 — Reuse-First Issue Design](../contributing/ai-contributors.md#23-reuse-first-issue-design), [§2.4 — DD011 Simulation Stack Integration](../contributing/ai-contributors.md#24-dd011-simulation-stack-integration)

**Totals:** 18 fresh issues to file (ai-workable: 12 / human-expert: 6 | L1: 6, L2: 7, L3: 5) **plus** ~12 existing issues kept live (see [Migration Context](#migration-context-stabilize-the-gold-standard-while-building-forward) below).

**Roadmap Context:** DD001 is a **Phase 0** DD (existing, working). Its draft issues span multiple roadmap phases:

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Validation Infrastructure (Issues [#233](https://github.com/openworm/sibernetic/issues/233)–[#235](https://github.com/openworm/sibernetic/issues/235)) | **Phase A1** | `[TO BE CREATED]` scripts called out by [DD001 §Backend Stabilization Roadmap](DD001_Body_Physics_Architecture.md#backend-stabilization-roadmap) |
| 2. Per-Demo Parity & CUDA Bring-Up (Issues [#236](https://github.com/openworm/sibernetic/issues/236)–[#240](https://github.com/openworm/sibernetic/issues/240)) | **Phase A1** | The substrate-correctness work consolidated on `ow-native-gpu-0.1.0`; each demo gets its own parity gate |
| 3. Substrate Docs & PR Enforcement (Issues [#241](https://github.com/openworm/sibernetic/issues/241)–[#243](https://github.com/openworm/sibernetic/issues/243)) | **Phase A1** | Documents what landed (kernels + paired backwards) and makes the 8-phase [Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology) discoverable to new PRs |
| 4. Output Pipeline & Viewer Bridge (Issues [#244](https://github.com/openworm/sibernetic/issues/244)–[#246](https://github.com/openworm/sibernetic/issues/246)) | **Phase A1/1** | OME-Zarr, surface mesh, configurable output for the visualization handoff |
| 5. Documentation & Onboarding (Issues [#247](https://github.com/openworm/sibernetic/issues/247)–[#248](https://github.com/openworm/sibernetic/issues/248)) | **Any** | Architecture overview, CONTRIBUTING.md (config-docs improvements folded into existing [#165](https://github.com/openworm/sibernetic/issues/165) and [#128](https://github.com/openworm/sibernetic/issues/128)) |
| 6. Future Backend Direction (Issues [#249](https://github.com/openworm/sibernetic/issues/249)–[#250](https://github.com/openworm/sibernetic/issues/250)) | **Phase 2+** | FEM Projective Dynamics evaluation; Python bindings |

---

## Issue Numbering

The 18 fresh issues below are labeled with **predicted** GitHub issue numbers (`[#233](https://github.com/openworm/sibernetic/issues/233)` through `[#250](https://github.com/openworm/sibernetic/issues/250)`) based on the current `openworm/sibernetic` numbering high-water mark (`[#232](https://github.com/openworm/sibernetic/issues/232)`, a closed PR, as of 2026-05-28). Actual numbers assigned at filing time will shift forward if other issues or PRs are opened on the repo first. After filing, this document should be updated to reflect the assigned numbers.

---

## Migration Context: Stabilize the Gold Standard While Building Forward

The 31 pre-existing `openworm/sibernetic` open issues have been re-evaluated with a more careful lens: **OpenCL is DD001's gold-standard reference implementation, and the native Metal / CUDA substrates must reach parity against it.** That means stabilizing OpenCL — fixing its bugs, documenting its behavior, exposing its parameters — is *supporting* work for the modernization, not a distraction from it. Issues that were earlier slated for blanket closure-as-superseded have been re-bucketed: real OpenCL defects, real docs gaps, and real build problems are kept live as **gold-standard stabilization** work. Issues that genuinely belong to held-back DDs (visualization, closed-loop touch, proprioception, foundation models) or duplicate other issues remain candidates for closure.

As of 2026-05-28, **27 issues remain open**, and 4 were closed in the last week ([#102](https://github.com/openworm/sibernetic/issues/102), [#130](https://github.com/openworm/sibernetic/issues/130), [#176](https://github.com/openworm/sibernetic/issues/176), [#221](https://github.com/openworm/sibernetic/issues/221)). Of the 27 open, ~12 are kept live, ~3 are folded into fresh DD001-derived issues, and ~12 will close with structured archive comments referencing DD001 or a held-back DD.

### Live issues (kept open, re-labeled by category)

#### A. OpenCL reference defects (real bugs, gold-standard stabilization)

| Issue | Title | Milestone | Why live |
|-------|-------|-----------|----------|
| [#125](https://github.com/openworm/sibernetic/issues/125) | Worm_motion_log contains only zeros in full scale resolution worm | **v0.0.8** | Real OpenCL output bug, assigned to @a-palyanov. The output system is what every Metal/CUDA parity test compares against — fix it. **Label:** `opencl`, `bug`, `gold-standard` |
| [#126](https://github.com/openworm/sibernetic/issues/126) | Liquid particles streaming out of standard cube | **v0.0.8** | Real OpenCL physics bug on `demo1` (the cube drop scenario that the Metal port already passes). If the reference itself is leaking particles, parity claims are meaningless. **Label:** `opencl`, `bug`, `gold-standard` |
| [#136](https://github.com/openworm/sibernetic/issues/136) | CL_OUT_OF_RESOURCES on Nvidia GTX 1060 copying position buffer | **v0.0.8** | Real OpenCL HW-portability bug. Anyone reproducing on the listed NVIDIA generation hits it. **Label:** `opencl`, `bug`, `hardware-specific` |
| [#160](https://github.com/openworm/sibernetic/issues/160) | Pressure buffer file issue | **v0.0.8** | Concrete repro from 2019 — verify still reproduces on current master. **Label:** `opencl`, `bug`, `needs-reproduction-current` |
| [#180](https://github.com/openworm/sibernetic/issues/180) | Resolve compiler warnings | **v0.0.8** | Code-quality cleanup against current master (compiler warnings drift with toolchains). Good first issue. **Label:** `code-quality`, `good-first-issue` |
| [#223](https://github.com/openworm/sibernetic/issues/223) | makefile.OSX doesn't work on M series Mac | **v0.0.8** | Build path still partially broken on ARM Mac (setup.sh helps but doesn't cover all entry points). **Label:** `build`, `apple-silicon` |

#### B. OpenCL reference enhancements + docs (low-risk, high-value)

| Issue | Title | Milestone | Why live |
|-------|-------|-----------|----------|
| [#127](https://github.com/openworm/sibernetic/issues/127) | Worm body modelling and mechanics — parameters, values etc. | **v0.3.0** | 12-comment discussion thread on parameter values (Young's modulus, etc.). Capture the canonical values in the codebase / config docs. **Label:** `docs`, `physics` |
| [#128](https://github.com/openworm/sibernetic/issues/128) | Enhance configuration files with physical parameters specific to full/half resolution | **v0.3.0** | Expose physical params through config rather than hard-coded in source. Reduces the "magic numbers" problem and helps reproducibility. **Label:** `enhancement`, `config` |
| [#147](https://github.com/openworm/sibernetic/issues/147) | How to expand the liquid particles? | **v0.0.8** | Real docs gap. Pairs with [#148](https://github.com/openworm/sibernetic/issues/148). Bundled with stabilization since the answer is part of the gold-standard usage docs. **Label:** `docs`, `good-first-issue` |
| [#148](https://github.com/openworm/sibernetic/issues/148) | Document the way to access the body position on each step? | **v0.0.8** | Real docs gap. Pairs with [#147](https://github.com/openworm/sibernetic/issues/147). Bundled with stabilization for the same reason. **Label:** `docs`, `good-first-issue` |
| [#165](https://github.com/openworm/sibernetic/issues/165) | User-defined geometries and muscle models | **v0.3.0** | 18-comment community thread. Custom-geometry workflow is the right scope; the fresh "config-onboarding docs" issue I previously proposed folds back into this one. **Label:** `docs`, `community-interest` |
| [#224](https://github.com/openworm/sibernetic/issues/224) | `QUEUE_EACH_KERNEL` OpenCL profiling flag | **v0.0.8** | Clean profiling enhancement to the reference backend; fits the stabilization release. **Label:** `opencl`, `enhancement`, `good-first-issue` |

#### C. Modernization tracking

| Issue | Title | Milestone | Why live |
|-------|-------|-----------|----------|
| [#226](https://github.com/openworm/sibernetic/issues/226) | Port sphFluid.cl to Metal for ARM64 Mac | **v0.1.0** | Canonical tracking issue for the Metal port. Wei Weng's filing is the statement of need that DD001 §Backend Stabilization Roadmap formalizes. The per-demo parity work ([Issues [#236](https://github.com/openworm/sibernetic/issues/236)–#239](#group-2-per-demo-opencl-native-parity-phase-a1)) consolidates implementation under this umbrella. Closes when v0.1.0 ships. **Label:** `native-gpu`, `phase-0`, `epic` |

### Issues slated for closure (mapping unchanged)

Closures fall into these buckets. The full per-issue migration plan with close-comment templates lives outside this DD; the buckets are summarized here.

| Bucket | Count | Examples | Rationale |
|--------|-------|----------|-----------|
| Out of DD001 scope (held-back DDs) | ~7 | [#100](https://github.com/openworm/sibernetic/issues/100) (steering — DD019), [#101](https://github.com/openworm/sibernetic/issues/101) (renders — DD012), [#117](https://github.com/openworm/sibernetic/issues/117), [#119](https://github.com/openworm/sibernetic/issues/119) (chart output — DD012), [#141](https://github.com/openworm/sibernetic/issues/141) (proprioception — DD019), [#144](https://github.com/openworm/sibernetic/issues/144) (touch — DD015), [#182](https://github.com/openworm/sibernetic/issues/182) (video recording — DD012) | Scope belongs to a design document held back from the current publish set. Fresh issues will be derived from those DDs when they publish. |
| Out of DD001 scope (boundaries) | 1 | [#163](https://github.com/openworm/sibernetic/issues/163) (chemotaxis molecules) | Explicitly out of DD001 §Boundaries (item 3: environmental complexity beyond liquid/gel). |
| Duplicate / answered | 2 | [#106](https://github.com/openworm/sibernetic/issues/106) (duplicate of [#107](https://github.com/openworm/sibernetic/issues/107)), [#168](https://github.com/openworm/sibernetic/issues/168) (stale help request, no reproduction info) | Routine dedup. |
| Replaced by fresh issue | 2 | [#108](https://github.com/openworm/sibernetic/issues/108) (calibration → covered by [Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology) workflow), [#122](https://github.com/openworm/sibernetic/issues/122) ([pySibernetic](https://github.com/openworm/sibernetic/issues/122) → replaced by [Issue #250](#issue-250-sibernetic-python-bindings-for-direct-api-access-replaces-122) formal Python bindings) | Clean DD001 replacement exists. |
| Coupling docs (decide) | 1 | [#107](https://github.com/openworm/sibernetic/issues/107) (Write doc on Sibernetic-NEURON) | Could be kept live as a docs issue (Sibernetic↔c302/NEURON coupling docs are still useful) OR closed as covered by DD001 §Integration Contract. **Leadership call.** |
| Multi-GPU performance scaling | 1 | [#135](https://github.com/openworm/sibernetic/issues/135) | Phase 2+ scope. Close as deferred. |

### Recent closures (last week, 4 issues)

For completeness: [#102](https://github.com/openworm/sibernetic/issues/102) (config docs) and [#130](https://github.com/openworm/sibernetic/issues/130) (build error) closed as Replaced / Superseded; [#176](https://github.com/openworm/sibernetic/issues/176) (c302 env issue on Windows) and [#221](https://github.com/openworm/sibernetic/issues/221) (Windows install question) closed as Answered / Superseded. The migration plan's dispositions matched the actual closures.

---

## Milestones

The current milestone landscape on `openworm/sibernetic`: three closed historical milestones (v0.0.3 in 2015, v0.0.4 in 2016, v0.0.5 in 2016) plus one active milestone (`v0.0.8 release`, currently due 2026-06-12 — proposed to slip). The proposal below repurposes the active milestone and adds three forward milestones aligned to the DD001 plan. **Each issue's milestone is shown in the issue tables above and on every individual issue section below.**

| Milestone | Status | Theme | What it ships |
|-----------|--------|-------|---------------|
| **v0.0.8 release** | Existing — **re-scope** (slip due date from 2026-06-12 to "when scope lands") | OpenCL Gold-Standard Stabilization | Lock in OpenCL as the validated reference: fix the real bugs, close the paired docs gaps, land the profiling enhancement. Without this the cross-substrate parity work has no trustworthy reference to compare against. |
| **v0.1.0 release** | **New** | Native-GPU Substrate Consolidation | The native-Metal port at OpenCL parity on the four working demos, native-CUDA scaffold brought up to demo1 parity, the consolidation PR merged. Native modernization shipped as a release. |
| **v0.2.0 release** | **New** | Validation Infrastructure + Output Pipeline | Cross-substrate validation scripts (stability, incompressibility) and the OME-Zarr + surface-mesh + configurable-output pipeline that bridges simulation output to the visualization handoff. |
| **v0.3.0 release** | **New** | Substrate Documentation + Contributor Onboarding | The substrate becomes understandable and contributor-ready: OpenCL kernel architecture documented, the 19 paired forward/backward kernels explained, MoaW PR assist live, architecture overview + CONTRIBUTING.md in place, community-tracked docs issues (#127, #128, #165) consolidated under this release. |
| **Unmilestoned** | — | Research / future-direction | FEM Projective Dynamics feasibility evaluation, Python bindings (replaces stale #122). Filed for tracking but no release commitment yet. |

### Milestone descriptions to post on GitHub

The text below is copy-paste-ready for the four GitHub milestone description fields. Each description references the published [DD001](https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/) so anyone landing on the milestone page can find the spec without searching.

#### `v0.0.8 release` — OpenCL Gold-Standard Stabilization

```
OpenCL gold-standard stabilization.

Scope: Lock in the OpenCL reference implementation as the validated
gold standard against which all native substrates (Metal, CUDA) are
measured. Fix real bugs, close paired docs gaps, land the profiling
enhancement. Without this milestone, cross-substrate parity claims
in v0.1.0 are meaningless — the reference itself must be trustworthy.

Spec: DD001 Body Physics Engine Architecture (the gold-standard
framing lives in DD001 §Backend Stabilization Roadmap).
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#backend-stabilization-roadmap

Filter for the work in this release: label:dd001 + this milestone.

No fixed due date — this milestone ships when its scope lands.
Previous "2026-06-12" due date is superseded; the four-issue scope
that triggered that date has been re-evaluated (see DD001 issue
migration plan).
```

#### `v0.1.0 release` — Native-GPU Substrate Consolidation

```
Native-GPU substrate consolidation.

Scope: Ship the native-Metal substrate at OpenCL parity on the
four working demos (demo1 cube drop, demo2 membrane permeability,
worm_alone, worm_swim). Bring native-CUDA scaffolding up to demo1
parity. Merge the native-gpu branch consolidation PR.

This milestone transitions native Metal from Experimental → Stable
per DD001 §Backend Graduation Criteria (Exit Conditions), and native
CUDA from Scaffolding → Experimental.

Spec: DD001 Body Physics Engine Architecture, especially §Cross-
Backend Parity Requirements, §Validation Methodology, and §Differ-
entiability.
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#cross-backend-parity-requirements

Filter for the work in this release: label:dd001 label:native-gpu
+ this milestone. PR #229 and PR #230 are part of the release.

Open-ended due date — ships when the four parity gates are green.
```

#### `v0.2.0 release` — Validation Infrastructure + Output Pipeline

```
Cross-substrate validation infrastructure and the simulation-output
pipeline.

Scope: Land scripts/check_stability.py and scripts/validate_
incompressibility.py so every simulation run on every substrate gets
the same gating. Ship OME-Zarr export, marching-cubes surface
reconstruction, and configurable output frequency — the data pipeline
that bridges raw simulation output to the visualization handoff.

Spec: DD001 Body Physics Engine Architecture, especially §Acceptance
Criteria and §Deliverables (the OME-Zarr rows).
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#acceptance-criteria-green-light-definitions

Filter for the work in this release: label:dd001 + this milestone.

Ships after v0.1.0 native substrates are at Stable.
```

#### `v0.3.0 release` — Substrate Documentation + Contributor Onboarding

```
Substrate becomes understandable and contributor-ready.

Scope: Document the OpenCL reference kernel architecture (~64KB
sphFluid.cl annotated walkthrough). Document the 19 paired forward/
backward kernels and the xpbd_full_bwd reverse-mode pipeline. Stand
up the Mind-of-a-Worm PR assist that surfaces the 8-phase Validation
Methodology checklist on PRs. Land the Sibernetic architecture
overview and CONTRIBUTING.md. Roll up the community-tracked docs
issues (#127, #128, #165) into this docs release.

Spec: DD001 Body Physics Engine Architecture, especially
§Differentiability and §Validation Methodology.
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#differentiability

Filter for the work in this release: label:dd001 label:docs
+ this milestone.

Ships after v0.2.0.
```

### Historical milestones (closed, reference only)

| Milestone | Closed | Issues | Scope |
|-----------|--------|--------|-------|
| v0.0.3 | 2015-07 | 12 | LeapFrog integrator, `-help` option, worm config from file, snapshot ability |
| v0.0.4 | 2016-04 | 15 | Bug-fixing pass: memory leaks, segfault on GPU-absent machines, NEURON interaction |
| v0.0.5 | 2016-05 | 2 | Multi-device parallelization, settings file format |

---

## Group 1: Validation Infrastructure (Phase A1)

Target: Scripts and infrastructure to measure simulation quality and gate cross-backend correctness.

---

### Issue [#233](https://github.com/openworm/sibernetic/issues/233): Create `scripts/check_stability.py`

- **Title:** `[DD001] Create check_stability.py — simulation divergence detector`
- **Labels:** `DD001`, `ai-workable`, `L1`, `phase-0`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.2.0** (Validation Infrastructure + Output Pipeline)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD001 — Acceptance Criteria](DD001_Body_Physics_Architecture.md#acceptance-criteria-green-light-definitions) and [DD001 Quality Criteria](DD001_Body_Physics_Architecture.md#quality-criteria) (criterion 1)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/owPhysicTest.cpp`](https://github.com/openworm/sibernetic) — Energy conservation test already exists; validates that total system energy (kinetic + potential) remains bounded across timesteps. Reuse its energy-bounding logic as a stability criterion alongside NaN/escape detection.
    - [`openworm/sibernetic/src/metal_diff/`](https://github.com/openworm/sibernetic) — Native-Metal substrate's `dump_metal_trajectory.py` shows how trajectory dumps are emitted; the stability check should accept both OpenCL `.dat` output and Metal/CUDA trajectory dumps.
- **Approach:** Extend — build on the energy conservation logic in `owPhysicTest.cpp`; wrap with NaN/escape/velocity checks usable across substrates.
- **DD011 Pipeline Role:** Body-stage validation gate. Runs after Sibernetic simulation completes. Non-zero exit code blocks the pipeline run as failed.
- **Files to Modify:**
    - `scripts/check_stability.py` (new)
    - `tests/test_check_stability.py` (new)
- **Test Commands:**
    - `python3 scripts/check_stability.py output.dat`
    - `python3 scripts/check_stability.py /tmp/demo1_metal.txt --substrate metal`
    - `pytest tests/test_check_stability.py`
- **Acceptance Criteria:**
    - [ ] Reads Sibernetic OpenCL output (`output.dat`) and native-substrate trajectory dumps
    - [ ] Detects NaN values in particle positions or velocities
    - [ ] Detects particles escaping bounding box (configurable box dimensions)
    - [ ] Detects velocity divergence (magnitude exceeding physical threshold)
    - [ ] Verifies simulation ran for at least the expected duration without early termination
    - [ ] Prints PASS/FAIL with diagnostic details (which particles, which timestep, what went wrong)
    - [ ] Returns exit code 0 on pass, non-zero on fail
    - [ ] Unit tests with synthetic data (clean → PASS; NaN-injected → FAIL; escaped particle → FAIL)
- **Sponsor Summary Hint:** The basic health check for any SPH simulation — did the physics blow up? NaN values mean the computation diverged (division by zero, impossible forces). Escaped particles mean the simulation lost containment. This script is called out in DD001's Acceptance Criteria but doesn't yet exist in the repo. The existing `owPhysicTest.cpp` already checks energy conservation — this extends that logic into a comprehensive Python checker that works across the OpenCL reference and the native Metal/CUDA substrates.

---

### Issue [#234](https://github.com/openworm/sibernetic/issues/234): Create `scripts/validate_incompressibility.py`

- **Title:** `[DD001] Create validate_incompressibility.py — density deviation checker`
- **Labels:** `DD001`, `ai-workable`, `L1`, `phase-0`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.2.0** (Validation Infrastructure + Output Pipeline)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD001 — Acceptance Criteria](DD001_Body_Physics_Architecture.md#acceptance-criteria-green-light-definitions) (validate gate) and [DD001 Quality Criteria](DD001_Body_Physics_Architecture.md#quality-criteria) (criterion 2)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Rest density ρ₀ and other physical constants with extensive inline documentation. Reference for expected density values and particle type classifications.
    - [`openworm/sibernetic/src/sphFluid.cl`](https://github.com/openworm/sibernetic) — The PCISPH pressure solver that enforces incompressibility; reference for understanding what the script validates.
- **Approach:** Create — no existing incompressibility validation script exists, but `owPhysicsConstant.h` provides all physical constants needed.
- **DD011 Pipeline Role:** Body-stage validation gate. Runs after Sibernetic simulation completes. Non-zero exit code blocks the pipeline run as failed.
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
- **Sponsor Summary Hint:** PCISPH (and the XPBD density constraint on the native substrate) enforces incompressibility — the virtual fluid shouldn't compress. If density deviates >1% from the rest density (1000 kg/m³), the pressure solver isn't converging properly. This script checks that the core physics invariant holds on every run.

---

### Issue [#235](https://github.com/openworm/sibernetic/issues/235): Create cross-backend parity test suite (`scripts/backend_parity_test.py`)

- **Title:** `[DD001] Create cross-backend parity test suite comparing native substrates against OpenCL reference`
- **Labels:** `DD001`, `ai-workable`, `L2`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.1.0** (Native-GPU Substrate Consolidation)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements) and [DD001 §Stabilization Sequence](DD001_Body_Physics_Architecture.md#stabilization-sequence) (step 2)
- **Depends On:** Issue [#233](https://github.com/openworm/sibernetic/issues/233) (`check_stability.py`)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/metal_diff/tests/test_demo1_backend_parity.py`](https://github.com/openworm/sibernetic) — Existing automated parity gate for the cube-drop demo; runs both backends, compares trajectories, reports per-metric pass/fail. **THIS is the template** — generalize to all four demos.
    - [`openworm/sibernetic/src/metal_diff/dump_metal_trajectory.py`](https://github.com/openworm/sibernetic) — Metal trajectory dumper used by the existing parity test.
- **Approach:** Extend — promote `test_demo1_backend_parity.py` into a general-purpose harness driven by a demo registry; per-demo logic lives in pluggable scenario files.
- **DD011 Pipeline Role:** Body-stage CI gate. Runs as part of `docker compose run validate` once Metal substrate is available in the image.
- **Files to Modify:**
    - `scripts/backend_parity_test.py` (new — generalized harness)
    - `scripts/parity_scenarios/{demo1,demo2,worm_alone,worm_swim}.py` (new — per-demo configs)
    - `tests/baseline/*_opencl.json` (new — see Issue [#240](https://github.com/openworm/sibernetic/issues/240))
- **Test Commands:**
    - `python3 scripts/backend_parity_test.py --backend metal-native --scenario demo1`
    - `python3 scripts/backend_parity_test.py --backend metal-native --all`
- **Acceptance Criteria:**
    - [ ] Runs each registered demo on the requested substrate; compares kinematics against the OpenCL reference trajectory
    - [ ] Reports per-metric Δ relative to OpenCL (position means, velocity stats, density stats, kinematic features); flags >±5% as fail
    - [ ] Demo registry supports demo1 (cube drop), demo2 (membrane permeability), worm_alone_half_resolution, worm_swim_half_resolution
    - [ ] `--substrate` flag accepts `opencl`, `metal-native`, `cuda-native` (CUDA produces error message until implemented)
    - [ ] Emits JSON summary + human-readable table; exit code reflects pass/fail
    - [ ] Wires into CI per [DD001 §Backend Graduation Criteria (Exit Conditions)](DD001_Body_Physics_Architecture.md#backend-graduation-criteria-exit-conditions) — a backend cannot graduate from Experimental → Stable without this passing
- **Sponsor Summary Hint:** OpenCL is the validated reference; every native substrate must reproduce its kinematic output within ±5%. The native-Metal port already has a parity gate for demo1 (the cube drop) — this issue generalizes that gate into a uniform harness covering all four working demos, and prepares the entry point for the CUDA substrate once its kernels land.

---

## Group 2: Per-Demo OpenCL ↔ Native Parity (Phase A1)

Target: Close OpenCL↔Metal parity per demo, then stand up the CUDA scaffold to the same bar. Each demo is its own deliverable so the parity gate (Issue [#235](https://github.com/openworm/sibernetic/issues/235)) can light up incrementally.

Per [DD001 §Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology), every PR landing under these issues must follow the 8-phase **predict → reference → inspect → refine → implement → SGD-tune → render → compare** workflow and satisfy the [MoaW PR review checklist](DD001_Body_Physics_Architecture.md#mind-of-a-worm-pr-review-checklist).

---

### Issue [#236](https://github.com/openworm/sibernetic/issues/236): OpenCL ↔ Metal parity on demo1 (cube drop)

- **Title:** `[DD001] OpenCL↔Metal parity on demo1 (cube drop) — confirm and lock in`
- **Labels:** `DD001`, `human-expert`, `L2`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.1.0** (Native-GPU Substrate Consolidation)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology) (8-phase workflow)
- **Depends On:** Issue [#235](https://github.com/openworm/sibernetic/issues/235) (parity harness)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/metal_diff/`](https://github.com/openworm/sibernetic) — Demo1 already at ±5% parity per DD001 §The Result Quality Gap.
    - `docs/<demo1>_opencl_vs_metal.mp4` — Side-by-side comparison MP4 (per §Validation Methodology Phase 6).
- **Approach:** Confirm — demo1 is the most-mature parity case; this issue locks the parity in CI and produces the canonical artifact bundle for the documentation set.
- **Status today:** ✅ ±5% on all 5 metrics per the existing parity test.
- **Acceptance Criteria:**
    - [ ] Parity test (Issue [#235](https://github.com/openworm/sibernetic/issues/235)) green on `--scenario demo1 --substrate metal-native`
    - [ ] Side-by-side MP4 committed under `docs/`
    - [ ] SGD convergence history committed (`tools/sgd_history/demo1_sgd_history.json`)
    - [ ] 3–4 spot-check frames with labeled y-values
    - [ ] All 10 items of the MoaW PR review checklist satisfied in the landing PR
- **Sponsor Summary Hint:** demo1 (a cube of liquid dropped under gravity) is the simplest scenario and already passes parity. This issue is the housekeeping pass: lock the existing parity result into CI, commit the comparison artifacts, and use this demo as the canonical worked example of the 8-phase validation methodology for future contributors.

---

### Issue [#237](https://github.com/openworm/sibernetic/issues/237): OpenCL ↔ Metal parity on demo2 (membrane permeability)

- **Title:** `[DD001] OpenCL↔Metal parity on demo2 (membrane permeability) — close remaining gap`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.1.0** (Native-GPU Substrate Consolidation)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology), §Differentiability (M10 membrane kernels)
- **Depends On:** Issue [#235](https://github.com/openworm/sibernetic/issues/235) (parity harness)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/metal_diff/`](https://github.com/openworm/sibernetic) — M10 membrane mechanism ported with FD-validated backward (<7e-4 rel-err per DD001 §What's Differentiable Today); sheet-scale parameter tuning in progress.
    - `sgd_demo2_membrane.py`, `sgd_demo2_permeability.py` — Tuning harnesses already exist.
- **Approach:** Finish — membrane kernels ported and backward-validated; sheet-scale `(spring_K, alpha_dist)` and membrane permeability need to converge in SGD against the OpenCL reference.
- **Status today:** 🟡 In tuning per DD001 §The Result Quality Gap.
- **Acceptance Criteria:**
    - [ ] SGD converges on the sheet-scale tuning loss within the convergence threshold called out in §Common Gotchas item 10 (`L < 1e-4`)
    - [ ] Parity test green on `--scenario demo2 --substrate metal-native`
    - [ ] Side-by-side MP4 committed under `docs/`
    - [ ] SGD convergence histories committed for both `sgd_demo2_membrane.py` and `sgd_demo2_permeability.py`
    - [ ] Frame-by-frame visual parity confirmed per §Validation Methodology Phase 7
    - [ ] All 10 MoaW PR review checklist items satisfied
- **Sponsor Summary Hint:** demo2 exercises the Ihmsen 2014 membrane mechanism (the M10 kernels). The forward and backward kernels are in place; what remains is finishing the SGD tune so the sheet-scale dynamics match OpenCL within ±5%. This is the second of four per-demo parity gates that must close before the Metal substrate can graduate to Stable.

---

### Issue [#238](https://github.com/openworm/sibernetic/issues/238): OpenCL ↔ Metal parity on `worm_alone_half_resolution`

- **Title:** `[DD001] OpenCL↔Metal parity on worm_alone_half_resolution — lock in visual parity`
- **Labels:** `DD001`, `human-expert`, `L2`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.1.0** (Native-GPU Substrate Consolidation)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology)
- **Depends On:** Issue [#235](https://github.com/openworm/sibernetic/issues/235) (parity harness)
- **Existing Code to Reuse:**
    - `sgd_worm.py` — Worm-scale parameter tuning harness already exists.
    - `render_worm.py` — Worm-scale comparison rendering already exists.
- **Approach:** Confirm — visual parity already demonstrated; this issue locks it into CI and commits the canonical worm-scale artifact bundle.
- **Status today:** ✅ Visual parity per DD001 §The Result Quality Gap.
- **Acceptance Criteria:**
    - [ ] Parity test green on `--scenario worm_alone_half_resolution --substrate metal-native`
    - [ ] Side-by-side MP4 committed under `docs/`
    - [ ] SGD convergence history committed
    - [ ] 3–4 spot-check frames with labeled metrics (cylindrical-diameter retention, gravity-drop displacement)
    - [ ] All 10 MoaW PR review checklist items satisfied
- **Sponsor Summary Hint:** The worm-alone scenario tests body mechanics (elastic + anchor bonds, gravity drop, cylindrical-diameter retention) without locomotion or fluid coupling. Already at visual parity; this issue makes it official with CI integration and artifact commits.

---

### Issue [#239](https://github.com/openworm/sibernetic/issues/239): OpenCL ↔ Metal parity on `worm_swim_half_resolution`

- **Title:** `[DD001] OpenCL↔Metal parity on worm_swim_half_resolution — close swim-gait gap`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.1.0** (Native-GPU Substrate Consolidation)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology)
- **Depends On:** Issue [#235](https://github.com/openworm/sibernetic/issues/235) (parity harness), Issue [#238](https://github.com/openworm/sibernetic/issues/238) (worm_alone parity)
- **Existing Code to Reuse:**
    - SPH pressure-force kernel (`pair_forces_pressure_grid`) already implemented (replaces XPBD-only density for water-on-worm dynamics) per DD001 §Extended Position-Based Dynamics.
- **Approach:** Finish — basic swim locomotion validated; remaining work is closing the kinematic-metric gap (swimming velocity, frequency, wavelength) against OpenCL.
- **Status today:** 🟡 Swim parity in progress per DD001 §The Result Quality Gap.
- **Acceptance Criteria:**
    - [ ] Parity test green on `--scenario worm_swim_half_resolution --substrate metal-native`
    - [ ] Swimming velocity, frequency, wavelength within ±5% of OpenCL reference and within DD001 §Validated Kinematic Outputs experimental ranges
    - [ ] Side-by-side MP4 committed under `docs/`
    - [ ] SGD convergence history committed
    - [ ] All 10 MoaW PR review checklist items satisfied
- **Sponsor Summary Hint:** Swimming is the demanding case — full fluid-structure coupling, time-varying muscle activation, and undulatory kinematics that need to land within both the cross-backend parity threshold AND the experimental Schafer-lab ranges. Once this lands, the Metal substrate can be officially graduated to Stable.

---

### Issue [#240](https://github.com/openworm/sibernetic/issues/240): CUDA substrate parity bring-up

- **Title:** `[DD001] CUDA substrate parity bring-up — demo1 first, then mirror Metal trajectory`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.1.0** (Native-GPU Substrate Consolidation)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, cuda, sph
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Stabilization Sequence](DD001_Body_Physics_Architecture.md#stabilization-sequence) (step 5), [§Differentiability](DD001_Body_Physics_Architecture.md#differentiability) (paired-backward architectural mandate)
- **Depends On:** Issue [#235](https://github.com/openworm/sibernetic/issues/235) (parity harness), Issue [#236](https://github.com/openworm/sibernetic/issues/236) (demo1 Metal parity as reference), [PR #229](https://github.com/openworm/sibernetic/pull/229) (sib_cuda — review and merge)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/cuda/`](https://github.com/openworm/sibernetic) — CUDA substrate scaffolding ([PR #229](https://github.com/openworm/sibernetic/pull/229) by @feldmannn). Per `src/cuda/README.md`, the substrate **must** mirror `src/metal_diff/` file-for-file including paired backward kernels per forward kernel.
    - [`openworm/sibernetic/src/metal_diff/`](https://github.com/openworm/sibernetic) — Reference architecture (19 forward + 19 backward kernels). CUDA implementation should follow Metal kernel-for-kernel.
- **Approach:** Bring up — review and merge [PR #229](https://github.com/openworm/sibernetic/pull/229); then port Metal's 19 paired forward/backward kernels and demo1 trajectory dumper to CUDA. Each forward kernel must ship with an FD-validated paired backward per the [Quality Criteria #7](DD001_Body_Physics_Architecture.md#quality-criteria) contract.
- **Acceptance Criteria:**
    - [ ] [PR #229](https://github.com/openworm/sibernetic/pull/229) reviewed and merged
    - [ ] `src/cuda/dump_cuda_trajectory.py` operational (CUDA equivalent of `dump_metal_trajectory.py`)
    - [ ] First wave of forward kernels (density, distance constraints, predict_positions, update_velocities, floor) implemented with paired analytic backwards
    - [ ] FD validators pass at <5% rel-err for each backward kernel
    - [ ] Parity test green on `--scenario demo1 --substrate cuda-native`
    - [ ] Substrate listed as Experimental → Stable in DD001 §Backend Graduation Criteria
- **Sponsor Summary Hint:** The CUDA substrate is the NVIDIA equivalent of the Metal port and the modernization story for the second-largest GPU platform. [PR #229](https://github.com/openworm/sibernetic/pull/229) puts the skeleton in place; this issue brings it through the same 8-phase methodology that got Metal to where it is. The paired-backward architectural mandate is non-negotiable — every forward kernel ships with its analytic backward, FD-validated, or it doesn't land.

---

## Group 3: Substrate Docs & PR Enforcement (Phase A1)

Target: Document what the native substrate is, and stand up an optional Mind-of-a-Worm assist that surfaces the 8-phase Validation Methodology checklist on PRs.

---

### Issue [#241](https://github.com/openworm/sibernetic/issues/241): Document OpenCL kernel architecture (`sphFluid.cl`)

- **Title:** `[DD001] Document OpenCL reference kernel architecture for substrate parity work`
- **Labels:** `DD001`, `human-expert`, `L2`, `phase-0`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.3.0** (Substrate Documentation + Contributor Onboarding)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** opencl, physics, sph
- **DD Section to Read:** [DD001 §Why Native Ports, Not Taichi](DD001_Body_Physics_Architecture.md#why-native-ports-not-taichi), [DD001 §Implementation References](DD001_Body_Physics_Architecture.md#implementation-references)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/sphFluid.cl`](https://github.com/openworm/sibernetic) — The 64KB OpenCL kernel file. THIS is the primary subject.
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Extensive inline documentation of physical constants, particle types, simulation parameters.
- **Approach:** Create — no kernel architecture documentation exists, but the source files themselves contain significant inline comments.
- **Files to Modify:**
    - `docs/opencl_kernel_architecture.md` (new — in Sibernetic repo)
- **Acceptance Criteria:**
    - [ ] Annotated walkthrough of `kernels/sphFluid.cl` (~64KB) — every major function documented
    - [ ] Maps each OpenCL kernel function to its DD001 equation (Wpoly6, ∇Wspiky, ∇²Wviscosity, F_elastic, PCISPH)
    - [ ] Documents coordinate spaces used (world vs. scaled) and where conversions happen — including the `sim_scale` factor and the 0.25 factor on non-worm-body elastic pairs (per [DD001 §Common Gotchas](DD001_Body_Physics_Architecture.md#common-gotchas-distilled-from-the-native-metal-port) item 1)
    - [ ] Documents the PCISPH iteration loop (predict → correct → converge)
    - [ ] Documents neighbor search data structures
    - [ ] Provides a function call graph showing the order of kernel invocations per timestep
    - [ ] Cross-references Metal kernel counterparts in `src/metal_diff/shaders.metal`
- **Sponsor Summary Hint:** The OpenCL kernel file is the 64KB brain of the physics engine — the actual GPU code that moves 100K particles. It's the validated reference every native substrate must match line-for-line. Documenting the kernels makes the parity work tractable: every Metal/CUDA kernel maps to a documented OpenCL counterpart, and the gotchas distilled from the Metal port (the 0.25 factor, the ε guards, the coordinate-space handling) are recorded once instead of relearned by every porter.

---

### Issue [#242](https://github.com/openworm/sibernetic/issues/242): Document the 19 paired forward/backward kernels (differentiable substrate)

- **Title:** `[DD001] Document the 19 paired forward/backward kernels and xpbd_full_bwd reverse-mode pipeline`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.3.0** (Substrate Documentation + Contributor Onboarding)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, sph, autograd
- **DD Section to Read:** [DD001 §Differentiability](DD001_Body_Physics_Architecture.md#differentiability), [§What's Differentiable Today](DD001_Body_Physics_Architecture.md#whats-differentiable-today), [§Multi-Step Reverse-Mode AD](DD001_Body_Physics_Architecture.md#multi-step-reverse-mode-ad-xpbd_full_fwd-xpbd_full_bwd)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/metal_diff/`](https://github.com/openworm/sibernetic) — 19 forward kernels, 19 paired backward kernels, `ops_xpbd_full.mm`, and 19 FD test files.
    - [`openworm/sibernetic/src/cuda/README.md`](https://github.com/openworm/sibernetic) — CUDA substrate's architectural mandate document.
- **Approach:** Create — the kernels exist and the FD tests pass; what's missing is a contributor-facing architecture doc explaining how the pieces fit together and how to add a new paired kernel.
- **Files to Modify:**
    - `docs/differentiable_substrate.md` (new — in Sibernetic repo)
- **Acceptance Criteria:**
    - [ ] Tables each of the 19 forward kernels and its paired backward, with FD-validation tolerance achieved
    - [ ] Explains the saved-state contract that `xpbd_full_fwd` writes and `xpbd_full_bwd` consumes (positions, velocities, density, ∇C, denominator helpers, per-kernel auxiliaries)
    - [ ] Explains `BWD_CLIP_NORM` and TBPTT support
    - [ ] Walks through the procedure for adding a new paired kernel (forward implementation, analytic backward derivation, FD test, hookup into `ops_xpbd_full.mm`)
    - [ ] Documents what's NOT (yet) differentiable: OpenCL reference (forward-only), CUDA substrate (scaffolding stage)
    - [ ] Cross-references the SGD harness scripts (`sgd_*.py`) as worked examples
- **Sponsor Summary Hint:** The native-Metal substrate is end-to-end differentiable — 19 forward kernels each have an FD-validated analytic backward, and `xpbd_full_bwd` walks K constraint-projection steps in reverse to produce parameter gradients. This is DD001's most-distinguishing architectural property and the design contract the CUDA substrate must mirror, but it's currently undocumented outside the code itself. This issue creates the substrate's autograd architecture doc.

---

### Issue [#243](https://github.com/openworm/sibernetic/issues/243): Mind-of-a-Worm 8-phase Validation Methodology PR assist

- **Title:** `[DD001] Mind-of-a-Worm PR assist surfacing the 8-phase Validation Methodology checklist`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`
- **Roadmap Phase:** Phase A1
- **Milestone:** **v0.3.0** (Substrate Documentation + Contributor Onboarding)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** ci-cd, python, github-api
- **DD Section to Read:** [DD001 §Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology), [§MoaW PR Review Checklist](DD001_Body_Physics_Architecture.md#mind-of-a-worm-pr-review-checklist), [DD001 Quality Criteria #8](DD001_Body_Physics_Architecture.md#quality-criteria) (Validation Methodology Followed)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/metal_diff/tests/test_demo1_backend_parity.py`](https://github.com/openworm/sibernetic) — Existing parity gate; the assist can shell out to it.
    - Mind-of-a-Worm GitHub bot scaffolding (see [AI Contributors](../contributing/ai-contributors.md))
- **Approach:** Create — there's no automated assist today. Build a GitHub Actions workflow that runs on PRs touching `src/sphFluid*.cl`, `src/metal_diff/**`, or `src/cuda/**` and posts a checklist-status comment summarizing which of the 10 items appear present. Approval and merge decisions stay with human reviewers.
- **Files to Modify:**
    - `.github/workflows/validation_methodology.yml` (new)
    - `scripts/moaw_checklist.py` (new — applies the 10-item checklist against the PR diff and committed artifacts)
- **Acceptance Criteria:**
    - [ ] Workflow triggers on PRs touching kernel sources or substrate code
    - [ ] Surfaces the status of each checklist item: written prediction, OpenCL reference trajectory, Metal/CUDA trajectory dump, side-by-side MP4 under `docs/`, SGD convergence history, FD test for any new kernel
    - [ ] Workflow posts a checklist-status comment on the PR (does **not** block merge; reviewers decide)
    - [ ] Documented in `CONTRIBUTING.md` (Issue [#248](https://github.com/openworm/sibernetic/issues/248)) and DD001 itself
- **Sponsor Summary Hint:** DD001's Validation Methodology gives reviewers a 10-item checklist to walk through. This issue makes that checklist easier to apply by posting an automated summary on each kernel-touching PR — "here's which items I can verify are present, here's what's missing." The bot is an assistant, not a gatekeeper: human reviewers decide whether a PR is ready to merge.

---

## Group 4: Output Pipeline & Viewer Bridge (Phase A1/1)

Target: Sibernetic produces output in formats that DD010 (validation), DD011 (simulation stack), and the visualization stage can consume.

---

### Issue [#244](https://github.com/openworm/sibernetic/issues/244): Implement OME-Zarr export for particle data

- **Title:** `[DD001] Implement OME-Zarr export for body/positions and body/types`
- **Labels:** `DD001`, `ai-workable`, `L2`, `phase-0`
- **Roadmap Phase:** Phase A1/1
- **Milestone:** **v0.2.0** (Validation Infrastructure + Output Pipeline)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 §Deliverables](DD001_Body_Physics_Architecture.md#deliverables) (OME-Zarr rows) and [DD001 §How to Visualize](DD001_Body_Physics_Architecture.md#how-to-visualize)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owVtkExport.h`](https://github.com/openworm/sibernetic) — VTK export already exists for particle data visualization. Reference for how particle data is extracted and formatted for external tools.
    - [`openworm/sibernetic/wcon/generate_wcon.py`](https://github.com/openworm/sibernetic) — Shows how to read Sibernetic output files from Python. Reference for I/O patterns.
- **Approach:** Create — no OME-Zarr export exists. Use `owVtkExport.h` and `generate_wcon.py` as references for how particle data is accessed.
- **DD011 Pipeline Role:** Body-stage post-processing. Runs after Sibernetic simulation completes. Produces Zarr store artifact at path configured via `openworm.yml` for the downstream visualization stage.
- **Files to Modify:**
    - `scripts/export_zarr.py` (new)
- **Test Commands:**
    - `python3 scripts/export_zarr.py output.dat --output output/openworm.zarr`
    - `python3 -c "import zarr; z = zarr.open('output/openworm.zarr'); print(z['body/positions'].shape, z['body/types'].shape)"`
- **Acceptance Criteria:**
    - [ ] Reads Sibernetic binary output and exports to OME-Zarr format
    - [ ] `body/positions/` array: shape `(n_timesteps, n_particles, 3)`, dtype float32
    - [ ] `body/types/` array: shape `(n_particles,)`, dtype int32 (0=liquid, 1=elastic, 2=boundary)
    - [ ] Export interval configurable (every Nth output frame)
    - [ ] Handles typical simulation sizes (~100K particles × ~500 frames) without OOM
    - [ ] Includes OME-Zarr metadata (axes labels, units)
- **Sponsor Summary Hint:** OME-Zarr is the universal data format connecting simulation to visualization. This script converts Sibernetic's raw binary output into a structured Zarr store that the downstream viewer can read — the bridge between physics engine and interactive visualization. The existing `owVtkExport.h` shows how particle data is already extracted for VTK; this creates the OME-Zarr equivalent.

---

### Issue [#245](https://github.com/openworm/sibernetic/issues/245): Implement surface mesh reconstruction from SPH particles

- **Title:** `[DD001] Implement marching cubes surface reconstruction from SPH particles`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`
- **Roadmap Phase:** Phase A1/1
- **Milestone:** **v0.2.0** (Validation Infrastructure + Output Pipeline)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, 3d-geometry
- **DD Section to Read:** [DD001 §Deliverables](DD001_Body_Physics_Architecture.md#deliverables) (surface mesh row), [DD001 §How to Visualize](DD001_Body_Physics_Architecture.md#how-to-visualize)
- **Depends On:** Issue [#244](https://github.com/openworm/sibernetic/issues/244) (OME-Zarr export)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/inc/owVtkExport.h`](https://github.com/openworm/sibernetic) — VTK export for particle visualization. Can serve as the input reader for surface reconstruction.
    - [`openworm/skeletonExtraction`](https://github.com/openworm/skeletonExtraction) — C++ skeleton extraction from Sibernetic mesh output (3D graphics skeleton for animation). Different purpose (animation skeleton vs. surface mesh) but related geometry processing on the same particle data.
- **Approach:** Extend — build on `owVtkExport.h` for particle data access and reference `skeletonExtraction` for geometry processing patterns on Sibernetic output.
- **DD011 Pipeline Role:** Body-stage post-processing. Runs after OME-Zarr export. Adds `geometry/body_surface/` group to the Zarr store for the viewer.
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

### Issue [#246](https://github.com/openworm/sibernetic/issues/246): Configurable output frequency via `openworm.yml`

- **Title:** `[DD001] Implement configurable output frequency from openworm.yml simulation.output_interval`
- **Labels:** `DD001`, `ai-workable`, `L2`, `phase-0`
- **Roadmap Phase:** Phase A1/1
- **Milestone:** **v0.2.0** (Validation Infrastructure + Output Pipeline)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, c++
- **DD Section to Read:** [DD001 §Configuration](DD001_Body_Physics_Architecture.md#configuration), DD011 (Simulation Stack — `simulation.output_interval` key)
- **Depends On:** DD011 master_openworm config loading
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/owPhysicsFluidSimulator.cpp`](https://github.com/openworm/sibernetic) — Contains the output writing logic. The output frequency is controlled here.
- **Approach:** Create — no configurable output frequency exists. Modify the output loop in `owPhysicsFluidSimulator.cpp` to respect an interval parameter; thread it through the native substrate trajectory dumpers as well.
- **DD011 Pipeline Role:** Body-stage configuration. `master_openworm.py` passes `simulation.output_interval` from `openworm.yml` to Sibernetic via command-line argument.
- **Files to Modify:**
    - `src/owPhysicsFluidSimulator.cpp` (output frequency)
    - `src/metal_diff/dump_metal_trajectory.py` (mirror the flag for the Metal trajectory dumper)
    - Sibernetic command-line argument parsing
- **Test Commands:**
    - `./build/Sibernetic -f configuration/worm_crawl_demo -output_interval 100`
    - `ls output/ | wc -l` (verify expected number of output files)
- **Acceptance Criteria:**
    - [ ] Sibernetic accepts `--output_interval N` command-line argument
    - [ ] Output frames written every N timesteps (default: 100)
    - [ ] `master_openworm.py` passes `simulation.output_interval` from `openworm.yml` to Sibernetic
    - [ ] Same flag plumbed through `dump_metal_trajectory.py` (consistent behavior across substrates)
    - [ ] Reducing output interval does not affect simulation accuracy (only I/O frequency)
    - [ ] Quick-test uses high interval (less output, faster), validation uses low interval (more output, thorough)
- **Sponsor Summary Hint:** How often the simulation saves its state to disk. Writing every timestep generates enormous files (100K particles × 50,000 steps = terabytes). Writing every 100th step is a good balance. This makes output frequency configurable so quick tests save less data and validation runs save more.

---

## Group 5: Documentation & Onboarding (Any Phase)

Target: Comprehensive documentation enabling new contributors to understand and modify Sibernetic. **Note:** Two previously-drafted issues in this group (config-onboarding docs and inline parameter comments) have been folded into the existing live issues [#165](https://github.com/openworm/sibernetic/issues/165) and [#128](https://github.com/openworm/sibernetic/issues/128) — see [Migration Context](#migration-context-stabilize-the-gold-standard-while-building-forward). Those community-tracked threads carry the work; no separate fresh issues are filed.

---

### Issue [#247](https://github.com/openworm/sibernetic/issues/247): Sibernetic architecture overview for new contributors

- **Title:** `[DD001] Create Sibernetic architecture overview for contributors`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Milestone:** **v0.3.0** (Substrate Documentation + Contributor Onboarding)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD001 §Technical Approach](DD001_Body_Physics_Architecture.md#technical-approach), [DD001 §Implementation References](DD001_Body_Physics_Architecture.md#implementation-references)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/README.md`](https://github.com/openworm/sibernetic) — 17.5KB README with build instructions, usage examples, and project overview. Start from this as the foundation and expand into a structured architecture document.
    - [`openworm/sibernetic/inc/owPhysicsConstant.h`](https://github.com/openworm/sibernetic) — Extensive inline documentation of simulation parameters and physics constants.
- **Approach:** Extend — the README and well-documented `owPhysicsConstant.h` provide substantial content to build on.
- **Files to Modify:**
    - `docs/architecture.md` (new — in Sibernetic repo)
- **Acceptance Criteria:**
    - [ ] High-level overview: what Sibernetic is, what it produces, who uses its output
    - [ ] File map: which source files contain which functionality (OpenCL reference, native Metal substrate, native CUDA scaffolding)
    - [ ] Data flow diagram: input config → particle init → SPH/XPBD loop → output
    - [ ] Timestep walkthrough: what happens in one simulation step (neighbor search → density → pressure → forces → integrate for SPH; predict → constraints → update for XPBD)
    - [ ] Backend comparison: OpenCL (gold-standard reference, losing platform support) vs. native Metal (Apple Silicon, end-to-end differentiable) vs. native CUDA (NVIDIA, scaffolding)
    - [ ] References to DD001 for specification details
    - [ ] Aimed at L2 contributors (familiar with physics but new to codebase)
- **Sponsor Summary Hint:** New contributors need a map before they can navigate. This document explains what each file does, how data flows through the simulation, and what happens in a single timestep — both for the OpenCL reference and the native Metal substrate. DD001 is the specification (what should happen); this is the implementation guide (where the code lives and how it works).

---

### Issue [#248](https://github.com/openworm/sibernetic/issues/248): Sibernetic CONTRIBUTING.md with substrate workflow

- **Title:** `[DD001] Create CONTRIBUTING.md with native-substrate development workflow and standards`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Milestone:** **v0.3.0** (Substrate Documentation + Contributor Onboarding)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD001 §Quality Criteria](DD001_Body_Physics_Architecture.md#quality-criteria), [DD001 §Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/README.md`](https://github.com/openworm/sibernetic) — 17.5KB README with build instructions. Reference for build workflow.
- **Approach:** Create — no CONTRIBUTING.md exists. Use the README and DD001 §Validation Methodology as the foundation.
- **Files to Modify:**
    - `CONTRIBUTING.md` (new — in Sibernetic repo)
- **Acceptance Criteria:**
    - [ ] Prerequisites: what to install for OpenCL reference + native Metal substrate + native CUDA scaffolding
    - [ ] Build instructions for each substrate
    - [ ] Testing workflow: unit tests → stability check → incompressibility check → cross-backend parity test
    - [ ] PR checklist from DD001 §Quality Criteria (all 8 criteria) AND the 10-item MoaW PR review checklist
    - [ ] Explicit pointer to the 8-phase Validation Methodology with examples
    - [ ] Branch naming convention: `dd001/description`
    - [ ] How to add a new kernel to the native substrate (paired-backward contract from §Differentiability)
    - [ ] How to run the cross-backend parity test suite (Issue [#235](https://github.com/openworm/sibernetic/issues/235))
    - [ ] Links to DD001 for specifications
- **Sponsor Summary Hint:** A CONTRIBUTING.md is the entry point for any developer. This one specifically guides physics-engine contributors through the multi-substrate testing workflow — build, test, compare against OpenCL baseline, satisfy the 8-phase Validation Methodology, submit PR. Without it, contributors won't know which tests to run or what quality bar to meet.

---

## Group 6: Advanced / Future Backend Direction (Phase 2+)

Target: Evaluate complementary backend approaches and expose programmatic access.

---

### Issue [#249](https://github.com/openworm/sibernetic/issues/249): Evaluate FEM Projective Dynamics backend feasibility

- **Title:** `[DD001] Evaluate Projective Dynamics FEM backend feasibility (Zhao et al. / BAAIWorm / Metaworm)`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 2+
- **Milestone:** Unmilestoned (future / research)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, c++, cuda
- **DD Section to Read:** [DD001 §Alternatives Considered — FEM](DD001_Body_Physics_Architecture.md#1-finite-element-method-fem) (the "Update 2026-02" section laying out the BAAIWorm direction)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`Jessie940611/BAAIWorm/Metaworm/sim/fem/`](https://github.com/Jessie940611/BAAIWorm) — Complete FEM Projective Dynamics implementation: `FEMSolver.cpp`, `Constraint.cpp`, `Muscle.cpp`, `World.cpp`. 984-vertex tetrahedral mesh, 96-muscle actuator model, ~30 FPS.
    - [`Jessie940611/BAAIWorm/Metaworm/data/worm_mesh_4.obj`](https://github.com/Jessie940611/BAAIWorm) — Ready-to-use FEM mesh: 984 vertices, 3,341 tetrahedrons.
- **Approach:** Evaluate — comprehensive feasibility study of the BAAIWorm/Metaworm FEM implementation for integration as an alternative Sibernetic backend.
- **Files to Modify:**
    - None (research issue — output is a feasibility report posted on the issue)
- **Acceptance Criteria:**
    - [ ] Clone and build BAAIWorm/Metaworm FEM solver (`sim/fem/`)
    - [ ] Document: build requirements — CUDA version, OptiX 7.x for rendering, C++17 compiler
    - [ ] Document: muscle actuator interface — verify mapping compatibility with the 96-muscle activation array
    - [ ] Document: constraint system — strain limits, volume preservation, attachment constraints
    - [ ] Document: physics fidelity — surface hydrodynamics only (no internal fluid simulation, unlike SPH)
    - [ ] Assess: effort to wrap as `body.backend: "fem-projective"` in the OpenWorm stack
    - [ ] Assess: CUDA/OptiX dependency — can it run on Apple Silicon? CI? (likely no — CUDA required)
    - [ ] Post feasibility report with go/no-go recommendation
- **Sponsor Summary Hint:** Zhao et al. (2024) demonstrated a worm body simulation running at 30 FPS using Projective Dynamics FEM — orders of magnitude faster than our SPH approach. Their code (BAAIWorm/Metaworm) is open source. This feasibility study determines whether we can add it as a "fast mode" backend for rapid iteration and CI testing, complementing the physically richer SPH and the differentiable native-Metal substrate.

---

### Issue [#250](https://github.com/openworm/sibernetic/issues/250): Sibernetic Python bindings for direct API access (replaces [#122](https://github.com/openworm/sibernetic/issues/122))

- **Title:** `[DD001] Create Python bindings for Sibernetic C++ library (formalize the existing CPython integration)`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 2+
- **Milestone:** Unmilestoned (future / research)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, c++, pybind11
- **DD Section to Read:** [DD001 §Integration Contract](DD001_Body_Physics_Architecture.md#integration-contract)
- **Depends On:** None
- **Replaces:** Closed issue [#122](https://github.com/openworm/sibernetic/issues/122) (pySibernetic, 2017 external wrapper)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/src/owSignalSimulator.cpp`](https://github.com/openworm/sibernetic) — Already contains a CPython API integration layer using direct `PyObject` calls to interface with NEURON/c302. C++↔Python interop already exists in the codebase; the question is formalization.
- **Approach:** Extend — build on the existing CPython API calls in `owSignalSimulator.cpp`. Two viable paths: (a) formalize with pybind11 for a clean public API, (b) extend the existing CPython embedding for backward compatibility.
- **Note:** Sibernetic uses a Makefile build system (the CMake migration of [PR #214](https://github.com/openworm/sibernetic/pull/214) is the current build path). Adding pybind11 will integrate with the current build path.
- **Files to Modify:**
    - `python/sibernetic_bindings.cpp` (new — pybind11 wrapper)
    - `python/sibernetic/__init__.py` (new — Python package)
    - `CMakeLists.txt` (add pybind11 target)
    - `pyproject.toml` (new — pip installable)
- **Test Commands:**
    - `pip install -e .`
    - `python3 -c "import sibernetic; sim = sibernetic.Simulation('configuration/worm_crawl_demo'); sim.step()"`
- **Acceptance Criteria:**
    - [ ] `pip install` produces a `sibernetic` Python package
    - [ ] Python API exposes: `Simulation(config_path)`, `.step()`, `.get_positions()`, `.get_velocities()`, `.get_densities()`
    - [ ] Can inject muscle forces from Python: `sim.set_muscle_activation(quadrant, value)`
    - [ ] Can read particle state without file I/O (direct memory access)
    - [ ] Works with OpenCL backend (C++ core + Python wrapper)
    - [ ] Enables `sibernetic_c302.py` to call Sibernetic directly instead of via subprocess
    - [ ] Pybind11 wraps the existing C++ API; no algorithmic changes
- **Sponsor Summary Hint:** Currently the neural circuit (Python) and body physics (C++) communicate via file I/O. Python bindings would allow direct function calls, dramatically simplifying the coupling code and eliminating file I/O bottlenecks. The existing `owSignalSimulator.cpp` already has CPython API calls — this formalizes that into a proper Python package, replacing the 2017 community-offered `pySibernetic` wrapper ([#122](https://github.com/openworm/sibernetic/issues/122)) with a maintained in-tree binding.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Fresh issues to file** | 18 |
| **ai-workable** | 12 |
| **human-expert** | 6 |
| **L1** | 6 |
| **L2** | 7 |
| **L3** | 5 |
| **Existing issues kept live** | ~12 (see [Migration Context](#migration-context-stabilize-the-gold-standard-while-building-forward)) |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Validation Infrastructure** | [#233](https://github.com/openworm/sibernetic/issues/233)–[#235](https://github.com/openworm/sibernetic/issues/235) | Stability/incompressibility scripts + cross-backend parity harness |
| **2: Per-Demo Parity & CUDA Bring-Up** | [#236](https://github.com/openworm/sibernetic/issues/236)–[#240](https://github.com/openworm/sibernetic/issues/240) | Close OpenCL↔Metal parity per demo; stand up CUDA |
| **3: Substrate Docs & PR Assist** | [#241](https://github.com/openworm/sibernetic/issues/241)–[#243](https://github.com/openworm/sibernetic/issues/243) | Document substrate + surface Validation Methodology checklist on PRs |
| **4: Output Pipeline** | [#244](https://github.com/openworm/sibernetic/issues/244)–[#246](https://github.com/openworm/sibernetic/issues/246) | OME-Zarr, surface mesh, configurable output |
| **5: Documentation & Onboarding** | [#247](https://github.com/openworm/sibernetic/issues/247)–[#248](https://github.com/openworm/sibernetic/issues/248) | Architecture overview, CONTRIBUTING.md (config-docs work folded into existing [#128](https://github.com/openworm/sibernetic/issues/128), [#165](https://github.com/openworm/sibernetic/issues/165)) |
| **6: Advanced / Future** | [#249](https://github.com/openworm/sibernetic/issues/249)–[#250](https://github.com/openworm/sibernetic/issues/250) | FEM evaluation, Python bindings |

### Dependency Graph (Critical Path)

```
Issue [#233](https://github.com/openworm/sibernetic/issues/233) (check_stability.py) ─┐
Issue [#234](https://github.com/openworm/sibernetic/issues/234) (incompressibility.py)┤
                                 ├→ Issue [#235](https://github.com/openworm/sibernetic/issues/235) (parity harness) ─┬→ Issue [#236](https://github.com/openworm/sibernetic/issues/236) (demo1 parity, mostly done)
                                 │                               ├→ Issue [#237](https://github.com/openworm/sibernetic/issues/237) (demo2 parity — close gap)
                                 │                               ├→ Issue [#238](https://github.com/openworm/sibernetic/issues/238) (worm_alone parity)
                                 │                               ├→ Issue [#239](https://github.com/openworm/sibernetic/issues/239) (worm_swim parity — close gap)
                                 │                               └→ Issue [#240](https://github.com/openworm/sibernetic/issues/240) (CUDA bring-up; also depends on [PR #229](https://github.com/openworm/sibernetic/pull/229))
                                 │
Issue [#241](https://github.com/openworm/sibernetic/issues/241) (OpenCL kernel docs) ─┘  (feeds parity work, not blocking)

Issue [#242](https://github.com/openworm/sibernetic/issues/242) (paired backward docs) — independent; pairs with Issue [#243](https://github.com/openworm/sibernetic/issues/243)
Issue [#243](https://github.com/openworm/sibernetic/issues/243) (MoaW PR assist) — independent; depends on existing parity test for one of its acceptance items

Issue [#244](https://github.com/openworm/sibernetic/issues/244) (OME-Zarr export) → Issue [#245](https://github.com/openworm/sibernetic/issues/245) (surface mesh)
Issue [#246](https://github.com/openworm/sibernetic/issues/246) (output frequency) — depends on DD011 config loading

Issue [#247](https://github.com/openworm/sibernetic/issues/247) (architecture overview) — independent
Issue [#248](https://github.com/openworm/sibernetic/issues/248) (CONTRIBUTING.md) — depends on Issues [#235](https://github.com/openworm/sibernetic/issues/235), [#241](https://github.com/openworm/sibernetic/issues/241), [#242](https://github.com/openworm/sibernetic/issues/242), [#243](https://github.com/openworm/sibernetic/issues/243) being defined (but not done)

Issue [#249](https://github.com/openworm/sibernetic/issues/249) (FEM evaluation) — independent research
Issue [#250](https://github.com/openworm/sibernetic/issues/250) (Python bindings) — independent
```
