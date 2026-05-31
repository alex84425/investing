"""
Fetch YouTube transcript and print it to stdout.
Fallback: if subtitles are disabled, download audio via yt-dlp and transcribe with Whisper.
Usage: uv run python .github/skills/yt-summary/script/get_transcript.py <youtube_url>
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def try_transcript_api(video_id: str) -> tuple[str, str, int] | None:
    """Try youtube-transcript-api. Returns (full_text, language, entry_count) or None."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            NoTranscriptFound,
            TranscriptsDisabled,
        )
    except ImportError:
        return None

    try:
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.list(video_id)
        preferred = ["zh-TW", "zh-Hant", "zh", "en"]
        transcript = None
        for lang in preferred:
            try:
                transcript = transcript_list.find_transcript([lang])
                break
            except Exception:
                continue
        if transcript is None:
            transcript = transcript_list.find_transcript([t.language_code for t in transcript_list])

        fetched = transcript.fetch()
        lines = []
        for entry in fetched:
            start = entry.start
            text = entry.text.replace("\n", " ")
            minutes = int(start // 60)
            seconds = int(start % 60)
            lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")

        return "\n".join(lines), transcript.language_code, len(fetched)
    except TranscriptsDisabled, NoTranscriptFound:
        return None
    except Exception:
        return None


def whisper_fallback(url: str, video_id: str) -> tuple[str, str, int]:
    """Download audio with yt-dlp, transcribe with Whisper."""
    print("INFO: No subtitles available. Falling back to Whisper transcription...", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = Path(tmpdir) / f"{video_id}.mp3"

        # Download audio
        result = subprocess.run(
            ["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "5", "-o", str(mp3_path).replace(".mp3", ".%(ext)s"), url],
            capture_output=True,
            text=True,
        )
        # yt-dlp may output to .mp3 directly or via conversion
        if not mp3_path.exists():
            # Check for webm -> mp3 conversion output
            for f in Path(tmpdir).glob(f"{video_id}.*"):
                if f.suffix == ".mp3":
                    mp3_path = f
                    break
        if not mp3_path.exists():
            print(f"ERROR: yt-dlp failed to download audio.\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        print("INFO: Audio downloaded. Transcribing with Whisper (this may take a few minutes)...", file=sys.stderr)

        # Transcribe with Whisper
        import whisper

        model = whisper.load_model("base")
        transcription = model.transcribe(str(mp3_path), language="zh")

        segments = transcription.get("segments", [])
        if segments:
            lines = []
            for seg in segments:
                start = seg["start"]
                text = seg["text"].strip()
                minutes = int(start // 60)
                seconds = int(start % 60)
                lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")
            return "\n".join(lines), "zh (whisper)", len(segments)
        else:
            # No segments, return raw text
            text = transcription.get("text", "")
            return text, "zh (whisper)", 1


def main():
    if len(sys.argv) < 2:
        print("Usage: get_transcript.py <youtube_url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)
    if not video_id:
        print(f"ERROR: Cannot extract video ID from URL: {url}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Try transcript API
    result = try_transcript_api(video_id)

    # Step 2: Fallback to Whisper if no transcript
    if result is None:
        try:
            result = whisper_fallback(url, video_id)
        except Exception as e:
            print(f"ERROR: Whisper fallback failed: {e}", file=sys.stderr)
            sys.exit(1)

    full_text, language, entry_count = result
    # Ensure stdout handles UTF-8
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(f"VIDEO_ID: {video_id}")
    print(f"URL: {url}")
    print(f"LANGUAGE: {language}")
    print(f"ENTRY_COUNT: {entry_count}")
    print("---TRANSCRIPT---")
    print(full_text)


if __name__ == "__main__":
    main()
