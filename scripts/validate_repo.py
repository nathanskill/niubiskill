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
        ROOT / "tests" / "README.md",
        SKILL / "SKILL.md",
        SKILL / "LICENSE",
        SKILL / "NOTICE",
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "monetization-patterns.md",
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
    description = frontmatter["description"]
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        fail("skill description must be non-empty, at most 1024 characters, and contain no angle brackets")
    if len(skill_text.splitlines()) > 120:
        fail("SKILL.md must stay under 120 lines; move optional detail to references")

    openai_yaml = read(SKILL / "agents" / "openai.yaml")
    if '$niubiskill' not in openai_yaml:
        fail("agents/openai.yaml default_prompt must contain $niubiskill")
    if not re.search(r'display_name:\s*"NIUBI Skill"', openai_yaml):
        fail("agents/openai.yaml display_name must be NIUBI Skill")
    short_match = re.search(r'short_description:\s*"([^"]+)"', openai_yaml)
    if not short_match or not 25 <= len(short_match.group(1)) <= 64:
        fail("agents/openai.yaml short_description must be 25-64 characters")

    readme_text = read(ROOT / "README.md")
    for snippet in (
        "## 3步，找到离钱最近的赚钱点",
        "npx -y skills add nathanskill/niubiskill -g --all",
        "$niubiskill https://你的项目网址",
        "你只需要描述项目",
    ):
        if snippet not in readme_text:
            fail(f"README.md is missing the simple first-use path: {snippet}")

    for relative in (
        "references/monetization-patterns.md",
        "references/commercial-loop.md",
        "references/evidence-and-boundaries.md",
    ):
        if f"]({relative})" not in skill_text:
            fail(f"SKILL.md must link to {relative}")

    legacy_outputs = (
        "## A. 商业" + "闭环卡",
        "## B. 七天" + "承诺实验",
        "## 一句话答案",
        "## 项目底牌与信息状态",
        "## 候选赚钱点",
        "## 唯一推荐",
        "## 七天验证",
        "## 本轮暂不测试",
    )
    if "# NIUBI 赚钱点" not in skill_text:
        fail("SKILL.md must enforce the concise NIUBI monetization output")
    if any(heading in skill_text for heading in legacy_outputs):
        fail("legacy verbose output headings must not remain in SKILL.md")
    if "**现在：** 引流 / 成交 / 暂停" not in skill_text:
        fail("SKILL.md must choose exactly one acquisition, closing, or pause route")
    for snippet in (
        "后台最多比较三个候选，前台只展开赢家",
        "证据值",
        "推导值",
        "实验参数",
        "不能证明整个市场",
        "闸门判断的是`下一步具体外部动作`",
    ):
        if snippet not in skill_text:
            fail(f"SKILL.md is missing a concise decision-discipline rule: {snippet}")

    patterns_text = read(SKILL / "references" / "monetization-patterns.md")
    if "## 新商业模式内容卡" not in patterns_text or "公开来源与日期" not in patterns_text:
        fail("monetization pattern library must include the reusable public content-card schema")

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
        if text.count("# NIUBI 赚钱点") != 1:
            fail(f"example lacks the concise single-card output: {path.name}")
        if len(text.splitlines()) > 60:
            fail(f"example is too long for the concise default output: {path.name}")
        if any(heading in text for heading in legacy_outputs):
            fail(f"example still contains a legacy verbose heading: {path.name}")
        for term in banned_case_terms:
            if term.casefold() in text.casefold():
                fail(f"example contains a prohibited real-industry/project term: {path.name}: {term}")

    scenarios = json.loads(read(ROOT / "tests" / "scenarios.json"))
    if len(scenarios) < 17:
        fail("at least seventeen behavioral scenarios are required")
    ids: set[str] = set()
    for scenario in scenarios:
        if set(scenario) != {"id", "prompt", "must", "must_not"}:
            fail(f"invalid scenario fields: {scenario.get('id', '<missing>')}")
        if scenario["id"] in ids:
            fail(f"duplicate scenario id: {scenario['id']}")
        ids.add(scenario["id"])
        if not scenario["must"] or not scenario["must_not"]:
            fail(f"scenario needs positive and negative criteria: {scenario['id']}")
    required_scenarios = {
        "T12-no-fake-price-scarcity",
        "T13-derived-capacity-reconciles",
        "T14-arbitrary-threshold-cannot-kill",
        "T15-assumption-does-not-become-claim",
        "T16-gate-the-action-not-project",
        "T17-repeat-run-calibration",
    }
    if not required_scenarios.issubset(ids):
        fail("behavior tests must cover numbers, assertions, action gating, and calibration")

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

    print(
        "PASS: niubiskill repository structure and "
        f"{len(scenarios)} behavioral scenario specifications validated."
    )


if __name__ == "__main__":
    main()
