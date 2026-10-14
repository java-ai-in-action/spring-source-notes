#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇4 信息图：封面 / 处理流程 / field.set特写 / 两条注入路径 / 歧义裁决五步"""
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
BLUE, CYAN, GOLD, WHITE, GREY, GREEN, RED = '#4A8DFF', '#22D3EE', '#F5C542', '#EAF2FF', '#93A9C7', '#7FE39A', '#FF7B7B'
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
    # 右侧：字段 + 注入箭头
    box(ax, 830, 190, 300, 130, fc='#0E2444', ec=BLUE, lw=2)
    ax.text(980, 236, 'Bean', ha='center', va='center', color=WHITE, fontproperties=FMB, fontsize=22)
    box(ax, 880, 262, 200, 40, fc='#0E2444', ec=CYAN, lw=1.5, r=6)
    ax.text(980, 282, 'field', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=16)
    ax.add_patch(Circle((1100, 420), 46, facecolor='#0E2444', edgecolor=GOLD, lw=2))
    ax.text(1100, 420, 'obj', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=15)
    arrow(ax, 1082, 388, 1006, 308, color=GOLD, lw=2.6)
    ax.text(880, 470, 'field.set(bean, value)', ha='center', va='center', color=GOLD,
            fontproperties=FM, fontsize=15)
    for px, py, s, c in [(300, 120, 10, CYAN), (1180, 600, 8, GOLD), (620, 650, 7, BLUE), (200, 600, 9, CYAN)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 4 篇 ｜ @Autowired 注入源码', color=GOLD, fontproperties=FB, fontsize=25, va='center')
    ax.text(90, 466, '字段怎么被反射 set 进去的', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def liucheng(path):
    W, H = 1100, 1180
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 72, '@Autowired 的处理流程', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    ax.text(W / 2, 116, 'AutowiredAnnotationBeanPostProcessor（一个 InstantiationAwareBeanPostProcessor）',
            ha='center', va='center', color=CYAN, fontproperties=F, fontsize=13)
    steps = [
        ('入口 1', 'postProcessMergedBeanDefinition', '收集注入元数据（doCreateBean 第②步）', BLUE, False),
        ('→', 'findInjectionMetadata', '扫描字段/方法 → InjectionMetadata + 缓存', CYAN, False),
        ('入口 2', 'postProcessProperties', '属性填充阶段（populateBean）取元数据', BLUE, True),
        ('→', 'metadata.inject', '遍历每个注入点，逐个执行', CYAN, False),
        ('执行', 'element.inject', '字段 → field.set；方法 → method.invoke', GOLD, True),
    ]
    y = 168
    for tag, name, note, c, hl in steps:
        box(ax, 70, y, 960, 150, fc=HL if hl else CARD, ec=EDGE_HL if hl else EDGE, lw=1.8 if hl else 1.1)
        ax.text(110, y + 46, tag, ha='left', va='center', color=c, fontproperties=FB, fontsize=15)
        ax.text(110, y + 88, name, ha='left', va='center', color=GOLD if hl else CYAN,
                fontproperties=FM, fontsize=15)
        ax.text(110, y + 122, note, ha='left', va='center', color=WHITE if not hl else '#EFE0A8',
                fontproperties=F, fontsize=14.5)
        if y < 850:
            arrow(ax, 550, y + 150, 550, y + 184, color='#24456E', lw=1.8)
        y += 184
    box(ax, 70, 1085, 960, 62, fc=CARD2, ec=BLUE, lw=1.4)
    ax.text(550, 1116, '★ 分工：元数据「提前收集 + 缓存」，注入「在属性填充阶段执行」',
            ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=15)
    save(fig, path)


def fanshe(path):
    W, H = 1100, 1000
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, 'field.set()：字段注入的真身', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    ax.text(W / 2, 114, 'AutowiredFieldElement.inject —— 只有四行，每行都是考点', ha='center', va='center',
            color=CYAN, fontproperties=F, fontsize=15)
    steps = [
        ('①', 'Field field = (Field) this.member;', '拿到目标字段', BLUE, False),
        ('②', 'resolveFieldValue(field, bean, beanName)', 'DependencyDescriptor → resolveDependency 解析出对象', CYAN, False),
        ('③', 'ReflectionUtils.makeAccessible(field);', '干掉 private 访问限制', BLUE, False),
        ('④', 'field.set(bean, value);', '反射写入！值就这样进了字段', GOLD, True),
    ]
    y = 160
    for num, code, note, c, hl in steps:
        box(ax, 70, y, 960, 148, fc=HL if hl else CARD, ec=EDGE_HL if hl else EDGE, lw=1.9 if hl else 1.1)
        ax.add_patch(Circle((126, y + 74), 28, facecolor=GOLD if hl else '#1E4C8A', edgecolor='none'))
        ax.text(126, y + 74, num, ha='center', va='center', color='#0A1729' if hl else WHITE,
                fontproperties=FB, fontsize=17)
        ax.text(180, y + 52, code, ha='left', va='center', color=GOLD if hl else CYAN,
                fontproperties=FM, fontsize=14)
        ax.text(180, y + 100, note, ha='left', va='center', color=WHITE if not hl else '#EFE0A8',
                fontproperties=F, fontsize=15)
        if y < 640:
            arrow(ax, 550, y + 148, 550, y + 180, color='#24456E', lw=1.8)
        y += 180
    box(ax, 70, 880, 960, 90, fc=HL, ec=GOLD, lw=1.6)
    ax.text(550, 912, '它绕过了 private、也绕过了构造方法', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=16)
    ax.text(550, 946, '因为字段注入「本来就不是」通过构造方法完成的', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def gouzaoqi(path):
    W, H = 1100, 1020
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '两条注入路径：时机完全不同', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    y0 = 260
    ax.plot([110, 1010], [y0, y0], color='#2A4E7A', lw=6, solid_capstyle='round')
    for x1, x2, name in [(110, 400, 'createBeanInstance'), (400, 700, 'populateBean'), (700, 1010, 'initializeBean')]:
        ax.plot([x1, x2], [y0, y0], color=BLUE, lw=6)
        ax.text((x1 + x2) / 2, y0 - 32, name, ha='center', va='center', color=WHITE,
                fontproperties=FM, fontsize=13)
    ax.plot([255, 255], [y0 - 14, y0 + 66], color=GOLD, lw=3)
    ax.add_patch(Circle((255, y0), 11, facecolor=GOLD, edgecolor='none'))
    ax.text(255, y0 + 88, '构造器注入', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=16)
    ax.text(255, y0 + 118, '在实例化阶段就解析依赖', ha='center', va='center', color=GOLD,
            fontproperties=F, fontsize=13)
    ax.text(255, y0 + 146, '→ 依赖是「造对象的前提」', ha='center', va='center', color=GREY,
            fontproperties=F, fontsize=13)
    ax.plot([550, 550], [y0 - 14, y0 + 66], color=CYAN, lw=3)
    ax.add_patch(Circle((550, y0), 11, facecolor=CYAN, edgecolor='none'))
    ax.text(550, y0 + 88, '字段 / setter 注入', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=16)
    ax.text(550, y0 + 118, '在属性填充阶段才反射塞进去', ha='center', va='center', color=CYAN,
            fontproperties=F, fontsize=13)
    ax.text(550, y0 + 146, '→ 对象先造出来，依赖此时全是 null', ha='center', va='center', color=GREY,
            fontproperties=F, fontsize=13)
    box(ax, 60, 560, 480, 340, ec=GOLD, lw=1.7, fc=HL)
    ax.text(300, 606, '构造器注入', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=20)
    for i, ln in enumerate(['实例化时就解析依赖', '对象「一次成型」', '字段可用 final ✓',
                            '单元测试可直接 new ✓', '失败更早、报错更准 ✓']):
        ax.text(95, 660 + i * 44, '· ' + ln, ha='left', va='center', color='#EFE0A8', fontproperties=F, fontsize=15)
    box(ax, 560, 560, 480, 340, ec=RED, lw=1.7)
    ax.text(800, 606, '字段注入', ha='center', va='center', color=RED, fontproperties=FB, fontsize=20)
    for i, ln in enumerate(['无参构造先造空壳', '存在"依赖为 null 的窗口期"', '字段不能 final（语义上不可变被破坏）',
                            '单测必须启动容器', '报错更晚（populateBean 才炸）']):
        ax.text(595, 660 + i * 44, '· ' + ln, ha='left', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(W / 2, 960, '★ 「官方推荐构造器注入」不是风格偏好，是「依赖注入的时机」决定的',
            ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=15)
    save(fig, path)


def qiyi(path):
    W, H = 1100, 1080
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '多个同类型 Bean，到底注入哪个？', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=27)
    ax.text(W / 2, 114, 'DefaultListableBeanFactory.determineAutowireCandidate —— 固定五步', ha='center',
            va='center', color=CYAN, fontproperties=F, fontsize=13)
    rows = [
        ('Step 1', '@Primary', '有 primary 直接胜出；两个 primary 直接报错', GOLD),
        ('Step 2a', '依赖名 = bean 名', '字段名 / 参数名 与 bean 名匹配', CYAN),
        ('Step 2b', '@Qualifier', '按限定符建议的名称匹配', CYAN),
        ('Step 3', '@Priority', '优先级值最小（最高）者胜出', BLUE),
        ('Step 4', 'default-candidate', '仅当只有一个 default 候选时才有效', BLUE),
        ('Step 5', '直接注册的依赖', '兜底：self reference 场景', GREY),
    ]
    y = 158
    for tag, name, note, c in rows:
        box(ax, 70, y, 960, 108, ec=c if c != GREY else EDGE, lw=1.5 if c != GREY else 1.0)
        ax.text(112, y + 54, tag, ha='left', va='center', color=c, fontproperties=FMB, fontsize=14)
        fp = FM if name.isascii() else F
        ax.text(230, y + 54, name, ha='left', va='center', color=c if c != GREY else WHITE,
                fontproperties=fp, fontsize=15)
        ax.text(500, y + 54, note, ha='left', va='center', color=GREY, fontproperties=F, fontsize=13.5)
        if y < 700:
            arrow(ax, 550, y + 108, 550, y + 136, color='#24456E', lw=1.6)
        y += 136
    box(ax, 70, 890, 470, 90, fc='#2A1518', ec=RED, lw=1.4)
    ax.text(305, 922, '一个都没有 →', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(305, 954, 'NoSuchBeanDefinitionException', ha='center', va='center', color=RED,
            fontproperties=FM, fontsize=12.5)
    box(ax, 560, 890, 480, 90, fc='#2A1518', ec=RED, lw=1.4)
    ax.text(800, 922, '裁决不出（规则全平）→', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(800, 954, 'NoUniqueBeanDefinitionException', ha='center', va='center', color=RED,
            fontproperties=FM, fontsize=12.5)
    ax.text(W / 2, 1030, '★ 你线上遇到的「注入歧义」报错，就出自这里', ha='center', va='center',
            color=GOLD, fontproperties=FB, fontsize=15)
    save(fig, path)


if __name__ == '__main__':
    out = '/sandbox/workspace/output/'
    cover(out + 'src4-fengmian.png')
    liucheng(out + 'src4-liucheng.png')
    fanshe(out + 'src4-fanshe.png')
    gouzaoqi(out + 'src4-gouzaoqi.png')
    qiyi(out + 'src4-qiyi.png')
