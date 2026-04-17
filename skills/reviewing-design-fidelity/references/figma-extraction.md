# Figma Extraction Tactics

## Choosing which frames to review

A design file may contain dozens of frames; not all are in scope.

- **In scope:** screen-level frames named for user-facing states (e.g., "Cart - Empty", "Cart - 3 items", "Cart - Loading", "Cart - Error")
- **Out of scope:** exploration frames, designer working frames marked with `_wip` or `[draft]` prefix, and component library frames (those belong to design-system review, not feature review)

When in doubt, ask the user which frames are sign-off frames.

## Multi-variant frames

A single frame may use Figma's variant property to encode multiple states (e.g., a Button frame with `state` and `size` variants). Use `get_metadata` to enumerate all variant combinations, then `get_design_context` per variant. Treat each variant as its own implementation target — a button that ships only "default" and "hover" but not "disabled" has a state coverage gap, not a styling gap.

## Code Connect mappings

If `get_code_connect_map` returns a mapping for a frame, the design system has declared the canonical code component for that design. Drift findings against a Code Connect-mapped component are higher severity — the team has explicitly committed that this code = this design.

When Code Connect is present, also verify that the implementation uses the mapped component rather than a one-off rebuild. A custom-built button reproducing the design closely is still a finding if Code Connect points at `<Button variant="primary" />`.

## Token extraction strategy

`get_variable_defs` returns design tokens used by the queried frame. Capture these before measurement so the comparison is "implementation value vs token value" rather than "implementation value vs Figma rendered value". Tokens are the contract; rendered Figma values are the result of applying the contract to a particular frame.

If a frame uses a raw hex code instead of a token, that's itself a design-side finding (file separately under "design issues" in the report).

## URL parsing

Figma URLs:
- `figma.com/design/<fileKey>/<filename>?node-id=<nodeId>` — convert `-` to `:` in nodeId before MCP calls (e.g., `123-456` → `123:456`)
- Branch URLs (`/branch/<branchKey>/`) — use the branchKey as fileKey
