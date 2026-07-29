from __future__ import annotations

import argparse
from pathlib import Path

from common import utc_now, write_json


MODE_SIGNALS = {
    "research-mentor": (
        "professor", "researcher", "paper", "papers", "publication", "academic",
        "实验", "论文", "教授", "导师", "科研", "选题", "学者",
    ),
    "person-thinking": (
        "thinking", "mental model", "decision", "interview", "biography",
        "思维", "心智", "决策", "访谈", "人物", "价值观",
    ),
    "work-expert": (
        "colleague", "job", "sop", "email", "workflow", "work record",
        "同事", "岗位", "工作流", "邮件", "操作流程", "经验",
    ),
    "corpus": (
        "corpus", "knowledge base", "documents", "book", "archive", "library",
        "语料", "知识库", "文档", "资料库", "论文库", "书籍",
    ),
    "case-pattern": (
        "successful case", "failed case", "applications", "grant", "examples",
        "成功案例", "失败案例", "基金", "申请书", "范例", "案例",
    ),
    "project-retro": (
        "repository", "commits", "incident", "project history", "postmortem",
        "项目复盘", "代码库", "提交记录", "故障", "决策记录",
    ),
    "self-evolution": (
        "feedback", "correction", "mistake", "chat history", "preference",
        "反馈", "纠正", "错误", "聊天记录", "个人偏好", "持续改进",
    ),
}


def route(brief: str) -> dict:
    lowered = brief.lower()
    scores = {
        mode: sum(1 for signal in signals if signal in lowered)
        for mode, signals in MODE_SIGNALS.items()
    }
    ranked = sorted(scores, key=lambda mode: (-scores[mode], mode))
    matched = [mode for mode in ranked if scores[mode] > 0]
    if not matched:
        matched = ["corpus"]
    primary = matched[0]
    supporting = [mode for mode in matched[1:] if scores[mode] >= max(1, scores[primary] // 2)]
    reasons = [
        {"mode": mode, "matched_signal_count": scores[mode]}
        for mode in [primary, *supporting]
    ]
    return {
        "schema_version": 1,
        "primary_mode": primary,
        "supporting_modes": supporting,
        "scores": scores,
        "reasons": reasons,
        "reviewed": False,
        "generated_at": utc_now(),
        "warning": "Rule-based recommendation. Review against purpose and evidence before use.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend OmniDistill modes from a task brief.")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = route(args.brief)
    if args.output:
        write_json(args.output.resolve(), result)
        print(args.output.resolve())
    else:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
