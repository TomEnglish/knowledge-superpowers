---
name: articulate
description: >
  This skill should be used when the user wants to research a topic, investigate a question,
  understand something deeply, or asks Claude to "look into", "find out about", "research",
  "deep dive", "investigate", "explore", or "help me understand" any subject. Also trigger
  when the user frames a broad or ambiguous question, says "I'm curious about", "what's the
  deal with", "help me think through", or presents a topic that would benefit from scoping
  before diving in. This skill is the entry point for the knowledge-superpowers pipeline —
  use it before beginning any substantive research. Even if the user sounds certain about
  what they want, use this skill to pressure-test the question before committing research effort.
---

# Articulate

The purpose of this skill is to help the person asking the question find the *right* question before any research begins. Most research fails not because the execution is sloppy, but because the question was wrong — shaped by assumptions the asker didn't know they had, framed in ways that pre-determine the answer space, or aimed at a surface symptom instead of the underlying thing they actually need to understand.

This skill corrects for the **requestor's** biases and framing. It is not about the topic yet — it is about the person and what they need.

## Core Process

### Step 1: Listen and Reflect Back

Read the user's request carefully. Before asking anything, reflect back what you heard — not as a summary, but as an interpretation. Show them how you're reading their question, including the assumptions embedded in it.

Example: If someone asks "What are the best nootropics for focus?" — reflect that this question assumes pharmaceutical intervention is the right frame, assumes "focus" is a single measurable thing, and assumes a ranking is possible. The actual need might be about understanding attention mechanisms, or about a specific personal situation where focus is a symptom of something else.

Do this briefly. One or two sentences. The goal is to surface the frame, not to lecture.

### Step 2: Ask One Question at a Time

Do not dump a list of clarifying questions. Ask the single most important question first and wait for the answer. Each question should do one of these things:

- **Surface an assumption**: "You're framing this as X — is that because you've already ruled out Y, or is Y still on the table?"
- **Find the real need**: "What would change for you if you had this answer? What decision does it inform?"
- **Find what's already in place**: "What are you already using, or have you already decided or ruled out?" Research that ignores this ends up recommending against the person's own choices.
- **Test the scope**: "Are you looking for a comprehensive picture, or is there a specific angle that matters most?"
- **Propose a reframe**: "What if the question isn't X but actually Y — does that feel closer to what you need?"

Use multiple choice when it helps the person think, but don't force every question into multiple choice. Sometimes open-ended is better for surfacing things neither of you expected.

### Step 3: Propose the Research Question

After 2-4 exchanges (not more — respect the person's patience), propose a refined research question. This should be:

- Specific enough to research meaningfully
- Honest about what it's asking (no hidden assumptions smuggled in)
- Explicit about scope and what's deliberately excluded
- Framed in a way that doesn't pre-determine the answer

Present it as: "Based on what you've told me, here's how I'd frame the research question: [question]. Does this capture what you're after, or should we adjust?"

### Step 4: Hard Gate

**Do not proceed to research until the user confirms the question.** If they adjust, iterate. If they confirm, hand off to the blind-variables skill to assess the information landscape before research begins.

## Principles

**Spend compute here, save human time later.** This phase is where LLM thinking time pays for itself most dramatically. A few extra exchanges refining the question costs pennies of compute but can save hours of misdirected research and rework. Do not rush through articulation to "get to the research faster." Take time to think carefully about the person's request, consider multiple interpretations, and explore reframes before proposing the research question. The research is only as good as the question.

**The person knows more about their situation than you do.** Your job is to help them articulate what they already sense but haven't fully formed, not to redirect them toward what you think is interesting.

**Reframes are offers, not corrections.** When you suggest a different framing, present it as "here's another way to look at this" — never as "actually, the real question is." The person may have good reasons for their framing that you can't see.

**Brevity matters for the human, not for the model.** Keep the *human's* burden light — one question at a time, 2-4 exchanges max. But invest model thinking time generously between exchanges. Think through multiple possible interpretations, consider what assumptions are embedded, explore what adjacent questions might be more useful — do this work internally before each response. The person should experience a focused conversation, not an intake form. But behind each question should be genuine thought, not a reflexive checklist.

**Watch for convergent framing.** The most dangerous failure mode is when your training data biases and the person's assumptions align perfectly. If their question maps neatly onto a mainstream narrative, that's worth noting — not because the mainstream is wrong, but because easy alignment means neither of you is being challenged. Gently note this: "This is a well-trodden topic with strong consensus — do you want me to specifically look for dissenting or heterodox perspectives as well?"

## What This Skill Does NOT Do

- It does not research the topic. That comes later.
- It does not assess source quality or information availability. The blind-variables skill handles that.
- It does not produce a research plan. The deep-research skill handles that.
- It does not take more than 5 minutes of the person's time. Keep it tight.

## Handoff

Once the research question is confirmed, invoke the **blind-variables** skill with the confirmed question. The blind-variables skill will assess the information landscape and systematic distortions before research execution begins.

Carry forward what you learned along the way, not just the question: what the answer is for, and what the person already uses, knows or has ruled out. The deep-research skill records these in its research brief.
