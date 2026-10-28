# Initial System Design

## Pipeline

1. **Transcription** — Gemini generates a transcript draft from source audio.
2. **Reading review** — a human confirms the pronunciation of the written text. This is a gate before prosody analysis.
3. **Prosody proposal** — Gemini receives source audio, confirmed text, and confirmed reading, then proposes mora-level H/L and accent-phrase boundaries.
4. **Acoustic analysis** — F0 is extracted and aligned with speech/mora intervals when alignment becomes available.
5. **Review** — humans inspect the proposed labels, F0 contour, and boundaries; uncertain values remain unresolved.
6. **Synthesis** — the reviewed reading/prosody is adapted to VOICEVOX AudioQuery and synthesized.
7. **Export** — annotations are saved in the engine-independent canonical schema.

## Separation of concerns

- **Gemini**: linguistic/audio-informed proposals, not ground truth.
- **F0 extractor**: acoustic measurements and supporting evidence, not phrase-boundary truth by itself.
- **Human reviewer**: final authority for reading and annotation.
- **VOICEVOX adapter**: converts canonical annotations to engine-specific synthesis requests.
- **Canonical annotation store**: keeps source, prediction, correction, and provenance.

## Important caveats

- F0 is undefined or unreliable in unvoiced segments and may contain octave errors.
- Absolute pitch varies by speaker and speaking style; H/L should use a documented relative criterion.
- F0 frames cannot be assigned to moras reliably without temporal alignment.
- Prosodic phrase boundaries cannot be inferred from pauses alone.
- Synthesized audio will not necessarily reproduce the original speaker's exact prosody.
