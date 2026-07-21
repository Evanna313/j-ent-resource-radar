# 添加一个新的艺人

## 方式一：直接生成配置

```bash
jent-radar init \
  --artist "艺人日文名" \
  --aliases "团名,昵称,其他常用写法" \
  --window "2026年秋冬" \
  --output watchlists/artist-name.json
```

## 方式二：复制示例

复制：

```text
watchlists/example_generic.json
```

然后修改：

- `artist`
- `aliases`
- `window`

## 推荐别名

只添加公众常用、与职业信息检索相关的名称：

- 团体名
- 官方罗马字
- 常见昵称
- 姓名的异体字或中日文写法

不要加入私人账号、家属账号或可能指向私人身份的关键词。
