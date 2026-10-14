#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇9 信息图：封面 / BFP vs BP / 调用顺序 / 生命周期扩展点 / 用途对照"""
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
    box(ax, 830, 150, 380, 150, fc='#0E2444', ec=GOLD, lw=1.8)
    ax.text(1020, 195, 'BeanFactoryPostProcessor', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=13)
    ax.text(1020, 240, '改「图纸」BeanDefinition', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    ax.text(1020, 275, '只跑一次', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    box(ax, 830, 350, 380, 150, fc='#0E2444', ec=GREEN, lw=1.8)
    ax.text(1020, 395, 'BeanPostProcessor', ha='center', va='center', color=GREEN, fontproperties=FM, fontsize=13)
    ax.text(1020, 440, '改「成品」Bean 实例', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    ax.text(1020, 475, '每个 Bean 都过一遍', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    ax.text(1020, 570, '差一个 Factory，差一个世界', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    for px, py, s, c in [(640, 120, 10, CYAN), (700, 648, 8, GOLD), (640, 452, 9, BLUE)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 9 篇 ｜ 扩展点全景', color=GOLD, fontproperties=FB, fontsize=25, va='center')
    ax.text(90, 466, 'BFP 和 BP，差一个字差一个世界', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def duibi(path):
    W, H = 1100, 820
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, 'BeanFactoryPostProcessor vs BeanPostProcessor', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=22)
    ax.text(W / 2, 102, '一个改"图纸"，一个改"成品"', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    rows = [
        ('调用时机', 'Bean 定义加载后、实例化前', '每个 Bean 实例化后'),
        ('操作对象', 'BeanDefinition（图纸）', 'Bean 实例（成品）'),
        ('调用次数', '一次', '每个 Bean 一次'),
        ('refresh 位置', '第 5 步', '第 6 步注册 / 第 11 步调用'),
        ('典型实现', 'ConfigurationClassPostProcessor', 'AutowiredAnnotationBPP / AutoProxyCreator'),
    ]
    y = 150
    # 表头
    box(ax, 90, y, 240, 66, fc='#0E2444', ec=EDGE, lw=1.2)
    box(ax, 340, y, 330, 66, fc='#2B2A12', ec=GOLD, lw=1.6)
    box(ax, 680, y, 330, 66, fc='#0E2A1E', ec=GREEN, lw=1.6)
    ax.text(210, y + 33, '对比项', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=15)
    ax.text(505, y + 33, 'BFP', ha='center', va='center', color=GOLD, fontproperties=FMB, fontsize=16)
    ax.text(845, y + 33, 'BP', ha='center', va='center', color=GREEN, fontproperties=FMB, fontsize=16)
    y += 66
    for a, b, c in rows:
        box(ax, 90, y, 240, 76, fc=CARD, ec=EDGE, lw=1.1)
        box(ax, 340, y, 330, 76, fc=CARD, ec='#3A3A1E', lw=1.1)
        box(ax, 680, y, 330, 76, fc=CARD, ec='#1E3A2E', lw=1.1)
        ax.text(210, y + 38, a, ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=14)
        ax.text(505, y + 38, b, ha='center', va='center', color=GREY, fontproperties=F if not b.isascii() else FM, fontsize=11)
        ax.text(845, y + 38, c, ha='center', va='center', color=GREY, fontproperties=F if not c.isascii() else FM, fontsize=11)
        y += 76
    save(fig, path)


def shunxu(path):
    W, H = 1100, 900
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, 'BFP 的调用顺序', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 102, '先后有序：子接口优先，再按排序接口分三级', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    steps = [
        ('BeanDefinitionRegistryPostProcessor', '能注册新的 BeanDefinition', GOLD),
        ('  PriorityOrdered -> Ordered -> others', '三级排序', GREY),
        ('BeanFactoryPostProcessor', '普通 BFP', CYAN),
        ('  PriorityOrdered -> Ordered -> others', '三级排序', GREY),
        ('clearMetadataCache()', 'BFP 可能改了元数据，清缓存', GREEN),
    ]
    y = 150
    for code, desc, c in steps:
        ind = code.startswith('  ')
        box(ax, 150 + (60 if ind else 0), y, 800 - (60 if ind else 0), 92, fc=CARD if not ind else CARD2, ec=c, lw=1.2)
        ax.text(190 + (60 if ind else 0), y + 36, code.strip(), ha='left', va='center', color=c if not ind else GREY, fontproperties=FM, fontsize=13)
        ax.text(190 + (60 if ind else 0), y + 68, desc, ha='left', va='center', color=GREY, fontproperties=F, fontsize=12)
        y += 108
    save(fig, path)


def shengming(path):
    W, H = 1100, 960
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, '一个 Bean 的生命周期：扩展点插在哪', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=25)
    ax.text(W / 2, 100, '从上到下，就是它被创建的顺序', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    steps = [
        ('createBeanInstance', '实例化（构造器）', BLUE),
        ('populateBean', '@Autowired 注入（BPP postProcessProperties）', BLUE),
        ('invokeAwareMethods', 'BeanNameAware / BeanFactoryAware 等', CYAN),
        ('applyBPPBeforeInitialization', '@PostConstruct 在这里触发', GOLD),
        ('invokeInitMethods', 'afterPropertiesSet -> init-method', CYAN),
        ('applyBPPAfterInitialization', 'AOP 代理在这里生成', GREEN),
        ('destroy / dispose', '销毁：@PreDestroy / DisposableBean.destroy', GREY),
    ]
    y = 136
    for code, desc, c in steps:
        box(ax, 110, y, 880, 96, fc=CARD, ec=c, lw=1.7 if c in (GOLD, GREEN) else 1.2)
        ax.text(150, y + 38, code, ha='left', va='center', color=WHITE, fontproperties=FM, fontsize=13)
        ax.text(150, y + 72, desc, ha='left', va='center', color=c if c in (GOLD, GREEN) else GREY, fontproperties=F, fontsize=13)
        if y < 136 + 96 * 6:
            arrow(ax, 550, y + 100, 550, y + 116, color='#3A5A80', lw=1.5)
        y += 116
    save(fig, path)


def yongtu(path):
    W, H = 1100, 820
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, '扩展点的典型用途', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 100, 'Spring 的"魔法"，几乎都长在这两类扩展点上', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    rows = [
        ('BeanDefinitionRegistryPostProcessor', 'ConfigurationClassPostProcessor（@Configuration / @MapperScan）', GOLD),
        ('BeanFactoryPostProcessor', 'PropertySourcesPlaceholderConfigurer（${} 占位符）', GOLD),
        ('BeanPostProcessor (before)', '@PostConstruct、@Resource', CYAN),
        ('BeanPostProcessor (after)', 'AOP 代理、@Async、@Transactional', GREEN),
        ('SmartInitializingSingleton', '所有单例初始化完成后回调', BLUE),
    ]
    y = 150
    for code, use, c in rows:
        box(ax, 90, y, 920, 96, fc=CARD, ec=c, lw=1.6)
        ax.text(120, y + 34, code, ha='left', va='center', color=c, fontproperties=FM, fontsize=13)
        ax.text(120, y + 70, use, ha='left', va='center', color=WHITE, fontproperties=F, fontsize=13)
        y += 110
    save(fig, path)


if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    cover('output/src9-fengmian.png')
    duibi('output/src9-duibi.png')
    shunxu('output/src9-shunxu.png')
    shengming('output/src9-shengming.png')
    yongtu('output/src9-yongtu.png')
