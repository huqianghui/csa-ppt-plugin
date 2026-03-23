# Customer Solution Demo Workflow

A customer demo deck typically needs to be professional, visually polished, and tell a
compelling story about how Azure solves the customer's specific problem.

## Recommended Tool Chain

- **Format**: .pptx (customers expect PowerPoint files they can share internally)
- **Diagrams**: azure-diagrams for architecture, excalidraw for conceptual flows
- **Deck creation**: pptx (html2pptx for rich layouts) or skywork-ppt (template-based)
- **Research**: Tavily for latest Azure updates, pricing, case studies

## Step-by-Step

### 1. Understand the Customer Context

Before creating anything, clarify:
- What problem is the customer trying to solve?
- What's their current infrastructure? (on-prem, hybrid, multi-cloud?)
- What Azure services are they already using?
- What's their decision timeline?
- Who is the audience? (technical vs. executive)

### 2. Research Phase

If Tavily MCP is available:
- Search for relevant Azure reference architectures
- Find recent case studies in the customer's industry
- Check latest pricing and SKU information
- Look for any recent service announcements that might be relevant

### 3. Narrative Structure

Follow this proven CSA demo structure:

```
Slide 1:  Title + Customer Name
Slide 2:  Agenda / What We'll Cover
Slide 3:  Understanding Your Challenges (customer's pain points)
Slide 4:  Solution Overview (high-level, one-sentence value prop)
Slide 5:  Architecture Overview (simplified diagram)
Slide 6-8: Architecture Deep-Dive (layer by layer)
Slide 9:  Security & Compliance
Slide 10: Cost Estimation / Optimization
Slide 11: Migration / Implementation Roadmap
Slide 12: Why Azure (competitive differentiators)
Slide 13: Next Steps
Slide 14: Q&A / Contact
```

Adjust based on the audience:
- **Executive audience**: More business value, fewer technical details, add ROI slide
- **Technical audience**: More architecture depth, include code samples, add demo links
- **Mixed audience**: Use appendix slides for technical depth

### 4. Generate Architecture Diagrams

Use **azure-diagrams** skill. Key guidelines:
- Create a simplified overview diagram first (3-5 key services)
- Then create detailed diagrams for each layer/component
- Use consistent color coding:
  - Blue: compute/application layer
  - Green: data/storage layer
  - Orange: networking/security
  - Purple: AI/ML services
- Always include data flow arrows with labels
- Include the Well-Architected Framework badge if relevant

### 5. Assemble the Deck

If using a template:
- Read `workflow-template-fill.md` for template handling
- Match diagram colors to the template's accent colors

If creating from scratch:
- Use clean, professional layout
- Azure blue (#0078D4) as primary accent
- White/light gray backgrounds
- Minimal text per slide (6 lines max, 6 words per line)

### 6. Review & Polish

- Verify all Azure service names are spelled correctly
- Check that pricing information is current
- Ensure architecture diagrams are legible at presentation resolution
- Add speaker notes for each slide with talking points
- Include backup/appendix slides for anticipated questions
