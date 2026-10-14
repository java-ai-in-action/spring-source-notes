#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇10 信息图：封面 / BeanFactory vs FactoryBean / ApplicationContext 体系 / 设计模式全景 / 系列回顾"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.font_manager import FontProperties

CJK_R = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CJK_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
MONO_B = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F, FB = FontProperties(fname=CJK_R), FontProperties(fname=CJK_B)
FM, FMB = FontProperties(fname=MONO), FontProperties(fname=MONO_B)

BG, CARD, CARD2 = '#0A1729', '#12263F', '#16304F'
BLUE, CYAN, GOLD, WHITE, GREY, GREEN, RED = '#4A8DFF', '#22D3EE', '#F5C542', '#EAF2FF', '#93A9C7', '#7FE39A', '#FF7B7B'
EDGE = '#1E3A5F'


def new_fig(w, h):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), w, h, facecolor=BG))
    return fig, ax


def box(ax, x, y, w, h, fc=CARD, ec=EDGE, lw=1.2, r=9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                 facecolor=fc, edgecolor=ec, linewidth=lw))


def arrow(ax, x1, y1, x2, y2, color=CYAN, lw=2.2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=18,
                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def save(fig, path):
    fig.savefig(path, facecolor=BG); plt.close(fig); print('saved:', path)


def cover(path):
    W, H = 1280, 720
    fig, ax = new_fig(W, H)
    for gx in range(0, W, 80):
        ax.plot([gx, gx], [0, H], color='#123055', lw=0.6, alpha=0.5)
    for gy in range(0, H, 80):
        ax.plot([0, W], [gy, gy], color='#123055', lw=0.6, alpha=0.5)
    box(ax, 830, 150, 380, 120, fc='#0E2444', ec=BLUE, lw=1.8)
    ax.text(1020, 185, 'BeanFactory', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=16)
    ax.text(1020, 225, '容器：管理所有 Bean', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    box(ax, 830, 300, 380, 120, fc='#0E2444', ec=GOLD, lw=1.8)
    ax.text(1020, 335, 'FactoryBean', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=16)
    ax.text(1020, 375, '一种 Bean：生产别的对象', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    box(ax, 830, 450, 380, 120, fc='#0E2444', ec=GREEN, lw=1.8)
    ax.text(1020, 485, 'ApplicationContext', ha='center', va='center', color=GREEN, fontproperties=FM, fontsize=14)
    ax.text(1020, 525, '门面：基础 + 事件 + 资源', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(1020, 620, '长得像的类，差在解决什么问题', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    for px, py, s, c in [(640, 120, 10, CYAN), (700, 648, 8, GOLD), (640, 452, 9, BLUE)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 10 篇（终篇）｜ 设计模式', color=GOLD, fontproperties=FB, fontsize=24, va='center')
    ax.text(90, 466, '那些"长得像"的类，差在哪', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def factorybean(path):
    W, H = 1100, 780
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, 'BeanFactory vs FactoryBean', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 102, '一个管所有 Bean，一个自己就是 Bean', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    # 左
    box(ax, 80, 150, 460, 150, fc='#0E2443', ec=BLUE, lw=1.8)
    ax.text(310, 190, 'BeanFactory', ha='center', va='center', color=BLUE, fontproperties=FM, fontsize=18)
    ax.text(310, 232, '容器本身', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=16)
    ax.text(310, 268, 'getBean() 是它给外界的能力', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    # 右
    box(ax, 560, 150, 460, 150, fc='#2B2A12', ec=GOLD, lw=1.8)
    ax.text(790, 190, 'FactoryBean', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=18)
    ax.text(790, 232, '一种特殊的 Bean', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=16)
    ax.text(790, 268, '住在容器里，生产别的对象', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    # 关键点
    box(ax, 130, 350, 840, 240, fc='#0B1C33', ec=CYAN, lw=1.4)
    ax.text(550, 388, '当 xxx 是一个 FactoryBean 时：', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    ax.text(180, 445, 'getBean("xxx")', ha='left', va='center', color=GREEN, fontproperties=FM, fontsize=16)
    ax.text(500, 445, '->  getObject() 的产物', ha='left', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(180, 505, 'getBean("&xxx")', ha='left', va='center', color=GOLD, fontproperties=FM, fontsize=16)
    ax.text(500, 505, '->  FactoryBean 工厂本身', ha='left', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(550, 560, 'FACTORY_BEAN_PREFIX = "&"', ha='center', va='center', color=GREY, fontproperties=FM, fontsize=12)
    ax.text(W / 2, 650, '典型：SqlSessionFactoryBean / ProxyFactoryBean', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=14)
    save(fig, path)


def context(path):
    W, H = 1100, 900
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, 'ApplicationContext 的继承体系', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=26)
    ax.text(W / 2, 102, '不是"对立"，而是继承 + 组合（门面模式）', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 350, 400, 400, 100, fc='#2B2A12', ec=GOLD, lw=2.0)
    ax.text(550, 450, 'ApplicationContext', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=18)
    caps = [
        ('ListableBeanFactory', 'Bean 工厂', BLUE, 90, 180),
        ('HierarchicalBeanFactory', '父子容器', BLUE, 700, 180),
        ('MessageSource', '国际化', CYAN, 90, 420),
        ('ResourcePatternResolver', '资源加载', CYAN, 700, 420),
        ('ApplicationEventPublisher', '事件发布', GREEN, 90, 660),
        ('EnvironmentCapable', '环境配置', GREEN, 700, 660),
    ]
    for name, desc, c, x, y in caps:
        box(ax, x, y, 310, 100, fc=CARD2, ec=c, lw=1.5)
        ax.text(x + 155, y + 36, name, ha='center', va='center', color=c, fontproperties=FM, fontsize=12)
        ax.text(x + 155, y + 70, desc, ha='center', va='center', color=WHITE, fontproperties=F, fontsize=14)
        tx = x + 155
        if tx < 550:
            arrow(ax, x + 310, y + 50, 350, 450, color=c, lw=1.4)
        else:
            arrow(ax, x, y + 50, 750, 450, color=c, lw=1.4)
    ax.text(W / 2, 800, '用 ApplicationContext = 一次拿到 Bean 工厂 + 事件 + 资源 + 国际化', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def mosi(path):
    W, H = 1100, 1000
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, 'Spring 里的设计模式全景', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 100, '不背名词，记它"解决了什么问题"', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    rows = [
        ('工厂模式', 'BeanFactory / FactoryBean', BLUE),
        ('单例模式', '三级缓存（篇3）', BLUE),
        ('代理模式', 'JDK / CGLIB（篇5）', GOLD),
        ('模板方法', 'refresh / doCreateBean / JdbcTemplate', GOLD),
        ('观察者模式', 'ApplicationEvent / Listener', GREEN),
        ('适配器模式', 'HandlerAdapter（篇7）', GREEN),
        ('策略模式', 'AopProxy / Resource', CYAN),
        ('责任链模式', '拦截器链 proceed（篇5）', CYAN),
        ('装饰器模式', 'BeanWrapper / BeanPostProcessor', BLUE),
        ('门面模式', 'ApplicationContext / JdbcTemplate', GOLD),
    ]
    y = 140
    for name, impl, c in rows:
        box(ax, 100, y, 900, 74, fc=CARD, ec=c, lw=1.4)
        ax.text(140, y + 37, name, ha='left', va='center', color=c, fontproperties=FB, fontsize=16)
        ax.text(400, y + 37, impl, ha='left', va='center', color=WHITE, fontproperties=F if not impl.isascii() else FM, fontsize=13)
        y += 84
    save(fig, path)


def huigu(path):
    W, H = 1100, 1160
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 58, '《Spring 源码现形记》10 篇回顾', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=26)
    ax.text(W / 2, 98, '一条从"容器启动"到"设计哲学"的完整链路', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    rows = [
        ('1', 'IoC refresh()', '定义了容器启动的全部顺序', BLUE),
        ('2', 'Bean 生命周期', '从 new 到可用的四步', BLUE),
        ('3', '三级缓存', '循环依赖为什么能解', CYAN),
        ('4', '@Autowired 注入', '字段怎么被反射 set 进去', CYAN),
        ('5', 'AOP 代理', 'JDK 还是 CGLIB，看一个 if', GOLD),
        ('6', '@Transactional 失效', '本质是代理失效', GOLD),
        ('7', 'MVC doDispatch', '一个请求，七步走完', GREEN),
        ('8', 'Boot 自动配置', '用户永远优先', GREEN),
        ('9', '扩展点全景', 'BFP 改图纸，BP 改成品', GOLD),
        ('10', '设计模式', '长得像的类，差在解决什么问题', CYAN),
    ]
    y = 132
    for num, title, desc, c in rows:
        box(ax, 90, y, 920, 90, fc=CARD, ec=c, lw=1.4)
        ax.add_patch(Circle((145, y + 45), 26, facecolor='#0E2444', edgecolor=c, lw=1.5))
        ax.text(145, y + 45, num, ha='center', va='center', color=c, fontproperties=FMB, fontsize=17)
        ax.text(200, y + 32, title, ha='left', va='center', color=WHITE, fontproperties=FB, fontsize=16)
        ax.text(200, y + 64, desc, ha='left', va='center', color=GREY, fontproperties=F, fontsize=12.5)
        y += 100
    save(fig, path)


if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    cover('output/src10-fengmian.png')
    factorybean('output/src10-factorybean.png')
    context('output/src10-context.png')
    mosi('output/src10-mosi.png')
    huigu('output/src10-huigu.png')
