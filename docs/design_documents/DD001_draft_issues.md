# DD001 Draft GitHub Issues

!!! warning "Internal planning document — to be deleted before master merge"
    This file exists to plan the openworm/sibernetic GitHub issues that will derive from DD001. Once the issues are filed on GitHub, **this entire document is to be deleted** and removed from the mkdocs nav. It is not part of the public design-document set. The canonical source of truth for implementation work is the issue tracker itself ([`label:dd001`](https://github.com/openworm/sibernetic/labels/dd001)) and the [release milestones](https://github.com/openworm/sibernetic/milestones).

**Epic:** DD001 — Body Physics Engine (Sibernetic) Architecture

**Generated from:** [DD001: Body Physics Engine Architecture](DD001_Body_Physics_Architecture.md)

**Methodology:** [§2.2 — DD Issue Generator](../contributing/ai-contributors.md#22-the-dd-issue-generator-automated-issue-creation), [§2.3 — Reuse-First Issue Design](../contributing/ai-contributors.md#23-reuse-first-issue-design), [§2.4 — DD011 Simulation Stack Integration](../contributing/ai-contributors.md#24-dd011-simulation-stack-integration)

**Totals:** 18 fresh issues to file (ai-workable: 8 / human-expert: 10 | L1: 7, L2: 7, L3: 4) **plus** ~12 existing issues kept live (see [Migration Context](#migration-context-stabilize-the-gold-standard-while-building-forward) below). **Per-issue audit complete (2026-05-28)** — each issue right-sized against existing Sibernetic infrastructure; three originally-proposed issues dropped (see [Considered and Dropped](#considered-and-dropped-after-audit) below).

**Roadmap Context:** DD001 is a **Phase 0** DD (existing, working). Its draft issues span multiple roadmap phases:

| Group | Milestone | Issues |
|-------|-----------|--------|
| 1. Parity Harness + Per-Demo Parity + CUDA Phase 3 | **v0.0.9 — Phase 0 Modernization** | [#236](#issue-236-generalize-teststest_demo1_backend_paritypy-into-a-scenario-registry-harness) generalize parity harness, [#237](#issue-237-lock-demo1-parity-test-into-ci) demo1 lock-in, [#238](#issue-238-add-demo2-membrane-permeability-parity-gate-to-harness) demo2 harness entry, [#239](#issue-239-add-worm_alone-parity-gate-worm-com-cross-section-max-span-metrics) worm_alone lock-in, [#240](#issue-240-implement-ihmsen-2010-boundary-active-sph-pressure-replaces-floor_y-proxy) Ihmsen 2010 boundary pressure, [#241](#issue-241-rewrite-xpbd-density-inner-loop-with-pcisph-iterative-pressure) PCISPH iterative pressure, [#242](#issue-242-worm_swim_half_resolution-set-up-muscle-driven-scenario-and-add-parity-gate) worm_swim driven scenario, [#243](#issue-243-cuda-phase-3-port-wpoly6_inplace-prove-nvcc-build-fd-validate-against-metal) CUDA Phase 3 |
| 2. Validation Tooling + Output Pipeline | **v0.1.0 — Phase 1 Validation Infrastructure** | [#233](#issue-233-extend-scriptsmeasure_cube_stabilitypy-with-nanescapevelocity-checks) extend stability checker, [#234](#issue-234-emit-per-particle-density-alongside-position-output-both-substrates) emit per-particle density, [#235](#issue-235-create-scriptsvalidate_incompressibilitypy-depends-on-234) incompressibility checker, [#247](#issue-247-ome-zarr-post-processing-converter-contingent-on-dd012-viewer-contract) OME-Zarr converter, [#248](#issue-248-plumb-simulationoutput_interval-from-openwormyml-through-to-existing-logstep-knob) output-interval plumbing |
| 3. Substrate Docs + Contributor Onboarding | **v0.1.1 — Phase 1 Substrate Documentation** | [#244](#issue-244-add-opencl-kernel-call-graph-equation-table-gotchas-appendix) OpenCL kernel call graph, [#245](#issue-245-document-xpbd_full-saved-state-contract-add-a-paired-kernel-runbook) paired-kernel runbook, [#246](#issue-246-static-github-action-post-validation-methodology-checklist-on-substrate-touching-prs) static-action PR checklist, [#249](#issue-249-add-contributingmd-link-heavy-owns-only-what-has-no-other-home) link-heavy CONTRIBUTING.md |
| 4. Closed-Loop | **v0.4.0 — Phase 4 Sensory Coupling** | [#250](#issue-250-in-process-simulation-handle-for-tight-loop-closed-loop-control) in-process Simulation handle |

---

## Issue Numbering

The 18 fresh issues below are labeled with **predicted** GitHub issue numbers (`#233` through `#250`) based on the current `openworm/sibernetic` numbering high-water mark (#232, a closed PR, as of 2026-05-28). Actual numbers assigned at filing time will shift forward if other issues or PRs are opened on the repo first. After filing, this document should be updated to reflect the assigned numbers.

---

## Migration Context: Stabilize the Gold Standard While Building Forward

The 31 pre-existing `openworm/sibernetic` open issues have been re-evaluated with a more careful lens: **OpenCL is DD001's gold-standard reference implementation, and the native Metal / CUDA substrates must reach parity against it.** That means stabilizing OpenCL — fixing its bugs, documenting its behavior, exposing its parameters — is *supporting* work for the modernization, not a distraction from it. Issues that were earlier slated for blanket closure-as-superseded have been re-bucketed: real OpenCL defects, real docs gaps, and real build problems are kept live as **gold-standard stabilization** work. Issues that genuinely belong to held-back DDs (visualization, closed-loop touch, proprioception, foundation models) or duplicate other issues remain candidates for closure.

As of 2026-05-28, **27 issues remain open**, and 4 were closed in the last week ([#102](https://github.com/openworm/sibernetic/issues/102), [#130](https://github.com/openworm/sibernetic/issues/130), [#176](https://github.com/openworm/sibernetic/issues/176), [#221](https://github.com/openworm/sibernetic/issues/221)). Of the 27 open, ~12 are kept live, ~3 are folded into fresh DD001-derived issues, and ~12 will close with structured archive comments referencing DD001 or a held-back DD.

### Live issues (kept open, re-labeled by category)

#### A. OpenCL reference defects (real bugs, gold-standard stabilization)

| Issue | Title | Milestone | Why live |
|-------|-------|-----------|----------|
| [#125](https://github.com/openworm/sibernetic/issues/125) | Worm_motion_log contains only zeros in full scale resolution worm | **v0.0.8 — Phase 0 Stabilization** | Real OpenCL output bug, assigned to @a-palyanov. The output system is what every Metal/CUDA parity test compares against — fix it. **Label:** `opencl`, `bug`, `gold-standard` |
| [#126](https://github.com/openworm/sibernetic/issues/126) | Liquid particles streaming out of standard cube | **v0.0.8 — Phase 0 Stabilization** | Real OpenCL physics bug on `demo1` (the cube drop scenario that the Metal port already passes). If the reference itself is leaking particles, parity claims are meaningless. **Label:** `opencl`, `bug`, `gold-standard` |
| [#136](https://github.com/openworm/sibernetic/issues/136) | CL_OUT_OF_RESOURCES on Nvidia GTX 1060 copying position buffer | **v0.0.8 — Phase 0 Stabilization** | Real OpenCL HW-portability bug. Anyone reproducing on the listed NVIDIA generation hits it. **Label:** `opencl`, `bug`, `hardware-specific` |
| [#160](https://github.com/openworm/sibernetic/issues/160) | Pressure buffer file issue | **v0.0.8 — Phase 0 Stabilization** | Concrete repro from 2019 — verify still reproduces on current master. **Label:** `opencl`, `bug`, `needs-reproduction-current` |
| [#180](https://github.com/openworm/sibernetic/issues/180) | Resolve compiler warnings | **v0.0.8 — Phase 0 Stabilization** | Code-quality cleanup against current master (compiler warnings drift with toolchains). Good first issue. **Label:** `code-quality`, `good-first-issue` |
| [#223](https://github.com/openworm/sibernetic/issues/223) | makefile.OSX doesn't work on M series Mac | **v0.0.8 — Phase 0 Stabilization** | Build path still partially broken on ARM Mac (setup.sh helps but doesn't cover all entry points). **Label:** `build`, `apple-silicon` |

#### B. OpenCL reference enhancements + docs (low-risk, high-value)

| Issue | Title | Milestone | Why live |
|-------|-------|-----------|----------|
| [#127](https://github.com/openworm/sibernetic/issues/127) | Worm body modelling and mechanics — parameters, values etc. | **v0.1.1 — Phase 1 Substrate Documentation** | 12-comment discussion thread on parameter values (Young's modulus, etc.). Capture the canonical values in the codebase / config docs. **Label:** `docs`, `physics` |
| [#128](https://github.com/openworm/sibernetic/issues/128) | Enhance configuration files with physical parameters specific to full/half resolution | **v0.1.1 — Phase 1 Substrate Documentation** | Expose physical params through config rather than hard-coded in source. Reduces the "magic numbers" problem and helps reproducibility. **Label:** `enhancement`, `config` |
| [#147](https://github.com/openworm/sibernetic/issues/147) | How to expand the liquid particles? | **v0.0.8 — Phase 0 Stabilization** | Real docs gap. Pairs with [#148](https://github.com/openworm/sibernetic/issues/148). Bundled with stabilization since the answer is part of the gold-standard usage docs. **Label:** `docs`, `good-first-issue` |
| [#148](https://github.com/openworm/sibernetic/issues/148) | Document the way to access the body position on each step? | **v0.0.8 — Phase 0 Stabilization** | Real docs gap. Pairs with [#147](https://github.com/openworm/sibernetic/issues/147). Bundled with stabilization for the same reason. **Label:** `docs`, `good-first-issue` |
| [#165](https://github.com/openworm/sibernetic/issues/165) | User-defined geometries and muscle models | **v0.1.1 — Phase 1 Substrate Documentation** | 18-comment community thread. Custom-geometry workflow is the right scope; the fresh "config-onboarding docs" issue I previously proposed folds back into this one. **Label:** `docs`, `community-interest` |
| [#224](https://github.com/openworm/sibernetic/issues/224) | `QUEUE_EACH_KERNEL` OpenCL profiling flag | **v0.0.8 — Phase 0 Stabilization** | Clean profiling enhancement to the reference backend; fits the stabilization release. **Label:** `opencl`, `enhancement`, `good-first-issue` |

#### C. Modernization tracking

| Issue | Title | Milestone | Why live |
|-------|-------|-----------|----------|
| [#226](https://github.com/openworm/sibernetic/issues/226) | Port sphFluid.cl to Metal for ARM64 Mac | **v0.0.9 — Phase 0 Modernization** | Canonical tracking issue for the Metal port. Wei Weng's filing is the statement of need that DD001 §Backend Stabilization Roadmap formalizes. The per-demo parity work (Issues [#237](#issue-237-lock-demo1-parity-test-into-ci) – [#242](#issue-242-worm_swim_half_resolution-set-up-muscle-driven-scenario-and-add-parity-gate)) consolidates implementation under this umbrella. Closes when v0.0.9 (Phase 0 Modernization) ships. **Label:** `native-gpu`, `phase-0`, `epic` |

### Issues to defer to later milestones (was: "close as superseded")

Earlier framing treated most non-Live issues as candidates for closure. Re-evaluating: a deferred-with-milestone disposition preserves contributor intent (the issue is *acknowledged* as in-scope eventually), keeps the discussion thread discoverable, and gives community contributors a target release if they want to pick the work up. **Most issues that would have been "closed as superseded" should instead be re-labeled, milestoned, and left open with a comment explaining the deferral.**

The milestones below extend the four-milestone plan with v0.4.0 (Phase 4 Sensory Coupling) and v0.3.0 (Phase 3 Visualization Enhancements) (covered in the [Milestones](#milestones) table). Per-issue dispositions:

| Issue | Defer to milestone | Add labels | Comment to post |
|-------|--------------------|-----------|-----------------|
| [#100](https://github.com/openworm/sibernetic/issues/100) | **v0.4.0 — Phase 4 Sensory Coupling** | `closed-loop`, `dd019`, `deferred` | Closed-loop neural control of worm steering needs the bidirectional Sibernetic↔neural coupling that lands under DD019 (Closed-Loop Touch Response — currently held back). Deferring to v0.4.0 (Phase 4 Sensory Coupling), which will pick this scope up once DD019 publishes. Original 2016 scope preserved here for reference. Current Sibernetic spec: [DD001](https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/). |
| [#163](https://github.com/openworm/sibernetic/issues/163) | **v0.4.1 — Phase 4 Environmental Modeling** | `environment`, `dd018`, `deferred` | Chemical species / molecular environment simulation is out of scope for DD001 (per its §Boundaries item 3, "beyond liquid/gel") but **in scope for DD018 — Environmental Modeling and Stimulus Delivery**, which is held back but on the [Phase 4 roadmap](DD_PHASE_ROADMAP.md#phase-4-slow-modulation-closed-loop-sensory) (chemotaxis on simulated NaCl gradient, thermotaxis). Deferring to v0.4.1 (Phase 4 Environmental Modeling), which will pick this scope up once DD018 publishes. |
| [#141](https://github.com/openworm/sibernetic/issues/141) | **v0.4.0 — Phase 4 Sensory Coupling** | `proprioception`, `dd019`, `deferred` | Stretch-receptor / proprioceptive feedback is the scope of DD019 (currently held back). Deferring to v0.4.0 (Phase 4 Sensory Coupling). The detailed checklist (zeroGinitTime, per-muscle length ratio extraction) is preserved in this thread as scope reference for when DD019 publishes. |
| [#144](https://github.com/openworm/sibernetic/issues/144) | **v0.4.0 — Phase 4 Sensory Coupling** | `touch`, `dd015`, `deferred` | MEC-4 mechanosensation and tap-withdrawal touch sensation is the scope of DD015 (currently held back). Deferring to v0.4.0 (Phase 4 Sensory Coupling), which will derive fresh issues from DD015 when it publishes. |
| [#101](https://github.com/openworm/sibernetic/issues/101) | **v0.3.0 — Phase 3 Visualization Enhancements** | `visualization`, `dd012`, `deferred` | Render-performance concerns are downstream of the visualization architecture (DD012, currently held back). Deferring to v0.3.0 (Phase 3 Visualization Enhancements). The OME-Zarr + surface-mesh pipeline shipping in v0.1.0 (Phase 1 Validation Infrastructure) reshapes what "rendering" means; this issue revisits afterward. |
| [#117](https://github.com/openworm/sibernetic/issues/117) | **v0.3.0 — Phase 3 Visualization Enhancements** | `visualization`, `dd012`, `deferred`, `duplicate` | Same scope as [#119](https://github.com/openworm/sibernetic/issues/119). Time-series speed-chart output belongs to DD012's visualization roadmap. Deferring to v0.3.0 (Phase 3 Visualization Enhancements); #119 will be the canonical issue going forward. |
| [#119](https://github.com/openworm/sibernetic/issues/119) | **v0.3.0 — Phase 3 Visualization Enhancements** | `visualization`, `dd012`, `deferred` | Time-series chart output for worm motion is a DD012 visualization concern (currently held back). Deferring to v0.3.0 (Phase 3 Visualization Enhancements). |
| [#182](https://github.com/openworm/sibernetic/issues/182) | **v0.3.0 — Phase 3 Visualization Enhancements** | `visualization`, `dd012`, `deferred` | Simulation video recording belongs to DD012's visualization scope (currently held back). Deferring to v0.3.0 (Phase 3 Visualization Enhancements). |
| [#107](https://github.com/openworm/sibernetic/issues/107) | **v0.1.1 — Phase 1 Substrate Documentation** | `docs`, `coupling`, `deferred` | Sibernetic↔NEURON coupling documentation is part of DD001 §Integration Contract and lands as part of the v0.1.1 (Phase 1 Substrate Documentation) release. Deferring rather than closing because @skhayrulin's original scope is the right shape. |
| [#108](https://github.com/openworm/sibernetic/issues/108) | **v0.1.1 — Phase 1 Substrate Documentation** | `docs`, `calibration`, `deferred` | Calibration of Sibernetic worm movements to neural signals is now structured by the 8-phase [Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology) in DD001. The original "how to calibrate" scope becomes part of the v0.1.1 (Phase 1 Substrate Documentation) substrate-documentation release. |
| [#135](https://github.com/openworm/sibernetic/issues/135) | **Unmilestoned (Phase 4+ research)** | `performance`, `multi-gpu`, `deferred`, `future` | Multi-GPU scaling is a Phase 4+ concern building on the native-gpu substrate landing in v0.0.9 (Phase 0 Modernization). Filing as Unmilestoned so the scope stays discoverable; revisit after v0.0.9 (Phase 0 Modernization) ships and Metal+CUDA are at Stable. |

### Issues to actually close (no good milestone match)

Three issues warrant outright closure rather than deferral:

| Issue | Disposition | Comment |
|-------|-------------|---------|
| [#106](https://github.com/openworm/sibernetic/issues/106) | Close as **duplicate of [#107](https://github.com/openworm/sibernetic/issues/107)** | Same scope as [#107](https://github.com/openworm/sibernetic/issues/107) (Sibernetic-NEURON sync docs). Consolidating discussion there; #107 is being deferred to v0.1.1 (Phase 1 Substrate Documentation). |
| [#168](https://github.com/openworm/sibernetic/issues/168) | Close as **stale, insufficient information** | 5-year-old generic help request with no reproduction details or specific ask. Original macOS build question is now addressed by `./setup.sh` and the in-progress native-Metal port. Please file a fresh issue with reproduction details if a current bug exists. |
| [#122](https://github.com/openworm/sibernetic/issues/122) | Close as **stale community offer**; see warmer comment below | A more generous close-comment text for @ranr01 is drafted alongside this DD; see the comment template at the end of this section. The current Python-binding direction is narrowed and re-scoped under [Issue #250](#issue-250-in-process-simulation-handle-for-tight-loop-closed-loop-control) (v0.4.0 (Phase 4 Sensory Coupling)). |

### Recent closures (last week, 4 issues)

For completeness: [#102](https://github.com/openworm/sibernetic/issues/102) (config docs) and [#130](https://github.com/openworm/sibernetic/issues/130) (build error) closed as Replaced / Superseded; [#176](https://github.com/openworm/sibernetic/issues/176) (c302 env issue on Windows) and [#221](https://github.com/openworm/sibernetic/issues/221) (Windows install question) closed as Answered / Superseded. The migration plan's dispositions matched the actual closures.

### Comment template (defer to milestone)

For any future "should we close this?" issue that lands in the held-back-DD or DD012-visualization bucket, use this comment template instead of closing:

```
Deferring to milestone <milestone-name> (<theme>).

This issue's scope is acknowledged as in-project but belongs to
work that hasn't started yet: <one-sentence-rationale, naming the
DD or capability the scope falls under>.

Original scope preserved in this thread for reference. Current
spec for Sibernetic: DD001 (https://docs.openworm.org/design_
documents/DD001_Body_Physics_Architecture/). Apply labels:
<label-list>.
```

This keeps the issue discoverable to community contributors who might pick it up at that milestone, rather than disappearing it under an archive label.

### Considered and dropped (after audit)

Three originally-proposed issues were dropped during the 2026-05-28 per-issue audit because their scope didn't justify a fresh Sibernetic issue:

| Dropped issue | Rationale |
|---------------|-----------|
| Marching-cubes surface reconstruction from SPH particles | Downstream geometry processing belongs in the DD012 viewer repo (or a `skeletonExtraction`-style sibling repo), not in `openworm/sibernetic`. The pattern was already established by [openworm/skeletonExtraction](https://github.com/openworm/skeletonExtraction). Sibernetic exports the particle data; downstream tools own surface reconstruction. |
| Sibernetic architecture overview document | The current `README.md` (679 lines on the `ow-native-gpu-0.1.0` branch) plus `src/metal_diff/README.md` plus `AGENTS.md` already cover ~85% of the proposed acceptance criteria. Net-new value (file map + data-flow diagram) fits as README sections rather than a parallel `docs/architecture.md` that would drift. |
| Evaluate FEM Projective Dynamics backend feasibility | Zero prior FEM exploration in tree, no assigned owner, no realistic timeline. DD001 §Alternatives Considered already captures the *intent* in prose. Filing the issue now creates a stale tracker item. Revisit when a human FEM/CUDA expert is committed. |

---

## Milestones

Seven release milestones proposed, named with a semantic-versioning scheme that continues the historical `v0.0.X` cadence and layers the [OpenWorm project Phase Roadmap](DD_PHASE_ROADMAP.md) into the version string.

**Naming scheme: `v0.<phase>.<sub-milestone>`**

- **Major** stays at `0` — the project is still pre-1.0
- **Middle** carries the roadmap phase identifier (`0`, `1`, `2`, `3`, `4`, ...) so a contributor scanning the milestones page can immediately tell which phase of the larger project the work supports
- **Right** is the sub-milestone counter within that phase

Phase 0 continues the historical patch sequence (`v0.0.5` → `v0.0.6` → `v0.0.7` → `v0.0.8` → `v0.0.9`), so the existing `v0.0.8` milestone keeps its name. Phase 1 and beyond use the middle slot for the phase identifier with sub-milestones starting at `0`. Each issue's milestone is shown in the issue tables above and on every individual issue section below. Historical milestones are at the bottom of this section.

| Milestone | Maps to roadmap phase | Status | What it ships |
|-----------|----------------------|--------|---------------|
| **v0.0.8 — Phase 0 Stabilization** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-core-architecture-functional-stabilizing) (Core Architecture stabilization) | Existing — **re-scope** (due date 2026-06-12) | Lock in OpenCL as the validated reference: fix the real bugs, close the paired docs gaps, land the profiling enhancement. Without this the cross-substrate parity work has no trustworthy reference to compare against. |
| **v0.0.9 — Phase 0 Modernization** | [Phase 0](DD_PHASE_ROADMAP.md#phase-0-core-architecture-functional-stabilizing) (modernizes the existing foundation) | **New** | Generalized cross-backend parity harness (scenario registry), the native-Metal substrate locked into CI at parity on demo1/demo2/worm_alone, Ihmsen 2010 boundary pressure landed (replaces `floor_y` proxy), PCISPH iterative-pressure XPBD rewrite shipped (closes worm_swim sink), worm_swim driven scenario at kinematic parity, CUDA Phase 3 (wpoly6_inplace) FD-validated. Native modernization shipped as a release. |
| **v0.1.0 — Phase 1 Validation Infrastructure** | [Phase 1](DD_PHASE_ROADMAP.md#phase-1-core-infrastructure) (validation toolbox + output pipeline are Phase 1 deliverables) | **New** | Extended stability checker, per-particle density emission on both substrates, incompressibility validator, OME-Zarr post-processing converter (contingent on DD012 viewer contract), `simulation.output_interval` YAML plumbing. (Parity-harness generalization moved to v0.0.9 since the per-demo parity issues there need it as a prerequisite.) |
| **v0.1.1 — Phase 1 Substrate Documentation** | [Phase 1](DD_PHASE_ROADMAP.md#phase-1-core-infrastructure) (contributor workflow is Phase 1 territory) | **New** | OpenCL kernel call graph + equation table + gotchas appendix, `xpbd_full` saved-state contract + add-a-paired-kernel runbook, static GitHub Action posting the validation-methodology checklist on substrate-touching PRs, link-heavy CONTRIBUTING.md. Community-tracked docs issues ([#127](https://github.com/openworm/sibernetic/issues/127), [#128](https://github.com/openworm/sibernetic/issues/128), [#165](https://github.com/openworm/sibernetic/issues/165)) consolidated. Also picks up Sibernetic↔NEURON coupling docs ([#107](https://github.com/openworm/sibernetic/issues/107)) and calibration scope ([#108](https://github.com/openworm/sibernetic/issues/108)). |
| **v0.3.0 — Phase 3 Visualization Enhancements** | [Phase 3](DD_PHASE_ROADMAP.md#phase-3-cell-type-specialization) (DD012 Phase 3 Post-Hoc Trame Viewer begins here) | **New** | Sibernetic-side improvements that DD012 (Dynamic Visualization Architecture) will spec when it publishes. Holds deferred visualization issues ([#101](https://github.com/openworm/sibernetic/issues/101), [#117](https://github.com/openworm/sibernetic/issues/117), [#119](https://github.com/openworm/sibernetic/issues/119), [#182](https://github.com/openworm/sibernetic/issues/182)). Ships after v0.1.0 (Phase 1 Validation Infrastructure) lands, which reshapes what "visualization" means for Sibernetic. |
| **v0.4.0 — Phase 4 Sensory Coupling** | [Phase 4](DD_PHASE_ROADMAP.md#phase-4-slow-modulation-closed-loop-sensory) (DD015 Touch + DD019 Proprioception live here) | **New** | Sibernetic-side support for closed-loop sensorimotor work that DD015 (Touch Response) and DD019 (Proprioceptive Feedback) will spec when those held-back DDs publish. Holds the deferred issues ([#100](https://github.com/openworm/sibernetic/issues/100) steering, [#141](https://github.com/openworm/sibernetic/issues/141) proprioception, [#144](https://github.com/openworm/sibernetic/issues/144) touch) plus the in-process `Simulation` handle ([Issue #250](#issue-250-in-process-simulation-handle-for-tight-loop-closed-loop-control)) that the closed-loop tight loop needs. |
| **v0.4.1 — Phase 4 Environmental Modeling** | [Phase 4](DD_PHASE_ROADMAP.md#phase-4-slow-modulation-closed-loop-sensory) (DD018 Environmental Modeling lives here) | **New** | Sibernetic-side support for chemical/thermal environment simulation that DD018 (Environmental Modeling and Stimulus Delivery) will spec when it publishes — chemotaxis on simulated NaCl gradient, thermotaxis, agar substrate enhancements beyond what DD001 already covers. Holds [#163](https://github.com/openworm/sibernetic/issues/163) (molecular environment). Out of DD001's §Boundaries ("beyond liquid/gel") but in scope for DD018. |
| **Unmilestoned** | — | — | FEM Projective Dynamics feasibility evaluation, multi-GPU performance scaling ([#135](https://github.com/openworm/sibernetic/issues/135) — Phase 4+ research after native substrates Stable). Filed for tracking but no release commitment yet. |

### Milestone descriptions to post on GitHub

The text below is copy-paste-ready for the four GitHub milestone description fields. Each description references the published [DD001](https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/) so anyone landing on the milestone page can find the spec without searching.

#### `v0.0.8 — Phase 0 Stabilization` — OpenCL Gold-Standard Stabilization

```
OpenCL gold-standard stabilization.

Maps to roadmap Phase 0 (Core Architecture — Functional, Stabilizing).
This is the "fix what's there" half of Phase 0; v0.0.9 (Phase 0
Modernization) handles the "rebuild for new platforms" half.

Scope: Lock in the OpenCL reference implementation as the validated
gold standard against which all native substrates (Metal, CUDA) are
measured. Fix real bugs, close paired docs gaps, land the profiling
enhancement. Without this milestone, cross-substrate parity claims
in v0.0.9 (Phase 0 Modernization) are meaningless — the reference itself must be trustworthy.

Spec: DD001 Body Physics Engine Architecture (the gold-standard
framing lives in DD001 §Backend Stabilization Roadmap).
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#backend-stabilization-roadmap

Filter for the work in this release: label:dd001 + this milestone.

Due date: 2026-06-12.
```

#### `v0.0.9 — Phase 0 Modernization` — Native-GPU Substrate Consolidation

```
Native-GPU substrate consolidation.

Maps to roadmap Phase 0 (Core Architecture). This modernizes the
existing foundation by moving from OpenCL (losing platform support)
to native Metal + native CUDA. Pairs with v0.0.8 (Phase 0 Stabilization).

Scope: Ship the native-Metal substrate at OpenCL parity on the
four working demos (demo1 cube drop, demo2 membrane permeability,
worm_alone, worm_swim). Bring native-CUDA scaffolding up to demo1
parity. Merge the native-gpu branch consolidation PR. Includes
generalizing the demo1 parity harness into a scenario registry,
since the per-demo parity gates here depend on it.

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

#### `v0.1.0 — Phase 1 Validation Infrastructure` — Validation Infrastructure + Output Pipeline

```
Cross-substrate validation infrastructure and the simulation-output
pipeline.

Maps to roadmap Phase 1 (Core Infrastructure). The validation
toolbox revival (DD017), the output pipeline that feeds DD012
visualization, and Sibernetic's place in the `docker compose run
validate` workflow (DD011) are all Phase 1 deliverables.

Scope: Extend scripts/measure_cube_stability.py with NaN/escape/
velocity checks. Emit per-particle density on OpenCL and Metal
substrates (prereq for density validation). Land
validate_incompressibility.py against that data. Ship the OME-Zarr
post-processing converter and the output-interval YAML plumbing.
(Parity-harness generalization co-ships with v0.0.9 since the
per-demo parity issues there depend on it. Marching-cubes surface
reconstruction dropped — belongs in the DD012 viewer repo, not
Sibernetic.)

Spec: DD001 Body Physics Engine Architecture, especially §Acceptance
Criteria and §Deliverables (the OME-Zarr rows).
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#acceptance-criteria-green-light-definitions

Filter for the work in this release: label:dd001 + this milestone.

Ships after v0.0.9 (Phase 0 Modernization) native substrates are at Stable.
```

#### `v0.1.1 — Phase 1 Substrate Documentation` — Substrate Documentation + Contributor Onboarding

```
Substrate becomes understandable and contributor-ready.

Maps to roadmap Phase 1 (Core Infrastructure). The contributor
workflow ("Fork subsystem → build with custom branch → quick-test
→ validate → PR") is a Phase 1 deliverable; this milestone
documents the Sibernetic side of that workflow.

Scope: Add a per-timestep kernel call graph + kernel→equation
table + line-numbered gotchas appendix to the OpenCL docs (don't
re-annotate sphFluid.cl — it's already inline-documented). Add the
xpbd_full_fwd/bwd saved-state contract + add-a-paired-kernel runbook
(the XPBD math + env vars already live in metal_diff/README +
M7_XPBD_PLAN.md). Stand up a static GitHub Action that posts the
Validation Methodology checklist on substrate-touching PRs (no
LLM/bot dependency). Land a link-heavy CONTRIBUTING.md that points
at existing README/metal_diff/DD001. Roll up the community-tracked
docs issues (#127, #128, #165) into this docs release. Also picks
up the Sibernetic-NEURON coupling docs (#107) and calibration
scope (#108).

Spec: DD001 Body Physics Engine Architecture, especially
§Differentiability and §Validation Methodology.
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#differentiability

Filter for the work in this release: label:dd001 label:docs
+ this milestone.

Ships after v0.1.0 (Phase 1 Validation Infrastructure).
```

#### `v0.3.0 — Phase 3 Visualization Enhancements` — Visualization & Output Enhancements

```
Visualization-side improvements that DD012 will spec.

Maps to roadmap Phase 3 (Cell-Type Specialization), where DD012
Phase 3 (Post-Hoc Trame Viewer) begins. Sibernetic-side rendering
and output enhancements line up with that visualization push.

Scope: Holds the deferred visualization issues (#101 render speed,
#117 + #119 chart output, #182 video recording) whose scope falls
under the held-back DD012 (Dynamic Visualization Architecture).
Fresh issues will derive from DD012 when it publishes.

The v0.1.0 (Phase 1 Validation Infrastructure) OME-Zarr + surface-mesh
+ configurable-output pipeline ships first and reshapes what
"visualization" means for Sibernetic; this milestone revisits these
deferred issues against the new pipeline.

Spec: DD001 Body Physics Engine Architecture, §How to Visualize
and §Deliverables (OME-Zarr rows).
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#how-to-visualize

Filter for the work in this release: label:dd001 label:visualization
+ this milestone.

Ships after v0.1.0 (Phase 1 Validation Infrastructure) lands and DD012 publishes.
```

#### `v0.4.0 — Phase 4 Sensory Coupling` — Sensory Coupling

```
Sibernetic-side support for closed-loop sensorimotor work.

Maps to roadmap Phase 4 (Slow Modulation + Closed-Loop Sensory),
where DD015 (Touch Response) and DD019 (Proprioceptive Feedback)
land. Sibernetic-side bidirectional coupling lives here.

Scope: Holds the deferred issues whose Sibernetic-side scope falls
under the held-back DDs DD015 and DD019. Includes #100 (steering),
#141 (proprioception), and #144 (touch sensation). Fresh issues
will derive from DD015 and DD019 when they publish, and this
milestone will be re-scoped accordingly.

Until DD015 and DD019 publish, this milestone is a deferral target
rather than an active sprint. The deferred issues stay open so
community contributors can pick them up if they want; the milestone
gives them a release target.

Spec: DD001 Body Physics Engine Architecture (the bidirectional
coupling mechanism lives in §Integration Contract).
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#integration-contract

Filter for the work in this release: label:dd001 label:closed-loop
OR label:touch OR label:proprioception + this milestone.

Ships after v0.3.0 (Phase 3 Visualization Enhancements) and
after DD015 / DD019 publish.
```

#### `v0.4.1 (Phase 4 Environmental Modeling)` — Environmental Modeling

```
Sibernetic-side support for chemical/thermal environment simulation.

Maps to roadmap Phase 4 (Slow Modulation + Closed-Loop Sensory),
where DD018 (Environmental Modeling and Stimulus Delivery) lands.
Chemotaxis on simulated NaCl gradient, thermotaxis, and agar-
substrate enhancements beyond what DD001 already covers all live
here on the Sibernetic side.

Scope: Holds the deferred issue #163 (molecular environment).
Out of DD001's §Boundaries (item 3, "beyond liquid/gel") but in
scope for the held-back DD018. Fresh issues will derive from DD018
when it publishes; this milestone is the deferral target until then.

Spec: DD018 when it publishes; DD001 §Boundaries for the explicit
hand-off line on what's in vs out of DD001's environment scope.
https://docs.openworm.org/design_documents/DD001_Body_Physics_Architecture/#boundaries-explicitly-out-of-scope

Filter for the work in this release: label:dd001 label:environment
+ this milestone.

Ships after v0.4.0 (Phase 4 Sensory Coupling) and after DD018 publishes.
```

### Historical milestones (closed, reference only)

| Milestone | Closed | Issues | Scope |
|-----------|--------|--------|-------|
| v0.0.3 | 2015-07 | 12 | LeapFrog integrator, `-help` option, worm config from file, snapshot ability |
| v0.0.4 | 2016-04 | 15 | Bug-fixing pass: memory leaks, segfault on GPU-absent machines, NEURON interaction |
| v0.0.5 | 2016-05 | 2 | Multi-device parallelization, settings file format |

---

## Group 1: v0.0.9 — Phase 0 Modernization (Per-Demo Parity & CUDA Phase 3)

Lock in the parity work that's already substantively done, close the remaining gaps (worm_swim sink, Ihmsen boundary pressure), and start CUDA at Phase 3 of its own README plan. Per audit, three of the four demos are at or near parity; only worm_swim is honestly in tuning.

Per [DD001 §Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology), every PR landing under these issues should follow the 8-phase workflow and satisfy the [MoaW PR review checklist](DD001_Body_Physics_Architecture.md#mind-of-a-worm-pr-review-checklist).

---

### Issue #236: Generalize `tests/test_demo1_backend_parity.py` into a scenario-registry harness

- **Title:** `[DD001] Generalize parity test into a scenario registry (demo1/demo2/worm_alone/worm_swim) — milestone Phase 1`
- **Labels:** `DD001`, `ai-workable`, `L2`, `validation`, `parity`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, physics
- **Audit note:** `tests/test_demo1_backend_parity.py` (256 lines) is already a fully-functional parity harness — parses position buffers with `.times.txt` sidecar handling, computes per-particle L2 + cube-center/extent drifts + init/mean/final L2, has explicit `THRESHOLDS` dict and 5 pass/fail gates, JSON + human-readable output. The proposed new file `scripts/backend_parity_test.py` would duplicate ~80% of this. **Milestone:** Logically validation infrastructure, but co-ships with v0.0.9 (Phase 0 Modernization) because the per-demo parity issues #237/#238/#239/#242 all depend on the generalized harness — splitting these across milestones would force v0.0.9 to ship without working CI gates.
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Backend Graduation Criteria](DD001_Body_Physics_Architecture.md#backend-graduation-criteria-exit-conditions)
- **Depends On:** None (the per-demo parity issues #237-#239, #242 depend on this)
- **Existing Code to Reuse / Refactor:**
    - `tests/test_demo1_backend_parity.py` — rename to `tests/test_backend_parity.py`, parameterize on scenario
    - `scripts/cross_backend_regression.py` — driver that runs N backends; already pluggable via `--binary NAME=PATH`
    - `src/metal_diff/dump_metal_trajectory.py` — Metal trajectory dumper writing OpenCL-compatible format
- **Approach:** Refactor — promote the existing demo1-specific harness into a scenario registry. Per-demo configs (THRESHOLDS, parsers, baselines) live in `tests/parity_scenarios/{demo1,demo2,worm_alone,worm_swim}.py`. Add `--scenario` and `--substrate` CLI flags. Keep the L2 engine and threshold logic that already exists.
- **Files to Modify:**
    - `tests/test_backend_parity.py` (rename from test_demo1_backend_parity.py)
    - `tests/parity_scenarios/{demo1,demo2,worm_alone,worm_swim}.py` (new — per-demo configs)
    - `tests/baseline/*_opencl.json` (new — committed reference metrics)
- **Acceptance Criteria:**
    - [ ] Runs `--scenario demo1 --substrate metal-native` and reproduces the existing demo1 parity check
    - [ ] Adds entry points for demo2, worm_alone, worm_swim (used by #238, #239, #242)
    - [ ] `--substrate cuda-native` returns "not implemented yet" error message
    - [ ] Emits JSON + human-readable table; exit code reflects pass/fail
    - [ ] `cross_backend_regression.py` continues to work
- **Sponsor Summary Hint:** The parity engine exists. This issue generalizes the existing demo1-specific harness so demo2/worm_alone/worm_swim each get a parity gate, without rewriting the L2/sampling/threshold core.

---

---

---

### Issue #237: Lock demo1 parity test into CI

- **Title:** `[DD001] Lock demo1 (cube drop) parity test into CI`
- **Labels:** `DD001`, `ai-workable`, `L1`, `phase-0`, `native-gpu`, `ci`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** ci-cd, python
- **Audit note:** demo1 parity is **substantively done**. `tests/test_demo1_backend_parity.py` exists (256 lines), `docs/cube_drop_demo1_25ms.mp4` + `.gif` committed, `scripts/render_demo1_parity.py` exists, `docs/demos.md` has the regenerate recipe + tuned params. The Metal smoke test in `.github/workflows/ci-build.yml` runs `xpbd_step` for 50 steps but doesn't call the full parity test (requires a pre-committed OpenCL reference, can't generate on macOS CI). This is a 1-2 day CI-wiring task.
- **Depends On:** [#236](#issue-236-generalize-teststest_demo1_backend_paritypy-into-a-scenario-registry-harness) (generalized harness)
- **Acceptance Criteria:**
    - [ ] Commit canonical OpenCL `position_buffer.txt` reference under `tests/data/demo1_opencl/` (or generate via Linux runner)
    - [ ] CI smoke test flipped to call `tests/test_backend_parity.py --scenario demo1 --substrate metal-native`
    - [ ] SGD convergence history JSON committed (`tools/sgd_history/demo1_sgd_history.json`)
    - [ ] PR review checklist (DD001 §MoaW PR Review Checklist) satisfied by the landing PR
- **Sponsor Summary Hint:** All the substantive work is done — parity test, MP4, tuned params, docs/demos.md. This locks it into CI so regressions get caught.

---

---

### Issue #238: Add demo2 (membrane permeability) parity gate to harness

- **Title:** `[DD001] Add demo2 membrane permeability parity gate (depends on #236)`
- **Labels:** `DD001`, `human-expert`, `L2`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph
- **Audit note:** SGD parameters for demo2 are **already converged and shipped** (commit bf6b333). `docs/demo2_v9_sgd_perm.mp4` + `.gif` exist; `docs/demos.md` documents tuned params (`spring_k=2697`, `anchor_k=12177`, `rho_rest=8e-13`, `alpha_dist=3.3e-9`). What's missing is a demo2-shaped parity check — cube-center/extent metrics don't apply to a sheet; need membrane-retention vs permeability ratio over time.
- **Depends On:** [#236](#issue-236-generalize-teststest_demo1_backend_paritypy-into-a-scenario-registry-harness) (generalized harness)
- **Acceptance Criteria:**
    - [ ] `tests/parity_scenarios/demo2.py` with membrane-specific THRESHOLDS (liquid fraction above sheet on membraned half vs porous half over 42ms, ±5% vs OpenCL)
    - [ ] Parity test green on `--scenario demo2 --substrate metal-native`
    - [ ] SGD convergence histories for membrane + permeability tuning committed under `tools/sgd_history/`
    - [ ] Existing MP4 stays canonical; no need to re-render
- **Sponsor Summary Hint:** The membrane physics ported and tuned; just needs an entry in the generalized parity harness.

---

---

### Issue #239: Add worm_alone parity gate (worm-COM + cross-section + max-span metrics)

- **Title:** `[DD001] Add worm_alone_half_resolution parity gate with worm-shaped metrics (depends on #236)`
- **Labels:** `DD001`, `human-expert`, `L2`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph
- **Audit note:** Visual + quantitative parity **already shipped** (commit 929ec8a). `docs/worm_alone_opencl_vs_metal.mp4` + `.gif` exist; `docs/demos.md` parity table shows worm-top y matching within 0.06 sim units across 25ms, MSE 0.112, cross-section diameter within ~1%, tuned params committed. What's missing: a worm-shaped parity test (cube metrics don't apply; need worm-COM, cross-section diameter, max-span change). Known caveat: `floor_y=2.25` is a soft proxy for missing Ihmsen 2010 boundary pressure — tracked separately as [Issue #240](#issue-240-implement-ihmsen-2010-boundary-active-sph-pressure-replaces-floor_y-proxy).
- **Depends On:** [#236](#issue-236-generalize-teststest_demo1_backend_paritypy-into-a-scenario-registry-harness) (generalized harness)
- **Acceptance Criteria:**
    - [ ] `tests/parity_scenarios/worm_alone.py` with worm-COM + cross-section + max-span THRESHOLDS
    - [ ] Parity test green on `--scenario worm_alone --substrate metal-native`
    - [ ] SGD convergence history committed
    - [ ] Cross-references [#240](#issue-240-implement-ihmsen-2010-boundary-active-sph-pressure-replaces-floor_y-proxy) as the real physics fix for the `floor_y` proxy
- **Sponsor Summary Hint:** Worm-alone parity is shipped; this just adds the parity-test entry. Real residual physics gap tracked separately in #240.

---

---

### Issue #240: Implement Ihmsen 2010 boundary → active SPH pressure (replaces `floor_y` proxy)

- **Title:** `[DD001] Implement Ihmsen 2010 boundary→active SPH pressure for native-Metal substrate`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`, `physics`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, sph, metal
- **Audit note (NEW issue surfaced by audit):** The current `worm_alone` parity uses `floor_y=2.25` as a soft proxy because the native substrate doesn't yet implement Ihmsen 2010 boundary→active SPH pressure (per `docs/demos.md` parity caveats). This is the real next physics step on the Metal substrate, not just an artifact-housekeeping item.
- **DD Section to Read:** [DD001 §Backend Stabilization Roadmap](DD001_Body_Physics_Architecture.md#backend-stabilization-roadmap)
- **Depends On:** None (#239 documents the caveat that motivates this)
- **Existing Code to Reuse:**
    - OpenCL reference implementation of boundary pressure in `src/sphFluid.cl`
    - `src/metal_diff/shaders.metal` for the kernel layer to add to
- **Acceptance Criteria:**
    - [ ] Implement boundary→active SPH pressure kernel in `shaders.metal` per Ihmsen 2010
    - [ ] Paired analytic backward kernel + FD validator (per DD001 Quality Criteria #7)
    - [ ] `worm_alone` parity test now passes with physical `floor_y` (not the elevated proxy value)
    - [ ] Tuned param updates committed
- **Sponsor Summary Hint:** Currently the worm-alone parity test passes with a `floor_y` elevated above the real floor — a workaround for missing physics. This issue is the actual physics: boundary particles applying SPH pressure to active particles per Ihmsen 2010.

---

---

### Issue #241: Rewrite XPBD density inner loop with PCISPH iterative pressure

- **Title:** `[DD001] Rewrite native-Metal XPBD density inner loop with PCISPH iterative pressure correction`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`, `physics`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, sph, metal, xpbd
- **Audit note (NEW issue surfaced by audit):** Per `docs/demos.md` worm_swim parity table: OpenCL's PCISPH iterates pressure until density exactly matches `rho_0` per step; Metal's XPBD density solver only fires when density *exceeds* `rho_rest`, so steady-state pressure is zero and the worm sinks ~3 sim units below OpenCL by 25ms. Closing this gap requires a PCISPH-iterative-pressure rewrite of the inner XPBD loop. Substantial physics work — split out from worm_swim parity (was tangled together in original [#239](#issue-239-add-worm_alone-parity-gate-worm-com-cross-section-max-span-metrics)).
- **DD Section to Read:** [DD001 §Extended Position-Based Dynamics](DD001_Body_Physics_Architecture.md#extended-position-based-dynamics-xpbd-native-metal-cuda-substrates)
- **Depends On:** None (#242 worm_swim parity depends on this)
- **Acceptance Criteria:**
    - [ ] PCISPH-style iterative pressure correction implemented in the XPBD density solver
    - [ ] Paired analytic backward + FD validator
    - [ ] Existing demo1, demo2, worm_alone parity tests still pass (no regression)
    - [ ] worm_swim sink rate measurably closer to OpenCL (validates the fix before #242 wraps it up with kinematic-gait checks)
- **Sponsor Summary Hint:** Why the worm sinks in worm_swim Metal: the density solver only fires when density exceeds the rest value, so equilibrium pressure is zero. PCISPH iterates until density matches exactly — that's the fix. This is real physics work, days to weeks.

---

---

### Issue #242: worm_swim_half_resolution — set up muscle-driven scenario and add parity gate

- **Title:** `[DD001] worm_swim_half_resolution — driven scenario + parity (depends on #236, #241)`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, opencl, metal, sph, muscle-actuation
- **Audit note:** Original issue conflated two things: (a) PCISPH-iterative density rewrite (now split to [#241](#issue-241-rewrite-xpbd-density-inner-loop-with-pcisph-iterative-pressure)) and (b) setting up a muscle-driven swim scenario plus parity. The current `worm_swim_half_resolution` config is a passive sink test (no muscle drive), so the kinematic-gait acceptance criteria (swimming velocity / frequency / wavelength within ±5%) can't be checked against it as-is.
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Validated Kinematic Outputs](DD001_Body_Physics_Architecture.md#validated-kinematic-outputs-palyanov-et-al-2018)
- **Depends On:** [#236](#issue-236-generalize-teststest_demo1_backend_paritypy-into-a-scenario-registry-harness) (harness), [#241](#issue-241-rewrite-xpbd-density-inner-loop-with-pcisph-iterative-pressure) (PCISPH iterative pressure — needed for steady-state behavior)
- **Acceptance Criteria:**
    - [ ] Muscle-driven worm_swim config in `configuration/worm_swim_half_resolution_driven/`
    - [ ] `tests/parity_scenarios/worm_swim.py` with kinematic THRESHOLDS (velocity / frequency / wavelength)
    - [ ] Parity test green on `--scenario worm_swim --substrate metal-native` within ±5% of OpenCL AND within DD001 §Validated Kinematic Outputs experimental ranges
    - [ ] SGD convergence history committed
- **Sponsor Summary Hint:** The current worm_swim Metal port is a passive sink; you can't check swim-gait kinematics on something that isn't swimming. This issue sets up the driven scenario and wires the kinematic-gait parity gate, gated on #241 fixing the density-equilibrium problem.

---

---

### Issue #243: CUDA Phase 3 — port `wpoly6_inplace`, prove nvcc build, FD-validate against Metal

- **Title:** `[DD001] CUDA Phase 3 — port wpoly6_inplace, prove nvcc build, FD-validate vs Metal`
- **Labels:** `DD001`, `human-expert`, `L3`, `phase-0`, `native-gpu`, `cuda`
- **Roadmap Phase:** Phase 0
- **Milestone:** [v0.0.9 — Phase 0 Modernization](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, cuda, sph, c++
- **Audit note (REPLACES original broad "CUDA substrate bring-up"):** `src/cuda/` contains exactly two files today: `README.md` (141 lines, comprehensive 5-phase plan) and `sphFluid.cu` (111 lines, all kernel bodies are `// TODO`). The README itself says `sphFluid.cu` "is *not* the right starting point under the current strategy — start fresh from `src/metal_diff/`." There is **no PR #229 by @feldmannn** — the scaffolding commit (`9f92972`) is by slarson; the original issue's "review and merge PR #229" criterion was unactionable. Per the README's 5-phase plan, this issue is Phase 3 only; Phases 2-5 file separately when Phase 3 lands.
- **DD Section to Read:** [DD001 §Cross-Backend Parity Requirements](DD001_Body_Physics_Architecture.md#cross-backend-parity-requirements), [§Backend Graduation Criteria](DD001_Body_Physics_Architecture.md#backend-graduation-criteria-exit-conditions), `src/cuda/README.md` for the 5-phase plan
- **Depends On:** Linux+CUDA build environment proven
- **Acceptance Criteria:**
    - [ ] Port `wpoly6_inplace` forward kernel to CUDA following the Metal counterpart pattern
    - [ ] nvcc build of the kernel + minimal test harness
    - [ ] FD test validating CUDA `wpoly6_inplace` matches Metal output within ±5%
    - [ ] `src/cuda/README.md` updated with status of Phase 3
    - [ ] When Phase 3 lands, file follow-up issues for Phases 2-5 from the README plan
- **Sponsor Summary Hint:** CUDA substrate is currently TODO stubs. The README has a sensible 5-phase work plan but filing a single "bring-up parity for demo1" issue with 5 acceptance criteria is premature — there's no working kernel of any kind. Start with one kernel, one FD test, prove the build. Then derive the next phases.

---

---

## Group 2: v0.1.0 — Phase 1 Validation Infrastructure (Validation Tooling + Output Pipeline)

Cross-substrate validation infrastructure and the simulation-output pipeline. The validation toolbox revival (DD017), the output pipeline that feeds DD012 visualization, and Sibernetic's place in the `docker compose run validate` workflow (DD011) are all Phase 1 deliverables. Per the 2026-05-28 audit, the existing stability/parity infrastructure is more built-out than the original proposal acknowledged; these issues extend/generalize rather than create from scratch.

---

### Issue #233: Extend `scripts/measure_cube_stability.py` with NaN/escape/velocity checks

- **Title:** `[DD001] Extend measure_cube_stability.py with NaN, bounding-box escape, and velocity-divergence checks`
- **Labels:** `DD001`, `ai-workable`, `L1`, `validation`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.0 — Phase 1 Validation Infrastructure](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, physics
- **Audit note:** `scripts/measure_cube_stability.py` already exists (171 lines) and does stability checking — streams position buffers, parses the 11-line header, computes extent retention / mean Y / min Y, exits 0/1 with JSON output. `scripts/cross_backend_regression.py` already calls its `measure()`. The original "create check_stability.py" framing overstated the gap.
- **DD Section to Read:** [DD001 — Acceptance Criteria](DD001_Body_Physics_Architecture.md#acceptance-criteria-green-light-definitions) (criterion 1)
- **Depends On:** None
- **Existing Code to Reuse / Extend:**
    - `scripts/measure_cube_stability.py` — the file to extend
    - `scripts/cross_backend_regression.py` — already imports `measure()`; no caller change needed
    - `src/metal_diff/dump_metal_trajectory.py` — writes the same position-buffer format the script already parses
- **Approach:** Extend the existing script with three new checks: (a) per-particle NaN detection in positions and velocities, (b) bounding-box escape detection (configurable box dimensions), (c) velocity-magnitude divergence threshold. Keep the same JSON output / exit-code contract.
- **Files to Modify:**
    - `scripts/measure_cube_stability.py` (extend)
    - `tests/test_measure_cube_stability.py` (new — synthetic NaN-injected / escaped-particle cases)
- **Acceptance Criteria:**
    - [ ] NaN detection in positions and velocities (returns FAIL with offending particle indices)
    - [ ] Bounding-box escape detection with configurable box (CLI flag)
    - [ ] Velocity-magnitude divergence check with configurable threshold
    - [ ] Existing extent / mean Y / min Y checks remain unchanged
    - [ ] `cross_backend_regression.py` continues to work without modification
    - [ ] Unit tests: clean data → PASS; NaN-injected → FAIL; escaped particle → FAIL; diverged velocity → FAIL
- **Sponsor Summary Hint:** The stability checker already exists and is wired into the cross-backend regression script. This issue just adds three missing failure-mode checks (NaN, escape, velocity-divergence) to the same file. Half a day of work, not a fresh-script effort.

---

---

### Issue #234: Emit per-particle density alongside position output (both substrates)

- **Title:** `[DD001] Emit per-particle density column alongside position_buffer.txt on OpenCL and Metal substrates`
- **Labels:** `DD001`, `human-expert`, `L2`, `validation`, `output-format`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.0 — Phase 1 Validation Infrastructure](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, c++, physics
- **Audit note (NEW issue surfaced by audit):** Sibernetic computes per-particle density on both substrates (`src/metal_diff/test_dens_grad.py`, `test_solve_dens_bwd.py` cover the Metal side; `sphFluid.cl` PCISPH on OpenCL) but **does not dump it to disk** in the normal run path. `position_buffer.txt` only has `x y z type`. Without this, [Issue #235](#issue-235-create-scriptsvalidate_incompressibilitypy-depends-on-234) (`validate_incompressibility.py`) has nothing to read against. This issue is the missing prerequisite.
- **DD Section to Read:** [DD001 — Acceptance Criteria](DD001_Body_Physics_Architecture.md#acceptance-criteria-green-light-definitions) (validate gate)
- **Depends On:** None (this is a prereq for #235)
- **Existing Code to Reuse:**
    - `src/owPhysicsFluidSimulator.cpp` — owns the OpenCL output writing path
    - `src/metal_diff/dump_metal_trajectory.py` — owns the Metal trajectory dump path
    - `inc/owPhysicsConstant.h` — already documents `rho0 = 1000.0f` and particle-type constants
- **Approach:** Add a per-particle density column to the output. Two options to pick from in the issue discussion: (a) extend `position_buffer.txt` to `x y z type density` (breaks the existing 4-column parser everywhere); (b) emit a sidecar `density_buffer.txt` keyed to the same frame indices. Recommend (b) for backward compatibility. Mirror in `dump_metal_trajectory.py`.
- **Files to Modify:**
    - `src/owPhysicsFluidSimulator.cpp` (OpenCL side density dump)
    - `src/metal_diff/dump_metal_trajectory.py` (Metal side density dump)
    - `inc/owConfigProperty.h`/`.cpp` (CLI flag for enabling dump, e.g., `dump_density=1`)
- **Acceptance Criteria:**
    - [ ] OpenCL substrate emits per-particle density per frame (file or extended buffer)
    - [ ] Metal substrate (`dump_metal_trajectory.py`) emits the same
    - [ ] Format is identical between substrates so a single downstream parser works
    - [ ] Disabled by default (no perf impact on standard runs)
    - [ ] Existing tests / parity scripts continue to work
- **Sponsor Summary Hint:** PCISPH/XPBD compute per-particle density inside the simulator, but it never makes it to disk. To validate incompressibility (the next issue) we need that data. This is the missing pipe.

---

---

### Issue #235: Create `scripts/validate_incompressibility.py` (depends on #234)

- **Title:** `[DD001] Create validate_incompressibility.py — density deviation checker (~50 lines NumPy)`
- **Labels:** `DD001`, `ai-workable`, `L1`, `validation`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.0 — Phase 1 Validation Infrastructure](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python
- **Audit note:** Original framing made this a from-scratch effort. With [Issue #234](#issue-234-emit-per-particle-density-alongside-position-output-both-substrates) emitting density data, the actual script is ~50 lines of NumPy.
- **DD Section to Read:** [DD001 — Acceptance Criteria](DD001_Body_Physics_Architecture.md#acceptance-criteria-green-light-definitions) (validate gate)
- **Depends On:** [#234](#issue-234-emit-per-particle-density-alongside-position-output-both-substrates) (density dump must exist first)
- **Files to Modify:**
    - `scripts/validate_incompressibility.py` (new — thin reader)
    - `tests/test_validate_incompressibility.py` (new)
- **Acceptance Criteria:**
    - [ ] Reads density output produced by #234
    - [ ] Filters to liquid-type particles
    - [ ] Reports max / mean / percentile deviation from ρ₀ = 1000 kg/m³
    - [ ] `--max_deviation` flag (default 0.01)
    - [ ] PASS/FAIL with statistics, exit code 0/1
- **Sponsor Summary Hint:** Thin checker, ~50 lines. Gated on #234 producing the data to check.

---

---

### Issue #247: OME-Zarr post-processing converter (contingent on DD012 viewer contract)

- **Title:** `[DD001] Add scripts/export_to_ome_zarr.py post-processing converter (gated on DD012 viewer requiring OME-Zarr)`
- **Labels:** `DD001`, `ai-workable`, `L2`, `output`, `visualization`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.0 — Phase 1 Validation Infrastructure](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python
- **Audit note:** `inc/owVtkExport.h` + `src/owVtkExport.cpp` (245 lines) already export per-frame particle positions, types, velocities, connections, membranes, muscles to VTK. OME-Zarr's actual value is (a) chunked/lazy random access for very long time series, (b) being the format the DD012 viewer (Neuroglancer/web tooling) expects. **This issue only justifies itself if DD012 publishes a viewer contract specifying OME-Zarr.** Reframe accordingly: post-processing converter reading VTK or `position_buffer.txt`, not a new C++ export path. Gated on DD012 contract.
- **DD Section to Read:** [DD001 §Deliverables](DD001_Body_Physics_Architecture.md#deliverables) (OME-Zarr rows), [§How to Visualize](DD001_Body_Physics_Architecture.md#how-to-visualize)
- **Depends On:** DD012 publishing a viewer contract requiring OME-Zarr (if VTK suffices, this issue closes WONTFIX)
- **Files to Modify:**
    - `scripts/export_to_ome_zarr.py` (new — post-processing converter)
- **Acceptance Criteria:**
    - [ ] Reads existing VTK output or `position_buffer.txt`
    - [ ] Writes OME-Zarr with `body/positions/`, `body/types/`, metadata
    - [ ] Cites the DD012 viewer contract specifically — if the contract isn't established, this issue stays WONTFIX
- **Sponsor Summary Hint:** VTK already exports the same particle data. OME-Zarr is only justified by an explicit downstream requirement. This issue is a post-processing converter, not a new C++ export path — and it's contingent on DD012's viewer contract calling for OME-Zarr specifically.

---

---

### Issue #248: Plumb `simulation.output_interval` from openworm.yml through to existing `logstep` knob

- **Title:** `[DD001] Plumb simulation.output_interval from openworm.yml through to existing logstep/--chunk knobs`
- **Labels:** `DD001`, `ai-workable`, `L1`, `config`, `integration`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.0 — Phase 1 Validation Infrastructure](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, c++
- **Audit note:** `inc/owConfigProperty.h:118-119` + `src/owConfigProperty.cpp:103-108` already implement `logstep=N` with default 10 + validation. `src/owPhysicsFluidSimulator.cpp` uses `config->getLogStep()` at three sites (lines 470/478/514) for pressure-dump / VTK / muscle-log gating. `src/metal_diff/dump_metal_trajectory.py` has `--chunk N` (default 150). **The original issue's claim "no configurable output frequency exists" is wrong.** The real work is thin: add `--output_interval N` as an alias for `logstep=N` so the DD011 `openworm.yml` key plumbs through cleanly; rename `--chunk` → `--output_interval` in the Metal dumper for consistency.
- **DD Section to Read:** [DD001 §Configuration](DD001_Body_Physics_Architecture.md#configuration)
- **Depends On:** DD011 master_openworm config loading
- **Acceptance Criteria:**
    - [ ] `--output_interval N` accepted as alias for `logstep=N` in the C++ binary
    - [ ] `master_openworm.py` (in openworm/openworm) passes `simulation.output_interval` from openworm.yml as `--output_interval`
    - [ ] `dump_metal_trajectory.py` accepts `--output_interval` as alias for `--chunk`
    - [ ] Documented default reconciled (currently 10 for C++, 150 for Metal — pick one with rationale)
- **Sponsor Summary Hint:** `logstep=N` already exists in the C++ binary; `--chunk N` in the Metal dumper. This issue is the thin YAML→flag plumbing, not a new feature. Rename for consistency so the DD011 `openworm.yml` key flows through. L1.

---

---

## Group 3: v0.1.1 — Phase 1 Substrate Documentation (Substrate Docs + Contributor Onboarding)

Substrate becomes understandable and contributor-ready. Fill the genuine doc gaps audit identified, without re-presenting what's already documented in `README.md` (679 lines), `src/metal_diff/README.md`, `M7_XPBD_PLAN.md`, or DD001 itself.

---

### Issue #244: Add OpenCL kernel call graph + equation table + gotchas appendix

- **Title:** `[DD001] Add per-timestep kernel call graph + kernel→equation table + gotchas appendix to OpenCL docs`
- **Labels:** `DD001`, `ai-workable`, `L1`, `docs`, `opencl`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.1 — Phase 1 Substrate Documentation](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** docs, opencl, physics, sph
- **Audit note:** `sphFluid.cl` (1515 lines) is already inline-documented — literature reference header, `/** */` doc-comments above kernels, macro semantics inline. `inc/owPhysicsConstant.h` is heavily annotated with units + citations + the CFL-condition explanation. The README §"From PCISPH to XPBD" already explains PCISPH conceptually. The real gap is a **top-level walkthrough** — call graph, equation table, gotchas with line numbers — not a kernel-by-kernel annotation pass.
- **DD Section to Read:** [DD001 §Common Gotchas](DD001_Body_Physics_Architecture.md#common-gotchas-distilled-from-the-native-metal-port)
- **Depends On:** None
- **Files to Modify:**
    - `docs/opencl_kernel_architecture.md` (new — ~2-3 pages)
- **Acceptance Criteria:**
    - [ ] Per-timestep kernel call graph showing the order of invocations
    - [ ] Table mapping each `__kernel` function in sphFluid.cl to its DD001 equation (Wpoly6, ∇Wspiky, ∇²Wviscosity, F_elastic, PCISPH)
    - [ ] Gotchas appendix listing the items from DD001 §Common Gotchas with specific `sphFluid.cl` line numbers (0.25 factor on non-worm-body elastic, ε guards, sim_scale coordinate-space conversion sites)
    - [ ] Cross-references Metal counterparts in `src/metal_diff/shaders.metal`
- **Sponsor Summary Hint:** Don't re-annotate sphFluid.cl — it's already documented inline. Add the top-level walkthrough that lets a porter find their way: call graph, equation table, gotchas-with-line-numbers. ~2-3 pages, L1.

---

---

### Issue #245: Document `xpbd_full` saved-state contract + add-a-paired-kernel runbook

- **Title:** `[DD001] Document xpbd_full saved-state contract + how-to-add-a-paired-kernel runbook + 19-kernel index`
- **Labels:** `DD001`, `human-expert`, `L2`, `docs`, `native-gpu`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.1 — Phase 1 Substrate Documentation](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** physics, sph, autograd, docs
- **Audit note:** `src/metal_diff/README.md` (8.8KB) tables the M6 perf summary and documents the major forward ops with CLI signatures. `M7_XPBD_PLAN.md` documents the XPBD derivation + α-compliance table + paired-backward rationale. The main README has the differentiable-substrate section with `xpbd_full_bwd` entry point + `BWD_TBPTT`/`BWD_CLIP_NORM` env vars. The 19 `test_*.py` files are themselves executable specs. The real gaps: (a) the saved-state contract that `xpbd_full_fwd` writes / `xpbd_full_bwd` consumes (implicit in `ops_xpbd_full.mm`, not documented), (b) the "how to add a new paired kernel" runbook, (c) a single 19-kernel index table.
- **DD Section to Read:** [DD001 §Differentiability](DD001_Body_Physics_Architecture.md#differentiability)
- **Depends On:** None
- **Files to Modify:**
    - `docs/differentiable_substrate.md` (new)
- **Acceptance Criteria:**
    - [ ] 19-kernel index table: forward kernel name | backward kernel name | FD tolerance achieved | test file
    - [ ] Saved-state contract: what `xpbd_full_fwd` writes (positions, velocities, density, ∇C, denominator helpers, per-kernel auxiliaries) and what `xpbd_full_bwd` consumes
    - [ ] Add-a-paired-kernel runbook (forward implementation → analytic backward derivation → FD test → hookup into `ops_xpbd_full.mm`)
    - [ ] Cross-links to existing docs (metal_diff/README, M7_XPBD_PLAN.md) rather than re-presenting XPBD math
- **Sponsor Summary Hint:** Don't re-derive XPBD — that's in metal_diff/README + M7_XPBD_PLAN.md. The genuine missing pieces are the saved-state contract spec and the runbook for adding new paired kernels (currently you reverse-engineer it from the existing kernels). Plus a single index table so the 19 paired kernels can be found in one place.

---

---

### Issue #246: Static GitHub Action — post Validation Methodology checklist on substrate-touching PRs

- **Title:** `[DD001] Static GitHub Action that posts Validation Methodology checklist on substrate-touching PRs`
- **Labels:** `DD001`, `ai-workable`, `L2`, `ci`, `docs`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.1 — Phase 1 Substrate Documentation](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** ci-cd, python, github-api
- **Audit note (rewrite of original MoaW PR assist):** The Mind-of-a-Worm bot is in-development per the [AI Contributors page](../contributing/ai-contributors.md) ("coming online in Q2 2026"). Filing an issue that depends on MoaW assumes infrastructure that doesn't exist. **Decouple the deliverable** — a 100-line GitHub Action using Python + `gh` CLI can scan the PR diff for the artifacts the 8-phase checklist names (parity MP4, SGD history JSON, FD test) and post a checklist-status comment, no LLM/bot required. If MoaW lands later, it subsumes the action.
- **DD Section to Read:** [DD001 §Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology), [§MoaW PR Review Checklist](DD001_Body_Physics_Architecture.md#mind-of-a-worm-pr-review-checklist)
- **Depends On:** None
- **Files to Modify:**
    - `.github/workflows/validation_methodology.yml` (new)
    - `scripts/validation_checklist.py` (new — static diff scanner)
- **Acceptance Criteria:**
    - [ ] Workflow triggers on PRs touching `src/sphFluid*.cl`, `src/metal_diff/**`, or `src/cuda/**`
    - [ ] Script statically scans the PR diff for: written prediction (PR description or commit message section), OpenCL reference trajectory under `tests/data/`, Metal/CUDA trajectory dump, side-by-side MP4 under `docs/`, SGD history JSON under `tools/sgd_history/`, new FD test file
    - [ ] Posts a checklist-status comment on the PR (does not block merge)
    - [ ] No dependency on Mind-of-a-Worm or any LLM infrastructure
- **Sponsor Summary Hint:** The validation-methodology checklist needs to surface automatically on PRs touching kernel code. A static GitHub Action does this without depending on MoaW. If MoaW eventually lands, it can replace the action; until then, contributors get the checklist immediately.

---

---

### Issue #249: Add CONTRIBUTING.md (link-heavy, owns only what has no other home)

- **Title:** `[DD001] Add CONTRIBUTING.md — link-heavy to README/metal_diff/DD001, own only PR checklist + branch convention`
- **Labels:** `DD001`, `ai-workable`, `L1`, `docs`, `onboarding`
- **Roadmap Phase:** Phase 1
- **Milestone:** [v0.1.1 — Phase 1 Substrate Documentation](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** docs
- **Audit note:** No `CONTRIBUTING.md` exists today. `AGENTS.md` carries minimal contributor guidance. The README has Building sections per-substrate, Quickstart, and per-substrate build scripts. `src/metal_diff/README.md` documents the FD-test pattern. DD001 has Validation Methodology + Quality Criteria. **The CONTRIBUTING.md should link to those, not duplicate them** — its unique content is the PR checklist, branch convention, and the add-a-kernel runbook (which is also delivered in [#245](#issue-245-document-xpbd_full-saved-state-contract-add-a-paired-kernel-runbook); cross-reference).
- **DD Section to Read:** [DD001 §Quality Criteria](DD001_Body_Physics_Architecture.md#quality-criteria), [§Validation Methodology](DD001_Body_Physics_Architecture.md#validation-methodology)
- **Depends On:** None
- **Acceptance Criteria:**
    - [ ] `CONTRIBUTING.md` created at repo root (GitHub renders it in the PR creation UI)
    - [ ] Prerequisites + build instructions: **link** to README sections, don't duplicate
    - [ ] Testing workflow: **link** to existing scripts (`measure_cube_stability.py`, `test_backend_parity.py`)
    - [ ] PR checklist: own this content (DD001 §Quality Criteria + MoaW checklist, condensed)
    - [ ] Branch naming convention (`dd001/description`): own this content
    - [ ] Add-a-kernel runbook: **link** to #245's `differentiable_substrate.md`, don't fork
    - [ ] Total length ~1.5 pages
- **Sponsor Summary Hint:** GitHub renders CONTRIBUTING.md in the PR creation UI — that's real value the README can't replace. But the file should mostly link to README/metal_diff/DD001 rather than duplicating their content. Own only what has no other home: PR checklist + branch convention.

---

---

## Group 4: v0.4.0 — Phase 4 Sensory Coupling (Closed-Loop)

Sibernetic-side support for closed-loop sensorimotor work. Deferral target for DD015 / DD019 until those held-back DDs publish; this milestone holds the in-process Simulation handle that the closed-loop tight loop needs.

---

### Issue #250: In-process Simulation handle for tight-loop closed-loop control

- **Title:** `[DD001] In-process Simulation handle for closed-loop tight-loop control`
- **Labels:** `DD001`, `human-expert`, `L3`, `closed-loop`
- **Roadmap Phase:** Phase 4
- **Milestone:** [v0.4.0 — Phase 4 Sensory Coupling](#milestones)
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, c++, pybind11
- **DD Section to Read:** [DD001 §Integration Contract](DD001_Body_Physics_Architecture.md#integration-contract)
- **Depends On:** DD015 (Touch Response) and/or DD019 (Proprioceptive Feedback) publishing — these establish the closed-loop coupling requirement that motivates this issue.
- **Audit note (Python already present in Sibernetic):** Sibernetic already has substantial Python infrastructure today: `src/owSignalSimulator.cpp` embeds CPython for the C++→Python neural-callback path (NEURON/c302 integration); `sibernetic_c302.py`, `src/metal_diff/dump_metal_trajectory.py`, and the SGD harnesses (`src/metal_diff/sgd_*.py`) all drive the simulation via subprocess; `tests/`, `scripts/`, and `wcon/` carry the post-processing and parity-test Python. The subprocess pattern handles every existing workflow today. **This issue is not about replacing that — it's narrowly about the per-timestep tight-loop case that subprocess overhead would block.**
- **Approach:** Add a single `Simulation` Python class with the minimum surface area for tight-loop closed-loop control. Builds on `owSignalSimulator.cpp`'s existing CPython embedding (the inverse direction). No `pip install`-able package, no replacement of the existing subprocess pattern — the binding is an additive option for workflows that need it.
- **Files to Modify:**
    - `python/sibernetic_loop.cpp` (new — pybind11 wrapper, minimum surface)
    - `python/sibernetic/__init__.py` (new — in-repo Python module, NOT a pip package)
    - `CMakeLists.txt` (add pybind11 target)
- **Test Commands:**
    - `python3 -c "from python.sibernetic import Simulation; sim = Simulation('configuration/worm_crawl_demo'); sim.step(); print(sim.get_positions()[:5])"`
    - Closed-loop control demo: read SPH strain → compute Python-side sensory response → inject muscle activation → step. Measure tight-loop overhead vs subprocess.
- **Acceptance Criteria:**
    - [ ] `Simulation(config_path)` constructs an in-process simulation instance
    - [ ] `.step()` advances one timestep without subprocess overhead
    - [ ] `.get_positions()`, `.get_velocities()` return particle state via direct memory access (zero-copy via numpy buffer protocol where possible)
    - [ ] `.set_muscle_activation(quadrant, value)` injects activation for the next step
    - [ ] Closed-loop demo shows the per-timestep loop is meaningfully faster than the equivalent subprocess pattern (target: <10% of subprocess time)
    - [ ] **Does not** require `pip install` or break the existing subprocess workflows in `sibernetic_c302.py`, `dump_metal_trajectory.py`, or the SGD harnesses
- **Sponsor Summary Hint:** Sibernetic already has substantial Python — embedded CPython for the neural callback, subprocess-driven Python for everything else. That works fine for current workflows. What it doesn't work for is the per-timestep tight loop a closed-loop sensorimotor controller needs: read strain, compute a sensory response, inject muscle activation, step. This issue adds a minimal `Simulation` class with just those four operations for the closed-loop case. It's scoped to support DD015/DD019 when they publish; until then, subprocess is the right answer.

---

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Fresh issues to file** | 18 |
| **ai-workable** | 8 |
| **human-expert** | 10 |
| **L1** | 7 |
| **L2** | 7 |
| **L3** | 4 |
| **Existing issues kept live** | ~12 (see [Migration Context](#migration-context-stabilize-the-gold-standard-while-building-forward)) |
| **Existing issues to defer to later milestones** | ~11 |
| **Existing issues to actually close** | 3 |
| **Originally-proposed issues dropped after audit** | 3 (surface mesh → DD012 viewer repo; architecture overview → README addendum; FEM eval → DD001 prose only) |

| Group | Milestone | Issues | Target |
|-------|-----------|--------|--------|
| **1: Parity Harness + Per-Demo Parity + CUDA Phase 3** | v0.0.9 — Phase 0 Modernization | [#236](#issue-236-generalize-teststest_demo1_backend_paritypy-into-a-scenario-registry-harness), [#237](#issue-237-lock-demo1-parity-test-into-ci), [#238](#issue-238-add-demo2-membrane-permeability-parity-gate-to-harness), [#239](#issue-239-add-worm_alone-parity-gate-worm-com-cross-section-max-span-metrics), [#240](#issue-240-implement-ihmsen-2010-boundary-active-sph-pressure-replaces-floor_y-proxy), [#241](#issue-241-rewrite-xpbd-density-inner-loop-with-pcisph-iterative-pressure), [#242](#issue-242-worm_swim_half_resolution-set-up-muscle-driven-scenario-and-add-parity-gate), [#243](#issue-243-cuda-phase-3-port-wpoly6_inplace-prove-nvcc-build-fd-validate-against-metal) | Generalize parity harness, lock in demo1/demo2/worm_alone, Ihmsen 2010 boundary pressure, PCISPH iterative rewrite, worm_swim driven scenario, CUDA Phase 3 |
| **2: Validation Tooling + Output Pipeline** | v0.1.0 — Phase 1 Validation Infrastructure | [#233](#issue-233-extend-scriptsmeasure_cube_stabilitypy-with-nanescapevelocity-checks), [#234](#issue-234-emit-per-particle-density-alongside-position-output-both-substrates), [#235](#issue-235-create-scriptsvalidate_incompressibilitypy-depends-on-234), [#247](#issue-247-ome-zarr-post-processing-converter-contingent-on-dd012-viewer-contract), [#248](#issue-248-plumb-simulationoutput_interval-from-openwormyml-through-to-existing-logstep-knob) | Extend stability checker, emit per-particle density, incompressibility validator, OME-Zarr converter (contingent on DD012 contract), output-interval YAML plumbing |
| **3: Substrate Docs + Contributor Onboarding** | v0.1.1 — Phase 1 Substrate Documentation | [#244](#issue-244-add-opencl-kernel-call-graph-equation-table-gotchas-appendix), [#245](#issue-245-document-xpbd_full-saved-state-contract-add-a-paired-kernel-runbook), [#246](#issue-246-static-github-action-post-validation-methodology-checklist-on-substrate-touching-prs), [#249](#issue-249-add-contributingmd-link-heavy-owns-only-what-has-no-other-home) | OpenCL kernel call graph + table, paired-kernel runbook + saved-state contract, static PR-checklist GitHub Action, link-heavy CONTRIBUTING.md |
| **4: Closed-Loop** | v0.4.0 — Phase 4 Sensory Coupling | [#250](#issue-250-in-process-simulation-handle-for-tight-loop-closed-loop-control) | In-process Simulation handle |

### Dependency Graph (Critical Path)

All issue-to-issue dependencies are within the same milestone (no
backwards cross-milestone deps).

```
v0.0.9 — Phase 0 Modernization
──────────────────────────────
  Issue #236 (generalize parity harness) ─┬→ Issue #237 (demo1 CI lock-in)
                                          ├→ Issue #238 (demo2 harness entry)
                                          ├→ Issue #239 (worm_alone harness entry)
                                          └→ Issue #242 (worm_swim parity)
  Issue #240 (Ihmsen 2010 boundary)  — follow-up from #239's known caveat;
                                       standalone physics work
  Issue #241 (PCISPH iterative)      ─→ Issue #242 (worm_swim parity)
  Issue #243 (CUDA Phase 3)          — independent; on success, derive
                                       Phases 2-5 separately

v0.1.0 — Phase 1 Validation Infrastructure
──────────────────────────────────────────
  Issue #233 (extend stability checker) — independent
  Issue #234 (density dump prereq)      ─→ Issue #235 (incompressibility validator)
  Issue #247 (OME-Zarr converter)       — gated on DD012 viewer contract
  Issue #248 (output-interval plumbing) — depends on DD011 config loading

v0.1.1 — Phase 1 Substrate Documentation
────────────────────────────────────────
  Issue #244 (OpenCL kernel call graph) — independent
  Issue #245 (paired-kernel runbook)    — independent; cross-refs with #249
  Issue #246 (static PR-checklist)      — independent
  Issue #249 (CONTRIBUTING.md)          — cross-refs #245 for add-a-kernel runbook

v0.4.0 — Phase 4 Sensory Coupling
─────────────────────────────────
  Issue #250 (in-process Simulation handle) — depends on DD015 / DD019 publishing
```
