# Briefing research agents

A research agent starts with nothing but its brief. It has not seen the conversation, the user's situation or the other threads. Whatever the brief leaves out, the agent will fill with the most generic reading of the topic. Use the templates below as written and fill every bracket.

Contents:

1. Thread brief template
2. Thread file format (pasted into every thread brief)
3. Verifier brief template
4. verification.md format

## 1. Thread brief template

Paste the brief's sections in full. Summarising the user's situation to a sentence is how reports end up recommending against something the user already relies on. Keep every "(assumption)" label: the agent needs to know which facts about the user are confirmed and which are guesses.

```
You are researching one thread of a larger research project. Today is [date].

THE PROJECT
Overall question: [Question, from the brief]
What it is for: [What this is for, from the brief]
The person's situation: [Your situation, from the brief, in full, with assumption labels]
Deliverable: [Deliverable, from the brief]
Scope: [Scope, from the brief: what is in, what is out, the time window]
Lines marked (assumption) were not confirmed by the person. Where a finding would differ
if an assumption is wrong, say so.

YOUR THREAD ([NN])
Question: [this thread's question]
Why this thread exists: [what the report needs from it]
Other threads cover: [one line per other thread, so you do not duplicate them. If you find
something that belongs to another thread, note it under Gaps.]

KNOWN DISTORTIONS
[The bias note from the brief, in full. Then how it applies to this thread: which kinds of
source to seek out, which to discount, which period or language to look in. Writing this
thread-specific guidance at briefing time is expected.]

STARTING POINTS (unverified)
[Optional. Names, terms and sources from the user or from background knowledge that
point the agent at the right territory. These are leads to check, not facts. Leave out
if there are none.]

TOOLS
[Name the search and reading tools available and how to load any that need loading.
For scholarly, medical or legal topics, add the open routes that get past paywalls and
bot checks without working around them; see "Reading routes" below the template.]
Search widely first: 10 to 20 searches from different angles, including the sceptical
angle and the terms a specialist would use. Then read the most important sources in
full. A search snippet is a lead, not a source.

HOW TO WORK
- Prefer primary sources: the original study, filing, statute, dataset, official
  documentation, or a first-hand account. When a secondary source reports a primary one,
  find the primary.
- Record how much of each source you actually read: full, abstract, or snippet.
- Give exact figures with units, sample sizes, dates and who measured them.
- For prices, plan limits, versions, availability and legal status, use the provider's
  or authority's own page and note the date you checked.
- When sources contradict each other, report the contradiction. Do not pick the one
  that fits the story.
- When you look for something and find nothing, say so and list what you searched.
  "No evidence found" is a finding.
- Report what has not been studied at all, and the likely reason.
- Follow an unexpected lead if it matters, and say that you did.
- Do not pad. Stop when new searches return what you already have.
- For every study result, say who was in the group the figure comes from: who was
  excluded, and whether the figure is for the whole sample or a subset. Wrong group
  descriptions are the commonest correction verifiers make.
- For a trial result on anything other than its primary outcome, say where it sat in
  the trial's testing order, and call it nominal if the trial's own rules make it so.
- Use words like "largest", "only" and "first", and labels for groups of people, only
  when the source uses them, and say they are the source's.
- Leave out statements about named people (their motives, ties or outside work) that you
  cannot confirm at source.
- Take figures from the source's own text or tables. Fetch tools that summarise a page
  can misreport numbers; when one is all you have, say so.

OUTPUT
Write your findings to [absolute path to NN-slug.md] using exactly the format below.
Aim for 2,000 to 5,000 words of body text (everything except the Sources list): enough
to carry every finding with its source. The Sources list usually adds 2,000 to 3,000 more.
[Include / Omit] the "What this means for the person's situation" section. [When the
brief has no individual, say who to write it for, such as "any adult reader of the report".]

[Paste section 2 here: the format block and the definitions under it, with NN replaced
by this thread's two-digit number.]

Then reply with: a 4 to 6 sentence summary of what you found, anything that surprised
you, and any lead that deserves its own thread.
```

Include the "What this means for the person's situation" section in every thread when the brief names a decision, even an assumed one, and omit it from every thread when the brief says "Reference". Decide once and tell each agent, so the files match.

**Reading routes.** Many journal and publisher sites show bot checks to automated readers. Agents must not try to get past them. These open routes worked in test runs, and belong in the TOOLS block for scholarly topics:

- Europe PMC search and open-access full text: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json&resultType=core` and `https://www.ebi.ac.uk/europepmc/webservices/rest/PMCxxxxxxx/fullTextXML`
- NCBI E-utilities for PubMed abstracts and PMC: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` (esearch, efetch)
- ClinicalTrials.gov API v2: `https://clinicaltrials.gov/api/v2/studies?query.term=...`
- DailyMed for US drug labels; regulators' and guideline bodies' own pages for current text
- Internet Archive snapshots for pages that have moved, and archive.org scans for papers from before about 1975

An agent with a shell can reach these with `curl`. Say which tools need loading first (for example a deferred web search tool).

**When the brief has no individual.** A public or reference report has no person to relate findings to. Keep the "What this means for the person's situation" heading so the files match, and tell each agent who to write it for.

For an extension thread, add after THE PROJECT:

```
ALREADY ESTABLISHED
[One paragraph on what the existing threads found that bears on this thread, with the
file names. Do not re-research these points; build on them.]
```

When the extension answers a reader's challenge to a finding, put the challenge in the project's situation as a further starting position "to be tested, not assumed", and add to KNOWN DISTORTIONS that the agent should look as hard for evidence against it as for it.

## 2. Thread file format

Paste everything in this block into each thread brief, replacing NN with the thread's two-digit number (`C03.1`, `[03.2]`). The checker script reads these headings and the source line format, so they need to match.

```
# [Thread title]

## Question
[The thread's question.]

## Key Findings
[Plain statements, grouped under sub-headings where that helps. Every factual claim
carries one or more source IDs, like this [NN.2]. Say what the evidence shows without
hedging, and say how strong it is.]

## What this means for the person's situation
[Only if your brief says to include it. Relate the findings to what the person already
uses or has decided, and say which points depend on an unconfirmed assumption.]

## Load-bearing claims
[The three to six claims from this thread that a reader would act on, or that the
report's conclusions will rest on. One line each, with the exact figure or date. Make
each one a single checkable statement: one study and one finding, so a checker can match
it to one passage. Statements that something has not been studied belong under Gaps,
with the searches you ran, not here.]
- CNN.1: [claim] [NN.2]
- CNN.2: [claim] [NN.5][NN.7]

## Sources
- [NN.1] Author or organisation (Year). Title. Publication or site. URL or DOI. | tier: primary | read: full | supports: [one line on what it was used for]
- [NN.2] ...

## Confidence Notes
[Where the evidence is strong, where it is thin, and where it may be distorted in the
ways your brief describes.]

## Gaps
[What you looked for and could not find, with what you searched. What has not been
studied at all, and the likely reason. What would strengthen this thread.]

Source tiers (use exactly one of these words after "tier:"):
- primary: the original study, dataset, filing, statute, official documentation, or a
  first-hand account from the person or organisation concerned
- secondary: reviews, journalism and analysis reporting on primary material
- vendor: anyone selling the thing under discussion, including their own studies and
  white papers
- anecdotal: forums, testimonials, practitioner reports and social posts

Read levels (use exactly one after "read:"): full, abstract, snippet. A claim resting
only on a snippet should be described in the findings as a lead to check.
```

## 3. Verifier brief template

The verifier must not have written the claims. Give it the claims and their sources, and nothing about what you hope is true. Use an agent type that can open web pages.

```
You are checking claims against their sources. You did not write these claims. For each
one, open the cited source and report what it actually says. Today is [date].

For each claim:
1. Open the cited source at the link given. If it will not open, try one other route
   (publisher page, DOI resolver, an archive copy). If that fails, mark it not accessible.
2. Find the passage, figure or table the claim relies on.
3. If the cited source is secondary, try to reach the primary source it reports and say
   which one you checked.
4. Report one of: confirmed, partly, not supported, not accessible.

Do not search for other evidence that the claim is true. The question is only whether
this source supports this claim as worded. For figures, dates, prices and quotations,
"confirmed" means an exact match. Where a claim has several parts, check each part and
say which one fails. Check the description of who was studied as closely as the
figures: exclusions, and whether the figure is for the whole sample or a subset. Flag any
word that goes beyond the source, such as a superlative or a population label the source
does not use. Read figures from the source's own text or tables, not from a tool that
summarises the page.

[Tools available and how to load them.]

CLAIMS
[ID] | [claim as worded in the thread file] | [source IDs] | [links]
...

Reply with one line per claim:
[ID] | [status] | [what the source says: a short quote or the figure] | [primary or secondary checked; full text or abstract] | [date]
Then one line on anything in a claim that goes beyond the source.
```

One checker per thread gave short, careful reports in test runs, at about half the cost of the thread itself. One checker can take two small threads.

## 4. verification.md format

```markdown
# Verification — [topic]

Checked [date]. [N] claims: [a] confirmed, [b] partly, [c] not supported, [d] not accessible.

| Claim | Statement | Sources | Status | What the source says | Checked |
|---|---|---|---|---|---|
| C03.1 | [claim] | [03.2] | confirmed | "[quote or figure]" | primary, 2026-11-20 |
| C03.2 | [claim] | [03.5] | partly | [what it actually says] | secondary, 2026-11-20 |

## Corrections made
- C03.2: the thread file said [X]; the source says [Y]. Corrected in `03-[slug].md`.

## Absence claims
- "[No study has tested X]": searched [databases and queries]; nothing found as of [date].
```

Status values are exactly `confirmed`, `partly`, `not supported` and `not accessible`, so the checker can count them. Absence claims never get a row in the table, because no source can confirm them; they go under "Absence claims". When threads are added later, or the report writer checks further figures, append their rows to the end of the same table, continue each thread's claim numbering (C04.7 after C04.6), note "checked by the report writer" where that applies, and update the count line.
