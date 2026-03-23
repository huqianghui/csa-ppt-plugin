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

This skill orchestrates 5 specialized sub-skills plus MCP integrations. Your job is to
analyze the request, pick the right tool chain, and deliver a polished result. For simple
requests, decide automatically. For complex or ambiguous ones, briefly present the
recommended approach and confirm before proceeding.

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

These paths are relative to the project root:

| Skill | Path | When to Read |
|-------|------|-------------|
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
