"""
Image conversion module for mediaconv.

Handles conversions from modern image formats (WebP, AVIF, SVG) to PNG.
"""

from pathlib import Path
from PIL import Image


def convert_webp_to_png(input_path: str, output_path: str) -> None:
    """
    Convert a WebP image to PNG format.
    
    Args:
        input_path: Path to the input WebP file
        output_path: Path where the PNG file will be saved
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a valid WebP image
        IOError: If there's an error reading or writing the file
        
    Example:
        >>> convert_webp_to_png('photo.webp', 'photo.png')
    """
    # Convert strings to Path objects for better path handling
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    # Validate input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Validate input file is actually a WebP
    if input_file.suffix.lower() != '.webp':
        raise ValueError(f"Input file must be a WebP image, got: {input_file.suffix}")
    
    try:
        # Open the image using a context manager
        # WHY: Context managers (with statement) automatically close the file
        # even if an error occurs, preventing memory leaks
        with Image.open(input_file) as img:
            
            # Check the image mode
            # WHY: WebP can be RGB (no transparency) or RGBA (with transparency)
            # PNG supports both modes, so we need to preserve transparency if it exists
            # Other modes like 'P' (palette) or 'L' (grayscale) should be converted
            if img.mode not in ('RGB', 'RGBA'):
                # Convert to RGBA to be safe (supports transparency)
                img = img.convert('RGBA')
            
            # Save as PNG
            # WHY: PNG format is specified explicitly to ensure correct output
            # Pillow determines format from extension, but being explicit is safer
            img.save(output_file, 'PNG')
            
    except Exception as e:
        # Catch any PIL-specific errors and provide helpful context
        raise IOError(f"Error converting {input_path} to PNG: {str(e)}") from e


def get_image_info(image_path: str) -> dict:
    """
    Get information about an image file.
    
    Useful for debugging and understanding what you're working with.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing image information (format, size, mode)
        
    Example:
        >>> info = get_image_info('photo.webp')
        >>> print(f"Size: {info['size']}, Mode: {info['mode']}")
    """
    image_file = Path(image_path)
    
    if not image_file.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    with Image.open(image_file) as img:
        return {
            'format': img.format,  # e.g., 'WEBP', 'PNG', 'JPEG'
            'size': img.size,      # (width, height) in pixels
            'mode': img.mode,      # e.g., 'RGB', 'RGBA', 'L'
            'width': img.width,
            'height': img.height,
        }