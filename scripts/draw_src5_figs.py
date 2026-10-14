#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇5 信息图：封面 / 选择逻辑 / 代理链 / proceed递归 / 通知顺序"""
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
    # 右侧：分叉 → 两个代理
    ax.add_patch(Circle((830, 200), 46, facecolor='#0E2444', edgecolor=BLUE, lw=2))
    ax.text(830, 200, 'Bean', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=15)
    arrow(ax, 866, 232, 950, 300, color=CYAN, lw=2.4)
    arrow(ax, 866, 240, 1080, 300, color=GOLD, lw=2.4)
    box(ax, 890, 310, 190, 96, fc='#0E2444', ec=CYAN, lw=1.8)
    ax.text(985, 344, 'JDK', ha='center', va='center', color=CYAN, fontproperties=FMB, fontsize=22)
    ax.text(985, 382, '动态代理', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=15)
    box(ax, 1100, 310, 150, 96, fc='#0E2444', ec=GOLD, lw=1.8)
    ax.text(1175, 344, 'CGLIB', ha='center', va='center', color=GOLD, fontproperties=FMB, fontsize=20)
    ax.text(1175, 382, '子类代理', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=15)
    ax.text(1030, 470, '怎么选？看一个 if', ha='center', va='center', color=GREY, fontproperties=F, fontsize=16)
    for px, py, s, c in [(300, 120, 10, CYAN), (620, 650, 8, GOLD), (200, 600, 9, BLUE)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 5 篇 ｜ AOP 代理生成', color=GOLD, fontproperties=FB, fontsize=26, va='center')
    ax.text(90, 466, 'JDK 还是 CGLIB，Spring 怎么选', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def xuanze(path):
    W, H = 1100, 1200
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '谁决定用 JDK 还是 CGLIB？', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    ax.text(W / 2, 112, 'DefaultAopProxyFactory.createAopProxy() 里的一个 if', ha='center', va='center',
            color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 300, 150, 500, 76, ec=BLUE, lw=1.8)
    ax.text(550, 188, 'createAopProxy()', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=17)
    arrow(ax, 550, 226, 550, 268)
    box(ax, 110, 268, 880, 116, fc=CARD2, ec=CYAN, lw=1.7)
    ax.text(550, 302, 'isOptimize()  ‖  isProxyTargetClass()  ‖  !hasUserSuppliedInterfaces()', ha='center',
            va='center', color=CYAN, fontproperties=FM, fontsize=13)
    ax.text(550, 342, '三个条件满足任一 → 进入「CGLIB 分支」', ha='center', va='center',
            color=WHITE, fontproperties=F, fontsize=15)
    arrow(ax, 260, 384, 260, 424, color=GOLD)
    ax.text(250, 404, '是', ha='right', va='center', color=GOLD, fontproperties=FB, fontsize=14)
    arrow(ax, 860, 384, 860, 424, color=CYAN)
    ax.text(872, 404, '否', ha='left', va='center', color=CYAN, fontproperties=FB, fontsize=14)
    box(ax, 60, 424, 400, 150, ec=GOLD, lw=1.7)
    ax.text(260, 460, '目标类还需要检查', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=16)
    ax.text(260, 502, '是接口 / 代理类 / lambda ？', ha='center', va='center', color=WHITE,
            fontproperties=F, fontsize=14)
    ax.text(260, 542, '是 → 仍然退回 JDK', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    box(ax, 660, 424, 380, 150, ec=CYAN, lw=1.7)
    ax.text(850, 466, 'JDK 动态代理', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=18)
    ax.text(850, 508, 'JdkDynamicAopProxy', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    ax.text(850, 544, '有用户接口且未强制', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    arrow(ax, 260, 574, 260, 616, color=BLUE)
    box(ax, 60, 616, 400, 120, ec=BLUE, lw=1.7)
    ax.text(260, 654, '不是 → CGLIB', ha='center', va='center', color=BLUE, fontproperties=FB, fontsize=17)
    ax.text(260, 698, 'ObjenesisCglibAopProxy', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    box(ax, 60, 790, 980, 150, fc=HL, ec=GOLD, lw=1.6)
    ax.text(550, 830, '流传很广的「有接口用 JDK，没接口用 CGLIB」', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=15)
    ax.text(550, 872, '只是这条逻辑的通俗版', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(550, 916, '准确版就是上面这三句', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=17)
    ax.text(W / 2, 1010, '★ 注意「CGLIB 分支」里还有一次「退回 JDK」的判断', ha='center', va='center',
            color=CYAN, fontproperties=FB, fontsize=15)
    ax.text(W / 2, 1070, '（6.2 起还多了 lambda 类判断）', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=13)
    save(fig, path)


def lian(path):
    W, H = 1100, 1000
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '两条路，同一套执行机制', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    box(ax, 90, 150, 440, 96, ec=BLUE, lw=1.8)
    ax.text(310, 184, '调用方法', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=17)
    ax.text(310, 218, '（从代理对象进入）', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    box(ax, 570, 150, 440, 96, ec=GOLD, lw=1.8)
    ax.text(790, 184, '取拦截器链', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=17)
    ax.text(790, 218, 'getInterceptorsAndDynamicInterceptionAdvice', ha='center', va='center',
            color=GREY, fontproperties=FM, fontsize=10.5)
    arrow(ax, 530, 198, 570, 198, color=CYAN, lw=2.4)
    arrow(ax, 790, 246, 790, 292)
    box(ax, 90, 292, 920, 120, fc=CARD2, ec=CYAN, lw=1.5)
    ax.text(550, 326, '链为空 ？', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=16)
    ax.text(300, 380, '空 → 直接反射调用目标方法', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(810, 380, '不空 → invocation.proceed()', ha='center', va='center', color=GOLD,
            fontproperties=F, fontsize=14)
    arrow(ax, 300, 412, 300, 470, color=GREY)
    arrow(ax, 810, 412, 810, 470, color=GOLD)
    box(ax, 120, 470, 360, 78, ec=GREY, lw=1.3)
    ax.text(300, 509, 'invokeJoinpoint()', ha='center', va='center', color=GREY, fontproperties=FM, fontsize=14)
    box(ax, 560, 470, 480, 250, ec=GOLD, lw=1.7, fc=HL)
    ax.text(800, 504, '拦截器链', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=18)
    chain = ['拦截器 1', '拦截器 2', '…', '目标方法']
    for i, c in enumerate(chain):
        yy = 540 + i * 44
        fp = F
        ax.text(610, yy, '·', ha='left', va='center', color=GOLD, fontproperties=F, fontsize=15)
        ax.text(645, yy, c, ha='left', va='center', color='#EFE0A8' if i < 3 else GREEN,
                fontproperties=fp, fontsize=15)
    box(ax, 90, 770, 920, 150, fc=CARD2, ec=BLUE, lw=1.4)
    ax.text(550, 810, 'JDK 与 CGLIB 的差别，只在「代理类怎么生成」', ha='center', va='center',
            color=WHITE, fontproperties=FB, fontsize=16)
    ax.text(550, 850, 'JdkDynamicAopProxy.invoke  |  CglibAopProxy.DynamicAdvisedInterceptor.intercept',
            ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=11.5)
    ax.text(550, 890, '执行机制（取链 → proceed）完全共用', ha='center', va='center',
            color=GOLD, fontproperties=FB, fontsize=15)
    ax.text(W / 2, 970, '★ 这就是为什么「AOP 原理」的答案，一半都是同一段逻辑',
            ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def proceed(path):
    W, H = 1100, 1180
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, 'proceed()：拦截器链的递归真相', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=27)
    ax.text(W / 2, 112, 'ReflectiveMethodInvocation.proceed()', ha='center', va='center',
            color=CYAN, fontproperties=FM, fontsize=14)
    # 嵌套示意：进入
    layers = [
        ('拦截器 1.invoke(this)', BLUE, 60, 170),
        ('拦截器 2.invoke(this)', CYAN, 150, 170),
        ('目标方法（invokeJoinpoint）', GREEN, 240, 170),
    ]
    ax.text(90, 178, '进入 ↓', ha='left', va='center', color=GREY, fontproperties=FB, fontsize=15)
    for i, (name, c, off, hh) in enumerate([('拦截器 1.invoke(this)', BLUE, 0, 300),
                                            ('拦截器 2.invoke(this)', CYAN, 70, 220),
                                            ('目标方法', GREEN, 140, 140)]):
        x = 200 + off
        y = 230 + i * 0
        box(ax, 200 + off, 220 + i * 130, 700 - off * 2, 110, ec=c, lw=1.9)
        ax.text(550, 258 + i * 130, name, ha='center', va='center', color=c, fontproperties=FB, fontsize=17)
        if i < 2:
            ax.text(550, 292 + i * 130, '内部调用 proceed() → 进入下一层', ha='center', va='center',
                    color=GREY, fontproperties=F, fontsize=13)
    ax.text(90, 620, '返回 ↑', ha='left', va='center', color=GREY, fontproperties=FB, fontsize=15)
    ax.text(550, 660, '目标方法返回 → 拦截器 2 的后置逻辑 → 拦截器 1 的后置逻辑', ha='center', va='center',
            color='#EFE0A8', fontproperties=F, fontsize=15)
    box(ax, 70, 710, 960, 130, fc=CARD2, ec=CYAN, lw=1.5)
    ax.text(550, 748, '索引从 -1 开始，每个拦截器 +1；走到最后一个 → invokeJoinpoint()', ha='center',
            va='center', color=WHITE, fontproperties=F, fontsize=15)
    ax.text(550, 792, '动态匹配失败 → 跳过该拦截器，直接 proceed() 下一个', ha='center',
            va='center', color=GREY, fontproperties=F, fontsize=14)
    box(ax, 70, 880, 960, 130, fc='#2A1518', ec=RED, lw=1.5)
    ax.text(550, 918, '★ 拦截器不调 proceed() → 链就断了', ha='center', va='center',
            color=RED, fontproperties=FB, fontsize=17)
    ax.text(550, 962, '后面的通知和目标方法都不会执行 —— 这就是 @Around 能"拦下"调用的原理',
            ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(W / 2, 1070, '所谓「拦截器链」，本质是「一层套一层的递归调用」', ha='center', va='center',
            color=GOLD, fontproperties=FB, fontsize=16)
    save(fig, path)


def shunxu(path):
    W, H = 1100, 820
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 70, '通知的执行顺序', ha='center', va='center', color=WHITE,
            fontproperties=FB, fontsize=28)
    ax.text(W / 2, 114, '顺序由拦截器链的排列决定（Advisor 排序 / @Order / @Aspect 规则）',
            ha='center', va='center', color=CYAN, fontproperties=F, fontsize=14)
    y0 = 360
    items = [
        ('@Around\n前半段', BLUE), ('@Before', CYAN), ('★ 目标方法', GREEN),
        ('@AfterReturning\n/ @AfterThrowing', CYAN), ('@After', CYAN), ('@Around\n后半段', BLUE),
    ]
    x = 80
    bw = 148
    for i, (name, c) in enumerate(items):
        box(ax, x, y0 - 70, bw, 140, ec=c, lw=1.9, fc=HL if i == 2 else CARD)
        for j, ln in enumerate(name.split('\n')):
            ax.text(x + bw / 2, y0 - 20 + j * 32, ln, ha='center', va='center',
                    color=GOLD if i == 2 else c, fontproperties=FB if i == 2 else F, fontsize=14)
        if i < len(items) - 1:
            arrow(ax, x + bw, y0, x + bw + 24, y0, color='#24456E', lw=2)
        x += bw + 24
    box(ax, 70, 560, 960, 130, fc=HL, ec=GOLD, lw=1.5)
    ax.text(550, 600, '为什么 @Around 能「包住所有人」？', ha='center', va='center', color=GOLD,
            fontproperties=FB, fontsize=17)
    ax.text(550, 644, '因为它的 proceed() 调用点，正好卡在「进入链」和「回来」之间', ha='center',
            va='center', color='#EFE0A8', fontproperties=F, fontsize=15)
    ax.text(W / 2, 740, '★ 这不是魔法，是 proceed() 递归源码的必然结果', ha='center', va='center',
            color=GREY, fontproperties=F, fontsize=15)
    save(fig, path)


if __name__ == '__main__':
    out = '/sandbox/workspace/output/'
    cover(out + 'src5-fengmian.png')
    xuanze(out + 'src5-xuanze.png')
    lian(out + 'src5-lian.png')
    proceed(out + 'src5-proceed.png')
    shunxu(out + 'src5-shunxu.png')
