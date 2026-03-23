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
4. **Verify** — Review the assembled result for consistency

For simple requests (< 5 slides), the planning can be lightweight. For anything larger,
use the full planning-with-files workflow to track progress.

## Planning Workflow (Plan First, Then Build)

Before creating any presentation with 5+ slides, initialize a plan using the
**planning-with-files** skill. Read `planning-with-files/SKILL.md` for the full system.

### Step 1: Create the Slide Plan

After understanding the user's request, create a `task_plan.md` with one task per
slide or logical chapter. Example:

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

### Phase 4: Assembly & Verification
**Status:** pending
- [ ] Assemble all slides into final .pptx
- [ ] Verify visual consistency across all slides
- [ ] Check Chinese text rendering
- [ ] Add speaker notes
```

### Step 2: Lock the Style Contract

The **Style Contract** in the plan is critical — it ensures consistency whether you build
slides sequentially or in parallel. Before creating any slide, the style contract must
define:

- Color palette (primary, secondary, accent, background)
- Font family for headings, body text, and code
- Language and text direction
- Content density rules (max bullets, max words per bullet)
- Diagram color coding conventions
- Output format and tool chain

Every slide must reference this contract. When using sub-agents, pass the Style Contract
to each one explicitly.

### Step 3: Execute Slide by Slide

Work through Phase 3 one task at a time. After completing each slide:

1. Mark it `[x]` in `task_plan.md`
2. Update `progress.md` with what was created
3. Move to the next slide

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

Example parallel dispatch:
```
Sub-agent A: "Build slides 3-5 (customer challenges + solution overview + architecture).
  Style Contract: [paste from plan]. Use pptx html2pptx workflow.
  Save to: outputs/slides-3-5/"

Sub-agent B: "Build slides 6-8 (data pipeline + Chinese optimization + security).
  Style Contract: [paste from plan]. Use pptx html2pptx workflow.
  Save to: outputs/slides-6-8/"

Sub-agent C: "Generate architecture diagrams using azure-diagrams.
  Color scheme: Azure Blue + Green + Orange.
  Save to: outputs/diagrams/"
```

After all sub-agents complete, assemble into the final deck in Phase 4.

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

Read the appropriate reference file for detailed step-by-step guidance:

### Customer Solution Demo
→ Read `references/workflow-customer-demo.md`

Typical flow: Research (Tavily) → Architecture diagram (azure-diagrams) → Deck with
solution narrative (pptx or skywork-ppt)

### Internal Tech Sharing / Brown Bag
→ Read `references/workflow-tech-sharing.md`

Typical flow: Content outline → Code/architecture visuals → Interactive HTML deck
(frontend-slides) or quick .pptx (skywork-ppt)

### Workshop / Hands-on Lab
→ Read `references/workflow-workshop.md`

Typical flow: Step-by-step content → Code snippets + diagrams → HTML presentation
(frontend-slides) with embedded architecture diagrams

### Architecture Review (CAF/WAF)
→ Read `references/workflow-architecture-review.md`

Typical flow: Current-state diagram → Gap analysis visuals → Recommendations deck

### Template Fill (Event / HR / External)
→ Read `references/workflow-template-fill.md`

Typical flow: Analyze template → Map content to layouts → Fill preserving style

## Orchestration Patterns

### Pattern 1: Diagrams + Deck (most common)

When the user needs architecture diagrams IN a presentation:

1. Generate diagrams first using **azure-diagrams** or **excalidraw-diagram**
   - Save as PNG files with descriptive names
   - Use high resolution (300 DPI / 2x scale)
2. Create the deck using **pptx** or **skywork-ppt**
   - Reference the generated images
   - Position diagrams with appropriate sizing
3. Verify: Open the .pptx or HTML and check that diagrams render correctly

### Pattern 2: Research + Content + Deck

When building a deck from a topic (not existing content):

1. Research using **Tavily** web search if available (Azure docs, best practices, latest updates)
2. Synthesize into a clear narrative arc:
   - Problem / Challenge
   - Solution Overview
   - Architecture Deep-Dive
   - Implementation Path
   - Benefits / ROI
3. Generate appropriate visuals
4. Assemble into the final deck

### Pattern 3: Template + Content Fill

When filling a provided template:

1. Analyze the template structure (layouts, placeholders, style)
2. If content needs research, do that first
3. Generate any needed diagrams
4. Fill the template, matching its style language
5. Verify nothing is broken

## MCP Integration

When these MCP servers are available, leverage them:

- **Tavily**: Research Azure services, pricing, best practices, case studies before
  building content. Especially useful for customer demos where you need current
  information.
- **Figma**: If the user has design specs in Figma, use `get_design_context` to extract
  visual specifications and maintain design consistency.
- **Pencil**: For quick UI mockups and wireframes that need to go into the presentation.
- **Playwright**: For capturing screenshots of live Azure portal, dashboards, or web
  apps to embed in slides.

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

- **Lead with the customer's problem**, not Azure features. Architecture slides should
  answer "why this design?" not just "what services are used."
- **Use progressive disclosure** in architecture diagrams — start simple, add layers.
  Don't dump a full architecture on slide 2.
- **Include decision rationale** — why CosmosDB over SQL? Why Event Hub over Service Bus?
  CSA credibility comes from showing you understand trade-offs.
- **Reference Well-Architected Framework pillars** when relevant — reliability, security,
  cost optimization, operational excellence, performance efficiency.
- **For workshops**: Include "try it yourself" moments with clear instructions. Screenshot
  the Azure Portal steps if possible (Playwright MCP can help here).
