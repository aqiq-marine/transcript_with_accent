# transcript_with_accent

日本語音声の文字起こし、読みの人手確認、Gemini + F0 によるアクセント句/H-L推定、VOICEVOXプロジェクトの生成を支援するプロジェクトです。

## Project status

初期設計段階です。推定された読み・アクセント句・H/Lは、確認前の候補として扱います。音声から得た推定値を正解ラベルとみなさず、人間によるレビューと修正履歴を保持します。

## Documentation

- [Docs index](docs/README.md)
- [Agent instructions](docs/AGENTS.md)
- [Architecture Decision Records](docs/adr/README.md)
- [Initial system design](docs/design.md)
- [ADR 0002: VOICEVOX project export](docs/adr/0002-voicevox-project-export.md)

## Intended workflow

1. Geminiで音声を文字起こしする
2. 辞書・モデルで読みを推定し、人間が確認・確定する
3. 確定したテキスト・読みと元音声を使い、Geminiがアクセント句とH/Lの候補を提案する
4. F0抽出結果で音響的な手がかりを補助し、推定を比較・レビューする
5. 人間がアクセント句・H/Lを修正する
6. 正規アノテーションからVOICEVOXの `.vvproj` ファイルを生成する
7. 生成したプロジェクトをVOICEVOXエディターで開き、アクセントを確認・編集して音声を合成する

## Principles

- 原音声、文字起こし、確定した読み、韻律推定、手動修正を別々に保持する
- 読みとモーラ列の対応が確定する前に、モーラ単位のF0ラベルを確定しない
- 不確実なラベルは無理に二値化せず、レビュー待ちとして扱う
- プロジェクト独自のアノテーションを正規データとし、VOICEVOX固有の形式はエクスポート先として扱う
- `.vvproj` はVOICEVOXエディターで開くために生成する。Engine APIへの送信だけでGUIのプロジェクトが作成・同期されるとは想定しない
- APIキーや個人情報をリポジトリにコミットしない
