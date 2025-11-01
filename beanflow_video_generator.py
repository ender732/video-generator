#!/usr/bin/env python3
"""
BeanFlow Video Generator
Creates a text-to-video presentation using free tools
"""

import os
from pathlib import Path
from gtts import gTTS
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip
)
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap

class BeanFlowVideoGenerator:
    def __init__(self, output_dir="beanflow_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.pexels_api_key = None  # Will be set by user

    def set_pexels_api_key(self, api_key):
        """Set Pexels API key for stock footage"""
        self.pexels_api_key = api_key

    def generate_audio(self, script, output_file="audio.mp3"):
        """Generate audio from text using gTTS"""
        print("Generating audio from script...")
        audio_path = self.output_dir / output_file

        tts = gTTS(text=script, lang='en', slow=False)
        tts.save(str(audio_path))
        print(f"Audio saved to {audio_path}")
        return audio_path

    def search_pexels_videos(self, query, per_page=5):
        """Search for videos on Pexels"""
        if not self.pexels_api_key:
            return []

        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": self.pexels_api_key}
        params = {"query": query, "per_page": per_page, "orientation": "landscape"}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("videos", [])
        except Exception as e:
            print(f"Error searching Pexels: {e}")
            return []

    def download_video(self, url, filename):
        """Download a video from URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filepath = self.output_dir / filename

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filepath
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

    def create_text_slide(self, text, duration, size=(1920, 1080),
                         fontsize=60, color=(255, 255, 255), bg_color=(30, 30, 30)):
        """Create a text slide with background using Pillow"""
        print(f"Creating text slide: {text[:50]}...")

        # Create image with PIL
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)

        # Try to use a system font, fallback to default
        try:
            # Try common macOS fonts
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", fontsize)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", fontsize)
            except:
                # Use default font if no TrueType fonts available
                font = ImageFont.load_default()
                fontsize = 20  # Default font is smaller

        # Wrap text to fit width
        max_width = size[0] - 200
        lines = []
        for paragraph in text.split('\n'):
            if paragraph.strip():
                # Estimate characters per line
                avg_char_width = fontsize * 0.6
                chars_per_line = int(max_width / avg_char_width)
                wrapped = textwrap.fill(paragraph, width=chars_per_line)
                lines.extend(wrapped.split('\n'))
            else:
                lines.append('')

        # Calculate text position (centered)
        line_height = int(fontsize * 1.5)
        total_height = len(lines) * line_height
        y = (size[1] - total_height) // 2

        # Draw each line
        for line in lines:
            # Get text bounding box for centering
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2

            draw.text((x, y), line, fill=color, font=font)
            y += line_height

        # Convert PIL image to numpy array for moviepy
        img_array = np.array(img)

        # Create ImageClip
        clip = ImageClip(img_array, duration=duration)

        return clip

    def create_video_without_pexels(self, audio_path, script):
        """Create video with text slides (no stock footage needed)"""
        print("\nCreating video with text slides...")

        # Get audio duration
        audio = AudioFileClip(str(audio_path))
        total_duration = audio.duration

        # Break script into scenes
        scenes = [
            ("BeanFlow\nAI-Powered Coffee Shop Solution", 3),
            ("The Problem:\nBottleneck at the Register", 8),
            ("Customers wait...\nBaristas are stressed...\nRevenue is lost", 8),
            ("The Solution:\nBeanFlow AI System", 5),
            ("Part 1:\nSeamless Mobile/Kiosk Ordering", 6),
            ("Part 2:\nPredictive AI Engine", 8),
            ("Forecast orders before\nthey're placed", 7),
            ("Pre-prep ingredients\nduring payment", 6),
            ("Result:\n20% Faster Service", 8),
            ("More customers served\nHigher revenue\nNo extra staff needed", 8),
            ("BeanFlow:\nYour Competitive Advantage", 5),
            ("Let's discuss your ROI", 3)
        ]

        # Adjust durations to match audio length
        total_scene_duration = sum(d for _, d in scenes)
        scale_factor = total_duration / total_scene_duration

        clips = []
        for text, duration in scenes:
            adjusted_duration = duration * scale_factor
            clip = self.create_text_slide(text, adjusted_duration, fontsize=70)
            clips.append(clip)

        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        final_video = final_video.set_audio(audio)

        return final_video

    def create_video_with_pexels(self, audio_path, script):
        """Create video with Pexels stock footage"""
        print("\nCreating video with stock footage...")

        # Get audio duration
        audio = AudioFileClip(str(audio_path))
        total_duration = audio.duration

        # Search queries for different sections
        queries = [
            "coffee shop busy",
            "coffee barista working",
            "people waiting in line",
            "mobile phone ordering",
            "artificial intelligence",
            "coffee preparation",
            "happy customers coffee",
            "business success"
        ]

        clips = []
        duration_per_clip = total_duration / len(queries)

        for i, query in enumerate(queries):
            print(f"Searching for: {query}")
            videos = self.search_pexels_videos(query, per_page=3)

            if videos and videos[0].get("video_files"):
                # Get HD quality video
                video_files = videos[0]["video_files"]
                hd_video = next((v for v in video_files if v.get("quality") == "hd"), video_files[0])
                video_url = hd_video["link"]

                # Download video
                video_path = self.download_video(video_url, f"clip_{i}.mp4")

                if video_path:
                    clip = VideoFileClip(str(video_path))
                    # Trim or loop to match duration
                    if clip.duration < duration_per_clip:
                        # Loop the clip
                        clip = clip.loop(duration=duration_per_clip)
                    else:
                        clip = clip.subclip(0, duration_per_clip)

                    clips.append(clip)
                else:
                    # Fallback to text slide
                    clip = self.create_text_slide(query.title(), duration_per_clip)
                    clips.append(clip)
            else:
                # Fallback to text slide
                clip = self.create_text_slide(query.title(), duration_per_clip)
                clips.append(clip)

        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        final_video = final_video.set_audio(audio)

        return final_video

    def generate_video(self, script, use_pexels=False):
        """Generate complete video from script"""
        print("=" * 60)
        print("BeanFlow Video Generator")
        print("=" * 60)

        # Generate audio
        audio_path = self.generate_audio(script)

        # Create video
        if use_pexels and self.pexels_api_key:
            final_video = self.create_video_with_pexels(audio_path, script)
        else:
            final_video = self.create_video_without_pexels(audio_path, script)

        # Export final video
        output_path = self.output_dir / "beanflow_pitch.mp4"
        print(f"\nExporting final video to {output_path}...")

        final_video.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.output_dir / 'temp-audio.m4a'),
            remove_temp=True
        )

        print("\n" + "=" * 60)
        print(f"✓ Video generated successfully!")
        print(f"✓ Output: {output_path}")
        print(f"✓ Duration: {final_video.duration:.1f} seconds")
        print("=" * 60)

        return output_path


def main():
    # BeanFlow script
    script = """Good morning. I want to talk about the real problem in every busy coffee shop: the bottleneck at the register. During the rush, customers wait, baristas are stressed, and critical revenue is lost when people walk away from a long line. The issue isn't barista speed; it's the reactive operational model.

My solution is BeanFlow: an AI-powered system that shifts operations from reactive to proactive.

It works in two parts: first, a seamless mobile/kiosk ordering system for speed. Second, and most critical, a predictive AI engine that ingests sales history, time patterns, and even weather data to accurately forecast the next three to five orders before they are fully placed.

This prediction is translated into actionable intelligence on the barista screen, allowing them to pre-prep key ingredients—grinding the beans, steaming the milk—during the customer's payment process.

The result? We are not waiting for the order to start making the coffee. Based on my projections, this leads to a 20% improvement in service speed during peak hours, directly translating to more customers served per hour and significantly higher revenue without having to hire extra staff.

BeanFlow isn't just software; it's a competitive advantage that increases throughput, boosts profitability, and makes the barista's job easier. It's the future of efficient coffee service.

I'd be happy to show you a detailed operational model and the ROI calculator for your locations."""

    # Initialize generator
    generator = BeanFlowVideoGenerator()

    # Optional: Add Pexels API key for stock footage
    # Get free API key at: https://www.pexels.com/api/
    pexels_key = input("\nEnter Pexels API key (or press Enter to skip for text-only video): ").strip()

    use_pexels = False
    if pexels_key:
        generator.set_pexels_api_key(pexels_key)
        use_pexels = True
        print("Will use Pexels stock footage")
    else:
        print("Will create text-based video (no API key needed)")

    # Generate video
    output_path = generator.generate_video(script, use_pexels=use_pexels)

    print(f"\n🎬 Your BeanFlow pitch video is ready at:\n   {output_path}")


if __name__ == "__main__":
    main()
