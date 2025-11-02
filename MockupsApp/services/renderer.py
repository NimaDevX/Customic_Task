from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from pathlib import Path
import textwrap

# مسیرهای پایه
BASE_DIR = Path(settings.BASE_DIR)
BASE_SHIRTS_DIR = BASE_DIR / "static" / "mockups" / "base"
FONTS_DIR = BASE_DIR / "static" / "fonts"

# پیش‌فرض‌ها
DEFAULT_FONT = "Vazirmatn.ttf"       
DEFAULT_TEXT_COLOR = "#000000"
ALL_SHIRT_COLORS = ("white", "black", "blue", "yellow")

# بارگذاری فونت
def load_font(font_name: str | None, size: int = 64) -> ImageFont.FreeTypeFont:

    name = font_name or DEFAULT_FONT
    path = FONTS_DIR / name
    if not path.exists():
        fallback = FONTS_DIR / DEFAULT_FONT
        if fallback.exists():
            path = fallback
    return ImageFont.truetype(str(path), size)

# رندر متن روی تی‌شرت
def render_text_on_shirt(
    text: str,
    shirt_color: str,
    font_name: str | None = None,
    text_color: str | None = None,
    *,
    max_width_ratio: float = 0.70,
    max_height_ratio: float = 0.40,
    start_size: int = 96,
    min_size: int = 24,
    line_spacing_ratio: float = 0.25,
    y_offset_ratio: float = 0.30,
) -> Image.Image:

    # بارگذاری تصویر پایه
    base_path = BASE_SHIRTS_DIR / f"{shirt_color}.png"
    if not base_path.exists():
        raise FileNotFoundError(
            f"Base shirt image not found for color '{shirt_color}' at {base_path}"
        )

    # تصویر پایه و لایهٔ متن شفاف
    base = Image.open(base_path).convert("RGBA")
    W, H = base.size
    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # اندازه‌گذاری پویا
    size = start_size
    wrapped = text
    font = load_font(font_name, size=size)

# کاهش اندازه فونت تا جاییکه متن در ناحیهٔ مجاز جا شود
    while size >= min_size:
        
        font = load_font(font_name, size=size)
        
		# تخمین عرض هر خط بر اساس اندازه فونت
        wrapped = textwrap.fill(text, width=max(10, int(W / (size * 0.6))))
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align="center", spacing=int(size * line_spacing_ratio))
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        if w <= int(W * max_width_ratio) and h <= int(H * max_height_ratio):
            break
        size -= 4

    # جایگذاری در مرکز ناحیهٔ سینه
    x = (W - w) // 2
    y = int(H * y_offset_ratio)
    
	# رسم متن
    fill_color = text_color or DEFAULT_TEXT_COLOR

    draw.multiline_text(
        (x, y),
        wrapped,
        font=font,
        fill=fill_color,
        align="center",
        spacing=int(size * line_spacing_ratio),
    )

    # ترکیب لایهٔ متن با تصویر پایه
    out = Image.alpha_composite(base, overlay)
    return out.convert("RGB")
