#!/usr/bin/env python3
"""Count the patterns that make prose read as machine-written.

Reports each hit with its line and category, plus density figures, for Markdown or plain
text. Code (fenced and inline) is skipped. Categories follow references/voice.md:

  phrase        stock phrases ("plays a vital role", "in today's fast-paced world")
  word          vocabulary that clusters in generated text (delve, seamless, leverage)
  construction  not X but Y, "Whether you... or...", "No more X, no more Y", reveals,
                significance tacked on with a participle (", highlighting...")
  framing       announcing openers, summaries, closing offers and sign-offs
  format        emoji, hashtags, inline-header bullets, Title Case headings, heavy bold
  rhythm        em dashes and triads per 100 words; sentence lengths too uniform

What it cannot judge: whether a sentence is generic, whether a detail was invented,
whether the structure suits the reader. Those are the voice pass in references/voice.md.
A clean report means the countable tells are gone, not that the text reads as human.

Usage:
  ai_tells.py FILE [--allow emoji,hashtags] [--json]

Exit status: 0 no strong tells and densities within limits, 1 otherwise, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

PHRASES = [
    r"in today'?s (?:fast[- ]paced |digital |modern |ever[- ]changing )?(?:world|landscape|age|era)",
    r"plays? an? (?:vital|crucial|key|pivotal|significant|important) role",
    r"(?:stands|serves) as a (?:testament|reminder|beacon)", r"is a testament to",
    r"it'?s (?:important|worth|crucial) (?:to note|noting|to remember|to consider|mentioning)",
    r"it is (?:important|worth) (?:to note|noting)", r"at the heart of", r"a (?:wide|broad) range of",
    r"when it comes to", r"in the realm of", r"nestled in", r"rich (?:history|heritage|tapestry|legacy)",
    r"(?:enduring|lasting) (?:legacy|impact)", r"leaves? a lasting", r"watershed moment",
    r"(?:the )?tools? (?:\w+ )?(?:deserve|deserves)\b", r"treat you like family",
    r"take (?:it|your \w+) to the next level", r"look no further", r"game[- ]changer",
    r"unlock (?:the |your )?(?:full )?potential", r"navigate the complexities",
    r"(?:a|the) (?:delicate|intricate) (?:balance|interplay|dance)", r"stay (?:hydrated|ahead) in style",
    r"designed (?:with you in mind|to last)", r"(?:elevate|transform) (?:your|the way)",
]
WORDS = [
    "delve", "delves", "delving", "underscore", "underscores", "underscoring", "showcase", "showcases",
    "showcasing", "foster", "fosters", "fostering", "bolster", "bolsters", "garner", "garnered", "leverage",
    "leveraging", "elevate", "elevates", "empower", "empowers", "empowering", "unleash", "streamline",
    "streamlines", "embark", "harness", "harnessing", "spearhead", "revolutionize", "revolutionizes",
    "pivotal", "crucial", "seamless", "seamlessly", "robust", "cutting-edge", "innovative", "vibrant",
    "intricate", "multifaceted", "holistic", "meticulous", "meticulously", "transformative",
    "ever-evolving", "fast-paced", "game-changing", "landscape", "realm", "tapestry", "testament",
    "synergy", "paradigm", "interplay", "cornerstone", "beacon", "moreover", "furthermore",
    "additionally", "notably", "ultimately",
]
CONSTRUCTIONS = [
    (r"\bnot (?:just|only|merely|simply) (?:a |an |the )?[\w' -]{1,40}?[,;—–]? but (?:also )?", "not just X but Y"),
    (r"\b(?:it|this|that)(?:'s| is| was)(?: not|n't) (?:just |only |merely )?(?:about )?[\w' -]{1,40}[.;—–] ?(?:it|this|that)(?:'s| is| was) ", "not X. It's Y."),
    (r"\bwhether you(?:'re| are)? [^.?!\n]{3,80}? or ", "Whether you... or..."),
    (r"\bno more [\w' -]{1,30}, no more ", "No more X, no more Y"),
    (r"(?:^|[.!?]\s+)(?:the (?:result|answer|catch|kicker|truth|secret|best part|twist)|why)\?(?=\s)", "reveal question"),
    (r"\bhere'?s the (?:thing|kicker|catch|deal|truth)\b", "Here's the thing"),
    (r",\s(?:highlighting|underscoring|showcasing|reflecting|emphasizing|emphasising|signaling|signalling|cementing|solidifying|demonstrating|marking)\b", "significance tacked on"),
    (r"\b(?:experts|studies|research|many|observers|critics) (?:say|suggest|show|believe|note|argue)s?\b", "vague authority"),
]
OPENERS = [r"^(?:great|good|excellent) question", r"^(?:certainly|absolutely|of course|sure)[!,.]",
           r"^here'?s (?:a|an|the|your) (?:draft|version|post|email|rewrite|breakdown|overview)",
           r"^in this (?:post|article|guide|piece|blog)", r"^let'?s (?:dive|delve|explore|break)",
           r"^(?:big|exciting) news\b"]
CLOSERS = [r"\bi hope this helps\b", r"\blet me know if\b", r"\bfeel free to\b", r"\bhappy to help\b",
           r"^(?:in conclusion|in summary|to sum up|overall|all in all)\b", r"\b(?:want|would you like) me to\b",
           r"\bi can also (?:write|make|draft|create|do)\b", r"\bdon'?t hesitate to\b"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F⭐✅]")
HASHTAG = re.compile(r"(?:^|\s)#[A-Za-z][\w]+")
INLINE_HEADER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]{2,60}\*\*(?:\s*[:.—-]|\s+[a-z(])")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
TRIAD = re.compile(r"\b[\w'-]+(?: [\w'-]+){0,2}, [\w'-]+(?: [\w'-]+){0,2},? and [\w'-]+\b")
SMALL = {"a", "an", "the", "and", "or", "of", "in", "on", "for", "to", "at", "by", "with", "vs", "is"}
STRONG = {"phrase", "construction", "framing"}


def prose_lines(text: str):
    """(line number, text) for prose, with fenced and inline code removed."""
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            yield number, re.sub(r"`[^`\n]*`", "", line)


def check(text: str, allow: set[str]) -> dict:
    hits: list[dict] = []
    lines = list(prose_lines(text))
    body = "\n".join(l for _, l in lines)
    words = re.findall(r"[A-Za-z][\w'-]*", body)
    n_words = max(len(words), 1)

    def add(category, number, detail):
        hits.append({"category": category, "line": number, "detail": detail})

    first_prose = next((n for n, l in lines if l.strip() and not l.lstrip().startswith(("#", "---"))), None)
    last_prose = [n for n, l in lines if l.strip()][-3:]
    inline: list[int] = []
    for number, line in lines:
        low = line.lower().strip()
        stripped = re.sub(r"^[>*_\s-]+", "", low)
        for pat in PHRASES:
            for m in re.finditer(pat, low):
                add("phrase", number, m.group(0))
        for w in re.findall(r"[a-z][a-z'-]*", low):
            if w in WORDS:
                add("word", number, w)
        for pat, label in CONSTRUCTIONS:
            if re.search(pat, low):
                add("construction", number, label)
        if number == first_prose:
            for pat in OPENERS:
                if re.search(pat, stripped):
                    add("framing", number, "announcing opener")
        for pat in CLOSERS:
            if re.search(pat, stripped) and (number in last_prose or pat.startswith("^(?:in conclusion")):
                add("framing", number, "summary, offer or sign-off")
        if "emoji" not in allow and EMOJI.search(line):
            add("format", number, "emoji")
        if "hashtags" not in allow and not HEADING.match(line) and HASHTAG.search(line):
            add("format", number, "hashtag")
        if INLINE_HEADER.match(line):
            inline.append(number)
        h = HEADING.match(line)
        if h:
            ws = [w for w in re.findall(r"[A-Za-z][\w'-]*", h.group(2))]
            content = [w for w in ws[1:] if w.lower() not in SMALL]
            if len(ws) >= 3 and content and all(w[0].isupper() for w in content):
                add("format", number, "Title Case heading")

    if len(inline) >= 3:  # one bold lead is emphasis; a list of them is a template
        for number in inline:
            add("format", number, "inline-header bullet")
    bolds = len(BOLD.findall(body))
    dashes = body.count("—") + len(re.findall(r"\s--\s", body))
    triads = len(TRIAD.findall(body))
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body)) if len(s.split()) >= 3]
    lengths = [len(s.split()) for s in sentences]
    cv = statistics.pstdev(lengths) / statistics.mean(lengths) if len(lengths) >= 8 else None
    density = {
        "words": len(words),
        "em_dashes_per_100": round(dashes * 100 / n_words, 2),
        "triads_per_100": round(triads * 100 / n_words, 2),
        "bold_per_100": round(bolds * 100 / n_words, 2),
        "sentence_length_variation": round(cv, 2) if cv is not None else None,
        "ai_words_per_100": round(sum(h["category"] == "word" for h in hits) * 100 / n_words, 2),
    }
    # Heuristic density thresholds, not rules: one em dash or one triad is fine; a page
    # dense with them reads as generated. Each message states the rate it flags, so a
    # reader can judge a borderline case.
    limits = []
    if density["em_dashes_per_100"] > 0.5:
        limits.append("em dashes: more than one per 200 words")
    if density["triads_per_100"] > 0.7 and triads >= 3:
        limits.append("triads: three-item lists in most paragraphs")
    if density["bold_per_100"] > 1.5 and bolds >= 4:
        limits.append("bold: more than one span per 70 words")
    if cv is not None and cv < 0.3:  # stdev/mean of sentence lengths; edited prose varies more
        limits.append("rhythm: sentence lengths too uniform")
    if density["ai_words_per_100"] > 1.0 and len(words) >= 100:
        limits.append("vocabulary: tell-words cluster")
    for item in limits:
        add("rhythm", 0, item)
    strong = [h for h in hits if h["category"] in STRONG or h["detail"] in {"emoji", "hashtag", "inline-header bullet"}]
    return {"hits": hits, "density": density, "strong": len(strong), "limits": limits}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--allow", default="", help="comma list: emoji,hashtags (for platforms whose norms use them)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.file.is_file():
        print(f"error: {args.file} not found", file=sys.stderr)
        return 2
    result = check(args.file.read_text(encoding="utf-8"), {a.strip() for a in args.allow.split(",") if a.strip()})
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for h in result["hits"]:
            where = f"line {h['line']}" if h["line"] else "document"
            print(f"{where}: {h['category']}: {h['detail']}")
        d = result["density"]
        print(f"\n{len(result['hits'])} hit(s), {result['strong']} strong; {d['words']} words; "
              f"em dashes {d['em_dashes_per_100']}/100, triads {d['triads_per_100']}/100, "
              f"sentence-length variation {d['sentence_length_variation']}. "
              "Countable tells only: still read it as the reader (references/voice.md).")
    return 1 if result["strong"] or result["limits"] else 0


if __name__ == "__main__":
    sys.exit(main())
