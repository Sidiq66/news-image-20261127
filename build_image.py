# THE DAILY GLOBE — Friday 27 November 2026 front page.
# Draws a 1024x1024 newspaper front page with PIL: masthead, one lead
# story and four panels, all text wrapped and measured so nothing overlaps.
# Run: python3 build_image.py  ->  writes entry.png beside this file.

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (163, 18, 18)
GREY = (90, 86, 76)
LIGHT = (214, 208, 192)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines top-left at (x, y); return y just below the block."""
    lh = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, label):
    f = font(SANS_B, 17)
    draw.text((x, y), label, font=f, fill=RED)
    return y + 24


def masthead(draw):
    """Nameplate, date line and edition strip."""
    f_name = font(SERIF_B, 88)
    name = "THE DAILY GLOBE"
    nw = draw.textlength(name, font=f_name)
    draw.text(((W - nw) / 2, 18), name, font=f_name, fill=INK)
    hrule(draw, 36, W - 36, 122, 3)
    hrule(draw, 36, W - 36, 128, 1)
    f_date = font(SANS_B, 26)
    date = "FRIDAY, 27 NOVEMBER 2026"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, 138), date, font=f_date, fill=INK)
    f_sub = font(SANS, 17)
    left = "ONE DAY'S WORLD NEWS"
    right = "FIVE STORIES  •  VERIFIED"
    draw.text((36, 172), left, font=f_sub, fill=GREY)
    rw = draw.textlength(right, font=f_sub)
    draw.text((W - 36 - rw, 172), right, font=f_sub, fill=GREY)
    hrule(draw, 36, W - 36, 198, 2)


def lead_panel(draw):
    """Full-width lead: Trump says Putin wants a deal."""
    x0, x1, y0, y1 = 36, W - 36, 212, 440
    y = kicker(draw, x0, y0, "WASHINGTON  •  MAR-A-LAGO")
    f_h = font(SERIF_B, 40)
    head = "TRUMP: PUTIN “WOULD LIKE TO MAKE A DEAL”"
    for line in wrap(draw, head, f_h, x1 - x0 - 250):
        draw.text((x0, y), line, font=f_h, fill=INK)
        y += 50
    f_d = font(SERIF, 21)
    deck = ("President Trump said the Russian leader wants an end to the "
            "war in Ukraine, and urged him to pull back military aggression "
            "across Europe so a deal can be made quickly.")
    y = text_block(draw, x0, y + 6, wrap(draw, deck, f_d, x1 - x0 - 250), f_d)
    # Right-hand fact box inside the lead.
    bx0, by0 = x1 - 250, y0 + 26
    draw.rectangle([bx0, by0, x1, by0 + 150], outline=INK, width=2)
    f_b = font(SANS_B, 18)
    f_bt = font(SANS, 16)
    draw.text((bx0 + 12, by0 + 10), "THE DEAL, IN BRIEF", font=f_b, fill=RED)
    facts = ["• 25,000 lost a month",
             "  — Trump",
             "• NATO chief Rutte briefed",
             "• G20 at Doral: 14–15 Dec",
             "• Putin–Zelenskyy “hate",
             "  each other”"]
    yy = by0 + 38
    for fact in facts:
        draw.text((bx0 + 12, yy), fact, font=f_bt, fill=INK)
        yy += 19
    hrule(draw, x0, x1, y1, 2)
    return y1


def panel(draw, x0, x1, y0, y1, kicker_text, headline, deck, motif):
    """One of the four smaller panels with a small drawn motif strip."""
    y = kicker(draw, x0, y0, kicker_text)
    f_h = font(SERIF_B, 29)
    y = text_block(draw, x0, y, wrap(draw, headline, f_h, x1 - x0), f_h,
                   leading=36)
    f_d = font(SANS, 18)
    y = text_block(draw, x0, y + 6,
                   wrap(draw, deck, f_d, x1 - x0), f_d, leading=23)
    motif(draw, x0, x1, y1 - 46, y1 - 8)
    hrule(draw, x0, x1, y1, 1)


def motif_ballot(draw, x0, x1, y0, y1):
    """Ballot box: New Zealand count."""
    cx = (x0 + x1) // 2
    draw.rectangle([cx - 90, y0 + 12, cx + 90, y1], outline=INK, width=2)
    draw.line([(cx - 30, y0 + 12), (cx + 30, y0 + 12)], fill=RED, width=5)
    f = font(SANS_B, 15)
    t = "65 – 65"
    draw.text((cx - draw.textlength(t, font=f) / 2, y0 + 16), t, font=f,
              fill=INK)


def motif_storm(draw, x0, x1, y0, y1):
    """Cloud and rain: the nor'easter."""
    cx = (x0 + x1) // 2
    cloud = (196, 190, 174)
    draw.ellipse([cx - 70, y0 + 2, cx - 14, y0 + 24], fill=cloud,
                 outline=INK, width=2)
    draw.ellipse([cx - 38, y0 - 2, cx + 32, y0 + 22], fill=cloud,
                 outline=INK, width=2)
    draw.ellipse([cx + 2, y0 + 2, cx + 70, y0 + 24], fill=cloud,
                 outline=INK, width=2)
    draw.rectangle([cx - 70, y0 + 14, cx + 70, y0 + 24], fill=cloud)
    draw.line([(cx - 70, y0 + 24), (cx + 70, y0 + 24)], fill=INK, width=2)
    for i, dx in enumerate([-50, -20, 10, 40]):
        draw.line([(cx + dx, y0 + 28), (cx + dx - 5, y1 - 2)],
                  fill=RED, width=3)


def motif_chart(draw, x0, x1, y0, y1):
    """Falling bars: SAP cuts."""
    base = y1
    heights = [30, 24, 18, 12]
    bw, gap = 34, 18
    x = (x0 + x1) // 2 - (4 * bw + 3 * gap) // 2
    for h in heights:
        draw.rectangle([x, base - h, x + bw, base], fill=RED)
        x += bw + gap
    draw.line([(x0, base), (x1, base)], fill=INK, width=2)


def motif_ball(draw, x0, x1, y0, y1):
    """American football: Bears–Lions."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.ellipse([cx - 95, cy - 16, cx + 95, cy + 16], fill=(120, 66, 32),
                 outline=INK, width=2)
    draw.line([(cx - 30, cy), (cx + 30, cy)], fill=(248, 244, 233), width=3)
    for dx in (-20, -7, 6, 19):
        draw.line([(cx + dx, cy - 7), (cx + dx, cy + 7)],
                  fill=(248, 244, 233), width=3)


def footer(draw):
    hrule(draw, 36, W - 36, 984, 2)
    f = font(SANS, 16)
    t = ("THE DAILY GLOBE  •  FRIDAY 27 NOVEMBER 2026  •  "
         "ALL STORIES VERIFIED AGAINST TWO INDEPENDENT SOURCES")
    tw = draw.textlength(t, font=f)
    draw.text(((W - tw) / 2, 992), t, font=f, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead_panel(draw)
    panel(draw, 36, 505, 456, 706, "WELLINGTON",
          "HUNG PARLIAMENT IN NEW ZEALAND",
          "The official count leaves Luxon's coalition one seat short at "
          "65 of 130 — and a party that never held a seat before now holds "
          "the balance of power.",
          motif_ballot)
    panel(draw, 519, 988, 456, 706, "NEW YORK  •  EAST COAST",
          "STORM STILL BATTERING THE COAST",
          "Nearly 900,000 without power and flood warnings through Friday "
          "night. The Macy's parade moves to Saturday — its first weather "
          "delay in 100 years.",
          motif_storm)
    panel(draw, 36, 505, 722, 972, "FRANKFURT  •  BUSINESS",
          "SAP WEIGHS 10,000 JOB CUTS",
          "The German software giant plans an AI-era overhaul of 9% of its "
          "workforce — its second cut of that size in under three years.",
          motif_chart)
    panel(draw, 519, 988, 722, 972, "DETROIT  •  SPORT",
          "BEARS STUN LIONS 39–35",
          "Caleb Williams finds Rome Odunze with three seconds left for "
          "the winner — Chicago takes the NFC North lead at 9–2.",
          motif_ball)
    footer(draw)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
