# Template Fill Workflow

This is one of the most common CSA scenarios: you receive a .pptx template from an event
organizer, HR, or a customer, and need to fill it with your content while preserving the
template's visual identity.

## Tool Selection

| Template Complexity | Tool | Why |
|-------------------|------|-----|
| Simple text placeholders | **skywork-ppt** (workflow_imitate.md) | Fast, preserves layouts well |
| Complex custom layouts | **pptx** (OOXML) | Full control over XML structure |
| Template with strict brand guidelines | **pptx** (OOXML) | Can precisely match colors, fonts, spacing |

## Step-by-Step

### 1. Analyze the Template

Before filling anything, understand the template structure:

```
Read the template using skywork-ppt's analyze_template.py or pptx's inventory.py:
- How many slide layouts are available?
- What placeholders exist (title, content, image, etc.)?
- What's the color scheme?
- What fonts are used?
- Are there any special elements (logos, footers, slide numbers)?
```

### 2. Map Content to Layouts

For each piece of content you need to add:
- Identify which template layout fits best
- Don't fight the template — adapt your content to its structure
- If you have 20 bullet points and the template has a "3 key points" layout,
  restructure to 3 key points with sub-items

### 3. Handle Images and Diagrams

When embedding architecture diagrams into a template:
- Match the diagram's color scheme to the template's accent colors
- Generate diagrams at the right aspect ratio for the template's image placeholders
- Use transparent backgrounds when the template has colored slide backgrounds

### 4. Fill the Template

Using **skywork-ppt** (simple fills):
- Use `workflow_imitate.md` which analyzes the template and generates matching content
- Provide your content outline and let it map to available layouts

Using **pptx** (complex fills):
- Unpack the template with `ooxml/scripts/unpack.py`
- Inspect the XML structure to understand placeholder IDs
- Fill placeholders while preserving all formatting attributes
- Repack with `ooxml/scripts/pack.py`

### 5. Verify Template Integrity

After filling:
- Open the .pptx and verify:
  - Master slides are unchanged
  - Color scheme is preserved
  - Fonts render correctly (especially Chinese characters)
  - Logos and branding elements are intact
  - Slide numbers and footers work
  - No broken layouts or overflow text

## Common Template Sources

### AI Tour / Microsoft Events
- Usually provide branded templates with specific layouts
- Follow the event's content guidelines strictly
- Often have required legal/disclaimer slides — don't remove them

### HR / Internal
- Company templates with logo, color scheme, disclaimer footer
- Usually more flexible on content layout
- Still respect the brand guidelines

### Customer-Provided
- Match their visual language as a sign of respect
- Pay extra attention to logo placement and sizing
- Verify you're using the latest version of their template

## Troubleshooting

**Chinese characters show as boxes**: The template's embedded fonts may not support CJK.
Use pptx (OOXML) to set font-family fallbacks, or switch to frontend-slides (HTML) for
Chinese-heavy content.

**Images are stretched/distorted**: Check the placeholder's aspect ratio before generating
diagrams. Generate at the matching ratio.

**Text overflows placeholder**: Reduce content or font size. Don't let text clip — it
looks unprofessional. Consider splitting across multiple slides.
