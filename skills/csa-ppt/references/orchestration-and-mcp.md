# Orchestration Patterns & MCP Integration

> **Prerequisites**: All orchestration patterns MUST follow the **Three Inviolable Rules** from SKILL.md:
> Rule 1 (CLARIFY-BEFORE-PLAN), Rule 2 (FILE-FIRST — workspace at `outputs/{project}/`),
> Rule 3 (UPDATE-AFTER-EVERY-TASK — mark `[x]` in task_plan.md after each step).

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

- **Tavily**: Research cloud services (Azure, AWS, GCP), pricing, best practices,
  case studies before building content. Especially useful for customer demos where
  you need current information. Write results to `findings.md`.
- **Figma**: If the user has design specs in Figma, use `get_design_context` to extract
  visual specifications and maintain design consistency.
- **Pencil**: For quick UI mockups and wireframes that need to go into the presentation.
- **Playwright**: For capturing screenshots of live cloud portals, dashboards, or web
  apps to embed in slides. Save screenshots to `diagrams/`.

## Error Recovery Patterns

When an agent fails, the orchestrator must handle the error gracefully. Each agent writes
errors to `{workspace_path}/progress.md` with `[ERROR]` prefix. The orchestrator should
check `progress.md` after each agent completes.

### Diagram Agent Failure → Slide Builder Impact

If the Diagram Agent fails to generate one or more diagrams:

1. **Check `diagrams/manifest.md`** for `[FAILED]` entries
2. **Decide per-diagram**:
   - Diagram is critical (e.g., main architecture) → **retry once** with simplified parameters
   - Diagram is supplementary → **continue without it**, instruct Slide Builder to use text-only layout
3. **Slide Builder instructions**: Pass `missing_diagrams: [list]` in the prompt so it knows
   which diagram references to skip and uses placeholder text instead
4. **Do NOT block the entire pipeline** for a non-critical diagram failure

### Research Agent Failure → Content Impact

If the Research Agent cannot find information for some topics:

1. **Check `findings.md`** for `[NOT_FOUND]` or `[INCOMPLETE]` markers
2. **For incomplete topics**: Proceed with available information, mark those slides as
   needing manual review in `task_plan.md`
3. **For fully missing topics**: Ask the user whether to skip those slides or provide
   the content manually

### Slide Builder Failure → Assembly Impact

If one or more Slide Builders fail:

1. **Check `slides/manifest.md`** for missing entries
2. **Retry the failed slides** (one retry per slide)
3. **If retry fails**: Try a different tool chain as fallback (e.g., switch from
   html2pptx to skywork-ppt for that specific slide)
4. **If still failing**: Assemble partial deck from successful slides, note gaps in
   `assembly-report.md`, and inform the user

### Assembly Agent Abort

If the Assembly Agent aborts (e.g., slides/ is empty):

1. **Do NOT retry Assembly** — the problem is upstream (Phase 3)
2. **Check which Slide Builder tasks are incomplete** in `task_plan.md`
3. **Re-dispatch Slide Builders** for missing slides
4. **Re-run Step 6 gate check** before re-invoking Assembly

### Review Agent Failure

If the Review Agent cannot read the assembled deck:

1. **Check if the file is corrupt** — try opening it with the relevant tool
2. **If corrupt**: Re-invoke Assembly Agent to rebuild from individual slides
3. **If the file is fine but unzip fails** (for .pptx): Suggest alternative review
   approach (e.g., extract text with `python -m markitdown` for content review, skip
   XML-level style inspection)

### General Recovery Principles

- **Never retry more than once** per agent per failure. Two failures = escalate to user.
- **Always check `progress.md`** for `[ERROR]` entries before starting the next phase.
- **Partial results are acceptable** — deliver what works, document what's missing.
- **Prefer fallback tool chains** over complete failure (e.g., simpler diagram style,
  different slide generation method).

## Tips for CSA Presentations

- **Lead with the customer's problem**, not cloud features. Architecture slides should
  answer "why this design?" not just "what services are used."
- **Use progressive disclosure** in architecture diagrams — start simple, add layers.
  Don't dump a full architecture on slide 2.
- **Include decision rationale** — why CosmosDB over DynamoDB? Why Event Hub over
  Kinesis? CSA credibility comes from showing you understand trade-offs.
- **Reference Well-Architected Framework pillars** when relevant (Azure WAF, AWS WAF,
  GCP Architecture Framework) — reliability, security, cost optimization, operational
  excellence, performance efficiency.
- **For workshops**: Include "try it yourself" moments with clear instructions. Screenshot
  the cloud portal steps if possible (Playwright MCP can help here).
