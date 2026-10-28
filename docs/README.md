# Documentation

プロジェクトの設計・開発方針をまとめる場所です。

## Documents

- [Agent instructions](AGENTS.md): コーディングエージェント向けの作業規約
- [Architecture Decision Records](adr/README.md): 設計判断の記録
- [ADR 0001: Canonical annotation model](adr/0001-canonical-annotation-model.md): 正規データモデルとエンジン非依存性
- [ADR 0002: VOICEVOX project export](adr/0002-voicevox-project-export.md): `.vvproj` を生成してVOICEVOXエディターで編集・合成する方針
- [Initial system design](design.md): 初期データフローと各コンポーネントの役割
- [VOICEVOX `.vvproj` MVP format](vvproj-format.md): 現在のプロジェクト構造と生成規則

## Documentation conventions

- READMEはプロジェクトの入口と最短の利用方法を説明する
- AGENTS.mdは作業時に守るべき規約を記載する
- ADRは「なぜその設計を選んだか」を記録する
- 未実装の機能は、実装済みであるかのように書かない
- 大きな設計変更は既存ADRを黙って書き換えず、新しいADRを追加する
