# password-gl [![PyPI version](https://img.shields.io/pypi/v/password-gl)](https://pypi.org/project/password-gl/) [![PyPI Downloads](https://static.pepy.tech/badge/password-gl)](https://pepy.tech/projects/password-gl) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

セキュアなパスワード / パスフレーズを１コマンドで生成する CLI ツール。

- **暗号的に安全な乱数** (`secrets` モジュール) を使用
- パスワード強度をエントロピー（bit）で可視化
- パスワード / パスフレーズ / PIN の３モード
- プロファイル保存・読み込み
- 対話モード (`-i`) で全オプションをガイド付き設定
- i18n（日本語 / English）対応
- 新バージョン検出時に自動更新

---

## インストール

```bash
pip install password-gl
```

クリップボードコピー機能を使う場合（任意）:

```bash
pip install pyperclip
```

---

## クイックスタート

```bash
pgl                        # info 画面
pgl -l 20 --strict         # 20文字・全種類必須
pgl --pin 6                # 6桁PIN
pgl --passphrase --words 5 # 5単語パスフレーズ
pgl --count 5 --copy       # 5個生成して最後をコピー
pgl -i                     # 対話モード（全設定をガイド付きで）
```

---

## 出力例

```
  🔑  K7#mPx@2qR!v
       強度  ████████░░  強い  72 bit

  🔑  1.  aB3$nQ9@wZ!r
       強度  ████████░░  強い  72 bit

  🔑  2.  mX4#pK7!vN2@
       強度  ████████░░  強い  72 bit
```

---

## オプション一覧

### モード

| オプション | 説明 | デフォルト |
|---|---|---|
| `-i, --interactive` | 対話モード（全設定をガイド付きで設定） | — |
| `--pin <n>` | 数字のみの PIN を生成 | 4 |
| `--passphrase` | 単語リストからパスフレーズを生成 | — |

### パスワード設定

| オプション | 説明 | デフォルト |
|---|---|---|
| `-l, --length <n>` | 文字数 | 12 |
| `--count <n>` | 生成する数 | 1 |
| `--strict` | 全種類（大文字・小文字・数字・記号）を必ず含める | — |
| `--no-upper` | 大文字を使わない | — |
| `--no-lower` | 小文字を使わない | — |
| `--no-digits` | 数字を使わない | — |
| `--no-symbols` | 記号を使わない | — |
| `--no-similar` | 類似文字を除外 (`O 0 l 1 I \|`) | — |
| `--readable` | 英数字のみ | — |
| `--exclude-chars <s>` | 指定した文字を除外 | — |
| `--charset <s>` | 使用文字を直接指定 | — |
| `--prefix <s>` | 先頭に追加する文字列 | — |
| `--suffix <s>` | 末尾に追加する文字列 | — |
| `--starts-with-lower` | 小文字で始まる | — |
| `--starts-with-upper` | 大文字で始まる | — |
| `--separator <s>` | 区切り文字 | — |
| `--every <n>` | N 文字ごとに区切り文字を挿入 | — |

### パスフレーズ設定

| オプション | 説明 | デフォルト |
|---|---|---|
| `--words <n>` | 単語数 | 4 |
| `--wordlist <path>` | 単語リストファイルのパス | 内蔵リスト |
| `--separator <s>` | 単語の区切り文字 | `-` |

### 出力設定

| オプション | 説明 |
|---|---|
| `--copy` | 最後の生成結果をクリップボードにコピー |
| `--output-file <path>` | ファイルに保存 |
| `--output-format <fmt>` | 出力形式 (`text` / `json` / `csv`) |
| `--add-date` | 日付 (`YYYYMMDD`) をプレフィックスに追加 |
| `--add-user` | ユーザー名をプレフィックスに追加 |

### プロファイル

よく使う設定を名前付きで保存・呼び出しできます。

```bash
pgl -l 20 --strict --no-similar --save-profile work   # 保存
pgl --profile work                                     # 呼び出し
pgl --list-profiles                                    # 一覧
```

プロファイルは `~/.pgl/profiles.json` に保存されます。

### その他

| オプション | 説明 |
|---|---|
| `-u, --update` | 最新バージョンに更新 |
| `--lang <ja\|en>` | 表示言語（環境変数 `PGL_LANG` でも設定可） |
| `-v, --version` | バージョンを表示 |
| `-h, --help` | ヘルプを表示 |

---

## 使用例

```bash
# 16文字・記号なし・全種類必須を3つ生成
pgl -l 16 --no-symbols --strict --count 3

# 4文字ごとにハイフンで区切る
pgl -l 16 --separator - --every 4
# → abcd-EFGH-1234-!@#$

# 日付＋ユーザー名をプレフィックスに
pgl --add-date --add-user -l 8

# 5単語パスフレーズをクリップボードにコピー
pgl --passphrase --words 5 --copy

# JSON形式でファイルに保存
pgl --count 10 --output-format json --output-file passwords.json

# プロファイルに保存して再利用
pgl -l 24 --strict --no-similar --save-profile strong
pgl --profile strong --count 3
```

---

## 開発者

**Lapius7** — [https://dev.lapius7.com](https://dev.lapius7.com)

- X: [@Lapius7](https://x.com/Lapius7)
- GitHub: [Lapius7/password-gl](https://github.com/Lapius7/password-gl)
- PyPI: [password-gl](https://pypi.org/project/password-gl/)

## ライセンス

MIT
