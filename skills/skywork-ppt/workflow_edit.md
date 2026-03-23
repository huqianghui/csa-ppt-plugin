# Local PPT Edit Workflow

Use this workflow to modify an existing local `.pptx`.

The edit path is deterministic and local:

1. inspect the presentation
2. build an edit plan JSON
3. apply the plan with `run_ppt_write.py --mode edit`

## 1. Inspect the current deck

Get slide count and titles:

```bash
$PYTHON_CMD scripts/local_pptx_ops.py info --file /absolute/path/input.pptx
```

If you need more text context, extract slide text:

```bash
$PYTHON_CMD scripts/parse_file.py /absolute/path/input.pptx -o /tmp/input.txt
```

## 2. Build a local edit plan

Supported actions in the JSON plan:

- `update_text`
- `append_slide`
- `delete_slide`
- `reorder_slides`

Example edit plan:

```json
{
  "edits": [
    {
      "action": "update_text",
      "slide": 2,
      "title": "Updated Overview",
      "bullets": [
        "Current position",
        "Key risks",
        "Recommended action"
      ]
    },
    {
      "action": "append_slide",
      "type": "bullets",
      "title": "Next Steps",
      "bullets": [
        "Finalize scope",
        "Assign owners",
        "Track delivery milestones"
      ]
    }
  ]
}
```

Save the plan to a local file such as `/tmp/edit-plan.json`.

## 3. Apply the edit plan

```bash
$PYTHON_CMD scripts/run_ppt_write.py \
  --mode edit \
  --pptx-file /absolute/path/input.pptx \
  --edit-plan-file /tmp/edit-plan.json \
  -o /absolute/path/output.pptx
```

If you already have the edit JSON inline, you can pass it directly:

```bash
$PYTHON_CMD scripts/run_ppt_write.py \
  --mode edit \
  --pptx-file /absolute/path/input.pptx \
  --edit-plan '{"edits":[{"action":"delete_slide","slide":3}]}' \
  -o /absolute/path/output.pptx
```

## 4. Output interpretation

On success the script prints:

- `RESULT: success`
- `MODE: edit`
- `OUTPUT_FILE: ...`
- `SLIDE_COUNT: ...`
- `SUMMARY: [...]`

Deliver:

1. the output path
2. the applied change summary
3. any follow-up edits still needed

## Notes

- The edit flow is local-file based only.
- There is no URL upload step.
- Slide references are 1-based in the edit plan.
- Reorder plans must include every slide exactly once.