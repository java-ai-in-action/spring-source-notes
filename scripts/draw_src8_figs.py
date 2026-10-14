#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇8 信息图：封面 / 注解拆解 / 加载链路 / 两级过滤 / SPI文件"""
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
    box(ax, 830, 120, 370, 68, fc='#0E2444', ec=BLUE, lw=1.8)
    ax.text(1015, 154, '@SpringBootApplication', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=14)
    arrow(ax, 1015, 192, 1015, 228)
    box(ax, 830, 228, 370, 66, fc='#0E2444', ec=CYAN, lw=1.8)
    ax.text(1015, 261, '@EnableAutoConfiguration', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    arrow(ax, 1015, 298, 1015, 334)
    box(ax, 830, 334, 370, 66, fc='#2B2A12', ec=GOLD, lw=2.0)
    ax.text(1015, 367, '@Import(ImportSelector)', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=13)
    arrow(ax, 1015, 404, 1015, 440)
    box(ax, 830, 440, 370, 80, fc='#0E2444', ec=GREEN, lw=1.8)
    ax.text(1015, 468, 'META-INF/spring/...imports', ha='center', va='center', color=GREEN, fontproperties=FM, fontsize=12)
    ax.text(1015, 496, '候选配置类名单', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=14)
    ax.text(1015, 570, '约定优于配置，但用户永远优先', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    for px, py, s, c in [(620, 120, 10, CYAN), (700, 648, 8, GOLD), (640, 452, 9, BLUE)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 8 篇 ｜ Spring Boot 自动配置', color=GOLD, fontproperties=FB, fontsize=23, va='center')
    ax.text(90, 466, 'MissingBean 到底"少"了什么', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Boot 3.4.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def chaijie(path):
    W, H = 1100, 720
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, '@SpringBootApplication 拆开是什么', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 102, '一个注解 = 三件事', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 350, 150, 400, 84, fc='#2B2A12', ec=GOLD, lw=2.0)
    ax.text(550, 192, '@SpringBootApplication', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=17)
    xs = [120, 430, 740]
    names = ['@SpringBootConfiguration', '@EnableAutoConfiguration', '@ComponentScan']
    descs = ['本质是 @Configuration\n标记主配置类', '★ 自动配置的总开关', '开启包扫描\n扫 @Service/@Controller']
    cols = [BLUE, GOLD, GREEN]
    for x, n, d, c in zip(xs, names, descs, cols):
        arrow(ax, 550, 236, x + 120, 320, color=c)
        box(ax, x, 322, 240, 120, fc='#0E2444', ec=c, lw=1.7)
        ax.text(x + 120, 355, n, ha='center', va='center', color=c, fontproperties=FM, fontsize=10.5)
        ax.text(x + 120, 400, d, ha='center', va='center', color=WHITE, fontproperties=F, fontsize=13)
    box(ax, 120, 500, 860, 130, fc='#0B1C33', ec=EDGE, lw=1.3)
    ax.text(550, 535, '前两个负责"配置"，第三个负责"扫描你自己写的 Bean"', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    ax.text(550, 585, '自动配置这道题，入口就是 @EnableAutoConfiguration', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    save(fig, path)


def lianlu(path):
    W, H = 1100, 1140
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, '自动配置的加载链路', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 100, '@EnableAutoConfiguration 到最终生效的 Bean', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    steps = [
        ('@EnableAutoConfiguration', '@Import(AutoConfigurationImportSelector)', BLUE),
        ('selectImports()', 'ImportSelector 的入口', CYAN),
        ('getAutoConfigurationEntry()', '读名单 -> 去重 -> 排除 -> 过滤', CYAN),
        ('getCandidateConfigurations()', '委托 ImportCandidates', BLUE),
        ('ImportCandidates.load()', '读 META-INF/spring/*.imports', GOLD),
        ('getConfigurationClassFilter().filter()', 'AutoConfigurationImportFilter 粗筛', GOLD),
        ('@Conditional', 'OnBeanCondition 等逐一评估', GREEN),
        ('AutoConfigured Bean', '生效的自动配置：用户没定义才补上', GREEN),
    ]
    y = 140
    for i, (code, desc, c) in enumerate(steps):
        box(ax, 120, y, 860, 104, fc=CARD, ec=c, lw=1.6 if i in (2, 5, 7) else 1.2)
        ax.text(150, y + 40, code, ha='left', va='center', color=WHITE, fontproperties=FM, fontsize=13)
        ax.text(150, y + 76, desc, ha='left', va='center', color=GREY, fontproperties=F, fontsize=13)
        if i < len(steps) - 1:
            arrow(ax, 550, y + 108, 550, y + 124, color='#3A5A80', lw=1.6)
        y += 124
    save(fig, path)


def guolv(path):
    W, H = 1100, 900
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, '@Conditional 是两级过滤', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 100, '不是"全加载再筛掉"，而是先粗筛、再评估', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 330, 140, 440, 64, ec=BLUE, lw=1.8)
    ax.text(550, 172, '候选名单（.imports）', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=16)
    arrow(ax, 550, 206, 550, 250)
    box(ax, 180, 250, 740, 150, fc='#0B1C33', ec=GOLD, lw=1.7)
    ax.text(550, 285, '第一层：AutoConfigurationImportFilter', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=17)
    ax.text(550, 325, 'OnClassCondition  @Order(HIGHEST_PRECEDENCE)', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=12)
    ax.text(550, 365, '检查要求的类在不在 classpath，快速踢掉不可能生效的', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    arrow(ax, 550, 402, 550, 446)
    box(ax, 180, 446, 740, 150, fc='#0B1C33', ec=GREEN, lw=1.7)
    ax.text(550, 481, '第二层：@Conditional 家族', ha='center', va='center', color=GREEN, fontproperties=FB, fontsize=17)
    ax.text(550, 521, 'OnBeanCondition / OnPropertyCondition ...', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=12)
    ax.text(550, 561, '逐个判定：类 / Bean / 属性 / 是否 Web 应用', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    arrow(ax, 550, 598, 550, 642)
    box(ax, 300, 642, 500, 74, fc='#0E2444', ec=CYAN, lw=1.7)
    ax.text(550, 679, '真正生效的配置类', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=17)
    ax.text(W / 2, 776, '粗筛为了快，评估为了准', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def spi(path):
    W, H = 1100, 900
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, '名单藏在哪：SPI 与 .imports 文件', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=26)
    ax.text(W / 2, 100, '约定路径；classpath 上所有同名文件都会被读进来', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 90, 150, 460, 300, fc='#0B1C33', ec=GOLD, lw=1.6)
    ax.text(320, 188, '配置文件名（写死的路径）', ha='center', va='center', color=GOLD, fontproperties=FB, fontsize=16)
    ax.text(320, 244, 'META-INF/spring/', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=13)
    ax.text(320, 282, 'org.springframework.boot', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=13)
    ax.text(320, 320, '.autoconfigure', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=13)
    ax.text(320, 358, 'AutoConfiguration.imports', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=13)
    ax.text(320, 410, 'LOCATION = "META-INF/spring/%s.imports"', ha='center', va='center', color=GREY, fontproperties=FM, fontsize=10)
    # 右侧：内容示例
    box(ax, 600, 150, 410, 300, fc='#0B1C33', ec=CYAN, lw=1.6)
    ax.text(805, 188, '文件内容（一行一个类）', ha='center', va='center', color=CYAN, fontproperties=FB, fontsize=16)
    lines = ['# Auto Configure', 'org.s.b.autoconfigure.a.A', 'org.s.b.autoconfigure.b.B', 'org.s.b.autoconfigure.c.C', '...']
    for i, ln in enumerate(lines):
        c = GREY if ln.startswith('#') else WHITE
        ax.text(630, 232 + i * 38, ln, ha='left', va='center', color=c, fontproperties=FM, fontsize=12)
    arrow(ax, 550, 300, 600, 300, color=GOLD)
    box(ax, 90, 500, 920, 120, fc='#0B1C33', ec=EDGE, lw=1.3)
    ax.text(550, 538, 'Java SPI：不硬编码，靠约定路径的配置文件发现实现', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=16)
    ax.text(550, 582, 'Boot 3.0 起只认 .imports；老版 spring.factories 的自动配置条目已移除', ha='center', va='center', color=GOLD, fontproperties=F, fontsize=14)
    save(fig, path)


if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    cover('output/src8-fengmian.png')
    chaijie('output/src8-chaijie.png')
    lianlu('output/src8-lianlu.png')
    guolv('output/src8-guolv.png')
    spi('output/src8-spi.png')
