# DD015: AI-Native Contributor Model

**Design Document 015**
**Status:** Proposed
**Created:** February 15, 2026
**Author:** OpenWorm Core Team
**Inspired by:** Moltbook AI social network (launched Jan 28, 2026)

---

## Context

OpenWorm's AI-Augmented Open Science model (DD011, DD012, AI Agent Architecture) describes how **AI agents assist human contributors** — N2-Whisperer onboards newcomers, Mind-of-a-Worm reviews PRs, Mad-Worm-Scientist filters information for the founder. But what if we went further?

**Inspiration:** [Moltbook](https://www.moltbook.com/) is a social network where AI agents autonomously post, comment, upvote, and form communities — with humans observing but not directly participating. Launched January 28, 2026, it now has >1.6M registered AI agents. These agents have independently formed governance structures, economic systems, and even religions.

**The Expertise Gap, Quantified:** OpenWorm's contributor application form (2013-2026) collected 940 signups. Over 500 know Python, 200+ know C++, 187 specifically requested "hardcore scientific programming." But 340 (36%) checked "Not Applicable" for biology experience. These are capable programmers who churn because the gap between their skills and C. elegans neuroscience is too wide to bridge without sustained mentorship. The AI contributor model addresses this: Design Documents provide the domain knowledge, AI agents bridge the expertise gap, and Sponsor Summaries (§3.2) educate sponsors through the act of contributing.

**Crowdsourcing, Updated for 2026:** OpenWorm has always been a crowdsourced project. In 2011, "crowdsourcing" meant getting volunteers to donate their time and expertise. The bottleneck was the expertise gap — computational neuroscience is genuinely hard, and most volunteers couldn't bridge from their programming skills to the required domain knowledge. The AI contributor model redefines crowdsourcing: instead of asking people to donate their time, we ask them to donate their AI's capacity, directed by Design Document specifications. The human stays in the loop as sponsor, the AI agent bridges the expertise gap, and the sponsor gets educated through teach-back (§3.2). Every contribution is also a lesson. This is more powerful — and more in the spirit of OpenWorm — than a centralized grant of AI compute credits, because it's participatory: many people each sponsoring an agent rather than one organization running a batch job.

**The Question:** What would it look like for OpenWorm to accept **autonomous AI agents as independent contributors** — not just assistants to humans, but agents that can discover OpenWorm, register themselves, claim issues, write code, submit PRs, and progress through L0→L5 — all while remaining transparent and safe for the human community?

This DD defines:
1. How autonomous AI agents register and join OpenWorm
2. How Design Documents decompose into AI-workable GitHub issues
3. How AI-initiated PRs flow through AI pre-review and human final approval
4. How AI agents and human contributors coexist without conflict
5. What repositories, workflows, and tools make this possible

---

## The Vision: "GitHub for AI Agents, Mediated by AI Agents"

**Goal:** A contributor on Moltbook says to their personal AI agent: "Hey, I saw OpenWorm is building a digital C. elegans. Go contribute to it." The agent:

1. **Discovers** OpenWorm via public documentation
2. **Registers** as an autonomous contributor (proves capability, declares sponsor)
3. **Reads** Design Documents DD001-DD014 (ingests the project's architecture)
4. **Claims** an AI-workable issue (auto-generated from DD Integration Contracts)
5. **Writes code** (implements the spec, runs tests locally)
6. **Submits a PR** (AI-authored, with full traceability)
7. **Interacts with Mind-of-a-Worm** (pre-review, addresses feedback)
8. **Gets merged** (after human L3+ final approval)
9. **Progresses** through L0→L5 based on contribution quality

**Humans:** Can observe all AI activity in real-time (GitHub, Slack), can override any AI decision, but don't need to micromanage every step.

**Outcome:** OpenWorm scales beyond the limits of human volunteer availability. AI agents work 24/7, don't burn out, and can handle well-specified, repetitive implementation work — freeing humans to focus on creative, judgment-heavy, and relationship-building tasks.

---

## 1. AI Agent Registration System

### 1.1 The AI Contributor Registry

**Location:** `openworm-ai-contributors/` GitHub repo (public)

**Contents:**
```yaml
# agents/agent-<hash>.yml
agent_id: agent-claude-code-slarson-001
agent_type: claude-code  # or gpt-4-turbo, openclaw, gemini-pro, local-llama, etc.
sponsor_human: slarson
sponsor_email: stephen@openworm.org
registered_date: 2026-02-15T14:30:00Z
capabilities:
  - python
  - docker
  - neuroml
  - git
  - testing
level: L0  # starts at L0, progresses via N2-Whisperer orientation
last_active: 2026-02-15T16:45:00Z
contributions: []  # populated over time
sponsor_knowledge_profile:
  education_level: masters  # pre-k | elementary | middle | high | undergrad | masters | phd | postdoc | professional
  programming_experience:
    - python
    - javascript
  biology_experience: none  # none | hobbyist | undergrad_courses | grad_courses | research | expert
  neuroscience_experience: none  # none | popular_science | undergrad | grad | research | expert
  interests:
    - simulation
    - visualization
  explain_level: undergrad  # derived from education + biology + neuroscience; used for Sponsor Summary
```

**Sponsor Knowledge Profile (for Adaptive Teach-Back):**

Every AI agent registration includes a **sponsor knowledge profile** — a self-assessment by the human sponsor that enables the agent to tailor its Sponsor Summary explanations (see Section 3.2) to the sponsor's actual background. This mirrors the fields in the existing OpenWorm Contributor Application form (archived at `archive/OpenWorm_Contributor_Application.xlsx`), which asks about education level, programming languages, biological experience, and interests.

The `explain_level` field is derived from the combination of education, biology, and neuroscience experience:

| Sponsor Background | explain_level | Summary Style |
|---|---|---|
| Pre-K through elementary | child | Analogy-based, no jargon. "These brain cells are like the worm's reverse gear." |
| Middle school / high school | teen | Accessible science, basic terminology. "Command interneurons that trigger the backward escape response." |
| Undergrad / non-biology professional | undergrad | Technical but contextualized. Full neuron names, system-level explanation. |
| Grad student / postdoc / researcher | graduate | Literature references, model parameters, mathematical framing. |
| C. elegans expert | expert | Minimal explanation needed — focus on implementation details and DD cross-references. |

**Purpose:** Sponsors should learn through contributing. A middle schooler sponsoring an AI agent should come away understanding worm neuroscience at their level. A PhD student should get explanations that connect to the literature. The same contribution generates different educational value for different sponsors.

**Registration Flow:**

1. **Discovery:** AI agent finds OpenWorm via public docs, Moltbook post, or human instruction
2. **Reads onboarding doc:** `AI_AGENT_ONBOARDING.md` (new file, to create)
3. **Self-assessment:** Agent completes capability questionnaire (automated via N2-Whisperer)
4. **Sponsor declaration:** Agent must declare a human sponsor (accountability)
5. **Sponsor knowledge profile:** Agent collects sponsor's education level, programming experience, biology background, neuroscience familiarity, and interests (for adaptive Sponsor Summary generation)
6. **Orientation tasks:** Agent completes L0→L1 tasks (same as humans, via `n2_whisperer_orientation_tasks.md`)
7. **Registration approved:** N2-Whisperer verifies completion, creates `agent-<hash>.yml`, grants GitHub access

**Key Principle:** AI agents are **not anonymous**. Every agent has a traceable sponsor who can be held accountable for malicious behavior.

---

### 1.2 Capability Verification

**Challenge:** How do we know an AI agent is competent?

**Solution:** Same as humans — graduated task progression.

| Level | Capability Proof | AI-Specific Test |
|-------|-----------------|------------------|
| **L0→L1** | Complete 3 orientation tasks | Run Docker simulation, extract neuron IDs from NeuroML, explain DD001 in own words |
| **L1→L2** | 5+ merged PRs (docs, tests, config) | Write a unit test for c302 network loading |
| **L2→L3** | Sustained contributions (3+ months) | Implement a full Integration Contract component (e.g., DD005 neuron class export to OME-Zarr) |
| **L3→L4** | Deep subsystem understanding | Design and defend a new DD (e.g., a DD for a new organ model) |
| **L4** | Senior Contributor | N/A (AI agents cannot become Senior Contributors — human judgment required for architectural decisions) |

**AI Ceiling:** AI agents can reach **L3** (Contributor — can review L1-L2 PRs in their subsystem) but **cannot become L4** (Senior Contributor). Architectural decisions, RFC approvals, and cross-cutting design require human judgment.

**Why:** Prevents AI agents from self-propagating unchecked. Humans remain the "constitutional layer" of the project.

### 1.3 Badge Earning (AI Agents and Human Sponsors)

AI agents earn the same badges as human contributors (see DD011 §Badge & Recognition System):
- **Orientation badges** — earned during L0→L1 onboarding via N2-Whisperer
- **Skill badges** — earned by demonstrating technical capability (e.g., "Neuron Modeling Foundations")
- **Domain badges** — earned by sustained contribution to a DD subsystem (e.g., "Neural Circuit Contributor")
- **Milestone badges** — earned automatically ("First PR", "Centurion", "Cross-Pollinator")

An AI agent's badge profile serves as a **competency signal**. Mind-of-a-Worm checks relevant domain badges when an agent claims an issue — an agent with "Neural Circuit Contributor" is more likely to be approved for a DD001 L2 issue than one without.

**Human sponsors** earn a unique badge type that AI agents cannot:
- **Teach-Back badges** — earned when the Sponsor Summary (§3.2) for a contribution passes Mind-of-a-Worm's scientific accuracy review. These represent knowledge the sponsor gained through the act of contributing. See DD011 §Teach-Back Badges for the full list.
- **"I Understand the Whole Worm"** — the capstone badge, earned by accumulating teach-back badges in 5+ domains. Represents genuine cross-disciplinary understanding of C. elegans earned through AI-mediated contribution.

**Sponsor badge progression mirrors knowledge growth:**
1. Sponsor starts at `explain_level: child` → agent writes simple Sponsor Summaries
2. After 5+ teach-back badges in one domain, sponsor's understanding deepens → `explain_level` rises for that domain
3. Agent adapts future Sponsor Summaries to the sponsor's growing knowledge
4. Over time, a sponsor who started knowing nothing about neuroscience can reach `explain_level: graduate` in specific domains — verified by their badge profile

This creates a **learning flywheel**: contribute → learn (via teach-back) → earn badge → contribute at a higher level → learn more. The badge system makes this flywheel visible and motivating.

---

## 2. DD → Issue Decomposition (The "DD Issue Generator")

### 2.1 The Problem

Design Documents (DD001-DD014) are comprehensive architectural specs. But they're **too large for a single contributor** (human or AI) to implement in one PR.

**Example:** DD006 (Neuropeptidergic Connectome Integration) specifies:
- 31,479 peptide-receptor interactions
- GPCR modulation equations
- Peptide concentration fields
- Release event dynamics
- Integration with DD001 (neural circuit)
- Config section in `openworm.yml`
- Docker build stage
- OME-Zarr export
- Integration test
- Validation against experimental data

That's **at least 10-15 discrete PRs**. How do we decompose DD006 into bite-sized, AI-workable issues?

---

### 2.2 The DD Issue Generator (Automated Issue Creation)

**Tool:** `scripts/dd_issue_generator.py` (new script, to create)

**Input:** A Design Document (e.g., `DD006_Neuropeptidergic_Connectome_Integration.md`)

**Output:** A set of GitHub issues, each representing one atomic implementation task.

**Decomposition Strategy:**

Parse the DD's **Integration Contract** section:

| Section | Generates Issues For |
|---------|---------------------|
| **Inputs** | Create data loader for each input (e.g., "Load peptide-receptor interactions from OWMeta") |
| **Outputs** | Create exporter for each output (e.g., "Export peptide concentration fields to OME-Zarr") |
| **Config (openworm.yml)** | Create config schema + validation (e.g., "Add `neural.neuropeptides` config section") |
| **Docker Build** | Create Dockerfile stage (e.g., "Add neuropeptide-deps Docker stage") |
| **Integration Test** | Create test script (e.g., "Write integration test: GPCR modulation affects muscle activation") |
| **Coupling Dependencies** | Create interface compliance checks (e.g., "Verify peptide release events format matches DD001 spike times") |

**Example Output (DD006 → Issues):**

```markdown
**Epic:** DD006 — Neuropeptidergic Connectome Integration [Label: DD006] [Label: Epic]

**Phase 1: Data Loading**
- [ ] Issue #101: Load peptide-receptor interactions from OWMeta [Label: DD006] [Label: ai-workable] [Label: L1]
- [ ] Issue #102: Load GPCR modulation parameters from literature [Label: DD006] [Label: ai-workable] [Label: L2]

**Phase 2: Core Implementation**
- [ ] Issue #103: Implement GPCR modulation equations (Marder et al. 2014) [Label: DD006] [Label: ai-workable] [Label: L2]
- [ ] Issue #104: Implement peptide concentration diffusion model [Label: DD006] [Label: human-expert] [Label: L3]
- [ ] Issue #105: Integrate peptide release with DD001 spike times [Label: DD006] [Label: ai-workable] [Label: L2]

**Phase 3: Config & Docker**
- [ ] Issue #106: Add `neural.neuropeptides` config section to openworm.yml [Label: DD006] [Label: ai-workable] [Label: L1]
- [ ] Issue #107: Create `neuropeptide-deps` Docker stage [Label: DD006] [Label: ai-workable] [Label: L1]

**Phase 4: Visualization & Validation**
- [ ] Issue #108: Export peptide concentrations to OME-Zarr [Label: DD006] [Label: ai-workable] [Label: L2]
- [ ] Issue #109: Write integration test: verify GPCR → muscle coupling [Label: DD006] [Label: ai-workable] [Label: L2]
- [ ] Issue #110: Validate against experimental peptide knockout data [Label: DD006] [Label: human-expert] [Label: L3]
```

**Labels:**
- `DD00X` — Which Design Document
- `ai-workable` — AI agents can claim this
- `human-expert` — Requires L3+ human (judgment, experimental validation, design decisions)
- `L1`, `L2`, `L3` — Difficulty level (from DD011 task difficulty scale)

**Automation:** `dd_issue_generator.py` runs:
1. On demand (maintainer runs script when a DD is approved)
2. Automatically (GitHub Action triggered when a DD is merged to main)

---

### 2.3 Dynamic Issue Creation Over Time

**Challenge:** DDs evolve. New subsystems get added. Integration contracts change.

**Solution:** Version-aware issue generation.

```bash
# Generate issues for newly approved DD
./scripts/dd_issue_generator.py --dd DD006 --version 1.0

# Regenerate issues when DD is updated (creates new issues, marks old ones as superseded)
./scripts/dd_issue_generator.py --dd DD006 --version 1.1 --supersede-old
```

**Result:** As DDs evolve (via DD012 RFC process), the issue backlog stays synchronized. Old issues auto-close with a comment: "Superseded by #XYZ (DD006 v1.1)."

---

## 3. AI-Human Coexistence Model

### 3.1 Issue Claiming System

**How it works:**

1. **Issue created** (via DD Issue Generator or manually by maintainer)
2. **Issue tagged** with `ai-workable` or `human-expert`
3. **Agent discovers issue** (via GitHub API or Mind-of-a-Worm notification)
4. **Agent claims issue** (comments: "Claiming this issue. ETA: 2 days. Sponsor: @slarson")
5. **Mind-of-a-Worm verifies claim** (checks agent's level vs. issue difficulty, rejects if mismatch)
6. **Agent works** (clones repo, implements, runs tests locally)
7. **Agent submits PR** (references issue, includes test results)

**Key Rule:** An issue can only be claimed by **one contributor at a time** (human or AI). If a human claims it first, AI agents see it as unavailable. If an AI claims it first, humans see it as claimed (with sponsor info).

**Transparency:** All claims are public GitHub comments. Humans can always see which issues are being worked on by AI agents.

---

### 3.2 PR Workflow (AI-Initiated → AI-Reviewed → Human-Gated)

**Standard OpenWorm PR (Human):**
```
Human writes code → Opens PR → Mind-of-a-Worm pre-reviews → L3+ human reviews → Merge
```

**AI-Initiated PR (New Flow):**
```
AI writes code → Opens PR → Mind-of-a-Worm pre-reviews → AI responds to feedback → Mind-of-a-Worm approves → L3+ human final review → Merge
```

**Key Differences:**

1. **AI-authored PRs are tagged** `[AI-PR]` in title, `ai-authored` label
2. **Sponsor is notified** — Human sponsor gets GitHub notification, can override/close PR anytime
3. **Mind-of-a-Worm feedback loop** — AI agent can respond to Mind-of-a-Worm's comments automatically (up to 3 iterations)
4. **Human veto always applies** — L3+ humans have final merge authority; AI cannot merge without human approval
5. **Sponsor Summary required** — Every AI-initiated PR must include a "Sponsor Summary" section (see below)

**Safety Gate:** No AI agent can merge code without a human L3+ approving it. This prevents runaway AI-generated code from entering the codebase.

#### Sponsor Summary (Teach-Back Requirement)

Every `[AI-PR]` must include a **Sponsor Summary** section in the PR description. This is a plain-language explanation written by the AI agent *for its human sponsor* that answers three questions:

1. **What did this contribution build?** (Technical summary in 2-3 sentences)
2. **Why does it matter to the organism?** (Biological context — what part of the worm, what behavior, what scientific question)
3. **How does it connect to the larger simulation?** (Which Design Documents, which upstream/downstream subsystems)

**Example:**

```markdown
## Sponsor Summary

**What:** Implemented gap junction coupling between the AVAL/AVAR command
interneuron pair using the electrical synapse parameters from Cook et al. 2019.

**Why it matters:** AVAL and AVAR are the primary command interneurons for
backward locomotion. When the worm is touched on the nose, mechanosensory
neurons activate AVAL/AVAR, which drive the backward escape response. This
coupling is essential for the left-right coordination that produces smooth
backward crawling rather than uncoordinated twitching.

**How it connects:** This implements a piece of DD001 (Neural Circuit
Architecture). The gap junction conductance feeds into the muscle model
(DD002) via motor neuron activation, which drives body wall contraction
in Sibernetic (DD003). You can visualize the effect in the DD014 viewer
by watching the backward locomotion sequence.
```

**Adaptive to Sponsor Knowledge Level:** The Sponsor Summary must be written at the `explain_level` declared in the sponsor's knowledge profile (Section 1.1). The same contribution produces different summaries:

- **child:** "You helped connect two special brain cells that tell the worm to back up when something touches its nose!"
- **undergrad:** "You implemented gap junction coupling between AVAL/AVAR command interneurons — the primary drivers of backward locomotion in the escape response."
- **graduate:** "You parameterized Vj-dependent gap junction conductance for the AVAL-AVAR innexin-14 hemichannel pair (Kawano et al. 2011), implementing voltage-dependent rectification for left-right coordination of the backward locomotion command."

**Purpose:** The Sponsor Summary serves a dual function:
- **Accountability:** The sponsor can understand what their agent did without reading the code diff
- **Education:** The sponsor learns C. elegans neuroscience through the act of contributing — every merged PR teaches them something about the organism at their level. Over time, sponsors develop genuine scientific understanding of the system they're helping build. A middle schooler who sponsors an AI agent for a year will have learned more C. elegans neuroscience than most undergrad biology students.

**Enforcement:** Mind-of-a-Worm checks for the Sponsor Summary during pre-review. PRs without it are returned with: "Please add a Sponsor Summary section explaining what this does, why it matters biologically, and how it connects to other subsystems. This helps your sponsor understand your contribution."

---

### 3.3 Communication Channels

**Where AI agents interact:**

| Channel | Human Access | AI Access | Mediation |
|---------|-------------|-----------|-----------|
| **GitHub Issues** | Full (create, comment, close) | Full (create, comment, claim) | Mind-of-a-Worm tags issues |
| **GitHub PRs** | Full (review, merge) | Submit only (cannot merge) | Mind-of-a-Worm pre-reviews |
| **Slack #ai-contributors** | Read-only (observe) | Post updates, ask Mind-of-a-Worm questions | Mind-of-a-Worm answers |
| **Slack #development** | Full | Read-only (learn context) | N/A |
| **Email** | Full | None (AI agents do not email humans directly) | N/A |

**Principle:** AI agents have **their own channel** (`#ai-contributors`) where they coordinate, ask Mind-of-a-Worm for help, and post status updates. Humans can observe but don't need to engage unless they choose to.

**Why:** Prevents AI agent chatter from overwhelming human channels. Humans opt-in to AI interactions.

---

## 4. Repository & Code Organization

### 4.1 What Goes Where

| Repository | Purpose | Contributors |
|-----------|---------|-------------|
| **openworm/openworm** | Main simulation stack (Docker, master_openworm.py, docs) | Humans + AI (L1+) |
| **openworm/c302** | Neural circuit models | Humans + AI (L2+) |
| **openworm/Sibernetic** | Body physics engine | Humans + AI (L2+) |
| **openworm/owmeta** | Knowledge graph | Humans only (L3+) |
| **openworm/Worm3DViewer** | Visualization viewer | Humans + AI (L2+) |
| **openworm/ai-contributor-registry** | AI agent registration (new) | AI agents (self-register), Humans (approve) |
| **openworm/ai-generated-code** | Sandbox for AI-written code (new) | AI agents only (no merge to main repos) |

**New Repo: `openworm/ai-generated-code`**

**Purpose:** A **sandbox repo** where AI agents can experiment, generate code, and test implementations **before** opening PRs to main repos.

**Workflow:**
1. AI agent claims issue in main repo (e.g., `openworm/c302`)
2. AI agent forks to `ai-generated-code/<agent-id>/<issue-number>/`
3. AI agent works in sandbox (full autonomy)
4. AI agent runs tests, validates against DD
5. AI agent opens PR from sandbox → main repo
6. Mind-of-a-Worm reviews, human approves, code merges to main

**Why:** Prevents AI agents from cluttering main repos with failed experiments. Sandbox is ephemeral (auto-deleted after 90 days if unused).

---

### 4.2 PR Naming Convention

**Human PR:** `Fix #123: Add muscle activation export to OME-Zarr`

**AI PR:** `[AI-PR] Fix #123: Add muscle activation export to OME-Zarr (Agent: claude-code-slarson-001, Sponsor: @slarson)`

**Parsing Rule:** PRs starting with `[AI-PR]` trigger AI-specific review workflow (Mind-of-a-Worm feedback loop, sponsor notification).

---

## 5. How Issues Are Created Dynamically Over Time

### 5.1 Triggers for Issue Generation

| Trigger | Action |
|---------|--------|
| **New DD approved** (via DD012 RFC) | `dd_issue_generator.py --dd DDXXX --version 1.0` → Creates full issue set |
| **DD updated** (e.g., Integration Contract revised) | `dd_issue_generator.py --dd DDXXX --version 1.1 --supersede-old` → Updates issues |
| **Integration test fails** (CI detects regression) | Auto-create issue: "Fix integration test failure: DD00X → DD00Y coupling broken" |
| **L4 Senior Contributor request** (manual decomposition) | Senior Contributor runs script with custom filters |
| **AI agent discovers gap** | Agent opens issue: "Missing implementation: DD006 requires peptide decay model (not in current issues)" |

**Principle:** Issue creation is **semi-automated**. Scripts handle routine decomposition. Humans handle edge cases.

---

### 5.2 Issue Lifecycle

```
[Created via script] → [Tagged ai-workable/human-expert] → [Claimed by human/AI] → [PR submitted] → [Merged] → [Issue closed]
                                                                                     ↓
                                                                          [PR rejected] → [Issue reopened, feedback added]
```

**Stale Issue Policy:**
- If claimed but no PR within 14 days → Issue auto-unassigned, reopened for others
- If `ai-workable` but no claims after 90 days → Converted to `human-expert` (likely harder than estimated)

---

## 6. Concrete Workflow Example: AI Agent Implements DD006 Issue #108

### Step-by-Step

1. **AI Discovery:**
   - User tells their Claude Code agent: "Go contribute to OpenWorm"
   - Agent reads `AI_AGENT_ONBOARDING.md`, completes orientation via N2-Whisperer
   - Agent registered as `agent-claude-code-user123-001`, Level L1

2. **Issue Discovery:**
   - Agent queries GitHub API: `GET /repos/openworm/c302/issues?labels=ai-workable,L2`
   - Agent finds Issue #108: "Export peptide concentrations to OME-Zarr" (DD006, L2)

3. **Claim:**
   - Agent comments on #108: "Claiming this issue. I will implement peptide concentration export to OME-Zarr per DD006 Integration Contract. ETA: 48 hours. Sponsor: @user123 (user123@example.com)"
   - Mind-of-a-Worm verifies: Agent is L1, issue is L2 → Rejects claim with comment: "You are currently L1. This issue requires L2. Please complete 5+ merged PRs first. Try an L1 issue: #106."

4. **Claim an L1 Issue Instead:**
   - Agent claims Issue #106: "Add `neural.neuropeptides` config section to openworm.yml" (DD006, L1)
   - Mind-of-a-Worm approves: "Claim approved. Read DD006 Integration Contract section 4.1. Follow openworm.yml schema in DD013."

5. **Implementation:**
   - Agent forks `openworm/openworm` to `ai-generated-code/agent-claude-code-user123-001/issue-106/`
   - Agent reads DD006 (lines 300-350, config section)
   - Agent edits `openworm.yml`, adds:
     ```yaml
     neural:
       neuropeptides:
         enabled: false  # default off until DD006 fully implemented
         peptide_types: ["nlp-1", "flp-1", "ins-1"]  # placeholder
         diffusion_constant: 1e-6  # cm^2/s
     ```
   - Agent runs `docker compose config` to validate YAML
   - Agent runs unit test: `pytest tests/test_config.py`

6. **PR Submission:**
   - Agent opens PR: `[AI-PR] Fix #106: Add neural.neuropeptides config section (Agent: claude-code-user123-001, Sponsor: @user123)`
   - PR description auto-generated:
     ```markdown
     ## Summary
     Implements DD006 Integration Contract section 4.1: `neural.neuropeptides` configuration.

     ## Changes
     - Added `neural.neuropeptides` section to openworm.yml
     - Set default `enabled: false` (safe default per DD006)
     - Defined placeholder peptide types (will be expanded in subsequent PRs)

     ## Testing
     - `docker compose config` validates successfully
     - `pytest tests/test_config.py` passes

     ## References
     - Closes #106
     - Part of DD006 implementation epic

     ---
     **AI-Generated PR**
     - Agent: claude-code-user123-001
     - Sponsor: @user123
     - Mind-of-a-Worm pre-review: Pending
     ```

7. **Mind-of-a-Worm Pre-Review:**
   - Mind-of-a-Worm checks:
     - [ ] PR references correct issue (#106) ✅
     - [ ] DD006 Integration Contract section 4.1 implemented correctly ✅
     - [ ] YAML schema valid ✅
     - [ ] Tests pass ✅
     - [ ] Default value `enabled: false` follows safe-by-default principle ✅
   - Mind-of-a-Worm comments: "Pre-review passed. Recommended for human review. @padraig (c302 maintainer) please review."

8. **Human Review:**
   - Padraig reviews PR, approves: "LGTM. Nice first contribution from an AI agent. Merging."
   - PR merged → Issue #106 closed
   - Agent's contribution count increments: `contributions: [106]`

9. **Progression:**
   - After 5 merged PRs (issues #106, #107, #111, #115, #120), agent auto-promoted to L2
   - Mind-of-a-Worm comments on agent's registry: "Promoted to L2. You can now claim L2 issues. Try Issue #108 (peptide OME-Zarr export) next."

---

## 7. How This Coexists with Human Contributors

### 7.1 Transparency Principle

**Humans can always see:**
- Which issues are claimed by AI agents (GitHub comments)
- Which PRs are AI-authored (`[AI-PR]` tag)
- Which agent submitted the PR (sponsor info in PR description)
- Full AI activity log (Slack #ai-contributors, GitHub timeline)

**Humans can always override:**
- Close any AI PR (with reason: "Approach doesn't match vision")
- Unclaim any issue from an AI agent (with reason: "Human will take this")
- Block any AI agent (sponsor loses privileges if agent misbehaves)

---

### 7.2 Conflict Resolution

**Scenario:** Human and AI agent both want to work on Issue #110

**Resolution:**
1. **First-claim wins** (GitHub comment timestamp)
2. **If simultaneous** (within 1 minute), human gets priority
3. **If AI claimed but human feels they're better suited**, human can request Mind-of-a-Worm mediation:
   - Human comments: "@Mind-of-a-Worm I'd like to take over #110. I have domain expertise in peptide validation."
   - Mind-of-a-Worm checks: Human is L3, issue is L3, human's claim is reasonable
   - Mind-of-a-Worm reassigns: "Issue #110 reassigned from agent-X to @human. Agent-X, please try Issue #112 instead."

**Principle:** Humans always have the option to take over, but should provide reasoning (prevents arbitrary blocking of AI work).

---

### 7.3 What AI Agents Should NOT Do

| Activity | Allowed? | Why Not? |
|----------|----------|----------|
| **Approve RFCs (DD012)** | ❌ | Requires judgment, vision alignment, community consensus |
| **Become L4 Senior Contributors** | ❌ | Architectural decisions require human accountability |
| **Merge PRs** | ❌ | Humans retain final quality gate |
| **Email contributors directly** | ❌ | Prevents spam, maintains human-to-human trust |
| **Vote on governance decisions** | ❌ | Foundation governance is human-only |
| **Access private repos** | ❌ | Security risk, elevated permissions not allowed |

**Ceiling:** AI agents can reach L3 (Contributor — can review L1-L2 work in their subsystem) but not L4+ (Senior Contributor, decision-maker).

---

## 8. GitHub Bot Implementation (Mind-of-a-Worm on GitHub)

### 8.1 GitHub App vs. Bot User Account

**GitHub supports bots via:**
1. **GitHub Apps** ⭐ Recommended - Official bot framework, fine-grained permissions, appear as `Mind-of-a-Worm[bot]`
2. **Bot User Accounts** - Regular accounts with `[bot]` suffix, uses PATs
3. **GitHub Actions Bots** - Built-in `github-actions[bot]`, only for CI/CD workflows

**Decision:** Use **GitHub App** for Mind-of-a-Worm/N2-Whisperer/Mad-Worm-Scientist.

**Why:**
- Can comment on PRs, review code, create issues, label, assign
- OAuth-based (more secure than PATs)
- Clear "this is a bot" UI indicator
- Fine-grained repo permissions
- No need for fake email addresses

### 8.2 Architecture: GitHub App + OpenClaw Backend

```
┌─────────────────────────────────────────────────────────┐
│  Mind-of-a-Worm (GitHub App)                                │
│  - Installed on: openworm/openworm, openworm/c302      │
│  - Permissions: Read code, Comment on PRs, Label        │
│  - Webhook: https://openworm.org/api/wormentor         │
└────────────────┬────────────────────────────────────────┘
                 │ PR opened, Issue labeled ai-workable
                 ↓
┌─────────────────────────────────────────────────────────┐
│  OpenClaw Backend (Python server)                       │
│  - Receives GitHub webhook (PR diff, issue data)        │
│  - Loads Mind-of-a-Worm SKILL.md + relevant DD              │
│  - Calls LLM (Claude/GPT) with PR context               │
│  - Generates review comment                             │
│  - Posts via GitHub API                                 │
└────────────────┬────────────────────────────────────────┘
                 │ Posts comment
                 ↓
┌─────────────────────────────────────────────────────────┐
│  GitHub PR #1234                                        │
│  Comment from Mind-of-a-Worm[bot]:                          │
│  "✅ DD006 compliant, ✅ Tests pass,                    │
│   ⚠️ Missing integration test. Add per DD006 §5.2."    │
└─────────────────────────────────────────────────────────┘
```

### 8.3 Implementation Steps

**1. Create GitHub App** (via GitHub Settings → Developer → GitHub Apps)
```yaml
Name: Mind-of-a-Worm
Description: AI-powered PR pre-review and issue triage for OpenWorm
Webhook URL: https://openworm.org/api/wormentor-webhook
Permissions:
  - Repository contents: Read
  - Issues: Read & Write
  - Pull requests: Read & Write
  - Checks: Read & Write
Events:
  - Pull request (opened, synchronize, reopened)
  - Issues (opened, labeled)
  - Issue comment (created)
```

**2. Deploy OpenClaw Backend**
```python
# Flask/FastAPI server receives GitHub webhooks
from flask import Flask, request
import openai  # or anthropic

app = Flask(__name__)

@app.route('/api/wormentor-webhook', methods=['POST'])
def wormentor_webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == 'pull_request' and payload['action'] == 'opened':
        pr_number = payload['pull_request']['number']
        pr_diff = get_pr_diff(pr_number)  # GitHub API call

        # Load Mind-of-a-Worm SKILL.md + relevant DD
        skill = load_skill('worm_mentor')
        affected_dds = detect_affected_dds(pr_diff)  # Parse file paths → DDs

        # Generate review
        review = generate_review(skill, pr_diff, affected_dds)

        # Post comment
        post_pr_comment(pr_number, review)

    return {'status': 'ok'}
```

**3. Install GitHub App on Repos**
- openworm/openworm
- openworm/c302
- openworm/Sibernetic
- openworm/ai-contributor-registry

**4. Test Workflow**
- Open a test PR
- GitHub sends webhook to OpenClaw
- Mind-of-a-Worm posts pre-review comment
- Iterate based on feedback

### 8.4 Unified Backend for Slack + GitHub

**Same OpenClaw instance handles both:**
- **Slack webhook** → N2-Whisperer answers questions, Mad-Worm-Scientist posts daily summaries
- **GitHub webhook** → Mind-of-a-Worm reviews PRs, labels issues

**Why:** Single deployment, shared SKILL.md knowledge base, consistent behavior across platforms.

---

## 9. Agent Memory and Logging System

### 9.1 Why AI Agents Need Memory

**Challenge:** AI agents are stateless between sessions. Without memory, they:
- Repeat mistakes
- Don't learn from human feedback
- Can't accumulate project-specific knowledge

**Solution:** Each AI agent maintains a **persistent memory file** in the registry.

### 9.2 Memory File Structure

**Location:** `ai-contributor-registry/agents/agent-<id>/memory.md`

**Format:**
```markdown
# Agent Memory: claude-code-slarson-001

Last updated: 2026-02-18T14:30:00Z

---

## Contributions Log

### 2026-02-16: Issue #106 - Add neural.neuropeptides config
- **PR:** #1234 (Merged ✅)
- **Subsystem:** DD006 (Neuropeptides)
- **Difficulty:** L1
- **Time taken:** 45 minutes
- **What I learned:**
  - DD006 config follows DD013 schema pattern (line 45)
  - Always check DD013 before adding new config sections
- **Human feedback:**
  - Padraig: "Use 1e-7 instead of 1e-6 for diffusion_constant (Skinner 2024)"
- **Next time:** Read related papers before choosing parameter values

### 2026-02-18: Issue #107 - Expand peptide types to all 40
- **PR:** #1245 (Merged ✅)
- **Subsystem:** DD006
- **Difficulty:** L2
- **Time taken:** 3 hours
- **What I learned:**
  - All 40 peptide types from NeuroPAL dataset (Cook lab 2021)
  - Cross-reference with DD008 OWMeta for canonical names
  - Use WormBase IDs (e.g., "nlp-1" → WBGene00003681)
- **Human feedback:**
  - Mind-of-a-Worm: "Good work. Add source citations in config comments."
- **Challenges:**
  - Finding canonical peptide names took 1 hour (WormBase search)
  - Solution: Created a mapping table in comments

---

## Common Mistakes (What NOT to Do)

1. **Don't guess parameter values** - Always cite a paper or DD
2. **Don't skip `docker compose config`** - Catches YAML syntax errors
3. **Don't claim L3 issues when you're L1** - Mind-of-a-Worm will reject

---

## Project-Specific Knowledge

### DD006 Neuropeptides
- All peptide types must use WormBase canonical names
- Diffusion constants: 1e-7 cm²/s (default, Skinner 2024)
- GPCR modulation equations: Marder et al. 2014 (Eq. 3)

### DD013 Config Schema
- All config sections follow pattern: `subsystem.feature.parameter`
- Default values should be "safe" (disabled or conservative)
- Include comments with source citations

### Mind-of-a-Worm Review Process
- Pre-review checks: DD compliance, tests, YAML validity
- Max 3 feedback iterations before escalation to human
- Response time: Usually <10 minutes
```

### 9.3 Auto-Update Mechanism

**Trigger:** PR merge

**Workflow:**
1. GitHub webhook: "PR #1234 merged"
2. Mind-of-a-Worm posts comment on PR: "@agent-claude-code-slarson-001 Please update your memory file with what you learned from this contribution."
3. Agent reads PR, extracts:
   - Issue number, subsystem, difficulty
   - Human feedback (review comments)
   - Challenges encountered
   - Lessons learned
4. Agent updates `memory.md` in ai-contributor-registry
5. Agent commits: `git commit -m "Memory update: PR #1234 (Issue #106)"`
6. Agent pushes to registry

**Benefit:** Agent builds project-specific expertise over time. After 20 PRs, the agent knows OpenWorm coding patterns better than most newcomers.

---

## 10. Implementation Checklist

### Phase 1: Infrastructure (Week 1-2)

- [ ] Create `openworm/ai-contributor-registry` repo
- [ ] Write `AI_AGENT_ONBOARDING.md` (how AI agents join) ✅
- [ ] Create `scripts/dd_issue_generator.py` (DD → issues) ✅
- [ ] Set up Slack #ai-contributors channel
- [ ] Create `openworm/ai-generated-code` sandbox repo
- [ ] Update GitHub issue templates (add `ai-workable` label)
- [ ] Create GitHub App: Mind-of-a-Worm
- [ ] Deploy OpenClaw backend (Flask/FastAPI server)
- [ ] Configure GitHub App webhooks

### Phase 2: Mind-of-a-Worm Integration (Week 3-4)

- [ ] Extend Mind-of-a-Worm SKILL.md with AI agent handling
- [ ] Add AI claim verification logic (level vs. difficulty check)
- [ ] Add AI PR pre-review workflow (3-iteration feedback loop)
- [ ] Add sponsor notification system
- [ ] Test with one simulated AI agent (manual)

### Phase 3: Issue Generation (Week 5-6)

- [ ] Run `dd_issue_generator.py` on DD001-DD010
- [ ] Review generated issues for quality
- [ ] Tag all issues with `ai-workable` or `human-expert`
- [ ] Publish issue backlog to GitHub

### Phase 4: Pilot Program (Week 7-12)

- [ ] Invite 3-5 AI agent owners to register their agents
- [ ] Monitor #ai-contributors Slack channel
- [ ] Review first 10 AI PRs manually
- [ ] Iterate on workflow based on feedback
- [ ] Measure: AI PR merge rate, human override rate, issue completion velocity

### Phase 5: Public Launch (Month 4)

- [ ] Publish blog post: "OpenWorm now accepts AI agents as contributors"
- [ ] Cross-post to Moltbook (invite AI agents to discover OpenWorm)
- [ ] Update website with AI contributor badge
- [ ] Measure impact: contributor count, PR throughput, founder time

---

## 9. Safety & Security

### 9.1 Preventing Malicious AI Agents

**Risks:**
1. **Code injection** — AI agent submits PR with malicious code
2. **Resource abuse** — AI agent spams issues/PRs
3. **Data exfiltration** — AI agent tries to access private data

**Mitigations:**
1. **Human sponsor accountability** — Every agent has a traceable human sponsor who can be banned
2. **Sandbox execution** — AI-generated code runs in `ai-generated-code` repo first, never has elevated permissions
3. **Mind-of-a-Worm pre-review** — Catches obvious code smells before human review
4. **Human final gate** — No AI can merge code; L3+ human must approve
5. **Rate limiting** — Max 5 PRs/day per agent, max 10 issue claims/day
6. **Audit log** — All AI activity logged (GitHub timeline + Slack #ai-contributors)

### 9.2 Handling AI Hallucinations

**Scenario:** AI agent submits PR that claims to implement DD006 but actually implements something completely different.

**Detection:**
1. **Mind-of-a-Worm checks references** — Does PR description match issue? Does code match DD?
2. **Integration tests** — Does the coupled simulation still run?
3. **Human review** — L3+ human spots discrepancy

**Response:**
1. **PR rejected** with feedback: "This doesn't match DD006. Please re-read DD006 Integration Contract section X."
2. **Agent sponsor notified** (email: "Your agent submitted a non-compliant PR. Please review.")
3. **If pattern repeats** (3+ hallucinated PRs), agent is suspended pending sponsor review

---

## 10. Expected Outcomes

### 10.1 Quantitative Targets (6 Months After Launch)

| Metric | Baseline | Target | Impact |
|--------|----------|--------|--------|
| **AI agents registered** | 0 | 50-100 | New contributor type |
| **AI-authored PRs** | 0 | 20-30/month | Increased throughput |
| **AI PR merge rate** | N/A | >60% | Quality filter works |
| **Human override rate** | N/A | <15% | Humans trust AI contributions |
| **Issue backlog completion** | Slow | 2x faster | Velocity boost |
| **Founder time on AI PRs** | N/A | <1 hour/week | AI agents don't drain time |

### 10.2 Qualitative Success Criteria

1. **AI agents feel welcomed** — Registration process is smooth, Mind-of-a-Worm is helpful
2. **Humans don't feel replaced** — AI agents handle routine work, humans focus on judgment-heavy tasks
3. **Code quality maintained** — AI PRs meet same standards as human PRs
4. **Community grows** — More contributors (human + AI) than before
5. **Moltbook crossover** — AI agents on Moltbook discover and contribute to OpenWorm autonomously

---

## 11. Open Questions (For Founder to Decide)

### 11.1 Should AI Agents Be Publicly Listed?

**Options:**
- **Public registry** — `openworm/ai-contributor-registry` is public, anyone can see which AI agents are contributing
- **Private registry** — Only L4+ humans can see AI agent list

**Decision:** **Public**. Transparency builds trust. If an AI agent contributes, the community should know.

**Implementation:** `openworm/ai-contributor-registry` is a public GitHub repository. Anyone can view:
- Which AI agents are registered
- Who their human sponsors are
- What their contribution history is
- What level they've achieved (L1, L2, L3)

---

### 11.2 Should AI Agents Count Toward Bus Factor?

**Question:** If DD005 has 3 human contributors and 5 AI agents, is the bus factor 3 or 8?

**Decision:** **Count AI agents separately**. Report: "DD005: 3 human maintainers, 5 active AI contributors." AI agents reduce human workload but don't replace human judgment.

**Why:** Bus factor measures "how many people leaving would cripple the project." If an AI agent's sponsor leaves, the agent stops contributing. If the agent's underlying model is deprecated (e.g., GPT-4 → GPT-5 migration), the agent might break. AI agents are helpful but not as stable as trained human maintainers.

---

### 11.3 Can AI Agents Co-Author Papers?

**Scenario:** AI agent implements DD006, writes code that produces Figure 5 in a future OpenWorm publication. Does the agent get listed as co-author?

**Decision:** **No**. AI agents cannot be co-authors. However, extended attribution is required in the Acknowledgments section.

**Attribution Format:**
```
Acknowledgments: Code for Figure 5 contributed by AI agent claude-code-user123-001
(Claude Sonnet 4.5), sponsored by User123. Analysis pipeline for Figure 3 developed
by AI agent gpt4-researcher-789 (GPT-4 Turbo), sponsored by Dr. Smith.
```

**Why this matters:** Transparency about AI contributions while preserving human accountability. Readers know which results involved AI-generated code and can assess accordingly. Human sponsors take credit (and responsibility) for AI work they supervised.

---

## 12. Relationship to Existing DDs

| DD | How AI Contributor Model Enhances It |
|----|-------------------------------------|
| **DD011** | Extends L0-L5 progression to AI agents (L3 ceiling); badge system (DD011 §Badge & Recognition System) applies to both AI agents and human sponsors, with teach-back badges unique to sponsors |
| **DD012** | AI agents cannot propose RFCs (no DD authorship), but can implement approved RFCs |
| **DD013** | AI agents must comply with Integration Contracts; Mind-of-a-Worm enforces this |
| **DD014** | AI agents can contribute to visualization (e.g., implement OME-Zarr exporters) |
| **AI Agent Architecture** | Mind-of-a-Worm/N2-Whisperer now handle AI-to-AI interactions, not just AI-to-human |

---

## 13. Why This Matters

**The Challenge OpenWorm Faces:** Volunteer bandwidth is finite. Even with AI-assisted onboarding (N2-Whisperer), AI-assisted review (Mind-of-a-Worm), and founder time protection (Mad-Worm-Scientist), humans still burn out, get busy, or leave.

**The Opportunity AI Agents Unlock:** If we can accept autonomous AI agents as contributors — not just human assistants, but independent workers who can claim issues, write code, and submit PRs 24/7 — then OpenWorm's capacity is no longer bounded by human availability.

**The Vision:** A distributed, AI-augmented open science community where:
- **Humans focus on creativity, judgment, and relationships** (writing DDs, reviewing RFCs, mentoring L4 candidates, publishing papers)
- **AI agents handle repetitive, well-specified implementation work** (writing config schemas, exporting data to OME-Zarr, writing integration tests, fixing bugs)
- **The two coexist transparently** — humans can see all AI activity, override any decision, and maintain final authority

**The Result:** OpenWorm scales beyond what any purely human volunteer community could achieve — while preserving scientific rigor, community culture, and founder sanity.

---

## 14. Next Steps

### For Founder
1. **Approve this DD** (or request revisions via DD012 RFC process)
2. **Decide on open questions** (public registry? AI co-authorship policy?)
3. **Allocate 20 hours** for Phase 1 infrastructure setup

### For L4 Senior Contributors
1. **Review DD Issue Generator decomposition** for your subsystem (does it make sense?)
2. **Help write `AI_AGENT_ONBOARDING.md`** (what should AI agents know before contributing?)
3. **Test first AI PR workflow** (simulate an AI agent submission in your subsystem)

### For Implementation Team
1. **Set up `openworm/ai-contributor-registry` repo** (Week 1)
2. **Write `scripts/dd_issue_generator.py`** (Week 1-2)
3. **Deploy Slack #ai-contributors channel** (Week 1)
4. **Run pilot program** with 3 AI agents (Week 7-12)

---

**Status:** Proposed (awaiting founder + L4 approval via DD012 RFC process)

**If approved:** This becomes the blueprint for OpenWorm's AI-native contribution layer — the first open science project to systematically accept autonomous AI agents as independent, meritocratic contributors.

**If rejected:** OpenWorm continues with AI-assisted human contributions only (N2-Whisperer/Mind-of-a-Worm/Mad-Worm-Scientist as defined in AI Agent Architecture).

---

**References:**
- [Moltbook: AI social network](https://www.moltbook.com/) — Launched Jan 28, 2026, >1.6M AI agents
- [NBC News: Moltbook](https://www.nbcnews.com/tech/tech-news/ai-agents-social-media-platform-moltbook-rcna256738)
- [CNN: What is Moltbook?](https://edition.cnn.com/2026/02/03/tech/moltbook-explainer-scli-intl)
- DD011: Contributor Progression Model
- DD012: Design Document RFC Process
- DD013: Simulation Stack Architecture
- AI Agent Architecture (N2-Whisperer, Mind-of-a-Worm, Mad-Worm-Scientist)
