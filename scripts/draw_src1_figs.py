#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇1 信息图全套：封面 / 十二步流程 / BD注册链路 / BeanFactory层级 / 启动时间线
   matplotlib 精确绘制，文字 100% 可控；坐标系一律用像素，y 轴向下。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.font_manager import FontProperties

CJK_R = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CJK_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
MONO_B = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = FontProperties(fname=CJK_R)
FB = FontProperties(fname=CJK_B)
FM = FontProperties(fname=MONO)
FMB = FontProperties(fname=MONO_B)

BG, CARD, CARD2, HLCARD = '#0A1729', '#12263F', '#16304F', '#2B2A12'
BLUE, CYAN, GOLD, WHITE, GREY = '#4A8DFF', '#22D3EE', '#F5C542', '#EAF2FF', '#93A9C7'
EDGE, EDGE_HL = '#1E3A5F', '#F5C542'


def new_fig(w, h):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), w, h, facecolor=BG))
    return fig, ax


def box(ax, x, y, w, h, fc=CARD, ec=EDGE, lw=1.2, r=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f'round,pad=0,rounding_size={r}',
                 facecolor=fc, edgecolor=ec, linewidth=lw))


def arrow(ax, x1, y1, x2, y2, color=CYAN, lw=2.2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                 mutation_scale=18, color=color, lw=lw,
                 shrinkA=0, shrinkB=0))


def save(fig, path):
    fig.savefig(path, facecolor=BG)
    plt.close(fig)
    print('saved:', path)


# ---------- 1) 封面 ----------
def draw_cover(path):
    W, H = 1280, 720
    fig, ax = new_fig(W, H)
    for gx in range(0, W, 80):
        ax.plot([gx, gx], [0, H], color='#123055', lw=0.6, alpha=0.5)
    for gy in range(0, H, 80):
        ax.plot([0, W], [gy, gy], color='#123055', lw=0.6, alpha=0.5)
    cx, cy, r = 930, 330, 195
    ax.add_patch(Circle((cx, cy), r + 16, facecolor='#0E2444', edgecolor='none', alpha=0.7))
    ax.add_patch(Circle((cx, cy), r, facecolor='none', edgecolor=BLUE, lw=7))
    ax.add_patch(Circle((cx, cy), r - 14, facecolor='none', edgecolor=CYAN, lw=1.5, alpha=0.8))
    for i, (bw, by, c) in enumerate([(150, cy - 90, CYAN), (170, cy - 10, BLUE), (130, cy + 66, GOLD)]):
        box(ax, cx - bw / 2, by, bw, 46, fc='#0E2444', ec=c, lw=1.8, r=6)
        ax.plot([cx - bw / 2 + 14, cx + bw / 2 - 14], [by + 23, by + 23], color=c, lw=2, alpha=0.55)
    ax.plot([cx + 138, cx + 210], [cy + 138, cy + 210], color=BLUE, lw=12, solid_capstyle='round')
    for px, py, s, c in [(300, 120, 10, CYAN), (1120, 150, 7, BLUE), (200, 600, 8, GOLD),
                         (1050, 610, 9, CYAN), (620, 90, 6, BLUE), (740, 640, 7, CYAN)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 320, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=45, va='center')
    ax.text(90, 405, '第 1 篇 ｜ IoC 容器 refresh() 全流程', color=GOLD, fontproperties=FB, fontsize=25, va='center')
    ax.text(90, 470, '面试官追着你问的那 10 个类', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [540, 540], color='#24456E', lw=1.2)
    ax.text(90, 585, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 625, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


# ---------- 2) refresh 十二步 ----------
STEPS = [
    ('① 搭台子 · 容器准备', [
        ('1', 'prepareRefresh', '状态准备：时间戳 / active 标志 / 属性校验', False),
        ('2', 'obtainFreshBeanFactory', '拿到 DefaultListableBeanFactory', False),
        ('3', 'prepareBeanFactory', '装配 ClassLoader / SpEL / 可解析依赖', False),
    ]),
    ('② 注册图纸 · BeanDefinition', [
        ('4', 'postProcessBeanFactory', '子类钩子（Web 场景扩展点）', False),
        ('5', 'invokeBeanFactoryPostProcessors', '扫描 @ComponentScan、自动配置注册 BD', True),
        ('6', 'registerBeanPostProcessors', 'BPP 就位（@Autowired 处理器等）', False),
    ]),
    ('③ 开工 · 实例化与收尾', [
        ('7', 'initMessageSource', '初始化国际化文案源', False),
        ('8', 'initApplicationEventMulticaster', '初始化事件广播器', False),
        ('9', 'onRefresh', '子类钩子（Boot 在此启动 Tomcat）', False),
        ('10', 'registerListeners', '登记事件监听器（不实例化）', False),
        ('11', 'finishBeanFactoryInitialization', 'freeze + 单例真正创建', True),
        ('12', 'finishRefresh', '发布 ContextRefreshedEvent，就绪', False),
    ]),
]


def draw_flow(path):
    W, H = 1100, 1520
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 78, 'Spring 启动：refresh() 十二步', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=30)
    ax.text(W / 2, 125, 'AbstractApplicationContext.refresh()   ·   Spring Framework 6.2.x',
            ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=14)
    y = 185
    for title, rows in STEPS:
        box(ax, 60, y, 980, 52, fc=CARD2, ec=BLUE, lw=1.4, r=8)
        ax.text(85, y + 26, title, ha='left', va='center', color=BLUE, fontproperties=FB, fontsize=17)
        y += 72
        for num, name, desc, hl in rows:
            box(ax, 60, y, 980, 62, fc=HLCARD if hl else CARD,
                ec=EDGE_HL if hl else EDGE, lw=1.6 if hl else 1.0)
            ax.add_patch(Circle((108, y + 31), 20, facecolor=GOLD if hl else '#1E4C8A', edgecolor='none'))
            ax.text(108, y + 31, num, ha='center', va='center', color='#0A1729' if hl else WHITE,
                    fontproperties=FB, fontsize=14)
            ax.text(148, y + 31, name, ha='left', va='center',
                    color=GOLD if hl else CYAN, fontproperties=FMB if hl else FM, fontsize=15)
            ax.text(1024, y + 31, desc, ha='right', va='center',
                    color='#EFE0A8' if hl else GREY, fontproperties=F, fontsize=14)
            y += 80
    ax.text(W / 2, H - 60, '★ 面试最高频的两步：图纸注册（第 5 步）与单例创建（第 11 步）',
            ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    save(fig, path)


# ---------- 3) BeanDefinition 注册链路 ----------
def draw_bd(path):
    W, H = 1100, 1150
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, 'BeanDefinition 是怎么注册进容器的？', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=28)
    box(ax, 350, 120, 400, 62, ec=BLUE, lw=1.8)
    ax.text(550, 151, '配置类 AppConfig', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=19)
    arrow(ax, 550, 182, 550, 218)
    box(ax, 200, 218, 700, 62, fc=CARD2, ec=CYAN, lw=1.6)
    ax.text(550, 249, 'ConfigurationClassPostProcessor（一个 BFPP）解析', ha='center', va='center',
            color=CYAN, fontproperties=F, fontsize=17)
    arrow(ax, 550, 280, 340, 320)
    arrow(ax, 550, 280, 760, 320)
    box(ax, 110, 320, 460, 74)
    ax.text(340, 345, '@ComponentScan', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=15)
    ax.text(340, 372, '扫描出所有 @Component 类', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    box(ax, 530, 320, 460, 74)
    ax.text(710, 345, '@Bean', ha='left', va='center', color=CYAN, fontproperties=FM, fontsize=15)
    ax.text(775, 345, '方法', ha='left', va='center', color=CYAN, fontproperties=F, fontsize=15)
    ax.text(760, 372, '每个方法 → 一个 Bean 定义', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    arrow(ax, 340, 394, 470, 442)
    arrow(ax, 760, 394, 630, 442)
    box(ax, 180, 442, 740, 132, ec=GOLD, lw=1.9, fc=HLCARD)
    ax.text(550, 478, 'BeanDefinition（对象说明书）', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=20)
    ax.text(550, 522, '类名  ·  scope  ·  是否懒加载  ·  依赖哪些 Bean  ·  init / destroy 方法',
            ha='center', va='center', color='#EFE0A8', fontproperties=F, fontsize=15)
    ax.text(550, 552, '—— 到这里它只是一份「数据」，还没有任何对象被 new 出来',
            ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    arrow(ax, 550, 574, 550, 616, color=GOLD)
    box(ax, 180, 616, 740, 120, ec=BLUE, lw=1.9)
    ax.text(550, 652, 'DefaultListableBeanFactory.beanDefinitionMap', ha='center', va='center',
            color=WHITE, fontproperties=FM, fontsize=17)
    ax.text(550, 690, 'Map<String, BeanDefinition>   =   ConcurrentHashMap(256)', ha='center', va='center',
            color=CYAN, fontproperties=FM, fontsize=14)
    ax.text(550, 718, '图纸柜：容器里所有 Bean 的「档案」都躺在这张 Map 里', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=14)
    box(ax, 120, 790, 860, 74, fc='#1B2C18', ec='#4CC46A', lw=1.6)
    ax.text(550, 827, '★ 此刻容器里只有「图纸」，没有任何 Bean 实例', ha='center', va='center',
            color='#7FE39A', fontproperties=FB, fontsize=19)
    ax.text(550, 920, 'Bean 要到第 11 步 finishBeanFactoryInitialization 才被真正创建（见篇 2）',
            ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(550, 1080, '源码依据：Spring Framework 6.2.x', ha='center', va='center',
            color='#5C7FA8', fontproperties=F, fontsize=13)
    save(fig, path)


# ---------- 4) BeanFactory 层级 ----------
def draw_hierarchy(path):
    W, H = 1100, 1250
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, 'BeanFactory 家族：一个类集齐四张门面', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=27)
    box(ax, 370, 120, 360, 66, ec=BLUE, lw=1.9)
    ax.text(550, 153, 'BeanFactory', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=19)
    for tx in (240, 550, 860):
        arrow(ax, 550, 186, tx, 232)
    layer2 = [
        (90, 'ListableBeanFactory', '可枚举：拿一批 Bean'),
        (400, 'HierarchicalBeanFactory', '有父子：可设父容器'),
        (710, 'AutowireCapableBeanFactory', '可装配：外部手动注入'),
    ]
    for x, name, note in layer2:
        box(ax, x, 232, 300, 96, ec=EDGE, lw=1.4)
        ax.text(x + 150, 262, name, ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
        ax.text(x + 150, 300, note, ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(550, 366, '三者都 extends BeanFactory', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=13)
    arrow(ax, 240, 396, 470, 440)
    arrow(ax, 860, 396, 630, 440)
    arrow(ax, 550, 396, 550, 440)
    box(ax, 150, 440, 800, 86, fc=CARD2, ec=GOLD, lw=1.7)
    ax.text(550, 472, 'ConfigurableListableBeanFactory（汇聚层）', ha='center', va='center',
            color=GOLD, fontproperties=F, fontsize=19)
    ax.text(550, 502, 'extends  ListableBeanFactory + AutowireCapableBeanFactory + ConfigurableBeanFactory',
            ha='center', va='center', color='#EFE0A8', fontproperties=FM, fontsize=11.5)
    arrow(ax, 550, 526, 550, 620, color=GOLD, lw=2.6)
    ax.text(600, 575, 'implements', ha='left', va='center', color=GREY, fontproperties=FM, fontsize=13)
    box(ax, 130, 620, 840, 128, ec=BLUE, lw=2.0)
    ax.text(550, 660, 'DefaultListableBeanFactory', ha='center', va='center', color=WHITE,
            fontproperties=FMB, fontsize=21)
    ax.text(550, 696, 'extends AbstractAutowireCapableBeanFactory', ha='center', va='center',
            color=CYAN, fontproperties=FM, fontsize=13)
    ax.text(550, 724, 'implements ConfigurableListableBeanFactory, BeanDefinitionRegistry',
            ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=12)
    box(ax, 120, 806, 860, 80, fc=HLCARD, ec=GOLD, lw=1.6)
    ax.text(550, 846, '★ 注解时代的容器，真正干活的实现类就是它', ha='center', va='center',
            color=GOLD, fontproperties=FB, fontsize=19)
    ax.text(550, 940, 'BeanDefinitionRegistry 这个身份是它能「登记图纸」的关键', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=15)
    ax.text(550, 1180, '源码依据：Spring Framework 6.2.x', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=13)
    save(fig, path)


# ---------- 5) 启动时间线 ----------
def draw_timeline(path):
    W, H = 1320, 800
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 66, '启动时间线：容器里什么时候有「图纸」，什么时候有「Bean」',
            ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=24)
    y0 = 430
    ax.plot([110, 1210], [y0, y0], color='#2A4E7A', lw=5, solid_capstyle='round')
    nodes = [
        (180, 't0', '构造器', '工厂已建好\nDefaultListableBeanFactory', False),
        (400, 't1', 'register()', '配置类登记为图纸\nBD = 1', False),
        (640, 't2', '第 5 步\ninvokeBFPP', '图纸齐了（数百条 BD）\nBean 仍为 0', True),
        (880, 't3', '第 11 步\nfinishBeanFactoryInit', '单例批量创建\nBean 全部就位', True),
        (1110, 't4', '第 12 步\nfinishRefresh', '发布 ContextRefreshedEvent\nctx 可用', False),
    ]
    for x, t, method, note, hl in nodes:
        c = GOLD if hl else CYAN
        ax.add_patch(Circle((x, y0), 17, facecolor=c if hl else '#1E4C8A', edgecolor=c, lw=2))
        ax.text(x, y0 - 62, t, ha='center', va='center', color=c, fontproperties=FMB, fontsize=13)
        for i, ln in enumerate(method.split('\n')):
            fp = FM if ln.isascii() else F
            ax.text(x, y0 - 34 + i * 20, ln, ha='center', va='center', color=WHITE,
                    fontproperties=fp, fontsize=11.5)
        for i, ln in enumerate(note.split('\n')):
            ax.text(x, y0 + 52 + i * 27, ln, ha='center', va='center',
                    color='#EFE0A8' if hl else GREY, fontproperties=F, fontsize=14)
    ax.plot([110, 1210], [690, 690], color='#24456E', lw=1)
    ax.text(W / 2, 740, '★ 第 5 步之前：只有图纸；第 11 步之后：才有真正的 Bean',
            ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=17)
    save(fig, path)


if __name__ == '__main__':
    out = '/sandbox/workspace/output/'
    draw_cover(out + 'src1-cover-v2.png')
    draw_flow(out + 'src1-flow-v2.png')
    draw_bd(out + 'src1-bd-v2.png')
    draw_hierarchy(out + 'src1-hierarchy-v2.png')
    draw_timeline(out + 'src1-timeline-v2.png')
