#!/usr/bin/env python3
"""Create branded WebP placeholders for cardrummy.org."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

SPECS = [
    ("card-rummy.webp", 512, 512, "Card\nRummy", "App icon placeholder"),
    ("card-rummy-og.webp", 1200, 630, "Card Rummy", "OG share image"),
    ("card-rummy-game-interface.webp", 800, 1000, "Lobby", "Game interface"),
    ("card-rummy-games.webp", 800, 1000, "Games", "Games collection"),
    ("card-rummy-earn-bonus.webp", 800, 1000, "Bonus", "Bonuses screen"),
    ("card-rummy-add-money.webp", 800, 1000, "Deposit", "Add money"),
    ("card-rummy-withdraw-money.webp", 800, 1000, "Withdraw", "Withdraw money"),
    ("card-rummy-refer-and-earn.webp", 800, 1000, "Refer", "Refer and earn"),
    ("card-rummy-recharge-rebate.webp", 800, 1000, "Rebate", "Recharge rebate"),
    ("card-rummy-bind-mail.webp", 800, 1000, "Bind", "Bind email"),
    ("favicon-192.webp", 192, 192, "CR", "Favicon"),
]


def font(size: int):
    for name in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make(name, w, h, label, _caption):
    img = Image.new("RGB", (w, h), "#0B0F2E")
    draw = ImageDraw.Draw(img)
    # atmosphere
    draw.ellipse((-w * 0.2, -h * 0.3, w * 0.7, h * 0.5), fill="#141B42")
    draw.ellipse((w * 0.4, h * 0.4, w * 1.2, h * 1.2), fill="#1A2458")
    # gold frame
    inset = max(12, min(w, h) // 18)
    draw.rounded_rectangle(
        (inset, inset, w - inset, h - inset),
        radius=min(w, h) // 12,
        outline="#F0D060",
        width=max(3, min(w, h) // 80),
    )
    f = font(max(28, min(w, h) // 8))
    bbox = draw.multiline_textbbox((0, 0), label, font=f, align="center", spacing=8)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(
        ((w - tw) / 2, (h - th) / 2),
        label,
        fill="#FFB84D",
        font=f,
        align="center",
        spacing=8,
    )
    img.save(OUT / name, "WEBP", quality=82)
    print("wrote", name)


if __name__ == "__main__":
    for spec in SPECS:
        make(*spec)
