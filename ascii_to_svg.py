import os
import sys
import subprocess
import math

# Automatically switch to .venv Python interpreter if PIL (Pillow) is not found in current interpreter
try:
    from PIL import Image, ImageEnhance  # pyright: ignore[reportMissingImports] # type: ignore
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(script_dir, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python) and os.path.abspath(sys.executable) != os.path.abspath(venv_python):
        print(f"PIL not installed in {sys.executable}. Auto-switching to workspace virtual environment: {venv_python}")
        sys.exit(subprocess.call([venv_python] + sys.argv))
    else:
        print("Error: Pillow library not installed. Please install it using: pip install Pillow")
        sys.exit(1)

downloads = r"C:\Users\RIPAN SAMUI\Downloads"
target_img_path = os.path.join(downloads, "WhatsApp Image 2026-07-27 at 9.27.00 PM (1).png")

if not os.path.exists(target_img_path):
    candidates = [
        os.path.join(downloads, "WhatsApp Image 2026-07-27 at 9.27.00 PM.png"),
        os.path.join(downloads, "WhatsApp Image 2026-07-27 at 9.27.00 PM.jpeg")
    ]
    for c in candidates:
        if os.path.exists(c):
            target_img_path = c
            break

if not os.path.exists(target_img_path):
    print(f"Error: Target image file not found at {target_img_path}")
    sys.exit(1)

print(f"Loading image for Full-Head & Hair Structural ASCII: {target_img_path}")

def generate_full_head_ascii(img_path, width=94, height=70):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    print(f"Original Image Size: {w}x{h}")
    
    char_aspect_ratio = 0.555
    target_ratio = (width * char_aspect_ratio) / height
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        new_w = int(target_ratio * h)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif current_ratio < target_ratio:
        new_h = h
        new_w = int(target_ratio * h)
        pad_left = (new_w - w) // 2
        padded_img = Image.new("RGB", (new_w, new_h), (70, 140, 80))
        padded_img.paste(img, (pad_left, 0))
        img = padded_img

    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    
    enhancer_sharp = ImageEnhance.Sharpness(img_resized)
    img_sharp = enhancer_sharp.enhance(1.5)
    enhancer_contrast = ImageEnhance.Contrast(img_sharp)
    img_final = enhancer_contrast.enhance(1.30)
    
    palette = ["@", "#", "$", "%", "*", "+", "=", "-", ":", ".", " ", " "]
    
    lines = []
    for y in range(height):
        line_chars = []
        for x in range(width):
            r, g, b = img_resized.getpixel((x, y))
            if g > r + 8 and g > b + 8 and g > 40:
                line_chars.append(" ")
            else:
                rc, gc, bc = img_final.getpixel((x, y))
                lum = 0.299 * rc + 0.587 * gc + 0.114 * bc
                norm_lum = lum / 255.0
                adjusted_lum = math.pow(norm_lum, 0.80)
                idx = int(adjusted_lum * (len(palette) - 1))
                idx = max(0, min(len(palette) - 1, idx))
                line_chars.append(palette[idx])
        lines.append("".join(line_chars))
    return lines

hd_lines = generate_full_head_ascii(target_img_path, width=94, height=70)

print("\n=== FULL-HEAD & HAIR STRUCTURAL ASCII PORTRAIT ===")
for line in hd_lines:
    print(line)
print("==================================================\n")

tspan_lines = []
start_y = 52.00
step_y = 6.10

for i, line in enumerate(hd_lines):
    y_val = f"{start_y + (i * step_y):.2f}"
    tspan_lines.append(f'<tspan x="110" y="{y_val}" xml:space="preserve">{line}</tspan>')

new_ascii_block = "\n  <text x=\"110\" y=\"0\" class=\"ascii\">\n  \n" + "\n".join(tspan_lines) + "\n\n  </text>\n"

def update_svg(svg_path):
    if not os.path.exists(svg_path):
        print(f"Error: Target SVG file not found: {svg_path}")
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_css_part = ".ascii  {"
    end_css_idx = content.find("}", content.find(old_css_part))
    if end_css_idx != -1 and content.find(old_css_part) != -1:
        start_css_idx = content.find(old_css_part)
        new_css = ".ascii  { font-family: 'Courier New', Consolas, monospace; font-size: 5.5px; fill: url(#asciiGrad); letter-spacing: -0.15px; }"
        content = content[:start_css_idx] + new_css + content[end_css_idx+1:]
        
    ascii_idx = content.find('class="ascii">')
    if ascii_idx == -1:
        print(f"Could not find class=\"ascii\" in {svg_path}")
        return
    
    start_idx = content.rfind("<text", 0, ascii_idx)
    end_tag = '</text>'
    end_idx = content.find(end_tag, ascii_idx)
    if start_idx != -1 and end_idx != -1:
        end_idx += len(end_tag)
        updated_content = content[:start_idx] + new_ascii_block.strip() + content[end_idx:]
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Successfully updated Full-Head structural ASCII in {os.path.basename(svg_path)}!")
    else:
        print(f"Error: Could not locate <text class=\"ascii\"> bounds in {svg_path}")

update_svg(r"c:\Users\RIPAN SAMUI\Documents\file\light.svg")
update_svg(r"c:\Users\RIPAN SAMUI\Documents\file\dark.svg")
