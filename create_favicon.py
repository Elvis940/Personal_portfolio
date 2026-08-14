from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Colors
primary_color = (108, 99, 255)  # #6C63FF
white = (255, 255, 255)

def create_favicon_ico():
    """Create favicon.ico (32x32)"""
    img = Image.new('RGBA', (32, 32), primary_color + (255,))
    draw = ImageDraw.Draw(img)
    draw.text((6, 4), '</>', fill=white)
    img.save('static/images/favicon.ico')
    print('✅ favicon.ico created')

def create_favicon_svg():
    """Create favicon.svg"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6C63FF" />
      <stop offset="100%" style="stop-color:#3F3D9E" />
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="48" fill="url(#grad)" />
  <text x="25" y="68" font-family="'Courier New', monospace" font-size="46" font-weight="bold" fill="white">&lt;/&gt;</text>
  <circle cx="50" cy="85" r="3" fill="white" opacity="0.5" />
</svg>'''
    
    with open('static/images/favicon.svg', 'w') as f:
        f.write(svg_content)
    print('✅ favicon.svg created')

def create_png_favicon(size, filename):
    """Create PNG favicon of given size"""
    img = Image.new('RGBA', (size, size), primary_color + (255,))
    draw = ImageDraw.Draw(img)
    
    # Adjust text position based on size
    if size == 16:
        draw.text((2, 1), '</>', fill=white)
    elif size == 32:
        draw.text((6, 4), '</>', fill=white)
    elif size == 180:
        draw.text((50, 45), '</>', fill=white)
    else:
        draw.text((size//4, size//4), '</>', fill=white)
    
    img.save(f'static/images/{filename}')
    print(f'✅ {filename} created')

def create_apple_touch_icon():
    """Create Apple Touch Icon (180x180)"""
    img = Image.new('RGBA', (180, 180), primary_color + (255,))
    draw = ImageDraw.Draw(img)
    draw.text((50, 45), '</>', fill=white)
    img.save('static/images/apple-touch-icon.png')
    print('✅ apple-touch-icon.png created')

def create_webmanifest():
    """Create site.webmanifest"""
    manifest = '''{
    "name": "Elvis T. Harmon - Software Engineer",
    "short_name": "Elvis Harmon",
    "description": "Building intelligent software that solves real problems.",
    "theme_color": "#6C63FF",
    "background_color": "#ffffff",
    "display": "standalone",
    "icons": [
        {
            "src": "images/apple-touch-icon.png",
            "sizes": "180x180",
            "type": "image/png"
        },
        {
            "src": "images/favicon-32x32.png",
            "sizes": "32x32",
            "type": "image/png"
        },
        {
            "src": "images/favicon-16x16.png",
            "sizes": "16x16",
            "type": "image/png"
        }
    ]
}'''
    
    with open('static/site.webmanifest', 'w') as f:
        f.write(manifest)
    print('✅ site.webmanifest created')

if __name__ == '__main__':
    print('🔄 Creating favicon files...')
    print('')
    
    create_favicon_ico()
    create_favicon_svg()
    create_png_favicon(16, 'favicon-16x16.png')
    create_png_favicon(32, 'favicon-32x32.png')
    create_apple_touch_icon()
    create_webmanifest()
    
    print('')
    print('✅ All favicon files created successfully!')
    print('📁 Location: static/images/')