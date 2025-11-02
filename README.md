# BeanFlow Video Generator

A free, open-source text-to-video generator for creating your pitch video.

## Features

- ✅ Converts your script to speech using Google Text-to-Speech (gTTS)
- ✅ Creates a 60+ second MP4 video
- ✅ Two modes:
  - **Text-only mode**: No API key needed, uses animated text slides
  - **Stock footage mode**: Optional Pexels integration for professional video backgrounds

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install FFmpeg (Required for video processing)

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Usage

### Quick Start (Text-only mode - No API key needed)

```bash
python3 beanflow_video_generator.py
```

When prompted for Pexels API key, just press Enter to skip.

### With Stock Footage (Optional)

1. Get a free Pexels API key:
   - Go to https://www.pexels.com/api/
   - Sign up for free
   - Copy your API key

2. Run the script:
```bash
python3 beanflow_video_generator.py
```

3. Enter your Pexels API key when prompted

## Output

The video will be saved as:
```
beanflow_output/beanflow_pitch.mp4
```

- **Format**: MP4 (H.264 video, AAC audio)
- **Duration**: 60+ seconds
- **Resolution**: 1920x1080 (Full HD)
- **Ready to share**: Upload to YouTube, LinkedIn, or email to investors!

## How It Works

1. **Audio Generation**: Converts your script to natural-sounding speech
2. **Visual Creation**:
   - Text mode: Creates professional text slides with your key points
   - Stock mode: Downloads relevant coffee shop footage from Pexels
3. **Video Assembly**: Combines audio and visuals into a single MP4 file

## Customization

Edit the script in `beanflow_video_generator.py`:

- Change text colors: Modify `color='white'` in `create_text_slide()`
- Change background: Modify `bg_color=(30, 30, 30)`
- Change font size: Modify `fontsize=70`
- Edit the script text: Modify the `script` variable in `main()`

## Troubleshooting

**Issue**: "ImageMagick not found"
- **Solution**: The script uses Pillow instead, but if you see this error:
  ```bash
  # macOS
  brew install imagemagick

  # Linux
  sudo apt install imagemagick
  ```

**Issue**: "FFmpeg not found"
- **Solution**: Install FFmpeg (see installation steps above)

**Issue**: Video generation is slow
- **Solution**: This is normal! Video processing takes time. A 60-second video may take 2-5 minutes to generate.

## Free Alternative Video Platforms

If you want even more professional results, you can also try these free online tools:

1. **Canva** (canva.com) - Free tier with text-to-video templates
2. **Clipchamp** (clipchamp.com) - Microsoft's free video editor
3. **Kapwing** (kapwing.com) - Free online video editor

## License

This script is free to use and modify for your BeanFlow pitch!
