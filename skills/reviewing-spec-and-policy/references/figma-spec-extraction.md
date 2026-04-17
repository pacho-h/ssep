# Extracting Spec Content from Figma

Figma planning files often hide critical spec content in places text-based docs don't. Treat them as a first-class spec source.

## What to extract

### 1. Frame structure
A planning file is usually organized as flow → screens → states. Use `mcp__plugin_figma_figma__get_metadata` first to understand the page/frame hierarchy without pulling full content. This avoids over-loading context with unrelated frames.

### 2. Per-screen acceptance criteria
For each frame relevant to the spec, call `mcp__plugin_figma_figma__get_design_context` with that node ID. Designers commonly annotate screens with:
- Empty state copy
- Error state copy
- Loading behavior notes
- Conditional visibility rules ("show only if X")
- Interaction notes ("tap → navigate to Y")

These are spec content, not design decoration. Pull them into the review.

### 3. Decision pins and comments
Comments on frames often record decisions ("PM confirmed: skip step 2 if user is verified") that never make it into the prose spec. Ask the user to share comment threads if Figma access is limited.

### 4. Variant matrices
Component variants encode state combinations. A button with `state={default,hover,disabled,loading} × size={sm,md,lg}` is a 12-cell behavior matrix. If the spec says "button" without specifying which variants are required, that's a completeness finding.

## URL parsing

Figma URLs follow this pattern:
- `figma.com/design/<fileKey>/<filename>?node-id=<nodeId>`
- Convert `-` to `:` in the nodeId before passing to MCP tools (e.g., `123-456` → `123:456`)

For a planning file URL without a specific node, default to extracting the page-level frames first, then drill into specific flows the user names.

## Practical sequence

1. `get_metadata` → page list, frame names → identify spec-relevant frames
2. `get_design_context` per relevant frame → structured content + annotations
3. `get_screenshot` for any frame whose meaning depends on visual layout (e.g., conditional banner placement)
4. Cross-reference findings against the prose spec — discrepancies between the two are themselves findings
