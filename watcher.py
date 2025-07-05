import os
import subprocess
import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

WATCH_DIR = os.environ.get("WATCH_DIR", "/media")
TRIGGER_SCRIPT = os.environ.get("TRIGGER_SCRIPT", "/scripts/trigger-jf-lib-scan.sh")

SUBTITLE_LANGS = ['nl', 'fr', 'en']  # Subtitle languages to check
SUB_EXT = ".srt"

def all_subtitles_exist(base_path):
    """Check if all subtitle files exist for the given base path."""
    for lang in SUBTITLE_LANGS:
        if not os.path.exists(f"{base_path}.{lang}{SUB_EXT}"):
            return False
    return True

class SubtitlesHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        # We only care about .srt files with the right lang suffix
        if not filepath.endswith(SUB_EXT):
            return
        base, ext = os.path.splitext(filepath)
        # Check if filename ends with a language suffix from the list
        if any(base.endswith(f".{lang}") for lang in SUBTITLE_LANGS):
            # Remove language suffix to get the common base media filename
            for lang in SUBTITLE_LANGS:
                suffix = f".{lang}"
                if base.endswith(suffix):
                    media_base = base[:-len(suffix)]
                    break
            else:
                return
            if all_subtitles_exist(media_base):
                print(f"[watchdog] Complete subtitle set detected for {media_base}, triggering scan")
                try:
                    subprocess.run([TRIGGER_SCRIPT], check=True)
                    print("[watchdog] Scan triggered successfully")
                except subprocess.CalledProcessError as e:
                    print(f"[watchdog] Failed to trigger scan: {e}")

if __name__ == "__main__":
    event_handler = SubtitlesHandler()
    observer = PollingObserver()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    print(f"[watchdog] Watching {WATCH_DIR} for subtitle sets...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()