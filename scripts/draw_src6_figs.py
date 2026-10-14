#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇6 信息图：封面 / 拦截器位置 / this 自调用 / 六类失效 / 传播边界"""
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
    # 右侧流程竖排
    bx, bw = 830, 360
    box(ax, bx, 130, bw, 74, fc='#0E2444', ec=BLUE, lw=1.8)
    ax.text(bx + bw / 2, 167, '@Transactional 方法', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=17)
    arrow(ax, bx + bw / 2, 206, bx + bw / 2, 244)
    box(ax, bx, 244, bw, 74, fc='#0E2444', ec=CYAN, lw=1.8)
    ax.text(bx + bw / 2, 281, '代理对象 invoke()', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=17)
    arrow(ax, bx + bw / 2, 320, bx + bw / 2, 358)
    box(ax, bx, 358, bw, 84, fc='#0E2444', ec=GOLD, lw=1.8)
    ax.text(bx + bw / 2, 388, 'TransactionInterceptor', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=14)
    ax.text(bx + bw / 2, 418, 'invokeWithinTransaction', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=12)
    arrow(ax, bx + bw / 2, 444, bx + bw / 2, 482)
    box(ax, bx, 482, bw, 66, fc='#0E2444', ec=GREEN, lw=1.8)
    ax.text(bx + bw / 2, 515, '开事务 / 提交 / 回滚', ha='center', va='center', color=GREEN, fontproperties=FB, fontsize=16)
    ax.text(1010, 590, '没经过代理 = 没有事务', ha='center', va='center', color=GREY, fontproperties=F, fontsize=16)
    for px, py, s, c in [(620, 116, 10, CYAN), (700, 652, 8, GOLD), (640, 452, 9, BLUE)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 6 篇 ｜ @Transactional 事务失效', color=GOLD, fontproperties=FB, fontsize=24, va='center')
    ax.text(90, 466, '问题从来不在注解，在代理', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def weizhi(path):
    W, H = 1100, 900
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 66, '事务拦截器在 AOP 链中的位置', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=28)
    ax.text(W / 2, 108, 'TransactionInterceptor 本质就是一个 MethodInterceptor', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 360, 150, 380, 66, ec=BLUE, lw=1.8)
    ax.text(550, 183, '外部调用 service.pay()', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=17)
    arrow(ax, 550, 218, 550, 262)
    box(ax, 250, 262, 600, 330, fc='#0B1C33', ec=CYAN, lw=1.6)
    ax.text(550, 300, '代理对象的拦截器链', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=18)
    box(ax, 300, 336, 500, 62, ec=EDGE, lw=1.3)
    ax.text(550, 367, '其他通知（日志 / 权限 ...）', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(300, 470, '->', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=20)
    box(ax, 300, 410, 500, 70, fc='#2B2A12', ec=GOLD, lw=2.2)
    ax.text(550, 434, 'TransactionInterceptor.invoke()', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=15)
    ax.text(550, 462, '事务在此开启', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=14)
    box(ax, 300, 500, 500, 62, fc='#0E2444', ec=GREEN, lw=1.3)
    ax.text(550, 531, '目标方法 invocation.proceed()', ha='center', va='center', color=GREEN, fontproperties=F, fontsize=15)
    arrow(ax, 550, 596, 550, 648)
    box(ax, 300, 648, 500, 72, fc='#0E2444', ec=CYAN, lw=1.6)
    ax.text(550, 684, '返回 -> 提交 / 异常 -> 回滚', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=17)
    ax.text(W / 2, 790, '事务只是链上的一个环节：链走不到它，事务就不存在', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    save(fig, path)


def zidiaoyong(path):
    W, H = 1100, 860
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 66, '为什么 this.method() 事务失效？', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=28)
    ax.text(W / 2, 108, '外部调用走代理，自调用走 this——this 不是代理', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    # 上半：外部调用 OK
    box(ax, 80, 150, 940, 300, fc='#0B1C33', ec=EDGE, lw=1.3)
    ax.text(120, 190, '外部调用（正常）', ha='left', va='center', color=GREEN, fontproperties=FB, fontsize=18)
    box(ax, 140, 230, 200, 70, fc='#0E2444', ec=BLUE, lw=1.6)
    ax.text(240, 265, '代理对象', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=16)
    arrow(ax, 344, 265, 480, 265, color=CYAN)
    box(ax, 484, 230, 190, 70, fc='#2B2A12', ec=GOLD, lw=1.8)
    ax.text(579, 265, '事务拦截器', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=15)
    arrow(ax, 678, 265, 814, 265, color=CYAN)
    box(ax, 818, 230, 160, 70, fc='#0E2444', ec=GREEN, lw=1.6)
    ax.text(898, 265, '目标方法', ha='center', va='center', color=GREEN, fontproperties=FB, fontsize=16)
    ax.text(550, 355, 'pay() 经过代理 -> 进拦截器 -> 事务开启  OK', ha='center', va='center', color=GREEN, fontproperties=F, fontsize=15)
    ax.text(550, 405, 'pay() 内部再执行 this.recordLog() 时：', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    # 下半：自调用 NG
    box(ax, 80, 460, 940, 300, fc='#1A1016', ec='#5A2530', lw=1.3)
    ax.text(120, 500, '内部自调用（失效）', ha='left', va='center', color=RED, fontproperties=FB, fontsize=18)
    box(ax, 440, 540, 220, 74, fc='#0E2444', ec=GOLD, lw=1.6)
    ax.text(550, 577, '目标对象 (this)', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=16)
    # 自调用弧线绕过代理
    ax.add_patch(FancyArrowPatch((550, 540), (550, 500), arrowstyle='-|>', mutation_scale=16,
                 color=RED, lw=2.2, connectionstyle='arc3,rad=0.5'))
    ax.text(700, 520, 'this.recordLog()', ha='left', va='center', color=RED, fontproperties=FM, fontsize=14)
    ax.text(550, 660, '直接调本类方法，不经过代理 -> 不进拦截器 -> 无事务', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    ax.text(550, 712, '修法：拆到别的 Bean / 注入自身代理 / AopContext.currentProxy()', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=14)
    save(fig, path)


def shixiao(path):
    W, H = 1100, 1000
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 66, '@Transactional 失效的六种典型', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=28)
    ax.text(W / 2, 108, '每一种都能在源码里找到确切位置', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    rows = [
        ('1', 'this.method() 自调用', 'this 不是代理，不进 invoke()', GOLD),
        ('2', '方法不是 public', 'computeTransactionAttribute 返回 null', GOLD),
        ('3', '异常被自己 catch 掉', '拦截器看不到异常 -> 提交', CYAN),
        ('4', '异常类型不匹配', 'rollbackOn 默认只认 RuntimeException', CYAN),
        ('5', '跨线程调用', '事务状态在 ThreadLocal，不跨线程', BLUE),
        ('6', '对象不是 Spring Bean', 'new 出来的没有代理', BLUE),
    ]
    y = 160
    for num, title, reason, c in rows:
        box(ax, 80, y, 940, 112, fc=CARD, ec=EDGE, lw=1.2)
        ax.add_patch(Circle((140, y + 56), 26, facecolor='#0E2444', edgecolor=c, lw=1.6))
        ax.text(140, y + 56, num, ha='center', va='center', color=c, fontproperties=FMB, fontsize=18)
        ax.text(200, y + 42, title, ha='left', va='center', color=WHITE, fontproperties=FB, fontsize=18)
        ax.text(200, y + 80, reason, ha='left', va='center', color=GREY, fontproperties=F, fontsize=14)
        y += 130
    save(fig, path)


def chuanbo(path):
    W, H = 1100, 820
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 66, 'REQUIRED 与 REQUIRES_NEW 的事务边界', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=26)
    ax.text(W / 2, 108, '传播行为的前提：外层事务真的存在（同样依赖代理）', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    # 左列 REQUIRED
    box(ax, 70, 150, 460, 560, fc='#0B1C33', ec=EDGE, lw=1.3)
    ax.text(300, 195, 'REQUIRED（默认）', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=21)
    box(ax, 110, 240, 380, 190, fc='#0E2444', ec=BLUE, lw=1.6)
    ax.text(300, 275, '外层事务', ha='center', va='center', color=BLUE, fontproperties=FB, fontsize=17)
    box(ax, 150, 320, 300, 88, fc='#2B2A12', ec=GOLD, lw=1.8)
    ax.text(300, 364, '内层方法：加入', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=16)
    ax.text(300, 470, '同一个事务', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=16)
    ax.text(300, 512, '内层回滚 -> 外层一起回滚', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(300, 610, '有外层就加入', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(300, 650, '无外层就新建', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    # 右列 REQUIRES_NEW
    box(ax, 570, 150, 460, 560, fc='#0B1C33', ec=EDGE, lw=1.3)
    ax.text(800, 195, 'REQUIRES_NEW', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=21)
    box(ax, 610, 240, 380, 90, fc='#0E2444', ec='#5C7FA8', lw=1.4)
    ax.text(800, 285, '外层事务：挂起', ha='center', va='center', color='#8FB4E0', fontproperties=FB, fontsize=16)
    box(ax, 610, 348, 380, 96, fc='#2B2A12', ec=GOLD, lw=1.8)
    ax.text(800, 396, '内层：另起新事务', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=16)
    ax.text(800, 490, '两个独立事务', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=16)
    ax.text(800, 532, '内层回滚不影响外层', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    ax.text(800, 610, '注意：自调用时外层不存在', ha='center', va='center', color=RED, fontproperties=F, fontsize=14)
    ax.text(800, 650, '挂起也就无从谈起', ha='center', va='center', color=RED, fontproperties=F, fontsize=14)
    save(fig, path)


if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    cover('output/src6-fengmian.png')
    weizhi('output/src6-weizhi.png')
    zidiaoyong('output/src6-zidiaoyong.png')
    shixiao('output/src6-shixiao.png')
    chuanbo('output/src6-chuanbo.png')
