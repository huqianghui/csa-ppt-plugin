# CSA PPT Plugin

All-in-one presentation toolkit for **Azure Cloud Solution Architects**, built for Claude Code.

## What's Inside

### Skills (7 sub-skills)

| Skill | Description |
|-------|-------------|
| **csa-ppt** | Smart orchestrator — analyzes your request and routes to the best tool chain |
| **azure-diagrams** | 700+ Azure icons, architecture diagrams, swimlane flows, ERDs, timelines |
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
| **Research Agent** | Phase 1 | Gathers Azure docs, features, case studies, industry context | Topics need web research |
| **Diagram Agent** | Phase 2 | Generates architecture diagrams and technical visuals | Deck includes architecture diagrams |
| **Slide Builder Agent** | Phase 3 | Builds individual slides per the Style Contract (parallelizable) | Large decks (10+ slides) |
| **Assembly Agent** | Phase 4 | Merges slides + diagrams into final deck | Multiple builders produced separate files |
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
4. **Assemble** — Combine into final .pptx or HTML
5. **Review & Fix** — Independent quality check + fix loop (max 2 rounds)

## Supported Scenarios

- **Customer Solution Demos** — Architecture diagrams + polished .pptx decks
- **Internal Tech Sharing** — HTML slides with code syntax highlighting
- **Workshops / Hands-on Labs** — Step-by-step interactive presentations
- **Architecture Reviews (CAF/WAF)** — Assessment decks with as-is/to-be diagrams
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
- "做一个内部AKS迁移到ACA的技术分享，中文，HTML格式"
- "用这个模板帮我填写季度工作汇报"
- "画一个Azure Landing Zone的架构图"

The **csa-ppt** skill will automatically:
1. Analyze your request (content type, language, format)
2. Choose the best tool chain
3. Dispatch sub-agents as needed based on deck size
4. Review the assembled deck for quality
5. Apply fixes and deliver

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
│   │   └── references/          # Workflow guides per scenario
│   │       ├── workflow-customer-demo.md
│   │       ├── workflow-tech-sharing.md
│   │       ├── workflow-workshop.md
│   │       ├── workflow-architecture-review.md
│   │       └── workflow-template-fill.md
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
