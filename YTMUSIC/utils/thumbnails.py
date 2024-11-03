import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

async def fetch_thumbnail(videoid):
    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        thumbnail_url = result["thumbnails"][0]["url"].split("?")[0]
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                        await f.write(await resp.read())
                    return f"cache/thumb{videoid}.png"
    return None

def create_laptop_thumbnail(videoid, title, channel, views, duration, thumbnail_path):
    # Create a blank background
    background = Image.new('RGB', (1280, 720), (255, 255, 255))
    draw = ImageDraw.Draw(background)

    # Create a laptop-like shape
    laptop_body = Image.new('RGB', (1000, 600), (0, 0, 0))
    laptop_screen = Image.new('RGB', (900, 500), (30, 30, 30))
    laptop_screen = laptop_screen.filter(ImageFilter.BoxBlur(10))  # Add blur to the screen

    # Load and process thumbnail
    youtube_thumb = Image.open(thumbnail_path)
    youtube_thumb = youtube_thumb.resize((900, 500))
    laptop_body.paste(youtube_thumb, (50, 50))

    # Paste the screen into the laptop
    laptop_body.paste(laptop_screen, (50, 50))

    # Create a shadow effect for the laptop
    shadow = Image.new('RGB', (1020, 620), (0, 0, 0))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    background.paste(shadow, (0, 0), shadow)

    # Paste the laptop onto the background
    background.paste(laptop_body, (140, 60))

    # Add text to the thumbnail
    title_font = ImageFont.truetype("path/to/font.ttf", 45)  # Replace with your font path
    channel_font = ImageFont.truetype("path/to/font.ttf", 30)  # Replace with your font path

    draw.text((160, 580), title, fill=(255, 255, 255), font=title_font)
    draw.text((160, 640), f"{channel}  |  {views}", fill=(255, 255, 255), font=channel_font)
    draw.text((900, 640), duration, fill=(255, 255, 255), font=channel_font)

    # Save the final thumbnail
    thumbnail_output = f"cache/{videoid}_laptop_thumbnail.png"
    background.save(thumbnail_output)
    return thumbnail_output

async def generate_thumbnail(videoid):
    thumbnail_path = await fetch_thumbnail(videoid)
    if thumbnail_path:
        title = "Sample Title"  # Replace with actual title
        channel = "Sample Channel"  # Replace with actual channel name
        views = "1M views"  # Replace with actual views
        duration = "5:00"  # Replace with actual duration
        return create_laptop_thumbnail(videoid, title, channel, views, duration, thumbnail_path)
    return None

# Example usage:
# asyncio.run(generate_thumbnail("YOUR_VIDEO_ID"))
