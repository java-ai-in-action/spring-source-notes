#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇3 信息图全套：封面 / 三级缓存结构 / A-B时序 / 构造器注入时间差 / 三级vs两级"""
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


def arrow(ax, x1, y1, x2, y2, color=CYAN, lw=2.2, ls='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=18,
                 color=color, lw=lw, shrinkA=0, shrinkB=0, linestyle=ls))


def save(fig, path):
    fig.savefig(path, facecolor=BG); plt.close(fig); print('saved:', path)


def cover(path):
    W, H = 1280, 720
    fig, ax = new_fig(W, H)
    for gx in range(0, W, 80):
        ax.plot([gx, gx], [0, H], color='#123055', lw=0.6, alpha=0.5)
    for gy in range(0, H, 80):
        ax.plot([0, W], [gy, gy], color='#123055', lw=0.6, alpha=0.5)
    # 右侧：A↔B 循环 + 三层缓存
    ax.add_patch(Circle((880, 220), 54, facecolor='#0E2444', edgecolor=BLUE, lw=2))
    ax.text(880, 220, 'A', ha='center', va='center', color=WHITE, fontproperties=FMB, fontsize=26)
    ax.add_patch(Circle((1080, 220), 54, facecolor='#0E2444', edgecolor=GOLD, lw=2))
    ax.text(1080, 220, 'B', ha='center', va='center', color=WHITE, fontproperties=FMB, fontsize=26)
    arrow(ax, 934, 196, 1026, 196, color=CYAN, lw=2.4)
    arrow(ax, 1026, 246, 934, 246, color=GOLD, lw=2.4)
    for i, (t, c) in enumerate([('一级', BLUE), ('二级', CYAN), ('三级', GOLD)]):
        yy = 360 + i * 82
        box(ax, 790, yy, 340, 64, fc='#0E2444', ec=c, lw=1.8, r=8)
        ax.text(960, yy + 32, t + '缓存', ha='center', va='center', color=c, fontproperties=FB, fontsize=20)
    for px, py, s, c in [(300, 120, 10, CYAN), (1180, 560, 8, GOLD), (620, 640, 7, BLUE), (200, 600, 9, CYAN)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 3 篇 ｜ 三级缓存与循环依赖', color=GOLD, fontproperties=FB, fontsize=25, va='center')
    ax.text(90, 466, '为什么构造器注入救不了', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def sanji(path):
    W, H = 1100, 1120
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 72, '三级缓存结构对照', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=28)
    ax.text(W / 2, 116, 'DefaultSingletonBeanRegistry 里的三个 Map', ha='center', va='center',
            color=CYAN, fontproperties=F, fontsize=15)
    rows = [
        ('一级', 'singletonObjects', '成品单例（能用）', '初始化完成后写入', 'getBean 首先命中', BLUE),
        ('二级', 'earlySingletonObjects', '早期引用（半成品）', '三级被取用时写入', '再次被依赖时命中', CYAN),
        ('三级', 'singletonFactories', 'ObjectFactory（工厂）', '实例化后 addSingletonFactory', '需要早期引用时才调用', GOLD),
    ]
    y = 168
    for tag, name, what, when, read, c in rows:
        box(ax, 60, y, 980, 250, ec=c, lw=1.8)
        ax.add_patch(Circle((122, y + 60), 34, facecolor=c, edgecolor='none'))
        ax.text(122, y + 60, tag, ha='center', va='center', color='#0A1729', fontproperties=FB, fontsize=19)
        ax.text(180, y + 46, name, ha='left', va='center', color=c, fontproperties=FM, fontsize=17)
        ax.text(180, y + 88, '存什么：' + what, ha='left', va='center', color=WHITE, fontproperties=F, fontsize=16)
        ax.text(180, y + 136, '写：' + when, ha='left', va='center', color=GREY, fontproperties=F, fontsize=14.5)
        ax.text(180, y + 176, '读：' + read, ha='left', va='center', color=GREY, fontproperties=F, fontsize=14.5)
        y += 280
    ax.text(W / 2, 1040, '★ 三级取出的不是对象，是工厂：调 getObject() 现场产出 → 工厂移除、结果升入二级',
            ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=15)
    save(fig, path)


def shixu(path):
    W, H = 1100, 1300
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, 'A ↔ B 循环依赖：完整时序', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    ax.text(W / 2, 112, 'A、B 互相 setter 注入（getBean(A) 开始）', ha='center', va='center',
            color=CYAN, fontproperties=F, fontsize=15)
    steps = [
        ('A', '① createBeanInstance(A)：造出 A 空壳（字段全 null）', BLUE),
        ('A', '② addSingletonFactory(A)：把 A 的工厂放进「三级」', GOLD),
        ('A', '③ populateBean(A) 需要 B → getBean(B)', BLUE),
        ('B', '④ B 造出空壳 → B 的工厂入「三级」', GOLD),
        ('B', '⑤ populateBean(B) 要 A → getSingleton(A) 三级命中', GOLD),
        ('—', '   → 取出 A 早期引用，工厂撤销、结果升入「二级」', CYAN),
        ('B', '⑥ B 注入 A → B 初始化完成 → B 入「一级」', GREEN),
        ('A', '⑦ 回到 A：拿到已完成的 B → A 初始化完成 → A 入「一级」', GREEN),
    ]
    y = 164
    for tag, txt, c in steps:
        box(ax, 70, y, 960, 118, fc=CARD if tag != '—' else CARD2, ec=c if tag != '—' else EDGE, lw=1.5 if tag != '—' else 1.0)
        if tag != '—':
            ax.add_patch(Circle((130, y + 59), 30, facecolor=c if c != GREEN else '#1B2C18',
                                edgecolor=c, lw=2))
            ax.text(130, y + 59, tag, ha='center', va='center',
                    color='#0A1729' if c in (GOLD,) else WHITE, fontproperties=FMB, fontsize=19)
        fp = FM if txt.isascii() else F
        ax.text(185, y + 59, txt, ha='left', va='center', color=WHITE if tag != '—' else GREY,
                fontproperties=fp, fontsize=15)
        if y < 1000:
            arrow(ax, 550, y + 118, 550, y + 148, color='#24456E', lw=1.6)
        y += 148
    box(ax, 70, 1050, 960, 120, fc='#1B2C18', ec=GREEN, lw=1.6)
    ax.text(550, 1082, '★ 关键在第 ② 步：A 还没"完工"，就先把"能产出自己的工厂"挂了出去',
            ha='center', va='center', color=GREEN, fontproperties=FB, fontsize=16)
    ax.text(550, 1130, '打破循环的不是缓存本身，而是「早期引用」这个提前暴露的机制',
            ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def gouzaoqi(path):
    W, H = 1100, 1020
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '为什么构造器注入救不了：一个"时间差"', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=26)
    # doCreateBean 时间轴
    y0 = 300
    ax.plot([110, 1010], [y0, y0], color='#2A4E7A', lw=6, solid_capstyle='round')
    segs = [(110, 330, 'createBeanInstance'), (330, 520, 'addSingletonFactory'),
            (520, 760, 'populateBean'), (760, 1010, 'initializeBean')]
    for x1, x2, name in segs:
        ax.plot([x1, x2], [y0, y0], color=BLUE, lw=6)
        fp = FM if name.isascii() else F
        ax.text((x1 + x2) / 2, y0 - 34, name, ha='center', va='center', color=WHITE,
                fontproperties=fp, fontsize=13)
    # 构造器注入依赖点（在 createBeanInstance 内）
    ax.plot([220, 220], [y0 - 14, y0 + 74], color=RED, lw=2.5)
    ax.add_patch(Circle((220, y0), 10, facecolor=RED, edgecolor='none'))
    ax.text(220, y0 + 96, '构造器注入：依赖在这里解析', ha='center', va='center', color=RED,
            fontproperties=FB, fontsize=14)
    ax.text(220, y0 + 126, '但工厂「还没」挂上 → 取不到', ha='center', va='center', color=RED,
            fontproperties=F, fontsize=13)
    # setter 注入依赖点（在 populateBean 内）
    ax.plot([640, 640], [y0 - 14, y0 + 74], color=GREEN, lw=2.5)
    ax.add_patch(Circle((640, y0), 10, facecolor=GREEN, edgecolor='none'))
    ax.text(640, y0 + 96, 'setter/字段注入：依赖在这里解析', ha='center', va='center', color=GREEN,
            fontproperties=FB, fontsize=14)
    ax.text(640, y0 + 126, '工厂已挂上 → 能取到早期引用', ha='center', va='center', color=GREEN,
            fontproperties=F, fontsize=13)
    # 结论
    box(ax, 70, 560, 960, 170, fc=HL, ec=GOLD, lw=1.6)
    ax.text(550, 600, '构造器注入的失败链路', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=19)
    ax.text(550, 648, 'createBeanInstance(A) 要 B → 造 B 时又要 A → getSingleton(A) 三级是空的', ha='center',
            va='center', color='#EFE0A8', fontproperties=F, fontsize=15)
    ax.text(550, 692, '→ beforeSingletonCreation(A) 发现 A 已在创建中 → 抛 BeanCurrentlyInCreationException', ha='center',
            va='center', color='#EFE0A8', fontproperties=F, fontsize=14)
    box(ax, 70, 780, 960, 100, fc='#2A1518', ec=RED, lw=1.4)
    ax.text(550, 818, '一句话：早期引用「实例化之后」才暴露，构造器注入「实例化之时」就要依赖',
            ha='center', va='center', color=RED, fontproperties=FB, fontsize=16)
    ax.text(550, 856, '时间差 → 无解', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def weishenme(path):
    W, H = 1100, 980
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '为什么必须是三级，两级不够？', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    ax.text(W / 2, 114, '关键：三级存的是 ObjectFactory（工厂），不是对象', ha='center', va='center',
            color=CYAN, fontproperties=F, fontsize=16)
    # 左：两级
    box(ax, 60, 160, 460, 620, ec=RED, lw=1.8)
    ax.text(290, 210, '只有两级：缓存里存对象', ha='center', va='center', color=RED,
            fontproperties=FB, fontsize=19)
    for i, ln in enumerate(['放进去之前就得决定', '「要不要生成代理」', '',
                             '→ 要么给所有 Bean 都提前代理', '（没循环依赖的也遭殃，语义/性能全乱）',
                             '', '→ 要么放弃"延迟"这个能力', '', '结论：做不到"按需"']):
        ax.text(95, 268 + i * 48, ln, ha='left', va='center',
                color=WHITE if i < 2 else (GREY if ln else GREY), fontproperties=F, fontsize=15)
    ax.text(290, 726, '× 不可行', ha='center', va='center', color=RED, fontproperties=FB, fontsize=20)
    # 右：三级
    box(ax, 580, 160, 460, 620, ec=GOLD, lw=1.8, fc=HL)
    ax.text(810, 210, '有三级：缓存里存工厂', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=19)
    for i, ln in enumerate(['决定被推迟到', '「真有人来取早期引用」那一刻', '',
                             '→ 没人来取，工厂就一直躺着', '（不执行 → 不生成代理）',
                             '', '→ 代理照旧在"初始化后"生成', '', '结论：做到"按需延迟"']):
        ax.text(615, 268 + i * 48, ln, ha='left', va='center',
                color='#EFE0A8' if i < 2 or i in (3, 6, 8) else GREY, fontproperties=F, fontsize=15)
    ax.text(810, 726, '✓ 正确', ha='center', va='center', color=GREEN, fontproperties=FB, fontsize=20)
    ax.text(W / 2, 860, '★ 三级的本质：用一个 ObjectFactory，把「是否提前代理」的判断推迟到最后一刻',
            ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=16)
    ax.text(W / 2, 910, '这是「代理最晚生成」原则在循环依赖下的妥协方案', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


if __name__ == '__main__':
    out = '/sandbox/workspace/output/'
    cover(out + 'src3-fengmian.png')
    sanji(out + 'src3-sanji.png')
    shixu(out + 'src3-shixu.png')
    gouzaoqi(out + 'src3-gouzaoqi.png')
    weishenme(out + 'src3-weishenme.png')
