---
name: csa-ppt
description: >
  Unified presentation skill for Azure Cloud Solution Architects. Orchestrates multiple
  specialized tools to create professional presentations, architecture diagrams, and
  technical content. Use this skill whenever the user mentions: creating slides, PPT,
  presentations, deck, 演示文稿, 幻灯片, architecture diagrams for slides, filling
  templates, customer demos, tech sharing, workshops, or any combination of diagrams +
  slides. Also trigger when the user provides a .pptx template to fill, asks to visualize
  Azure architectures in a presentation context, or needs Chinese-language slide content.
  This skill covers ALL presentation-related work — from a quick internal deck to a
  polished customer-facing solution demo with architecture diagrams.
---

# CSA Presentation Skill

## ⛔ THREE INVIOLABLE RULES

**These are HARD CONSTRAINTS, not suggestions. Violation = broken output.**

### Rule 1: CLARIFY-BEFORE-PLAN — Ask questions when requirements are unclear

**Before creating ANY plan or workspace, check if the user's request is complete enough.**

If ANY of these are unknown, call the **AskUserQuestion** tool with 1–4 questions:

| Must Know | Example Question |
|-----------|-----------------|
| Slide count | "大约需要多少页幻灯片？(5-8页 / 8-12页 / 12-20页)" |
| Target audience | "面向的观众是？(客户决策者 / 技术团队 / 内部同事)" |
| Language | "使用什么语言？(中文 / English / 中英混合)" |
| Output format | "输出格式？(.pptx / HTML网页 / 两者都要)" |

**Optional** (ask only if not obvious from context):
- Visual style preference (professional / technical / workshop)
- Whether to include architecture diagrams
- Whether a template is provided
- Key messages or must-include content

**Rules for asking:**
- ❌ Do NOT ask if the user already specified it (e.g., "做一个10页的PPT" → slide count is known)
- ❌ Do NOT ask more than 4 questions — infer the rest from context
- ❌ Do NOT start `mkdir` or any work before questions are answered
- ✅ Ask ALL questions in ONE AskUserQuestion call, not multiple rounds
- ✅ If the request is very detailed, skip directly to Step 1

### Rule 2: FILE-FIRST — All work must be written to files

The workspace markdown files (task_plan.md, style_contract.md, findings.md) are the
**single source of truth**. Sub-agents READ these files. If they don't exist, sub-agents
have no input and produce garbage.

- ❌ Running `python3` (diagrams) before task_plan.md exists = FORBIDDEN
- ❌ Generating HTML/PPTX slides before style_contract.md exists = FORBIDDEN
- ❌ Creating ANY content before the workspace directory exists = FORBIDDEN
- ✅ The ONLY correct first action is: `mkdir -p outputs/{project}/...`

### Rule 3: UPDATE-AFTER-EVERY-TASK — Enable resume from interruption

**After completing ANY task (research, diagram, slide, assembly, review), IMMEDIATELY
update `task_plan.md` to mark that task `[x]`.**

This is critical because:
- Sessions can be interrupted at any time (`/clear`, timeout, crash)
- On resume, the FIRST thing to do is `Read task_plan.md` to see what's done
- If task_plan.md is not updated, resume starts from scratch = wasted work

**Resume protocol** (when starting a new session in an existing workspace):
1. Call `ls outputs/` to find existing project directories
2. Call Read tool → `outputs/{project}/task_plan.md`
3. Find the first unchecked `[ ]` task → continue from there
4. Do NOT redo tasks already marked `[x]`

**THEREFORE: Execute the steps below in EXACT ORDER. No reordering. No skipping.**

### Step 1 → Determine project name, then create directories (ONLY after Rule 1 questions are answered)

Derive a short, descriptive project name from the user's request content:
- "帮我做Azure RAG方案的PPT" → `rag-demo`
- "AKS迁移到ACA的技术分享" → `aks-to-aca`
- "季度工作汇报" → `quarterly-report`

Then call the Bash tool:
```bash
mkdir -p outputs/{project}/{diagrams,slides,final}
```

**ALL files for this presentation go under `outputs/{project}/`. No exceptions.**

### Step 2 → Write tool: Create 3 mandatory files

Call the Write tool 3 times in sequence. These files MUST exist before ANY other work.

**Call Write tool** → file_path: `outputs/{project}/task_plan.md`
Content: The slide plan with checkboxes. Use the task_plan.md template below.

**Call Write tool** → file_path: `outputs/{project}/style_contract.md`
Content: Colors, fonts, language, density rules. Use the style_contract.md template below.

**Call Write tool** → file_path: `outputs/{project}/progress.md`
Content: `# Progress Log\n\n## Workspace initialized\n- task_plan.md created\n- style_contract.md created`

### Step 3 → CHECKPOINT: Verify files exist

Call the Bash tool:
```bash
ls -la outputs/{project}/task_plan.md outputs/{project}/style_contract.md outputs/{project}/progress.md
```
If ANY file is missing, go back to Step 2. **Do NOT proceed until all 3 files are confirmed.**

### Step 4 → Research (if needed) → Write findings to file

If the topic needs research (web search, Azure docs), do the research, then:

**Call Write tool** → file_path: `outputs/{project}/findings.md`
Content: Structured research findings (topics, key points, terminology).

**Then immediately update task_plan.md:**
**Call Edit tool** → mark Phase 1 research tasks as `[x]` in `outputs/{project}/task_plan.md`
**Call Edit tool** → append to `outputs/{project}/progress.md`: "Phase 1 complete. findings.md written."

### Step 5 → PRE-CHECK before EVERY phase

**Before starting ANY phase (diagrams, slides, assembly, review), run this check:**

```bash
ls outputs/{project}/task_plan.md outputs/{project}/style_contract.md
```

If either file is missing → STOP → go back to Step 1 and create them.

Additionally, each phase must READ the outputs of previous phases:
- Before diagrams → READ `task_plan.md` + `style_contract.md`
- Before slides → READ `task_plan.md` + `style_contract.md` + `findings.md` (if exists) + check `diagrams/`
- Before assembly → READ `task_plan.md` + check `slides/` directory
- Before review → READ `style_contract.md` + check `final/` directory

**If a required input file does not exist, do NOT proceed. Create it first.**

### Step 6 → Create diagrams and slides (ONLY after Step 5 passes)

Only NOW may you call sub-skills (azure-diagrams, frontend-slides, pptx, etc.).

**AFTER EVERY artifact, update task_plan.md immediately:**

- Each diagram → Write to `outputs/{project}/diagrams/{name}.png`
  → **Edit `task_plan.md`**: mark this diagram task `[x]`
  → **Append to `progress.md`**: "Diagram {name}.png generated."
- Each slide → Write to `outputs/{project}/slides/slide-{N}.{pptx|html}`
  → Write speaker notes to `outputs/{project}/slides/slide-{N}-notes.md`
  → **Edit `task_plan.md`**: mark this slide task `[x]`
  → **Append to `progress.md`**: "Slide N complete."
- After ALL diagrams done → **Edit `task_plan.md`**: mark Phase 2 status as complete
- After ALL slides done → **Edit `task_plan.md`**: mark Phase 3 status as complete

**RULE: If you are about to run a python3/node script but `task_plan.md` does not exist yet, STOP and go back to Step 1.**

---

## Context

You are helping an Azure Cloud Solution Architect create presentations. This person
regularly delivers customer solution demos, internal tech deep-dives, workshop materials,
and architecture reviews. They work across Chinese and English content and often receive
templates from event organizers or HR that need to be filled with content.

## File Contract (all paths under `outputs/{project}/`)

| Phase | MUST Write (output files) | MUST Read (input files) |
|-------|--------------------------|------------------------|
| Phase 0: Init | `task_plan.md`, `progress.md`, `style_contract.md` | — |
| Phase 1: Research (if needed) | `findings.md` | `task_plan.md` |
| Phase 2: Diagrams | `diagrams/*.png`, `diagrams/manifest.md` | `task_plan.md`, `style_contract.md` |
| Phase 3: Slides | `slides/slide-{N}.{pptx\|html}`, `slides/manifest.md` | `task_plan.md`, `style_contract.md`, `findings.md` (if exists), `diagrams/` |
| Phase 4: Assembly | `final/final-deck.{pptx\|html}`, `final/assembly-report.md` | `slides/`, `diagrams/`, `task_plan.md` |
| Phase 5: Review | `final/review_report.md`, `final/fix_summary.md` | `final/final-deck.*`, `style_contract.md` |

**After completing EACH phase:**
1. Update `task_plan.md` — mark completed items `[x]`, update phase status
2. Append to `progress.md` — what was done, files created, any issues

All files live under `outputs/{project}/`. See README for the full directory tree.

## Templates (referenced by Execution Protocol above)

For 5+ slides, also read `planning-with-files/SKILL.md` for the full system.

### task_plan.md Template

Write this to `outputs/{project}/task_plan.md` in Step 1. **Replace ALL placeholders
with content from the user's ACTUAL request. Do NOT copy the example text verbatim.**

```markdown
## Goal
{Describe the actual presentation goal based on user's request}

## Style Contract
- **Color palette**: {Choose appropriate colors for the topic}
- **Font**: {Choose appropriate fonts}
- **Language**: {Language from Rule 1 answers or user's request}
- **Layout rules**: Max 6 lines per slide, max 8 words per bullet
- **Diagram style**: {If diagrams needed, describe style}
- **Output format**: {Format from Rule 1 answers or user's request}

## Phases

### Phase 1: Research & Content Preparation
**Status:** pending
- [ ] {Research task 1 based on actual topic}
- [ ] {Research task 2}
- [ ] Save findings to findings.md

### Phase 2: Diagram Generation
**Status:** pending
- [ ] {Diagram 1 based on actual content needs}
- [ ] {Diagram 2 if needed}

### Phase 3: Slide-by-Slide Creation
**Status:** pending
- [ ] Slide 1: {Actual title from user's topic}
- [ ] Slide 2: {Actual slide content}
- [ ] ...{One line per slide, based on Rule 1 answers for slide count}

### Phase 4: Assembly
**Status:** pending
- [ ] Assemble all slides into final deck
- [ ] Add speaker notes
- [ ] Verify file opens correctly

### Phase 5: Review & Fix (max 2 rounds)
**Status:** pending
- [ ] Round 1: Review → review_report.md
- [ ] Apply fixes (if any)
- [ ] Round 2: Verify fixes
- [ ] Deliver
```

### style_contract.md Template

Write this to `outputs/{project}/style_contract.md` in Step 1. **Fill in based on
Rule 1 answers and the user's request. Do NOT copy example values blindly.**

```markdown
# Style Contract

## Colors
- Primary: {Choose based on topic — e.g., #0078D4 for Azure, #107C10 for sustainability}
- Background: {Dark or light based on audience preference}
- Surface: {Complementary color}
- Accent: {Highlight color}
- Text: {Contrast text color}

## Fonts
- Headings: {Professional font, 28pt}
- Body: {Readable font, 16pt}
- Code: {Monospace font if code needed, 14pt}

## Language
- Primary: {From user's request or Rule 1 answer}
- Technical terms: {Which terms stay in English}

## Content Density
- Max 6 lines per slide
- Max 8 words per bullet (Chinese: 15 characters)
- Overflow → speaker notes

## Diagram Colors
- Azure services: #0078D4
- Data flow: #50E6FF
- External systems: #FF8C00

## Output Format
- Tool chain: pptx via html2pptx
- Image resolution: 300 DPI / 2x scale
```

**Every sub-agent prompt must include**: "Read `style_contract.md` at
`outputs/{project}/style_contract.md` for all styling rules."

### Per-Phase File Write Commands

After completing each task, use these exact commands:

**Phase 1 — Research:**
```
# After research is done, WRITE to disk:
Write findings.md → outputs/{project}/findings.md
Edit task_plan.md → mark research tasks [x]
Append to progress.md → "Phase 1 complete. findings.md written with N topics."
```

**Phase 2 — Diagrams:**
```
# After each diagram is generated, WRITE to disk:
Save PNG → outputs/{project}/diagrams/{name}.png
Write manifest → outputs/{project}/diagrams/manifest.md
Edit task_plan.md → mark diagram tasks [x]
Append to progress.md → "Phase 2 complete. N diagrams saved to diagrams/."
```

**Phase 3 — Slides:**

Each sub-agent **chooses the intermediate format per-slide** based on content:
- **Use .pptx** (via python-pptx) for: simple layouts, English-only content, standard bullet slides
- **Use .html** for: complex layouts, Chinese-heavy content, code blocks, rich formatting

The Assembly Agent handles mixed formats during merge.

```
# After each slide is built, WRITE to disk:
Save slide → outputs/{project}/slides/slide-{N}.{pptx|html}  (format chosen by content)
Save notes → outputs/{project}/slides/slide-{N}-notes.md
Write manifest → outputs/{project}/slides/manifest.md  (must record format per slide)
Edit task_plan.md → mark slide task [x]
Append to progress.md → "Slide N complete. Format: {pptx|html}."
```

### Step 7 → Assembly (Phase 4) — ONLY after all slides and diagrams are complete

Spawn the **Assembly Agent** to merge individual slides into the final deck.
Read `agents/assembly-agent.md` for the full assembly protocol.

```
Assembly Agent: "Merge all slides and diagrams into the final deck.
  Workspace: outputs/{project}/
  READ task_plan.md from: outputs/{project}/task_plan.md
  READ slides from: outputs/{project}/slides/
  READ diagrams from: outputs/{project}/diagrams/
  WRITE final deck to: outputs/{project}/final/final-deck.{pptx|html}
  WRITE assembly report to: outputs/{project}/final/assembly-report.md
  Instructions: Read agents/assembly-agent.md for the assembly protocol."
```

**After assembly:**
**Call Edit tool** → mark Phase 4 tasks as `[x]` in `outputs/{project}/task_plan.md`
**Append to `progress.md`**: "Phase 4 complete. Final deck assembled."

### Step 8 → Review & Fix (Phase 5) — ONLY after assembly is complete

Read `agents/review-agent.md` for the full review protocol. Max 2 rounds.

**Round 1 — Full Review:**
```
Review Agent: "Review the assembled presentation for quality and consistency.
  Workspace: outputs/{project}/
  READ style_contract.md from: outputs/{project}/style_contract.md
  READ deck from: outputs/{project}/final/final-deck.{pptx|html}
  Review round: 1
  WRITE review_report.md to: outputs/{project}/final/review_report.md
  Instructions: Read agents/review-agent.md for the full review protocol."
```

**Apply Fixes (if verdict is NEEDS_FIX):**
```
Fix Agent: "Apply fixes from the review report.
  Workspace: outputs/{project}/
  READ review_report.md from: outputs/{project}/final/review_report.md
  READ style_contract.md from: outputs/{project}/style_contract.md
  READ/WRITE deck: outputs/{project}/final/final-deck.{pptx|html}
  WRITE fix_summary.md to: outputs/{project}/final/fix_summary.md
  Instructions: Read agents/fix-agent.md for the fix protocol."
```

**Round 2 — Verify Fixes:**
```
Review Agent: "Verify Round 1 fixes were applied correctly.
  Workspace: outputs/{project}/
  READ style_contract.md from: outputs/{project}/style_contract.md
  READ deck from: outputs/{project}/final/final-deck.{pptx|html}
  READ previous review from: outputs/{project}/final/review_report.md
  Review round: 2
  WRITE updated review_report.md to: outputs/{project}/final/review_report.md
  Instructions: Read agents/review-agent.md for the Round 2 protocol."
```

**After review:**
- If PASS → deliver the deck
- If NEEDS_FIX after Round 2 → mark remaining as KNOWN_ISSUES, deliver with report
- Do NOT loop a third time
- **Call Edit tool** → mark Phase 5 tasks as `[x]` in `outputs/{project}/task_plan.md`
- **Append to `progress.md`**: "Phase 5 complete. Review verdict: {PASS|NEEDS_FIX}."

---

### Guidance: Parallel Execution (Optional, for 10+ slides)

For large presentations (10+ slides), you can use multiple sub-agents to build different
chapters simultaneously. The key rules for parallel execution:

**What to parallelize:**
- Independent content chapters (e.g., "Security" and "Cost Optimization" slides)
- Diagram generation (can run alongside slide creation)
- Research tasks (web search for different topics)

**What must be sequential:**
- Title slide and agenda (created first, defines the structure)
- Final assembly and verification (created last)

**How to keep style consistent across sub-agents:**
Each sub-agent MUST receive:
1. The **Style Contract** from the plan (colors, fonts, layout rules)
2. The **output format** and tool chain to use
3. A reference to any already-completed slides for visual consistency
4. The same sub-skill SKILL.md instructions

Example parallel dispatch — note every agent gets the **workspace path** so it reads
shared files (style_contract.md, findings.md) and writes to the correct location:

```
Slide Builder A: "Build slides 3-5 ({actual slide titles from task_plan.md}).
  Workspace: outputs/{project}/
  READ style_contract.md from: outputs/{project}/style_contract.md
  READ findings from: outputs/{project}/findings.md
  READ diagrams from: outputs/{project}/diagrams/
  WRITE slides to: outputs/{project}/slides/slide-{N}.{pptx|html}
    → Choose format per-slide: .pptx for simple layouts, .html for complex/Chinese content
  WRITE notes to: outputs/{project}/slides/slide-{N}-notes.md
  Sub-skill: pptx/SKILL.md (for .pptx slides) or frontend-slides/SKILL.md (for .html slides)
  Instructions: Read agents/slide-builder-agent.md for the build protocol."

Slide Builder B: "Build slides 6-8 ({actual slide titles from task_plan.md}).
  Workspace: outputs/{project}/
  READ style_contract.md from: outputs/{project}/style_contract.md
  READ findings from: outputs/{project}/findings.md
  WRITE slides to: outputs/{project}/slides/slide-{N}.{pptx|html}
    → Use .html for Chinese-heavy slides, .pptx for simple layouts
  Sub-skill: pptx/SKILL.md or frontend-slides/SKILL.md
  Instructions: Read agents/slide-builder-agent.md for the build protocol."

Diagram Agent: "Generate architecture diagrams.
  Workspace: outputs/{project}/
  READ style_contract.md from: outputs/{project}/style_contract.md
  WRITE diagrams to: outputs/{project}/diagrams/
  WRITE manifest to: outputs/{project}/diagrams/manifest.md
  Instructions: Read azure-diagrams/SKILL.md + agents/diagram-agent.md."
```

After all sub-agents complete, assemble into the final deck in Phase 4.

### Guidance: Review Details

See Step 8 above for the review and fix protocol. Key points:
- Max 2 review rounds
- After Round 2, remaining issues become KNOWN_ISSUES — the user decides what to fix manually

## Decision Framework

> ⛔ **PREREQUISITE**: Before using this framework, `task_plan.md` and `style_contract.md`
> MUST already exist on disk. If they don't, go back to the Execution Sequence at the top.

Analyze the request along these dimensions, then route accordingly:

### 1. What's the primary content type?

| Content | Best Tool | Why |
|---------|-----------|-----|
| Azure architecture diagram | **azure-diagrams** | 700+ official Azure icons, professional layout |
| Hand-drawn / conceptual diagram | **excalidraw-diagram** | Whiteboard aesthetic, great for brainstorming visuals |
| Swimlane / business process flow | **azure-diagrams** (matplotlib) | Built-in swimlane support |
| Sequence / auth flow | **azure-diagrams** | Dedicated sequence diagram patterns |
| Design mockup / wireframe | **Figma** or **Pencil** MCP | Interactive design tools |

### 2. What's the delivery format?

| Scenario | Format | Tool Chain |
|----------|--------|------------|
| Given a .pptx template to fill | .pptx | **skywork-ppt** (template workflow) or **pptx** (OOXML for complex templates) |
| Customer-facing formal deck | .pptx | **pptx** (html2pptx for rich layouts) or **skywork-ppt** (quick generation) |
| Internal sharing / demo | HTML or .pptx | **frontend-slides** if animation/中文 heavy; otherwise skywork-ppt |
| Architecture review document | Images + .pptx | **azure-diagrams** → embed in pptx |
| Workshop hands-on guide | HTML | **frontend-slides** (step-by-step with code blocks renders best in HTML) |

### 3. Language & encoding considerations

- **Chinese-heavy content (中文为主)**: Prefer **frontend-slides** (HTML) — it avoids
  font embedding issues that plague .pptx generation. If .pptx is required, use
  **pptx** (html2pptx.js) which handles CJK better than python-pptx.
- **English or mixed**: Any tool works fine.
- **Code snippets**: **frontend-slides** renders code beautifully with syntax highlighting.
  For .pptx, use **pptx** with monospace font blocks.

### 4. Template handling

When the user provides a template:

1. **Inspect first**: Read the template to understand its layouts, color scheme, and
   placeholder structure
2. **Choose the right tool**:
   - Simple content fill (text + images) → **skywork-ppt** `workflow_imitate.md`
   - Complex layout changes or strict formatting → **pptx** OOXML workflow
3. **Preserve template integrity**: Never change the template's master slides, color
   scheme, or font theme unless explicitly asked

## Common CSA Workflows

Read the appropriate reference file for the scenario at hand:

| Scenario | Reference | Typical Flow |
|----------|-----------|-------------|
| Customer Demo | `references/workflow-customer-demo.md` | Research → Diagrams → Narrative deck |
| Tech Sharing | `references/workflow-tech-sharing.md` | Outline → Code visuals → HTML/PPTX |
| Workshop | `references/workflow-workshop.md` | Steps → Code + diagrams → HTML slides |
| Architecture Review | `references/workflow-architecture-review.md` | As-is diagram → Gap analysis → Deck |
| Template Fill | `references/workflow-template-fill.md` | Analyze template → Map → Fill → Verify |

For orchestration patterns and MCP integration details, read `references/orchestration-and-mcp.md`.

## Sub-Skill Locations

> ⛔ **PREREQUISITE**: Do NOT read or invoke any sub-skill until Steps 1–4 of the
> Execution Sequence are complete and workspace files exist on disk.

These paths are relative to the skill directory:

| Skill | Path | When to Read |
|-------|------|-------------|
| planning-with-files | `planning-with-files/SKILL.md` | **Always** for 5+ slide decks — plan before build |
| azure-diagrams | `azure-diagrams/SKILL.md` | Need any Azure/architecture diagram |
| excalidraw-diagram | `excalidraw-diagram/SKILL.md` | Need hand-drawn style diagrams |
| frontend-slides | `frontend-slides/SKILL.md` | Creating HTML presentations |
| pptx | `pptx/SKILL.md` | Complex .pptx creation/editing |
| skywork-ppt | `skywork-ppt/SKILL.md` | Quick .pptx generation or template fill |

**Read the relevant sub-skill's SKILL.md before using it.** Each has specific patterns,
scripts, and constraints that matter for quality output.

## Sub-Agents

> ⛔ **PREREQUISITE**: Do NOT spawn any sub-agent until workspace files (task_plan.md,
> style_contract.md, findings.md) exist on disk. Agents READ these files as input.

The `agents/` directory contains instructions for specialized sub-agents. Read the
relevant agent file before spawning it.

| Agent | File | When to Spawn |
|-------|------|--------------|
| **Research Agent** | `agents/research-agent.md` | Phase 1 — gather Azure docs, features, case studies |
| **Diagram Agent** | `agents/diagram-agent.md` | Phase 2 — generate architecture diagrams and visuals |
| **Slide Builder Agent** | `agents/slide-builder-agent.md` | Phase 3 — build individual slides (parallelizable) |
| **Assembly Agent** | `agents/assembly-agent.md` | Phase 4 — merge slides + diagrams into final deck |
| **Review Agent** | `agents/review-agent.md` | Phase 5 — quality review (7 dimensions, max 2 rounds) |
| **Fix Agent** | `agents/fix-agent.md` | Phase 5 — apply fixes from review report |

**Agent interaction flow (file-based):**
```
Phase 0: Orchestrator
  WRITES → task_plan.md, style_contract.md, progress.md

Phase 1: Research Agent
  READS  ← task_plan.md
  WRITES → findings.md

Phase 2: Diagram Agent
  READS  ← task_plan.md, style_contract.md
  WRITES → diagrams/*.png, diagrams/manifest.md

Phase 3: Slide Builder Agent(s)  [parallelizable]
  READS  ← style_contract.md, findings.md, diagrams/
  WRITES → slides/slide-{N}.{pptx|html}, slides/slide-{N}-notes.md, slides/manifest.md
  FORMAT CHOICE: .pptx (simple/English) or .html (complex/Chinese/code) per slide

Phase 4: Assembly Agent
  READS  ← task_plan.md, slides/, diagrams/
  WRITES → final/final-deck.pptx, final/assembly-report.md

Phase 5: Review Agent (Round 1)
  READS  ← style_contract.md, final/final-deck.pptx
  WRITES → final/review_report.md

Phase 5: Fix Agent
  READS  ← final/review_report.md, style_contract.md, final/final-deck.pptx
  WRITES → final/final-deck.pptx (updated), final/fix_summary.md

Phase 5: Review Agent (Round 2)
  READS  ← style_contract.md, final/final-deck.pptx, final/review_report.md
  WRITES → final/review_report.md (updated)
```

Each sub-agent receives the **workspace path** so it can READ shared files
(style_contract.md, findings.md) and WRITE outputs to the correct location.
All files are in `outputs/{project}/`.

## Quality Checklist

Before delivering any presentation, verify:

- [ ] **Content accuracy**: Azure service names, pricing tiers, and features are current
- [ ] **Visual consistency**: Diagrams use consistent colors and icon styles throughout
- [ ] **Language**: No mixed-language issues (don't accidentally leave English labels in a
      Chinese deck or vice versa)
- [ ] **Font rendering**: For .pptx with Chinese text, verify characters render correctly
- [ ] **Image resolution**: All embedded diagrams are crisp, not pixelated
- [ ] **Template compliance**: If using a provided template, verify master slides are intact
- [ ] **Narrative flow**: Slides tell a story, not just list features

## Tips for CSA Presentations

→ For detailed tips, read `references/orchestration-and-mcp.md`

Key principles:
- Lead with the customer's problem, not Azure features
- Use progressive disclosure in architecture diagrams
- Include decision rationale (why CosmosDB over SQL?)
- Reference Well-Architected Framework pillars when relevant
