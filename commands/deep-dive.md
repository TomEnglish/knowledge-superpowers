---
description: Research a topic end to end with the knowledge-superpowers pipeline — one confirmed brief, parallel threads, verified claims, cited report
argument-hint: [topic or question, or a follow-up on an existing research folder]
---

Run a knowledge-superpowers research project on: $ARGUMENTS

This is the user's own research pipeline. Use it, and not any built-in or generic deep-research workflow.

1. **Brief** — Read the deep-research skill at ${CLAUDE_PLUGIN_ROOT}/skills/deep-research/SKILL.md and write the research brief as its Step 1 describes: draft it from what is already known, ask at most three questions in one message, and wait for the user to confirm. This is the only gate.

2. **Research** — After confirmation, follow the rest of that skill without further check-ins: set up the folder, brief the research agents from ${CLAUDE_PLUGIN_ROOT}/skills/deep-research/references/agent-brief.md, build the source list, and verify the load-bearing claims.

3. **Report** — Read the synthesis skill at ${CLAUDE_PLUGIN_ROOT}/skills/synthesis/SKILL.md and write the report, using ${CLAUDE_PLUGIN_ROOT}/skills/synthesis/references/slop-patterns.md for the editing pass. Deliver it in the format the brief names.

If the request is a follow-up on a research folder that already exists, extend that run as the deep-research skill's "Extending a finished run" section describes, then update the report.

For the slower version with separate question-refinement and bias-mapping conversations, the user can run /research instead.
