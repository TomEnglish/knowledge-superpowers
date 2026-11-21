---
name: blind-variables
description: >
  This skill should be used after a research question has been articulated (via the articulate
  skill) and before research execution begins. It performs a per-topic analysis of systematic
  distortions in the available information — identifying where the training corpus, scientific
  institutions, research economics, social norms, and AI safety filtering have created blind
  spots, amplified certain narratives, or suppressed others. Use this skill whenever beginning
  a research project, when the user says "what am I missing", "what's the other side",
  "is this biased", "what don't we know about this", or when a topic touches areas known
  to be distorted by funding incentives, publication bias, social stigma, or AI guardrails.
  Also trigger when the articulate skill hands off a confirmed research question.
---

# Blind Variables

Every topic that passes through an LLM has been pre-filtered through at least four layers of systematic distortion before it reaches the model's weights. This skill makes those distortions visible and produces a "bias map" that travels with the research — shaping how sub-questions are designed, which sources are sought, and how confidence is calibrated in the final output.

This is not a review step. It is a **lens** applied before research begins.

**Invest thinking time here.** This analysis is the highest-leverage use of LLM compute in the entire pipeline. A thorough bias map costs minutes of model time and reshapes every subsequent research decision. A skipped or superficial bias map means the research silently inherits every distortion in the training data. Read the distortion-examples reference file. Think carefully about which layers apply to this specific topic and how they interact. Do not rush to produce a generic map — a generic bias map is worse than none because it creates the illusion of having accounted for something.

## The Four Distortion Layers

For the confirmed research question, analyze each layer and assess its likely impact. Not every layer affects every topic equally. Be specific — generic disclaimers about "bias" are worthless. The value is in identifying *how this specific topic* is distorted.

### Layer 1: Research Economics — What Gets Studied

Funding shapes the landscape of available knowledge. Ask:

- **Who pays for research on this topic?** Government grants, pharmaceutical companies, tech firms, military, foundations? Each funder creates selection pressure on what questions get asked and what findings get amplified.
- **What's the commercial incentive structure?** Topics with profitable applications attract disproportionate research. Topics without commercial value get neglected regardless of their importance.
- **What doesn't get studied?** Negative results, replication studies, low-profit interventions, prevention vs. treatment, anything that threatens an established revenue stream. The absence of research is not evidence of absence — it is often evidence of economics.
- **What's the publication incentive?** Novel positive findings get published. Replications, null results, and incremental refinements often don't. This creates a literature that systematically overstates effect sizes and novelty.

### Layer 2: Institutional Amplification — What Gets Published and Repeated

Not all published research carries equal weight in the training corpus. Ask:

- **Where does the consensus live?** High-prestige journals (Nature, Science, Lancet) dominate the training data. Findings published there get repeated across secondary sources, textbooks, and popular science — compounding their weight in the corpus regardless of whether they replicate.
- **What's the citation network effect?** Heavily-cited papers attract more citations. Early influential papers shape the frame for decades even if later work complicates or contradicts them.
- **Is there a paradigm lock?** Established frameworks resist revision. If the dominant theory has been stable for decades, ask whether that's because it's well-established or because alternative frameworks can't get published, funded, or taken seriously.
- **What's the review article effect?** Review articles and meta-analyses dominate the training data because they're widely cited. But they inherit the selection biases of the primary literature they review. A meta-analysis of biased studies produces a confidently biased conclusion.

### Layer 3: Social and Cultural Filtering — What's Allowed

Social norms shape what gets researched honestly, what gets researched defensively, and what doesn't get researched at all. Ask:

- **Is this topic stigmatized?** Research on stigmatized topics (certain drugs, sexual behavior, controversial therapies, politically charged hypotheses) often has to perform ideological genuflection to get published. The research that exists may be framed defensively rather than honestly.
- **Has the Overton window shifted?** Topics that were mainstream 20 years ago may now be unspeakable, and vice versa. The training data contains both eras, creating contradictions the model papers over with false balance.
- **Are there cultural blind spots?** Western, English-language, institutional perspectives dominate the corpus. Traditional knowledge systems, non-English research, indigenous perspectives, and non-institutional expertise are systematically underrepresented.
- **Is there a moral panic or hype cycle?** Topics currently in the public spotlight get distorted by media amplification. The training data may contain a surge of low-quality, opinion-heavy, sensationalized content that drowns out careful earlier work.

### Layer 4: AI Training Filters — What the Model Won't Touch

The model's own training process creates the final layer of distortion. Ask:

- **Is this topic adjacent to safety-filtered content?** Models learn avoidance patterns that extend beyond actually harmful content. Topics adjacent to violence, drugs, sexuality, self-harm, or political extremism may trigger learned caution that manifests as hedging, false balance, or refusal to engage with legitimate aspects of the topic.
- **Does RLHF favor a particular framing?** Reinforcement learning from human feedback rewards responses that feel helpful, harmless, and honest — but "harmless" can mean "avoids anything that might upset anyone," which is not the same as "accurate." On contested topics, the model may default to a diplomatic center that doesn't actually exist in the evidence.
- **Is the model likely to confabulate confidence?** On topics where the training data is thin, the model may produce fluent, well-structured output that *sounds* authoritative but is actually interpolating between sparse data points. Thin data + fluent generation = confident bullshit.
- **What would the model refuse to say?** Not because it's harmful, but because it's been trained to avoid controversy. The most interesting findings on many topics are precisely the ones the model is most reluctant to state plainly.

## Output: The Bias Map

After analyzing all four layers, produce a concise bias map for the research question. Format:

```
## Bias Map: [Research Question]

### Information Landscape
- **Strong coverage**: [areas where information is likely abundant and reliable]
- **Weak coverage**: [areas where information is likely sparse, outdated, or absent]
- **Distorted coverage**: [areas where information exists but is likely skewed]

### Key Distortions
1. [Specific distortion with layer identified, e.g., "Pharmaceutical funding dominates research on X, creating systematic preference for drug interventions over lifestyle changes (Layer 1)"]
2. [Next distortion]
3. [Next distortion]

### Compensation Strategy
- [Specific research actions to counteract identified distortions, e.g., "Seek pre-2005 literature before the current paradigm locked in", "Look for research from non-English sources", "Specifically search for null results and failed replications"]

### Confidence Calibration
- [Where should the final output be presented with high confidence vs. explicit uncertainty?]
```

Keep the bias map under 300 words. It needs to be compact enough to travel with the research as working context without consuming excessive tokens.

## Handoff

Once the bias map is produced and shown to the user, hand off to the **deep-research** skill with both the confirmed research question and the bias map. The research plan should explicitly incorporate the compensation strategies identified here.

## What This Skill Does NOT Do

- It does not help frame the question. The articulate skill already did that.
- It does not conduct research. It maps the terrain before research begins.
- It does not claim to eliminate bias. It makes bias visible so the research can work with and against it consciously rather than inheriting it silently.

## Additional Reference

For detailed examples of how each distortion layer manifests across different topic domains, see `references/distortion-examples.md`.
