# DD012: Design Document RFC Process (How Decisions Are Made)

**Status:** Proposed (Governance)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** Informal decision-making  
**Related:** [DD011](DD011_Contributor_Progression_Model.md) (Contributor Progression), AI-Augmented Open Science Proposal

---

## Context

Currently, architectural decisions in OpenWorm happen through:
- Informal Slack discussions
- GitHub issue debates
- Private conversations
- Founder's judgment

This creates problems:
- Decisions are **not documented** (newcomers re-propose rejected approaches)
- **Rationale is lost** (future contributors don't know *why* decisions were made)
- **No clear process** for contributors to propose changes
- **Founder becomes bottleneck** for all decisions

The Rust project's **RFC (Request for Comments) process** provides a proven model for preserving vision while distributing decision-making. Python's **PEP (Python Enhancement Proposal)** system serves a similar function.

---

## Decision

### All Major Architectural Decisions Must Be Documented as Design Documents

A "major architectural decision" is any change that:
- Affects multiple subsystems
- Changes a fundamental modeling approach (e.g., switching from HH to FitzHugh-Nagumo)
- Adds a new data source or validation target
- Changes contributor workflows or policies
- Has long-term implications (difficult to reverse)

**Not major:** Bug fixes, parameter tuning within documented ranges, documentation improvements, refactoring that preserves behavior.

### Design Document Template

Every Design Document follows this structure. **Lead with impact, end with background.** A contributor reading top-to-bottom should answer "what do I build?" on page 1, not page 5.

```markdown
# DD###: Title

**Status:** Proposed | Accepted | Superseded | Rejected  
**Author:** Name(s)  
**Date:** YYYY-MM-DD  
**Supersedes:** DD### (if applicable)  
**Related:** DD### (cross-references)

## TL;DR                                         ← REQUIRED
2-3 sentences. What this DD does, why it matters,
and the single most important success metric.

## Goal & Success Criteria                        ← REQUIRED
- Which [DD010](DD010_Validation_Framework.md) validation tier does this improve?
- Quantitative success metric (threshold, not vague)
- Before/after: what simulation gains

## Deliverables                                   ← REQUIRED
- Exact files on disk (paths relative to repo root)
- File formats
- Example content snippet or schema

## Repository & Issues                            ← REQUIRED
- GitHub repo (e.g., `openworm/c302`)
- Issue label convention (e.g., `dd005`)
- Milestone link
- Example PR title

## How to Build & Test                            ← REQUIRED
- Prerequisites (Docker, packages, data downloads)
- Step-by-step commands (copy-pasteable)
- Expected output at each step
- Green light criteria (what "success" looks like)
- Scripts that don't exist yet: mark [TO BE CREATED]
  with a GitHub issue link

## How to Visualize                               ← REQUIRED
- Which [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer layer displays this work
- Color mapping or rendering specification
- What you should SEE when it works correctly
- (If not applicable, e.g., governance DDs: state "N/A")

## Technical Approach                             ← REQUIRED
(The science/engineering — models, equations,
 parameters, algorithms. Renamed from "Decision.")

## Alternatives Considered                        ← REQUIRED
What other approaches were evaluated?
Why were they rejected?

## Quality Criteria                               ← REQUIRED
How will we know if an implementation is correct?
What tests must pass? What validation is required?

## Boundaries (Explicitly Out of Scope)           ← REQUIRED
What does this DD NOT cover?

## Context & Background                           ← REQUIRED
Why is this decision needed? Biological background,
prior art, project history. (Moved from top —
contributors who need action first, context second.)

## Implementation References                      ← OPTIONAL
Code locations, data sources, external documentation.

## Migration Path                                 ← OPTIONAL
If this decision changes in the future, how do we
transition?

## References                                     ← REQUIRED
Papers, datasets, external documentation.

## Integration Contract                           ← REQUIRED
(See expanded requirements below)
```

### Integration Contract Required Sub-Sections

Every science/infrastructure DD's Integration Contract MUST include:

```markdown
## Integration Contract

### Inputs / Outputs
Tables of what this subsystem consumes and produces.
Each row: Input/Output name, Source/Consumer DD,
Variable name, Format, Units, Timestep (if applicable).

### Repository & Packaging
- Primary repository (e.g., `openworm/c302`)
- Docker stage in multi-stage build ([DD013](DD013_Simulation_Stack_Architecture.md))
- `versions.lock` key
- Build dependencies (pip/apt packages)

### Configuration
- `openworm.yml` section with all keys documented
- Default values and valid ranges

### How to Test (Contributor Workflow)
- `docker compose run quick-test` — what it checks
- `docker compose run validate` — which [DD010](DD010_Validation_Framework.md) tiers
  block merge
- Per-PR checklist (what must pass before merge)

### How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) Connection)
- Which OME-Zarr groups this DD's output populates
- Which viewer layer displays it
- Color mapping specification

### Coupling Dependencies
- Upstream: what I depend on, what breaks if they change
- Downstream: who depends on me, what breaks if I change
```

### RFC Workflow (Rust-Style)

**Step 1: Proposal**
- Anyone (L1+) can propose a Design Document
- Open a PR to `openworm-admin/design_documents/` with a new DD file
- Assign a DD number (next available, e.g., [DD013](DD013_Simulation_Stack_Architecture.md))
- Tag relevant subsystem maintainers (L4) for review

**Step 2: Discussion**
- Community discusses in PR comments
- Author revises based on feedback
- Subsystem maintainer (L4) facilitates discussion, ensures all concerns are addressed

**Step 3: Decision**
- **For subsystem-specific DDs:** L4 maintainer makes final decision (approve/reject/request-changes)
- **For cross-cutting DDs:** L4 maintainers reach consensus; if conflict, founder (L5) arbitrates
- **For governance DDs:** Founder decides after community input

**Step 4: Approval**
- Status changed to "Accepted"
- PR merged
- DD becomes binding

**Step 5: Implementation**
- Code changes to implement the DD are tracked separately (GitHub issues, milestones)
- Implementation PRs reference the DD number
- Mind-of-a-Worm checks that implementation PRs comply with the DD

### When to Write a Design Document vs. Just Opening a PR

**Write a DD if:**
- The change affects how other contributors will work
- You are proposing a new modeling approach
- You are adding a major dataset or validation target
- You are changing an existing Design Document

**Just open a PR if:**
- Fixing a bug
- Improving documentation
- Adding tests
- Refactoring without changing behavior
- Making changes within an existing DD's scope

---

## Alternatives Considered

### 1. Benevolent Dictator (Founder Decides Everything)

**Rejected:** Does not scale. Founder becomes bottleneck. Decisions are not transparent or documented.

### 2. Consensus Without Documentation (Slack Discussions Only)

**Rejected:** Decisions are lost to Slack history. Newcomers don't know what was decided or why. Constantly re-litigating settled questions.

### 3. Formal Voting on Every Decision

**Rejected:** Voting ends discussion and creative thinking (Fogel). Consensus-seeking is preferable. Voting is last resort.

### 4. No Process (Let Code Speak)

**Rejected:** "Code is the documentation" fails for architectural decisions. Why a particular approach was chosen over alternatives is not visible in the code.

---

## Quality Criteria

### What Makes a Good Design Document?

1. **Actionable:** A contributor can implement the DD without needing additional clarification.

2. **Justification of Alternatives:** Explains *why* rejected approaches were rejected, preventing re-proposals.

3. **Clear Scope:** Boundaries section makes explicit what the DD does NOT cover.

4. **Testable:** Quality criteria are measurable (acceptance thresholds, validation procedures).

5. **Concise:** Aim for 1,000-2,000 words. If longer, split into multiple DDs.

6. **Living Document:** Can be amended. If a DD proves wrong or incomplete, propose a new DD that supersedes it.

7. **Validation-First:** Goal & Success Criteria section must reference a specific [DD010](DD010_Validation_Framework.md) tier and quantitative threshold. The reader should know what "done" looks like before reading the technical approach.

8. **Concrete Deliverables:** Must list exact output files with paths, not just describe them in prose. A contributor should know precisely what artifacts they are building.

9. **Runnable Commands:** Build & Test section must contain commands that a contributor can copy-paste. Scripts referenced must either exist or be marked `[TO BE CREATED]` with a GitHub issue link.

10. **Visualizable:** Must describe what the work looks like in the [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer. If not applicable (governance DDs), state "N/A."

### Bad Design Document Anti-Patterns

1. **Vague:** "Use good ion channel models." → What defines "good"?
2. **No alternatives:** Only describes the chosen approach, doesn't explain why others were rejected.
3. **Untestable:** No validation criteria, no way to know if implementation is correct.
4. **Scope creep:** Tries to cover too much. Split into focused DDs.
5. **Obsolete:** DD written years ago, no longer reflects current practice. Mark as "Superseded."
6. **Buried punchline:** Validation goal appears at Step 6 instead of being the starting point. Lead with WHY, not HOW.
7. **Phantom scripts:** Commands reference scripts that don't exist and have no issue tracking their creation.
8. **Disconnected from viewer:** No description of how work appears in the visualization layer. Contributors can't see what they're building.
9. **No repo guidance:** Contributor can't determine which repo to clone, where to file issues, or what to name their branch.

---

## Mind-of-a-Worm Enforcement

Mind-of-a-Worm uses Design Documents as **automated review criteria**:

**When a PR is opened:**
1. Mind-of-a-Worm identifies which subsystem (based on files modified)
2. Retrieves relevant Design Documents (e.g., modifying `c302/` triggers [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
3. Checks **subsystem compliance:**
   - Are changes within the DD's scope?
   - Do quality criteria pass? (e.g., NeuroML validation, test coverage)
   - Are alternatives-considered principles violated? (e.g., re-proposing integrate-and-fire for all neurons when [DD001](DD001_Neural_Circuit_Architecture.md) explicitly rejected this)
4. Checks **integration compliance** (Integration Contract section):
   - Does the PR change any **output variable** listed in the DD's Integration Contract?
   - If yes: Identify all **consuming DDs** from the Coupling Dependencies table and tag their maintainers
   - Does the PR add configurable parameters? If yes: verify `openworm.yml` schema is updated
   - Has the contributor run the integration test (`docker compose run quick-test`)?
5. Posts automated review comment:
   - ✅ "Passes [DD001](DD001_Neural_Circuit_Architecture.md) quality criteria (NeuroML validates, units correct)"
   - ⚠️ "Warning: Modifies core HH parameters; confirm alignment with [DD001](DD001_Neural_Circuit_Architecture.md) Section 2.3"
   - ⚠️ "**Integration alert:** This PR modifies calcium output format ([DD001](DD001_Neural_Circuit_Architecture.md) Integration Contract). [DD002](DD002_Muscle_Model_Architecture.md) (Muscle) and [DD003](DD003_Body_Physics_Architecture.md) (Body Physics) consume this output. @muscle-maintainer @body-physics-maintainer please verify integration."
   - ❌ "Violates [DD001](DD001_Neural_Circuit_Architecture.md): Uses IAF model for all neurons (rejected in [DD001](DD001_Neural_Circuit_Architecture.md) Alternatives)"
   - ❌ "Missing integration test: No evidence of `docker compose run quick-test` in PR description"

**Human reviewer** (L3+) considers Mind-of-a-Worm's assessment but makes final decision. **For PRs that modify coupling interfaces, at least one reviewer from each affected consuming subsystem must approve.**

---

## Migration Path

### Bootstrapping the DD System

**Current state:** Zero Design Documents exist (except those created in this proposal).

**Phase 1 (Week 1-4):** Founder writes initial DDs for existing subsystems:
- [DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md): Neural, Muscle, Physics (document current architecture)
- [DD005](DD005_Cell_Type_Differentiation_Strategy.md)-[DD010](DD010_Validation_Framework.md): Future work (document proposed phases)
- [DD011](DD011_Contributor_Progression_Model.md)-[DD012](DD012_Design_Document_RFC_Process.md): Governance

**Phase 2 (Month 2-3):** Community reviews. Open each DD as a PR, invite discussion, revise.

**Phase 3 (Month 4+):** DDs are accepted, become binding. New proposals follow RFC process.

---

## Examples of When a DD Is Needed

### Example 1: Switching from NEURON to Brian2 Simulator

**Trigger:** Contributor proposes replacing NEURON with Brian2 for faster simulation.

**Action:**
1. Write [DD013](DD013_Simulation_Stack_Architecture.md): "Simulator Backend Selection"
2. Include: Context (why switch?), Decision (Brian2 vs. NEURON), Alternatives (NEST, custom solver), Quality Criteria (must reproduce all existing validation), Migration Path (parallel implementation during transition)
3. Open RFC PR
4. Community discusses performance benchmarks, NeuroML compatibility, learning curve
5. L4 Neural Circuit maintainer decides

**Outcome:** Either approved (begin migration) or rejected (stay with NEURON, document why).

### Example 2: Adding Sensory Transduction Models

**Trigger:** Contributor wants to model mechanosensation in touch neurons (ALM, AVM, PLM).

**Action:**
1. Write [DD014](DD014_Dynamic_Visualization_Architecture.md): "Mechanosensory Transduction (MEC-4 Channel Model)"
2. Include: MEC-4/MEC-10 DEG/ENaC channel kinetics, Goodman et al. 1998 data, coupling to Sibernetic mechanical strain
3. Open RFC PR
4. Discuss with L4 Neural Circuit maintainer
5. Approve

**Outcome:** [DD014](DD014_Dynamic_Visualization_Architecture.md) becomes the specification. Contributor implements according to [DD014](DD014_Dynamic_Visualization_Architecture.md). Mind-of-a-Worm checks compliance.

---

## References

1. **Rust RFC Process:** rust-lang.github.io/rfcs/
2. **Python PEPs:** peps.python.org
3. **Architecture Decision Records:** Google Cloud ADR guide, 18F blog
4. **Fogel, *Producing Open Source Software*** (Chapter on written culture and design docs)

---

**Approved by:** Pending (governance DD, requires community ratification)
**Implementation Status:** Proposed
**Next Actions:**
1. Publish [DD001](DD001_Neural_Circuit_Architecture.md)-[DD012](DD012_Design_Document_RFC_Process.md) for community review
2. Set up design_documents/ directory in CElegansNeuroML and Sibernetic repos
3. Document DD RFC process in CONTRIBUTING.md
4. Train Mind-of-a-Worm on DD compliance checking
