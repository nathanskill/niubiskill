#!/usr/bin/env python3
"""Validate the public NIUBI Skill repository without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "niubiskill"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        fail("SKILL.md frontmatter is not closed")

    result: dict[str, str] = {}
    for raw_line in block.splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            fail(f"unsupported frontmatter line: {raw_line}")
        key, value = raw_line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def main() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "NOTICE",
        ROOT / "AUTHOR.md",
        ROOT / "TRADEMARKS.md",
        ROOT / "METHOD_SOURCES.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "CHANGELOG.md",
        ROOT / "CITATION.cff",
        ROOT / "VERSION",
        SKILL / "SKILL.md",
        SKILL / "LICENSE",
        SKILL / "NOTICE",
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "commercial-loop.md",
        SKILL / "references" / "evidence-and-boundaries.md",
        ROOT / "tests" / "scenarios.json",
    ]
    for path in required:
        read(path)

    skill_text = read(SKILL / "SKILL.md")
    frontmatter = parse_frontmatter(skill_text)
    if set(frontmatter) != {"name", "description"}:
        fail("SKILL.md frontmatter must contain only name and description")
    if frontmatter["name"] != "niubiskill":
        fail("skill name must be exactly niubiskill")
    if len(skill_text.splitlines()) > 500:
        fail("SKILL.md must stay under 500 lines")

    openai_yaml = read(SKILL / "agents" / "openai.yaml")
    if '$niubiskill' not in openai_yaml:
        fail("agents/openai.yaml default_prompt must contain $niubiskill")
    if not re.search(r'display_name:\s*"NIUBI Skill"', openai_yaml):
        fail("agents/openai.yaml display_name must be NIUBI Skill")

    for relative in (
        "references/commercial-loop.md",
        "references/evidence-and-boundaries.md",
    ):
        if f"]({relative})" not in skill_text:
            fail(f"SKILL.md must link to {relative}")

    if "## A. 商业闭环卡" not in skill_text or "## B. 七天承诺实验" not in skill_text:
        fail("SKILL.md must enforce exactly the two named top-level output blocks")

    if (SKILL / "README.md").exists():
        fail("the installable skill package must not contain README.md")

    if read(ROOT / "LICENSE") != read(SKILL / "LICENSE"):
        fail("root and installable-package LICENSE files must be identical")
    if read(ROOT / "NOTICE") != read(SKILL / "NOTICE"):
        fail("root and installable-package NOTICE files must be identical")

    version = read(ROOT / "VERSION").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must use semantic version format such as 0.1.1")
    if f'version: "{version}"' not in read(ROOT / "CITATION.cff"):
        fail("CITATION.cff version must match VERSION")

    examples = sorted((ROOT / "examples").glob("*.md"))
    if len(examples) < 3:
        fail("at least three cross-industry synthetic examples are required")
    banned_case_terms = [
        "Blueberry",
        "MT4",
        "MT5",
        "外汇",
        "跟单",
        "niubang",
        "eaxau",
        "eaea.ai",
        "mql0",
        "huisucha",
    ]
    for path in examples:
        text = read(path)
        if "SYNTHETIC / 合成" not in text:
            fail(f"example lacks synthetic label: {path.name}")
        for term in banned_case_terms:
            if term.casefold() in text.casefold():
                fail(f"example contains a prohibited real-industry/project term: {path.name}: {term}")

    scenarios = json.loads(read(ROOT / "tests" / "scenarios.json"))
    if len(scenarios) < 10:
        fail("at least ten behavioral scenarios are required")
    ids: set[str] = set()
    for scenario in scenarios:
        if set(scenario) != {"id", "prompt", "must", "must_not"}:
            fail(f"invalid scenario fields: {scenario.get('id', '<missing>')}")
        if scenario["id"] in ids:
            fail(f"duplicate scenario id: {scenario['id']}")
        ids.add(scenario["id"])
        if not scenario["must"] or not scenario["must_not"]:
            fail(f"scenario needs positive and negative criteria: {scenario['id']}")

    text_extensions = {".md", ".yaml", ".yml", ".json", ".cff", ".py", ""}
    forbidden_narrow_terms = [
        "客户" + "经理",
        "account" + " manager",
        "account" + "-manager",
    ]
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        for term in forbidden_narrow_terms:
            if term.casefold() in relative.casefold():
                fail(f"narrow audience term found in path: {relative}")
        if path.is_file() and ".git" not in path.parts and path.suffix in text_extensions:
            content = path.read_text(encoding="utf-8", errors="ignore")
            forbidden_identifier = "niubi" + "-skill"
            if forbidden_identifier.casefold() in content.casefold():
                fail(f"hyphenated project identifier found in {path.relative_to(ROOT)}")
            for term in forbidden_narrow_terms:
                if term.casefold() in content.casefold():
                    fail(f"narrow audience term found in {relative}")

    print(f"PASS: niubiskill repository validation succeeded ({len(scenarios)} scenarios).")


if __name__ == "__main__":
    main()
