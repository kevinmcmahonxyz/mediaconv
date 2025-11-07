"""
Command-line interface for mediaconv.

Simple usage: mediaconv input.webp output.png
Auto output: mediaconv input.webp (creates input.png)
Interactive: mediaconv (prompts for files)
"""

import click
from pathlib import Path
from .image_converter import (
    convert_webp_to_png,
    convert_avif_to_png,
    convert_svg_to_png,
)
from .audio_converter import (
    convert_mp3_to_wav,
    convert_mp4_to_wav,
    convert_m4a_to_wav,
)


# Mapping of input extension to output extension
OUTPUT_EXTENSIONS = {
    '.webp': '.png',
    '.avif': '.png',
    '.svg': '.png',
    '.mp3': '.wav',
    '.mp4': '.wav',
    '.m4a': '.wav',
}

# Mapping of (input_ext, output_ext) to conversion function
CONVERTERS = {
    ('.webp', '.png'): convert_webp_to_png,
    ('.avif', '.png'): convert_avif_to_png,
    ('.svg', '.png'): convert_svg_to_png,
    ('.mp3', '.wav'): convert_mp3_to_wav,
    ('.mp4', '.wav'): convert_mp4_to_wav,
    ('.m4a', '.wav'): convert_m4a_to_wav,
}


def auto_generate_output_path(input_path: Path) -> Path:
    """
    Generate output path by replacing input extension with appropriate output extension.
    
    Examples:
        image.webp -> image.png
        song.mp3 -> song.wav
    """
    input_ext = input_path.suffix.lower()
    
    if input_ext not in OUTPUT_EXTENSIONS:
        return None
    
    output_ext = OUTPUT_EXTENSIONS[input_ext]
    return input_path.with_suffix(output_ext)

def get_safe_output_path(output_path: Path) -> Path:
    """
    Check if output file exists, append (1), (2), etc. if needed.
    
    Examples:
        image.png exists -> image (1).png
        image (1).png exists -> image (2).png
    """
    if not output_path.exists():
        return output_path
    
    # File exists, need to find a unique name
    stem = output_path.stem  # filename without extension
    suffix = output_path.suffix  # .png, .wav, etc.
    parent = output_path.parent
    
    counter = 1
    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_path = parent / new_name
        
        if not new_path.exists():
            return new_path
        
        counter += 1

@click.command()
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.argument('output_file', type=click.Path(), required=False)
def cli(input_file, output_file):
    """
    Convert media files between formats.
    
    Supports:
      - Images: WebP, AVIF, SVG → PNG
      - Audio: MP3, MP4, M4A → WAV
    
    Examples:
        mediaconv image.webp image.png    # Specify output
        mediaconv image.webp              # Auto-generate output (image.png)
        mediaconv                         # Interactive mode
    """
    # Interactive mode if no arguments
    if input_file is None:
        click.echo("🎯 Interactive Mode")
        click.echo()
        input_file = click.prompt("Input file path")
        
        # Validate input exists
        if not Path(input_file).exists():
            click.echo(f"❌ Error: File not found: {input_file}", err=True)
            raise click.Abort()
    
    input_path = Path(input_file)
    
    # Auto-generate output if not provided
    if output_file is None:
        output_path = auto_generate_output_path(input_path)
        if output_path is None:
            click.echo(f"❌ Error: Unsupported input format: {input_path.suffix}", err=True)
            click.echo(f"\nSupported formats:", err=True)
            click.echo(f"  Images: .webp, .avif, .svg", err=True)
            click.echo(f"  Audio: .mp3, .mp4, .m4a", err=True)
            raise click.Abort()
        
        click.echo(f"📝 Auto-generating output: {output_path.name}")
    else:
        output_path = Path(output_file)
    
    # Get file extensions
    input_ext = input_path.suffix.lower()
    output_ext = output_path.suffix.lower()
    
    # Find the right converter
    converter_key = (input_ext, output_ext)
    
    if converter_key not in CONVERTERS:
        click.echo(f"❌ Error: Unsupported conversion {input_ext} → {output_ext}", err=True)
        click.echo(f"\nSupported conversions:", err=True)
        click.echo(f"  Images → PNG: .webp, .avif, .svg", err=True)
        click.echo(f"  Audio → WAV: .mp3, .mp4, .m4a", err=True)
        raise click.Abort()
    
    # Do the conversion
    converter = CONVERTERS[converter_key]
    
    try:
        # Check if output exists and find safe name
        safe_output_path = get_safe_output_path(output_path)
        
        if safe_output_path != output_path:
            click.echo(f"⚠️  Output file exists, using: {safe_output_path.name}")
        
        click.echo(f"🔄 Converting {input_path.name} → {safe_output_path.name}...")
        converter(str(input_path), str(safe_output_path))
        click.echo(f"✅ Success! Saved to: {safe_output_path}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()