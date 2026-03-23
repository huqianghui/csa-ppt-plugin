# Internal Tech Sharing Workflow

Internal tech talks, brown bags, and deep-dives are less formal but still need clear
structure and good visuals. The audience is usually technical colleagues.

## Recommended Tool Chain

- **Format**: HTML (frontend-slides) for interactive feel, or .pptx for recording/sharing
- **Diagrams**: azure-diagrams for architecture, excalidraw for conceptual/whiteboard style
- **Chinese content**: Strongly prefer frontend-slides (HTML) to avoid encoding issues

## When to Use HTML vs PPTX

Choose **HTML (frontend-slides)** when:
- Heavy Chinese text content
- You want code syntax highlighting
- Interactive elements (expand/collapse, tabs)
- Animation and transitions matter
- The talk will be delivered live from your own laptop

Choose **PPTX** when:
- Need to share the file for others to present
- Recording for async viewing (some recording tools prefer .pptx)
- Need to add to a shared slide library
- The audience needs to edit/remix your slides

## Typical Structure

```
Slide 1:  Title + Your Name + Date
Slide 2:  Background / Why This Topic
Slide 3:  Key Concepts (keep it to 3-5)
Slide 4-8: Technical Deep-Dive
          - Architecture diagrams
          - Code snippets
          - Demo screenshots
Slide 9:  Lessons Learned / Gotchas
Slide 10: Resources & Links
Slide 11: Q&A
```

## Tips for Internal Talks

- Be more casual and opinionated — internal audiences appreciate honest takes
- Include "what I tried that didn't work" — it's more educational than just the happy path
- Add live demo links if applicable
- Code snippets should be real, not pseudocode
- For architecture talks, show the evolution: V1 → V2 → current state
