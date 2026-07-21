from __future__ import annotations

from datetime import datetime, timezone

from .queries import SearchTask


def render_plan(
    artist: str,
    aliases: list[str],
    window: str,
    tasks: list[SearchTask],
) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    alias_text = "、".join(aliases) if aliases else "无"

    lines = [
        f"# {artist} 资源检索计划",
        "",
        f"- **时间范围：** {window or '未指定'}",
        f"- **别名/团名：** {alias_text}",
        f"- **生成时间：** {generated}",
        "",
        "> 原则：No receipts, no certainty。先官方，后媒体，再SNS，最后匿名论坛。",
        "",
    ]

    current_tier = None
    for index, task in enumerate(tasks, start=1):
        if task.tier != current_tier:
            current_tier = task.tier
            lines.extend([f"## Tier {current_tier}", ""])

        lines.extend(
            [
                f"### {index}. {task.source}",
                "",
                f"- **目的：** {task.purpose}",
                f"- **查询：** `{task.query}`",
                f"- **入口：** [打开检索]({task.url})",
            ]
        )
        if task.caution:
            lines.append(f"- **注意：** {task.caution}")
        lines.append("")

    lines.extend(
        [
            "## 记录模板",
            "",
            "| 日期 | 等级 | 来源 | 新信息 | 是否有原文 | 是否交叉验证 |",
            "|---|---|---|---|---|---|",
            "| YYYY-MM-DD | A-E | 来源名 | 一句话摘要 | 是/否 | 是/否 |",
            "",
            "## 完成检索后的结论规则",
            "",
            "- 有 Tier A：可写“已官宣”。",
            "- 只有 Tier B：写“可靠媒体报道，但尚未官宣”。",
            "- 只有 Tier C：写“公开SNS/repo，未获官方确认”。",
            "- 只有 Tier D：写“信息号或匿名论坛传闻”。",
            "- 只有 Tier E：只能作为分析，不得写成新资源。",
            "- 全部为空：写“截至检索时间，没有发现有意义的新进展”。",
        ]
    )
    return "\n".join(lines) + "\n"
