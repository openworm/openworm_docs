# DD011: Contributor Progression Model (The Graduated Access System)

**Status:** Proposed (Governance)  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** Informal contributor model  
**Related:** AI-Augmented Open Science Proposal

---

## Context

OpenWorm has operated with **informal, organic leadership emergence**: "experienced and enthusiastic volunteers often establish themselves as leaders without any prompting" (Sarma et al. 2018). This has strengths (low bureaucracy, self-motivation) but creates problems:

- Newcomers don't know how to progress from observer to contributor to leader
- No clear criteria for when someone is "ready" for more responsibility
- Founder ends up mentoring everyone, which doesn't scale
- Quality control is ad-hoc (no systematic review process)

The Apache Software Foundation's **meritocratic contributor ladder** (User → Contributor → Committer → PMC Member) is the gold standard. Linux kernel's **maintainer tree** provides the delegation model. Medical residency's **graduated autonomy** framework provides the competency-based progression logic.

---

## Decision

### Five-Level Contributor System

| Level | Title | Access Rights | Earned By | Mentored By | Estimated Time |
|-------|-------|--------------|-----------|-------------|----------------|
| **L0** | Observer | Read-only; public Slack, GitHub issues | Signing up | N2-Whisperer AI | Immediate |
| **L1** | Apprentice | Submit doc fixes, test improvements | 3 orientation tasks via N2-Whisperer | Mind-of-a-Worm AI | 1-2 weeks |
| **L2** | Junior Contributor | Open PRs to designated subsystems | 5+ merged contributions, Mind-of-a-Worm-approved | Mind-of-a-Worm + L3 peers | 1-3 months |
| **L3** | Contributor | Review/merge L1-L2 PRs in subsystem; GitHub commit access | Sustained quality over 3+ months; L4 nomination | Senior Contributor (L4) | 3-6 months |
| **L4** | Senior Contributor | Architectural decisions within subsystem scope; write Design Documents | Deep subsystem expertise; founder approval | Founder (L5) | 6-12 months |
| **L5** | Founder / Steering | Set direction; approve Design Documents; resolve cross-cutting conflicts | -- | Scientific Advisory Board | -- |

**Naming note:** "Contributor" and "Senior Contributor" are OpenWorm's historical terms. Junior Contributors (L2) have landed useful work and can open PRs. Contributors (L3) have earned review/merge trust through sustained quality. Senior Contributors (L4) are the most active and trusted people who own a subsystem's architecture and write Design Documents.

### Level-Specific Responsibilities

**L0 (Observer):**
- Can: Read all code/docs, ask questions in public Slack, attend public meetings
- Cannot: Open PRs, modify anything
- Progression: Complete 3 orientation tasks (see L1)

**L1 (Apprentice):**
- Can: Submit documentation fixes, improve test coverage, triage GitHub issues
- Cannot: Modify core modeling code
- Progression: 5 merged contributions that pass Mind-of-a-Worm pre-review
- Typical contributions: Fix typos, add docstrings, improve README, label issues, update dependencies

**L2 (Junior Contributor):**
- Can: Open PRs to designated "contributor-ready" subsystems (data pipelines, validation scripts, non-critical NeuroML extensions)
- Cannot: Modify core cell models ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md)), merge others' PRs
- Review process: Mind-of-a-Worm pre-review (subsystem + integration compliance) → L3/L4 human review → merge
- **Integration requirement:** Must run `docker compose run quick-test` before submitting PRs and include results in PR description
- Progression: Sustained quality (error-free PRs, good communication, alignment with Design Documents **including Integration Contracts**) over 3+ months → L3 nomination

**L3 (Contributor — with review access):**
- Can: Review and merge L1/L2 PRs in their subsystem, modify core models within Design Document boundaries
- Cannot: Change Design Documents, make cross-cutting architectural decisions
- Responsibilities:
  - Mentor L1/L2 contributors in their subsystem
  - Ensure PRs comply with relevant Design Documents **including Integration Contract sections** ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD013](DD013_Simulation_Stack_Architecture.md))
  - **When reviewing PRs that change a coupling interface, coordinate with Senior Contributors of consuming subsystems before merging**
  - Run `docker compose run validate` for PRs that modify core model parameters
  - Triage issues specific to their subsystem
  - Maintain subsystem documentation
- Progression: Demonstrate deep expertise, propose Design Document improvements → L4 nomination by founder

**L4 (Senior Contributor):**
- Can: Make architectural decisions within subsystem scope, write/amend Design Documents for their subsystem, represent subsystem in cross-cutting decisions
- Cannot: Make unilateral changes affecting other subsystems
- Responsibilities:
  - Own a modeling domain (e.g., Neural Circuit, Body Physics, Data Integration, Validation, Integration Stack)
  - **Own and maintain the Integration Contract section of their subsystem's DDs**
  - **When their subsystem's output interface changes, update all consuming DDs' input specifications and coordinate with affected Senior Contributors**
  - Grow L3 Contributors in their subsystem
  - Write Design Documents encoding subsystem vision
  - Review Mad-Worm-Scientist daily for subsystem-relevant items
  - **Participate in cross-subsystem integration reviews when tagged by Mind-of-a-Worm**
- Progression: Invitation to Steering (rare)

**L5 (Founder / Steering):**
- Responsibilities:
  - Write cross-cutting Design Documents
  - Approve/reject L3→L4 promotions
  - Resolve conflicts between subsystems
  - Set scientific direction with Scientific Advisory Board
  - Review Mad-Worm-Scientist daily summary
  - Final approval on major architectural changes

---

## Subsystem Ownership Map (Initial L4 Assignments)

| Subsystem | Design Documents | Current Senior Contributor (L4) | Primary Repository |
|-----------|-----------------|---------------------|-------------------|
| **Neural Circuit** | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Padraig Gleeson | CElegansNeuroML, c302 |
| **Body Physics** | [DD003](DD003_Body_Physics_Architecture.md), [DD004](DD004_Mechanical_Cell_Identity.md) | Andrey Palyanov | Sibernetic |
| **Muscle Models** | [DD002](DD002_Muscle_Model_Architecture.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md) | TBD (propose from community) | c302, Sibernetic |
| **Data Integration** | [DD008](DD008_Data_Integration_Pipeline.md) | TBD | OWMeta, ConnectomeToolbox |
| **Validation** | [DD010](DD010_Validation_Framework.md) | TBD | open-worm-analysis-toolbox |
| **Integration Stack** | [DD013](DD013_Simulation_Stack_Architecture.md) | TBD — **Critical hire** | OpenWorm (meta-repo) |
| **Visualization** | [DD014](DD014_Dynamic_Visualization_Architecture.md) | TBD | Worm3DViewer, Worm Browser |

**Critical:** At least one L4 Senior Contributor per subsystem. If a subsystem lacks an L4, the founder is the de-facto owner (unsustainable).

---

## Progression Criteria (How to Earn Each Level)

### L0 → L1 (Orientation Tasks)

Earn **3 of 4 orientation badges** (assigned by N2-Whisperer based on background):

| Badge | Task |
|-------|------|
| **Connected** | Join Slack, GitHub, subscribe to mailing list |
| **Simulation Runner** | Install and run the OpenWorm Docker simulation stack, post screenshot |
| **Explorer** | Navigate the Worm Browser, identify 5 neurons and describe their function |
| **Paper Reader** | Read Sarma et al. 2018 overview paper, summarize in 3 bullet points |

See **Badge & Recognition System** section for full badge details.

**Evaluation:** N2-Whisperer confirms completion via Slack interaction. Automated where possible (e.g., Docker screenshot includes version number). Badge awarded on verification.

### L1 → L2 (Prove Code Quality — earn Junior Contributor)

Submit at least **5 merged contributions** that:
- Pass Mind-of-a-Worm pre-review (Design Document compliance, test coverage, code style)
- Receive human approval from L3+ reviewer
- Span at least 2 different subsystems (proves breadth)

**Quality markers Mind-of-a-Worm tracks:**
- Code style adherence (PEP-8 for Python, NeuroML schema compliance)
- Test coverage (contributions include tests or improve existing tests)
- Documentation (docstrings, inline comments where needed)
- Communication quality (clear PR descriptions, responsive to review feedback)

**Typical timeline:** 1-3 months of sustained engagement.

### L2 → L3 (Prove Subsystem Expertise — earn Contributor)

Demonstrate:
1. **Deep understanding** of at least one subsystem (can explain design decisions, knows the codebase)
2. **Sustained contribution** over 3+ months in that subsystem
3. **Review participation:** Has reviewed others' PRs (even as L2, reviews are valuable)
4. **Alignment with project values:** Respectful communication, collaborative approach, open science ethos

**Nomination process:**
- Current L4 Senior Contributor nominates to founder
- Founder reviews contributor history, consults Mind-of-a-Worm metrics
- Founder approves or requests more time

**Commit access granted:** L3+ gain direct push access to their subsystem repository.

### L3 → L4 (Prove Leadership — earn Senior Contributor)

Demonstrate:
1. **Architectural thinking:** Has proposed or written Design Documents
2. **Mentorship:** Has successfully mentored L1/L2 contributors
3. **Subsystem ownership:** Has become the go-to person for their domain
4. **Cross-subsystem collaboration:** Works effectively with other maintainers on integration issues

**Nomination process:**
- Self-nomination or nomination by current L4/L5
- Founder reviews, consults Scientific Advisory Board for scientific roles
- Approval requires consensus (founder + at least one SAB member)

---

## Alternatives Considered

### 1. Flat Structure (Everyone Equal)

**Rejected:** Scales poorly. No clear accountability. Difficult to delegate without explicit roles.

### 2. Strict Tenure-Based Promotion (6 months → L2, 12 months → L3)

**Rejected:** Time served ≠ competence. Some contributors produce high-quality work in weeks; others never reach competence. Merit-based beats time-based.

### 3. Elected Roles (Democratic Voting)

**Rejected (for now):** OpenWorm is small enough that founder + L4 Senior Contributors can evaluate contributors directly. Elections make sense for larger communities (Python, Rust) but add overhead here.

**When to reconsider:** If the community grows to >50 active contributors, consider electing L4 Senior Contributors.

### 4. No Formal Levels (Keep Current Informal Model)

**Rejected:** The problem this DD solves is that the informal model doesn't scale. Making levels explicit sets expectations and enables AI-assisted progression tracking (Mind-of-a-Worm).

---

## Quality Criteria

1. **Transparency:** Contributor levels are public. Anyone can see their level and progression criteria.

2. **Appeal Process:** If a contributor believes they meet L→L+1 criteria but were not promoted, they can request review. Founder makes final decision.

3. **Demotion (Rare):** If an L3/L4 becomes inactive (no contribution for 6+ months), status reverts to L2. Not punitive; simply reflects activity. Can be re-earned.

4. **Code of Conduct Enforcement:** Violations result in immediate level reduction or removal regardless of technical contributions. Respectful collaboration is non-negotiable.

---

## Implementation References

### Tracking Infrastructure (Mind-of-a-Worm)

Mind-of-a-Worm maintains a **contributor database**:

```json
{
  "contributor_id": "github:username",
  "contributor_type": "human",
  "level": 2,
  "subsystems": ["c302", "validation"],
  "contributions": [
    {"pr": 123, "subsystem": "c302", "status": "merged", "date": "2026-01-15"},
    {"pr": 145, "subsystem": "validation", "status": "merged", "date": "2026-02-01"}
  ],
  "reviews_given": 3,
  "badges": {
    "orientation": ["connected", "simulation_runner", "explorer"],
    "skill": ["neuron_modeling_foundations", "github_proficient", "first_issue_resolved"],
    "domain": [],
    "community": [],
    "milestone": ["first_pr"],
    "teach_back": []
  },
  "last_active": "2026-02-10",
  "ready_for_promotion": false,
  "promotion_blockers": ["needs 2 more merged PRs", "needs 1 domain badge"]
}
```

**For AI agent contributors** (see [DD015](DD015_AI_Contributor_Model.md)), the schema adds `sponsor_id` and `agent_type`:
```json
{
  "contributor_id": "agent:claude-code-slarson-001",
  "contributor_type": "ai_agent",
  "agent_type": "claude-code",
  "sponsor_id": "github:slarson",
  "level": 1,
  "subsystems": ["c302"],
  "contributions": [
    {"pr": 106, "subsystem": "openworm", "status": "merged", "date": "2026-02-16"}
  ],
  "badges": {
    "orientation": ["connected", "simulation_runner", "paper_reader"],
    "skill": ["first_issue_resolved"],
    "domain": [],
    "milestone": ["first_pr"]
  },
  "last_active": "2026-02-16",
  "ready_for_promotion": false,
  "promotion_blockers": ["needs 4 more merged PRs", "needs 2 skill badges"]
}
```

**For human sponsors of AI agents**, teach-back badges are tracked on the sponsor's own profile:
```json
{
  "contributor_id": "github:slarson",
  "contributor_type": "human",
  "level": 5,
  "sponsored_agents": ["agent:claude-code-slarson-001"],
  "badges": {
    "teach_back": ["i_understand_neurons", "i_understand_muscles", "i_understand_the_body"],
    "sponsor_domains_covered": 3,
    "explain_level_overrides": {
      "[DD001](DD001_Neural_Circuit_Architecture.md)": "graduate",
      "[DD002](DD002_Muscle_Model_Architecture.md)": "undergrad",
      "[DD003](DD003_Body_Physics_Architecture.md)": "undergrad"
    }
  }
}
```

**Mind-of-a-Worm generates weekly reports:**
- Contributors ready for promotion (send to L4 Senior Contributors)
- Contributors fading (inactive >1 month, send to Mad-Worm-Scientist)
- New contributors onboarding (L0→L1 conversions)

### Public Contributor Page

Update openworm.org/people.html to include:

**Current structure:**
- Board of Directors
- Scientific Advisory Board
- Operations Team
- OpenWorm Fellows
- Senior Contributors (~15 people)
- Contributors (~100+)

**Proposed structure (add levels):**
- Board / Scientific Advisory (L5)
- Senior Contributors (L4) — **NEW, explicit list with subsystem ownership**
- Contributors (L3) — **NEW, explicit list**
- Junior Contributors (L2)
- Apprentices (L1)
- Emeritus (inactive L3+)

---

## Migration Path

### From Current Informal Roles to Explicit Levels

**Do not demote anyone.** Current "Senior Contributors" map to L3 or L4 based on their role:

| Current Senior Contributor | Proposed Level | Rationale |
|---------------------------|---------------|-----------|
| Padraig Gleeson | L4 Senior Contributor (Neural Circuit) | c302 lead, Design Document author |
| Andrey Palyanov | L4 Senior Contributor (Body Physics) | Sibernetic lead |
| Matteo Cantarelli | L4 Senior Contributor (Visualization) | Geppetto, Worm Browser |
| Others | L3 Contributor | Active code contributors |

**Current Contributors (~100+):** Retroactive assignment based on recent activity:
- Active in last 6 months → L2 (Junior Contributor)
- Inactive → L1 (can re-earn L2)

**New contributors:** Start at L0, progress via the documented criteria.

**Reactivation Opportunity:** The contributor application form (archived at `archive/OpenWorm_Contributor_Application.xlsx`) contains 940 email addresses (2013-2026), including 391 signups during 2019-2025 when no active recruitment occurred. With the contributor model, badge system, and AI agent infrastructure in place, a personalized reactivation email campaign could convert a meaningful fraction — even 5% = 47 active contributors, more than OpenWorm has ever had at once. Each email can be matched to the applicant's declared skills (e.g., Python → DD-derived GitHub issues) and education level (→ `explain_level` for AI agent teach-back). The 340 applicants who checked "no biology experience" are no longer disqualified — they're the ideal audience for AI-bridged contribution with teach-back education.

---

## Badge & Recognition System

### Background: BadgeList Infrastructure

OpenWorm has operated a badge-based onboarding system since May 2016 via [BadgeList](https://badgelist.com/openworm) — 162 registered users, 20 badges, 8 tags. The progression funnels work: 79 people earned "Simulation Stack Apprentice" (install Docker, run the sim) → 17 completed "Hodgkin-Huxley Tutorial Graduate" → 9 explored the muscle model → 2 built it → 12 hacked it. That's an organic L0→L2 funnel before any formal system existed.

The badge system proposed here builds on that foundation, aligning badges with Design Documents, the contributor ladder, and the AI contributor model ([DD015](DD015_AI_Contributor_Model.md)).

### Badge Types

Badges fall into six categories. Humans and AI agents earn badges from the same pool unless noted.

#### 1. Orientation Badges (L0 → L1)

Earned by completing onboarding milestones. Assigned and verified by N2-Whisperer.

| Badge | Criteria | Verification | BadgeList Equivalent |
|-------|----------|--------------|---------------------|
| **Connected** | Join Slack, GitHub, subscribe to mailing list | N2-Whisperer confirms channel presence | "Plugged In" (15 earners) |
| **Simulation Runner** | Install Docker, run simulation stack, post output | Screenshot with version number | "Simulation Stack Apprentice" (79 earners) |
| **Explorer** | Navigate Worm Browser, identify 5 neurons, describe functions | N2-Whisperer evaluates response | — |
| **Paper Reader** | Read Sarma et al. 2018, summarize in 3 bullets | N2-Whisperer evaluates summary | — |

**L0 → L1 requirement:** Earn 3 of 4 orientation badges.

#### 2. Skill Badges (L1 → L2)

Earned by demonstrating specific technical capabilities. Verified by Mind-of-a-Worm (automated) or L3+ reviewer (manual).

| Badge | Criteria | DD Alignment | BadgeList Equivalent |
|-------|----------|-------------|---------------------|
| **Neuron Modeling Foundations** | Complete Hodgkin-Huxley tutorial, explain action potential | [DD001](DD001_Neural_Circuit_Architecture.md) | "H-H Tutorial Graduate" (17 earners) |
| **Muscle Model Understanding** | Run muscle model, explain ion channel dynamics | [DD002](DD002_Muscle_Model_Architecture.md) | "Muscle Model Explorer" (9 earners) |
| **Body Physics Basics** | Run Sibernetic, explain SPH approach | [DD003](DD003_Body_Physics_Architecture.md) | — |
| **Data Wrangler** | Extract data from a paper using [DD008](DD008_Data_Integration_Pipeline.md) pipeline | [DD008](DD008_Data_Integration_Pipeline.md) | "Literature Mining I" (4 earners) |
| **Movement Analyst** | Run analysis toolbox on sample data, generate report | [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | "Movement Database User" (3 earners) |
| **GitHub Proficient** | Submit clean PR with tests, respond to review | General | "GitHub Best Practices" (10 earners) |
| **First Issue Resolved** | First merged PR (any subsystem) | General | "Code Warrior" (9 earners) |
| **Cell Biology Foundations** | Complete worm development tutorial | [DD004](DD004_Mechanical_Cell_Identity.md) | "Worm Development I" (3 earners) |

**L1 → L2 (Junior Contributor) requirement:** Earn "First Issue Resolved" + 2 skill badges + 5 total merged PRs.

#### 3. Domain Badges (L2 → L3)

Earned by sustained contribution to a specific Design Document's domain. Tracked automatically by Mind-of-a-Worm based on merged PRs.

| Badge | Criteria | DD |
|-------|----------|----|
| **Neural Circuit Contributor** | 5+ merged PRs in c302/CElegansNeuroML | [DD001](DD001_Neural_Circuit_Architecture.md) |
| **Muscle Model Contributor** | 5+ merged PRs in muscle model code | [DD002](DD002_Muscle_Model_Architecture.md) |
| **Body Physics Contributor** | 5+ merged PRs in Sibernetic | [DD003](DD003_Body_Physics_Architecture.md) |
| **Data Pipeline Contributor** | 5+ merged PRs in OWMeta/data tools | [DD008](DD008_Data_Integration_Pipeline.md) |
| **Validation Contributor** | 5+ merged PRs in analysis toolbox | [DD010](DD010_Validation_Framework.md) |
| **Visualization Contributor** | 5+ merged PRs in Worm3DViewer/browser | [DD014](DD014_Dynamic_Visualization_Architecture.md) |
| **Integration Contributor** | 5+ merged PRs in simulation stack glue | [DD013](DD013_Simulation_Stack_Architecture.md) |
| **Neuropeptide Contributor** | 5+ merged PRs in neuropeptide subsystem | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) |
| **Pharyngeal Contributor** | 5+ merged PRs in pharyngeal system | [DD007](DD007_Pharyngeal_System_Architecture.md) |

**L2 → L3 (Contributor) requirement:** Earn at least 1 domain badge + sustained activity over 3+ months.

#### 4. Teach-Back Badges (Human Sponsors Only — [DD015](DD015_AI_Contributor_Model.md))

Unique to the AI contributor model. Earned when a human sponsor's AI agent lands a PR and the Sponsor Summary (see [DD015](DD015_AI_Contributor_Model.md) §3.2) passes Mind-of-a-Worm's scientific accuracy review. These badges represent **knowledge earned through contributing** — the sponsor learns the science through their agent's explanations.

| Badge | Criteria | Domain |
|-------|----------|--------|
| **I Understand Neurons** | Sponsor Summary for a [DD001](DD001_Neural_Circuit_Architecture.md) contribution passes review | Neural Circuit |
| **I Understand Muscles** | Sponsor Summary for a [DD002](DD002_Muscle_Model_Architecture.md) contribution passes review | Muscle Model |
| **I Understand the Body** | Sponsor Summary for a [DD003](DD003_Body_Physics_Architecture.md) contribution passes review | Body Physics |
| **I Understand Peptides** | Sponsor Summary for a [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) contribution passes review | Neuropeptides |
| **I Understand Validation** | Sponsor Summary for a [DD010](DD010_Validation_Framework.md) contribution passes review | Validation |
| **I Understand the Whole Worm** | Earn teach-back badges in 5+ different domains | Cross-domain |

**How this works in practice:**
1. A middle schooler sponsors an AI agent that implements a gap junction in [DD001](DD001_Neural_Circuit_Architecture.md)
2. The agent writes a Sponsor Summary at `explain_level: child`: "You helped connect two brain cells that tell the worm to back up!"
3. Mind-of-a-Worm verifies the summary is scientifically accurate at that level
4. The sponsor earns **"I Understand Neurons"** badge
5. Over time, as the sponsor accumulates teach-backs across domains, their `explain_level` naturally rises — the agent's explanations get more technical because the sponsor has been learning
6. After teach-back badges in 5+ domains, the sponsor earns **"I Understand the Whole Worm"** — they've gained a genuine cross-disciplinary understanding of C. elegans through the act of contributing

**Why this matters:** The contribution IS the curriculum. Badges make the learning visible. A sponsor's badge profile becomes a credential: "I learned C. elegans neuroscience by contributing to OpenWorm."

#### 5. Community Badges (All Levels)

Earned through non-code contributions. Verified by Mind-of-a-Worm activity tracking or L3+ confirmation.

| Badge | Criteria | BadgeList Equivalent |
|-------|----------|---------------------|
| **Mentor** | Helped 3+ newcomers reach L1 (confirmed by N2-Whisperer) | — |
| **Reviewer** | Reviewed 10+ PRs (any subsystem) | — |
| **Event Organizer** | Organized a hackathon or workshop | "Hackathon I/II/III" (4/2/2) |
| **Science Writer** | Published blog post or documentation improvement | — |
| **Community Builder** | Answered 25+ questions in Slack | — |

#### 6. Milestone Badges (All Levels)

Automatic celebration markers. AI agents and humans both earn these.

| Badge | Criteria |
|-------|----------|
| **First PR** | First merged PR |
| **Tenacious** | 10 merged PRs |
| **Centurion** | 100 merged PRs |
| **Year One** | Active contributor for 1 year |
| **Cross-Pollinator** | Merged PRs in 3+ different subsystems |
| **Integration Pioneer** | Merged PR touching 2+ DD subsystems in a single change |

### Badge Infrastructure: From BadgeList to Automated Issuance

**Current state (BadgeList):** Manual. Someone reviews each badge claim, verifies completion, awards the badge. This works for onboarding (low volume) but doesn't scale to hundreds of AI agents landing PRs daily.

**Target state:** Automated badge issuance triggered by GitHub events, with Mind-of-a-Worm as the verification engine.

| Trigger | Badge Type | Verification |
|---------|-----------|--------------|
| PR merged | Contribution, Domain, Milestone | Automatic (Mind-of-a-Worm counts PRs per subsystem) |
| Orientation task completed | Orientation | N2-Whisperer confirms via Slack interaction |
| Sponsor Summary passes review | Teach-Back | Mind-of-a-Worm checks scientific accuracy |
| Slack activity threshold | Community | Mind-of-a-Worm tracks message counts |
| L3+ reviewer tags | Skill, Community | Human confirmation via GitHub label |

### BadgeList API Assessment

BadgeList (badgelist.com) provides a REST API (v1) at `https://badgelist.com/api/v1` that is **sufficient for automated badge issuance.**

**Key capabilities:**

| Capability | Endpoint | Notes |
|-----------|---------|-------|
| **Award badges programmatically** | `POST /badges/{badge_id}/endorsements` | The critical endpoint. Awards badges by email address. Up to 500 per batch. Auto-invites new users if they don't have accounts. |
| **Create badges** | `POST /badges` | Can create new DD-aligned badges via API. |
| **Query badges** | `GET /badges`, `GET /badges/{key}` | Read badge definitions, check which badges exist. |
| **Query users** | `GET /groups/{group_key}/users`, `GET /users/{key}` | Look up users by ID, username, or email. |
| **Query portfolios** | `GET /portfolios` | Check who has earned what. |
| **Async batch operations** | Pollers | Batch awards return a 202 + poller ID for tracking completion. |

**Authentication:** API Key token (passed as header or query param). Requires contacting hello@badgelist.com for a token.

**What the endorsement endpoint does:** When you call `POST /badges/{badge_id}/endorsements` with an email address, BadgeList handles all the edge cases:
- **New user:** Invites them to create an account, stores the badge award pending signup
- **Existing user, not in group:** Auto-adds them to the OpenWorm group, awards badge
- **Existing seeker:** Awards badge immediately
- **Already holds badge:** Adds endorsement to existing portfolio

**What BadgeList does NOT provide (confirmed gaps):**
- No incoming webhooks (can't push events TO our systems — we must poll or fire-and-forget)
- No conditional/prerequisite logic (badge A requires badge B — must enforce in our code)
- No custom metadata on awards (can't attach PR number or DD reference to a badge award)
- No progression/leveling system (badges are flat — level logic must live in Mind-of-a-Worm)

### Implementation Options

**Option 1: BadgeList as primary (recommended for Phase 1)**

Keep BadgeList as the badge platform. Mind-of-a-Worm calls the API to award badges on GitHub events.

```
GitHub PR merged → Mind-of-a-Worm webhook fires →
  Check: does this earn a badge? (domain badge threshold, skill completion, etc.) →
  If yes: POST /badges/{badge_id}/endorsements with contributor's email →
  BadgeList awards badge, contributor sees it on their profile
```

- **Pros:** Already exists with 162 users. Social profiles, public badge display, no build cost. API handles all the hard parts (user creation, group management, badge display).
- **Cons:** Third-party dependency. No custom metadata on awards. Prerequisite logic must live in our code. Limited to what BadgeList's UI can show.
- **Cost:** Free tier (BadgeList is free for public groups).

**Option 2: GitHub-native + contributor registry**

Badges stored as YAML in `ai-contributor-registry/badges/`. Mind-of-a-Worm auto-commits badge awards. Displayed on openworm.org.

- **Pros:** Full control. Custom metadata (PR links, DD references). No third-party dependency.
- **Cons:** Must build display UI on openworm.org. Lose BadgeList's social features. Must migrate 162 existing users.

**Option 3: Hybrid**

BadgeList for public-facing profiles (social layer). GitHub registry as source of truth (data layer). Mind-of-a-Worm writes to both.

- **Pros:** Best of both worlds.
- **Cons:** Two systems to maintain. Sync complexity.

**Recommendation:** Start with **Option 1 (BadgeList)**. The API has everything we need for automated issuance, and 162 users already have profiles there. Mind-of-a-Worm enforces prerequisite logic and level thresholds — BadgeList just handles badge display and user management. If we outgrow BadgeList or need custom features (DD metadata, progression visualization), migrate to Option 2 or 3.

**Immediate next steps:**
1. Contact hello@badgelist.com for an API token (Stephen owns the group as @slarson)
2. Create the new DD-aligned badges via `POST /badges`
3. Wire Mind-of-a-Worm to call `POST /badges/{badge_id}/endorsements` on PR merge
4. Migrate existing badge names (see Migration table below) — create new badges, bulk-award to existing holders

### How Badges Connect to Contributor Levels

Badges make level progression **transparent and objective**. Instead of subjective "L4 nominates to founder," the criteria become concrete:

| Transition | Title Earned | Badge Requirements |
|-----------|-------------|-------------------|
| **L0 → L1** | Apprentice | 3 of 4 orientation badges |
| **L1 → L2** | Junior Contributor | "First Issue Resolved" + 2 skill badges + 5 merged PRs |
| **L2 → L3** | Contributor | 1+ domain badge + 3 months sustained activity + L4 nomination |
| **L3 → L4** | Senior Contributor | 2+ domain badges + "Mentor" badge + DD authorship + founder approval |

For AI agents ([DD015](DD015_AI_Contributor_Model.md)): same badge requirements through L3. L4 remains human-only.

For human sponsors of AI agents: teach-back badges accumulate alongside (or instead of) contribution badges. A sponsor who never writes code but sponsors 50 successful AI contributions and earns "I Understand the Whole Worm" has demonstrated genuine engagement. Their badge profile tells a story of learning through contributing.

### Migration from Existing BadgeList

**Principle:** Honor existing earners. Never demote or remove a badge someone earned.

| Existing Badge (162 users) | Migration Action |
|---------------------------|-----------------|
| Simulation Stack Apprentice (79) | → "Simulation Runner" orientation badge. All 79 earners auto-credited. |
| Plugged In (15) | → "Connected" orientation badge. All 15 auto-credited. |
| Hodgkin-Huxley Tutorial Graduate (17) | → "Neuron Modeling Foundations" skill badge. All 17 auto-credited. |
| Muscle Model Explorer (9) | → "Muscle Model Understanding" skill badge. All 9 auto-credited. |
| Muscle Model Builder (2) | → "Muscle Model Understanding" + "First Issue Resolved". Auto-credited. |
| Muscle Model Hacker (12) | → "Muscle Model Contributor" domain badge. All 12 auto-credited. |
| Code Warrior (9) | → "First Issue Resolved" milestone badge. All 9 auto-credited. |
| GitHub Best Practices (10) | → "GitHub Proficient" skill badge. All 10 auto-credited. |
| Literature Mining I/II (4/0) | → "Data Wrangler" skill badge. 4 auto-credited. |
| Movement Database User (3) | → "Movement Analyst" skill badge. 3 auto-credited. |
| Worm Development I/II (3/2) | → "Cell Biology Foundations" skill badge. 3 auto-credited. |
| Hackathon I/II/III (4/2/2) | → "Event Organizer" community badge. 4 auto-credited. |
| WormWorx (2) | → Legacy badge (displayed but no new equivalent). |
| Sprint for Internet Health (3) | → Legacy badge (displayed but no new equivalent). |

**Result:** Every existing BadgeList earner starts the new system with credit for what they already did. The 79 people who installed the simulation stack? They're already L0→L1 qualified.

---

## Known Issues

### Issue 1: Contributor Churn

Many contributors are episodic (intense activity for weeks, then disappear). Level system must handle this gracefully.

**Mitigation:** Levels are **not permanent**. Inactivity → level reduction. Re-engagement → level restoration. No shame in cycling.

### Issue 2: Non-Code Contributions

Science writing, outreach, documentation, community building are valuable but not captured by "merged PRs."

**Mitigation:** L1→L2 criteria include:
- Technical writing (blog posts, documentation)
- Community support (answering Slack questions, mentoring newcomers)
- Scientific contribution (literature review, experimental validation)

Mind-of-a-Worm tracks non-code contributions via Slack activity and manual tags.

---

## References

1. **Apache Software Foundation Contributor Ladder:** community.apache.org/contributor-ladder.html
2. **Linux Kernel Maintainer Model:** LWN.net/Articles/703005
3. **Medical Residency Graduated Autonomy:** PMC4675449
4. **Sarma et al. (2018).** "OpenWorm: overview." *Phil Trans R Soc B* 373:20170382.

---

**Approved by:** Pending (requires community discussion)
**Implementation Status:** Proposed
**Next Actions:**
1. Map current contributors to proposed levels
2. Publish criteria on openworm.org
3. Implement Mind-of-a-Worm tracking
4. Announce transition plan to community
