#!/usr/bin/env python3
"""Build the source list for a research run, and score a run against the pipeline's conventions.

Usage:
  python3 runcheck.py sources <research-dir>          write sources.md, list citation problems
  python3 runcheck.py check   <research-dir> [--json] scorecard for the whole run

The scorecard also works on older runs that predate source IDs and verification files;
those simply fail the checks they do not meet, which gives a baseline to compare against.
"""
import datetime
import json
import os
import re
import statistics
import subprocess
import sys

THREAD_RE = re.compile(r"^(\d{2})-.+\.md$")
CITE_RE = re.compile(r"\[(\d{2}\.\d+)\]")
CLAIM_RE = re.compile(r"\bC(\d{2}\.\d+)\b")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
LINK_RE = re.compile(r"https?://|\b10\.\d{4,9}/\S+|\bPMID\b|\barXiv:|\bISBN\b", re.I)
SOURCE_LINE_RE = re.compile(r"^\s*(?:[-*]\s*)?\[(\d{2}\.\d+)\]\s*(.+)$")
LEGACY_SOURCE_RE = re.compile(r"^\s*(?:[-*]|\d+[.)]|\[\d+\])\s+\S")
ANY_CITE_RE = re.compile(
    r"\[\d{2}\.\d+\]|\[\d{1,3}\]|https?://|\[[^\]\n]*\b(?:19|20)\d{2}[a-z]?\b[^\]\n]*\]"
    r"|\([^()\n]*\b(?:19|20)\d{2}[a-z]?\b[^()\n]*\)"  # older style: (Author, 2024)
)
DECISION_HEADING_RE = re.compile(
    r"means for you|recommend|takeaway|strategy|protocol|shortlist|decide|decision|what to do|next steps",
    re.I,
)
REQUIRED_THREAD_SECTIONS = [
    "question", "key findings", "load-bearing claims", "sources", "confidence notes", "gaps",
]
STATUSES = ["confirmed", "partly", "not supported", "not accessible"]


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def split_sections(text):
    """Return [(heading, body)] split on level-2 headings; the part before the first is ''."""
    sections, heading, buf = [], "", []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            sections.append((heading, "\n".join(buf)))
            heading, buf = m.group(1), []
        else:
            buf.append(line)
    sections.append((heading, "\n".join(buf)))
    return sections


def norm(heading):
    return re.sub(r"[’`]", "'", heading).strip().lower()


def find_section(sections, prefix):
    for heading, body in sections:
        if norm(heading).startswith(prefix):
            return body
    return None


def title_of(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def parse_thread(path):
    text = read(path)
    name = os.path.basename(path)
    num = THREAD_RE.match(name).group(1)
    sections = split_sections(text)
    src_body = find_section(sections, "sources") or ""
    sources, legacy_sources = [], 0
    for line in src_body.splitlines():
        m = SOURCE_LINE_RE.match(line)
        if m:
            rest = m.group(2)
            tier = re.search(r"tier:\s*([a-z]+)", rest, re.I)
            readl = re.search(r"read:\s*([a-z]+)", rest, re.I)
            sources.append({
                "id": m.group(1), "line": line.strip().lstrip("-* ").strip(),
                "tier": tier.group(1).lower() if tier else None,
                "read": readl.group(1).lower() if readl else None,
                "has_link": bool(LINK_RE.search(rest)),
            })
        elif LEGACY_SOURCE_RE.match(line):
            legacy_sources += 1
    body_without_sources = "\n".join(b for h, b in sections if not norm(h).startswith("sources"))
    claims_body = find_section(sections, "load-bearing") or ""
    present = [s for s in REQUIRED_THREAD_SECTIONS if find_section(sections, s) is not None]
    return {
        "file": name, "num": num, "title": title_of(text, name), "words": len(text.split()),
        "body_words": len(body_without_sources.split()),
        "sources": sources, "legacy_sources": legacy_sources,
        "cited": CITE_RE.findall(body_without_sources),
        "claims": ["C" + c for c in CLAIM_RE.findall(claims_body)],
        "sections_present": present,
        "sections_missing": [s for s in REQUIRED_THREAD_SECTIONS if s not in present],
        "urls": set(URL_RE.findall(text)),
    }


def load_threads(rdir):
    names = sorted(n for n in os.listdir(rdir) if THREAD_RE.match(n))
    return [parse_thread(os.path.join(rdir, n)) for n in names]


def source_problems(threads):
    blocking, warnings = [], []
    all_ids = {}
    for t in threads:
        ids = [s["id"] for s in t["sources"]]
        if not t["sources"]:
            blocking.append(f"{t['file']}: no source entries in the [NN.n] format")
        for sid in ids:
            if ids.count(sid) > 1 and f"{t['file']}: duplicate source ID [{sid}]" not in blocking:
                blocking.append(f"{t['file']}: duplicate source ID [{sid}]")
            if not sid.startswith(t["num"] + "."):
                blocking.append(f"{t['file']}: source ID [{sid}] does not start with {t['num']}.")
            all_ids[sid] = t["file"]
    for t in threads:
        for sid in sorted(set(t["cited"])):
            if sid not in all_ids:
                blocking.append(f"{t['file']}: cites [{sid}] but no thread lists that source")
        own = {s["id"] for s in t["sources"]}
        unused = sorted(own - set(c for tt in threads for c in tt["cited"]))
        if unused:
            warnings.append(f"{t['file']}: listed but never cited: " + ", ".join(f"[{u}]" for u in unused))
        for s in t["sources"]:
            if not s["has_link"]:
                warnings.append(f"{t['file']}: [{s['id']}] has no URL, DOI or other identifier")
            if s["tier"] is None or s["read"] is None:
                warnings.append(f"{t['file']}: [{s['id']}] is missing tier: or read:")
            elif s["read"] == "snippet":
                warnings.append(f"{t['file']}: [{s['id']}] was only seen as a search snippet")
    return blocking, warnings


def tally(threads, key):
    out = {}
    for t in threads:
        for s in t["sources"]:
            out[s[key] or "unlabelled"] = out.get(s[key] or "unlabelled", 0) + 1
    return out


def cmd_sources(rdir):
    threads = load_threads(rdir)
    if not threads:
        print(f"No thread files (NN-name.md) found in {rdir}")
        return 1
    blocking, warnings = source_problems(threads)
    total = sum(len(t["sources"]) for t in threads)
    tiers, reads = tally(threads, "tier"), tally(threads, "read")
    readme = os.path.join(rdir, "README.md")
    topic = title_of(read(readme), os.path.basename(os.path.abspath(rdir))) if os.path.exists(readme) else os.path.basename(os.path.abspath(rdir))
    topic = re.sub(r"\s*[—-]\s*Research brief\s*$", "", topic)
    lines = [
        f"# Sources — {topic}", "",
        f"Built by runcheck.py on {datetime.date.today().isoformat()} from {len(threads)} thread files. "
        "Do not edit by hand: fix the thread file and rebuild.", "",
        f"{total} sources. By tier: " + ", ".join(f"{k} {v}" for k, v in sorted(tiers.items())) + ". "
        "By how much was read: " + ", ".join(f"{k} {v}" for k, v in sorted(reads.items())) + ".", "",
    ]
    for t in threads:
        lines += [f"## {t['num']} — {t['title']}", ""]
        lines += [f"- {s['line']}" for s in t["sources"]]
        lines.append("")
    with open(os.path.join(rdir, "sources.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote sources.md: {total} sources from {len(threads)} threads.")
    if blocking:
        print(f"\nPROBLEMS to fix ({len(blocking)}):")
        for b in blocking:
            print("  - " + b)
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print("  - " + w)
    if not blocking and not warnings:
        print("No problems found.")
    return 1 if blocking else 0


def parse_verification(rdir):
    path = os.path.join(rdir, "verification.md")
    legacy = os.path.exists(os.path.join(rdir, "verification-notes.md"))
    if not os.path.exists(path):
        return {"present": False, "legacy_notes": legacy, "rows": {}, "counts": {}}
    rows = {}
    for line in read(path).splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.fullmatch(r"C\d{2}\.\d+", cells[0]):
            status = cells[3].lower()
            rows[cells[0]] = next((s for s in STATUSES if status.startswith(s)), "other")
    counts = {s: sum(1 for v in rows.values() if v == s) for s in STATUSES + ["other"]}
    return {"present": True, "legacy_notes": legacy, "rows": rows, "counts": counts}


def find_report(rdir):
    names = os.listdir(rdir)
    for cand in ["REPORT.md", "synthesis.md"]:
        if cand in names:
            return cand
    others = sorted(n for n in names if "REPORT" in n.upper() and n.lower().endswith(".md"))
    return others[0] if others else None


def parse_report(rdir):
    name = find_report(rdir)
    if not name:
        return None
    text = read(os.path.join(rdir, name))
    sections = split_sections(text)
    headings = [norm(h) for h, _ in sections if h]
    src_body = find_section(sections, "sources") or ""
    listed = {m.group(1) for line in src_body.splitlines() if (m := SOURCE_LINE_RE.match(line))}
    legacy_listed = sum(1 for line in src_body.splitlines() if LEGACY_SOURCE_RE.match(line))
    skip = ("research question", "sources", "method note", "appendix")
    paragraphs = cited = 0
    cites = []
    for heading, body in sections:
        if norm(heading).startswith(skip):
            continue
        cites += CITE_RE.findall(body)
        for block in re.split(r"\n\s*\n", body):
            b = block.strip()
            if not b or b.startswith(("#", "|", "```")) or len(b.split()) < 40:
                continue
            paragraphs += 1
            cited += bool(ANY_CITE_RE.search(b))
    return {
        "file": name, "words": len(text.split()), "headings": headings,
        "cites": cites, "listed_ids": listed, "legacy_listed": legacy_listed,
        "urls": set(URL_RE.findall(text)),
        "paragraphs": paragraphs, "cited_paragraphs": cited,
        "has_summary": any(h.startswith("summary") for h in headings),
        "has_means_for_you": any(h.startswith("what this means for you") for h in headings),
        "has_decision_heading": any(DECISION_HEADING_RE.search(h) for h in headings),
        "has_doesnt_say": any("evidence doesn't say" in h for h in headings),
        "has_method_note": any(h.startswith("method note") for h in headings),
    }


def parse_brief(rdir):
    path = os.path.join(rdir, "README.md")
    if not os.path.exists(path):
        return {"present": False}
    sections = split_sections(read(path))
    deliverable = find_section(sections, "deliverable") or ""
    return {
        "present": True,
        "purpose": find_section(sections, "what this is for") is not None,
        "situation": find_section(sections, "your situation") is not None,
        "deliverable": bool(deliverable.strip()),
        "bias": any(norm(h).startswith("bias") for h, _ in sections),
        "threads": any(norm(h).startswith(("threads", "sub-questions")) for h, _ in sections),
        "decision_expected": bool(re.search(r"\bdecision", deliverable, re.I)),
    }


def git_info(rdir):
    def run(*args):
        try:
            return subprocess.run(["git", "-C", rdir, *args], capture_output=True, text=True, timeout=10)
        except Exception:
            return None
    top = run("rev-parse", "--show-toplevel")
    if not top or top.returncode != 0:
        return {"state": "none", "commits": []}
    own = os.path.realpath(top.stdout.strip()) == os.path.realpath(rdir)
    log = run("log", "--format=%s")
    commits = log.stdout.strip().splitlines() if log and log.returncode == 0 else []
    return {"state": "own" if own else "inside another repository", "commits": commits if own else []}


def cmd_check(rdir, as_json=False):
    threads = load_threads(rdir)
    brief, ver, report, git = parse_brief(rdir), parse_verification(rdir), parse_report(rdir), git_info(rdir)
    blocking, warnings = source_problems(threads) if threads else ([], [])
    all_sources = [s for t in threads for s in t["sources"]]
    source_ids = {s["id"] for s in all_sources}
    claims = [c for t in threads for c in t["claims"]]
    thread_urls = set().union(*[t["urls"] for t in threads]) if threads else set()
    words = [t["words"] for t in threads]
    body_words = [t["body_words"] for t in threads]
    sm_path = os.path.join(rdir, "sources.md")
    sm_ids = set(CITE_RE.findall(read(sm_path))) if os.path.exists(sm_path) else set()
    linked = sum(1 for s in all_sources if s["has_link"])
    unresolved_thread = sorted({c for t in threads for c in t["cited"]} - source_ids)

    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "result": "n/a" if ok is None else ("pass" if ok else "fail"), "detail": detail})

    add("Brief states purpose, situation and deliverable",
        brief.get("present") and brief.get("purpose") and brief.get("situation") and brief.get("deliverable"),
        "" if brief.get("present") else "no README.md")
    add("Brief has a bias note", bool(brief.get("present") and brief.get("bias")))
    add("Every thread has all required sections",
        bool(threads) and all(not t["sections_missing"] for t in threads),
        "; ".join(f"{t['file']} missing {', '.join(t['sections_missing'])}" for t in threads if t["sections_missing"])[:300])
    add("Every thread lists load-bearing claims", bool(threads) and all(t["claims"] for t in threads),
        f"{sum(1 for t in threads if t['claims'])}/{len(threads)} threads")
    add("Every citation in the threads resolves to a source",
        bool(all_sources) and not unresolved_thread,
        "no ID'd sources" if not all_sources else ", ".join(unresolved_thread)[:200])
    add("At least 90% of sources carry a link or identifier",
        bool(all_sources) and linked / len(all_sources) >= 0.9,
        f"{linked}/{len(all_sources)}" if all_sources else "no ID'd sources")
    add("sources.md is present and matches the threads",
        bool(source_ids) and sm_ids == source_ids,
        "missing" if not os.path.exists(sm_path) else f"{len(sm_ids)} IDs in sources.md vs {len(source_ids)} in threads")
    add("verification.md is present", ver["present"],
        "older verification-notes.md found" if ver["legacy_notes"] and not ver["present"] else "")
    covered = [c for c in claims if c in ver["rows"]]
    add("Every load-bearing claim has a verification result",
        bool(claims) and len(covered) == len(claims), f"{len(covered)}/{len(claims)} claims")
    add("A report is present", report is not None, report["file"] if report else "")
    if report:
        rep_ids = set(report["cites"])
        add("Every citation in the report resolves to a source",
            bool(rep_ids) and rep_ids <= source_ids,
            "no ID citations in report" if not rep_ids else ", ".join(sorted(rep_ids - source_ids))[:200])
        add("The report's Sources section lists every source it cites",
            bool(rep_ids) and rep_ids <= report["listed_ids"],
            "no ID citations in report" if not rep_ids else f"{len(rep_ids & report['listed_ids'])}/{len(rep_ids)} listed")
        share = report["cited_paragraphs"] / report["paragraphs"] if report["paragraphs"] else 0
        add("At least 80% of report paragraphs carry a citation", share >= 0.8,
            f"{report['cited_paragraphs']}/{report['paragraphs']} paragraphs")
        add("The report says what the evidence doesn't say", report["has_doesnt_say"])
        add("The report has a 'What this means for you' section when the brief names a decision",
            report["has_means_for_you"] if brief.get("decision_expected") else None,
            "" if brief.get("decision_expected") else "brief does not name a decision")
    if git["state"] == "own":
        msgs = git["commits"]
        trail = [any(m.startswith(p) for m in msgs) for p in ("Research plan", "Research complete")]
        if report:
            trail.append(any(m.startswith(("Final report", "Report")) for m in msgs))
        add("Git history shows each stage committed", all(trail), f"{len(msgs)} commits")
    else:
        add("Git history shows each stage committed", None, f"git: {git['state']}")

    passed = sum(1 for c in checks if c["result"] == "pass")
    applicable = sum(1 for c in checks if c["result"] != "n/a")
    metrics = {
        "run": os.path.abspath(rdir),
        "threads": len(threads),
        "thread_words_total": sum(words),
        "thread_words_min_median_max": [min(words), int(statistics.median(words)), max(words)] if words else [],
        "thread_body_words_min_median_max": [min(body_words), int(statistics.median(body_words)), max(body_words)] if body_words else [],
        "thread_body_words_by_file": {t["file"]: t["body_words"] for t in threads},
        "sources_with_ids": len(all_sources),
        "legacy_source_entries": sum(t["legacy_sources"] for t in threads),
        "sources_by_tier": tally(threads, "tier"),
        "sources_by_read": tally(threads, "read"),
        "unique_urls_in_threads": len(thread_urls),
        "load_bearing_claims": len(claims),
        "verification": ver["counts"] if ver["present"] else {},
        "report_file": report["file"] if report else None,
        "report_words": report["words"] if report else 0,
        "report_id_citations": len(report["cites"]) if report else 0,
        "report_unique_urls": len(report["urls"]) if report else 0,
        "report_cited_paragraph_share": round(report["cited_paragraphs"] / report["paragraphs"], 2) if report and report["paragraphs"] else None,
        "report_decision_heading": report["has_decision_heading"] if report else None,
        "research_to_report_ratio": round(sum(words) / report["words"], 1) if report and report["words"] and words else None,
        "git": git["state"], "commits": len(git["commits"]),
        "checks_passed": passed, "checks_applicable": applicable,
    }
    if as_json:
        print(json.dumps({"metrics": metrics, "checks": checks, "source_warnings": len(warnings)}, indent=2))
        return 0
    print(f"Run: {metrics['run']}")
    print(f"Checks passed: {passed}/{applicable}\n")
    for c in checks:
        mark = {"pass": "PASS", "fail": "FAIL", "n/a": " n/a"}[c["result"]]
        print(f"  {mark}  {c['check']}" + (f"  ({c['detail']})" if c["detail"] else ""))
    print("\nMeasurements")
    for k in ["threads", "thread_words_total", "thread_words_min_median_max",
              "thread_body_words_min_median_max", "sources_with_ids",
              "legacy_source_entries", "sources_by_tier", "sources_by_read", "unique_urls_in_threads",
              "load_bearing_claims", "verification", "report_file", "report_words", "report_id_citations",
              "report_unique_urls", "report_cited_paragraph_share", "report_decision_heading",
              "research_to_report_ratio", "git", "commits"]:
        print(f"  {k.replace('_', ' ')}: {metrics[k]}")
    if warnings:
        print(f"\nSource warnings: {len(warnings)} (run the 'sources' command to list them)")
    return 0


def main(argv):
    if len(argv) < 3 or argv[1] not in ("sources", "check"):
        print(__doc__)
        return 2
    rdir = argv[2]
    if not os.path.isdir(rdir):
        print(f"Not a directory: {rdir}")
        return 2
    if argv[1] == "sources":
        return cmd_sources(rdir)
    return cmd_check(rdir, as_json="--json" in argv[3:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
