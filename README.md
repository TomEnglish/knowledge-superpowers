# knowledge-superpowers

A Claude Code plugin that researches a question from many sources and ends with a report in which every claim can be traced to its source.

It is built around four problems with AI-written research: the report answers the literal sentence and misses what the person needed; sources get lost between the research and the report; the claims the conclusions rest on are never checked; and the model quietly inherits the slant of the literature it was trained on.

## How a run works

1. **Brief.** The pipeline drafts a research brief: the question, what the answer is for, the person's situation, the deliverable, the scope, a bias note and the list of research threads. Anything it had to guess is marked as an assumption. It asks at most three questions, and this is the one point where the person steers the run.
2. **Threads.** Each thread goes to its own research agent, briefed from a fixed template so that the whole brief and the bias note reach every agent. Each agent writes one file in a fixed format, with a numbered source for every claim.
3. **Source list.** A script builds one `sources.md` from the thread files and reports citations that do not resolve, sources without links, and sources seen only as search snippets.
4. **Verification.** Each thread names the handful of claims a reader would act on. Agents that did not write those claims open the cited sources and report what they say. Results and corrections go in `verification.md`.
5. **Report.** A single report cites source IDs throughout, relates the findings to the person's decision when the brief names one, says what the evidence does not show, and lists every cited source with its link.

## Commands and skills

| | |
|---|---|
| `/deep-dive <topic>` | Brief, research, verification and report, with one gate at the brief. |
| `/research <topic>` | The same, with separate conversations first to sharpen the question and map the bias. |

| Skill | What it does |
|---|---|
| `articulate` | Turns a rough idea into a research question with no hidden assumptions. |
| `blind-variables` | Maps how funding, institutions, social pressure and the model's own training are likely to distort the sources on this topic, and what to do about it. |
| `deep-research` | Writes the brief, runs the threads, builds the source list and verifies the key claims. Also extends a finished run with new threads. |
| `synthesis` | Writes the report from the research folder and strips AI writing patterns. |

## What a run produces

```
research/[topic]/
├── README.md          the confirmed research brief
├── 01-[thread].md     one file per research thread
├── 02-[thread].md
├── sources.md         every source from every thread, built by script
├── verification.md    the key claims, each checked against its source
└── REPORT.md          the report
```

## The checker

`skills/deep-research/scripts/runcheck.py` needs only Python 3.

```bash
python3 skills/deep-research/scripts/runcheck.py sources research/my-topic
```

builds `sources.md` and lists problems.

```bash
python3 skills/deep-research/scripts/runcheck.py check research/my-topic
```

prints a scorecard for the whole folder: whether the brief is complete, every citation resolves, every key claim has a verification result, the report cites its sources, and so on. It checks form. It cannot tell whether the research is right.

## Trying it

Load the plugin for one session:

```bash
claude --plugin-dir /path/to/knowledge-superpowers
```

Then type `/deep-dive` followed by your question.

## Examples

Two complete runs from 21 November 2026, unedited apart from the corrections that verification made. Both started from one request, which the brief split into two runs. Both used the full `blind-variables` pass and were written for a general reader, with no personal information. Start with each folder's `REPORT.md`.

### [`examples/thyroid-cholesterol/`](examples/thyroid-cholesterol/)

How thyroid function affects cholesterol; whether thyroid should be brought to a healthy level, by the symptom-based standard used before the TSH test, before a cholesterol-lowering drug is prescribed; and whether TSH itself does harm. [Report](examples/thyroid-cholesterol/REPORT.md).

- Five threads, citing 268 sources: 112 read in full, 148 as abstracts and 8 seen only as search snippets.
- The model's safety filter stopped the first agent on the TSH thread before it wrote anything. The same brief, run on another model, completed. The brief's run notes record both attempts.
- 34 key claims were checked against their sources. 21 were confirmed as written. 13 had the right figures but needed rewording, mostly for overreach or wrong attribution; all were corrected. None was unsupported.
- About 4.1 million sub-agent tokens.

### [`examples/cholesterol-lowering-mortality/`](examples/cholesterol-lowering-mortality/)

Whether lowering cholesterol reduces death from any cause, and not only cardiovascular events: for whom, by how much in absolute terms, and by which means. [Report](examples/cholesterol-lowering-mortality/REPORT.md).

- Four threads, citing 235 sources: 96 read in full, 131 as abstracts and 8 seen only as search snippets.
- 34 key claims were checked: 24 by verifiers and 10 more by the report writer. 28 were confirmed as written and 6 were corrected. None was unsupported.
- The research agents' brief had four additions here that are not yet in the skill: one checkable statement per key claim, statements that something is missing kept to the Gaps section, words like "largest" and labels for groups of people taken from the source, and a length guide for body text only. The share of key claims that needed rewording fell from 11 in 24 on the first version of the thyroid run to 5 in 24.
- About 3.2 million sub-agent tokens and about 90 minutes.

Both folders pass all of the checker's checks. The examples are evidence reviews. They are not medical advice.

## Cost

Runs are expensive. In the examples, each research thread used 445,000 to 520,000 tokens, each verifier 150,000 to 310,000, and each report 435,000 to 470,000. A run of four or five threads used 3.2 to 4.1 million tokens in all. The brief tells you how many agents will run before anything starts.

## Known limits

- Many journal sites show bot checks to automated readers. The agents do not work around them; they fall back to PubMed, Europe PMC and the Internet Archive, which often gives an abstract only. Each source records how much of it was read.
- Research agents write longer thread files than the skill's guide suggests, because the source lists themselves run to two or three thousand words.
- A model's safety filter can stop a thread on some biology topics. The run continues without it and the report states what is missing. In the thyroid example, the same brief run on another model completed.
- Two complete runs have been made with this version, both on health questions.
