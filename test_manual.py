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
    get_image_info
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


if __name__ == '__main__':
    test_webp()
    test_avif()