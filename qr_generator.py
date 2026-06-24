import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

QR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "qr_codes")

def generate_qr(grave_id: int, unique_code: str, full_name: str = "") -> str:
    os.makedirs(QR_DIR, exist_ok=True)

    # The QR encodes the unique code (in real deployment: full URL)
    data = f"GRAVE:{unique_code}"

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=3
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="#1a472a", back_color="white").convert("RGB")

    # Add label below QR
    w, h = qr_img.size
    label_h = 50
    final = Image.new("RGB", (w, h + label_h), "white")
    final.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(final)
    draw.text((w//2, h + 8), unique_code, fill="#1a1a1a", anchor="mt")
    if full_name:
        draw.text((w//2, h + 28), full_name[:30], fill="#555555", anchor="mt")

    path = os.path.join(QR_DIR, f"{unique_code}.png")
    final.save(path)

    # Update DB
    from database.db_connection import get_connection
    conn = get_connection()
    conn.execute("UPDATE graves SET qr_code_path=? WHERE id=?", (path, grave_id))
    conn.commit()
    conn.close()

    return path
