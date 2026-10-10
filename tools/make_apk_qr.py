# -*- coding: utf-8 -*-
r"""生成「猫猫歌单」安卓安装包下载二维码。

用法：
    python tools\make_apk_qr.py            # 用下面的默认链接
    python tools\make_apk_qr.py <url>      # 临时换链接

产物（落在项目 dist\ 下）：
    安卓下载二维码.png      纯二维码，白底黑码，方便直接贴用
    安卓下载二维码-卡片.png  带标题和说明的分享卡片

换 APK 版本时不用重跑：链接里的文件名固定是 maomao-songlist.apk，
覆盖 dist\ 里的安装包重新部署即可。
"""
import os
import sys

import qrcode
from PIL import Image, ImageDraw, ImageFont

# 默认直链：GitHub 仓库里的固定文件名 APK，走 jsDelivr CDN（实测国内最快）
DEFAULT_URL = "https://cdn.jsdelivr.net/gh/WLKsir/song-list@main/apk/maomao-songlist.apk"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "dist")

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",   # 微软雅黑 粗体
    r"C:\Windows\Fonts\msyh.ttc",     # 微软雅黑
    r"C:\Windows\Fonts\simhei.ttf",   # 黑体
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_qr(url, box_size=16):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def centered(draw, text, font, y, width, fill):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (right - left)) / 2 - left, y), text, font=font, fill=fill)
    return bottom - top


def build_card(qr_img, url):
    pad = 48
    qr_w, qr_h = qr_img.size
    W = qr_w + pad * 2
    H = qr_h + pad * 2 + 210

    card = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(card)

    f_title = load_font(46)
    f_sub = load_font(26)
    f_tip = load_font(24)

    y = pad - 4
    y += centered(draw, "猫猫歌单 · 安卓版", f_title, y, W, "#1A1A1A") + 14
    y += centered(draw, "扫码下载安装包  v1.0 · 支持安卓 7.0 及以上", f_sub, y, W, "#666666") + 26

    card.paste(qr_img, ((W - qr_w) // 2, y))
    y += qr_h + 26

    centered(draw, "手机扫码 → 浏览器打开 → 直接下载安装", f_tip, y, W, "#666666")
    return card


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    os.makedirs(OUT_DIR, exist_ok=True)

    qr_img = make_qr(url)
    plain_path = os.path.join(OUT_DIR, "安卓下载二维码.png")
    qr_img.save(plain_path)
    print("纯二维码 ->", plain_path, qr_img.size)

    card = build_card(qr_img, url)
    card_path = os.path.join(OUT_DIR, "安卓下载二维码-卡片.png")
    card.save(card_path)
    print("分享卡片 ->", card_path, card.size)

    print("二维码内容 ->", url)


if __name__ == "__main__":
    main()
