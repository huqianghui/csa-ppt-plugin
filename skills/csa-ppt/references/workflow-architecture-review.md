# Architecture Review (CAF/WAF) Workflow

> **Prerequisites**: Before starting, ensure the **Three Inviolable Rules** from SKILL.md are followed:
> Rule 1 (CLARIFY-BEFORE-PLAN), Rule 2 (FILE-FIRST — create workspace `outputs/{project}/` first),
> Rule 3 (UPDATE-AFTER-EVERY-TASK — mark `[x]` in task_plan.md after each step).

Architecture reviews require structured assessment against Azure's Well-Architected
Framework and Cloud Adoption Framework. The output is usually a mix of diagrams and a
formal assessment deck.

## Recommended Tool Chain

- **Diagrams**: azure-diagrams for current-state and target-state architectures
- **Format**: .pptx for formal deliverable (pptx or skywork-ppt)
- **Research**: Tavily for latest WAF recommendations and Azure best practices

## Well-Architected Framework Pillars

Every architecture review should assess against these five pillars:

1. **Reliability** — Resiliency, availability, disaster recovery
2. **Security** — Identity, network security, data protection
3. **Cost Optimization** — Cost management, right-sizing
4. **Operational Excellence** — Monitoring, automation, DevOps
5. **Performance Efficiency** — Scaling, caching, data optimization

## Typical Deck Structure

```
Slide 1:  Title — "[Customer] Architecture Review"
Slide 2:  Executive Summary (RAG status per pillar)
Slide 3:  Scope & Methodology
Slide 4:  Current Architecture (diagram — as-is state)
Slide 5:  Pillar 1: Reliability Assessment
          - Findings (with severity: High/Medium/Low)
          - Recommendations
Slide 6:  Pillar 2: Security Assessment
Slide 7:  Pillar 3: Cost Optimization
Slide 8:  Pillar 4: Operational Excellence
Slide 9:  Pillar 5: Performance Efficiency
Slide 10: Recommended Target Architecture (diagram — to-be state)
Slide 11: Prioritized Action Plan
Slide 12: Next Steps
```

## Diagram Guidelines for Reviews

Create two key diagrams:

### Current State (As-Is)
- Show all existing Azure services and their connections
- Highlight pain points with red indicators or callouts
- Include region/zone deployment information
- Show data flows with arrows

### Target State (To-Be)
- Show the recommended architecture
- Use green indicators for improvements
- Include new services added
- Show how identified gaps are addressed

### Comparison Approach
Consider placing both diagrams side by side or using a transition diagram
showing the migration path from as-is to to-be.

## Color Coding for Findings

Use consistent RAG (Red/Amber/Green) status:
- **Red**: Critical risk, needs immediate attention
- **Amber**: Moderate risk, should address in near term
- **Green**: Meets best practices, no action needed

## Tips

- Reference specific WAF recommendations with their IDs when possible
- Include Azure Advisor findings if the customer has shared access
- Cost optimization findings should include estimated savings
- For each finding, provide a clear "what to do" not just "what's wrong"
