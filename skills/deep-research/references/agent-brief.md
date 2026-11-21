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
[Name the search and reading tools available and how to load any that need loading.]
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

OUTPUT
Write your findings to [absolute path to NN-slug.md] using exactly the format below.
Aim for 1,500 to 4,000 words: enough to carry every finding with its source.
[Include / Omit] the "What this means for the person's situation" section.

[Paste section 2 here: the format block and the definitions under it, with NN replaced
by this thread's two-digit number.]

Then reply with: a 4 to 6 sentence summary of what you found, anything that surprised
you, and any lead that deserves its own thread.
```

Include the "What this means for the person's situation" section in every thread when the brief names a decision, even an assumed one, and omit it from every thread when the brief says "Reference". Decide once and tell each agent, so the files match.

For an extension thread, add after THE PROJECT:

```
ALREADY ESTABLISHED
[One paragraph on what the existing threads found that bears on this thread, with the
file names. Do not re-research these points; build on them.]
```

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
report's conclusions will rest on. One line each, with the exact figure or date.]
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
"confirmed" means an exact match.

[Tools available and how to load them.]

CLAIMS
[ID] | [claim as worded in the thread file] | [source IDs] | [links]
...

Reply with one line per claim:
[ID] | [status] | [what the source says: a short quote or the figure] | [primary or secondary checked] | [date]
```

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

Status values are exactly `confirmed`, `partly`, `not supported` and `not accessible`, so the checker can count them. When threads are added later, append their rows to the same table and update the count line.
