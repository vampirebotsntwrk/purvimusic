import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from youtubesearchpython import VideosSearch

async def get_thumb(videoid):
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

def create_thumbnail(videoid, title, channel, views, duration, thumbnail_path):
    # Create a blank background
    background = Image.new('RGB', (1280, 720), (255, 255, 255))
    
    # Load and process thumbnail
    youtube_thumb = Image.open(thumbnail_path)
    youtube_thumb = youtube_thumb.resize((400, 225))  # Resize to fit the circles

    # Create circles
    draw = ImageDraw.Draw(background)
    circle_radius = 115
    left_circle_center = (320, 360)
    right_circle_center = (960, 360)

    # Draw circles
    draw.ellipse((left_circle_center[0] - circle_radius, left_circle_center[1] - circle_radius,
                   left_circle_center[0] + circle_radius, left_circle_center[1] + circle_radius), outline=(0, 0, 0), width=5)
    draw.ellipse((right_circle_center[0] - circle_radius, right_circle_center[1] - circle_radius,
                   right_circle_center[0] + circle_radius, right_circle_center[1] + circle_radius), outline=(0, 0, 0), width=5)

    # Create blurred background
    blurred_background = background.filter(ImageFilter.GaussianBlur(15))

    # Paste the YouTube thumbnail images into the circles
    blurred_background.paste(youtube_thumb, (left_circle_center[0] - 200, left_circle_center[1] - 112), youtube_thumb)
    blurred_background.paste(youtube_thumb, (right_circle_center[0] - 200, right_circle_center[1] - 112), youtube_thumb)

    # Paste the blurred background
    background.paste(blurred_background, (0, 0))

    # Add text details below the circles
    font_path = "path/to/font.ttf"  # Replace with your actual font path
    draw.text((320 - 100, 500), title, fill=(0, 0, 0), font=ImageFont.truetype(font_path, 30))
    draw.text((960 - 100, 500), f"{channel}  |  {views}  |  {duration}", fill=(0, 0, 0), font=ImageFont.truetype(font_path, 30))

    # Save the final thumbnail
    thumbnail_output = f"cache/{videoid}_thumbnail.png"
    background.save(thumbnail_output)
    return thumbnail_output

async def generate_thumbnail(videoid):
    thumbnail_path = await get_thumb(videoid)
    if thumbnail_path:
        title = "Sample Title"  # Replace with actual title
        channel = "Sample Channel"  # Replace with actual channel name
        views = "1M views"  # Replace with actual views
        duration = "5:00"  # Replace with actual duration
        return create_thumbnail(videoid, title, channel, views, duration, thumbnail_path)
    return None

# Example usage:
# asyncio.run(generate_thumbnail("YOUR_VIDEO_ID"))
