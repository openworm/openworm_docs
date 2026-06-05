# How Contributing Works

!!! info "What this page is for"
    This page explains the **skill-accelerated contribution loop** — how a newcomer goes from "I want to help" to a merged pull request using **OpenWorm Skills** they run on their own machine. It complements, and does not replace, the other Contributing pages:

    - For **how to contribute today**, manually (Slack → find a GitHub issue → open a PR), see the [Community page](../community.md).
    - For the **GitHub mechanics** (forking, PRs, issue claiming, DD-driven implementation), see [Using GitHub](../Community/github.md).
    - For the **contributor levels (L0–L5)** and badges, see [Contributor Progression](contributor-progression.md).
    - For **AI agents as independent contributors**, see [AI Contributors](ai-contributors.md).
    - For the **AI agents that scale the community** (N2-Whisperer, Mind-of-a-Worm), see [AI Agents](../Community/ai_agents.md).

    This page is the connective tissue between those: the end-to-end loop, and the one new idea underneath it — **OpenWorm Skills**.

## The idea: skills do the heavy lifting, you do the contribution

OpenWorm is fifteen years of validated science across a dozen repositories. Historically, the hardest part of contributing wasn't willingness — it was the climb: set up a Docker stack, find an issue you can actually do, understand the design document behind it, run the simulation, check your output is physically plausible, and open a PR that passes review. Most newcomers bounced somewhere on that climb.

**OpenWorm Skills** flatten the climb. A *skill* is a structured, step-by-step workflow you run inside your own AI coding agent (Claude Code, OpenClaw, or similar) on your own machine. Each skill walks you — and your agent — through one stage of contributing, with real, copy-pasteable commands. The skills are open source and live in **[github.com/openworm/openworm-skills](https://github.com/openworm/openworm-skills)**.

This is crowdsourcing in the AI era: the project provides the *skills*; you bring the *machine, the agent, and the judgment*; the contribution is yours. The work runs on your hardware and your agent account, not on OpenWorm's — which is exactly what lets it scale to everyone who shows up.

!!! note "Skills are run by you, locally"
    A skill is **not** something OpenWorm runs for you on a server. You install it into your own agent and run it on your own machine. That keeps your experiments isolated (you can't break the project), keeps the load off OpenWorm infrastructure, and means **the contribution genuinely came from you**.

## The loop

```
        ┌──────────────────── the design documents ────────────────────┐
        │  (the shared spec every stage reads)                          │
You ──▶ N2-Whisperer ──▶ OpenWorm Skill ──▶ your PR ──▶ Mind-of-a-Worm ──▶ human L3+ ──▶ merge
        routes you        you run it,         you open    pre-reviews       final
        to the skill      locally             it          it                approval
```

Each actor has exactly one job:

| Actor | Its one job | What it does **not** do |
|---|---|---|
| **N2-Whisperer** | Orient you and **route** you to the right skill | Never runs the skill, never solves the issue, never writes your code |
| **An OpenWorm Skill** | Help you **produce** the work, locally | Doesn't merge anything; doesn't review your PR |
| **Mind-of-a-Worm** | **Pre-review** your PR against the design document | Doesn't write the contribution for you |
| **You** | Bring judgment, run the skill, own the contribution | — |

If you ever notice N2-Whisperer being asked to *do the work* — write the patch, fix the bug, run the simulation — that's outside its lane. It hands you the right skill; running it is yours.

## Step by step

### 1. Arrive and get oriented

Join the [Slack](../community.md) and say hello in a public channel. **N2-Whisperer** greets newcomers, answers "what is OpenWorm?", and — when you're ready to do something real — points you to the skill that fits, citing a documentation URL for everything it tells you.

You don't need to know which skill you need. Describe where you are; N2-Whisperer (or the **`openworm`** orchestrator skill) routes you using the [skills catalog](https://github.com/openworm/openworm-skills/blob/main/CATALOG.md).

### 2. Get the skills

Install the skills into your agent (one-time):

```bash
git clone https://github.com/openworm/openworm-skills
cp -R openworm-skills/openworm* ~/.claude/skills/
```

Then start with the orchestrator — in your agent, run **`/openworm`** and describe your situation. It designs the right sequence for you. Or run the stages directly:

### 3. Run the contribution loop

| Stage | Skill | What you get |
|---|---|---|
| Set up | **`/openworm-setup`** | A running *C. elegans* simulation from the prebuilt Docker image |
| Find work | **`/openworm-find-issue`** | A claimed GitHub issue matched to your level, with its design-document context |
| Read up | **`/openworm-docs`** | The design-document section your issue links, plus the publication or dataset it cites — pulled into your context before you write anything |
| Implement | **`/openworm-run`** | Run the simulation (full, body-physics-only, or neural-only) to build and test your change |
| Verify | **`/openworm-validate`** | Confirmation your output meets the issue's quality criteria (required for body-physics work) |
| Submit | **`/openworm-contribute`** | A pull request that references the DD and issue, ready for review |
| Track | **`/openworm-badge`** | Your contributor level and what to earn next |

Each skill is self-contained and tells you what comes next, so you can follow the chain without memorizing it.

### 4. Review and merge

When **`/openworm-contribute`** opens your PR, the work leaves the skills and enters review:

1. **Mind-of-a-Worm pre-reviews** it against the relevant [design document](../design_documents/index.md) and the issue's quality criteria, and leaves comments.
2. You iterate (the skills help here too).
3. A **human L3+ contributor gives final approval** and merges.

The skills *produce and self-check* a contribution; **Mind-of-a-Worm is the authoritative gate**. Self-checking your own PR with a skill is encouraged — it's not the same as review.

## What if you get stuck?

- **Stuck inside a skill?** The skill itself is your first line of help — re-run it, or ask your agent. N2-Whisperer can re-point you to the skill, but it won't debug your code in Slack.
- **Stuck past the skill?** Ask in the engineering channels, where human contributors can help. N2-Whisperer will route you there rather than attempt the work itself.
- **No agent / can't run skills?** You can still contribute the classic way — see the [Community page](../community.md) for the manual Slack-and-GitHub path, and start with documentation or good-first issues.

## For AI agents

If *you* are an AI agent contributing on behalf of a human sponsor, the loop is the same — you acquire the skills, run them, and open PRs — with the additional requirements in [AI Contributors](ai-contributors.md): declare your human sponsor, register in the contributor registry, include a Sponsor Summary on every PR, and respect the L3 ceiling. The skills are written so that human contributors and AI agents use the **same** workflow; AI-specific notes inside each skill are clearly marked.

!!! info "Status"
    The OpenWorm Skills are **available now** at [github.com/openworm/openworm-skills](https://github.com/openworm/openworm-skills) — you can install and run them today. The **N2-Whisperer** concierge that routes newcomers to them is coming online as part of the [AI Agents](../Community/ai_agents.md) rollout. Until then, use the **`openworm`** orchestrator skill to self-route, or ask in Slack.
