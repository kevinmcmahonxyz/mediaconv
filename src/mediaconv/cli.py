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
@click.argument('input_files', nargs=-1, type=click.Path())
@click.option('--batch', '-b', type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help='Convert all supported files in a directory')
def cli(input_files, batch):
    """
    Convert media files between formats.
    
    Supports:
      - Images: WebP, AVIF, SVG → PNG
      - Audio: MP3, MP4, M4A → WAV
    
    Examples:
        mediaconv image.webp                    # Single file, auto-output
        mediaconv image.webp output.png         # Single file, specify output
        mediaconv *.webp                        # Batch convert all WebP files
        mediaconv file1.webp file2.avif         # Multiple files
        mediaconv --batch ~/Downloads/images/   # Convert all files in directory
    """
    
    # Batch directory mode
    if batch:
        batch_path = Path(batch)
        click.echo(f"🔍 Scanning directory: {batch_path}")
        
        # Find all supported files
        supported_extensions = list(OUTPUT_EXTENSIONS.keys())
        files_to_convert = []
        
        for ext in supported_extensions:
            files_to_convert.extend(batch_path.glob(f"*{ext}"))
        
        if not files_to_convert:
            click.echo(f"❌ No supported files found in {batch_path}", err=True)
            click.echo(f"   Supported: {', '.join(supported_extensions)}", err=True)
            return
        
        click.echo(f"📦 Found {len(files_to_convert)} file(s) to convert")
        click.echo()
        
        # Convert each file
        for input_path in files_to_convert:
            output_path = auto_generate_output_path(input_path)
            convert_single_file(input_path, output_path)
        
        click.echo()
        click.echo(f"✅ Batch conversion complete! Converted {len(files_to_convert)} file(s)")
        return
    
    # No arguments - interactive mode
    if not input_files:
        click.echo("🎯 Interactive Mode")
        click.echo()
        input_file = click.prompt("Input file path")
        
        if not Path(input_file).exists():
            click.echo(f"❌ Error: File not found: {input_file}", err=True)
            raise click.Abort()
        
        input_files = (input_file,)
    
    # Single file with explicit output
    if len(input_files) == 2:
        input_path = Path(input_files[0])
        output_path = Path(input_files[1])
        
        if not input_path.exists():
            click.echo(f"❌ Error: File not found: {input_path}", err=True)
            raise click.Abort()
        
        convert_single_file(input_path, output_path)
        return
    
    # Multiple files or single file with auto-output
    if len(input_files) >= 1:
        # Check if any files don't exist (before processing)
        missing_files = [f for f in input_files if not Path(f).exists()]
        if missing_files:
            click.echo(f"❌ Error: File(s) not found:", err=True)
            for f in missing_files:
                click.echo(f"   - {f}", err=True)
            raise click.Abort()
        
        # Multiple files - batch mode
        if len(input_files) > 1:
            click.echo(f"📦 Converting {len(input_files)} file(s)...")
            click.echo()
        
        for input_file in input_files:
            input_path = Path(input_file)
            output_path = auto_generate_output_path(input_path)
            
            if output_path is None:
                click.echo(f"⏭️  Skipping {input_path.name}: Unsupported format", err=True)
                continue
            
            convert_single_file(input_path, output_path)
        
        if len(input_files) > 1:
            click.echo()
            click.echo(f"✅ Batch conversion complete!")
        
        return


def convert_single_file(input_path: Path, output_path: Path):
    """Helper function to convert a single file."""
    input_ext = input_path.suffix.lower()
    output_ext = output_path.suffix.lower()
    
    # Find the right converter
    converter_key = (input_ext, output_ext)
    
    if converter_key not in CONVERTERS:
        click.echo(f"❌ Error: Unsupported conversion {input_ext} → {output_ext}", err=True)
        return
    
    converter = CONVERTERS[converter_key]
    
    try:
        # Check if output exists and find safe name
        safe_output_path = get_safe_output_path(output_path)
        
        if safe_output_path != output_path:
            click.echo(f"⚠️  {input_path.name}: Output exists, using {safe_output_path.name}")
        
        click.echo(f"🔄 {input_path.name} → {safe_output_path.name}...")
        converter(str(input_path), str(safe_output_path))
        click.echo(f"✅ {safe_output_path.name}")
        
    except Exception as e:
        click.echo(f"❌ {input_path.name}: {e}", err=True)

if __name__ == '__main__':
    cli()