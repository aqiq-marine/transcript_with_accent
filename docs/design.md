# Initial System Design

## Pipeline

1. **Transcription** — Gemini generates a transcript draft from source audio.
2. **Reading review** — a human confirms the pronunciation of the written text. This is a gate before prosody analysis.
3. **Prosody proposal** — Gemini receives source audio, confirmed text, and confirmed reading, then proposes mora-level H/L and accent-phrase boundaries.
4. **Acoustic analysis** — F0 is extracted and aligned with speech/mora intervals when alignment becomes available.
5. **Review** — humans inspect the proposed labels, F0 contour, and boundaries; uncertain values remain unresolved.
6. **Canonical annotation** — the reviewed text, reading, mora segmentation, accent-phrase boundaries, H/L labels, provenance, and review state are stored in an engine-independent model.
7. **VOICEVOX project export** — a converter maps the canonical annotation into a `.vvproj` project that can be opened by the VOICEVOX editor.
8. **Editor review and synthesis** — the user opens the generated project in the VOICEVOX editor, checks or adjusts the imported reading/accent, and performs synthesis in the editor.

## Separation of concerns

- **Gemini**: linguistic/audio-informed proposals, not ground truth.
- **F0 extractor**: acoustic measurements and supporting evidence, not phrase-boundary truth by itself.
- **Human reviewer**: final authority for reading and annotation.
- **Canonical annotation store**: keeps source, prediction, correction, and provenance.
- **VOICEVOX project exporter**: converts canonical annotations to the editor's `.vvproj` project format.
- **VOICEVOX editor**: final manual review, editing, playback, and synthesis.

## VOICEVOX integration boundary

The intended deliverable for the synthesis stage is a `.vvproj` file that the user can open in the VOICEVOX editor. The editor, rather than this application, remains the place where final synthesis is performed.

The standard VOICEVOX Engine API provides synthesis-related operations such as creating an AudioQuery and synthesizing audio. Sending text or an AudioQuery to the Engine does not itself create or synchronize a project in the editor GUI. Therefore, the project exporter is a separate component and must follow the editor's project-file schema and loading behavior.

Treat the `.vvproj` schema as version-sensitive unless the editor provides a stable public compatibility guarantee. Start with a minimal project saved by the target VOICEVOX version, compare it with the editor's schema and migration/loading code, then test generated files by opening them in that version. Do not claim compatibility until verified.

VOICEVOX-specific fields belong in the export adapter, not in the canonical annotation schema. If a canonical pitch contour cannot be represented exactly by VOICEVOX's accent and mora model, preserve it in the canonical annotation and document the limitation rather than silently discarding it.

## Important caveats

- F0 is undefined or unreliable in unvoiced segments and may contain octave errors.
- Absolute pitch varies by speaker and speaking style; H/L should use a documented relative criterion.
- F0 frames cannot be assigned to moras reliably without temporal alignment.
- Prosodic phrase boundaries cannot be inferred from pauses alone.
- Synthesized audio will not necessarily reproduce the original speaker's exact prosody.
- A canonical H/L contour and VOICEVOX's accent-kernel/pitch representation are not necessarily equivalent; the conversion must be tested and may be lossy.
