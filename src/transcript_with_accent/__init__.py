"""Japanese transcription, reading review, accent analysis and vvproj export."""
from .pipeline import run_pipeline

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", nargs="?")
    parser.add_argument("-o", "--output", default="output.vvproj")
    parser.add_argument("--text")
    parser.add_argument("--no-gui", action="store_true")
    args = parser.parse_args()
    run_pipeline(args.audio, args.output, args.text, not args.no_gui)
