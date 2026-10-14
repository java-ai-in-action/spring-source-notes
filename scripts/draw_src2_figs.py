#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇2 信息图全套：封面 / 生命周期全景 / 实例化vs初始化 / 初始化四步 / AOP插入点"""
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

BG, CARD, CARD2, HL = '#0A1729', '#12263F', '#16304F', '#2B2A12'
BLUE, CYAN, GOLD, WHITE, GREY, GREEN = '#4A8DFF', '#22D3EE', '#F5C542', '#EAF2FF', '#93A9C7', '#7FE39A'
EDGE, EDGE_HL = '#1E3A5F', '#F5C542'


def new_fig(w, h):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), w, h, facecolor=BG))
    return fig, ax


def box(ax, x, y, w, h, fc=CARD, ec=EDGE, lw=1.2, r=10):
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
    # 右侧：四步流水线隐喻
    labels = ['①', '②', '③', '④']
    bx, by = 800, 200
    for i, lb in enumerate(labels):
        x = bx + (i % 2) * 170
        y = by + (i // 2) * 170
        c = GOLD if i in (2, 3) else BLUE
        box(ax, x, y, 140, 120, fc='#0E2444', ec=c, lw=2)
        ax.text(x + 70, y + 60, lb, ha='center', va='center', color=c, fontproperties=FB, fontsize=34)
        if i % 2 == 0 and i < 3:
            arrow(ax, x + 140, y + 60, x + 170, y + 60, color=CYAN, lw=2)
        if i == 1:
            arrow(ax, x + 70, y + 120, x + 70, y + 170, color=CYAN, lw=2)
    for px, py, s, c in [(320, 110, 10, CYAN), (1180, 120, 7, BLUE), (600, 648, 8, GOLD), (1080, 640, 9, CYAN)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 2 篇 ｜ Bean 生命周期', color=GOLD, fontproperties=FB, fontsize=27, va='center')
    ax.text(90, 466, '从 new 到可用：四步源码谁先谁后', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def quanjing(path):
    W, H = 1100, 1500
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 74, 'Bean 生命周期全景：四步 + 扩展点', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=28)
    ax.text(W / 2, 118, 'doCreateBean()  ·  AbstractAutowireCapableBeanFactory  ·  Spring 6.2.x',
            ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    stages = [
        ('① 实例化', 'createBeanInstance', '反射造出对象，依赖字段全是 null',
         ['InstantiationAwareBeanPostProcessor', 'determineCandidateConstructors（@Autowired 构造器）'], False),
        ('② 属性填充', 'populateBean', '把依赖注入进去（此后再无 null 依赖）',
         ['postProcessAfterInstantiation', 'postProcessProperties  ← @Autowired / @Resource'], True),
        ('③ 初始化', 'initializeBean', 'Aware → @PostConstruct → afterPropertiesSet → init-method',
         ['invokeAwareMethods（仅 3 个 Aware）', 'BPP Before（@PostConstruct）'], True),
        ('④ AOP 增强', 'postProcessAfterInitialization', '生成代理对象（需要切面才会生成）',
         ['AbstractAutoProxyCreator', 'wrapIfNecessary → createProxy'], True),
    ]
    y = 168
    for name, method, desc, exts, hl in stages:
        box(ax, 55, y, 990, 260, fc=HL if hl else CARD, ec=EDGE_HL if hl else EDGE, lw=1.7 if hl else 1.1)
        ax.text(85, y + 44, name, ha='left', va='center', color=GOLD if hl else BLUE,
                fontproperties=FB, fontsize=22)
        ax.text(85, y + 88, method, ha='left', va='center', color=CYAN, fontproperties=FM, fontsize=16)
        ax.text(85, y + 128, desc, ha='left', va='center', color=WHITE, fontproperties=F, fontsize=15)
        ax.plot([85, 1015], [y + 158, y + 158], color='#24456E', lw=1)
        ax.text(85, y + 186, '扩展点：', ha='left', va='center', color=GREY, fontproperties=F, fontsize=14)
        for i, e in enumerate(exts):
            fp = FM if e.isascii() else F
            ax.text(105, y + 216 + i * 28, '· ' + e, ha='left', va='center',
                    color='#9FD8E8' if hl else GREY, fontproperties=fp, fontsize=13)
        if y < 1100:
            arrow(ax, 550, y + 260, 550, y + 300, color=GOLD if hl else CYAN)
        y += 300
    box(ax, 300, 1385 - 45, 500, 70, fc='#1B2C18', ec='#4CC46A', lw=1.6)
    ax.text(550, 1375, '★ 容器暴露的是「代理对象」，不是原始对象', ha='center', va='center',
            color=GREEN, fontproperties=FB, fontsize=18)
    save(fig, path)


def shilihua(path):
    W, H = 1100, 980
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '实例化 ≠ 初始化', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=30)
    ax.text(W / 2, 116, '很多人栽在这一步：以为"造出来"就等于"能用了"', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=15)
    left = [
        ('实例化', 'createBeanInstance', BLUE, ['反射 new 出一个对象', '依赖字段全是 null',
         '只负责"挑构造器 + 造壳"', '产物：一个「空壳」对象']),
    ]
    box(ax, 60, 180, 460, 560, ec=BLUE, lw=1.8)
    ax.text(290, 232, '① 实例化', ha='center', va='center', color=BLUE, fontproperties=FB, fontsize=24)
    ax.text(290, 276, 'createBeanInstance', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=14)
    for i, ln in enumerate(['反射 new 出一个对象', '依赖字段全是 null', '只负责挑构造器 + 造壳']):
        ax.text(100, 340 + i * 46, '· ' + ln, ha='left', va='center', color=WHITE, fontproperties=F, fontsize=16)
    ax.text(290, 500, '产物', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(290, 546, '一个「空壳」对象', ha='center', va='center', color=GREY, fontproperties=FB, fontsize=19)
    ax.text(290, 660, '（还不能用）', ha='center', va='center', color='#C46A6A', fontproperties=F, fontsize=15)

    box(ax, 580, 180, 460, 560, ec=GOLD, lw=1.8, fc=HL)
    ax.text(810, 232, '②③④ 属性填充 + 初始化', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=20)
    ax.text(810, 276, 'populateBean + initializeBean', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    for i, ln in enumerate(['@Autowired 注入依赖', 'Aware → @PostConstruct → init-method', 'AOP 代理最后套上']):
        ax.text(620, 340 + i * 46, '· ' + ln, ha='left', va='center', color='#EFE0A8', fontproperties=F, fontsize=15)
    ax.text(810, 500, '产物', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(810, 546, '可用的 Bean', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=19)
    ax.text(810, 660, '（可能是代理对象）', ha='center', va='center', color=GREEN, fontproperties=F, fontsize=15)

    ax.text(W / 2, 800, '实例化 = 造空壳；初始化 = 注入依赖 + 织入增强', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=19)
    ax.text(W / 2, 870, '顺序不可逆：先有对象，才有得注入、才谈得上初始化', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=15)
    save(fig, path)


def chushi(path):
    W, H = 1100, 1180
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, 'initializeBean() 内部：四步顺序', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=28)
    steps = [
        ('1', 'invokeAwareMethods', 'Aware 回调：只有 3 个！',
         'BeanNameAware / BeanClassLoaderAware / BeanFactoryAware', False),
        ('2', 'applyBeanPostProcessorsBeforeInitialization', '初始化前：@PostConstruct 在这里',
         '由 CommonAnnotationBeanPostProcessor 调用', False),
        ('3', 'invokeInitMethods', '自定义初始化',
         'InitializingBean.afterPropertiesSet()  +  init-method', False),
        ('4', 'applyBeanPostProcessorsAfterInitialization', '初始化后：AOP 代理诞生',
         'AbstractAutoProxyCreator.postProcessAfterInitialization', True),
    ]
    y = 140
    for num, name, note, sub, hl in steps:
        box(ax, 70, y, 960, 150, fc=HL if hl else CARD, ec=EDGE_HL if hl else EDGE, lw=1.8 if hl else 1.1)
        ax.add_patch(Circle((122, y + 75), 25, facecolor=GOLD if hl else '#1E4C8A', edgecolor='none'))
        ax.text(122, y + 75, num, ha='center', va='center', color='#0A1729' if hl else WHITE,
                fontproperties=FB, fontsize=17)
        fp = FM if name.isascii() else F
        ax.text(168, y + 48, name, ha='left', va='center', color=GOLD if hl else CYAN,
                fontproperties=fp, fontsize=14)
        ax.text(168, y + 88, note, ha='left', va='center', color=WHITE if not hl else '#EFE0A8',
                fontproperties=F, fontsize=16)
        ax.text(168, y + 120, sub, ha='left', va='center', color=GREY, fontproperties=F, fontsize=12.5)
        if y < 700:
            arrow(ax, 550, y + 150, 550, y + 184, color=GOLD if hl else CYAN)
        y += 184
    box(ax, 70, 905, 960, 96, fc=CARD2, ec=BLUE, lw=1.4)
    ax.text(550, 934, '记忆链（面试直接背这条）', ha='center', va='center', color=BLUE,
            fontproperties=FB, fontsize=17)
    ax.text(550, 972, '构造方法 → @Autowired → Aware → @PostConstruct → afterPropertiesSet → init-method → AOP 代理',
            ha='center', va='center', color=WHITE, fontproperties=F, fontsize=14.5)
    ax.text(550, 1060, '★ 高频追问：ApplicationContextAware 不在这 3 个里，它由 ApplicationContextAwareProcessor（一个 BPP）在第 2 步处理',
            ha='center', va='center', color=GOLD, fontproperties=F, fontsize=13)
    save(fig, path)


def aop(path):
    W, H = 1100, 820
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 66, 'AOP 代理在哪一刻套上？', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    y0 = 400
    ax.plot([90, 1010], [y0, y0], color='#2A4E7A', lw=5, solid_capstyle='round')
    nodes = [
        (160, '实例化'), (335, '属性填充'), (510, '初始化'), (685, '初始化后'), (900, '暴露')
    ]
    for i, (x, name) in enumerate(nodes):
        hl = (name == '初始化后')
        c = GOLD if hl else CYAN
        ax.add_patch(Circle((x, y0), 20 if hl else 14, facecolor=GOLD if hl else '#1E4C8A',
                            edgecolor=c, lw=2))
        if hl:
            ax.text(x, y0, '★', ha='center', va='center', color='#0A1729', fontsize=13)
        ax.text(x, y0 - 52, name, ha='center', va='center', color=c, fontproperties=FB, fontsize=16)
        ms = ['createBeanInstance', 'populateBean', 'initializeBean', 'BPP After', ''][i]
        if ms:
            fp = FM if ms.isascii() else F
            ax.text(x, y0 - 24, ms, ha='center', va='center', color=GREY, fontproperties=fp, fontsize=11.5)
    ax.text(685, y0 + 60, '代理在这里生成', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=17)
    ax.text(685, y0 + 96, 'AbstractAutoProxyCreator', ha='center', va='center', color=GOLD,
            fontproperties=FM, fontsize=12.5)
    ax.text(685, y0 + 126, '→ wrapIfNecessary → createProxy', ha='center', va='center', color=GOLD,
            fontproperties=FM, fontsize=12.5)
    ax.text(900, y0 - 52, '暴露', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=16)
    ax.text(900, y0 + 60, '容器拿到的是', ha='center', va='center', color=GREEN, fontproperties=F, fontsize=15)
    ax.text(900, y0 + 92, '代理对象', ha='center', va='center', color=GREEN, fontproperties=FB, fontsize=18)
    box(ax, 90, 610, 920, 100, fc=HL, ec=GOLD, lw=1.5)
    ax.text(550, 642, '★ 代理"最晚生成" → 循环依赖时，B 注入的 A 可能是「早期代理」', ha='center',
            va='center', color=GOLD, fontproperties=FB, fontsize=17)
    ax.text(550, 682, '这是下一篇《三级缓存与循环依赖》的伏笔', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=15)
    save(fig, path)


if __name__ == '__main__':
    out = '/sandbox/workspace/output/'
    cover(out + 'src2-fengmian.png')
    quanjing(out + 'src2-quanjing.png')
    shilihua(out + 'src2-shilihua.png')
    chushi(out + 'src2-chushi.png')
    aop(out + 'src2-aop.png')
