---
name: deep-research
description: >
  The knowledge-superpowers research engine. Turns a question into a confirmed research brief,
  runs parallel research threads with traceable sources, verifies the claims the conclusions
  rest on, and hands a research folder to the synthesis skill. Use whenever the user wants a
  topic researched in depth from many sources: "/deep-dive", "/research", "do the research",
  "go research this", "dig into this", "find out about", or when the articulate and
  blind-variables skills hand off a confirmed question and bias map. Also use to extend a
  finished research folder ("also look into...", "add a thread on...", a follow-up question
  about an earlier report). Prefer this over any generic or built-in research workflow when
  the user refers to their research pipeline or to knowledge-superpowers.
---

# Deep Research

This skill runs a research project up to the point of writing the report. It agrees a brief with the user, researches the question as a set of parallel threads, builds one source list, checks the claims the conclusions will rest on, and hands the folder to the **synthesis** skill.

Two commands start it. `/deep-dive` runs this skill and then synthesis with the single gate described in Step 1. `/research` holds the articulate and blind-variables conversations first and then runs this skill. Neither adds a gate after the brief.

## What a finished run looks like

```
research/[topic-slug]/
├── README.md          # the confirmed research brief
├── 01-[thread].md     # one file per research thread
├── 02-[thread].md
├── sources.md         # every source from every thread, built by script
├── verification.md    # the load-bearing claims, each checked against its source
└── REPORT.md          # written afterwards by the synthesis skill
```

Create the folder under the current working folder unless the user names another place. If a calling skill (for example chapter-pipeline) specifies its own paths or file names, use those; the contents and conventions below stay the same.

## Step 1: Write the research brief

The brief is the one place the user steers the run, so it has to capture more than the question. Reports go wrong in predictable ways when it doesn't: they recommend against something the person already uses, they answer the literal sentence and miss the angle a practitioner would have named first, or they arrive in a form the person then has to convert.

Before asking anything, collect what is already available: the user's message, attached files, the working folder and its notes, and anything remembered about them. Then draft the whole brief with your best reading, mark each assumption as an assumption, and ask only what you could not find and what would change the research. Ask at most three questions, all in one message, alongside the draft. Choose the ones whose answers would most change the threads or the recommendations, and assume the rest. The user should be able to reply "go" or correct two lines.

```markdown
# [Topic] — Research brief

## Question
[One or two sentences. No hidden assumptions.]

## What this is for
[The decision it informs or what the user will do with the answer. Write "Reference" if there is no decision.]

## Your situation
[What the user already uses, knows, has decided or has ruled out. Constraints: budget, place, timeframe, skill level. Write "Not stated" where unknown.]

## Deliverable
[Decision document, reference source, or both. Audience. Any format beyond markdown: Word, PDF, one-pager, NotebookLM briefing.]

## Scope
[What is in, what is deliberately out, the time window.]

## Bias note
[Who dominates the sources on this topic, what is likely overstated or missing, and the specific actions that compensate. Three to six lines.]

## Threads
1. `01-[slug]` — [the thread's question] — [why it is needed]
2. ...
```

If the **articulate** and **blind-variables** skills have already run, copy their confirmed question and bias map into the brief and fill in the rest. If they have not, write the bias note yourself. When the topic is one where funding, stigma or vendor marketing shapes the literature, add one line after the questions offering the full blind-variables pass. It is an offer and does not count as one of the three questions; the default is to proceed with the bias note as drafted. If the user takes it, run that skill, replace the bias note with its result and carry on without asking them to confirm the brief again.

Ask about "Your situation" directly when the topic involves tools, products, treatments or methods the person may already be using. A recommendation that ignores what they already have is the most common way a report loses their trust.

**When the user answers or corrects without saying "go".** Update the brief and treat the reply as confirmation, unless the changes add or drop threads or change the size of the run. In that case show the revised thread list and agent count, and wait. Say in one line that the run is starting.

**When the user says "go" without answering.** The assumptions stand, and they stay labelled as assumptions in `README.md` and in every agent brief. An unconfirmed guess must not turn into a fact about the user on its way to the research agents. Where a finding or recommendation depends on an assumption, the thread and the report say so.

**Close the gate message with what "go" will start**: the folder the work will be saved to, how many research agents and checkers will run, a token estimate, and that it then runs through to the report without further questions. This is the user's one chance to object to the size of the run. Estimate from these measurements on test runs: about 0.5 million tokens per research thread, 0.25 million per checker and 0.5 million for the report, so a four-thread run used about 3.2 million and a five-thread run about 4 million.

### Designing the threads

Thread design is the highest-leverage decision in the run. Plan three to seven threads that can be researched independently.

- Do not stop at splitting the user's sentence into its clauses. A thread per clause is fine where the sources differ, but also ask what a specialist or working practitioner would call the core variables of the subject, and check that each one has a thread or a place inside one. The angles a specialist would name first are the ones users come back and ask for afterwards.
- Include one thread that makes the strongest case against the obvious answer, shaped by the bias note. If the request has several obvious answers, or the counter-case would also have to carry safety and law, split it so no thread is overloaded.
- Every thread reports what has not been studied and why, in its Gaps section. Add a dedicated thread on absence only when it is central to the question.
- When the brief names a decision, make sure some thread covers the practical side: costs, effort, availability, and what people who tried it report.
- Check every line of "Your situation" and "Deliverable" against the thread list. Each named country, guideline, tool or audience needs a thread or a named place inside one. In one test run the brief put US guidelines first and no thread covered guidelines, so the report had to say it could not answer.
- When a request holds several questions, keep them in one run if they share sources and their answers inform each other. Write the Question as a short numbered list, and let the thread count go as high as nine. If the parts would each need three or more threads of their own, or have little evidence in common, propose separate runs, or the core question now and the rest as extensions, and let the user choose at the gate. Split runs can share one blind-variables pass when their literatures overlap: copy the parts of the bias map that apply into each brief, and name the companion run in each.

Name the folder with a short lowercase slug, such as `research/ai-model-strategy/`.

Present the brief and threads together. **Wait for the user to confirm or correct them.** This is the only gate; after it, run to the end without further check-ins unless the research changes the question.

## Step 2: Set up the folder

Write the confirmed brief to `README.md`.

Use git when it helps and does no harm. If the research folder is not inside an existing repository and git is available, run `git init` in the folder and commit the brief as `Research plan: [short description]`. If the folder is inside an existing repository, do not create a nested one and do not commit to the user's repository unless they ask.

## Step 3: Run the threads

Give each thread to its own sub-agent, and launch them all in one message so they run in parallel. Read `references/agent-brief.md` now and build every agent's brief from its template. An agent knows only what its brief says, so the template carries the whole brief (question, purpose, situation, deliverable, scope), the bias note, the source rules and the file format. Briefs improvised from memory drop exactly those parts.

Use an agent type that can both search the web and write files, such as a general-purpose agent. A read-only research agent cannot save its thread file.

Check which search and reading tools this session has before writing the briefs. Names differ between environments (web search, page fetch, a fetch agent, scholarly or PubMed connectors, the user's Drive, a browser), and some need loading first. Name the tools in each brief, with how to load them, because a sub-agent will not go looking. For scholarly topics, add the open reading routes listed in the reference file; publisher sites often block automated readers, and agents must not work around bot checks. If the user's own documents matter, read them yourself and put the relevant facts in the briefs.

If sub-agents are not available, research the threads yourself one at a time, using the same template as your checklist, and write each file before starting the next.

When the agents report back:

- Read each summary, then check each file for form: findings carry source IDs, and the Sources and Load-bearing claims sections are there.
- Send a thin or malformed file back to its agent with specifics. Judge length on body text, not counting the Sources list: under about 1,500 words is usually too thin, and over about 6,000 usually should have been two threads. In test runs, good threads ran 3,700 to 5,900 words of body text. The checker reports body words for each thread.
- If an agent found a lead that deserves its own thread, tell the user in one line and add it using the extension steps below.

**When the model's safety filter stops an agent.** Some topics, often in biology, trip a safety filter that stops an agent before it writes anything. Tell the user in one line, and do not redo that thread's research yourself in the main conversation. Carry on with the other threads. Offer to rerun the same brief on another model, which worked in a test run with the brief unchanged. If the user declines, or the rerun is also stopped, record it in the brief's run notes and mark the question unanswered; the report then says what is missing.

## Step 4: Build the source list

Run the checker from this skill's folder:

```bash
python3 scripts/runcheck.py sources [research-dir]
```

It writes `sources.md` from the Sources sections of the thread files and lists problems: citations with no source entry, sources with no link, and sources that were only seen as search snippets. Fix problems in the thread files, or send them back to the agent, and run it again until it reports none. Never edit `sources.md` by hand, because the next build overwrites it.

## Step 5: Verify the load-bearing claims

A report is only as reliable as the handful of claims its conclusions rest on, so that is where checking effort goes. Checking a random sample of links does not protect the reader.

1. Collect the claims listed under "Load-bearing claims" in every thread file. Add any other claim you expect the summary or recommendations to lean on.
2. Have each one checked by an agent that did not write it, using the verifier template in `references/agent-brief.md`. The checker opens the cited source and reports what it says. Use one checker per thread; one can take two small threads. If a claim holds several facts despite the brief, split it into rows before sending it, so one wrong word does not sink the rest.
3. Write the results to `verification.md` in the format given in that reference file.
4. Apply the results. Correct any thread file whose claim the source did not support, and record the correction. Where a source could not be opened, mark the claim `[unverified]` in the thread file.

Four kinds of claim need particular care:

- **Figures, dates, prices and quotations** must match the source exactly.
- **Time-sensitive facts** (prices, plan limits, version numbers, availability, legal status) should be checked on the provider's or authority's own page, with the date checked recorded. Trade-press reports of these go stale and are often wrong.
- **Absence claims** ("no trial has tested X") cannot be confirmed by a source. Keep them out of the claims table. List them under "Absence claims" in `verification.md`, with the searches that were tried and the date.
- **Descriptions of who was studied** are where checkers most often find errors: a result given for everyone that applies to a subset, or exclusions left out. Put the corrected wording back into the thread file.

Do this once. A claim that cannot be verified gets labelled and carried forward honestly; do not loop on it.

## Step 6: Commit and hand off

If using git, commit as `Research complete: [N] threads, [M] claims verified`.

Hand the folder to the **synthesis** skill. Go straight on unless a calling command or skill sets a gate here. If the report is written by a sub-agent, follow synthesis's "Writing the report in a sub-agent".

Before handing off, check:

- `README.md` holds the confirmed brief.
- Every thread file has findings with source IDs, and Sources, Load-bearing claims, Confidence Notes and Gaps sections.
- `sources.md` builds with no unresolved citations.
- `verification.md` has a row for every load-bearing claim.
- The work is committed, if git is in use.

`python3 scripts/runcheck.py check [research-dir]` reports all of these at once.

## Extending a finished run

Users often read a report and come back with the question it raised. Treat that as a continuation of the same project.

1. Search the existing thread files first. If they already answer the follow-up, answer from them with their source IDs and do no new research.
2. Otherwise add threads, numbered on from the last file. Brief the agents with the same template, plus a paragraph on what the existing threads already found so they do not repeat it.
   - When the follow-up challenges a finding ("the report doesn't separate X from Y"), record the challenge in the brief's "Your situation" as a further starting position to be tested, not assumed. Brief the thread to test it and to look as hard for evidence against it as for it. A model tends to confirm the framing it is handed, and a reader's challenge is a framing too.
3. Update `README.md`: add the new threads to the list with a dated line saying what was added and why. If the follow-up revealed something about the user's situation, add that too.
4. Rebuild `sources.md`, verify the new load-bearing claims and append them to `verification.md`.
5. Commit as `Extend: [what was added]`, then hand to synthesis, which rewrites the report so the new material is integrated. Tell synthesis which earlier statements the new thread corrects or narrows, so they are revised wherever they appear, the Summary included.

## When research changes the question

Sometimes the research shows the question was wrong or too narrow. Note the finding in the relevant thread file and tell the user briefly: "Research on [thread] suggests the question should be reframed because [reason]. Adjust, or continue as scoped?" If they adjust, update the brief and continue. If not, record the possible reframe for synthesis to address.

## Managing context

Research produces far more text than fits in working memory. Let the files hold it: agents write to disk, you work from their summaries, and you re-read full files only when checking form or applying corrections. For long or multi-session projects, see `references/context-hygiene.md`.

## What this skill does not do

- It does not write the final report or clean up the prose. Synthesis does both.
- It does not question the user repeatedly. Everything it needs to ask goes in the brief, once.
- It does not replace the full articulate and blind-variables passes when the user wants them. It uses their output when it exists.
