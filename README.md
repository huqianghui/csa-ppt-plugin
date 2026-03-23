# CSA PPT Plugin

All-in-one presentation toolkit for **Azure Cloud Solution Architects**, built for Claude Code.

## What's Inside

### Skills

| Skill | Description |
|-------|-------------|
| **csa-ppt** | Smart orchestrator — analyzes your request and routes to the best tool chain |
| **azure-diagrams** | 700+ Azure icons, architecture diagrams, swimlane flows, ERDs, timelines |
| **excalidraw-diagram** | Hand-drawn style diagrams for brainstorming and conceptual visuals |
| **frontend-slides** | Zero-dependency HTML presentations, great for Chinese content and code |
| **pptx** | Full OOXML-level PowerPoint creation and editing |
| **skywork-ppt** | Quick PowerPoint generation, template-based creation, and slide operations |
| **planning-with-files** | Task planning with file-based progress tracking for multi-slide decks |

### Sub-Agents

The orchestrator dispatches specialized sub-agents for each phase of the workflow:

| Agent | Phase | Role |
|-------|-------|------|
| **Research Agent** | Phase 1 | Gathers Azure docs, features, case studies, and industry context |
| **Diagram Agent** | Phase 2 | Generates architecture diagrams and technical visuals |
| **Slide Builder Agent** | Phase 3 | Builds individual slides per the Style Contract (parallelizable) |
| **Assembly Agent** | Phase 4 | Merges slides + diagrams into final deck |
| **Review Agent** | Phase 5 | Quality review across 7 dimensions, max 2 rounds |
| **Fix Agent** | Phase 5 | Applies targeted fixes from the review report |

### Workflow

```
Plan → Style Contract → Research → Diagrams → Slides → Assembly → Review → Fix → Deliver
```

Each presentation follows a **5-phase workflow**:

1. **Plan** — Break the deck into tasks (one per slide/chapter)
2. **Define Style** — Lock colors, fonts, layout rules into a Style Contract
3. **Execute** — Build slides (parallel sub-agents for large decks)
4. **Assemble** — Combine into final .pptx or HTML
5. **Review & Fix** — Quality check + fix loop (max 2 rounds)

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
3. Dispatch research, diagram, and slide-builder agents
4. Review the assembled deck for quality
5. Apply fixes and deliver

## Prerequisites

- Python 3.8+ with `python-pptx` (for skywork-ppt and azure-diagrams)
- Node.js (for pptx html2pptx conversion)
- `graphviz` system package (for azure-diagrams)
- `diagrams` and `matplotlib` Python libraries (for azure-diagrams)

## License

MIT
