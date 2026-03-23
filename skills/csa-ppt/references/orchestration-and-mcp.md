# Orchestration Patterns & MCP Integration

## Orchestration Patterns

### Pattern 1: Diagrams + Deck (most common)

When the user needs architecture diagrams IN a presentation:

1. **Initialize workspace** first (Step 0 from SKILL.md)
2. Generate diagrams using **azure-diagrams** or **excalidraw-diagram**
   - Save as PNG files to `outputs/{project}/diagrams/`
   - Use high resolution (300 DPI / 2x scale)
3. Create the deck using **pptx** or **skywork-ppt**
   - Reference the generated images from `diagrams/`
   - Position diagrams with appropriate sizing
4. Assemble and verify

### Pattern 2: Research + Content + Deck

When building a deck from a topic (not existing content):

1. **Initialize workspace** — `mkdir -p outputs/{name}/{diagrams,slides,final}`
2. **Write task_plan.md + style_contract.md** to the workspace
3. Research using **Tavily** web search → **write findings.md** to workspace
4. Generate diagrams → **save PNGs to diagrams/** in workspace
5. Build slides using findings.md as input → **save to slides/** in workspace
6. Assemble → **write final deck to final/** in workspace
7. Review → **write review_report.md to final/** in workspace

### Pattern 3: Template + Content Fill

When filling a provided template:

1. **Initialize workspace** with the template file
2. Analyze the template structure (layouts, placeholders, style)
3. If content needs research → write findings.md
4. Generate any needed diagrams → save to diagrams/
5. Fill the template, matching its style language → save to final/
6. Review and verify nothing is broken

## MCP Integration

When these MCP servers are available, leverage them:

- **Tavily**: Research Azure services, pricing, best practices, case studies before
  building content. Especially useful for customer demos where you need current
  information. Write results to `findings.md`.
- **Figma**: If the user has design specs in Figma, use `get_design_context` to extract
  visual specifications and maintain design consistency.
- **Pencil**: For quick UI mockups and wireframes that need to go into the presentation.
- **Playwright**: For capturing screenshots of live Azure portal, dashboards, or web
  apps to embed in slides. Save screenshots to `diagrams/`.

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
