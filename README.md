# transcript_with_accent

日本語音声の文字起こし、読みの人手確認、Gemini + F0 によるアクセント句/H-L推定、VOICEVOXによる音声合成を支援するプロジェクトです。

## Project status

初期設計段階です。推定された読み・アクセント句・H/Lは、確認前の候補として扱います。音声から得た推定値を正解ラベルとみなさず、人間によるレビューと修正履歴を保持します。

## Documentation

- [Docs index](docs/README.md)
- [Agent instructions](docs/AGENTS.md)
- [Architecture Decision Records](docs/adr/README.md)

## Intended workflow

1. Geminiで音声を文字起こしする
2. 辞書・モデルで読みを推定し、人間が確認・確定する
3. 確定したテキスト・読みと元音声を使い、Geminiがアクセント句とH/Lの候補を提案する
4. F0抽出結果で音響的な手がかりを補助し、推定を比較・レビューする
5. 人間がアクセント句・H/Lを修正する
6. VOICEVOX Engineで音声を合成し、必要に応じて結果を確認する

## Principles

- 原音声、文字起こし、確定した読み、韻律推定、手動修正を別々に保持する
- 読みとモーラ列の対応が確定する前に、モーラ単位のF0ラベルを確定しない
- 不確実なラベルは無理に二値化せず、レビュー待ちとして扱う
- VOICEVOX固有のデータ形式を正規の保存形式にしない。エンジン連携はアダプターとして扱う
- APIキーや個人情報をリポジトリにコミットしない
