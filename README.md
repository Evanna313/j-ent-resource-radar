# J-Ent Resource Radar 🎬🔎

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

> **A receipts-first entertainment monitoring toolkit, built by a technical fangirl.**

一个面向 **日本娱乐圈艺人新资源** 的公开信息检索与证据分级工具。  
它不负责“画饼”，只负责把公开线索整理成可复核的结论。

适用对象不限于某位艺人，可用于演员、偶像、歌手或团体，例如：

- 新电视剧、连续剧、SP
- 新电影
- Netflix、Prime Video、Disney+ 等配信作品
- 主演、W主演、主要番手
- 舞台、MC、CM 等重要个人资源
- X、Yahoo!リアルタイム、Threads、5ch、Girls Channel 等公开区域的信息号外溢

## About / 概要 / 项目简介

### English

J-Ent Resource Radar is a receipts-first research toolkit for monitoring upcoming work and public information about Japanese entertainers.

It follows a structured search order:

1. Official agencies, broadcasters, production companies, film distributors, and streaming platforms
2. Reliable entertainment media
3. Public discussions on X, Yahoo! Realtime Search, and Threads
4. Public rumor spillover from 5ch, Girls Channel, and information accounts
5. Cross-checking through project titles, co-stars, filming notices, schedules, and original sources

The toolkit clearly separates:

- Official confirmation
- Named media reporting
- Public SNS and fan reports
- Information-account and anonymous-forum rumors
- Analysis and speculation

It does not bypass private accounts, locked posts, paywalls, or access restrictions, and it does not collect private locations or personal schedules.

**No receipts, no certainty.**

---

### 日本語

J-Ent Resource Radar は、日本の芸能人に関する今後の出演情報や公開情報を、根拠を重視して調査・整理するためのツールキットです。

以下の順序で情報を確認します。

1. 所属事務所、テレビ局、制作会社、映画会社、配信プラットフォームなどの公式情報
2. 信頼できる芸能メディア
3. X、Yahoo!リアルタイム検索、Threads上の公開情報
4. 5ch、ガールズちゃんねる、情報垢などから公開範囲に流出した噂
5. 作品名、共演者、撮影情報、放送枠、原文などによるクロスチェック

調査結果は、以下のように明確に分類します。

- 公式発表
- 記名メディアによる報道
- 公開SNS・ファンレポ
- 情報垢・匿名掲示板の噂
- 分析・推測

非公開アカウント、鍵付き投稿、ペイウォール、アクセス制限を回避することはありません。また、私的な居場所や行動予定も収集しません。

**根拠がなければ、確定情報とは扱いません。**

---

### 中文

J-Ent Resource Radar 是一个面向日本娱乐圈的公开信息检索与证据分级工具，用于追踪艺人的电视剧、电影、流媒体作品、舞台、主持、广告及其他未来资源。

工具按照以下顺序进行检索：

1. 事务所、电视台、制作方、电影公司和流媒体平台的官方信息
2. 可靠且具名的娱乐媒体报道
3. X、Yahoo! 实时搜索和 Threads 的公开讨论
4. 5ch、Girls Channel 及信息号在公开区域的外溢信息
5. 通过项目名称、共演者、拍摄信息、档期和原始来源进行交叉核验

检索结果会明确区分：

- 已确认官宣
- 可靠媒体报道
- 公开SNS和粉丝repo
- 信息号及匿名论坛传闻
- 分析与推测

本项目不会绕过私人账号、锁推、付费墙或访问限制，也不会收集艺人的私人位置、航班、酒店或非公开行程。

**没有证据，就不写成确定消息。**

> Built by a technical fangirl who prefers receipts over rumors. 🎬🔎  
> 噂より根拠を重視する、技術系オタクによる小さな試みです。  
> 一个技术追星女关于“不要把传闻写成官宣”的小型开源实践。

---

## 核心理念：先看证据，再看情绪

| 等级 | 类型 | 例子 |
|---|---|---|
| A | 官宣 | 电视台、制作方、事务所、电影公司、平台 |
| B | 可靠媒体 | 具名媒体报道、周刊报道（仍非官宣） |
| C | 公开SNS / 粉丝repo | 官方预告、公开采访搬运、公开目击 |
| D | 信息号 / 匿名论坛 | 5ch、Girls Channel、匿名爆料、锁推外溢 |
| E | 推测 | 档期猜测、角色适配、粉丝愿望 |

**D 和 E 永远不能写成事实。**

---

## 项目内容

- `SKILL.md`：给 ChatGPT、Codex 或其他 AI 使用的标准检索流程
- `src/jent_resource_radar/`：Python 命令行工具
- `watchlists/`：艺人监测配置示例
- `examples/`：示例发现记录和报告
- `prompts/`：可直接复制给 AI 的检索提示词
- `docs/`：方法论与扩展说明
- `UPLOAD_TO_GITHUB.md`：小白友好的 GitHub 上传步骤
- `.github/workflows/ci.yml`：自动测试

---

## 它实际能做什么？

### 1. 生成完整的人工检索计划

工具会根据艺人姓名、团名、昵称和时间范围，生成：

- 官方与制作方检索
- 可靠媒体检索
- X 实时搜索
- Yahoo!リアルタイム搜索
- Threads 搜索
- 5ch 站内外检索
- Girls Channel 检索
- 拍摄、解禁、档期和共演线索关键词

```bash
jent-radar plan \
  --artist "渡辺翔太" \
  --aliases "Snow Man,しょっぴー,なべしょ" \
  --window "2026年秋冬" \
  --output reports/shota-plan.md
```

### 2. 把手工收集的线索整理成分级报告

把发现写入 JSON 后：

```bash
jent-radar report \
  --artist "渡辺翔太" \
  --window "2026年秋冬" \
  --findings examples/findings.example.json \
  --output reports/shota-report.md
```

报告会自动分成：

- 已确认官宣
- 可靠媒体报道
- 公开SNS / repo
- 信息号与匿名论坛传闻
- 推测
- 风险提示
- 当前结论

### 3. 生成艺人配置文件

```bash
jent-radar init \
  --artist "京本大我" \
  --aliases "SixTONES,きょも" \
  --window "2026年下半年" \
  --output watchlists/kyomoto-taiga.json
```

---

## 安装

需要 Python 3.10 或更高版本。

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

安装本项目：

```bash
pip install -e .
```

确认安装成功：

```bash
jent-radar --help
```

---

## 不会做什么

本项目坚持：

- 不绕过登录、锁推、验证码、付费墙或访问限制
- 不抓私人账号
- 不追踪航班、酒店、住址、电话或私人行程
- 不自动扩散匿名爆料
- 不把“搜不到”写成“确定没有”
- 不把旧VTR、重播或旧闻误写成新资源
- 不用其他艺人的负面消息证明目标艺人“被打压”

这会让项目没那么“黑科技”，但更安全、更可复核，也更适合公开上传 GitHub。

---

## 建议检索顺序

1. **官方**：事务所、电视台、制作方、电影公司、流媒体平台
2. **可靠媒体**：ORICON、映画ナタリー、音楽ナタリー、モデルプレス等
3. **公开SNS**：X、Yahoo!リアルタイム、Threads
4. **匿名论坛**：5ch、Girls Channel
5. **交叉核验**：检查日期、原文、是否为旧料回收，寻找第二来源
6. **输出结论**：明确区分官宣、报道、repo、传闻、推测

---

## 一句话定位

> **为日娱粉丝设计的公开信息 OSINT 工作流。**  
> Technical fangirl, but with receipts. 💙

---

## 开源协议

MIT License。欢迎 fork 并改造成你推的版本，但请保留隐私与证据分级原则。
