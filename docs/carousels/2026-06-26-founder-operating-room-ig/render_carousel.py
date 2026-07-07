from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

DIR = Path(__file__).resolve().parent
W, H = 1080, 1350

INK = (5, 6, 10)
SURFACE = (10, 12, 20)
BORDER = (26, 31, 46)
IVORY = (241, 243, 249)
PAPER = (244, 241, 232)
MUTED = (138, 144, 168)
BLUE = (110, 168, 254)
VIOLET = (167, 139, 250)
GOLD = (228, 197, 122)
EMERALD = (121, 215, 166)

FONT_DIR = Path("C:/Windows/Fonts")

def font(name, size):
    candidates = {
        "serif": ["georgia.ttf", "georgiab.ttf"],
        "serif_bold": ["georgiab.ttf", "georgia.ttf"],
        "sans": ["segoeui.ttf", "arial.ttf"],
        "sans_semibold": ["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"],
        "mono": ["consola.ttf", "cour.ttf"],
        "mono_bold": ["consolab.ttf", "courbd.ttf"],
    }[name]
    for candidate in candidates:
        path = FONT_DIR / candidate
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

SERIF_98 = font("serif", 98)
SERIF_88 = font("serif", 88)
SERIF_78 = font("serif", 78)
SERIF_66 = font("serif", 66)
SANS_40 = font("sans_semibold", 40)
SANS_35 = font("sans_semibold", 35)
SANS_30 = font("sans_semibold", 30)
SANS_25 = font("sans_semibold", 25)
SANS_22 = font("sans_semibold", 22)
SANS_19 = font("sans_semibold", 19)
SANS_17 = font("sans_semibold", 17)
MONO_20 = font("mono_bold", 20)
MONO_17 = font("mono_bold", 17)

def rgba(color, alpha):
    return (color[0], color[1], color[2], alpha)

def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]

def draw_spaced(draw, xy, text, fnt, fill, spacing=4):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w, _ = text_size(draw, ch, fnt)
        x += w + spacing

def wrap_lines(draw, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = word if not current else current + " " + word
        if text_size(draw, test, fnt)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def cover_image(path, anchor=(0.5, 0.5)):
    img = Image.open(DIR / path).convert("RGB")
    sw, sh = img.size
    scale = max(W / sw, H / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    ax, ay = anchor
    left = int((nw - W) * ax)
    top = int((nh - H) * ay)
    left = max(0, min(left, nw - W))
    top = max(0, min(top, nh - H))
    return img.crop((left, top, left + W, top + H)).convert("RGBA")

def add_gradient(base, left=0.82, top=0.55, bottom=0.70, accent=None):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = overlay.load()
    for y in range(H):
        yy = y / (H - 1)
        vertical = top * (1 - min(yy / 0.46, 1)) + bottom * max((yy - 0.45) / 0.55, 0)
        for x in range(W):
            xx = x / (W - 1)
            horizontal = left * max(0, 1 - xx / 0.75)
            a = int(255 * min(0.90, vertical + horizontal * 0.58))
            px[x, y] = (*INK, a)
    base.alpha_composite(overlay)
    if accent:
        rad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rpx = rad.load()
        cx, cy, rr = int(W * 0.20), int(H * 0.16), int(W * 0.62)
        for y in range(max(0, cy - rr), min(H, cy + rr)):
            for x in range(max(0, cx - rr), min(W, cx + rr)):
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / rr
                if d <= 1:
                    a = int(48 * (1 - d) ** 1.75)
                    rpx[x, y] = (*accent, a)
        base.alpha_composite(rad)
    return base

def base_dark():
    img = Image.new("RGBA", (W, H), (*INK, 255))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, H, 28):
        a = int(6 + 8 * (1 - y / H))
        d.line((0, y, W, y), fill=(255, 255, 255, a), width=1)
    for x in range(0, W, 36):
        a = int(4 + 6 * (1 - x / W))
        d.line((x, 0, x, H), fill=(255, 255, 255, a), width=1)
    for i in range(64):
        x = (i * 173) % W
        y = (i * 311) % H
        d.ellipse((x, y, x + 2, y + 2), fill=rgba(BLUE if i % 3 else GOLD, 52))
    blur = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blur, "RGBA")
    bd.ellipse((-220, -180, 520, 460), fill=rgba(BLUE, 34))
    bd.ellipse((660, 720, 1320, 1460), fill=rgba(GOLD, 28))
    blur = blur.filter(ImageFilter.GaussianBlur(70))
    img.alpha_composite(blur)
    return img

def border_and_meta(img, eyebrow, idx, accent=GOLD, footer="FRANKX / STARLIGHT"):
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((34, 34, W - 34, H - 34), outline=(241, 243, 249, 72), width=1)
    d.line((82, 91, 126, 91), fill=rgba(accent, 255), width=2)
    draw_spaced(d, (142, 77), eyebrow.upper(), SANS_22, rgba(IVORY, 220), 5)
    draw_spaced(d, (82, 1218), footer.upper(), SANS_19, rgba(IVORY, 178), 3)
    count = f"{idx:02d} / 08"
    w, _ = text_size(d, count, MONO_20)
    d.text((W - 82 - w, 1218), count, font=MONO_20, fill=rgba(accent, 255))

def title_block(d, lines, x=82, y=250, size="large", fill=IVORY):
    fnt = {"large": SERIF_98, "mid": SERIF_88, "small": SERIF_78, "compact": SERIF_66}[size]
    leading = {"large": 100, "mid": 90, "small": 80, "compact": 70}[size]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=rgba(fill, 255))
        y += leading
    return y

def body_block(d, lines, x=84, y=650, width=760, fnt=SANS_35, fill=IVORY, leading=45):
    out = []
    for line in lines:
        out.extend(wrap_lines(d, line, fnt, width))
    for line in out:
        d.text((x, y), line, font=fnt, fill=rgba(fill, 224))
        y += leading
    return y

def round_rect(d, box, fill, outline=None, width=1, radius=18):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def chip(d, xy, text, accent=BLUE):
    x, y = xy
    w = text_size(d, text, SANS_19)[0] + 34
    round_rect(d, (x, y, x + w, y + 38), fill=(255, 255, 255, 18), outline=rgba(accent, 110), radius=19)
    d.text((x + 17, y + 8), text, font=SANS_19, fill=rgba(IVORY, 218))
    return x + w + 10

def node_card(d, box, title, body, accent=BLUE):
    round_rect(d, box, fill=(10, 12, 20, 198), outline=rgba(accent, 118), width=1, radius=16)
    x1, y1, x2, y2 = box
    d.ellipse((x1 + 18, y1 + 20, x1 + 30, y1 + 32), fill=rgba(accent, 255))
    d.text((x1 + 42, y1 + 14), title, font=SANS_22, fill=rgba(IVORY, 238))
    body_lines = wrap_lines(d, body, SANS_17, x2 - x1 - 44)
    yy = y1 + 51
    for line in body_lines[:2]:
        d.text((x1 + 22, yy), line, font=SANS_17, fill=rgba(MUTED, 232))
        yy += 24

def draw_flow(d, points, accent=BLUE):
    for a, b in zip(points, points[1:]):
        d.line((a[0], a[1], b[0], b[1]), fill=rgba(accent, 130), width=2)
        d.ellipse((b[0] - 5, b[1] - 5, b[0] + 5, b[1] + 5), fill=rgba(accent, 210))

def slide_1():
    img = add_gradient(cover_image("source-01-founder-operating-room.png", (0.54, 0.45)), accent=GOLD)
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "Founder Operating Room", 1, GOLD)
    y = title_block(d, ["A calmer", "company.", "A smarter", "system."], size="mid")
    body_block(d, ["AI agents become valuable when the company gives them rooms, roles, proof, and approvals."], y=y + 26, width=780)
    return img

def slide_2():
    img = base_dark()
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "The operating idea", 2, BLUE)
    title_block(d, ["One insight", "becomes a", "system."], size="small")
    body_block(d, ["Great content explains the idea and reveals the operating room behind it."], y=560, width=760)
    steps = [
        ("01", "Signal", "lab updates + founder insight"),
        ("02", "Brief", "angle, audience, proof"),
        ("03", "Build", "copy, image, carousel"),
        ("04", "Proof", "sources, QA, preview"),
        ("05", "Approve", "human yes before public"),
        ("06", "Publish", "many platform cuts"),
    ]
    x, y = 86, 728
    for i, (num, t, b) in enumerate(steps):
        row = i // 2
        col = i % 2
        bx = x + col * 464
        by = y + row * 134
        accent = GOLD if i in [0, 5] else BLUE
        round_rect(d, (bx, by, bx + 414, by + 96), fill=(10, 12, 20, 214), outline=rgba(accent, 130), radius=18)
        d.text((bx + 22, by + 18), num, font=MONO_20, fill=rgba(accent, 255))
        d.text((bx + 78, by + 13), t, font=SANS_30, fill=rgba(IVORY, 246))
        d.text((bx + 78, by + 52), b, font=SANS_19, fill=rgba(MUTED, 236))
    return img

def slide_3():
    img = add_gradient(cover_image("source-02-slack-cockpit.png", (0.47, 0.42)), left=0.86, top=0.50, bottom=0.68, accent=BLUE)
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "Slack cockpit", 3, BLUE)
    title_block(d, ["Slack becomes", "the cockpit."], size="mid")
    body_block(d, ["Each channel has a job: route work, create proof, and protect decisions."], y=474, width=700)
    channels = [
        ("#work-queue", "intake and routing"),
        ("#execution-room", "active work and proof"),
        ("#daily-report", "portfolio signal"),
        ("#social-carousels", "design review"),
        ("#social-approvals", "human yes/no"),
        ("#repo-command", "branches, tests, risks"),
    ]
    yy = 662
    for i, (name, desc) in enumerate(channels):
        accent = GOLD if i in [3, 4] else BLUE
        round_rect(d, (82, yy, 604, yy + 74), fill=(10, 12, 20, 204), outline=rgba(accent, 112), radius=16)
        d.text((106, yy + 14), name, font=SANS_25, fill=rgba(IVORY, 244))
        d.text((106, yy + 43), desc, font=SANS_17, fill=rgba(MUTED, 232))
        yy += 86
    return img

def slide_4():
    img = base_dark()
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "Agent ownership", 4, VIOLET)
    title_block(d, ["Every agent", "gets a job."], size="mid")
    body_block(d, ["A premium agent team starts with ownership, proof, and human judgment."], y=474, width=760)
    rules = [
        ("Role", "What is this agent trusted to own?"),
        ("Room", "Where does the work live in Slack?"),
        ("Proof", "What evidence must be attached?"),
        ("Gate", "What needs a human yes?"),
    ]
    y = 684
    for i, (title, body) in enumerate(rules):
        accent = [BLUE, VIOLET, EMERALD, GOLD][i]
        round_rect(d, (82, y, 998, y + 108), fill=(10, 12, 20, 220), outline=rgba(accent, 142), radius=20)
        d.text((112, y + 26), f"{i+1:02d}", font=MONO_20, fill=rgba(accent, 255))
        d.text((178, y + 18), title, font=SANS_35, fill=rgba(IVORY, 248))
        d.text((430, y + 30), body, font=SANS_25, fill=rgba(MUTED, 238))
        y += 126
    round_rect(d, (82, 1180, 734, 1242), fill=rgba(PAPER, 232), radius=18)
    d.text((112, 1198), "Approval keeps trust visible.", font=SANS_25, fill=rgba(INK, 255))
    return img

def slide_5():
    img = add_gradient(cover_image("source-03-proof-wall.png", (0.43, 0.44)), left=0.84, top=0.48, bottom=0.70, accent=EMERALD)
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "Proof before publish", 5, EMERALD)
    title_block(d, ["Proof makes", "momentum", "trustworthy."], size="small")
    body_block(d, ["Every public action earns its way through source, build, preview, QA, approval, and archive."], y=570, width=730)
    checks = ["source-backed", "build checked", "preview inspected", "visual QA", "human approval", "proof archived"]
    yy = 806
    for c in checks:
        round_rect(d, (82, yy, 486, yy + 54), fill=(10, 12, 20, 190), outline=rgba(EMERALD, 100), radius=16)
        d.ellipse((105, yy + 17, 125, yy + 37), fill=rgba(EMERALD, 210))
        d.text((144, yy + 13), c, font=SANS_22, fill=rgba(IVORY, 232))
        yy += 64
    return img

def slide_6():
    img = add_gradient(cover_image("source-04-content-studio.png", (0.48, 0.45)), left=0.84, top=0.52, bottom=0.70, accent=GOLD)
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "Content studio", 6, GOLD)
    title_block(d, ["Content becomes", "a studio", "pipeline."], size="small")
    body_block(d, ["Research becomes a recording brief. The brief becomes visuals, captions, approvals, and platform cuts."], y=570, width=760)
    x = 88
    for txt in ["research", "brief", "imagegen", "carousel", "approval", "post"]:
        x = chip(d, (x, 858), txt, GOLD if txt in ["brief", "approval"] else BLUE)
        if x > 870:
            x = 88
    return img

def slide_7():
    img = base_dark()
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "Motion-ready system", 7, BLUE)
    title_block(d, ["One idea.", "Four cuts."], size="mid")
    body_block(d, ["The best carousel is already a storyboard for motion."], y=474, width=680)
    formats = [
        ("4:5", "Instagram carousel", (96, 670, 348, 985), GOLD),
        ("9:16", "Reel / Story", (402, 620, 612, 995), BLUE),
        ("16:9", "YouTube / deck", (666, 705, 982, 883), VIOLET),
        ("1:1", "grid crop", (705, 935, 950, 1180), EMERALD),
    ]
    for ratio, label, box, accent in formats:
        round_rect(d, box, fill=(10, 12, 20, 200), outline=rgba(accent, 150), radius=18)
        x1, y1, x2, y2 = box
        d.text((x1 + 24, y1 + 22), ratio, font=SERIF_66, fill=rgba(IVORY, 245))
        d.text((x1 + 24, y2 - 52), label, font=SANS_19, fill=rgba(MUTED, 235))
        d.line((x1 + 24, y1 + 108, x2 - 24, y1 + 108), fill=rgba(accent, 140), width=2)
    return img

def slide_8():
    img = add_gradient(cover_image("source-01-founder-operating-room.png", (0.55, 0.52)), left=0.88, top=0.54, bottom=0.76, accent=GOLD)
    d = ImageDraw.Draw(img, "RGBA")
    border_and_meta(img, "The founder OS", 8, GOLD)
    title_block(d, ["Build the", "company that", "learns daily."], size="small")
    body_block(d, ["Daily scans. Repo proof. Domain health. Social approvals. Customer signals. Better decisions."], y=570, width=800)
    round_rect(d, (82, 915, 690, 1020), fill=(244, 241, 232, 232), outline=None, radius=22)
    d.text((112, 943), "Follow the operating maps.", font=SANS_30, fill=rgba(INK, 255))
    d.text((112, 982), "FrankX / Starlight", font=SANS_19, fill=rgba((36, 39, 52), 240))
    return img

SLIDES = [slide_1, slide_2, slide_3, slide_4, slide_5, slide_6, slide_7, slide_8]

def main():
    exports = DIR / "exports"
    png_dir = exports / "png"
    jpg_dir = exports / "jpg"
    png_dir.mkdir(parents=True, exist_ok=True)
    jpg_dir.mkdir(parents=True, exist_ok=True)
    for idx, maker in enumerate(SLIDES, 1):
        img = maker().convert("RGB")
        png = png_dir / f"{idx:02d}-founder-operating-room.png"
        jpg = jpg_dir / f"{idx:02d}-founder-operating-room.jpg"
        img.save(png, optimize=True)
        img.save(jpg, quality=94, optimize=True, progressive=True)
        print(png)

if __name__ == "__main__":
    main()
