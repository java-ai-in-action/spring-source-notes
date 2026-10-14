#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""篇7 信息图：封面 / doDispatch七步 / handler匹配 / 参数解析链 / 视图渲染"""
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
    # 右侧：请求 -> DispatcherServlet -> 组件
    box(ax, 830, 120, 370, 70, fc='#0E2444', ec=BLUE, lw=1.8)
    ax.text(1015, 155, 'HTTP 请求  /user/1', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    arrow(ax, 1015, 194, 1015, 232)
    box(ax, 830, 232, 370, 78, fc='#2B2A12', ec=GOLD, lw=2.0)
    ax.text(1015, 271, 'DispatcherServlet', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=16)
    arrow(ax, 1015, 314, 1015, 352)
    comps = [('HandlerMapping', CYAN), ('HandlerAdapter', GREEN), ('ViewResolver', BLUE)]
    yy = 352
    for name, c in comps:
        box(ax, 830, yy, 370, 54, fc='#0E2444', ec=c, lw=1.4)
        ax.text(1015, yy + 27, name, ha='center', va='center', color=c, fontproperties=FM, fontsize=13)
        yy += 66
    ax.text(1015, 588, '九大组件协作，一步都不能少', ha='center', va='center', color=GREY, fontproperties=F, fontsize=15)
    for px, py, s, c in [(620, 120, 10, CYAN), (700, 648, 8, GOLD), (640, 452, 9, BLUE)]:
        ax.plot(px, py, marker='s', markersize=s, color=c, alpha=0.75)
    ax.plot([90, 210], [196, 196], color=CYAN, lw=3)
    ax.text(90, 240, 'SPRING 全家桶源码拆解', color=CYAN, fontproperties=FB, fontsize=17, va='center')
    ax.text(90, 318, '《Spring 源码现形记》', color=WHITE, fontproperties=FB, fontsize=44, va='center')
    ax.text(90, 400, '第 7 篇 ｜ Spring MVC 全链路', color=GOLD, fontproperties=FB, fontsize=24, va='center')
    ax.text(90, 466, '一个请求，doDispatch 走了几步', color=GREY, fontproperties=F, fontsize=19, va='center')
    ax.plot([90, 700], [536, 536], color='#24456E', lw=1.2)
    ax.text(90, 580, '公众号：Java程序员面试宝典', color=GREY, fontproperties=F, fontsize=16, va='center')
    ax.text(90, 620, '源码基于 Spring Framework 6.2.x 官方仓库逐行核对', color='#5C7FA8', fontproperties=F, fontsize=13, va='center')
    save(fig, path)


def dodispatch(path):
    W, H = 1100, 1080
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 60, 'doDispatch 七步全景', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=28)
    ax.text(W / 2, 100, 'DispatcherServlet 的核心方法，Spring MVC 流程 = 这七步', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    steps = [
        ('1', 'checkMultipart(request)', '文件上传包装', BLUE),
        ('2', 'getHandler(request)', 'URL -> HandlerMethod + 拦截器', CYAN),
        ('3', 'getHandlerAdapter(handler)', '找能调它的适配器', CYAN),
        ('4', 'mappedHandler.applyPreHandle()', '拦截器 preHandle（返回 false 就结束）', GOLD),
        ('5', 'ha.handle(...)', '真正执行 @Controller 方法', GREEN),
        ('6', 'applyPostHandle(...)', '拦截器 postHandle', GOLD),
        ('7', 'processDispatchResult(...)', '异常处理 + 视图渲染', BLUE),
    ]
    y = 140
    for num, code, desc, c in steps:
        box(ax, 90, y, 920, 108, fc=CARD, ec=c, lw=1.6 if num in ('2', '5', '7') else 1.2)
        ax.add_patch(Circle((150, y + 54), 27, facecolor='#0E2444', edgecolor=c, lw=1.6))
        ax.text(150, y + 54, num, ha='center', va='center', color=c, fontproperties=FMB, fontsize=18)
        ax.text(205, y + 40, code, ha='left', va='center', color=WHITE, fontproperties=FM, fontsize=15)
        ax.text(205, y + 76, desc, ha='left', va='center', color=GREY, fontproperties=F, fontsize=14)
        if num != '7':
            arrow(ax, 150, y + 112, 150, y + 128, color='#3A5A80', lw=1.6)
        y += 128
    save(fig, path)


def handler(path):
    W, H = 1100, 900
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, 'URL 是怎么匹配到你的方法的', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 102, 'getHandler 遍历所有 HandlerMapping，谁先返回就归谁', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 380, 140, 340, 62, ec=BLUE, lw=1.8)
    ax.text(550, 171, 'getHandler(request)', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=16)
    arrow(ax, 550, 204, 550, 240)
    box(ax, 200, 240, 700, 200, fc='#0B1C33', ec=CYAN, lw=1.5)
    ax.text(550, 275, 'for (HandlerMapping mapping : handlerMappings)', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=14)
    box(ax, 250, 300, 600, 54, ec=EDGE, lw=1.3)
    ax.text(550, 327, 'mapping.getHandler(request)', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=14)
    box(ax, 250, 364, 600, 54, fc='#2B2A12', ec=GOLD, lw=1.5)
    ax.text(550, 391, 'getHandlerInternal  ->  匹配 URL', ha='center', va='center', color=GOLD, fontproperties=F, fontsize=14)
    arrow(ax, 550, 444, 550, 486)
    box(ax, 250, 486, 600, 74, fc='#0E2444', ec=GREEN, lw=1.7)
    ax.text(550, 511, 'HandlerMethod', ha='center', va='center', color=GREEN, fontproperties=FM, fontsize=16)
    ax.text(550, 540, '哪个 Bean 的哪个方法', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    ax.text(300, 575, '+', ha='center', va='center', color=WHITE, fontproperties=FMB, fontsize=20)
    box(ax, 250, 588, 600, 74, fc='#0E2444', ec=GOLD, lw=1.5)
    ax.text(550, 613, 'HandlerExecutionChain', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=15)
    ax.text(550, 642, 'handler + 拦截器列表', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    ax.text(W / 2, 720, '返回的不是"一个方法"，而是 handler + 拦截器', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    ax.text(W / 2, 762, '拦截器就是这样被带进后续流程的', ha='center', va='center', color=GREY, fontproperties=F, fontsize=14)
    save(fig, path)


def resolver(path):
    W, H = 1100, 940
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, '参数是怎么"变"出来的', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 102, 'HandlerMethodArgumentResolverComposite 逐个问：谁能处理这个参数？', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=14)
    box(ax, 360, 140, 380, 62, ec=BLUE, lw=1.8)
    ax.text(550, 171, 'invokeForRequest()', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=16)
    arrow(ax, 550, 204, 550, 240)
    box(ax, 360, 240, 380, 56, fc='#2B2A12', ec=GOLD, lw=1.5)
    ax.text(550, 268, 'getMethodArgumentValues()', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=14)
    arrow(ax, 550, 298, 550, 334)
    box(ax, 150, 334, 800, 300, fc='#0B1C33', ec=CYAN, lw=1.5)
    ax.text(550, 366, 'resolvers.resolveArgument(parameter, ...)', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    rows = [('@PathVariable', 'PathVariableMethodArgumentResolver', BLUE),
            ('@RequestParam', 'RequestParamMethodArgumentResolver', CYAN),
            ('@RequestBody', 'RequestResponseBodyMethodProcessor', GREEN),
            ('HttpServletRequest', 'ServletRequestMethodArgumentResolver', GOLD)]
    y = 396
    for ann, cls, c in rows:
        box(ax, 190, y, 720, 50, fc=CARD2, ec=c, lw=1.2)
        ax.text(220, y + 25, ann, ha='left', va='center', color=c, fontproperties=FM, fontsize=13)
        ax.text(880, y + 25, '->  ' + cls, ha='right', va='center', color=WHITE, fontproperties=FM, fontsize=11)
        y += 60
    arrow(ax, 550, 644, 550, 686)
    box(ax, 300, 686, 500, 74, fc='#0E2444', ec=GREEN, lw=1.8)
    ax.text(550, 712, 'doInvoke(args)', ha='center', va='center', color=GREEN, fontproperties=FM, fontsize=16)
    ax.text(550, 741, 'method.invoke(getBean(), args)', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=13)
    ax.text(W / 2, 812, '参数解析成数组 -> 反射塞进你的方法', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    save(fig, path)


def view(path):
    W, H = 1100, 820
    fig, ax = new_fig(W, H)
    ax.text(W / 2, 62, '返回值是怎么渲染出去的', ha='center', va='center', color=WHITE, fontproperties=FB, fontsize=27)
    ax.text(W / 2, 102, 'render()：视图名 -> View -> 写入响应', ha='center', va='center', color=CYAN, fontproperties=F, fontsize=15)
    box(ax, 380, 140, 340, 60, ec=GOLD, lw=1.8)
    ax.text(550, 170, 'processDispatchResult()', ha='center', va='center', color=GOLD, fontproperties=FM, fontsize=15)
    arrow(ax, 550, 202, 550, 240)
    box(ax, 200, 240, 700, 90, fc='#1A1016', ec='#5A2530', lw=1.4)
    ax.text(550, 268, '有异常？先交给 HandlerExceptionResolver', ha='center', va='center', color=RED, fontproperties=F, fontsize=15)
    ax.text(550, 302, '@ControllerAdvice / @ExceptionHandler 兜底', ha='center', va='center', color=GREY, fontproperties=F, fontsize=13)
    arrow(ax, 550, 334, 550, 372)
    box(ax, 380, 372, 340, 60, ec=BLUE, lw=1.8)
    ax.text(550, 402, 'render(mv, request, response)', ha='center', va='center', color=WHITE, fontproperties=FM, fontsize=14)
    arrow(ax, 550, 434, 550, 472)
    box(ax, 250, 472, 600, 70, fc=CARD2, ec=CYAN, lw=1.5)
    ax.text(550, 500, 'resolveViewName  ->  ViewResolver', ha='center', va='center', color=CYAN, fontproperties=FM, fontsize=13)
    ax.text(550, 526, '遍历所有视图解析器', ha='center', va='center', color=GREY, fontproperties=F, fontsize=12)
    arrow(ax, 550, 544, 550, 582)
    box(ax, 280, 582, 540, 70, fc='#0E2444', ec=GREEN, lw=1.8)
    ax.text(550, 617, 'view.render(model, request, response)', ha='center', va='center', color=GREEN, fontproperties=FM, fontsize=13)
    ax.text(W / 2, 712, '视图名 -> View 对象 -> 把 Model 写进 HTTP 响应', ha='center', va='center', color=WHITE, fontproperties=F, fontsize=15)
    save(fig, path)


if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    cover('output/src7-fengmian.png')
    dodispatch('output/src7-dodispatch.png')
    handler('output/src7-handler.png')
    resolver('output/src7-resolver.png')
    view('output/src7-view.png')
