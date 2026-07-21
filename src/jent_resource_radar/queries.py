from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class SearchTask:
    tier: str
    source: str
    purpose: str
    query: str
    url: str
    caution: str = ""


HIGH_SIGNAL_TERMS = (
    "主演 OR W主演 OR 出演決定 OR ドラマ OR 映画 OR 配信 OR "
    "新作 OR 解禁 OR 撮影 OR 10月期 OR 1月期 OR 4月期 OR 7月期"
)

OFFICIAL_DOMAINS = (
    "site:starto.jp OR site:ntv.co.jp OR site:tbs.co.jp OR "
    "site:fujitv.co.jp OR site:tv-asahi.co.jp OR site:tv-tokyo.co.jp OR "
    "site:nhk.jp OR site:netflix.com OR site:primevideo.com OR "
    "site:disneyplus.com"
)

MEDIA_DOMAINS = (
    "site:oricon.co.jp OR site:natalie.mu OR site:modelpress.jp OR "
    "site:thetv.jp OR site:mantan-web.jp OR site:mdpr.jp"
)


def _google_url(query: str) -> str:
    return f"https://www.google.com/search?q={quote_plus(query)}"


def _yahoo_realtime_url(query: str) -> str:
    return f"https://search.yahoo.co.jp/realtime/search?p={quote_plus(query)}"


def _x_url(query: str) -> str:
    return f"https://x.com/search?q={quote_plus(query)}&src=typed_query&f=live"


def _threads_url(query: str) -> str:
    return f"https://www.threads.com/search?q={quote_plus(query)}"


def _quoted_names(artist: str, aliases: list[str]) -> str:
    names = [artist, *aliases]
    return " OR ".join(f'"{name.strip()}"' for name in names if name.strip())


def build_search_tasks(
    artist: str,
    aliases: list[str] | None = None,
    window: str = "",
) -> list[SearchTask]:
    aliases = aliases or []
    names = _quoted_names(artist, aliases)
    window_term = f' "{window}"' if window.strip() else ""
    core = f"({names}) ({HIGH_SIGNAL_TERMS}){window_term}"
    sns_core = (
        f"({names}) (ドラマ OR 映画 OR 配信 OR 主演 OR 共演 OR "
        f"撮影 OR 目撃 OR 解禁 OR 近日){window_term}"
    )

    tasks = [
        SearchTask(
            tier="A",
            source="Official / Primary",
            purpose="事务所、电视台、平台、制作方的正式公告",
            query=f"{core} ({OFFICIAL_DOMAINS})",
            url=_google_url(f"{core} ({OFFICIAL_DOMAINS})"),
        ),
        SearchTask(
            tier="A",
            source="Official social accounts",
            purpose="节目官方账号、次日晨间预告、发布会和解禁信息",
            query=f"{sns_core} (公式 OR official)",
            url=_x_url(f"{sns_core} (公式 OR official)"),
            caution="X可能要求登录；只查看公开结果。",
        ),
        SearchTask(
            tier="B",
            source="Named entertainment media",
            purpose="可靠娱乐媒体、具名新闻和制作报道",
            query=f"{core} ({MEDIA_DOMAINS})",
            url=_google_url(f"{core} ({MEDIA_DOMAINS})"),
        ),
        SearchTask(
            tier="B",
            source="Weekly magazines / newspapers",
            purpose="周刊、报纸的内定或制作消息；仍不能视为官宣",
            query=f"{core} (内定 OR 関係者 OR 週刊誌 OR 報道)",
            url=_google_url(f"{core} (内定 OR 関係者 OR 週刊誌 OR 報道)"),
            caution="周刊报道属于媒体报道，不等于正式出演确认。",
        ),
        SearchTask(
            tier="C",
            source="X live search",
            purpose="公开目击、节目预告、粉丝repo与二手搬运",
            query=sns_core,
            url=_x_url(sns_core),
            caution="高转发量不等于真实性；检查原帖日期和来源。",
        ),
        SearchTask(
            tier="C",
            source="Yahoo!リアルタイム",
            purpose="日本X公开讨论的聚合检索",
            query=sns_core,
            url=_yahoo_realtime_url(sns_core),
            caution="注意旧帖重新传播、同文案复制和广告号。",
        ),
        SearchTask(
            tier="C",
            source="Threads",
            purpose="Threads上的公开粉丝讨论和资讯搬运",
            query=sns_core,
            url=_threads_url(sns_core),
            caution="部分结果可能需要登录；不访问私人账号。",
        ),
        SearchTask(
            tier="C",
            source="Filming traces",
            purpose="公开拍摄、エキストラ募集、ロケ与制作痕迹",
            query=f"{names} (エキストラ OR 撮影 OR ロケ OR クランクイン OR 目撃){window_term}",
            url=_google_url(
                f"{names} (エキストラ OR 撮影 OR ロケ OR クランクイン OR 目撃){window_term}"
            ),
            caution="只记录公开的制作线索，不扩散精确私人位置或行程。",
        ),
        SearchTask(
            tier="D",
            source="5ch",
            purpose="匿名论坛的信息号外溢、旧料复盘与真假争议",
            query=f"({names}) (情報垢 OR 漏洩 OR ドラマ OR 映画 OR 解禁) (site:5ch.net OR site:5ch.io)",
            url=_google_url(
                f"({names}) (情報垢 OR 漏洩 OR ドラマ OR 映画 OR 解禁) "
                f"(site:5ch.net OR site:5ch.io)"
            ),
            caution="匿名论坛内容必须标注未证实，并保留楼层与日期。",
        ),
        SearchTask(
            tier="D",
            source="Girls Channel",
            purpose="ガールズちゃんねる的讨论、信息号搬运和资源体感",
            query=f"({names}) (ドラマ OR 映画 OR 情報垢 OR 10月期 OR 1月期) site:girlschannel.net",
            url=_google_url(
                f"({names}) (ドラマ OR 映画 OR 情報垢 OR 10月期 OR 1月期) "
                f"site:girlschannel.net"
            ),
            caution="论坛共识不是事实；检查是否只是粉丝愿望或旧闻。",
        ),
        SearchTask(
            tier="D",
            source="Information-account spillover",
            purpose="公开区域对锁推或信息号内容的二手搬运",
            query=f"{names} (情報垢 OR 垢 OR 箱 OR 漏洩 OR 匂わせ OR 近日解禁){window_term}",
            url=_google_url(
                f"{names} (情報垢 OR 垢 OR 箱 OR 漏洩 OR 匂わせ OR 近日解禁){window_term}"
            ),
            caution="无法核对原文时必须写“二手外溢，无法验证原账号内容”。",
        ),
        SearchTask(
            tier="E",
            source="Cross-check",
            purpose="核对是否为重播、旧VTR、旧闻回收或已失败的历史料",
            query=f"{names} (再放送 OR 過去映像 OR VTR OR 未発表 OR ガセ OR 外れ OR 訂正)",
            url=_google_url(
                f"{names} (再放送 OR 過去映像 OR VTR OR 未発表 OR ガセ OR 外れ OR 訂正)"
            ),
            caution="先排除旧内容，再讨论是否为新资源。",
        ),
    ]
    return tasks
