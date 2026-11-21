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

## Example

[`examples/thyroid-cholesterol/`](examples/thyroid-cholesterol/) is a complete run from 21 November 2026, unedited apart from the corrections that verification made. Start with its [`REPORT.md`](examples/thyroid-cholesterol/REPORT.md).

The question was how thyroid function affects cholesterol, whether thyroid should be brought to a healthy level (by the symptom-based standard used before the TSH test) before a cholesterol-lowering drug is prescribed, and whether TSH is itself harmful. It was run with the full `blind-variables` pass and written for a general reader, with no personal information.

What the run looked like:

- Five threads were planned and four were completed. The agent for the thread on the direct effects of TSH was stopped by the model's safety filter before it wrote anything. The report says so and leaves that question unanswered.
- The four threads cite 221 sources: 107 read in full, 108 as abstracts and 6 seen only as search snippets.
- 24 key claims were checked against their sources. 13 were confirmed as written. 11 had the right figures and needed rewording, mostly for overreach or wrong attribution; all were corrected. None was unsupported.
- The folder passes all of the checker's checks.
- It used about 3.4 million tokens across its sub-agents and took about 80 minutes.

The example is an evidence review. It is not medical advice.

## Cost

Runs are expensive. In the example, each research thread used 450,000 to 480,000 tokens, each verifier 230,000 to 310,000, and the report about 470,000. The brief tells you how many agents will run before anything starts.

## Known limits

- Many journal sites show bot checks to automated readers. The agents do not work around them; they fall back to PubMed, Europe PMC and the Internet Archive, which often gives an abstract only. Each source records how much of it was read.
- Research agents write longer thread files than the skill's guide suggests, because the source lists themselves run to two or three thousand words.
- A model's safety filter can stop a thread on some biology topics. The run continues without it and the report states what is missing.
- One complete run has been made with this version.
