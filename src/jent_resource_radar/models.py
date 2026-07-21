from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EvidenceTier(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


TIER_NAMES: dict[EvidenceTier, str] = {
    EvidenceTier.A: "官宣 / Official",
    EvidenceTier.B: "可靠媒体 / Named media",
    EvidenceTier.C: "公开SNS或粉丝repo / Public SNS",
    EvidenceTier.D: "信息号或匿名论坛 / Rumor ecosystem",
    EvidenceTier.E: "推测 / Analysis",
}

VALID_STATUSES = {"new", "unchanged", "debunked", "unclear"}


@dataclass(frozen=True)
class Finding:
    tier: EvidenceTier
    headline: str
    source_name: str
    url: str
    published_at: str
    summary: str
    status: str = "new"
    corroboration: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Finding":
        missing = [
            key
            for key in ("tier", "headline", "source_name", "url", "published_at", "summary")
            if not str(raw.get(key, "")).strip()
        ]
        if missing:
            raise ValueError(f"Finding is missing required fields: {', '.join(missing)}")

        try:
            tier = EvidenceTier(str(raw["tier"]).upper())
        except ValueError as exc:
            raise ValueError("tier must be one of A, B, C, D or E") from exc

        status = str(raw.get("status", "new")).lower()
        if status not in VALID_STATUSES:
            raise ValueError(
                f"status must be one of {', '.join(sorted(VALID_STATUSES))}"
            )

        return cls(
            tier=tier,
            headline=str(raw["headline"]).strip(),
            source_name=str(raw["source_name"]).strip(),
            url=str(raw["url"]).strip(),
            published_at=str(raw["published_at"]).strip(),
            summary=str(raw["summary"]).strip(),
            status=status,
            corroboration=str(raw.get("corroboration", "")).strip(),
            notes=str(raw.get("notes", "")).strip(),
        )
