import argparse
import random
import string
import sys
import os
import json
import datetime
import getpass

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

DEFAULT_WORDLIST = os.path.join(os.path.dirname(__file__), "words.txt")


def load_wordlist(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception:
        return [
            "apple", "banana", "choco", "dragon", "echo", "fox", "giant", "hero",
            "island", "jelly", "kite", "lemon", "magic", "ninja", "ocean", "panda",
            "queen", "robot", "sun", "tiger", "umbrella", "vivid", "wolf", "xenon",
            "yeti", "zebra", "angel", "book", "cloud", "dance", "earth", "flame",
            "glow", "honey", "ice", "jewel", "king", "leaf", "moon", "night",
            "opal", "pearl", "quest", "rose", "sky", "tree", "unity", "voice",
            "wave", "xray", "yarn", "zen", "acorn", "bubble", "candy", "dream",
            "ember", "feather", "gold", "harmony", "ignite", "joy", "karma",
            "lucky", "mint", "nest", "orbit", "peace", "quartz", "raven", "star",
            "twilight", "under", "valley", "whale", "xmas", "young", "zest",
            "arch", "blade", "crystal", "daisy", "ember", "frost", "groove",
            "halo", "ink", "jungle", "karma", "loop", "muse", "nova", "noble",
            "pulse", "ripple", "soul", "tempo", "vault", "willow", "zenith"
        ]



def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True,
                      use_symbols=True, strict=False, exclude_chars="", starts_with=None,
                      prefix="", suffix="", no_similar=False, readable=False,
                      charset=None, separator=None, every=None):
    similar_chars = "O0l1I|"

    if charset:
        character_pool = charset
    else:
        character_pool = ''
        if use_upper:
            character_pool += string.ascii_uppercase
        if use_lower:
            character_pool += string.ascii_lowercase
        if use_digits:
            character_pool += string.digits
        if use_symbols:
            character_pool += string.punctuation

    if no_similar:
        character_pool = ''.join(c for c in character_pool if c not in similar_chars)

    if exclude_chars:
        character_pool = ''.join(c for c in character_pool if c not in exclude_chars)

    if readable:
        character_pool = ''.join(c for c in character_pool if c.isalnum())

    if not character_pool:
        raise ValueError("使用可能な文字がありません。")

    body_length = length - len(prefix) - len(suffix)
    if body_length <= 0:
        raise ValueError("パスワード長がプレフィックスとサフィックスよりも短いです。")

    max_attempts = 1000  # 失敗時の試行上限
    for attempt in range(max_attempts):
        pw = ''.join(random.choice(character_pool) for _ in range(body_length))

        if separator and every:
            parts = [pw[i:i + every] for i in range(0, len(pw), every)]
            pw = separator.join(parts)

        password = prefix + pw + suffix

        if starts_with:
            if starts_with == 'lower' and not password[0].islower():
                continue
            if starts_with == 'upper' and not password[0].isupper():
                continue

        if strict:
            checks = [
                not use_upper or any(c.isupper() for c in password),
                not use_lower or any(c.islower() for c in password),
                not use_digits or any(c.isdigit() for c in password),
                not use_symbols or any(c in string.punctuation for c in password)
            ]
            if not all(checks):
                continue

        return password

    raise ValueError("指定された条件で有効なパスワードを生成できませんでした。")


def generate_passphrase(words=4, wordlist=None, separator="-"):
    wl = load_wordlist(wordlist or DEFAULT_WORDLIST)
    return separator.join(random.choice(wl) for _ in range(words))


def main():
    parser = argparse.ArgumentParser(description="高機能パスワード/パスフレーズ生成ツール")
    parser.add_argument("--passphrase", action="store_true", help="パスワードではなくパスフレーズを生成する")
    parser.add_argument("--words", type=int, default=4, help="パスフレーズで使う単語数（デフォルト: 4）")
    parser.add_argument("--wordlist", type=str, help="パスフレーズ用単語リストファイルのパス")

    parser.add_argument("-l", "--length", type=int, default=12, help="パスワードの長さ")
    parser.add_argument("--count", type=int, default=1, help="生成する数")
    parser.add_argument("--prefix", type=str, default="", help="プレフィックス（先頭文字列, 最初に-を含めることはできません）")
    parser.add_argument("--suffix", type=str, default="", help="サフィックス（末尾文字列, 最初に-を含めることはできません）")
    parser.add_argument("--starts-with-lower", action="store_true", help="小文字で始まる")
    parser.add_argument("--starts-with-upper", action="store_true", help="大文字で始まる")
    parser.add_argument("--no-upper", action="store_true", help="大文字を使用しない")
    parser.add_argument("--no-lower", action="store_true", help="小文字を使用しない")
    parser.add_argument("--no-digits", action="store_true", help="数字を使用しない")
    parser.add_argument("--no-symbols", action="store_true", help="記号を使用しない")
    parser.add_argument("--no-similar", action="store_true", help="類似文字を除外 (O0l1)")
    parser.add_argument("--exclude-chars", type=str, default="", help="除外文字")
    parser.add_argument("--strict", action="store_true", help="全ての種類（大文字、小文字、数字、記号）を必ず含める")
    parser.add_argument("--readable", action="store_true", help="英数字のみ")
    parser.add_argument("--charset", type=str, help="使用文字を直接指定")
    parser.add_argument("--separator", type=str, help="区切り文字")
    parser.add_argument("--every", type=int, help="区切りを入れる文字数単位")
    parser.add_argument("--copy", action="store_true", help="最後の出力をクリップボードへコピーします(pyperclipがない場合はコピーされません)")
    parser.add_argument("--add-date", action="store_true", help="日付（YYYYMMDD）をプレフィックスに追加")
    parser.add_argument("--add-user", action="store_true", help="ユーザー名をプレフィックスに追加")
    parser.add_argument("--output-format", choices=["text", "json", "csv"], default="text", help="出力フォーマット（text, json, csv）")
    parser.add_argument("--output-file", type=str, help="出力ファイルに保存")

    args = parser.parse_args()

    starts_with = None
    if args.starts_with_lower:
        starts_with = "lower"
    elif args.starts_with_upper:
        starts_with = "upper"

    if args.add_date:
        args.prefix = datetime.datetime.now().strftime("%Y%m%d") + args.prefix
    if args.add_user:
        args.prefix = getpass.getuser() + args.prefix

    # 生成したいパスワード/フレーズを出力するリスト
    output = []

    try:
        for _ in range(args.count):
            if args.passphrase:
                pw = generate_passphrase(args.words, args.wordlist, separator=args.separator or "-")
            else:
                pw = generate_password(
                    length=args.length,
                    use_upper=not args.no_upper,
                    use_lower=not args.no_lower,
                    use_digits=not args.no_digits,
                    use_symbols=not args.no_symbols,
                    strict=args.strict,
                    exclude_chars=args.exclude_chars,
                    starts_with=starts_with,
                    prefix=args.prefix,
                    suffix=args.suffix,
                    no_similar=args.no_similar,
                    readable=args.readable,
                    charset=args.charset,
                    separator=args.separator,
                    every=args.every,
                )
            output.append(pw)
            print(pw)

        if args.copy and CLIPBOARD_AVAILABLE:
            pyperclip.copy(output[-1])
            print("✅ 最後のパスワード/パスフレーズをクリップボードにコピーしました。")

        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                if args.output_format == "json":
                    json.dump(output, f, ensure_ascii=False, indent=2)
                elif args.output_format == "csv":
                    f.write("\n".join(output))
                else:
                    f.write("\n".join(output))
            print(f"📁 {args.output_file} に保存しました。")

    except ValueError as e:
        print(f"❌ エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()