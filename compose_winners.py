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


def card_visual(img, draw, story, box, big=None):
    x0, y0, x1, y1 = box
    kind, arg = story["kind"]
    if kind == "img":
        src = Image.open(ASSETS / arg).convert("L")
        src = ImageOps.autocontrast(src)
        img.paste(ImageOps.fit(src, (x1 - x0, y1 - y0)), (x0, y0))
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

    img.save(HERE / "entry.png", optimize=True)
    print("wrote", HERE / "entry.png")


if __name__ == "__main__":
    main()
