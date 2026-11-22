<div align="center">

<p align="center"><a href="README.md">English</a> | <b>日本語</b></p>

<h1 align="center">Password GL</h1>

<h3 align="center">セキュアなパスワードやパスフレーズを、1コマンドで生成。</h3>

<p align="center">Python の <code>secrets</code> モジュールでパスワード、パスフレーズ、PIN を生成し、強度をbitで表示する CLI です。コマンドは <code>password-gl</code> と短縮名 <code>pgl</code> です。</p>

<p align="center">
  <a href="https://pypi.org/project/password-gl/"><img alt="PyPI" src="https://img.shields.io/pypi/v/password-gl?style=flat-square&color=3775a9&logo=pypi&logoColor=white"></a>
  <a href="https://www.npmjs.com/package/@lapius/password-gl"><img alt="npm" src="https://img.shields.io/npm/v/@lapius/password-gl?style=flat-square&color=cb3837&logo=npm"></a>
  <a href="https://pepy.tech/projects/password-gl"><img alt="Downloads" src="https://static.pepy.tech/badge/password-gl?style=flat-square"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/Lapius7/password-gl?style=flat-square&color=97ca00"></a>
  <a href="https://www.python.org"><img alt="Python 3.9+" src="https://img.shields.io/badge/python-3.9%2B-ffd43b?style=flat-square&logo=python&logoColor=000000"></a>
  <a href="https://github.com/Lapius7/password-gl/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Lapius7/password-gl?style=flat-square&color=e3b341&logo=github"></a>
  <a href="https://github.com/Lapius7/password-gl/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Lapius7/password-gl?style=flat-square&color=3b82f6"></a>
</p>

<p align="center">
  <a href="#クイックスタート">クイックスタート</a> ·
  <a href="#オプション">オプション</a> ·
  <a href="#使用例">使用例</a> ·
  <a href="#開発">開発</a>
</p>

</div>

---

## 特長

- 暗号的に安全な乱数（`secrets` モジュール）を使います。
- パスワードの強度をエントロピー（bit）で表示します。
- パスワード、パスフレーズ、PIN の3モードがあります。
- 設定に名前を付けて保存し、読み込めます。
- 対話モード（`-i`）で、すべてのオプションをガイド付きで設定できます。
- 日本語と English の表示に対応しています。
- 新しいバージョンを検出すると自動で更新します。

## クイックスタート

Python 3.9 以降が必要です。npm 版は、さらに Node.js 18 以降が必要です（Python はシステムのものを使います）。

**1. インストール**

pnpm（推奨）:

```sh
pnpm add -g @lapius/password-gl
```

`password-gl` と短縮名 `pgl` の2つのコマンドが使えるようになります。更新も同じコマンドで行えます。npm で入れた場合は、`pgl -u` も npm 経由で更新します。

> [!IMPORTANT]
> このパッケージは **pnpm 前提**です。npm と pnpm の両方に入れると同じコマンドが二重になるため、`pnpm add -g` だけを使ってください。

pip:

```sh
pip install password-gl
```

更新は `pip install --upgrade password-gl` または `pgl -u` です。

`--copy` を使う場合は、どちらの入れ方でも pyperclip を追加で入れてください。

```sh
pip install pyperclip
```

**2. 試す**

```sh
pgl                        # info 画面
pgl -l 20 --strict         # 20文字・全種類必須
pgl --pin 6                # 6桁PIN
pgl --passphrase --words 5 # 5単語パスフレーズ
pgl --count 5 --copy       # 5個生成して最後をコピー
pgl -i                     # 対話モード（全設定をガイド付きで）
```

出力例です（値は例で、ラベルはロケールに従い、`--lang ja|en` でも指定できます）。

```
  🔑  K7#mPx@2qR!v
       強度  ████████░░  強い  72 bit

  🔑  1.  aB3$nQ9@wZ!r
       強度  ████████░░  強い  72 bit

  🔑  2.  mX4#pK7!vN2@
       強度  ████████░░  強い  72 bit
```

## オプション

### モード

| オプション | 説明 | デフォルト |
|---|---|---|
| `-i, --interactive` | 対話モード（全設定をガイド付きで設定） | - |
| `--pin <n>` | 数字のみの PIN を生成 | 4 |
| `--passphrase` | 単語リストからパスフレーズを生成 | - |

### パスワード設定

| オプション | 説明 | デフォルト |
|---|---|---|
| `-l, --length <n>` | 文字数 | 12 |
| `--count <n>` | 生成する数 | 1 |
| `--strict` | 全種類（大文字・小文字・数字・記号）を必ず含める | - |
| `--no-upper` | 大文字を使わない | - |
| `--no-lower` | 小文字を使わない | - |
| `--no-digits` | 数字を使わない | - |
| `--no-symbols` | 記号を使わない | - |
| `--no-similar` | 類似文字を除外（`O 0 l 1 I \|`） | - |
| `--exclude-chars <s>` | 指定した文字を除外 | - |
| `--charset <s>` | 使用文字を直接指定（他の文字種フラグより優先） | - |
| `--starts-with <v>` | 先頭文字の制約（`lower` / `upper`） | - |
| `--prefix <s>` | 先頭に追加する文字列 | - |
| `--suffix <s>` | 末尾に追加する文字列 | - |
| `--separator <s>` | 区切り文字 | - |
| `--every <n>` | N 文字ごとに区切り文字を挿入（`--separator` と組み合わせて使用） | - |

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
| `--output-format <fmt>` | 出力形式（`text` / `json` / `csv`） |
| `--add-date` | 日付（`YYYYMMDD`）をプレフィックスに追加 |
| `--add-user` | ユーザー名をプレフィックスに追加 |

### プロファイル

よく使う設定を名前付きで保存し、呼び出せます。

```sh
pgl -l 20 --strict --no-similar --save-profile work   # 保存
pgl --profile work                                     # 呼び出し
pgl --list-profiles                                    # 一覧
```

プロファイルは `~/.pgl/profiles.json` に保存されます。

### その他

| オプション | 説明 |
|---|---|
| `-u, --update` | 最新バージョンに更新（npm で入れた場合は npm、pip の場合は pip で更新） |
| `--lang <ja\|en>` | 表示言語（環境変数 `PGL_LANG` でも設定可） |
| `-v, --version` | バージョンを表示 |
| `-h, --help` | ヘルプを表示 |

## 使用例

```sh
# 16文字・記号なし・全種類必須を3つ生成
pgl -l 16 --no-symbols --strict --count 3

# 4文字ごとにハイフンで区切る
pgl -l 16 --separator - --every 4
# -> abcd-EFGH-1234-!@#$

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

> [!NOTE]
> 上のオプションは `password_gl/generator.py` の引数定義と照合しました。書き直しにあたって実行はしておらず、クリップボード、自動更新、npm 経由の動作は、ここでは未検証です。

## 開発

ソースは `password_gl/generator.py`（単一モジュール）です。GitHub Release を公開すると、PyPI（`.github/workflows/publish.yml`）と npm（`.github/workflows/npm.yml`）に公開されます。npm は Trusted Publisher を使うのでトークンは不要です。`npm/` の npm パッケージは Python のソースを同梱し、システムの Python で実行します。

**開発者**: Lapius7 - [https://dev.lapius7.com](https://dev.lapius7.com) · X: [@Lapius7](https://x.com/Lapius7) · PyPI: [password-gl](https://pypi.org/project/password-gl/)

## ライセンス

MIT
