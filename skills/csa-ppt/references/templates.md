# Planning Templates

Use these templates when initializing a presentation workspace.

## Task Plan Template (`task_plan.md`)

```markdown
## Goal
[One-sentence summary of the presentation goal, audience, and scope]

## Style Contract
- **Color palette**: [Primary], [Background], [Surface], [Accent]
- **Font**: [Heading font] (headings), [Body font] (body), [Code font] (code)
- **Language**: [Primary language]
- **Layout rules**: Max [N] lines per slide, max [N] words per bullet
- **Diagram style**: [Icon set, color coding conventions]
- **Output format**: [Tool chain: pptx-html2pptx / pptx-ooxml / frontend-slides / skywork-ppt]

## Phases

### Phase 1: Research & Content Preparation
**Status:** pending
- [ ] [Research topic 1]
- [ ] [Research topic 2]
- [ ] Save findings to findings.md

### Phase 2: Diagram Generation
**Status:** pending
- [ ] [Diagram 1 name and type]
- [ ] [Diagram 2 name and type]

### Phase 3: Slide-by-Slide Creation
**Status:** pending
- [ ] Slide 1: [Title]
- [ ] Slide 2: [Title]
- [ ] ...

### Phase 4: Assembly
**Status:** pending
- [ ] Assemble all slides into final deck
- [ ] Add speaker notes
- [ ] Verify file opens correctly

### Phase 5: Review & Fix (max 2 rounds)
**Status:** pending
- [ ] Round 1: Spawn review agent → review_report.md
- [ ] Apply Round 1 fixes (if any)
- [ ] Round 2: Verify fixes → final review_report.md
- [ ] Deliver with any KNOWN_ISSUES documented
```

### Lightweight Variant (< 5 slides)

For simple requests, merge the task plan and style contract into a single file. Skip
Phase 1 (research) and Phase 5 (formal review) — do a quick self-check instead.

```markdown
## Goal
[One-sentence summary]

## Style
- Colors: [Primary] / [Background] / [Accent]
- Font: [Heading] / [Body]
- Language: [Language]
- Output: [Format]

## Slides
- [ ] Slide 1: [Title]
- [ ] Slide 2: [Title]
- [ ] Slide 3: [Title]
- [ ] Assembly & self-check
```

## Style Contract Template (`style_contract.md`)

For 5+ slide decks, write this as a standalone file so every sub-agent can read it
directly without parsing task_plan.md.

```markdown
# Style Contract

## Colors
- Primary: #0078D4 (Azure Blue)
- Background: #1B1B1B (Dark) or #FFFFFF (Light)
- Surface: #F5F5F5 (Light Gray)
- Accent: #50E6FF (Cyan)
- Text: #FFFFFF on dark, #1B1B1B on light

## Fonts
- Headings: Arial, 28pt
- Body: Segoe UI, 16pt
- Code: Consolas, 14pt

## Language
- Primary: Chinese (中文) / English / Mixed
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
- Tool chain: [pptx-html2pptx / pptx-ooxml / frontend-slides / skywork-ppt]
- Image resolution: 300 DPI / 2x scale
```

## Example: 10-Slide Customer Demo Plan

A concrete example combining the templates above:

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
