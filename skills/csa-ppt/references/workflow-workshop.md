# Workshop / Hands-on Lab Workflow

Workshop materials need to be action-oriented with clear step-by-step instructions.
Participants follow along on their own machines.

## Recommended Tool Chain

- **Format**: HTML (frontend-slides) — best for code blocks, interactive elements, and
  step-by-step navigation
- **Diagrams**: azure-diagrams for architecture overview, Playwright for Azure Portal
  screenshots
- **Fallback**: .pptx via skywork-ppt if the organizer requires PowerPoint format

## Why HTML is Best for Workshops

- Syntax-highlighted code blocks that participants can read easily
- No font issues with monospace code
- Participants can open the HTML locally and follow along at their own pace
- Responsive — works on different screen sizes
- Can include embedded links to Azure Portal, documentation, GitHub repos

## Typical Structure

```
Slide 1:  Workshop Title + Prerequisites
Slide 2:  What We'll Build Today (architecture overview diagram)
Slide 3:  Environment Setup
          - Azure subscription requirements
          - Tools to install
          - Pre-configured resources
Slide 4:  Lab 1 — [Foundation Step]
          - Goal
          - Step-by-step instructions with screenshots
          - Verification: "You should see..."
Slide 5-N: Lab 2-N — [Additional Steps]
          - Same pattern as Lab 1
          - Each lab builds on the previous
Slide N+1: Architecture Review (show what they've built)
Slide N+2: Cleanup Instructions
Slide N+3: Next Steps & Resources
```

## Key Principles

- **Every step should be verifiable** — include "you should see X" checkpoints
- **Include the Azure Portal path** — e.g., "Navigate to Resource Groups > myRG > myApp"
- **Screenshot key screens** — use Playwright MCP to capture Azure Portal if available
- **Provide escape hatches** — "If step 3 failed, run this script to catch up"
- **Estimate timing** — "This lab takes approximately 15 minutes"
- **Mark optional sections** — advanced content shouldn't block beginners
