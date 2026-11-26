#!/usr/bin/env python3
"""Compose the winners-style final image, Wednesday 25 November 2026.

Modelled on the 24 November winners (#1 sage-finch-75, #2 buavita-x):
black top bar, giant serif date masthead, red italic tagline, a strip
of six giant red statistics, navy UTC timeline bar, fine-grained
region bar, three lead cards (number badge and credibility pill on the
picture, red fact banner across its foot, place line, serif headline,
body, source line), a ten-card grid in the same style, a pinned world
map with a HOW SURE legend, a numbered ALSO list, and a red DATE
CHECK box over a sources line.

Data: winners_data.py (LOCK_PACK-verified stories 1-40).
Run:  python3 compose_winners.py  ->  writes entry.png beside this file.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

import winners_data as D

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
W = H = 1024
M = 14
BG = (247, 242, 228)
INK = (16, 16, 16)
RED = (186, 28, 24)
DARKRED = (150, 24, 20)
GREY = (95, 95, 95)
NAVY = (10, 22, 52)
CERT_FILL = {
    "OFFICIAL": (24, 128, 58),
    "CONFIRMED": (24, 128, 58),
    "REPORTED": (28, 38, 64),
    "CLAIM": (196, 30, 24),
}

LIB = Path("/usr/share/fonts/truetype/liberation")
SERIF_B = str(LIB / "LiberationSerif-Bold.ttf")
SERIF_I = str(LIB / "LiberationSerif-Italic.ttf")
SANS_B = str(LIB / "LiberationSans-Bold.ttf")
SANS = str(LIB / "LiberationSans-Regular.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_width, min_size=8):
    size = start
    while size > min_size:
        font = f(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return f(path, min_size)


def wrap(draw, text, font, max_width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_width, line_h, max_lines, fill=INK):
    lines = wrap(draw, text, font, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "...", font=font) > max_width:
            last = last[:-1]
        lines[-1] = last + "..."
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += line_h
    return y


def cert_pill(draw, right_x, y, cert):
    font = f(SANS_B, 8)
    w_ = draw.textlength(cert, font=font) + 12
    draw.rounded_rectangle([right_x - w_, y, right_x, y + 15], radius=7,
                           fill=CERT_FILL[cert])
    draw.text((right_x - w_ + 6, y + 3), cert, font=font, fill=(255, 255, 255))


def num_badge(draw, cx, cy, num, r=13):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    font = f(SANS_B, 13 if num < 10 else 11.5)
    t = str(num)
    tw = draw.textlength(t, font=font)
    draw.text((cx - tw / 2, cy - 7.5), t, font=font, fill=(255, 255, 255))


def mini_chart(draw, kind, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(14, 20, 44))
    if kind == "gdp":
        vals = [0.4, 0.1, -0.2, 0.0, 0.1]
        base = y0 + (y1 - y0) * 0.55
        draw.line([x0 + 6, base, x1 - 6, base], fill=(190, 190, 190), width=1)
        bw = (x1 - x0 - 18) / len(vals)
        for i, v in enumerate(vals):
            bx = x0 + 9 + i * bw + bw * 0.22
            hh = abs(v) * 34
            if v >= 0:
                draw.rectangle([bx, base - hh, bx + bw * 0.56, base],
                               fill=(96, 175, 96))
            else:
                draw.rectangle([bx, base, bx + bw * 0.56, base + hh],
                               fill=(205, 80, 70))
    elif kind == "cpi":
        for i, (lab, v) in enumerate([("SEP", 4.3), ("OCT", 4.9)]):
            by = y0 + 3 + i * 15
            draw.text((x0 + 7, by), lab, font=f(SANS_B, 8), fill=(220, 220, 220))
            draw.rectangle([x0 + 34, by, x0 + 34 + int(v * 15), by + 10],
                           fill=(232, 160, 60) if i else (145, 145, 155))
            draw.text((x0 + 37 + int(v * 15), by), str(v), font=f(SANS_B, 8),
                      fill=(255, 255, 255))
    elif kind in ("stoxx", "sensex"):
        if kind == "stoxx":
            pts = [(0.06, 0.25), (0.3, 0.35), (0.5, 0.32), (0.72, 0.55),
                   (0.97, 0.75)]
            col = (230, 90, 80)
            lab = "626.03"
        else:
            pts = [(0.06, 0.78), (0.3, 0.6), (0.52, 0.52), (0.74, 0.33),
                   (0.97, 0.18)]
            col = (96, 220, 120)
            lab = "83,938"
        xy = [(x0 + p[0] * (x1 - x0 - 52), y0 + 3 + p[1] * (y1 - y0 - 6))
              for p in pts]
        draw.line(xy, fill=col, width=2)
        for px, py in xy:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
        draw.text((x1 - 50, y0 + (y1 - y0) / 2 - 6), lab, font=f(SANS_B, 10),
                  fill=(255, 255, 255))



def _bands(draw, box, top, bottom, steps=24):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t0 = i / steps
        col = tuple(int(top[k] + (bottom[k] - top[k]) * t0) for k in range(3))
        ya = y0 + (y1 - y0) * i // steps
        yb = y0 + (y1 - y0) * (i + 1) // steps + 1
        draw.rectangle([x0, ya, x1, yb], fill=col)


def _stars(draw, box, n, seed=7):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i in range(n):
        sx = x0 + ((i * 67 + seed * 31) % max(w - 6, 1))
        sy = y0 + ((i * 41 + seed * 17) % max(int(h * 0.62), 1))
        r = 2.6 if i % 5 == 0 else 1.6
        draw.ellipse([sx, sy, sx + r, sy + r], fill=(235, 238, 248))
        if i % 5 == 0:
            draw.line([sx - 3, sy + r / 2, sx + r + 3, sy + r / 2],
                      fill=(200, 205, 225), width=1)
            draw.line([sx + r / 2, sy - 3, sx + r / 2, sy + r + 3],
                      fill=(200, 205, 225), width=1)


def drawn_scene(draw, name, box):
    """Flat code-drawn pictures, richer pass: gradients, shading, detail."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if name == "rocket.webp":
        _bands(draw, box, (16, 24, 58), (44, 58, 104))
        _stars(draw, box, 26)
        draw.ellipse([x1 - w * 0.17, y0 + h * 0.07, x1 - w * 0.085,
                      y0 + h * 0.24], fill=(226, 228, 220))
        draw.ellipse([x1 - w * 0.155, y0 + h * 0.09, x1 - w * 0.13,
                      y0 + h * 0.14], fill=(198, 200, 192))
        draw.rectangle([x0, y1 - h * 0.15, x1, y1], fill=(46, 40, 34))
        draw.rectangle([x0, y1 - h * 0.15, x1, y1 - h * 0.135],
                       fill=(70, 62, 52))
        bx = cx - w * 0.05
        bw_ = w * 0.10
        draw.polygon([(bx, y0 + h * 0.30), (cx, y0 + h * 0.06),
                      (bx + bw_, y0 + h * 0.30)], fill=(240, 240, 242))
        draw.polygon([(bx, y0 + h * 0.30), (cx, y0 + h * 0.06),
                      (bx + bw_ * 0.45, y0 + h * 0.30)], fill=(208, 210, 216))
        draw.rectangle([bx, y0 + h * 0.30, bx + bw_, y0 + h * 0.78],
                       fill=(232, 232, 236))
        draw.rectangle([bx, y0 + h * 0.30, bx + bw_ * 0.45, y0 + h * 0.78],
                       fill=(203, 205, 212))
        draw.ellipse([cx - w * 0.018, y0 + h * 0.36, cx + w * 0.018,
                      y0 + h * 0.47], fill=(40, 70, 120),
                     outline=(150, 190, 230), width=2)
        draw.rectangle([bx, y0 + h * 0.55, bx + bw_, y0 + h * 0.60],
                       fill=(198, 52, 44))
        draw.polygon([(bx - w * 0.045, y0 + h * 0.78), (bx, y0 + h * 0.52),
                      (bx, y0 + h * 0.78)], fill=(198, 52, 44))
        draw.polygon([(bx + bw_, y0 + h * 0.52), (bx + bw_ + w * 0.045,
                       y0 + h * 0.78), (bx + bw_, y0 + h * 0.78)],
                     fill=(178, 44, 38))
        draw.polygon([(bx + bw_ * 0.18, y0 + h * 0.78), (cx, y1 - h * 0.06),
                      (bx + bw_ * 0.82, y0 + h * 0.78)], fill=(245, 166, 55))
        draw.polygon([(bx + bw_ * 0.34, y0 + h * 0.78), (cx, y1 - h * 0.13),
                      (bx + bw_ * 0.66, y0 + h * 0.78)], fill=(252, 214, 120))
        tx = cx + w * 0.17
        draw.line([tx, y0 + h * 0.08, tx, y1 - h * 0.15],
                  fill=(158, 163, 178), width=3)
        for f_ in range(6):
            yy = y0 + h * (0.12 + f_ * 0.12)
            draw.line([tx, yy, tx + w * 0.11, yy - h * 0.05],
                      fill=(158, 163, 178), width=2)
            draw.line([tx, yy, bx + bw_, yy + h * 0.10],
                      fill=(120, 125, 140), width=1)
        for ex, ew in [(-0.34, 0.16), (-0.20, 0.20), (0.16, 0.20),
                       (0.32, 0.15)]:
            exx = cx + w * ex
            draw.ellipse([exx - w * ew / 2, y1 - h * 0.26, exx + w * ew / 2,
                          y1 - h * 0.13], fill=(216, 216, 222))
            draw.ellipse([exx - w * ew / 3, y1 - h * 0.29, exx + w * ew / 3,
                          y1 - h * 0.17], fill=(228, 228, 233))
    elif name == "chips.webp":
        _bands(draw, box, (10, 16, 30), (22, 34, 56))
        for gx in range(6):
            xx = x0 + w * (0.06 + gx * 0.18)
            draw.line([xx, y0 + h * 0.10, xx, y0 + h * 0.30],
                      fill=(44, 74, 104), width=1)
            draw.line([xx, y0 + h * 0.30, xx + w * 0.07, y0 + h * 0.30],
                      fill=(44, 74, 104), width=1)
            draw.ellipse([xx + w * 0.07 - 2, y0 + h * 0.30 - 2,
                          xx + w * 0.07 + 2, y0 + h * 0.30 + 2],
                         fill=(90, 160, 200))
        s = min(w, h) * 0.54
        draw.rectangle([cx - s / 2 + 3, cy - s / 2 + 4, cx + s / 2 + 3,
                        cy + s / 2 + 4], fill=(6, 9, 16))
        draw.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                       fill=(42, 58, 86), outline=(120, 200, 245), width=2)
        s2 = s * 0.55
        draw.rectangle([cx - s2 / 2, cy - s2 / 2, cx + s2 / 2, cy + s2 / 2],
                       fill=(26, 38, 60), outline=(120, 200, 245), width=1)
        for i in range(3):
            yy = cy - s2 * 0.22 + i * s2 * 0.22
            draw.line([cx - s2 * 0.3, yy, cx + s2 * 0.3, yy],
                      fill=(80, 130, 170), width=1)
        draw.ellipse([cx - s / 2 + 5, cy - s / 2 + 5, cx - s / 2 + 11,
                      cy - s / 2 + 11], outline=(200, 220, 240), width=1)
        for i in range(6):
            off = -s / 2 + (i + 0.5) * s / 6
            for sx0, sx1 in [(cx - s / 2 - w * 0.075, cx - s / 2),
                             (cx + s / 2, cx + s / 2 + w * 0.075)]:
                draw.line([sx0, cy + off, sx1, cy + off],
                          fill=(120, 200, 245), width=2)
            for sy0, sy1 in [(cy - s / 2 - h * 0.075, cy - s / 2),
                             (cy + s / 2, cy + s / 2 + h * 0.075)]:
                draw.line([cx + off, sy0, cx + off, sy1],
                          fill=(120, 200, 245), width=2)
        ax, ay = x1 - w * 0.315, y0 + h * 0.13
        draw.polygon([(ax, ay), (ax + w * 0.14, ay + h * 0.05),
                      (ax + w * 0.055, ay + h * 0.14), (ax + w * 0.175,
                      ay + h * 0.175), (ax + w * 0.02, ay + h * 0.33),
                      (ax - w * 0.025, ay + h * 0.155), (ax - w * 0.10,
                      ay + h * 0.185)], fill=(228, 62, 52))
        draw.polygon([(ax, ay), (ax + w * 0.14, ay + h * 0.05),
                      (ax + w * 0.055, ay + h * 0.14), (ax + w * 0.02,
                      ay + h * 0.33), (ax - w * 0.025, ay + h * 0.155)],
                     fill=(240, 92, 78))
    elif name == "gaza.webp":
        _bands(draw, box, (232, 150, 84), (120, 70, 66))
        draw.ellipse([x0 + w * 0.40, y0 + h * 0.30, x0 + w * 0.52,
                      y0 + h * 0.52], fill=(250, 214, 150))
        draw.rectangle([x0, y1 - h * 0.10, x1, y1], fill=(66, 48, 44))
        specs = [(0.02, 0.20, 0.44), (0.24, 0.15, 0.60), (0.41, 0.22, 0.38),
                 (0.65, 0.16, 0.52), (0.83, 0.15, 0.42)]
        for i, (fx, fw_, fh) in enumerate(specs):
            bx = x0 + w * fx
            by = y1 - h * fh
            tone = (58, 46, 44) if i % 2 == 0 else (48, 38, 38)
            draw.rectangle([bx, by, bx + w * fw_, y1], fill=tone)
            draw.rectangle([bx, by, bx + w * fw_, by + 3], fill=(84, 66, 60))
            rows = max(int(fh * 6), 2)
            for r_ in range(rows):
                for c_ in range(2):
                    if (r_ * 2 + c_ + i) % 3 == 0:
                        continue
                    wx = bx + w * fw_ * (0.16 + c_ * 0.44)
                    wy = by + h * fh * (0.12 + r_ * 0.8 / rows)
                    draw.rectangle([wx, wy, wx + w * fw_ * 0.22,
                                    wy + h * fh * 0.11],
                                   fill=(246, 208, 128))
        for px, ps in [(0.55, 0.16), (0.63, 0.22), (0.71, 0.13)]:
            px_ = x0 + w * px
            draw.ellipse([px_, y0 + h * 0.02, px_ + w * ps, y0 + h * 0.24],
                         fill=(96, 88, 92))
            draw.ellipse([px_ + w * ps * 0.2, y0 - h * 0.02,
                          px_ + w * ps * 1.05, y0 + h * 0.15],
                         fill=(110, 102, 106))
    elif name == "drone.webp":
        _bands(draw, box, (12, 20, 44), (30, 44, 78))
        _stars(draw, box, 20, seed=3)
        draw.ellipse([x0 + w * 0.05, y0 + h * 0.07, x0 + w * 0.115,
                      y0 + h * 0.20], fill=(224, 226, 218))
        r = min(w, h) * 0.115
        for dx, dy, col in [(-1, -1, (240, 80, 70)), (1, -1, (90, 220, 130)),
                            (-1, 1, (235, 238, 242)), (1, 1, (235, 238, 242))]:
            ex, ey = cx + dx * w * 0.15, cy + dy * h * 0.22
            draw.line([cx, cy, ex, ey], fill=(215, 219, 228), width=3)
            draw.ellipse([ex - r, ey - r * 0.38, ex + r, ey + r * 0.38],
                         outline=(228, 231, 238), width=2)
            draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=col)
        draw.rectangle([cx - w * 0.065, cy - h * 0.10, cx + w * 0.065,
                        cy + h * 0.10], fill=(232, 235, 240))
        draw.rectangle([cx - w * 0.065, cy - h * 0.10, cx + w * 0.065,
                        cy - h * 0.03], fill=(198, 203, 214))
        draw.ellipse([cx - w * 0.02, cy + h * 0.02, cx + w * 0.02,
                      cy + h * 0.10], fill=(30, 40, 60),
                     outline=(140, 190, 235), width=2)
        draw.line([cx - w * 0.03, cy + h * 0.10, cx - w * 0.05, y1 - h * 0.06],
                  fill=(180, 186, 198), width=2)
        draw.line([cx + w * 0.03, cy + h * 0.10, cx + w * 0.05, y1 - h * 0.06],
                  fill=(180, 186, 198), width=2)
        for i in range(3):
            rr = w * (0.10 + i * 0.055)
            draw.arc([cx - rr, y0 + h * 0.03 - rr * 0.4, cx + rr,
                      y0 + h * 0.03 + rr * 0.6], 20, 160,
                     fill=(120, 200, 245), width=2)
    elif name == "treaty.webp":
        _bands(draw, box, (38, 104, 156), (24, 74, 122))
        draw.ellipse([x0 + w * 0.05, y0 + h * 0.08, x0 + w * 0.17,
                      y0 + h * 0.32], fill=(248, 204, 92))
        for a in range(8):
            import math as _m
            ang = a * 3.14159 / 4
            sx, sy = x0 + w * 0.11, y0 + h * 0.20
            draw.line([sx + _m.cos(ang) * w * 0.075, sy + _m.sin(ang) * h * 0.14,
                       sx + _m.cos(ang) * w * 0.105,
                       sy + _m.sin(ang) * h * 0.20], fill=(248, 204, 92),
                      width=2)
        for i, base_col in enumerate([(150, 205, 235), (110, 180, 220),
                                      (80, 150, 205)]):
            yy = y0 + h * (0.60 + i * 0.13)
            draw.arc([x0 - w * 0.08 + i * w * 0.05, yy - h * 0.09,
                      x1 + w * 0.08, yy + h * 0.15], 180, 360,
                     fill=base_col, width=3)
        for fx, cols in [(0.40, None), (0.66, None)]:
            px = x0 + w * fx
            draw.line([px, y0 + h * 0.14, px, y0 + h * 0.62],
                      fill=(226, 228, 232), width=3)
            draw.ellipse([px - 3, y0 + h * 0.11, px + 3, y0 + h * 0.155],
                         fill=(248, 204, 92))
        draw.polygon([(x0 + w * 0.40, y0 + h * 0.15), (x0 + w * 0.615,
                       y0 + h * 0.185), (x0 + w * 0.615, y0 + h * 0.40),
                      (x0 + w * 0.40, y0 + h * 0.43)], fill=(24, 52, 130))
        draw.polygon([(x0 + w * 0.40, y0 + h * 0.15), (x0 + w * 0.51,
                       y0 + h * 0.29), (x0 + w * 0.40, y0 + h * 0.43)],
                     fill=(196, 40, 46))
        for i in range(4):
            sx = x0 + w * (0.53 + (i % 2) * 0.045)
            sy = y0 + h * (0.21 + (i // 2) * 0.09)
            draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(240, 240, 245))
        draw.polygon([(x0 + w * 0.66, y0 + h * 0.15), (x0 + w * 0.875,
                       y0 + h * 0.185), (x0 + w * 0.875, y0 + h * 0.40),
                      (x0 + w * 0.66, y0 + h * 0.43)], fill=(24, 110, 62))
        draw.polygon([(x0 + w * 0.66, y0 + h * 0.15), (x0 + w * 0.875,
                       y0 + h * 0.185), (x0 + w * 0.875, y0 + h * 0.275),
                      (x0 + w * 0.66, y0 + h * 0.29)], fill=(244, 200, 60))
        draw.polygon([(x0 + w * 0.735, y0 + h * 0.24), (x0 + w * 0.75,
                       y0 + h * 0.31), (x0 + w * 0.72, y0 + h * 0.31),
                      (x0 + w * 0.765, y0 + h * 0.36), (x0 + w * 0.70,
                       y0 + h * 0.30), (x0 + w * 0.73, y0 + h * 0.30)],
                     fill=(240, 240, 245))
    elif name == "mine.webp":
        draw.rectangle(box, fill=(22, 18, 14))
        draw.polygon([(x0 + w * 0.26, y1), (cx, y0 + h * 0.26),
                      (x0 + w * 0.74, y1)], fill=(52, 42, 32))
        draw.polygon([(x0 + w * 0.33, y1), (cx, y0 + h * 0.34),
                      (x0 + w * 0.67, y1)], fill=(66, 54, 40))
        for fx in (0.30, 0.70):
            bx = x0 + w * fx
            draw.rectangle([bx - 3, y0 + h * 0.30, bx + 3, y1],
                           fill=(96, 72, 46))
            draw.line([bx - 3, y0 + h * 0.52, bx + 3, y0 + h * 0.52],
                      fill=(70, 52, 34), width=2)
        draw.rectangle([x0 + w * 0.28, y0 + h * 0.28, x0 + w * 0.72,
                        y0 + h * 0.335], fill=(96, 72, 46))
        for gx in (-0.055, 0.055):
            draw.line([cx + w * gx, y0 + h * 0.86, cx + w * gx * 1.7, y1],
                      fill=(150, 150, 155), width=2)
        draw.rectangle([cx - w * 0.085, y0 + h * 0.66, cx + w * 0.085,
                        y0 + h * 0.86], fill=(40, 34, 28),
                       outline=(120, 100, 74), width=2)
        draw.rectangle([cx - w * 0.085, y0 + h * 0.66, cx + w * 0.085,
                        y0 + h * 0.72], fill=(120, 92, 54))
        for rr, alpha_col in [(0.16, (120, 100, 60)), (0.115, (190, 160, 88)),
                              (0.075, (250, 216, 122))]:
            draw.ellipse([cx - w * rr, y0 + h * 0.10, cx + w * rr,
                          y0 + h * 0.10 + w * rr * 2 * h / w],
                         fill=alpha_col)
        draw.ellipse([cx - w * 0.035, y0 + h * 0.155, cx + w * 0.035,
                      y0 + h * 0.26], fill=(255, 240, 190))
        draw.polygon([(cx - w * 0.028, y0 + h * 0.25), (cx - w * 0.15, y1),
                      (cx + w * 0.15, y1), (cx + w * 0.028, y0 + h * 0.25)],
                     fill=(250, 226, 152))
        draw.rectangle([x0, y1 - h * 0.07, x1, y1], fill=(12, 10, 8))
    elif name == "capitol.webp":
        _bands(draw, box, (22, 34, 70), (48, 66, 110))
        _stars(draw, box, 14, seed=5)
        base = y1 - h * 0.12
        draw.rectangle([x0, base, x1, y1], fill=(36, 48, 40))
        bw_ = w * 0.66
        draw.rectangle([cx - bw_ / 2, base - h * 0.06, cx + bw_ / 2, base],
                       fill=(196, 199, 206))
        draw.rectangle([cx - bw_ * 0.44, base - h * 0.12, cx + bw_ * 0.44,
                        base - h * 0.06], fill=(214, 217, 223))
        draw.rectangle([cx - bw_ / 2, base - h * 0.32, cx + bw_ / 2,
                        base - h * 0.12], fill=(230, 232, 237))
        for i in range(9):
            wx = cx - bw_ / 2 + bw_ * (0.055 + i * 0.105)
            draw.rectangle([wx, base - h * 0.29, wx + bw_ * 0.045,
                            base - h * 0.15], fill=(52, 72, 112))
            draw.rectangle([wx, base - h * 0.29, wx + bw_ * 0.045,
                            base - h * 0.26], fill=(250, 214, 130))
        draw.rectangle([cx - bw_ * 0.27, base - h * 0.36, cx + bw_ * 0.27,
                        base - h * 0.32], fill=(214, 217, 223))
        draw.pieslice([cx - bw_ * 0.25, base - h * 0.86, cx + bw_ * 0.25,
                       base - h * 0.10], 180, 360, fill=(233, 235, 240))
        draw.pieslice([cx - bw_ * 0.25, base - h * 0.86, cx + bw_ * 0.05,
                       base - h * 0.10], 180, 270, fill=(206, 209, 216))
        for i in range(5):
            ax = cx - bw_ * 0.16 + i * bw_ * 0.08
            draw.arc([ax, base - h * 0.72, ax + bw_ * 0.07, base - h * 0.40],
                     180, 360, fill=(170, 174, 184), width=1)
        draw.rectangle([cx - bw_ * 0.20, base - h * 0.44, cx + bw_ * 0.20,
                        base - h * 0.40], fill=(206, 209, 216))
        draw.rectangle([cx - 2, base - h * 0.94, cx + 2, base - h * 0.70],
                       fill=(230, 232, 237))
        draw.polygon([(cx + 2, base - h * 0.94), (cx + w * 0.055,
                       base - h * 0.915), (cx + 2, base - h * 0.89)],
                     fill=(198, 52, 44))
    elif name == "storm.webp":
        _bands(draw, box, (40, 52, 72), (70, 84, 104))
        for ex, ey, ew, tone in [(0.08, 0.10, 0.36, (150, 160, 178)),
                                 (0.44, 0.05, 0.44, (140, 150, 170)),
                                 (0.24, 0.20, 0.48, (168, 178, 196)),
                                 (0.60, 0.22, 0.34, (156, 166, 186))]:
            draw.ellipse([x0 + w * ex, y0 + h * ey, x0 + w * (ex + ew),
                          y0 + h * (ey + 0.30)], fill=tone)
            draw.ellipse([x0 + w * (ex + ew * 0.2), y0 + h * (ey + 0.16),
                          x0 + w * (ex + ew * 0.8), y0 + h * (ey + 0.34)],
                         fill=tuple(max(v - 18, 0) for v in tone))
        draw.polygon([(cx + w * 0.05, y0 + h * 0.34), (cx - w * 0.03,
                       y0 + h * 0.58), (cx + w * 0.015, y0 + h * 0.58),
                      (cx - w * 0.05, y0 + h * 0.82), (cx + w * 0.06,
                       y0 + h * 0.53), (cx + w * 0.015, y0 + h * 0.53)],
                     fill=(250, 205, 70))
        for i in range(11):
            rx = x0 + w * (0.05 + i * 0.09)
            draw.line([rx, y0 + h * 0.52, rx - w * 0.028, y0 + h * 0.74],
                      fill=(140, 190, 235), width=2)
        draw.arc([x0 - w * 0.05, y0 + h * 0.62, x1 + w * 0.05, y1 + h * 0.22],
                 180, 360, fill=(96, 158, 205), width=3)
        draw.arc([x0 + w * 0.1, y0 + h * 0.72, x1 - w * 0.05, y1 + h * 0.3],
                 180, 360, fill=(210, 230, 245), width=2)
    elif name == "cricket.webp":
        _bands(draw, box, (30, 96, 46), (44, 128, 62))
        draw.ellipse([cx - w * 0.46, cy - h * 0.46, cx + w * 0.46,
                      cy + h * 0.46], outline=(120, 190, 130), width=2)
        draw.rectangle([cx - w * 0.055, y0 + h * 0.10, cx + w * 0.055, y1],
                       fill=(208, 190, 142))
        draw.rectangle([cx - w * 0.055, y0 + h * 0.10, cx + w * 0.055, y1],
                       outline=(170, 152, 108), width=1)
        for yy in (0.16, 0.30, 0.70, 0.84):
            draw.line([cx - w * 0.055, y0 + h * yy, cx + w * 0.055,
                       y0 + h * yy], fill=(170, 152, 108), width=1)
        for yy in (0.17, 0.80):
            for sx in (-0.032, 0.0, 0.032):
                draw.line([cx + w * sx, y0 + h * yy, cx + w * sx,
                           y0 + h * (yy + 0.11)], fill=(243, 243, 240),
                          width=2)
            draw.line([cx - w * 0.045, y0 + h * yy, cx + w * 0.045,
                       y0 + h * yy], fill=(243, 243, 240), width=2)
        draw.polygon([(cx + w * 0.17, y0 + h * 0.50), (cx + w * 0.225,
                       y0 + h * 0.525), (cx + w * 0.115, y0 + h * 0.88),
                      (cx + w * 0.06, y0 + h * 0.855)], fill=(158, 112, 64))
        draw.polygon([(cx + w * 0.17, y0 + h * 0.50), (cx + w * 0.19,
                       y0 + h * 0.51), (cx + w * 0.085, y0 + h * 0.865),
                      (cx + w * 0.06, y0 + h * 0.855)], fill=(178, 130, 78))
        draw.arc([cx - w * 0.24, y0 + h * 0.44, cx - w * 0.02, y0 + h * 0.72],
                 300, 60, fill=(240, 240, 235), width=2)
        draw.ellipse([cx - w * 0.225, y0 + h * 0.545, cx - w * 0.165,
                      y0 + h * 0.625], fill=(204, 42, 42))
        draw.arc([cx - w * 0.225, y0 + h * 0.545, cx - w * 0.165,
                  y0 + h * 0.625], 100, 260, fill=(240, 200, 200), width=1)
    else:
        draw.rectangle(box, fill=(60, 60, 66))


def card_visual(img, draw, story, box, big=None):
    x0, y0, x1, y1 = box
    kind, arg = story["kind"]
    if kind == "img":
        drawn_scene(draw, arg, box)
    else:
        mini_chart(draw, arg, box)
    num_badge(draw, x0 + 17, y0 + 17, story["num"])
    cert_pill(draw, x1 - 5, y0 + 5, story["cert"])
    if big:  # rank-1 style: the hard number lives inside the picture
        bf = fit_font(draw, big, SANS_B, 17, (x1 - x0) - 14, min_size=10)
        draw.text((x0 + 7, y1 - 24), big, font=bf, fill=(255, 255, 255),
                  stroke_width=2, stroke_fill=(20, 20, 20))


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # black top bar
    draw.rectangle([0, 0, W, 20], fill=(8, 8, 8))
    draw.text((M, 4), D.TOP_LEFT, font=f(SANS_B, 10.5), fill=(255, 255, 255))
    tw = draw.textlength(D.TOP_RIGHT, font=f(SANS_B, 10.5))
    draw.text((W - M - tw, 4), D.TOP_RIGHT, font=f(SANS_B, 10.5),
              fill=(255, 255, 255))

    # masthead
    mf = fit_font(draw, D.MASTHEAD, SERIF_B, 62, W - 2 * M)
    tw = draw.textlength(D.MASTHEAD, font=mf)
    draw.text(((W - tw) / 2, 24), D.MASTHEAD, font=mf, fill=INK)
    sf = fit_font(draw, D.TAGLINE, SERIF_I, 14.5, W - 2 * M)
    tw = draw.textlength(D.TAGLINE, font=sf)
    draw.text(((W - tw) / 2, 90), D.TAGLINE, font=sf, fill=DARKRED)

    # giant stat strip
    y = 114
    col_w = (W - 2 * M) / 6
    draw.line([M, y - 4, W - M, y - 4], fill=(30, 30, 30), width=1)
    for i, (num, cap) in enumerate(D.STATS):
        x = M + i * col_w
        nf = fit_font(draw, num, SANS_B, 27, col_w - 52)
        nw = draw.textlength(num, font=nf)
        draw.text((x + 2, y + 8), num, font=nf, fill=RED)
        draw_wrapped(draw, cap, f(SANS, 8), x + 6 + nw, y + 6, col_w - nw - 12,
                     10, 4, fill=(35, 35, 35))
        if i:
            draw.line([x - 5, y + 2, x - 5, y + 48], fill=(190, 180, 160), width=1)
    draw.line([M, y + 58, W - M, y + 58], fill=(30, 30, 30), width=1)

    # UTC timeline bar
    y = 178
    draw.rectangle([M, y, W - M, y + 17], fill=NAVY)
    tf = fit_font(draw, D.UTC_BAR, SANS_B, 9.5, W - 2 * M - 12)
    draw.text((M + 6, y + 3.5), D.UTC_BAR, font=tf, fill=(255, 255, 255))

    # region bar (parallelograms, fine-grained regions)
    y = 199
    seg_w = (W - 2 * M) / len(D.REGIONS)
    for i, (label, colour) in enumerate(D.REGIONS):
        x = M + i * seg_w
        rgb = tuple(int(colour[j:j + 2], 16) for j in (1, 3, 5))
        draw.rectangle([x + 1, y, x + seg_w - 2, y + 15], fill=rgb)
        lf = fit_font(draw, label, SANS_B, 9, seg_w - 14, min_size=7)
        tw = draw.textlength(label, font=lf)
        draw.text((x + (seg_w - tw) / 2, y + 3), label, font=lf,
                  fill=(255, 255, 255))

    # lead cards
    y = 222
    card_w = (W - 2 * M - 16) / 3
    pic_h = 110
    for i, s in enumerate(D.LEADS):
        x = M + i * (card_w + 8)
        card_visual(img, draw, s, (int(x), y, int(x + card_w), y + pic_h))
        ty = y + pic_h + 5
        draw.text((x, ty), s["place"], font=f(SANS_B, 9.5), fill=RED)
        hy = draw_wrapped(draw, s["headline"], f(SERIF_B, 19), int(x), ty + 14,
                          card_w, 22, 3)
        draw_wrapped(draw, s["body"], f(SANS, 9.5), int(x), hy + 2, card_w, 12.5,
                     3, fill=(45, 45, 45))
        draw.text((x, y + 240), s["src"], font=f(SANS, 7.5), fill=GREY)
    lead_bottom = y + 250
    draw.line([M, lead_bottom, W - M, lead_bottom], fill=(30, 30, 30), width=1)

    # grid header + cards 4-13
    gy = lead_bottom + 6
    draw.text((M, gy), "THE DAY IN TEN MORE", font=f(SANS_B, 12), fill=RED)
    tw = draw.textlength("Wednesday's other big stories, across nine regions",
                         font=f(SANS, 9))
    draw.text((W - M - tw, gy + 2), "Wednesday's other big stories, across "
              "nine regions", font=f(SANS, 9), fill=GREY)
    gy += 18
    cell_w = (W - 2 * M - 32) / 5
    strip_h = 50
    row_h = 126
    for idx, s in enumerate(D.GRID):
        r, c = divmod(idx, 5)
        x = M + c * (cell_w + 8)
        y0 = gy + r * row_h
        _big = {4: "88 / 112", 7: "9 DEAD", 9: "259", 10: "4,200+"}.get(s["num"])
        card_visual(img, draw, s, (int(x), y0, int(x + cell_w), y0 + strip_h),
                    big=_big)
        ty = y0 + strip_h + 4
        draw.text((x, ty), s["place"], font=f(SANS_B, 7.5), fill=RED)
        hy = draw_wrapped(draw, s["headline"], f(SERIF_B, 12.5), int(x), ty + 11,
                          cell_w, 15, 2)
        draw_wrapped(draw, s["body"], f(SANS, 8), int(x), hy + 1, cell_w, 10.5,
                     2, fill=(45, 45, 45))
        draw.text((x, y0 + row_h - 11), s["src"], font=f(SANS, 7), fill=GREY)
    grid_bottom = gy + 2 * row_h
    draw.line([M, grid_bottom, W - M, grid_bottom], fill=(30, 30, 30), width=1)

    # bottom: map + ALSO
    y = grid_bottom + 6
    draw.text((M, y), "WHERE IT HAPPENED", font=f(SANS_B, 11), fill=RED)
    draw.text((M + 316, y), "ALSO ON WEDNESDAY 25 NOVEMBER 2026 - STORIES 14-40",
              font=f(SANS_B, 11), fill=RED)
    map_box = (M, y + 17, M + 296, y + 150)
    mx0, my0, mx1, my1 = map_box
    # real coastline world map (country polygons, equirectangular)
    import json as _json
    draw.rectangle(map_box, fill=(226, 233, 238))
    _world = _json.loads((HERE / "world_countries.geojson").read_text())

    def _proj(pt):
        lon, lat = pt
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my0 + (90 - lat) / 180 * (my1 - my0))

    def _ring(coords):
        pts = [_proj(p) for p in coords]
        if len(pts) >= 3:
            draw.polygon(pts, fill=(216, 198, 152), outline=(150, 132, 92))

    for _feat in _world["features"]:
        _g = _feat["geometry"]
        if _g["type"] == "Polygon":
            for _r in _g["coordinates"]:
                _ring(_r)
        elif _g["type"] == "MultiPolygon":
            for _poly in _g["coordinates"]:
                for _r in _poly:
                    _ring(_r)
    offsets = {10: (13, -11), 12: (-15, 11)}
    for num, (lon, lat) in D.PINS_LONLAT.items():
        tx = mx0 + (lon + 180) / 360 * (mx1 - mx0)
        ty2 = my0 + (90 - lat) / 180 * (my1 - my0)
        cx, cy = tx, ty2
        if num in offsets:
            dx, dy = offsets[num]
            draw.line([tx, ty2, tx + dx, ty2 + dy], fill=RED, width=1)
            cx, cy = tx + dx, ty2 + dy
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
        t = str(num)
        tf2 = f(SANS_B, 8.5)
        tw = draw.textlength(t, font=tf2)
        draw.text((cx - tw / 2, cy - 4.5), t, font=tf2, fill=(255, 255, 255))
    # HOW SURE legend: two compact rows under the map
    ly = y + 154
    draw.text((M, ly), "HOW SURE", font=f(SANS_B, 9), fill=INK)
    rows_hs = [[("OFFICIAL", "= on the record"), ("REPORTED", "= wires")],
               [("CLAIM", "= one side's account")]]
    for row in rows_hs:
        ly += 14
        lx = M
        for cert, desc in row:
            font = f(SANS_B, 7.5)
            w_ = draw.textlength(cert, font=font) + 10
            draw.rounded_rectangle([lx, ly, lx + w_, ly + 12], radius=6,
                                   fill=CERT_FILL[cert])
            draw.text((lx + 5, ly + 2), cert, font=font, fill=(255, 255, 255))
            draw.text((lx + w_ + 4, ly + 2), desc, font=f(SANS, 8), fill=INK)
            lx += w_ + 4 + draw.textlength(desc, font=f(SANS, 8)) + 12

    ax = M + 316
    ay = y + 17
    col2_w = (W - M - ax - 12) / 2
    half = (len(D.ALSO) + 1) // 2
    for j, items in enumerate([D.ALSO[:half], D.ALSO[half:]]):
        x = ax + j * (col2_w + 12)
        yy = ay
        for num, lead, rest in items:
            draw.ellipse([x, yy + 1, x + 12, yy + 13], fill=RED)
            tf2 = f(SANS_B, 8)
            t = str(num)
            tw = draw.textlength(t, font=tf2)
            draw.text((x + (12 - tw) / 2, yy + 2.5), t, font=tf2,
                      fill=(255, 255, 255))
            bf = f(SANS_B, 8.5)
            draw.text((x + 16, yy + 1.5), lead, font=bf, fill=INK)
            rf = f(SANS, 8.5)
            t = rest
            while t and draw.textlength(lead + t, font=rf) > col2_w - 16:
                t = t[:-1]
            draw.text((x + 16 + draw.textlength(lead, font=bf), yy + 1.5), t,
                      font=rf, fill=(35, 35, 35))
            yy += 11.5

    # date check + sources
    y = H - 72
    draw.rectangle([M, y, W - M, H - 34], outline=RED, width=2)
    draw.rectangle([M, y, M + 44, H - 34], fill=RED)
    draw.text((M + 7, y + 5), "DATE", font=f(SANS_B, 10), fill=(255, 255, 255))
    draw.text((M + 4, y + 19), "CHECK", font=f(SANS_B, 10), fill=(255, 255, 255))
    draw_wrapped(draw, D.DATE_CHECK, f(SANS, 8.5), M + 52, y + 5,
                 W - 2 * M - 60, 11, 3, fill=(30, 30, 30))
    tw = draw.textlength(D.SOURCES_LINE, font=f(SANS, 7.5))
    draw.text(((W - tw) / 2, H - 26), D.SOURCES_LINE, font=f(SANS, 7.5),
              fill=GREY)

    img.convert("RGB").quantize(colors=256,
                                method=Image.MEDIANCUT).save(
        HERE / "entry.png", optimize=True)
    print("wrote", HERE / "entry.png")


if __name__ == "__main__":
    main()
