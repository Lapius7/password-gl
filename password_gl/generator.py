import math
import secrets
import string
import sys
import os
import json
import datetime
import getpass
import locale
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

from . import __version__


# ── Console ────────────────────────────────────────────────────────

def _setup_console():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_setup_console()


# ── Colors ─────────────────────────────────────────────────────────

R    = "\033[0m"
CYAN = "\033[36m"
BCYN = "\033[1;96m"
GREEN= "\033[32m"
YEL  = "\033[33m"
BYEL = "\033[1;33m"
WHITE= "\033[97m"
BWHT = "\033[1;97m"
GRAY = "\033[90m"
RED  = "\033[31m"

def c(text, color): return f"{color}{text}{R}"
def bar():  return c("  " + "─" * 52, GRAY)
def dbar(): return c("  " + "═" * 52, GRAY)


# ── i18n ──────────────────────────────────────────────────────────

def _detect_lang(override: Optional[str] = None) -> str:
    if override in ("ja", "en"):
        return override
    env = os.environ.get("PGL_LANG", "")
    if env in ("ja", "en"):
        return env
    try:
        loc = locale.getdefaultlocale()[0] or ""
        return "ja" if loc.startswith("ja") else "en"
    except Exception:
        return "en"


T: dict = {
    "ja": {
        "tagline":      "セキュアなパスワード / パスフレーズを１コマンドで生成",
        "author":       "開発者",
        "ver_ok":       "最新",
        "ver_fail":     "確認失敗",
        "ver_new":      "↑ v{}",
        "auto_upd":     "↑ v{} が利用可能 — 自動更新中...",
        "auto_upd_ok":  "✓ v{} に更新しました。もう一度実行してください",
        "auto_upd_ng":  "✗ 自動更新に失敗しました — pip install --upgrade password-gl",
        "guide":        "使い方",
        "help_lbl":     "ヘルプ",
        "usage":        "使い方",
        "usage_cmd":    "pgl [オプション]",
        "opts":         "オプション",
        "examples":     "例",
        "updating":     "🔄 pgl を最新バージョンに更新中...",
        "up_done":      "✓ 更新完了",
        "already_up":   "✓ 既に最新です (v{})",
        "strength":     "強度",
        "weak":         "弱い",
        "fair":         "普通",
        "strong":       "強い",
        "very_strong":  "非常に強い",
        "copied":       "✓ クリップボードにコピーしました",
        "copy_fail":    "✗ クリップボードには pyperclip が必要です — pip install pyperclip",
        "saved":        "✓ {} に保存しました",
        "prof_saved":   "✓ プロファイル '{}' を保存しました",
        "prof_missing": "✗ プロファイル '{}' が見つかりません",
        "prof_none":    "(プロファイルなし)",
        "no_chars":     "使用可能な文字がありません",
        "too_short":    "長さがプレフィックス/サフィックスより短いです",
        "gen_fail":     "指定条件でパスワードを生成できませんでした",
        "warn_every_no_sep":     "⚠  --separator が未指定のため '-' を使用します",
        "warn_charset_override": "⚠  --charset が指定されているため、文字種フラグは無視されます",
        "warn_all_off":          "✗  すべての文字種が無効です。--charset を指定するか文字種を有効にしてください",
        "warn_strict_conflict":  "⚠  --strict が指定されていますが、一部の文字種が無効なため必須チェックは部分的になります",
        "yn_hint":               "y または N を入力してください",
        "skip_hint":             "スキップ: Enter",
        "int_output":            "出力",
        "int_settings":          "設定",
        "o_starts_with":         "先頭文字の制約 (lower / upper)",
        "int_title":    "interactive",
        "int_mode":     "モード",
        "int_mode_pw":  "パスワード",
        "int_mode_pp":  "パスフレーズ",
        "int_mode_pin": "PIN",
        "int_length":   "パスワードの長さ",
        "int_words":    "単語数",
        "int_digits":   "桁数",
        "int_strict":   "全種類を必ず含める？",
        "int_nosim":    "類似文字を除外 (O0l1)？",
        "int_count":    "生成する数",
        "int_copy":     "クリップボードにコピー？",
        "int_no_upper": "大文字を使わない？",
        "int_no_lower": "小文字を使わない？",
        "int_no_digits":"数字を使わない？",
        "int_no_sym":   "記号を使わない？",
        "int_exclude":  "除外する文字 (例: @#$)",
        "int_prefix":   "プレフィックス",
        "int_suffix":   "サフィックス",
        "int_separator":"区切り文字",
        "int_every":    "区切りを入れる文字数",
        "int_sw":       "先頭文字の制約",
        "int_sw_none":  "なし",
        "int_sw_lower": "小文字",
        "int_sw_upper": "大文字",
        "int_outfile_yn":"ファイルに保存する？",
        "int_outfile":  "保存先のファイルパス",
        "int_pp_sep":   "単語の区切り文字",
        "int_adv":      "詳細設定も行う？",
        "int_charset":  "使用文字を直接指定",
        "o_interactive":"対話モードで設定",
        "o_pin":        "数字のみのPINを生成",
        "o_passphrase": "パスフレーズを生成",
        "o_length":     "パスワードの長さ",
        "o_count":      "生成する数",
        "o_strict":     "全種類を必ず含める",
        "o_no_upper":   "大文字を使わない",
        "o_no_lower":   "小文字を使わない",
        "o_no_digits":  "数字を使わない",
        "o_no_symbols": "記号を使わない",
        "o_no_similar": "類似文字を除外 (O0l1)",
        "o_exclude":    "除外する文字",
        "o_charset":    "使用文字を直接指定",
        "o_prefix":     "先頭に追加する文字列",
        "o_suffix":     "末尾に追加する文字列",
        "o_separator":  "区切り文字",
        "o_every":      "区切りを入れる文字数",
        "o_words":      "パスフレーズの単語数",
        "o_wordlist":   "単語リストファイルのパス",
        "o_copy":       "クリップボードにコピー",
        "o_outfile":    "ファイルに保存",
        "o_outfmt":     "出力形式",
        "o_add_date":   "日付をプレフィックスに追加",
        "o_add_user":   "ユーザー名をプレフィックスに追加",
        "o_save_prof":  "現在の設定をプロファイルに保存",
        "o_profile":    "プロファイルを読み込む",
        "o_list_prof":  "プロファイル一覧を表示",
        "o_update":     "最新バージョンに更新",
        "o_lang":       "表示言語",
        "o_version":    "バージョンを表示",
        "o_help":       "このヘルプを表示",
        "ex_1":         "# デフォルト",
        "ex_2":         "# 20文字・全種類",
        "ex_3":         "# 6桁PIN",
        "ex_4":         "# 5単語パスフレーズ",
        "ex_5":         "# 5個生成してコピー",
        "ex_6":         "# プロファイル保存",
        "ex_7":         "# 対話モード",
    },
    "en": {
        "tagline":      "Generate secure passwords / passphrases in one command",
        "author":       "Author",
        "ver_ok":       "latest",
        "ver_fail":     "check failed",
        "ver_new":      "↑ v{}",
        "auto_upd":     "↑ v{} available — auto-updating...",
        "auto_upd_ok":  "✓ Updated to v{}. Run the command again to continue",
        "auto_upd_ng":  "✗ Auto-update failed — pip install --upgrade password-gl",
        "guide":        "Guide",
        "help_lbl":     "Help",
        "usage":        "Usage",
        "usage_cmd":    "pgl [options]",
        "opts":         "Options",
        "examples":     "Examples",
        "updating":     "🔄 Updating pgl to the latest version...",
        "up_done":      "✓ Update complete",
        "already_up":   "✓ Already up to date (v{})",
        "strength":     "Strength",
        "weak":         "Weak",
        "fair":         "Fair",
        "strong":       "Strong",
        "very_strong":  "Very Strong",
        "copied":       "✓ Copied to clipboard",
        "copy_fail":    "✗ pyperclip required — pip install pyperclip",
        "saved":        "✓ Saved to {}",
        "prof_saved":   "✓ Profile '{}' saved",
        "prof_missing": "✗ Profile '{}' not found",
        "prof_none":    "(no profiles)",
        "no_chars":     "No characters available",
        "too_short":    "Length is shorter than prefix + suffix",
        "gen_fail":     "Could not generate password with given constraints",
        "warn_every_no_sep":     "⚠  --separator not set, using '-'",
        "warn_charset_override": "⚠  --charset specified; character type flags are ignored",
        "warn_all_off":          "✗  All character types disabled. Specify --charset or enable at least one type",
        "warn_strict_conflict":  "⚠  --strict with some types disabled; strict check applies only to active types",
        "yn_hint":               "Please enter y or N",
        "skip_hint":             "skip: Enter",
        "int_output":            "Output",
        "int_settings":          "Settings",
        "o_starts_with":         "First char constraint (lower / upper)",
        "int_title":    "interactive",
        "int_mode":     "Mode",
        "int_mode_pw":  "Password",
        "int_mode_pp":  "Passphrase",
        "int_mode_pin": "PIN",
        "int_length":   "Password length",
        "int_words":    "Word count",
        "int_digits":   "Number of digits",
        "int_strict":   "Require all character types?",
        "int_nosim":    "Exclude similar chars (O0l1)?",
        "int_count":    "How many to generate",
        "int_copy":     "Copy to clipboard?",
        "int_no_upper": "Exclude uppercase?",
        "int_no_lower": "Exclude lowercase?",
        "int_no_digits":"Exclude digits?",
        "int_no_sym":   "Exclude symbols?",
        "int_exclude":  "Exclude chars (e.g. @#$)",
        "int_prefix":   "Prefix",
        "int_suffix":   "Suffix",
        "int_separator":"Separator character",
        "int_every":    "Insert separator every N chars",
        "int_sw":       "First character constraint",
        "int_sw_none":  "none",
        "int_sw_lower": "lowercase",
        "int_sw_upper": "uppercase",
        "int_outfile_yn":"Save to file?",
        "int_outfile":  "File path to save",
        "int_pp_sep":   "Word separator",
        "int_adv":      "Configure advanced options?",
        "int_charset":  "Custom charset",
        "o_interactive":"Interactive setup mode",
        "o_pin":        "Generate numeric PIN",
        "o_passphrase": "Generate a passphrase",
        "o_length":     "Password length",
        "o_count":      "Number to generate",
        "o_strict":     "Require all character types",
        "o_no_upper":   "No uppercase letters",
        "o_no_lower":   "No lowercase letters",
        "o_no_digits":  "No digits",
        "o_no_symbols": "No symbols",
        "o_no_similar": "Exclude similar chars (O0l1)",
        "o_exclude":    "Characters to exclude",
        "o_charset":    "Custom character set",
        "o_prefix":     "Prefix string",
        "o_suffix":     "Suffix string",
        "o_separator":  "Separator character",
        "o_every":      "Insert separator every N chars",
        "o_words":      "Passphrase word count",
        "o_wordlist":   "Path to wordlist file",
        "o_copy":       "Copy to clipboard",
        "o_outfile":    "Save to file",
        "o_outfmt":     "Output format",
        "o_add_date":   "Add date as prefix",
        "o_add_user":   "Add username as prefix",
        "o_save_prof":  "Save current settings as profile",
        "o_profile":    "Load a saved profile",
        "o_list_prof":  "List all profiles",
        "o_update":     "Update to the latest version",
        "o_lang":       "Display language",
        "o_version":    "Show version",
        "o_help":       "Show this help",
        "ex_1":         "# default",
        "ex_2":         "# 20 chars, all types",
        "ex_3":         "# 6-digit PIN",
        "ex_4":         "# 5-word passphrase",
        "ex_5":         "# generate 5, copy last",
        "ex_6":         "# save profile",
        "ex_7":         "# interactive mode",
    },
}


# ── Version ────────────────────────────────────────────────────────

def fetch_remote_version() -> Optional[str]:
    try:
        url = "https://pypi.org/pypi/password-gl/json"
        with urllib.request.urlopen(url, timeout=3) as r:
            return json.loads(r.read())["info"]["version"]
    except Exception:
        return None


def _parse_ver(v: str) -> tuple:
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0,)


def _is_newer(remote: str) -> bool:
    return _parse_ver(remote) > _parse_ver(__version__)


def _ver_badge(remote: Optional[str], lang: str) -> str:
    s = T[lang]
    if remote is None:        return c(f"（{s['ver_fail']}）", GRAY)
    if remote == __version__: return c(f"（{s['ver_ok']}）", GREEN)
    if _is_newer(remote):     return c(f"（{s['ver_new'].format(remote)}）", YEL)
    return c(f"（{s['ver_ok']}）", GREEN)


def _do_pip_upgrade() -> Optional[str]:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", "password-gl"],
        capture_output=True
    )
    if result.returncode != 0:
        return None
    try:
        import importlib.metadata
        return importlib.metadata.version("password-gl")
    except Exception:
        return None


def auto_update(remote: str, lang: str):
    s = T[lang]
    print()
    print(c("  " + s["auto_upd"].format(remote), YEL))
    installed = _do_pip_upgrade()
    if installed and _parse_ver(installed) >= _parse_ver(remote):
        print(c("  " + s["auto_upd_ok"].format(installed), GREEN))
    else:
        print(c("  " + s["auto_upd_ng"], RED))
    print()
    sys.exit(0)


def do_update(remote: Optional[str], lang: str):
    s = T[lang]
    if remote and remote == __version__:
        print(c(s["already_up"].format(__version__), GREEN))
        return
    print(c(s["updating"], CYAN))
    installed = _do_pip_upgrade()
    if installed and _parse_ver(installed) >= _parse_ver(remote or "0"):
        print(c(s["up_done"], GREEN))
    else:
        print(c(s["auto_upd_ng"], RED))


# ── Logo & UI helpers ──────────────────────────────────────────────

def _logo():
    return c("p", BCYN) + c("gl", BYEL)


def _opt(flags: str, desc: str, note: str = ""):
    print(f"  {c(flags.ljust(28), CYAN)}{c(desc, WHITE)}{c('  (' + note + ')', GRAY) if note else ''}")

def _section(title: str):
    print(f"\n  {c(title, YEL)}")


def show_info(remote: Optional[str], lang: str):
    s = T[lang]
    W = 10
    print()
    print(dbar())
    print(f"  🔑  {_logo()}  {c(f'v{__version__}', GRAY)}{_ver_badge(remote, lang)}")
    print(dbar())
    print(f"\n  {c(s['tagline'], GRAY)}\n")
    _dev_info(lang)
    print(f"  {c((s['guide']+' ').ljust(W), GRAY)}{s['usage_cmd']}")
    print(f"  {c((s['help_lbl']+' ').ljust(W), GRAY)}pgl --help")
    print()
    print(dbar())
    print()


def _dev_info(lang: str):
    s = T[lang]
    W = 10
    print()
    print(f"  {c(s['author'], GRAY)}    Lapius7（https://dev.lapius7.com）")
    print(f"  {c('X'.ljust(W), GRAY)}https://x.com/Lapius7")
    print(f"  {c('GitHub'.ljust(W), GRAY)}https://github.com/Lapius7/password-gl")
    print(f"  {c('PyPI'.ljust(W), GRAY)}https://pypi.org/project/password-gl")
    print()


def show_help(lang: str):
    s = T[lang]
    print()
    print(dbar())
    print(f"  🔑  {_logo()}  {c(f'v{__version__}', GRAY)}")
    print(c(f"  {s['tagline']}", GRAY))
    print(dbar())
    _dev_info(lang)
    print(dbar())

    _section(s["usage"])
    print(f"    {c(s['usage_cmd'], WHITE)}")

    _section(s["opts"])
    _opt("-i, --interactive",      s["o_interactive"])
    _opt("    --pin <n>",          s["o_pin"],        "4")
    _opt("    --passphrase",       s["o_passphrase"])
    print()
    _opt("-l, --length <n>",       s["o_length"],     "12")
    _opt("    --count <n>",        s["o_count"],      "1")
    _opt("    --strict",           s["o_strict"])
    _opt("    --no-upper",         s["o_no_upper"])
    _opt("    --no-lower",         s["o_no_lower"])
    _opt("    --no-digits",        s["o_no_digits"])
    _opt("    --no-symbols",       s["o_no_symbols"])
    _opt("    --no-similar",       s["o_no_similar"])
    _opt("    --exclude-chars <s>",s["o_exclude"])
    _opt("    --charset <s>",      s["o_charset"])
    _opt("    --prefix <s>",       s["o_prefix"])
    _opt("    --suffix <s>",       s["o_suffix"])
    _opt("    --starts-with <v>",   s["o_starts_with"])
    _opt("    --separator <s>",    s["o_separator"])
    _opt("    --every <n>",        s["o_every"])
    print()
    _opt("    --words <n>",        s["o_words"],      "4")
    _opt("    --wordlist <path>",  s["o_wordlist"])
    print()
    _opt("    --copy",             s["o_copy"])
    _opt("    --output-file <p>",  s["o_outfile"])
    _opt("    --output-format <f>",s["o_outfmt"],     "text/json/csv")
    _opt("    --add-date",         s["o_add_date"])
    _opt("    --add-user",         s["o_add_user"])
    print()
    _opt("    --save-profile <n>", s["o_save_prof"])
    _opt("    --profile <n>",      s["o_profile"])
    _opt("    --list-profiles",    s["o_list_prof"])
    print()
    _opt("-u, --update",           s["o_update"])
    _opt("    --lang <lang>",      s["o_lang"],       "ja / en")
    _opt("-v, --version",          s["o_version"])
    _opt("-h, --help",             s["o_help"])

    _section(s["examples"])
    print(f"    {c('pgl', WHITE):<40} {c(s['ex_1'], GRAY)}")
    print(f"    {c('pgl -l 20 --strict', WHITE):<40} {c(s['ex_2'], GRAY)}")
    print(f"    {c('pgl --pin 6', WHITE):<40} {c(s['ex_3'], GRAY)}")
    print(f"    {c('pgl --passphrase --words 5', WHITE):<40} {c(s['ex_4'], GRAY)}")
    print(f"    {c('pgl --count 5 --copy', WHITE):<40} {c(s['ex_5'], GRAY)}")
    print(f"    {c('pgl --save-profile work', WHITE):<40} {c(s['ex_6'], GRAY)}")
    print(f"    {c('pgl -i', WHITE):<40} {c(s['ex_7'], GRAY)}")
    print()
    print(dbar())
    print()


# ── Strength & Entropy ─────────────────────────────────────────────

def _pool_size(use_upper, use_lower, use_digits, use_symbols,
               no_similar, exclude_chars, charset) -> int:
    if charset:
        return max(len(set(charset)), 1)
    pool = set()
    if use_upper:   pool |= set(string.ascii_uppercase)
    if use_lower:   pool |= set(string.ascii_lowercase)
    if use_digits:  pool |= set(string.digits)
    if use_symbols: pool |= set(string.punctuation)
    if no_similar:  pool -= set("O0l1I|")
    if exclude_chars: pool -= set(exclude_chars)
    return max(len(pool), 1)


def _entropy(pool: int, length: int) -> float:
    return math.log2(pool) * length if pool > 1 else 0.0


def _strength_info(bits: float, lang: str):
    s = T[lang]
    filled = min(round(bits / 128 * 10), 10)
    bar_str = c("█" * filled, GREEN if bits >= 60 else YEL if bits >= 40 else RED) + c("░" * (10 - filled), GRAY)
    if bits < 40:   return s["weak"],        RED,   bar_str
    if bits < 60:   return s["fair"],        YEL,   bar_str
    if bits < 80:   return s["strong"],      GREEN, bar_str
    return              s["very_strong"],    BCYN,  bar_str


def _show_password(pw: str, bits: float, lang: str, index: Optional[int] = None):
    s = T[lang]
    label, color, bar_str = _strength_info(bits, lang)
    num = f"  {c(str(index) + '.', GRAY)}  " if index is not None else "  🔑  "
    print(f"{num}{c(pw, BWHT)}")
    print(f"     {c(s['strength'], GRAY)}  {bar_str}  {c(label, color)}  {c(f'{bits:.0f} bit', GRAY)}")


def _show_settings_summary(args, starts_with, lang: str):
    s = T[lang]
    items = []
    if getattr(args, "passphrase", False):
        items.append(("mode", s["int_mode_pp"]))
        items.append(("words", str(args.words)))
    elif getattr(args, "pin", None) is not None:
        items.append(("mode", s["int_mode_pin"]))
        items.append(("digits", str(args.pin)))
    else:
        items.append(("mode", s["int_mode_pw"]))
        items.append(("length", str(args.length)))
        if args.charset:
            items.append(("charset", args.charset))
        else:
            types = []
            if not args.no_upper:   types.append("A-Z")
            if not args.no_lower:   types.append("a-z")
            if not args.no_digits:  types.append("0-9")
            if not args.no_symbols: types.append("!@#…")
            if types: items.append(("chars", " ".join(types)))
        if args.strict:      items.append(("strict", "✓"))
        if args.no_similar:  items.append(("no-similar", "✓"))
        if args.exclude_chars: items.append(("exclude", args.exclude_chars))
        if starts_with:      items.append(("starts-with", starts_with))
        if args.separator:   items.append(("sep", f"'{args.separator}' / {args.every}"))
    if args.prefix:  items.append(("prefix", args.prefix))
    if args.suffix:  items.append(("suffix", args.suffix))
    if args.count > 1: items.append(("count", str(args.count)))

    parts = "  ".join(f"{c(k, GRAY)} {c(v, WHITE)}" for k, v in items)
    print(f"  {c(s['int_settings'], GRAY)}  {parts}")


# ── Profile management ─────────────────────────────────────────────

_PROFILE_FILE = Path.home() / ".pgl" / "profiles.json"


def _load_profiles() -> dict:
    if not _PROFILE_FILE.exists():
        return {}
    try:
        return json.loads(_PROFILE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_profile(name: str, settings: dict):
    _PROFILE_FILE.parent.mkdir(exist_ok=True)
    profiles = _load_profiles()
    profiles[name] = settings
    _PROFILE_FILE.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")


def _list_profiles(lang: str):
    s = T[lang]
    profiles = _load_profiles()
    print()
    print(dbar())
    print(f"  🔑  {_logo()}  {c('Profiles', GRAY)}")
    print(dbar())
    print()
    if not profiles:
        print(c(f"  {s['prof_none']}", GRAY))
    else:
        for name, settings in profiles.items():
            parts = "  ".join(f"{c(k, CYAN)} {c(str(v), WHITE)}" for k, v in settings.items() if v)
            print(f"  {c(name, BYEL)}  {parts}")
    print()
    print(dbar())
    print()


# ── Wordlist ──────────────────────────────────────────────────────

_DEFAULT_WORDLIST = os.path.join(os.path.dirname(__file__), "words.txt")

_FALLBACK_WORDS = [
    "apple", "banana", "choco", "dragon", "echo", "fox", "giant", "hero",
    "island", "jelly", "kite", "lemon", "magic", "ninja", "ocean", "panda",
    "queen", "robot", "sun", "tiger", "umbrella", "vivid", "wolf", "xenon",
    "yeti", "zebra", "angel", "book", "cloud", "dance", "earth", "flame",
    "glow", "honey", "ice", "jewel", "king", "leaf", "moon", "night",
    "opal", "pearl", "quest", "rose", "sky", "tree", "unity", "voice",
    "wave", "yarn", "zen", "acorn", "bubble", "candy", "dream", "ember",
    "feather", "gold", "harmony", "ignite", "joy", "karma", "lucky", "mint",
    "nest", "orbit", "peace", "quartz", "raven", "star", "twilight", "valley",
    "whale", "young", "zest", "arch", "blade", "crystal", "daisy", "frost",
    "groove", "halo", "ink", "jungle", "loop", "muse", "nova", "noble",
    "pulse", "ripple", "soul", "tempo", "vault", "willow", "zenith",
]


def _load_wordlist(path: Optional[str] = None) -> list:
    target = path or _DEFAULT_WORDLIST
    try:
        words = [ln.strip() for ln in open(target, encoding="utf-8") if ln.strip()]
        return words if words else _FALLBACK_WORDS
    except Exception:
        return _FALLBACK_WORDS


# ── Generation ────────────────────────────────────────────────────

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True,
                      use_symbols=True, strict=False, exclude_chars="", starts_with=None,
                      prefix="", suffix="", no_similar=False,
                      charset=None, separator=None, every=None):
    if charset:
        pool = list(charset)
    else:
        pool = []
        if use_upper:   pool += list(string.ascii_uppercase)
        if use_lower:   pool += list(string.ascii_lowercase)
        if use_digits:  pool += list(string.digits)
        if use_symbols: pool += list(string.punctuation)
        if no_similar:  pool = [ch for ch in pool if ch not in "O0l1I|"]
        if exclude_chars: pool = [ch for ch in pool if ch not in exclude_chars]

    if not pool:
        raise ValueError("no_chars")

    body_len = length - len(prefix) - len(suffix)
    if body_len <= 0:
        raise ValueError("too_short")

    for _ in range(1000):
        pw = "".join(secrets.choice(pool) for _ in range(body_len))

        if separator and every:
            parts = [pw[i:i + every] for i in range(0, len(pw), every)]
            pw = separator.join(parts)

        password = prefix + pw + suffix

        if starts_with == "lower" and not password[0].islower():
            continue
        if starts_with == "upper" and not password[0].isupper():
            continue

        if strict:
            checks = [
                not use_upper   or any(ch.isupper() for ch in password),
                not use_lower   or any(ch.islower() for ch in password),
                not use_digits  or any(ch.isdigit() for ch in password),
                not use_symbols or any(ch in string.punctuation for ch in password),
            ]
            if not all(checks):
                continue

        return password

    raise ValueError("gen_fail")


def generate_passphrase(words=4, wordlist=None, separator="-"):
    wl = _load_wordlist(wordlist)
    return separator.join(secrets.choice(wl) for _ in range(words))


def generate_pin(digits=4):
    return "".join(secrets.choice(string.digits) for _ in range(digits))


# ── Interactive mode ──────────────────────────────────────────────

_OVR = "\x1b[1A\r\x1b[2K"  # cursor up, return, erase line


def _ask(prompt: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    full = f"  {c('?', CYAN)} {c(prompt + hint + ': ', WHITE)}"
    try:
        val = input(full)
        result = val.strip() or default
        if not val.strip() and result:
            sys.stdout.write(f"{_OVR}{full}{c(result, GRAY)}\n")
            sys.stdout.flush()
        return result
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def _ask_yn(prompt: str, lang: str = "ja") -> bool:
    s = T[lang]
    full = f"  {c('?', CYAN)} {c(prompt + ' (y/N): ', WHITE)}"
    while True:
        try:
            val = input(full).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if val in ("y", "n", ""):
            result = val == "y"
            chosen = c("y", GREEN) if result else c("N", GRAY)
            sys.stdout.write(f"{_OVR}{full}{chosen}\n")
            sys.stdout.flush()
            return result
        print(f"  {c('  ' + s['yn_hint'], GRAY)}")


def _interactive(lang: str) -> dict:
    s = T[lang]
    print()
    print(dbar())
    print(f"  🔑  {_logo()}  {c(s['int_title'], YEL)}")
    print(dbar())
    print()

    modes = f"[1] {s['int_mode_pw']}  [2] {s['int_mode_pp']}  [3] {s['int_mode_pin']}"
    mode = _ask(f"{s['int_mode']}  {c(modes, GRAY)}", "1")
    print()

    result: dict = {}
    skip = f"（{s['skip_hint']}）"

    if mode == "2":
        # ── Passphrase ──
        result["passphrase"] = True
        w = _ask(s["int_words"], "4")
        result["words"] = int(w) if w.isdigit() else 4
        sep = _ask(s["int_pp_sep"], "-")
        if sep != "-":
            result["separator"] = sep
        pfx = _ask(f"{s['int_prefix']}{skip}", "")
        if pfx: result["prefix"] = pfx
        sfx = _ask(f"{s['int_suffix']}{skip}", "")
        if sfx: result["suffix"] = sfx

    elif mode == "3":
        # ── PIN ──
        d = _ask(s["int_digits"], "6")
        result["pin"] = int(d) if d.isdigit() else 6

    else:
        # ── Password ──
        ln = _ask(s["int_length"], "12")
        result["length"] = int(ln) if ln.isdigit() else 12

        print()
        print(f"  {c('── ' + s['opts'] + ' ──', GRAY)}")
        result["strict"]     = _ask_yn(s["int_strict"],  lang)
        result["no_similar"] = _ask_yn(s["int_nosim"],   lang)

        advanced = _ask_yn(s["int_adv"], lang)
        if advanced:
            print()
            no_upper  = _ask_yn(s["int_no_upper"],  lang)
            no_lower  = _ask_yn(s["int_no_lower"],  lang)
            no_digits = _ask_yn(s["int_no_digits"], lang)
            no_symbols= _ask_yn(s["int_no_sym"],    lang)
            result["no_upper"]  = no_upper
            result["no_lower"]  = no_lower
            result["no_digits"] = no_digits
            result["no_symbols"]= no_symbols

            charset = _ask(f"{s['int_charset']}{skip}", "")
            if charset:
                result["charset"] = charset
                if no_upper or no_lower or no_digits or no_symbols:
                    print(c(f"  {s['warn_charset_override']}", YEL))
            else:
                if no_upper and no_lower and no_digits and no_symbols:
                    print(c(f"  {s['warn_all_off']}", RED))
                    sys.exit(1)
                if result["strict"] and (no_upper or no_lower or no_digits or no_symbols):
                    print(c(f"  {s['warn_strict_conflict']}", YEL))

            excl = _ask(f"{s['int_exclude']}{skip}", "")
            if excl: result["exclude_chars"] = excl

            print()
            sw_opts = f"[0] {s['int_sw_none']}  [1] {s['int_sw_lower']}  [2] {s['int_sw_upper']}{skip}"
            sw = _ask(f"{s['int_sw']}  {c(sw_opts, GRAY)}", "0")
            if sw == "1": result["starts_with"] = "lower"
            elif sw == "2": result["starts_with"] = "upper"

            sep = _ask(f"{s['int_separator']}{skip}", "")
            if sep:
                result["separator"] = sep
                every = _ask(s["int_every"], "4")
                result["every"] = int(every) if every.isdigit() else 4

            pfx = _ask(f"{s['int_prefix']}{skip}", "")
            if pfx: result["prefix"] = pfx
            sfx = _ask(f"{s['int_suffix']}{skip}", "")
            if sfx: result["suffix"] = sfx

    print()
    print(f"  {c('── ' + s['int_output'] + ' ──', GRAY)}")
    cnt = _ask(s["int_count"], "1")
    result["count"] = int(cnt) if cnt.isdigit() else 1
    result["copy"]  = _ask_yn(s["int_copy"],       lang)
    if _ask_yn(s["int_outfile_yn"], lang):
        outfile = _ask(s["int_outfile"], "")
        if outfile: result["output_file"] = outfile

    print()
    print(dbar())
    print()
    return result


# ── Entry point ───────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(prog="pgl", add_help=False)
    parser.add_argument("-i", "--interactive",  action="store_true")
    parser.add_argument("--pin",                type=int, default=None)
    parser.add_argument("--passphrase",         action="store_true")
    parser.add_argument("--words",              type=int, default=4)
    parser.add_argument("--wordlist",           type=str)
    parser.add_argument("-l", "--length",       type=int, default=12)
    parser.add_argument("--count",              type=int, default=1)
    parser.add_argument("--prefix",             type=str, default="")
    parser.add_argument("--suffix",             type=str, default="")
    parser.add_argument("--starts-with",         choices=["lower", "upper"], default=None)
    parser.add_argument("--no-upper",           action="store_true")
    parser.add_argument("--no-lower",           action="store_true")
    parser.add_argument("--no-digits",          action="store_true")
    parser.add_argument("--no-symbols",         action="store_true")
    parser.add_argument("--no-similar",         action="store_true")
    parser.add_argument("--exclude-chars",      type=str, default="")
    parser.add_argument("--strict",             action="store_true")
    parser.add_argument("--charset",            type=str)
    parser.add_argument("--separator",          type=str)
    parser.add_argument("--every",              type=int)
    parser.add_argument("--copy",               action="store_true")
    parser.add_argument("--add-date",           action="store_true")
    parser.add_argument("--add-user",           action="store_true")
    parser.add_argument("--output-format",      choices=["text", "json", "csv"], default="text")
    parser.add_argument("--output-file",        type=str)
    parser.add_argument("--save-profile",       type=str)
    parser.add_argument("--profile",            type=str)
    parser.add_argument("--list-profiles",      action="store_true")
    parser.add_argument("-u", "--update",       action="store_true")
    parser.add_argument("--lang",               default=None)
    parser.add_argument("-v", "--version",      action="store_true")
    parser.add_argument("-h", "--help",         action="store_true")

    args = parser.parse_args()
    lang = _detect_lang(args.lang)
    s = T[lang]

    if args.version:
        print(f"pgl v{__version__}")
        return

    if args.help:
        show_help(lang)
        return

    if args.list_profiles:
        _list_profiles(lang)
        return

    remote = fetch_remote_version()

    if args.update:
        do_update(remote, lang)
        return

    if remote and _is_newer(remote):
        auto_update(remote, lang)

    # Load profile
    if args.profile:
        profiles = _load_profiles()
        if args.profile not in profiles:
            print(c(s["prof_missing"].format(args.profile), RED))
            sys.exit(1)
        for key, val in profiles[args.profile].items():
            attr = key.replace("-", "_")
            if not getattr(args, attr, None):
                setattr(args, attr, val)

    # Interactive mode
    if args.interactive:
        opts = _interactive(lang)
        if "passphrase" in opts:
            args.passphrase = True
            args.words      = opts.get("words", 4)
            args.separator  = opts.get("separator", args.separator)
            args.prefix     = opts.get("prefix", args.prefix)
            args.suffix     = opts.get("suffix", args.suffix)
        elif "pin" in opts:
            args.pin = opts.get("pin", 6)
        else:
            args.length      = opts.get("length", 12)
            args.strict      = opts.get("strict", False)
            args.no_similar  = opts.get("no_similar", False)
            args.no_upper    = opts.get("no_upper",   False)
            args.no_lower    = opts.get("no_lower",   False)
            args.no_digits   = opts.get("no_digits",  False)
            args.no_symbols  = opts.get("no_symbols", False)
            args.charset     = opts.get("charset",    args.charset)
            args.exclude_chars = opts.get("exclude_chars", args.exclude_chars)
            args.prefix      = opts.get("prefix", args.prefix)
            args.suffix      = opts.get("suffix", args.suffix)
            args.separator   = opts.get("separator", args.separator)
            args.every       = opts.get("every",   args.every)
            args.count       = opts.get("count", 1)
        args.copy        = opts.get("copy",  False)
        args.output_file = opts.get("output_file", args.output_file)

    # No generation intent → info screen
    generation_intent = (
        args.interactive or args.pin is not None or args.passphrase or args.profile or
        args.no_upper or args.no_lower or args.no_digits or args.no_symbols or
        args.strict or args.no_similar or args.charset or
        args.count != 1 or args.length != 12 or args.prefix or args.suffix or
        args.copy or args.output_file or args.add_date or args.add_user or
        args.exclude_chars or args.separator or args.every or args.starts_with
    )
    if not generation_intent:
        show_info(remote, lang)
        return

    if args.add_date:
        args.prefix = datetime.datetime.now().strftime("%Y%m%d") + args.prefix
    if args.add_user:
        args.prefix = getpass.getuser() + args.prefix

    # Conflict validation (password mode only)
    if not args.passphrase and args.pin is None:
        if args.every and not args.separator:
            print(c(f"  {s['warn_every_no_sep']}", YEL))
            args.separator = "-"
        if args.charset and (args.no_upper or args.no_lower or args.no_digits or args.no_symbols or args.exclude_chars):
            print(c(f"  {s['warn_charset_override']}", YEL))
        if not args.charset and args.no_upper and args.no_lower and args.no_digits and args.no_symbols:
            print(c(f"  {s['warn_all_off']}", RED))
            sys.exit(1)

    # starts_with: from interactive opts or CLI flag
    starts_with = None
    if args.interactive:
        starts_with = opts.get("starts_with")
    elif args.starts_with:
        starts_with = args.starts_with

    # Entropy
    if args.pin is not None:
        bits = math.log2(10) * args.pin
    elif args.passphrase:
        wl = _load_wordlist(args.wordlist)
        bits = math.log2(len(wl)) * args.words
    else:
        ps = _pool_size(
            not args.no_upper, not args.no_lower, not args.no_digits, not args.no_symbols,
            args.no_similar, args.exclude_chars, args.charset
        )
        bits = _entropy(ps, args.length)

    output = []
    print()

    if args.interactive:
        _show_settings_summary(args, starts_with, lang)
        print()

    try:
        for i in range(args.count):
            if args.pin is not None:
                pw = generate_pin(args.pin)
            elif args.passphrase:
                pw = generate_passphrase(args.words, args.wordlist, args.separator or "-")
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
                    charset=args.charset,
                    separator=args.separator,
                    every=args.every,
                )
            output.append(pw)
            idx = i + 1 if args.count > 1 else None
            _show_password(pw, bits, lang, index=idx)
            if args.count > 1:
                print()

    except ValueError as e:
        print(c(f"  ✗  {s.get(str(e), str(e))}", RED))
        sys.exit(1)

    print()

    if args.copy:
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(output[-1])
            print(c(f"  {s['copied']}", GREEN))
            print()
        else:
            print(c(f"  {s['copy_fail']}", YEL))
            print()

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            if args.output_format == "json":
                json.dump(output, f, ensure_ascii=False, indent=2)
            else:
                f.write("\n".join(output))
        print(c(f"  {s['saved'].format(args.output_file)}", GREEN))
        print()

    if args.save_profile:
        profile_data: dict = {}
        if args.passphrase:
            profile_data["passphrase"] = True
            profile_data["words"] = args.words
            if args.separator: profile_data["separator"] = args.separator
        elif args.pin is not None:
            profile_data["pin"] = args.pin
        else:
            profile_data["length"] = args.length
            if args.no_upper:    profile_data["no_upper"]    = True
            if args.no_lower:    profile_data["no_lower"]    = True
            if args.no_digits:   profile_data["no_digits"]   = True
            if args.no_symbols:  profile_data["no_symbols"]  = True
            if args.strict:      profile_data["strict"]      = True
            if args.no_similar:  profile_data["no_similar"]  = True
            if args.charset:     profile_data["charset"]     = args.charset
            if args.exclude_chars: profile_data["exclude_chars"] = args.exclude_chars
            if starts_with:      profile_data["starts_with"] = starts_with
            if args.separator:   profile_data["separator"]   = args.separator
            if args.every:       profile_data["every"]       = args.every
        if args.prefix:   profile_data["prefix"]  = args.prefix
        if args.suffix:   profile_data["suffix"]  = args.suffix
        if args.count > 1: profile_data["count"]  = args.count
        _save_profile(args.save_profile, profile_data)
        print(c(f"  {s['prof_saved'].format(args.save_profile)}", GREEN))
        print()


if __name__ == "__main__":
    main()
