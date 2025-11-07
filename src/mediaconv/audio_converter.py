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
    
def convert_mp4_to_wav(input_path: str, output_path: str) -> None:
    """
    Convert an MP4 file to WAV format (extracts audio track).
    
    MP4 is a container format that typically holds video + audio.
    This extracts only the audio track and converts it to WAV.
    
    Args:
        input_path: Path to the input MP4 file
        output_path: Path where the WAV file will be saved
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a valid MP4
        IOError: If there's an error during conversion
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() not in ['.mp4', '.m4v']:
        raise ValueError(f"Input file must be an MP4, got: {input_file.suffix}")
    
    try:
        # Load MP4 and extract audio
        audio = AudioSegment.from_file(str(input_file), format='mp4')
        audio.export(str(output_file), format='wav')
        
    except Exception as e:
        raise IOError(f"Error converting {input_path} to WAV: {str(e)}") from e


def convert_m4a_to_wav(input_path: str, output_path: str) -> None:
    """
    Convert an M4A file to WAV format.
    
    M4A is MPEG-4 Audio (same as MP4 but audio-only).
    Common format for iTunes and Apple Music downloads.
    
    Args:
        input_path: Path to the input M4A file
        output_path: Path where the WAV file will be saved
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a valid M4A
        IOError: If there's an error during conversion
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() != '.m4a':
        raise ValueError(f"Input file must be an M4A, got: {input_file.suffix}")
    
    try:
        # Load M4A file
        audio = AudioSegment.from_file(str(input_file), format='m4a')
        audio.export(str(output_file), format='wav')
        
    except Exception as e:
        raise IOError(f"Error converting {input_path} to WAV: {str(e)}") from e