# Context Hygiene

Guidelines for managing the context window during long research sessions. The core problem: research generates far more text than the model can hold in working memory. Without deliberate management, later sub-topics lose access to earlier findings, quality degrades, and the model starts confabulating connections between things it vaguely remembers.

## Principles

### Files Are Memory

The research files *are* the persistent memory. Write findings to disk immediately. Don't hold them in context hoping to synthesize later. A finding that exists only in the context window is one compaction away from being lost.

### Summaries Are Pointers

After completing each sub-topic, write a 2-3 sentence summary. These summaries serve as pointers — enough information to know what's in the file without needing to re-read it. Keep a running list of these summaries as the research progresses.

### Fresh Agents for Fresh Context

When sub-agents are available, use them. Each sub-agent starts with a clean context window, focused entirely on its sub-topic. This is the most reliable way to ensure each research thread gets full attention rather than competing for context space with other threads.

When sub-agents are not available, work sequentially and write to files between each sub-topic. Mentally treat each sub-topic as a fresh start — re-read the research question and bias map, but don't try to hold all previous findings in mind.

## Strategies by Research Size

### Small Research (3-4 sub-topics, ~30 min)

Context management is minimal. Research can likely complete within a single session without significant context pressure.

- Write findings to files as you go (always do this regardless of size)
- Summarize each sub-topic before moving to the next
- Synthesis can likely work from the files directly

### Medium Research (5-7 sub-topics, ~1-2 hours)

Context pressure becomes real. Later sub-topics will have less context available for earlier findings.

- Use sub-agents if available — one per sub-topic
- If working sequentially, explicitly release earlier context by writing summaries and moving on
- Before synthesis, re-read all sub-topic files to rebuild full context
- Consider doing synthesis in a fresh session/agent

### Large Research (8+ sub-topics, multi-session)

Context management is a primary concern. The research will span multiple sessions or require significant agent coordination.

- Sub-agents are strongly recommended — parallel execution + context isolation
- Maintain a `research-log.md` file that tracks: what's been researched, what's remaining, key cross-topic connections discovered
- The synthesis skill should be invoked in a fresh context with access to all files but no accumulated research context
- Consider breaking the research into phases: first pass (breadth), second pass (depth on key findings), synthesis

## Anti-Patterns

**Holding everything in context**: Trying to keep all findings in working memory leads to degraded quality on later sub-topics and hallucinated connections during synthesis.

**Re-reading everything before each sub-topic**: Wastes context space. Only re-read the research question, bias map, and summaries — not full sub-topic files.

**Synthesizing from memory**: The synthesis skill should work from the files, not from what the research agent remembers about the files. If synthesis happens in the same session as research, re-read the files fresh rather than relying on stale context.

**Skipping git commits**: Each commit is a checkpoint. If something goes wrong during later research, you can see what the earlier findings looked like before they were potentially contaminated by later framing.

**Editing sources.md or rebuilding it from memory**: The source list is built by `scripts/runcheck.py sources` from the thread files. Fix the thread file and rebuild, so the list and the citations cannot drift apart.

**Briefing agents from memory**: In a long session the user's situation and the bias note are the first things to fall out of an improvised brief. Re-read `README.md` and fill the template in `agent-brief.md` each time, including for extension threads added hours later.
