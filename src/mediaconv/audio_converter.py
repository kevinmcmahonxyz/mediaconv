"""
Audio conversion module for mediaconv.

Handles conversions from compressed audio formats to WAV.
"""

from pathlib import Path
from pydub import AudioSegment


def convert_mp3_to_wav(input_path: str, output_path: str) -> None:
    """
    Convert an MP3 file to WAV format.
    
    WAV is uncompressed - this doesn't restore MP3's lost quality,
    just changes the container format.
    
    Args:
        input_path: Path to the input MP3 file
        output_path: Path where the WAV file will be saved
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a valid MP3
        IOError: If there's an error during conversion
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() != '.mp3':
        raise ValueError(f"Input file must be an MP3, got: {input_file.suffix}")
    
    try:
        # Load the MP3 file
        # pydub uses FFmpeg under the hood
        audio = AudioSegment.from_mp3(str(input_file))
        
        # Export as WAV
        # Default settings: 16-bit, original sample rate, original channels
        audio.export(str(output_file), format='wav')
        
    except Exception as e:
        raise IOError(f"Error converting {input_path} to WAV: {str(e)}") from e