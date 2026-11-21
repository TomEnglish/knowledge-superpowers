---
name: synthesis
description: >
  This skill should be used after the deep-research skill has completed research and produced
  thread files, a source list and a verification file. It consolidates the research into a
  final report whose every claim can be traced to a source, relates the findings to the
  user's decision when the brief names one, strips AI writing patterns, and delivers the
  report in the format the brief asked for. Also trigger when the user says "pull it
  together", "write the report", "synthesize this", "consolidate my research", when the
  deep-research skill hands off a research folder, or when new threads have been added to a
  finished run and the report needs updating. Can also be used standalone when the user has
  existing research files they want consolidated into a coherent document.
---

# Synthesis

This skill takes a research folder and produces a single report that a reader can rely on and build from. It has four jobs: consolidate, keep every claim traceable, clean the prose, and deliver.

## Inputs

- **Research folder**: the brief in `README.md`, the thread files, `sources.md` and `verification.md`, as produced by the deep-research skill. It also works on any organised set of research files; where the source list or verification file is missing, say so in the report's method note.
- **The brief** decides what kind of report this is. "What this is for", "Your situation" and "Deliverable" are instructions to this skill.

## Core Process

### Step 1: Read everything

Read the brief, every thread file, `sources.md` and `verification.md`. Work from the files, in a fresh context if possible, and not from memory of producing them.

Build a picture of:

- what findings are consistent across threads
- what findings contradict each other
- what gaps were identified
- what the bias note predicted against what was found
- which claims verification confirmed, corrected, or could not check

Read the threads against each other as well as one by one. In test runs the report writer was the one who caught a result stated for everyone that held only for a subset, and a court ruling described as deciding something it expressly did not, because another thread showed the difference. Keep a list of these as you go; see "Thread corrections found while writing".

### Step 2: Choose the structure

Decide on a structure that serves the question and the purpose in the brief. Common structures:

- **Question-Answer**: for focused questions with identifiable answers. State what is known, what is contested, what is unknown.
- **Landscape Map**: for broad exploratory questions. Map the main positions, the evidence for each, and the fault lines.
- **Problem-Analysis-Implications**: for understanding a phenomenon. Describe it, analyse the evidence, draw out what it means.
- **Chronological/Evolution**: for how something developed. Trace the arc, where current understanding came from and where it is heading.

Organise the body by what the reader needs to understand, which is rarely one section per thread. Tell the user which structure you chose and why, in a sentence.

### Step 3: Draft the report

```markdown
# [Title: descriptive, not clever]

## Research Question
[The question from the brief.]

## Summary
[Three to five sentences giving the essential findings. If the brief names a decision,
the answer to it is here. Someone who reads nothing else gets the core picture.]

## What this means for you
[Include when the brief names a decision or a situation; omit for a pure reference report.
See below.]

## [Body sections, by the chosen structure]

## What the evidence doesn't say
[Gaps, uncertainties and limits: questions the sources could not answer, where the bias
note predicted distortion and what was done about it, where evidence is thin, and what
further research would settle.]

## Sources
[Every source cited in this report: its ID, full citation and link, copied from
sources.md. Sources the report does not cite stay in sources.md.]

## Method note
[Two to four lines: the date, the number of threads, how many load-bearing claims were
checked and with what result, and a pointer to verification.md.]
```

**Citing.** Put the source ID after each factual claim, like this [03.2], exactly as it appears in the thread files. Name the author in the sentence where it reads better ("Ingendoh's 2023 review found... [03.4]"). The IDs are what let a reader, or a later project, get from any sentence to its source without opening the thread files, so every cited ID must appear in the Sources section with its link.

**Body sections** should state findings plainly, note confidence where it varies, flag contradictions instead of resolving them artificially, and name what is absent when absence is informative.

**Keep the splits that change the answer.** When a thread breaks a result down by dose, level, band, subgroup or treatment status, and the breakdown changes what a reader should do, the breakdown goes in the report, as a table if that is clearest. If the decision depends on it, it goes in the Summary too. In one test run a thread's table separated a suppressed hormone level, which carried the harm, from a low but measurable one, which mostly did not; the first report kept one sentence, and a reader had to point out the difference.

**What this means for you.** Place it directly after the Summary, because a reader with a decision came for the answer. In it:

- Give recommendations for the person's actual situation as the brief records it. Start from what they already use or have decided. Do not tell them to drop something they have chosen unless the evidence gives a specific reason, and then state the reason and how far it applies.
- Tie each recommendation to the findings and sources it rests on.
- Say what would change the recommendation: a price, a pending study, a fact about their situation you did not have.
- Where the brief marks part of their situation as an assumption, name the assumption the recommendation rests on, so they can see at a glance which advice to discount if the guess was wrong.
- Keep it to what the evidence supports. Where the research cannot choose between options, say so and say what would.

**Using the verification results.**

- A claim marked *not supported* does not appear.
- A claim marked *partly* appears in its corrected form.
- A claim marked *not accessible* or `[unverified]` may appear only with that stated in the sentence ("reported in trade press; not confirmed on the provider's page"), and it cannot be the sole basis of a recommendation.
- Before delivery, look at every figure, date, price and quotation in the Summary and in "What this means for you". Any that is not already a checked claim gets checked now against its source, and the result is appended to the end of the table in `verification.md`, continuing that thread's claim numbering (C04.7 after C04.6) with "checked by the report writer" in the Checked column. Update the count line. This is a bounded check of those two sections and is the only new fetching this skill does.

**Length.** Let the evidence set it. A run of five to seven threads usually supports a report of 3,000 to 6,000 words. The test is whether each thread's load-bearing claims made it in, and whether a reader could act on the report without opening the thread files.

### Step 4: The Slop Pass

After drafting, do a single editing pass specifically targeting AI writing patterns. Read `references/slop-patterns.md` for the full list, but the core targets:

**Remove hedging that says nothing:**
- "It's worth noting that..." → just state it
- "It's important to consider..." → just state it
- "There are many factors to consider..." → name them or cut it
- "This is a complex topic..." → everything is complex; say something specific

**Remove false balance:**
- "Some experts say X while others say Y" → who specifically? How many? What's the evidence for each?
- "There are arguments on both sides" → only if there genuinely are, and then state them
- "The truth probably lies somewhere in the middle" → sometimes it doesn't. Sometimes one side has the evidence.

**Remove hollow transitions:**
- "Furthermore..." "Moreover..." "Additionally..." → restructure so the logic flows without crutch words
- "In conclusion..." → if it's the conclusion, it's self-evident

**Remove performative nuance:**
- "This is a nuanced topic that defies simple answers" → then give the nuanced answer instead of announcing it
- "Reasonable people can disagree" → on what basis? With what evidence?

**Remove sycophantic framing:**
- "This is a great question" → never
- "As you rightly point out" → never
- "Building on your excellent insight" → never

**Remove list-ification:**
- If the draft contains more than 2 bulleted lists in the body sections, convert them to prose. Lists are for quick reference, not for making arguments. Research reports argue; they don't enumerate. Recommendations in "What this means for you" may be a list.

The goal is writing that sounds like a knowledgeable human wrote it for another human: direct, specific, honest about uncertainty, and free of the verbal tics that mark AI-generated text. Keep the source IDs intact through this pass.

### Step 5: Bias note reconciliation

Brief check against the bias note in the brief:

- Did the research actually compensate for the identified distortions, or did it just acknowledge them?
- Are the conclusions disproportionately drawn from the sources the bias note predicted would dominate? The tier counts at the top of `sources.md` help here.
- Is the report presenting distorted consensus as settled fact anywhere?

If issues are found, revise the relevant sections. One pass.

### Step 6: Check and deliver

Save the report as `REPORT.md` in the research folder, or under the name a calling skill specifies.

Run the checker, which lives in the deep-research skill's folder:

```bash
python3 ../deep-research/scripts/runcheck.py check [research-dir]
```

Fix what it flags in the report: citations that do not resolve, cited sources missing from the Sources section, long uncited paragraphs, a missing section. Leave a check failing only when there is a reason, and give the reason in the method note.

If using git, commit as `Final report: [short title]`.

Present the report to the user with a two or three sentence account of what it found. If the brief's Deliverable names another format (Word, PDF, a one-page summary, a NotebookLM briefing), produce it now from `REPORT.md`, using the skill for that format where one exists, and save it in the same folder. The markdown stays the master copy; regenerate the other formats from it after any revision.

## Thread corrections found while writing

Do not leave a thread statement you know to be wrong or overstated, and do not quietly write around it. Fix the report, then list each one with the file, the passage and the correction. If you are the main session, apply them to the thread files and add a line for each under "Corrections made" in `verification.md`, marked as found by the report writer. If you are a sub-agent, report them back and leave the thread files alone.

## Writing the report in a sub-agent

When the main session hands the report to a sub-agent, the harness may refuse that agent's write to `REPORT.md`. Have the writer save its draft and its extra checked rows to scratch files and report back: what changed, the word count, the claims it checked and their results, and any thread corrections. The main session then reads the Summary and "What this means for you" itself, copies the draft into place, appends the rows to `verification.md`, applies the thread corrections, runs the checker and commits. Brief the writer with the paths to this skill and to `references/slop-patterns.md`, the research folder, the output paths, and the rules the brief sets for the report (public release, no personal information, length).

## Updating a report after new threads

When deep-research has added threads to a finished run, rewrite the report with the new material integrated. Re-read all the threads, revise the Summary and "What this means for you" in light of everything, and place new findings where they belong in the structure. Do not bolt a section on the end. Where a new thread corrects or narrows an earlier finding, revise that statement everywhere it appears, the Summary included, and say in the body what changed it. Update the Sources section and the method note, adding a line on why the threads were added, run the checker, and commit as `Report updated: [what was added]`.

## What This Skill Does NOT Do

- It does not do additional research. Gaps found during synthesis go in "What the evidence doesn't say"; if a gap matters to the user's decision, say so when presenting the report so they can ask for a new thread.
- It does not re-question the user's intent. The brief settled that.
- It does not re-analyse bias. It reconciles against the bias note in the brief.

## Additional Reference

For the complete list of AI writing anti-patterns to target during the slop pass, see `references/slop-patterns.md`.
