#!/usr/bin/env python3
"""
Manual test script for image conversions.

This is for quick testing during development.
Run with: python test_manual.py
"""

import sys
from pathlib import Path

# Add src to path so we can import our module
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from mediaconv.image_converter import (
    convert_webp_to_png,
    convert_avif_to_png,
    convert_svg_to_png,  # Add this
    get_image_info
)

from mediaconv.audio_converter import (
    convert_mp3_to_wav,
    convert_mp4_to_wav,  # Add this
    convert_m4a_to_wav   # Add this
)

def test_webp():
    """Test WebP to PNG conversion."""
    input_file = 'test_image.webp'
    output_file = 'test_output_webp.png'
    
    print("=" * 50)
    print("🔍 Testing WebP to PNG conversion")
    print("=" * 50)
    
    if not Path(input_file).exists():
        print(f"⏭️  Skipping: {input_file} not found")
        return
    
    try:
        print(f"📊 Input: {input_file}")
        info = get_image_info(input_file)
        print(f"   Format: {info['format']}, Size: {info['size']}, Mode: {info['mode']}")
        
        convert_webp_to_png(input_file, output_file)
        
        print(f"✅ Output: {output_file}")
        info = get_image_info(output_file)
        print(f"   Format: {info['format']}, Size: {info['size']}, Mode: {info['mode']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()


def test_avif():
    """Test AVIF to PNG conversion."""
    input_file = 'test_image.avif'
    output_file = 'test_output_avif.png'
    
    print("=" * 50)
    print("🔍 Testing AVIF to PNG conversion")
    print("=" * 50)
    
    if not Path(input_file).exists():
        print(f"⏭️  Skipping: {input_file} not found")
        print(f"   To test AVIF, create one with:")
        print(f"   python -c \"from PIL import Image; import pillow_avif; Image.open('test_image.webp').save('test_image.avif', 'AVIF')\"")
        return
    
    try:
        print(f"📊 Input: {input_file}")
        info = get_image_info(input_file)
        print(f"   Format: {info['format']}, Size: {info['size']}, Mode: {info['mode']}")
        
        convert_avif_to_png(input_file, output_file)
        
        print(f"✅ Output: {output_file}")
        info = get_image_info(output_file)
        print(f"   Format: {info['format']}, Size: {info['size']}, Mode: {info['mode']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

def test_svg():
    """Test SVG to PNG conversion."""
    input_file = 'test_image.svg'
    
    print("=" * 50)
    print("🔍 Testing SVG to PNG conversion")
    print("=" * 50)
    
    if not Path(input_file).exists():
        print(f"⏭️  Skipping: {input_file} not found")
        print(f"   To test SVG, download one from:")
        print(f"   curl -o test_image.svg https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/car.svg")
        return
    
    try:
        # Test 1: Default size
        output1 = 'test_output_svg_default.png'
        print(f"📊 Test 1: Default size")
        convert_svg_to_png(input_file, output1)
        info = get_image_info(output1)
        print(f"   Output: {output1}")
        print(f"   Size: {info['size']}, Mode: {info['mode']}")
        print()
        
        # Test 2: Fixed width (height scales)
        output2 = 'test_output_svg_512w.png'
        print(f"📊 Test 2: Fixed width (512px)")
        convert_svg_to_png(input_file, output2, width=512)
        info = get_image_info(output2)
        print(f"   Output: {output2}")
        print(f"   Size: {info['size']}, Mode: {info['mode']}")
        print()
        
        # Test 3: Scale factor
        output3 = 'test_output_svg_2x.png'
        print(f"📊 Test 3: 2x scale")
        convert_svg_to_png(input_file, output3, scale=2.0)
        info = get_image_info(output3)
        print(f"   Output: {output3}")
        print(f"   Size: {info['size']}, Mode: {info['mode']}")
        print()
        
        # Test 4: Exact dimensions
        output4 = 'test_output_svg_1920x1080.png'
        print(f"📊 Test 4: Exact dimensions (1920x1080)")
        convert_svg_to_png(input_file, output4, width=1920, height=1080)
        info = get_image_info(output4)
        print(f"   Output: {output4}")
        print(f"   Size: {info['size']}, Mode: {info['mode']}")
        
        print()
        print("✅ All SVG tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

def test_mp3():
    """Test MP3 to WAV conversion."""
    input_file = 'test_audio.mp3'
    output_file = 'test_output.wav'
    
    print("=" * 50)
    print("🔍 Testing MP3 to WAV conversion")
    print("=" * 50)
    
    if not Path(input_file).exists():
        print(f"⏭️  Skipping: {input_file} not found")
        print(f"   Place an MP3 file named 'test_audio.mp3' in the project directory")
        return
    
    try:
        print(f"📊 Input: {input_file}")
        print(f"   Size: {Path(input_file).stat().st_size / 1024:.1f} KB")
        
        convert_mp3_to_wav(input_file, output_file)
        
        print(f"✅ Output: {output_file}")
        print(f"   Size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        print(f"   Note: WAV files are much larger (uncompressed)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

def test_mp4():
    """Test MP4 to WAV conversion (audio extraction)."""
    input_file = 'test_video.mp4'
    output_file = 'test_output_mp4.wav'
    
    print("=" * 50)
    print("🔍 Testing MP4 to WAV conversion")
    print("=" * 50)
    
    if not Path(input_file).exists():
        print(f"⏭️  Skipping: {input_file} not found")
        print(f"   Place an MP4 file named 'test_video.mp4' in the project directory")
        return
    
    try:
        print(f"📊 Input: {input_file}")
        print(f"   Size: {Path(input_file).stat().st_size / 1024:.1f} KB")
        
        convert_mp4_to_wav(input_file, output_file)
        
        print(f"✅ Output: {output_file}")
        print(f"   Size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()


def test_m4a():
    """Test M4A to WAV conversion."""
    input_file = 'test_audio.m4a'
    output_file = 'test_output_m4a.wav'
    
    print("=" * 50)
    print("🔍 Testing M4A to WAV conversion")
    print("=" * 50)
    
    if not Path(input_file).exists():
        print(f"⏭️  Skipping: {input_file} not found")
        print(f"   Place an M4A file named 'test_audio.m4a' in the project directory")
        return
    
    try:
        print(f"📊 Input: {input_file}")
        print(f"   Size: {Path(input_file).stat().st_size / 1024:.1f} KB")
        
        convert_m4a_to_wav(input_file, output_file)
        
        print(f"✅ Output: {output_file}")
        print(f"   Size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

if __name__ == '__main__':
    test_webp()
    test_avif()
    test_svg()
    test_mp3()
    test_mp4()
    test_m4a()