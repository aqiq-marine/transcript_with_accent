from __future__ import annotations
import copy, json, os, re, subprocess, tkinter as tk
from dataclasses import dataclass, asdict
from pathlib import Path
from tkinter import ttk
from uuid import uuid4

@dataclass
class Segment:
    text: str
    reading: str = ""
    accents: list[int] | None = None
    phrase_breaks: list[int] | None = None

def transcribe(audio: str | None, text: str | None) -> str:
    if text: return text
    if not audio: return ""
    key = os.getenv("GEMINI_API_KEY")
    if not key: raise RuntimeError("GEMINI_API_KEY が未設定です。--textで文字列を指定してください。")
    try:
        from google import genai
        client = genai.Client(api_key=key)
        uploaded = client.files.upload(file=audio)
        result = client.models.generate_content(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), contents=[uploaded, "日本語音声を文字起こしし、本文だけを返してください。"])
        return result.text.strip()
    except ImportError as exc: raise RuntimeError("Gemini利用には google-genai をインストールしてください。") from exc

def reading_with_openjtalk(text: str) -> str:
    try:
        import pyopenjtalk
        return pyopenjtalk.g2p(text, kana=True)
    except ImportError:
        try: subprocess.run([os.getenv("OPEN_JTALK", "open_jtalk"), "-h"], capture_output=True, check=False)
        except OSError: pass
        return text

def analyze_accent(reading: str) -> tuple[list[int], list[int]]:
    chunks = [c for c in re.split(r"[、。！？,.!?]+", reading) if c]
    accents, breaks, pos = [], [], 0
    for chunk in chunks:
        mora = re.findall(r"[ァ-ヶー]+", chunk) or list(chunk)
        if mora: accents.append(pos + 1); pos += len(mora); breaks.append(pos)
    return accents, breaks

def _sample_project() -> dict | None:
    """Use a project saved by the target VOICEVOX version as a schema template."""
    for candidate in (Path("data/sample.vvproj"), Path(__file__).parents[2] / "data/sample.vvproj"):
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return None

def make_vvproj(segments: list[Segment], speaker: int = 3) -> dict:
    template = _sample_project()
    if template is None:
        raise RuntimeError("VOICEVOXの正しい雛形 data/sample.vvproj が必要です。")
    project = copy.deepcopy(template)
    talk = project["talk"]
    source_key = talk["audioKeys"][0]
    source_item = talk["audioItems"][source_key]
    talk["audioKeys"] = []
    talk["audioItems"] = {}
    for segment in segments:
        key = str(uuid4())
        item = copy.deepcopy(source_item)
        item["text"] = segment.text
        item["voice"]["styleId"] = speaker
        # Keep the valid AudioQuery shape. The confirmed reading and analysis are
        # retained in metadata; query refinement can be connected to Engine later.
        item["query"]["kana"] = segment.reading
        talk["audioKeys"].append(key)
        talk["audioItems"][key] = item
    project["metadata"] = {"transcriptWithAccent": [asdict(s) for s in segments]}
    return project

class ReviewWindow:
    def __init__(self, segments):
        self.segments, self.root, self.entries = segments, tk.Tk(), []
        self.root.title("文字起こし・読み確認（MVP）")
        frame = ttk.Frame(self.root, padding=12); frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="本文").grid(row=0, column=0); ttk.Label(frame, text="読み（カタカナ）").grid(row=0, column=1)
        for row, s in enumerate(segments, 1):
            a, b = ttk.Entry(frame, width=55), ttk.Entry(frame, width=55); a.insert(0, s.text); b.insert(0, s.reading)
            a.grid(row=row, column=0, padx=4, pady=3); b.grid(row=row, column=1, padx=4, pady=3); self.entries.append((a, b))
        ttk.Button(frame, text="確定して保存へ", command=self.accept).grid(row=len(segments)+1, column=0, columnspan=2, pady=10); self.accepted = False
    def accept(self):
        for s, (a, b) in zip(self.segments, self.entries): s.text, s.reading = a.get().strip(), b.get().strip()
        self.accepted = True; self.root.destroy()
    def run(self): self.root.mainloop(); return self.accepted

def run_pipeline(audio, output, text=None, gui=True):
    raw = transcribe(audio, text)
    segments = [Segment(t.strip(), reading_with_openjtalk(t.strip())) for t in re.split(r"\n|(?<=[。！？])", raw) if t.strip()]
    if not segments: raise RuntimeError("文字起こし結果が空です。")
    if gui and not ReviewWindow(segments).run(): return
    for s in segments: s.accents, s.phrase_breaks = analyze_accent(s.reading)
    Path(output).write_text(json.dumps(make_vvproj(segments), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {output}")
