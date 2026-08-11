# StackOnward Organization Profile

## 目标

`stackonward/.github` 是远栈在 GitHub 的公开入口，负责表达品牌身份、公开能力、开源项目、已发布内容和有效联系方式。它不承担个人履历、公司法律身份、未公开产品路线或 OneX 内部架构披露。

## 行业参考

| 决策点 | 行业模式 | 参考 | 远栈选择 | 原因 |
|---|---|---|---|---|
| 组织主页入口 | `.github/profile/README.md` | [GitHub Organization Profile](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile) | 使用 GitHub 原生 Organization Profile | README 与最多六个精选仓库共同承担公开导航 |
| 识别系统 | 响应式品牌身份 | [Linear Brand](https://linear.app/brand)、[Vercel Geist Brands](https://vercel.com/geist/brands) | 字标、远迹符号和平台派生资产分工 | 小头像不反向限制横幅与内容排版 |
| 信息密度 | 身份、证据、入口 | [GitHub `.github`](https://github.com/github/.github)、[Microsoft `.github`](https://github.com/microsoft/.github) | 保留一个品牌视觉、一个能力图、一个当前项目和一个内容列表 | 避免把组织主页写成完整官网或技术清单 |
| 多栏视觉 | 固定比例视觉资产 + 原生语义文本 | [GitHub Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github) | 非对称 SVG 栅格负责层次，Markdown 负责链接与阅读 | GitHub 会限制自定义 CSS，原生表格无法稳定承担复杂响应式布局 |
| 内容刷新 | 仓库内计划任务 | [GitHub Actions scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) | 每日从公开 RSS 更新最近文章 | 只展示网站已经发布的权威版本，数据不变时不提交 |

## 公开信息架构

1. 品牌识别：名称、事实型描述、网站与联系方式。
2. 公开系统图：产品工程、商业系统、交付运维、开源工具和技术内容。
3. 当前开源项目：只展示已经公开且可验证的项目。
4. 最新内容：只读取 `stackonward.com/posts/` 下的公开文章。
5. 公开入口：网站、GitHub、npm、维护者和联系方式。

## 文案契约

- 使用事实型描述，不使用自我对话、机构拟人或宣传口号。
- 不使用“领先”“一站式”“赋能”“全方位”等无法验证的价值判断。
- 不宣称尚未成立的公司主体、尚未上线的产品或尚未开通的社媒账号。
- OneX 资料只用于提炼能力边界，不公开项目名称、客户、内部模块或实现状态。
- 当前核心描述为“软件产品、工程系统与技术内容”。

## 能力映射

| 公开层 | 资料来源 | 对外表达 |
|---|---|---|
| 产品工程 | 全栈、AI、身份、数据与架构资料 | 产品设计、AI、前端、后端、数据与架构 |
| 商业系统 | 商品、定价、订单、支付、订阅与权益资料 | 目录、定价、订单、支付与订阅 |
| 交付运维 | 云基础设施、网关、工作流、可观测与安全资料 | 云基础设施、CI/CD、可观测与安全 |
| 开源工具 | 已公开仓库与软件包入口 | 开发工具、自动化、脚本与模板 |
| 技术内容 | 远栈内容系统与网站公开文章 | 教程、设计决策、测评、复盘与资源 |

## 视觉系统

- 画布：`#F7F4ED`，正文与标志：`#111214`。
- 珊瑚色 `#D9786F` 只标记内容与商业节点；蓝色 `#3657B3` 只标记系统与交付节点。
- 能力图采用非对称十二栏构图：一个主区块、两个窄区块、一个小区块和一个横向区块，由一条低对比路径贯穿。
- 公开入口使用六栏表格：首行 `4 + 2`、次行 `2 + 2 + 2`，在 GitHub 内容区内保持满宽并建立层次。
- 横幅直接使用角色原图的自然留白承载文字，不使用覆盖人物的分区遮罩。
- SVG 内置暗色主题，不依赖 GitHub 页面自定义 CSS。
- 移动端按图片整体等比缩放，不产生横向滚动。

## 内容更新

```text
stackonward.com/index.xml
          │
          ▼
refresh_published_articles.py
          │
          ▼
profile/README.md 的受管文章区
```

刷新任务每天执行一次，也支持手动触发。RSS 解析、域名和路径边界、文章排序、Markdown 转义与原子写入均由单元测试覆盖。
