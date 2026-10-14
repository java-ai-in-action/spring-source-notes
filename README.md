# Spring 源码现形记 · Spring Source Notes

> 面试官追着你问的那 10 个类 —— 配《Spring 源码现形记》公众号系列

选 Spring 全家桶里 10 个核心类，**从一行关键方法切入，把源码走通**，再回答面试官最爱追问的"为什么"。

所有源码结论均基于官方仓库稳定分支**逐行核对**（Spring Framework **6.2.x** / Spring Boot **3.4.x**），不凭印象写 API。每篇配 5 张带文字标注的信息图，辅助阅读。

## 目录

| # | 篇名 | 核心源码 |
|---|---|---|
| 1 | [IoC 容器 refresh() 全流程：Spring 启动到底干了啥](articles/src1-article.md) | `AbstractApplicationContext.refresh()` |
| 2 | [Bean 生命周期：从 new 到可用，四步源码谁先谁后](articles/src2-article.md) | `doCreateBean` / `initializeBean` |
| 3 | [三级缓存与循环依赖：为什么构造器注入救不了](articles/src3-article.md) | `getSingleton` / `addSingletonFactory` |
| 4 | [@Autowired 注入源码：字段怎么被反射 set 进去的](articles/src4-article.md) | `AutowiredFieldElement.inject` / `determineAutowireCandidate` |
| 5 | [AOP 代理生成：Spring 怎么决定用 JDK 还是 CGLIB](articles/src5-article.md) | `DefaultAopProxyFactory.createAopProxy` / `proceed()` |
| 6 | [@Transactional 事务失效：问题从来不在注解，在代理](articles/src6-article.md) | `TransactionInterceptor.invokeWithinTransaction` |
| 7 | [Spring MVC 请求全链路：doDispatch 到底做了什么](articles/src7-article.md) | `DispatcherServlet.doDispatch` |
| 8 | [Spring Boot 自动配置原理：@ConditionalOnMissingBean 到底"少"了什么](articles/src8-article.md) | `AutoConfigurationImportSelector` / `ImportCandidates` |
| 9 | [Spring 扩展点全景：BFP 和 BP 差一个字，差了一个世界](articles/src9-article.md) | `initializeBean` / `PostProcessorRegistrationDelegate` |
| 10 | [Spring 里的设计模式：那些"长得像"的类，差在哪](articles/src10-article.md) | `FactoryBean` / `ApplicationContext` |

## 推荐阅读路径

- **主线通关（推荐）**：1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10，从容器启动到设计哲学，层层递进；
- **面试急救**：3（循环依赖）+ 6（事务失效），面试最高频的两个坑；
- **Web 方向**：1 → 2 → 9 → 5 → 7（IoC → 生命周期 → 扩展点 → AOP → MVC）；
- **Boot 专项**：8 + 9（自动配置 + 扩展点）。

## 仓库结构

```
spring-source-notes/
├── README.md              # 本文件（系列导读）
├── articles/              # 10 篇正文（Markdown）
│   └── srcN-article.md
├── images/                # 每篇 5 张信息图（50 张）
│   └── srcN-<名称>.jpg
└── scripts/               # 绘图脚本（matplotlib，可复现配图）
    └── draw_srcN_figs.py
```

## 每篇的固定规格

1. 正文约 2800 字：故事开场 → 旧问法 vs 新问法对照 → 源码推演 → 加分点 → 速查表 + 动手验证；
2. 5 张科技蓝信息图（matplotlib 代码绘制，带准确文字标注），逐张核验；
3. 源码基于官方仓库稳定分支逐行核对，版本在文首注明；
4. 附"动手验证"清单，读完可自己跑一遍。

## 姊妹系列

- **《八股变形记》**：讲"考点怎么问"——面试官不再考你会不会背，而是问线上怎么处理；
- **《Spring 源码现形记》**（本系列）：讲"源码为什么这么写"。

## License

文章内容版权归作者所有，转载请注明出处。代码片段与绘图脚本可自由使用。
