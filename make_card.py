#!/usr/bin/env python3
"""Generate a premium editorial business card with QR code for the portfolio website."""

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont
import io
import os

# === Config ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
URL = "https://pihan1996-glitch.github.io/pihan-portfolio/"
PORTRAIT_PATH = os.path.join(SCRIPT_DIR, "portrait.jpg")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "portfolio-card.png")

# Card dimensions (high-res for digital sharing)
W, H = 1080, 1620

# Morandi palette (matching the website)
BG          = (245, 241, 232)  # Warm ivory
NAVY        = (26, 39, 68)     # Deep navy
CHARCOAL    = (42, 42, 42)     # Charcoal
WARM_GREY   = (138, 133, 128)  # Warm grey
LIGHT_LINE  = (212, 207, 196)  # Light warm grey for dividers
MUTED_OLIVE = (122, 122, 94)   # Muted olive accent

# Fonts
FONT_SONGTI    = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_HIRAGINO  = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_NY        = "/System/Library/Fonts/NewYork.ttf"
FONT_NY_ITALIC = "/System/Library/Fonts/NewYorkItalic.ttf"
FONT_BODONI    = "/System/Library/Fonts/Bodoni 72.ttc"

def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except:
        return ImageFont.truetype(path, size)

def center_text(draw, text, fnt, y, fill, W_=W):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (W_ - tw) // 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return tw

def draw_divider(draw, y, width=520):
    x1 = (W - width) // 2
    x2 = x1 + width
    draw.line([(x1, y), (x2, y)], fill=LIGHT_LINE, width=1)

# === 1. Create background ===
card = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(card)

# === 2. Portrait at top (editorial style) ===
try:
    portrait = Image.open(PORTRAIT_PATH)
    # Crop to 2:3 ratio from center
    pw, ph = portrait.size
    target_ratio = 2 / 3
    current_ratio = pw / ph
    if current_ratio > target_ratio:
        # Too wide, crop width
        new_w = int(ph * target_ratio)
        left = (pw - new_w) // 2
        portrait = portrait.crop((left, 0, left + new_w, ph))
    else:
        # Too tall, crop height
        new_h = int(pw / target_ratio)
        top = (ph - new_h) // 2
        portrait = portrait.crop((0, top, pw, top + new_h))

    # Resize to card size
    portrait_w, portrait_h = 300, 450
    portrait = portrait.resize((portrait_w, portrait_h), Image.LANCZOS)
    px = (W - portrait_w) // 2
    py = 80
    card.paste(portrait, (px, py))
    current_y = py + portrait_h + 50
except Exception as e:
    print(f"Portrait not loaded: {e}")
    current_y = 120

# === 3. Name ===
fnt_name_cn = font(FONT_SONGTI, 68, index=1)  # Songti SC Regular/Bold
fnt_name_en = font(FONT_NY_ITALIC, 34)

center_text(draw, "皮晗", fnt_name_cn, current_y, NAVY)
current_y += 82
center_text(draw, "Pihan", fnt_name_en, current_y, WARM_GREY)
current_y += 55

# === 4. Title ===
fnt_title_cn = font(FONT_SONGTI, 30, index=0)
fnt_title_en = font(FONT_NY, 20)

center_text(draw, "品牌营销 ｜ 消费者增长", fnt_title_cn, current_y, NAVY)
current_y += 42
center_text(draw, "Brand Marketing & Consumer Growth", fnt_title_en, current_y, WARM_GREY)
current_y += 45

# === 5. Divider ===
draw_divider(draw, current_y)
current_y += 35

# === 6. Skills ===
fnt_skill = font(FONT_HIRAGINO, 23, index=0)

center_text(draw, "消费者洞察 · 品牌策略 · 整合营销", fnt_skill, current_y, CHARCOAL)
current_y += 36
center_text(draw, "社交媒体 · 用户增长", fnt_skill, current_y, CHARCOAL)
current_y += 45

# === 7. Divider ===
draw_divider(draw, current_y)
current_y += 35

# === 8. Contact info ===
fnt_label = font(FONT_HIRAGINO, 17, index=0)
fnt_value = font(FONT_HIRAGINO, 22, index=0)

contacts = [
    ("邮箱", "pihan1996@qq.com"),
    ("电话", "+86 130 2813 7740"),
    ("所在地", "Shanghai · Sydney"),
    ("教育", "UTS · Master of Strategic Communication"),
]

# Center the contact block
label_w = 60
value_w = max(draw.textbbox((0, 0), v, font=fnt_value)[2] for _, v in contacts)
block_w = label_w + 24 + value_w
block_x = (W - block_w) // 2
label_x = block_x
value_x = block_x + label_w + 24

for label, value in contacts:
    draw.text((label_x, current_y + 3), label, font=fnt_label, fill=WARM_GREY)
    draw.text((value_x, current_y), value, font=fnt_value, fill=CHARCOAL)
    current_y += 38

current_y += 30

# === 9. Divider ===
draw_divider(draw, current_y)
current_y += 40

# === 10. QR Code ===
qr = qrcode.QRCode(
    version=None,
    error_correction=ERROR_CORRECT_H,
    box_size=8,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#1a2744", back_color="#f5f1e8").convert("RGB")
qr_size = qr_img.size[0]

# Paste QR code centered
qx = (W - qr_size) // 2
qy = current_y
card.paste(qr_img, (qx, qy))
current_y += qr_size + 20

# === 11. QR label ===
fnt_qr_label = font(FONT_HIRAGINO, 20, index=0)
center_text(draw, "扫码访问作品集", fnt_qr_label, current_y, WARM_GREY)
current_y += 30
fnt_url = font(FONT_NY, 16)
center_text(draw, "pihan-portfolio", fnt_url, current_y, LIGHT_LINE)

# === 12. Save ===
card.save(OUTPUT_PATH, "PNG", quality=95)
print(f"Card saved: {OUTPUT_PATH} ({card.size[0]}x{card.size[1]})")
