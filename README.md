# mediaconv - Media Format Converter

A simple command-line tool to convert modern media formats to universal formats.

## Supported Conversions

### Images → PNG
- WebP → PNG
- AVIF → PNG
- SVG → PNG

### Audio → WAV
- MP3 → WAV
- MP4 → WAV (audio extraction)
- M4A → WAV

## Installation

### Prerequisites

- Python 3.10 or higher
- FFmpeg (for audio conversions)

#### Installing FFmpeg

**Ubuntu/Debian (WSL2):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget`:
```bash
winget install ffmpeg
```

### Setup
```bash
# Clone the repository
git clone https://github.com/kevinmcmahonxyz/mediaconv.git
cd mediaconv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### Activate Environment (Each Session)
```bash
cd /path/to/mediaconv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Convert Files

**Specify output path:**
```bash
mediaconv input.webp output.png
mediaconv song.mp3 song.wav
```

**Auto-generate output path:**
```bash
mediaconv image.webp
# Creates: image.png

mediaconv audio.mp3
# Creates: audio.wav
```

**Interactive mode:**
```bash
mediaconv
# Prompts you for input file path
```

### Features

- ✅ **Auto-output generation** - Just provide input file, output is created automatically
- ✅ **Duplicate file handling** - Appends (1), (2), etc. if output file exists
- ✅ **Interactive mode** - Run without arguments for prompts
- ✅ **Smart format detection** - Automatically picks the right converter

## Examples
```bash
# Convert downloaded WebP images to PNG
mediaconv ~/Downloads/screenshot.webp

# Extract audio from MP4 video
mediaconv video.mp4 audio.wav

# Convert SVG logo to PNG at default size
mediaconv logo.svg logo.png

# Interactive mode
mediaconv
> Input file path: /mnt/c/Users/kpmcm/Downloads/photo.avif
📝 Auto-generating output: photo.png
🔄 Converting photo.avif → photo.png...
✅ Success! Saved to: photo.png
```

## Development

### Running Tests

Manual testing script included for development:
```bash
python test_manual.py
```

Requires test files in the project directory:
- `test_image.webp`
- `test_image.avif` 
- `test_image.svg`
- `test_audio.mp3`
- `test_audio.m4a`
- `test_video.mp4`

### Project Structure
```
mediaconv/
├── src/
│   └── mediaconv/
│       ├── __init__.py
│       ├── cli.py              # Click-based CLI
│       ├── image_converter.py  # Image conversion logic
│       └── audio_converter.py  # Audio conversion logic
├── requirements.txt            # Python dependencies
├── setup.py                    # Package configuration
├── test_manual.py              # Development testing script
└── README.md
```

## Troubleshooting

### "mediaconv: command not found"

Make sure you've:
1. Activated the virtual environment: `source venv/bin/activate`
2. Installed the package: `pip install -e .`

### "FFmpeg not found" errors

Install FFmpeg using the instructions in the Prerequisites section.

### Permission errors on Windows/WSL2

Accessing Windows files from WSL2:
```bash
# Windows paths are mounted at /mnt/c/
mediaconv /mnt/c/Users/YourUsername/Desktop/file.webp
```

## License

MIT License - See LICENSE file for details

## Author

Kevin McMahon ([@kevinmcmahonxyz](https://github.com/kevinmcmahonxyz))