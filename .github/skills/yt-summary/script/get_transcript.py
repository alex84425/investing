"""
Fetch YouTube transcript and print it to stdout.
Usage: uv run python .github/skills/yt-summary/script/get_transcript.py <youtube_url>
"""

import sys
import re
import json


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: get_transcript.py <youtube_url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)
    if not video_id:
        print(f"ERROR: Cannot extract video ID from URL: {url}", file=sys.stderr)
        sys.exit(1)

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    except ImportError:
        print("ERROR: youtube-transcript-api not installed. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    try:
        ytt = YouTubeTranscriptApi()
        # Try to get transcript; prefer zh-TW/zh/en order
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
            # Fall back to first available
            transcript = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            )

        fetched = transcript.fetch()
        # Format: plain text with timestamps
        lines = []
        for entry in fetched:
            start = entry.start
            text = entry.text.replace("\n", " ")
            minutes = int(start // 60)
            seconds = int(start % 60)
            lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")

        full_text = "\n".join(lines)
        print(f"VIDEO_ID: {video_id}")
        print(f"URL: {url}")
        print(f"LANGUAGE: {transcript.language_code}")
        print(f"ENTRY_COUNT: {len(fetched)}")
        print("---TRANSCRIPT---")
        print(full_text)

    except TranscriptsDisabled:
        print("ERROR: Transcripts are disabled for this video.", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print("ERROR: No transcript found for this video.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
