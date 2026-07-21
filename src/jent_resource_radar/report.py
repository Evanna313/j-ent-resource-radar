from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Iterable

from .models import EvidenceTier, Finding, TIER_NAMES


def _finding_block(finding: Finding) -> list[str]:
    icon = {
        "new": "🆕",
        "unchanged": "➖",
        "debunked": "❌",
        "unclear": "❓",
    }[finding.status]

    lines = [
        f"### {icon} {finding.headline}",
        "",
        f"- **来源：** [{finding.source_name}]({finding.url})",
        f"- **发布日期：** {finding.published_at}",
        f"- **状态：** {finding.status}",
        f"- **摘要：** {finding.summary}",
    ]
    if finding.corroboration:
        lines.append(f"- **交叉验证：** {finding.corroboration}")
    if finding.notes:
        lines.append(f"- **备注：** {finding.notes}")
    lines.append("")
    return lines


def render_report(
    artist: str,
    window: str,
    findings: Iterable[Finding],
) -> str:
    finding_list = list(findings)
    grouped: dict[EvidenceTier, list[Finding]] = defaultdict(list)
    for finding in finding_list:
        grouped[finding.tier].append(finding)

    meaningful = [
        item
        for item in finding_list
        if item.status == "new" and item.tier in {EvidenceTier.A, EvidenceTier.B}
    ]
    official = [item for item in meaningful if item.tier == EvidenceTier.A]
    media_only = [item for item in meaningful if item.tier == EvidenceTier.B]

    if official:
        bottom_line = (
            f"发现 {len(official)} 条新的官方确认。可将对应项目视为已官宣，"
            "但仍需核对播出/上映时间和番手。"
        )
    elif media_only:
        bottom_line = (
            f"发现 {len(media_only)} 条新的可靠媒体报道，但没有新的官方确认。"
            "应写成“媒体报道/内定传闻”，不能写成已官宣。"
        )
    elif finding_list:
        bottom_line = (
            "发现了一些公开讨论或传闻，但没有足以确认新影视资源的高等级证据。"
        )
    else:
        bottom_line = (
            "截至本次检索，没有发现有意义的新进展。"
            "这只代表公开信息层面暂无证据，不等于艺人没有未公开工作。"
        )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# {artist} 资源检测报告",
        "",
        f"- **关注窗口：** {window or '未指定'}",
        f"- **生成时间：** {generated}",
        f"- **发现总数：** {len(finding_list)}",
        "",
        "## 结论",
        "",
        bottom_line,
        "",
    ]

    for tier in EvidenceTier:
        lines.extend([f"## Tier {tier.value}｜{TIER_NAMES[tier]}", ""])
        tier_findings = sorted(
            grouped.get(tier, []),
            key=lambda item: (item.published_at, item.headline),
            reverse=True,
        )
        if not tier_findings:
            lines.extend(["暂无记录。", ""])
            continue
        for finding in tier_findings:
            lines.extend(_finding_block(finding))

    lines.extend(
        [
            "## 风险提示",
            "",
            "- 未看到外溢，不等于没有未公开项目。",
            "- 信息号反复重复同一句话，不构成独立交叉验证。",
            "- 周刊“内定”报道仍可能出现调档、降板或企划取消。",
            "- 旧VTR、重播、旧作上架和回顾SP不属于新出演。",
            "- 公开拍摄repo只能证明可能存在制作活动，不能自动确认角色与番手。",
            "",
            "## 下一轮建议",
            "",
            "1. 先复查电视台、制作方、事务所和平台官方页面。",
            "2. 对新增媒体报道搜索标题原句与制作公司。",
            "3. 在X、Yahoo!リアルタイム、Threads寻找原始公开帖。",
            "4. 最后查看5ch与Girls Channel，记录楼层、日期和质疑意见。",
        ]
    )
    return "\n".join(lines) + "\n"
