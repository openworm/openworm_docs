# Contributing to Design Documents

This guide covers how to use, write, review, and contribute to OpenWorm Design Documents. For the overview of all DDs and the implementation roadmap, see the [Design Documents Overview](index.md).

---

## How to Use Design Documents

### For Contributors

**Before implementing a feature:**

1. Check if a relevant DD exists (search this directory or ask in #development Slack)
2. Read the DD's "Technical Approach" and "Quality Criteria" sections
3. Check the DD's Integration Contract (what it consumes from other DDs, what it produces)
4. Implement according to the DD's specifications
5. Run the DD's validation procedure (`docker compose run quick-test`, `docker compose run validate`)
6. Reference the DD number in your PR description (e.g., "Implements [DD005](DD005_Cell_Type_Differentiation_Strategy.md) CeNGEN calibration")

**If you disagree with a DD:**

1. Propose a new DD that supersedes it (follow [DD012](DD012_Design_Document_RFC_Process.md) RFC process)
2. Do NOT silently deviate from an accepted DD without approval

### For Reviewers (L3+)

**When reviewing a PR:**

1. Check which DDs are relevant (Mind-of-a-Worm will flag these automatically)
2. Verify the PR aligns with DD specifications (check Quality Criteria section)
3. **If PR modifies a coupling interface** (changes output format, variable names, OME-Zarr schema):
    - Check the DD's "Depends On Me" table in Integration Contract
    - Tag maintainers of consuming DDs for coordination
    - Require integration test evidence (`docker compose run validate` output)
4. If the PR deviates from a DD, request justification or DD amendment via [DD012](DD012_Design_Document_RFC_Process.md) RFC

### For Mind-of-a-Worm AI

**Automated compliance checking:**

- Parse PR files to identify affected subsystems (e.g., `c302/` → [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md))
- Retrieve relevant DDs and their Integration Contracts
- Check:
  - ✅ NeuroML validation ([DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md): `jnml -validate` must pass)
  - ✅ Unit compliance ([DD010](DD010_Validation_Framework.md): biophysical units correct)
  - ✅ Parameter ranges (conductances, voltages, time constants within DD-specified ranges)
  - ⚠️ Coupling interface changes (flag if output variables, file formats, or OME-Zarr schema modified)
  - ❌ Alternatives-considered violations (re-proposing explicitly rejected approaches)
- Post automated review comment with pass/warn/fail status per DD
- Tag relevant L4 maintainers for cross-subsystem coordination

---

## Design Document Lifecycle

```
┌─────────────┐
│  Proposed   │ ← New DD opened as PR to openworm-admin
└──────┬──────┘
       │ Community discussion in PR comments, DD revised based on feedback
       v
┌─────────────┐
│  Accepted   │ ← L4 maintainer (subsystem-specific) or L5 founder approves, PR merged
└──────┬──────┘
       │ Implementation proceeds (GitHub issues created, PRs reference DD)
       │
       ├─── Implementation complete, validation passes → Stable (no further changes unless bugs found)
       │
       ├─── New DD proposed that supersedes this one → Superseded (reference new DD number in header)
       │
       └─── Community testing reveals approach is wrong → Rejected (rare, but document why for future)
```

**Status definitions:**

- ✅ **Accepted:** Binding specification. All implementations must comply. Can be amended via [DD012](DD012_Design_Document_RFC_Process.md) RFC.
- ⚠️ **Proposed:** Under review or approved but not yet implemented. Not binding until marked Accepted.
- 🔴 **Blocked:** Cannot proceed due to missing prerequisite (e.g., [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) blocked on toolbox dormancy).
- 📦 **Archived / Backburner:** Deferred or superseded. Do not implement without reopening discussion.
- **Superseded:** Replaced by a newer DD. Reference the superseding DD number.
- **Rejected:** Explicitly not adopted. Alternatives Considered section documents why.

---

## Template & Reference

- **[DD012](DD012_Design_Document_RFC_Process.md):** Defines the Design Document template and all required sections (TL;DR, Goal, Deliverables, Build & Test, How to Visualize, Technical Approach, Alternatives, Quality Criteria, Boundaries, Integration Contract)
- **[DD005](DD005_Cell_Type_Differentiation_Strategy.md):** **Reference implementation** — demonstrates the full expanded template with all sections filled. Use [DD005](DD005_Cell_Type_Differentiation_Strategy.md) as your model when writing a new DD.
- **[DD001](DD001_Neural_Circuit_Architecture.md):** Example of Quick Action Reference table (7 key questions answered at the top)

All science DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)-[DD019](DD019_Closed_Loop_Touch_Response.md)) include a **Quick Action Reference** table answering:

1. What does this produce?
2. Success metric (which [DD010](DD010_Validation_Framework.md) tier, quantitative threshold)
3. Repository (GitHub link, issue label convention)
4. Config toggle (openworm.yml keys)
5. Build & test (docker commands, green-light criteria)
6. Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) layer, color mapping, what you should see)
7. CI gate (what blocks merge)

---

## Writing Your First Design Document

### Step 1: Check Mission Alignment

**Before writing a DD, ask:**

- Does this advance the mission ("world's first virtual organism")?
- Does it maintain physical realism ("soft and squishy")?
- Is it experimentally validated ([DD010](DD010_Validation_Framework.md) tiers)?
- Is it open source and causally interpretable?

**If yes to all:** Proceed. **If no:** Reconsider or clarify how it serves the mission.

### Step 2: Check if a DD Already Exists

Search this directory:
```bash
grep -r "keyword" design_documents/*.md
```

Check [INTEGRATION_MAP.md](INTEGRATION_MAP.md) — your topic may be covered by an existing DD's Integration Contract.

### Step 3: Use the Template

Follow [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) template structure. Use [DD005 (Cell-Type Specialization)](DD005_Cell_Type_Differentiation_Strategy.md) as your reference implementation.

**Required sections (from [DD012](DD012_Design_Document_RFC_Process.md)):**

- TL;DR (2-3 sentences)
- Goal & Success Criteria (which [DD010](DD010_Validation_Framework.md) tier, quantitative threshold)
- Deliverables (exact files, paths, formats)
- Repository & Issues (GitHub repo, issue label, branch convention)
- How to Build & Test (copy-pasteable commands, green-light criteria)
- How to Visualize ([DD014](DD014_Dynamic_Visualization_Architecture.md) layer, color mapping, what you should see)
- Technical Approach (equations, parameters, algorithms)
- Alternatives Considered (why other approaches were rejected)
- Quality Criteria (testable acceptance criteria)
- Boundaries (explicitly out of scope)
- Context & Background (biological motivation, project history)
- References (papers, datasets, DOIs)
- Integration Contract (inputs/outputs, repository & packaging, configuration, how to test, how to visualize, coupling dependencies)

### Step 4: Check Integration Map

Before finalizing your DD, check [INTEGRATION_MAP.md](INTEGRATION_MAP.md):

- Which DDs does yours depend on? (Add to "I Depend On" table)
- Which DDs will depend on yours? (Add to "Depends On Me" table)
- What data format do you consume/produce? (Document in Integration Contract)
- Who's the upstream/downstream maintainer? (Coordinate before merging)

### Step 5: Open RFC PR

```bash
cd openworm-admin/
git checkout -b rfc/dd0XX-your-topic
# (write DD0XX_Your_Topic.md)
git add design_documents/DD0XX_Your_Topic.md
git commit -m "RFC: DD0XX Your Topic"
git push origin rfc/dd0XX-your-topic
# Open PR on GitHub, tag relevant L4 maintainers
```

### Step 6: Respond to Feedback & Iterate

- Community discusses in PR comments
- You revise based on feedback
- Subsystem L4 maintainer facilitates discussion
- If fundamental disagreement: L5 founder arbitrates

### Step 7: Implementation (After Approval)

Once DD is approved and merged:

- DD status changes to "Accepted"
- Open implementation issues (or run `dd_issue_generator.py` to auto-generate from Integration Contract)
- Implementation PRs reference the DD number
- Mind-of-a-Worm checks implementation PRs for DD compliance

---

## Examples of Excellent Design Documents

### [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Cell-Type Specialization) — REFERENCE IMPLEMENTATION

**Why it's excellent:**

- ✅ **TL;DR at top** — Reader knows what/why/success metric in 3 sentences
- ✅ **Mission-aligned** — Uses CeNGEN (world's largest single-cell atlas for any organism) to create biologically distinct neurons
- ✅ **Goal & Success Criteria** — [DD010](DD010_Validation_Framework.md) Tier 2, quantitative threshold (≥20% improvement in functional connectivity)
- ✅ **Deliverables** — Exact files (128 `.cell.nml` files), paths, formats (NeuroML 2 XML)
- ✅ **Repository & Issues** — `openworm/c302`, issue label `dd005`, branch convention
- ✅ **How to Build & Test** — 8 copy-pasteable commands, green-light criteria, scripts marked `[TO BE CREATED]`
- ✅ **How to Visualize** — [DD014](DD014_Dynamic_Visualization_Architecture.md) neural/ layer, color-by-neuron-class mode
- ✅ **Technical Approach** — 6-step pipeline with code examples
- ✅ **7 alternatives considered** — All rejected with rationale
- ✅ **Integration Contract** — Complete with all 5 required sub-sections

### [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit Architecture)

**Why it's excellent:**

- ✅ **Quick Action Reference** — 7-question table at top answers contributor questions immediately
- ✅ **Clear decision** — Level C1 graded synapses (not IAF, not spiking), biologically justified
- ✅ **Quantitative parameters** — Table of conductances with exact values and units
- ✅ **Alternatives explained** — IAF rejected, AlphaFold+MD rejected, multicompartmental deferred
- ✅ **Validation procedure** — 5-step command sequence from `jnml -validate` to kinematic comparison
- ✅ **Migration path** — If decision changes, add Level D (don't modify C1, backward compatibility sacred)

---

## Anti-Patterns (What NOT to Do)

From [DD012](DD012_Design_Document_RFC_Process.md) Quality Criteria section:

**❌ Too vague:**
> "We should use realistic channel models."

*What's realistic? Which channels? What parameters? Which papers?*

**❌ No alternatives:**
> "We decided to use SPH for body physics."

*Why not FEM? Why not mass-spring? Future contributors will re-propose without knowing they were already rejected.*

**❌ No validation:**
> "Implement IP3 receptor model."

*How do you know if it works? What's the acceptance test? Which [DD010](DD010_Validation_Framework.md) tier?*

**❌ Scope creep:**
> "This DD covers neurons, muscles, intestine, hypodermis, and gonad."

*Too broad. Split into focused DDs (one per organ system).*

**❌ Buried punchline:**
> Validation goal appears at line 300 instead of the Goal section (line 30).

*Lead with WHY and WHAT (impact), end with HOW (background). [DD012](DD012_Design_Document_RFC_Process.md) template enforces this.*

**❌ Phantom scripts:**
> Commands reference `validate_network.py` with no tracking, no `[TO BE CREATED]` marker.

*Mark all non-existent scripts `[TO BE CREATED]` with GitHub issue link or #TBD.*

**❌ Disconnected from viewer:**
> No "How to Visualize" section, no mention of [DD014](DD014_Dynamic_Visualization_Architecture.md) layers.

*Contributors can't see what they're building. Every science DD must specify its [DD014](DD014_Dynamic_Visualization_Architecture.md) visualization.*

**❌ No repo guidance:**
> Doesn't specify which GitHub repo, where to file issues, branch naming convention.

*Contributor doesn't know where to start. Repository & Issues section is required.*

**❌ Consecutive bold-key lines without list markers:**
> ```
> **Status:** Accepted
> **Author:** OpenWorm Core Team
> **Date:** 2026-02-14
> ```

*Standard Markdown treats consecutive lines as a single paragraph — these will render as one run-together line. Always use list markers (`- `) for metadata blocks:*

> ```
> - **Status:** Accepted
> - **Author:** OpenWorm Core Team
> - **Date:** 2026-02-14
> ```

---

## Frequently Asked Questions

**Q: Do I need a DD to fix a typo?**
A: No. Trivial fixes (typos, dead link updates, comment improvements) do not require DDs.

**Q: Do I need a DD to add a new neuron to the connectome?**
A: No, if the neuron is from published connectome data (Cook, Witvliet). The connectome topology is biological ground truth ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)), not an architectural decision. Yes, if you are proposing a novel *modeling approach* for that neuron (e.g., multicompartmental morphology, new channel type).

**Q: Can I modify an accepted DD?**
A: Yes, via amendment. Open a PR modifying the DD, add "Amended YYYY-MM-DD" to the header, go through [DD012](DD012_Design_Document_RFC_Process.md) RFC process. L4 maintainer or founder approves amendments.

**Q: What if my DD is rejected?**
A: The rejection itself is documented (DD status → Rejected, Alternatives Considered explains why). You (and future contributors) now know that approach was considered and why it doesn't serve the mission. This preserves institutional memory.

**Q: How do DDs relate to the Scientific Advisory Board?**
A: DDs with major scientific implications (e.g., choosing what biological detail to model, which validation targets to prioritize) should be reviewed by SAB before final approval. L4 maintainers coordinate SAB review for their subsystem.

**Q: What's the difference between [DD014](DD014_Dynamic_Visualization_Architecture.md), [DD014.1](DD014.1_Visual_Rendering_Specification.md), and [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md)?**
A: [DD014](DD014_Dynamic_Visualization_Architecture.md) is the main visualization architecture (data pipeline, viewer framework, phase roadmap). [DD014.1](DD014.1_Visual_Rendering_Specification.md) (Visual Rendering Specification) is a companion defining appearance (colors, materials, lighting, mockups). [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (Mesh Deformation) is a companion defining how to deform Virtual Worm meshes to follow SPH particles.

**Q: Where are the GitHub issues for DD implementation?**
A: Not yet created. After DDs are approved, `dd_issue_generator.py` ([DD015](DD015_AI_Contributor_Model.md)) will auto-generate GitHub issues from Integration Contract sections.

**Q: Why are so many DDs "Proposed" instead of "Accepted"?**
A: Phase 0 DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-003, [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) are Accepted because they're implemented and working. Phase A-4 DDs are Proposed because they're the roadmap for future work. They'll become Accepted as each phase is implemented and validated.
