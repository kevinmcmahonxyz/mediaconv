"""
Command-line interface for mediaconv.

Simple usage: mediaconv input.webp output.png
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


# Mapping of (input_ext, output_ext) to conversion function
CONVERTERS = {
    ('.webp', '.png'): convert_webp_to_png,
    ('.avif', '.png'): convert_avif_to_png,
    ('.svg', '.png'): convert_svg_to_png,
    ('.mp3', '.wav'): convert_mp3_to_wav,
    ('.mp4', '.wav'): convert_mp4_to_wav,
    ('.m4a', '.wav'): convert_m4a_to_wav,
}


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def cli(input_file, output_file):
    """
    Convert media files between formats.
    
    Supports:
      - Images: WebP, AVIF, SVG → PNG
      - Audio: MP3, MP4, M4A → WAV
    
    Example:
        mediaconv image.webp image.png
        mediaconv song.mp3 song.wav
    """
    input_path = Path(input_file)
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
        click.echo(f"🔄 Converting {input_path.name} → {output_path.name}...")
        converter(str(input_path), str(output_path))
        click.echo(f"✅ Success! Saved to: {output_path}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()