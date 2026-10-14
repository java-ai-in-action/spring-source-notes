# IoC 容器 refresh() 全流程：Spring 启动到底干了啥

> 《Spring 源码现形记》第 1 篇 ｜ 本文源码基于 Spring Framework 6.2.x 分支

![IoC容器封面：工厂与图纸](../images/src1-fengmian.jpg)

## 一个让大厂候选人当场沉默的问题

上周一个粉丝去面某大厂，前面聊得顺风顺水，直到面试官慢悠悠扔出一句：

"你说你熟悉 Spring，那容器启动的时候，`refresh()` 方法里到底做了哪几步？"

他背过的八股是"IoC 是控制反转，DI 是依赖注入"，当场卡壳。

更扎心的是面试官的补刀："你连 Spring 启动时干了什么都说不上来，线上出了 Bean 初始化问题，你怎么下手？"

这道题不是为了为难人——`refresh()` 是整个 Spring 的"总装车间"，后面的事务失效、循环依赖、Bean 生命周期，全部挂在它的流程上。这一篇，我们把这条流水线走通。

## 旧问法 vs 新问法

| 旧问法（背就完事） | 新问法（要真读过源码） |
|---|---|
| 什么是 IoC / DI？ | `refresh()` 十二步里，BeanDefinition 是怎么注册进容器的？ |
| BeanFactory 和 ApplicationContext 什么区别？ | 为什么说 BeanDefinition 是"说明书"，BeanFactory 是"工厂"？ |
| 说一下 Spring 的启动流程 | 为什么 `invokeBeanFactoryPostProcessors` 必须排在 `registerBeanPostProcessors` 前面？ |

旧问法考概念，新问法考你**有没有真跟过一遍启动链路**。三道新问法，读完这一篇你都能接住。

## 从一行你最熟的代码开始

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
```

这一行背后藏着三个动作（6.2.x 真实源码）：

```java
public AnnotationConfigApplicationContext(Class<?>... componentClasses) {
    this();                     // ① 内部工厂在这里就 new 好了
    register(componentClasses); // ② 把配置类注册成 BeanDefinition
    refresh();                  // ③ 容器启动总开关
}
```

先纠正一个流传很广的误解：**容器不是在 `refresh()` 里才创建工厂的**。看它的父类 `GenericApplicationContext` 的构造器——

```java
public GenericApplicationContext() {
    this.beanFactory = new DefaultListableBeanFactory();
}
```

工厂（`DefaultListableBeanFactory`）在构造阶段就建好了。`register(AppConfig.class)` 只是把你的配置类**登记成一张"图纸"**（BeanDefinition），此刻容器里没有任何真实对象。真正的重头戏是 `refresh()`。

## refresh() 十二步：三段流水线

![refresh十二步流程](../images/src1-flow.jpg)

先上原文骨架（只保留主干，异常兜底后面单独讲）：

```java
public void refresh() throws BeansException, IllegalStateException {
    this.startupShutdownLock.lock();   // 新版已改用显式锁，面试提一嘴是加分项
    try {
        prepareRefresh();
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
        prepareBeanFactory(beanFactory);
        try {
            postProcessBeanFactory(beanFactory);
            invokeBeanFactoryPostProcessors(beanFactory);
            registerBeanPostProcessors(beanFactory);
            initMessageSource();
            initApplicationEventMulticaster();
            onRefresh();
            registerListeners();
            finishBeanFactoryInitialization(beanFactory);
            finishRefresh();
        } catch (RuntimeException | Error ex) {
            destroyBeans();      // 已创建的单例全部销毁
            cancelRefresh(ex);   // active 标志复位
            throw ex;
        } finally { /* ... */ }
    } finally {
        this.startupShutdownLock.unlock();
    }
}
```

十二步看着眼晕？按功能分三段，每段一句话就能记住。

### 第一段（1~3 步）：搭台子

**第 1 步 `prepareRefresh()`**：打启动时间戳、把 `active` 标志置为 true、校验必填属性、准备一个"早期事件"暂存区（这些事件攒着，等广播器就位后再补发）。细节不考点，记住它是"状态准备"。

**第 2 步 `obtainFreshBeanFactory()`**：拿到容器里最核心的对象——`DefaultListableBeanFactory`。这里有个能区分"读过源码"和"背过面经"的细节，两种子类实现完全不同：

- **XML 时代**（`AbstractRefreshableApplicationContext`）：每次 refresh 都 `createBeanFactory()` 造一个新工厂，再 `loadBeanDefinitions()` 重新加载——所以 XML 配置改了之后，`refresh()` 一下就能生效；
- **注解时代**（`AnnotationConfigApplicationContext` 的父类 `GenericApplicationContext`）：工厂构造期已建好，`refreshBeanFactory()` 里只做了一个 CAS 防重复刷新，**绝不重建**。

**第 3 步 `prepareBeanFactory()`**：给工厂"装机"——设置 ClassLoader 和 SpEL 解析器，注册 `ApplicationContextAwareProcessor`，还有一处很多人说不清来源的逻辑：把 `BeanFactory`、`ApplicationContext` 等 4 个对象注册为"可解析依赖"。**这就是为什么你的任意 Bean 里可以直接 `@Autowired ApplicationContext`**——容器自己被提前登记进了依赖解析白名单。

### 第二段（4~6 步）：图纸的注册与加工——全篇最重要

**第 4 步 `postProcessBeanFactory()`**：留给子类的钩子，默认空实现（Web 应用在这一步补充 Servlet 相关的 Scope）。知道即可。

**第 5 步 `invokeBeanFactoryPostProcessors()`**：**你的 `@Configuration`、`@ComponentScan`、`@Bean`，全部在这一步变成 BeanDefinition。**

展开说：`ConfigurationClassPostProcessor` 是一个 BeanFactoryPostProcessor（BFPP），它在这一步被触发，解析你的配置类——`@ComponentScan` 扫出的每个 `@Component`、每个 `@Bean` 方法，统统转成 BeanDefinition，塞进 `DefaultListableBeanFactory` 内部的 `beanDefinitionMap`。

![BeanDefinition注册链路](../images/src1-bd.jpg)

划重点：**到这一步为止，容器里只有"图纸"，没有一个真实的 Bean 被创建。**

这里埋着一个高频追问：为什么 BFPP 必须排在 BPP（BeanPostProcessor）前面？因为 BFPP 改的是**图纸**，BPP 加工的是**产品**。图纸没定稿就开工，后面全是返工——所以这个顺序不可动摇。也正因为所有扩展都发生在"图纸层"：`@PropertySource`、`@MapperScan`、Spring Boot 的自动配置，本质上都是在这一步往容器里多塞了几张图纸。

**第 6 步 `registerBeanPostProcessors()`**：把容器里所有 BPP 类型的 bean **提前实例化并登记**。注意只是注册，真正的拦截发生在后面每个 Bean 的创建过程中。管 `@Autowired` 的 `AutowiredAnnotationBeanPostProcessor`、管 `@Resource` 和 `@PostConstruct` 的 `CommonAnnotationBeanPostProcessor`，都在这一步就位。

### 第三段（7~12 步）：基础设施就位，然后开工

**第 7~8 步**：`initMessageSource()` 初始化国际化文案源，`initApplicationEventMulticaster()` 初始化事件广播器——没有广播器，事件机制无从谈起。

**第 9 步 `onRefresh()`**：子类钩子。**Spring Boot 的内嵌 Tomcat 就是在这一步起来的**，不是很多人以为的最后一步。

**第 10 步 `registerListeners()`**：把事件监听器登记给广播器——注意此时只登记 bean 名字，监听器对象还没实例化。

**第 11 步 `finishBeanFactoryInitialization()`**：**全篇第二个重点——所有非懒加载的单例 Bean，在这一步被真正创建。** 方法尾部两行是灵魂：

```java
// 冻结配置：图纸定稿，此后不允许再改 BeanDefinition
beanFactory.freezeConfiguration();
// 逐个 getBean，触发完整的 Bean 生命周期
beanFactory.preInstantiateSingletons();
```

实例化、属性填充、初始化、AOP 代理……一个 Bean 从图纸变成成品的完整工序（下一篇的主角）全部从这里触发。

**第 12 步 `finishRefresh()`**：初始化 `LifecycleProcessor`、启动实现了 `Lifecycle` 接口的 bean，最后 `publishEvent(new ContextRefreshedEvent(this))`——**收到这个事件，容器才算正式"可用"**，你才在 `main` 方法里拿到了那个 `ctx`。

### 失败兜底：启动失败时发生了什么

任何一步抛异常，都会走进 `catch`：先 `destroyBeans()` 把**已创建**的单例销毁干净（不会留半吊子容器），再 `cancelRefresh()` 复位状态，异常抛给调用者。所以 Spring 启动失败的异常栈，最顶上的 Spring 内部帧几乎都在 `refresh()` 里——这不是巧合，是设计。

## 加分点：BeanDefinition 和 BeanFactory 为什么必须分离

![BeanFactory层级结构](../images/src1-hierarchy.jpg)

背定义不如记两个比喻：

- **BeanDefinition = 对象说明书**：类名、scope、是否懒加载、依赖哪些对象、初始化方法叫什么……它只是一份数据；
- **BeanFactory = 按说明书生产产品的工厂**：而 `DefaultListableBeanFactory` 一个类就集齐了四张门面——`ConfigurableListableBeanFactory`、`BeanDefinitionRegistry`，加上继承链上的 Listable（可枚举）、Hierarchical（有父子）、AutowireCapable（可装配）。

为什么这个分离是 Spring 一切扩展性的根本？因为**"图纸"是数据，数据就可以被程序增删改**。Spring Boot 自动配置的全部魔法，就是第 5 步往容器里塞图纸；`@ConditionalOnMissingBean` 的"用户自定义优先"，本质也是图纸层面的判断。没有这层分离，注解都是空中楼阁。

面试时把这句话甩出去：**"Spring 的可扩展性，就是让扩展代码有机会在图纸定稿前参与画图。"**

## 十二步速查表

![启动时序概览](../images/src1-timeline.jpg)

| # | 方法 | 干什么 | 面试重要度 |
|---|---|---|---|
| 1 | prepareRefresh | 状态准备、早期事件暂存 | ⭐ |
| 2 | obtainFreshBeanFactory | 拿到 DefaultListableBeanFactory | ⭐⭐⭐ 注解模式工厂早已建好 |
| 3 | prepareBeanFactory | 装配 ClassLoader/SpEL/可解析依赖 | ⭐⭐⭐ @Autowired ApplicationContext 的来源 |
| 4 | postProcessBeanFactory | 子类钩子 | ⭐ |
| 5 | invokeBeanFactoryPostProcessors | **BD 注册：扫描/自动配置全在这** | ⭐⭐⭐⭐⭐ 最高频 |
| 6 | registerBeanPostProcessors | 注册 BPP | ⭐⭐⭐⭐ 处理器就位时机 |
| 7 | initMessageSource | 国际化 | ⭐ |
| 8 | initApplicationEventMulticaster | 事件广播器 | ⭐⭐ |
| 9 | onRefresh | 子类钩子 | ⭐⭐⭐⭐ Boot 在这起 Tomcat |
| 10 | registerListeners | 登记监听器 | ⭐⭐ 只登记不实例化 |
| 11 | finishBeanFactoryInitialization | **freeze + preInstantiateSingletons** | ⭐⭐⭐⭐⭐ 单例真正创建 |
| 12 | finishRefresh | Lifecycle + ContextRefreshedEvent | ⭐⭐⭐ 容器可用标志 |

## 动手验证（10 分钟，比背十遍都管用）

1. 在配置类构造器里打一行日志，再在某个 Bean 的 `@PostConstruct` 里打一行——跑起来你会看到：**配置类构造器先执行**，因为它自己也是一张"被提前加载的图纸"；
2. 断点打在第 5 步 `invokeBeanFactoryPostProcessors`，对比前后 `beanDefinitionMap.size()`——你会亲眼看到它从个位数暴涨到几百；
3. 把一个 Bean 的 `@Lazy` 去掉/加上，在第 11 步 `preInstantiateSingletons` 里找它，感受"懒加载到底懒在哪一步"。

## 下一篇预告

Bean 在第 11 步拿到"出生许可"之后，经历了什么？实例化、属性填充、初始化、AOP 代理——四步源码谁先谁后，扩展点插在哪？

下一篇：《Bean 生命周期：从 new 到可用，四步源码谁先谁后》。
