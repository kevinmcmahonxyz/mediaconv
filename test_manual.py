#!/usr/bin/env python3
"""
Manual test script for WebP to PNG conversion.

This is for quick testing during development.
Run with: python test_manual.py
"""

import sys
from pathlib import Path

# Add src to path so we can import our module
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from mediaconv.image_converter import convert_webp_to_png, get_image_info


def test_conversion():
    """Test the WebP to PNG conversion with a sample file."""
    
    # You'll need to provide a test WebP file
    input_file = 'test_image.webp'
    output_file = 'test_output.png'
    
    print(f"🔍 Testing WebP to PNG conversion")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print()
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"❌ Error: {input_file} not found!")
        print(f"   Please place a WebP image in the current directory.")
        return
    
    try:
        # Get info about the input image
        print("📊 Input image info:")
        info = get_image_info(input_file)
        for key, value in info.items():
            print(f"   {key}: {value}")
        print()
        
        # Perform the conversion
        print("🔄 Converting...")
        convert_webp_to_png(input_file, output_file)
        
        # Get info about the output image
        print("✅ Conversion successful!")
        print("📊 Output image info:")
        info = get_image_info(output_file)
        for key, value in info.items():
            print(f"   {key}: {value}")
        
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
    except ValueError as e:
        print(f"❌ Validation error: {e}")
    except IOError as e:
        print(f"❌ Conversion error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == '__main__':
    test_conversion()