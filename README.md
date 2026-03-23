# CSA PPT Plugin

All-in-one presentation toolkit for **Cloud Solution Architects** (Azure / AWS / GCP), built for Claude Code.

## What's Inside

### Skills (1 orchestrator + 5 sub-skills + 1 utility)

| Skill | Description |
|-------|-------------|
| **csa-ppt** | Smart orchestrator — analyzes your request and routes to the best tool chain |
| **azure-diagrams** | 700+ cloud icons (Azure/AWS/GCP), architecture diagrams, swimlane flows, ERDs, timelines |
| **excalidraw-diagram** | Hand-drawn style diagrams for brainstorming and conceptual visuals |
| **frontend-slides** | Zero-dependency HTML presentations, great for Chinese content and code |
| **pptx** | Full OOXML-level PowerPoint creation and editing |
| **skywork-ppt** | Quick PowerPoint generation, template-based creation, and slide operations |
| **planning-with-files** | Task planning with file-based progress tracking for multi-slide decks |

### Sub-Agents (6 agents)

The orchestrator **按需调度** sub-agents — not every agent is used every time. The orchestrator
decides based on deck size and complexity:

| Agent | Phase | Role | When Dispatched |
|-------|-------|------|-----------------|
| **Research Agent** | Phase 1 | Gathers cloud docs (Azure/AWS/GCP), features, case studies, industry context | Topics need web research |
| **Diagram Agent** | Phase 2 | Generates architecture diagrams and technical visuals | Deck includes architecture diagrams |
| **Slide Builder Agent** | Phase 3 | Builds individual slides, smart format selection per slide (parallelizable) | Large decks (10+ slides) |
| **Assembly Agent** | Phase 4 | Normalizes mixed formats + merges slides + diagrams into final deck | Multiple builders produced separate files |
| **Review Agent** | Phase 5 | Quality review across 7 dimensions, max 2 rounds | Always for 5+ slide decks |
| **Fix Agent** | Phase 5 | Applies targeted fixes from the review report | Review found issues |

**Dispatch strategy by deck size:**

| Deck Size | Orchestrator Does | Sub-Agents Handle |
|-----------|-------------------|-------------------|
| Small (< 5 slides) | Everything directly, quick self-check | — |
| Medium (5–10 slides) | Phase 1, 2, 4 | Slide Builder (Phase 3), Review + Fix (Phase 5) |
| Large (10+ slides) | Coordination only | All 6 agents, Slide Builders run in parallel |

### Workflow

```
Plan → Style Contract → Research → Diagrams → Slides → Assembly → Review → Fix → Deliver
                         Phase 1    Phase 2    Phase 3   Phase 4    Phase 5
```

Each presentation follows a **5-phase workflow**:

1. **Plan** — Break the deck into tasks (one per slide/chapter)
2. **Define Style** — Lock colors, fonts, layout rules into a Style Contract
3. **Execute** — Research + diagrams + slides (parallel where possible)
4. **Assemble** — Normalize mixed intermediate formats + combine into final .pptx or HTML
5. **Review & Fix** — Independent quality check + fix loop (max 2 rounds)

### Smart Intermediate Format Selection

Slide Builder Agents **choose the best intermediate format per-slide** based on content — not
forced to match the final output format:

| Content | Intermediate Format | Why |
|---------|-------------------|-----|
| Simple bullets, English content | `.pptx` (python-pptx) | Direct, no conversion overhead |
| Diagram-only slides | `.pptx` (python-pptx) | Simple image embed |
| Chinese-heavy (中文为主) | `.html` | Better CJK font rendering |
| Code blocks with syntax highlighting | `.html` | Native code rendering |
| Complex multi-column layouts | `.html` | CSS flexbox/grid flexibility |

The Assembly Agent handles the format mix — normalizing all slides to the target format
before merging into the final deck.

## Supported Scenarios

- **Customer Solution Demos** — Architecture diagrams + polished .pptx decks
- **Internal Tech Sharing** — HTML slides with code syntax highlighting
- **Workshops / Hands-on Labs** — Step-by-step interactive presentations
- **Architecture Reviews (CAF/WAF/Well-Architected)** — Assessment decks with as-is/to-be diagrams
- **Template Filling** — Fill company/event templates while preserving branding

## Installation

### Add the marketplace and install:

```bash
/plugin marketplace add huqianghui/csa-ppt-plugin
/plugin install csa-ppt@csa-skills
```

### Or load directly for testing:

```bash
claude --plugin-dir /path/to/csa-ppt-plugin
```

## Usage

Just describe what you need in natural language:

- "帮我做一个给客户演示Azure RAG方案的PPT"
- "Create an AWS to Azure migration comparison deck in English"
- "做一个内部AKS迁移到ACA的技术分享，中文，HTML格式"
- "用这个模板帮我填写季度工作汇报"
- "画一个Azure Landing Zone的架构图"

The **csa-ppt** skill will automatically:
1. Analyze your request (content type, language, format)
2. Initialize a file-based workspace (`outputs/{project}/`)
3. Choose the best tool chain and intermediate format per slide
4. Dispatch sub-agents as needed based on deck size
5. Assemble, normalizing any mixed intermediate formats
6. Review the assembled deck for quality and apply fixes

### Workspace — Intermediate Outputs You Can Inspect

Every presentation creates a workspace folder under `outputs/`. All intermediate files are
written to disk so you can **review, edit, or adjust** them at any point before the final
deck is assembled.

```
outputs/{project}/
├── task_plan.md              ← Slide plan with checkboxes — edit to reorder/add/remove slides
├── progress.md               ← Session log — see what's been done and what's next
├── style_contract.md         ← Colors, fonts, layout rules — edit to change the look
├── findings.md               ← Research results — review before slides are built
├── diagrams/
│   ├── manifest.md           ← List of generated diagrams
│   ├── rag-architecture.png  ← Architecture diagram — open to preview
│   └── data-pipeline.png     ← Flow diagram — replace with your own if needed
├── slides/
│   ├── manifest.md           ← Per-slide format (pptx/html) and status
│   ├── slide-1.pptx          ← Individual slide — open in PowerPoint to check
│   ├── slide-1-notes.md      ← Speaker notes — edit to refine talking points
│   ├── slide-2.html          ← HTML slide — open in browser to preview
│   └── ...
└── final/
    ├── final-deck.pptx       ← Assembled deck — the deliverable
    ├── assembly-report.md    ← What was merged, format conversions applied
    ├── review_report.md      ← Quality review results (per-slide PASS/FIX)
    └── fix_summary.md        ← What was fixed after review
```

**How to use this during creation:**

- **Adjust the plan** — Edit `task_plan.md` to add/remove/reorder slides before Phase 3
- **Change the style** — Edit `style_contract.md` to change colors or fonts before slides are built
- **Review research** — Read `findings.md` to verify the content before it goes into slides
- **Preview individual slides** — Open `.pptx` files in PowerPoint or `.html` files in a browser
- **Replace diagrams** — Drop your own `.png` files into `diagrams/` and update `manifest.md`
- **Edit speaker notes** — Modify any `slide-{N}-notes.md` before assembly
- **Check review results** — Read `review_report.md` to see what the Review Agent flagged

All changes you make to intermediate files will be picked up by the next phase.

## Project Structure

```
csa-ppt-plugin/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   └── marketplace.json         # Marketplace registration
├── skills/
│   ├── csa-ppt/                 # Main orchestrator
│   │   ├── SKILL.md             # Routing logic, workflow, Style Contract
│   │   ├── agents/              # 6 specialized sub-agents
│   │   │   ├── research-agent.md
│   │   │   ├── diagram-agent.md
│   │   │   ├── slide-builder-agent.md
│   │   │   ├── assembly-agent.md
│   │   │   ├── review-agent.md
│   │   │   └── fix-agent.md
│   │   ├── references/          # Workflow guides per scenario
│   │   │   ├── templates.md
│   │   │   ├── orchestration-and-mcp.md
│   │   │   ├── workflow-customer-demo.md
│   │   │   ├── workflow-tech-sharing.md
│   │   │   ├── workflow-workshop.md
│   │   │   ├── workflow-architecture-review.md
│   │   │   └── workflow-template-fill.md
│   │   └── evals/               # Skill evaluation test cases
│   │       └── evals.json
│   ├── azure-diagrams/          # 700+ Azure icons, diagram scripts
│   ├── excalidraw-diagram/      # Hand-drawn style diagrams
│   ├── frontend-slides/         # HTML presentations
│   ├── pptx/                    # OOXML PowerPoint creation
│   ├── skywork-ppt/             # Quick PPT generation
│   └── planning-with-files/     # Task planning system
└── README.md
```

## Prerequisites

- Python 3.8+ with `python-pptx` (for skywork-ppt and azure-diagrams)
- Node.js (for pptx html2pptx conversion)
- `graphviz` system package (for azure-diagrams)
- `diagrams` and `matplotlib` Python libraries (for azure-diagrams)

## License

MIT
