"""
Image conversion module for mediaconv.

Handles conversions from modern image formats (WebP, AVIF, SVG) to PNG.
"""

from pathlib import Path
from PIL import Image
import pillow_avif  # This import registers AVIF support with Pillow
import cairosvg

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

# At the top, add this import after the PIL import
import pillow_avif  # This import registers AVIF support with Pillow


# Add this new function after convert_webp_to_png
def convert_avif_to_png(input_path: str, output_path: str) -> None:
    """
    Convert an AVIF image to PNG format.
    
    AVIF (AV1 Image File Format) is a modern image format with better
    compression than WebP. It's becoming more common but not universally supported.
    
    Args:
        input_path: Path to the input AVIF file
        output_path: Path where the PNG file will be saved
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a valid AVIF image
        IOError: If there's an error reading or writing the file
        
    Example:
        >>> convert_avif_to_png('photo.avif', 'photo.png')
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() != '.avif':
        raise ValueError(f"Input file must be an AVIF image, got: {input_file.suffix}")
    
    try:
        # The pillow_avif import above registered AVIF support
        # Now Pillow knows how to open AVIF files automatically
        with Image.open(input_file) as img:
            
            # AVIF can also be RGB or RGBA, same as WebP
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            
            img.save(output_file, 'PNG')
            
    except Exception as e:
        raise IOError(f"Error converting {input_path} to PNG: {str(e)}") from e

def convert_svg_to_png(
    input_path: str,
    output_path: str,
    width: int = None,
    height: int = None,
    scale: float = 1.0
) -> None:
    """
    Convert an SVG (vector) image to PNG (raster) format.
    
    SVG files don't have a fixed pixel size - they're mathematical descriptions
    that can scale infinitely. You need to specify the output dimensions.
    
    Args:
        input_path: Path to the input SVG file
        output_path: Path where the PNG file will be saved
        width: Output width in pixels (optional)
        height: Output height in pixels (optional)
        scale: Scale factor for default SVG size (default: 1.0)
        
    Note:
        - If width and height are both None, uses SVG's default size * scale
        - If only width is set, height scales proportionally
        - If only height is set, width scales proportionally
        - If both are set, uses those exact dimensions (may distort)
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a valid SVG image
        IOError: If there's an error reading or writing the file
        
    Examples:
        >>> # Use SVG's default size
        >>> convert_svg_to_png('logo.svg', 'logo.png')
        
        >>> # Specify exact dimensions
        >>> convert_svg_to_png('logo.svg', 'logo.png', width=512, height=512)
        
        >>> # Scale up 2x from default size
        >>> convert_svg_to_png('logo.svg', 'logo.png', scale=2.0)
        
        >>> # Width only (height scales proportionally)
        >>> convert_svg_to_png('logo.svg', 'logo.png', width=1920)
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() not in ['.svg', '.svgz']:
        raise ValueError(f"Input file must be an SVG image, got: {input_file.suffix}")
    
    try:
        # cairosvg handles the conversion
        # WHY use url= instead of file_obj: cairosvg needs the path for relative references
        # (SVG files can reference other files, like embedded images or fonts)
        cairosvg.svg2png(
            url=str(input_file),
            write_to=str(output_file),
            output_width=width,
            output_height=height,
            scale=scale,
        )
        
    except Exception as e:
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