# CSA PPT Plugin

All-in-one presentation toolkit for **Azure Cloud Solution Architects**, built for Claude Code.

## What's Inside

| Skill | Description |
|-------|-------------|
| **csa-ppt** | Smart orchestrator — analyzes your request and routes to the best tool chain |
| **azure-diagrams** | 700+ Azure icons, architecture diagrams, swimlane flows, ERDs, timelines |
| **excalidraw-diagram** | Hand-drawn style diagrams for brainstorming and conceptual visuals |
| **frontend-slides** | Zero-dependency HTML presentations, great for Chinese content and code |
| **pptx** | Full OOXML-level PowerPoint creation and editing |
| **skywork-ppt** | Quick PowerPoint generation, template-based creation, and slide operations |

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
3. Generate diagrams, slides, and presentations

## Prerequisites

- Python 3.8+ with `python-pptx` (for skywork-ppt and azure-diagrams)
- Node.js (for pptx html2pptx conversion)
- `graphviz` system package (for azure-diagrams)
- `diagrams` and `matplotlib` Python libraries (for azure-diagrams)

## License

MIT
