# VOICEVOX `.vvproj` MVP形式

## 対象

現在のMVPは、VOICEVOX Editor `0.26.1`で保存された`data/sample.vvproj`を基準にする。`.vvproj`は内部形式であり、将来のEditorで変更される可能性があるため、対象バージョンの保存サンプルをテンプレートとして使用する。

## ルート構造

```json
{
  "appVersion": "0.26.1",
  "talk": {},
  "song": {}
}
```

## `talk`

`talk`は、音声項目のUUID配列とUUIDから項目へのマップで構成される。

```json
{
  "audioKeys": ["<audio-item-uuid>"],
  "audioItems": {
    "<audio-item-uuid>": {
      "text": "本文",
      "voice": {
        "engineId": "<engine-uuid>",
        "speakerId": "<speaker-uuid>",
        "styleId": 3
      },
      "query": {
        "accentPhrases": [],
        "speedScale": 1,
        "pitchScale": 0,
        "intonationScale": 1,
        "volumeScale": 1,
        "prePhonemeLength": 0.1,
        "postPhonemeLength": 0.1,
        "pauseLengthScale": 1,
        "outputSamplingRate": 24000,
        "outputStereo": false,
        "kana": "カクテイシタヨミ"
      },
      "presetKey": "<preset-uuid>"
    }
  }
}
```

`query.accentPhrases`には、アクセント句ごとの`moras`、`accent`、`isInterrogative`を含める。moraには`text`、`vowel`、`vowelLength`を持たせ、必要に応じて`consonant`、`consonantLength`、`pitch`を持たせる。読点などのポーズは`pauseMora`として格納される。

トークのみのプロジェクトでも、`song`の`tempos`、`timeSignatures`、`tracks`、`trackOrder`をサンプルと同じ形で保持する。通常のトーク変換では`notes`は空配列でよい。

## 本プロジェクトの生成規則

1. `data/sample.vvproj`を読み込み、対象バージョンの形式を継承する。
2. `talk.audioKeys`と`talk.audioItems`を新しいUUIDで再構成する。
3. 確認後の本文を`audioItems[*].text`に設定する。
4. 確定読みを`audioItems[*].query.kana`に設定する。
5. 正規アノテーションとアクセント推定は`metadata.transcriptWithAccent`に保存する。

## 注意点

- `query`を空にしたり、独自の`tracks`形式に置き換えたりするとEditorで読み込めない。
- `appVersion`と`query`のフィールドはVOICEVOX Editorのバージョンに依存する。
- 現在のMVPでは、サンプルの`query.accentPhrases`を形式上の雛形として再利用している。正確なmora列生成は今後、VOICEVOX Engineの`/audio_query`等に置き換える。
- 新しいEditorに対応するときは、そのEditorで保存したサンプルに更新し、読み込みテストを行う。
