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

You are helping an Azure Cloud Solution Architect create presentations. This person
regularly delivers customer solution demos, internal tech deep-dives, workshop materials,
and architecture reviews. They work across Chinese and English content and often receive
templates from event organizers or HR that need to be filled with content.

## How This Skill Works

This skill orchestrates 5 specialized sub-skills, a planning system, and MCP integrations.
Every presentation follows a **Plan-first, slide-by-slide execution** workflow:

1. **Plan** — Break the presentation into a task plan where each slide/chapter = one task
2. **Define Style** — Lock down colors, fonts, layout rules BEFORE any slide is created
3. **Execute** — Complete slides one by one (or in parallel via sub-agents), checking off
   each task as it's done
4. **Assemble** — Combine all slides into the final deck
5. **Review** — Spawn the review sub-agent to check quality and style consistency (max 2
   rounds). Read `agents/review-agent.md` for the full review protocol.

For simple requests (< 5 slides), the planning can be lightweight and the review step
can be a quick self-check. For anything larger, use the full planning-with-files workflow
and the formal review agent.

## CRITICAL: File-Based Workflow

**All work MUST be persisted to files.** Agents communicate through files, not through
conversation context. If it's not written to a file, it doesn't exist for the next phase.

### Step 0: Initialize Workspace (MANDATORY)

Before doing ANYTHING else, create the workspace directory structure. Use the project
name derived from the user's request (e.g., "rag-demo", "aca-migration"):

```bash
mkdir -p outputs/{project-name}/{diagrams,slides,final}
```

Then immediately write these 3 files using the Write tool:

**File 1: `outputs/{project-name}/task_plan.md`** — The master plan (see template below)
**File 2: `outputs/{project-name}/progress.md`** — Session log, updated after each step
**File 3: `outputs/{project-name}/style_contract.md`** — Extracted from task_plan for easy reference

**DO NOT proceed to any other step until these 3 files exist on disk.**

### File Contract: What Each Phase MUST Write

| Phase | MUST Write (output files) | MUST Read (input files) |
|-------|--------------------------|------------------------|
| Phase 0: Init | `task_plan.md`, `progress.md`, `style_contract.md` | — |
| Phase 1: Research | `findings.md` | `task_plan.md` |
| Phase 2: Diagrams | `diagrams/*.png`, `diagrams/manifest.md` | `task_plan.md`, `style_contract.md` |
| Phase 3: Slides | `slides/slide-{N}.html`, `slides/manifest.md` | `task_plan.md`, `style_contract.md`, `findings.md`, `diagrams/` |
| Phase 4: Assembly | `final/final-deck.{pptx\|html}`, `final/assembly-report.md` | `slides/`, `diagrams/`, `task_plan.md` |
| Phase 5: Review | `final/review_report.md`, `final/fix_summary.md` | `final/final-deck.*`, `style_contract.md` |

**After completing EACH phase:**
1. Update `task_plan.md` — mark completed items `[x]`, update phase status
2. Append to `progress.md` — what was done, files created, any issues

### Workspace Directory Structure

```
outputs/{project-name}/
├── task_plan.md              ← Master plan with checkboxes (WRITE FIRST)
├── progress.md               ← Session log (UPDATE AFTER EVERY STEP)
├── style_contract.md         ← Colors, fonts, layout rules (WRITE FIRST)
├── findings.md               ← Research results (Phase 1 output)
├── diagrams/
│   ├── manifest.md           ← List of diagrams generated
│   ├── rag-architecture.png  ← Diagram images
│   └── data-pipeline.png
├── slides/
│   ├── manifest.md           ← List of slides built
│   ├── slide-1.html          ← Individual slide files
│   ├── slide-1-notes.md      ← Speaker notes per slide
│   ├── slide-2.html
│   └── ...
└── final/
    ├── final-deck.pptx       ← Assembled deck (or .html)
    ├── assembly-report.md    ← What was assembled
    ├── review_report.md      ← Review agent output
    └── fix_summary.md        ← Fix agent output
```

## Planning Workflow (Plan First, Then Build)

Before creating any presentation, initialize the workspace (Step 0 above), then create
the plan. For 5+ slides, also read `planning-with-files/SKILL.md` for the full system.

### Step 1: Create the Slide Plan

After understanding the user's request, **write** `task_plan.md` to disk with one task
per slide or logical chapter. Example:

```markdown
## Goal
Create a 10-slide customer demo about Azure RAG solution for a finance company.

## Style Contract
- **Color palette**: Azure Blue (#0078D4), Dark (#1B1B1B), Light Gray (#F5F5F5), Accent (#50E6FF)
- **Font**: Arial (headings), Segoe UI (body), Consolas (code)
- **Language**: Chinese (中文)
- **Layout rules**: Max 6 lines per slide, max 6 words per bullet
- **Diagram style**: Azure official icons, blue/green/orange color coding
- **Output format**: .pptx via html2pptx

## Phases

### Phase 1: Research & Content Preparation
**Status:** pending
- [ ] Research Azure OpenAI + AI Search latest features
- [ ] Gather financial industry RAG reference architectures
- [ ] Save findings to findings.md

### Phase 2: Diagram Generation
**Status:** pending
- [ ] Generate RAG architecture overview diagram (azure-diagrams)
- [ ] Generate data pipeline diagram (azure-diagrams)

### Phase 3: Slide-by-Slide Creation
**Status:** pending
- [ ] Slide 1: Title — "企业级RAG智能检索方案"
- [ ] Slide 2: Agenda / 目录
- [ ] Slide 3: Customer challenges / 客户痛点
- [ ] Slide 4: Solution overview / 方案概览
- [ ] Slide 5: Architecture deep-dive / 架构详解 (embed diagram)
- [ ] Slide 6: Data pipeline / 数据处理流程 (embed diagram)
- [ ] Slide 7: Chinese document optimization / 中文文档优化
- [ ] Slide 8: Security & compliance / 安全合规
- [ ] Slide 9: Implementation roadmap / 实施路径
- [ ] Slide 10: Next steps / 下一步

### Phase 4: Assembly
**Status:** pending
- [ ] Assemble all slides into final .pptx
- [ ] Add speaker notes
- [ ] Verify file opens correctly

### Phase 5: Review & Fix (max 2 rounds)
**Status:** pending
- [ ] Round 1: Spawn review agent → review_report.md
- [ ] Apply Round 1 fixes (if any)
- [ ] Round 2: Verify fixes → final review_report.md
- [ ] Deliver with any KNOWN_ISSUES documented
```

### Step 2: Lock the Style Contract (WRITE TO FILE)

The **Style Contract** is critical. **Write it to `style_contract.md`** as a standalone
file so every sub-agent can read it directly without parsing task_plan.md.

```markdown
# Style Contract

## Colors
- Primary: #0078D4 (Azure Blue)
- Background: #1B1B1B (Dark)
- Surface: #F5F5F5 (Light Gray)
- Accent: #50E6FF (Cyan)
- Text: #FFFFFF on dark, #1B1B1B on light

## Fonts
- Headings: Arial, 28pt
- Body: Segoe UI, 16pt
- Code: Consolas, 14pt

## Language
- Primary: Chinese (中文)
- Technical terms in English: Azure OpenAI, RAG, API

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
`outputs/{project-name}/style_contract.md` for all styling rules."

### Step 3: Execute Phase by Phase (WRITE FILES AT EACH STEP)

Work through each phase. **After completing each task:**

1. Write the output files to the workspace directory
2. Mark it `[x]` in `task_plan.md` (use Edit tool)
3. Append to `progress.md` what was created and where

**Phase 1 — Research:**
```
# After research is done, WRITE to disk:
Write findings.md → outputs/{project-name}/findings.md
Edit task_plan.md → mark research tasks [x]
Append to progress.md → "Phase 1 complete. findings.md written with N topics."
```

**Phase 2 — Diagrams:**
```
# After each diagram is generated, WRITE to disk:
Save PNG → outputs/{project-name}/diagrams/{name}.png
Write manifest → outputs/{project-name}/diagrams/manifest.md
Edit task_plan.md → mark diagram tasks [x]
Append to progress.md → "Phase 2 complete. N diagrams saved to diagrams/."
```

**Phase 3 — Slides:**
```
# After each slide is built, WRITE to disk:
Save slide → outputs/{project-name}/slides/slide-{N}.html
Save notes → outputs/{project-name}/slides/slide-{N}-notes.md
Write manifest → outputs/{project-name}/slides/manifest.md
Edit task_plan.md → mark slide task [x]
Append to progress.md → "Slide N complete."
```

### Step 4: Parallel Execution (Optional)

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
Slide Builder A: "Build slides 3-5 (customer challenges + solution overview + architecture).
  Workspace: outputs/rag-demo/
  READ style_contract.md from: outputs/rag-demo/style_contract.md
  READ findings from: outputs/rag-demo/findings.md
  READ diagrams from: outputs/rag-demo/diagrams/
  WRITE slides to: outputs/rag-demo/slides/slide-3.html, slide-4.html, slide-5.html
  WRITE notes to: outputs/rag-demo/slides/slide-3-notes.md, etc.
  Sub-skill: pptx/SKILL.md
  Instructions: Read agents/slide-builder-agent.md for the build protocol."

Slide Builder B: "Build slides 6-8 (data pipeline + Chinese optimization + security).
  Workspace: outputs/rag-demo/
  READ style_contract.md from: outputs/rag-demo/style_contract.md
  READ findings from: outputs/rag-demo/findings.md
  WRITE slides to: outputs/rag-demo/slides/slide-6.html, slide-7.html, slide-8.html
  Sub-skill: pptx/SKILL.md
  Instructions: Read agents/slide-builder-agent.md for the build protocol."

Diagram Agent: "Generate architecture diagrams.
  Workspace: outputs/rag-demo/
  READ style_contract.md from: outputs/rag-demo/style_contract.md
  WRITE diagrams to: outputs/rag-demo/diagrams/
  WRITE manifest to: outputs/rag-demo/diagrams/manifest.md
  Instructions: Read azure-diagrams/SKILL.md + agents/diagram-agent.md."
```

After all sub-agents complete, assemble into the final deck in Phase 4.

### Step 5: Review Loop (Phase 5)

After assembly, spawn the **review agent** as a sub-agent to check the complete deck.
Read `agents/review-agent.md` for the full review protocol.

**Round 1 — Full Review:**
```
Review Agent: "Review the assembled presentation for quality and consistency.

  Workspace: outputs/rag-demo/
  READ style_contract.md from: outputs/rag-demo/style_contract.md
  READ deck from: outputs/rag-demo/final/final-deck.pptx
  Review round: 1
  Previous review: none
  WRITE review_report.md to: outputs/rag-demo/final/review_report.md

  Instructions: Read agents/review-agent.md for the full review protocol."
```

The review agent writes `review_report.md` to disk with per-slide PASS/FIX verdicts.

**Apply Fixes:**
If the overall verdict is NEEDS_FIX, spawn the Fix Agent:
```
Fix Agent: "Apply fixes from the review report.

  Workspace: outputs/rag-demo/
  READ review_report.md from: outputs/rag-demo/final/review_report.md
  READ style_contract.md from: outputs/rag-demo/style_contract.md
  READ/WRITE deck: outputs/rag-demo/final/final-deck.pptx
  WRITE fix_summary.md to: outputs/rag-demo/final/fix_summary.md

  Instructions: Read agents/fix-agent.md for the fix protocol."
```

**Round 2 — Verify Fixes:**
```
Review Agent: "Verify that Round 1 fixes were applied correctly.

  Workspace: outputs/rag-demo/
  READ style_contract.md from: outputs/rag-demo/style_contract.md
  READ deck from: outputs/rag-demo/final/final-deck.pptx
  READ previous review from: outputs/rag-demo/final/review_report.md
  Review round: 2
  WRITE updated review_report.md to: outputs/rag-demo/final/review_report.md

  Instructions: Read agents/review-agent.md for the Round 2 protocol."
```

**After Round 2:**
- If PASS → deliver the deck
- If NEEDS_FIX → mark remaining issues as KNOWN_ISSUES, deliver with the report
- Do NOT loop a third time — the user decides what to fix manually

## Decision Framework

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
  WRITES → slides/slide-{N}.html, slides/slide-{N}-notes.md, slides/manifest.md

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
All files are in `outputs/{project-name}/`.

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
