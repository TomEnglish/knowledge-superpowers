---
description: Launch the full knowledge-superpowers research pipeline, with separate question-refinement and bias-mapping stages
argument-hint: [topic or question]
---

Start a knowledge-superpowers deep research session on: $ARGUMENTS

This is the user's own research pipeline. Use it, and not any built-in or generic deep-research workflow. For the faster single-gate version, the user can run /deep-dive instead.

Follow this pipeline in order:

1. **Articulate** — Read the articulate skill at ${CLAUDE_PLUGIN_ROOT}/skills/articulate/SKILL.md and follow its process to refine the research question with the user. Do not skip this even if the topic seems clear.

2. **Blind Variables** — Once the question is confirmed, read the blind-variables skill at ${CLAUDE_PLUGIN_ROOT}/skills/blind-variables/SKILL.md and produce a bias map for the confirmed question. Reference ${CLAUDE_PLUGIN_ROOT}/skills/blind-variables/references/distortion-examples.md for domain-specific patterns.

3. **Deep Research** — Read the deep-research skill at ${CLAUDE_PLUGIN_ROOT}/skills/deep-research/SKILL.md and execute it. Its research brief takes the confirmed question and bias map from stages 1 and 2 and adds the user's situation, the deliverable and the threads. Brief the research agents from ${CLAUDE_PLUGIN_ROOT}/skills/deep-research/references/agent-brief.md. Reference ${CLAUDE_PLUGIN_ROOT}/skills/deep-research/references/context-hygiene.md for long sessions.

4. **Synthesis** — Read the synthesis skill at ${CLAUDE_PLUGIN_ROOT}/skills/synthesis/SKILL.md and consolidate findings into a final report. Reference ${CLAUDE_PLUGIN_ROOT}/skills/synthesis/references/slop-patterns.md during the editing pass.

Get user confirmation at the end of stages 1 and 2 and on the research brief in stage 3. After the brief is confirmed, run research and synthesis through to the report.
