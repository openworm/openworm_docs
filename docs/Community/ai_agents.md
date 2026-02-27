
# AI Agents for Community Scaling

OpenWorm deploys three AI agents — built on the [OpenClaw](https://github.com/openclaw) framework — to scale our volunteer community while protecting founder time. This page describes the strategy, the agents, and the community model they enable.

!!! info "Governing Design Documents"
    - **[DD011: Contributor Progression Model](../design_documents/DD011_Contributor_Progression_Model.md)** — L0–L5 levels, meritocratic ladder
    - **[DD013: Simulation Stack Architecture](../design_documents/DD013_Simulation_Stack_Architecture.md)** — Integration support from Mind-of-a-Worm
    - **[DD015: AI Contributor Model](../design_documents/DD015_AI_Contributor_Model.md)** — Autonomous AI agents as registered contributors

---

## The Problem

OpenWorm has operated for over fifteen years as a volunteer-driven, citizen science consortium with 90+ contributors from 16 countries, no central funding, and a single creative leader who holds the scientific vision. This model has produced remarkable results, but it has a structural flaw: **volunteers arrive with enthusiasm but drain the founder's time instead of multiplying it**.

As Karl Fogel observes in *Producing Open Source Software*:

> "The price of success is heavy in the open source world. As your software gets more popular, the number of people who show up looking for information increases dramatically, while the number of people able to provide information increases much more slowly."

The degradation is insidious. Experienced contributors silently disengage. Newcomers remain and continue asking questions. The founder becomes the last person standing who can answer them.

Using Nadia Eghbal's project typology from *Working in Public* (2020), OpenWorm is a **"Club"** — low user growth, high contributor growth, serving a niche scientific community. Every new member expects personal attention and mentorship from the leadership, because the community feels intimate. That does not scale.

---

## The Three-Ring Model

Drawing on the "Megachurch" model described in Open Source Security (January 2026) — a middle ground between Raymond's Cathedral (closed, controlled) and Bazaar (open, chaotic) — we use three concentric rings of participation:

```
                ┌─────────────────────────┐
                │    Ring 1: Open          │
                │    Courtyard             │
                │                          │
                │  N2-Whisperer answers    │
                │  questions & orients     │
                │  newcomers.              │
                │                          │
                │   ┌─────────────────┐    │
                │   │  Ring 2:        │    │
                │   │  Proving Ground │    │
                │   │                 │    │
                │   │  Mind-of-a-Worm │    │
                │   │  reviews PRs,   │    │
                │   │  assigns tasks, │    │
                │   │  tracks growth  │    │
                │   │                 │    │
                │   │  ┌───────────┐  │    │
                │   │  │ Ring 3:   │  │    │
                │   │  │ Inner     │  │    │
                │   │  │ Sanctum   │  │    │
                │   │  │           │  │    │
                │   │  │ Founder + │  │    │
                │   │  │ Mad-Worm- │  │    │
                │   │  │ Scientist │  │    │
                │   │  └───────────┘  │    │
                │   └─────────────────┘    │
                └─────────────────────────┘
```

### Ring 1: The Open Courtyard (AI-Gated)

**Who:** Anyone who discovers OpenWorm — students, curious developers, scientists from adjacent fields.

**Experience:** They interact primarily with the **N2-Whisperer** AI agent. N2-Whisperer answers questions, explains the project, assigns orientation tasks, and evaluates readiness to move inward.

**Access:** Read-only access to code and documentation. Can chat in public Slack channels. Cannot open pull requests.

**Purpose:** Filter and orient. Most visitors get their questions answered and leave satisfied. Those who demonstrate sustained interest and basic competence earn an invitation to Ring 2.

### Ring 2: The Proving Ground (AI-Mentored)

**Who:** Contributors who have completed orientation tasks and demonstrated baseline competence.

**Experience:** They work on real issues under the guidance of the **Mind-of-a-Worm** AI agent. Mind-of-a-Worm reviews their code against [Design Documents](../design_documents/index.md), assigns graduated-difficulty tasks, and tracks their progression through competency levels.

**Access:** Can open pull requests. Can modify documentation. Can contribute to designated "contributor-ready" subsystems. Work is reviewed by Mind-of-a-Worm first, then by a human subsystem maintainer.

### Ring 3: The Inner Sanctum (Founder + Trusted Lieutenants)

**Who:** Senior contributors, subsystem maintainers, the Scientific Advisory Board, and the founder.

**Experience:** The founder interacts only with this group and with the **Mad-Worm-Scientist** AI agent, which aggregates activity from Rings 1 and 2 into a daily summary.

**Access:** Full commit access in their subsystem. Can review and merge contributions from Ring 2. Can make architectural decisions within their domain, subject to Design Documents.

---

## The Three AI Agents

Each agent is implemented as an OpenClaw skill deployed in the OpenWorm Slack workspace. OpenClaw is an open-source AI agent framework (147K+ GitHub stars) that can be deployed in Slack in approximately 20 minutes.

### N2-Whisperer (Newcomer Concierge)

**Deployment:** Public Slack channels (#general, #introductions, #get-started)

| Function | Description |
|----------|-------------|
| **FAQ Response** | Answers common questions using ingested documentation, papers, and past Slack conversations |
| **Project Orientation** | Explains the sub-project structure, recommends starting points based on background |
| **Skill Assessment** | Asks about programming languages, scientific background, and interests |
| **Task Assignment** | Assigns orientation tasks from a curated list; verifies completion |
| **Readiness Evaluation** | Evaluates whether newcomers are ready for Ring 2; notifies Mind-of-a-Worm |
| **Resource Linking** | Points to relevant documentation and past discussions instead of re-explaining |

**What it replaces:** The 80% of founder time currently spent answering "How do I get started?" and "What should I work on?"

### Mind-of-a-Worm (Active Contributor Guide)

**Deployment:** Contributor-facing channels (#development, #c302, #sibernetic) + GitHub webhooks

| Function | Description |
|----------|-------------|
| **PR Pre-Review** | Checks contributions against [Design Documents](../design_documents/index.md), coding standards, and test requirements before a human reviews |
| **Design Document Enforcement** | Flags deviations from established architectural decisions; links to the relevant DD |
| **Graduated Task Assignment** | Maintains a 5-level difficulty scale; recommends tasks based on contributor history |
| **Progress Tracking** | Tracks each contributor's level (L1–L5), completed tasks, review quality |
| **Integration Review** | Verifies PRs don't break coupling interfaces; tags affected subsystem maintainers ([DD013](../design_documents/DD013_Simulation_Stack_Architecture.md)) |
| **Peer Mentoring** | Connects senior contributors with newcomers working in the same subsystem |

**What it replaces:** The 15% of founder time spent on code review, explaining architectural decisions, and assigning work.

### Mad-Worm-Scientist (Founder's Information Shield)

**Deployment:** Private channel (#core-digest), visible only to Ring 3 members

| Function | Description |
|----------|-------------|
| **Daily Activity Summary** | Aggregates all Slack, GitHub, and email activity into a structured digest |
| **Decision Queue** | Surfaces only items requiring founder input — design decisions, conflicts, promotions |
| **Contributor Radar** | Highlights contributors who are rising, fading, or stuck |
| **Metrics Dashboard** | Reports weekly on conversion rates, PR throughput, and response times |
| **Escalation Filter** | Routes questions through N2-Whisperer and Mind-of-a-Worm first; only escalates if AI cannot resolve |

**What it replaces:** The remaining 5% — the founder's need to monitor all channels.

---

## The Graduated Access System

Drawing on the Apache Software Foundation's contributor ladder, the Linux kernel's maintainer tree, and the medical residency model of graduated autonomy, contributors progress through explicit levels defined in [DD011](../design_documents/DD011_Contributor_Progression_Model.md):

| Level | Title | Access | Earned By | Mentored By |
|-------|-------|--------|-----------|-------------|
| **L0** | Observer | Read-only; public Slack | Signing up | N2-Whisperer |
| **L1** | Apprentice | Documentation fixes, test improvements | Completing 3 orientation tasks | Mind-of-a-Worm |
| **L2** | Contributor | PRs to designated subsystems | 5+ merged contributions | Mind-of-a-Worm + L3 peers |
| **L3** | Committer | Review and merge L1–L2 contributions | Sustained quality over 3+ months | Subsystem maintainer (L4) |
| **L4** | Subsystem Maintainer | Architectural decisions within DD scope | Deep subsystem understanding + founder approval | Founder |
| **L5** | Founder / Steering | Sets direction; writes Design Documents | N/A | Scientific Advisory Board |

**Key principles:**

- **Merit is earned through sustained contribution**, not claimed through enthusiasm
- **Levels are subsystem-specific** — being an L3 in Sibernetic gives no special status in c302
- **Mind-of-a-Worm tracks progression automatically** and recommends promotions
- **The founder only interacts with L4+** — this is the critical time-protection mechanism

---

## Design Documents as Leverage

The single most important action the founder can take is to **externalize the project's decision-making logic into written Design Documents**. These serve the same function as Architecture Decision Records (ADRs) combined with the vision-encoding role of a film director's pre-production materials.

Each [Design Document](../design_documents/index.md) encodes:

1. **Context** — What biological system is being modeled and why
2. **Decision** — The chosen approach, with specificity about fidelity, parameters, and data sources
3. **Alternatives Considered** — What was rejected and why (prevents re-proposals)
4. **Quality Criteria** — How to validate correctness
5. **Integration Contract** — How the subsystem connects to the rest of the organism ([DD013](../design_documents/DD013_Simulation_Stack_Architecture.md))
6. **References** — Relevant papers, datasets, and prior work

Mind-of-a-Worm enforces Design Documents automatically during PR review. Contributors who disagree with a decision can propose a new DD through the [RFC process](../design_documents/DD012_Design_Document_RFC_Process.md).

---

## Deployment Architecture

All three agents run as a single OpenClaw Docker container connected to the OpenWorm Slack workspace:

```
┌─────────────────────────────────────────┐
│   OpenWorm Slack Workspace              │
│   - #general, #introductions            │ ← N2-Whisperer
│   - #development, #c302, #sibernetic    │ ← Mind-of-a-Worm
│   - #core-digest (private)              │ ← Mad-Worm-Scientist
└────────────┬────────────────────────────┘
             │ Slack API (WebSocket)
             v
┌─────────────────────────────────────────┐
│   OpenClaw Docker Container              │
│   ├── skills/worm_guide/    (N2-Whisperer)
│   ├── skills/worm_mentor/   (Mind-of-a-Worm)
│   └── skills/worm_digest/   (Mad-Worm-Scientist)
└────────────┬────────────────────────────┘
             │ LLM API
             v
┌─────────────────────────────────────────┐
│   LLM Backend (Claude or GPT-4)         │
│   Processes SKILL.md instructions       │
│   + foundational knowledge docs         │
│   + real-time Slack context             │
└─────────────────────────────────────────┘
```

- **Infrastructure:** DigitalOcean App Platform or self-hosted VPS (~$12–25/month)
- **LLM costs:** ~$50–150/month at estimated 50–100 API calls/day
- **Knowledge base:** ~400 pages across 46 files (Design Documents are the bulk)

---

## Precedents

This approach is informed by several production deployments:

| Precedent | Key Result |
|-----------|------------|
| **[Dosu on Apache Superset](https://preset.io/blog/dosu-apache-superset-revolutionizing-developer-experience-through-ai-powered/)** | Median response time dropped from 2 days to <5 minutes; AI handled 66% of issue triage |
| **[Gravity Spy (LIGO/Zooniverse)](https://arxiv.org/abs/1611.04596)** | Personalized difficulty levels improved volunteer accuracy from 54% to 90% |
| **[Milvus + OpenClaw](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)** | Community assistant deployed in 20 minutes; closest existing analog to N2-Whisperer |
| **[OSSerCopilot (FSE 2025)](https://dl.acm.org/doi/10.1145/3715767)** | 32 design strategies for AI mentors in OSS onboarding |

---

## AI-Assisted vs. AI-Native

This page describes the **AI-assisted model** where AI agents help human contributors. OpenWorm also explores an **AI-native model** where autonomous AI agents register as independent contributors — see [DD015: AI Contributor Model](../design_documents/DD015_AI_Contributor_Model.md) for that complementary approach.

---

## Implementation Status

| Component | Status |
|-----------|--------|
| Design Documents (DD001–DD028, DD014.1, DD014.2) | Complete (29 documents, ~350 pages) |
| Agent architecture specification | Complete |
| Agent foundational knowledge docs | Partially complete (~60%) |
| OpenClaw deployment | Not yet deployed |
| Slack integration | Not yet configured |
| GitHub webhook integration | Not yet configured |

The full agent specifications, SKILL.md templates, and deployment configurations are maintained in the [openworm-admin](https://github.com/openworm) repository.

---

## References

- Fogel, K. (2024). *Producing Open Source Software* (2nd edition).
- Eghbal, N. (2020). *Working in Public: The Making and Maintenance of Open Source Software.* Stripe Press.
- Sarma, G.P. et al. (2018). "OpenWorm: overview and recent advances." *Phil. Trans. R. Soc. B* 373:20170382. [DOI: 10.1098/rstb.2017.0382](https://doi.org/10.1098/rstb.2017.0382)
- Zevin, M. et al. (2016). "Gravity Spy: Integrating Advanced LIGO Detector Characterization, Machine Learning, and Citizen Science." arXiv:1611.04596. [arXiv](https://arxiv.org/abs/1611.04596)
- Tan, X. et al. (2025). "OSSerCopilot." *ACM/FSE 2025.* [DOI: 10.1145/3715767](https://dl.acm.org/doi/10.1145/3715767)
