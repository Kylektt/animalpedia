# 动物数据约定（待团队确认的草案）

先统一这个格式，再并行做列表、详情和内容。建议初版使用静态 JSON，每种动物一个文件：`data/animals/<id>.json`。此约定不绑定前端框架。

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| id | string | 稳定的英文短标识，用于详情路由 |
| nameZh | string | 中文名称 |
| nameEn | string | 英文名称 |
| scientificName | string | 学名 |
| category | string | 团队约定的分类筛选值 |
| summary | string | 简介 |
| habitat | string | 栖息地 |
| diet | string | 食性 |
| sources | Source[] | 事实依据，真实内容至少一项 |
| image | Image 或 null | 有许可记录的图片；为空时用占位图 |

`Source`：`id`、`title`、`url`、`accessedAt`（YYYY-MM-DD）、`supports`（该来源支持的字段名数组）。

`Image`：`url`、`alt`、`sourceUrl`、`creator`、`license`、`licenseUrl`、`attribution`。

约束：

- `id` 唯一，采用小写英文、数字和连字符；详情地址由前端初始化任务统一确定。
- 列表和详情使用同一份数据，不分别维护动物名称或简介。
- `category` 的允许值由团队在开始整理内容前确认。
- 图片缺失不应阻止页面展示。
- 不明确的事实暂时省略；不要为了填满字段而编造。
- 需要保护等级、体重、寿命等新字段时，一并约定单位、来源和时间范围。

这份文件是工作草案，目前尚无加载器或校验器实现。
