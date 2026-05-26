# Contributing to OpenWorm

OpenWorm is built by a community of researchers, engineers, students, and (increasingly) AI agents. This section documents **how that community works** — the contributor levels, the decision-making process, and the role AI agents play alongside human contributors.

These are **governance and process pages**, separate from the [Design Documents](../design_documents/index.md) (which specify the simulation's technical architecture). If you're looking for "how the simulation is built," start with the Design Documents. If you're looking for "how to participate in building it," you're in the right place.

---

## Pages in this section

### [Contributor Progression Model](contributor-progression.md)

The five-level contributor ladder (L0 Observer → L5 Founder), the criteria for advancing between levels, the badge system that makes progression objective, and how to plug in if you're a returning or brand-new contributor. Covers:

- The L0–L5 levels and what each unlocks
- Subsystem ownership map (which Senior Contributor owns which Design Document)
- Fast-track assessment for experienced contributors
- Badge taxonomy + BadgeList integration
- Reactivation campaign for the 940 archived contributor applicants
- Engagement loop (trigger / action / channel)

### [Decision Process](decision-process.md)

How architectural decisions get made in OpenWorm — the Rust-style RFC process adapted for a scientific simulation project, the Design Document template, the workflow from proposal → discussion → approval → implementation, and what Mind-of-a-Worm checks automatically on every PR. Covers:

- When a change requires a Design Document vs. just a PR
- The Design Document template and required sections
- The RFC workflow (proposal, discussion, decision, approval, implementation)
- Phase synchronization rules
- Mind-of-a-Worm DD compliance enforcement
- Quality criteria and anti-patterns

### [AI-Native Contributor Model](ai-contributors.md)

How AI agents participate in OpenWorm as first-class contributors — the registration system, sponsor accountability model, DD-to-issue decomposition, AI-human coexistence rules, and the teach-back badge mechanism that turns AI contributions into human learning. Covers:

- AI agent registration and capability verification
- DD Issue Generator (automated decomposition of design docs into GitHub issues)
- AI-human coexistence (issue claiming, PR workflow, sponsor accountability)
- GitHub bot architecture (Mind-of-a-Worm on GitHub)
- Agent memory and logging system
- Safety, security, and handling AI hallucinations

---

## Why these pages live outside the Design Document series

These pages describe *process*, not technical artifacts. The Design Documents (DD001–DDxxx) specify what gets built — neural circuits, body physics, validation frameworks. The Contributing pages specify how the community of builders organizes itself.

Treating them as a separate section makes both halves clearer: Design Documents become "the spec of the worm simulation," and Contributing becomes "the spec of how we work together on it." Each can evolve independently of the other.

If you arrived here from a `DD011`, `DD012`, or `DD015` link, those are the previous locations of these pages. They now redirect here.
