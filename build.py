#!/usr/bin/env python3
"""
build.py — mdファイルを prompts.json に変換するスクリプト
使い方: python build.py
※ このスクリプトを WEBプロジェクト/ フォルダに置いて実行してください
"""

import os
import json
import re
from pathlib import Path

# ── 設定 ──────────────────────────────────────────
ROOT = Path(__file__).parent          # このスクリプトと同じフォルダ
OUTPUT = ROOT / "prompts.json"        # 出力先
EXCLUDE_DIRS  = {".git", "node_modules", "__pycache__"}
EXCLUDE_FILES = {"README.md", "readme.md"}
# ────────────────────────────────────────────────

# カテゴリごとのアイコン（フォルダ名に含まれるキーワードで自動判定）
ICON_MAP = [
    (["LP", "ランディング", "landing"], "🖥️"),
    (["AI", "人工知能", "GPT", "ChatGPT"], "🤖"),
    (["ライティング", "writing", "コピー", "セールス"], "✍️"),
    (["ビジネス", "business", "業務"], "💼"),
    (["分析", "リサーチ", "調査", "research"], "🔍"),
    (["マーケ", "marketing", "広告", "SNS"], "📣"),
    (["エキスパ", "システム", "system"], "⚙️"),
    (["その他", "other", "misc"], "📂"),
]

def get_icon(name: str) -> str:
    for keywords, icon in ICON_MAP:
        if any(k.lower() in name.lower() for k in keywords):
            return icon
    return "📄"

def parse_md(content: str, filepath: Path) -> list[dict]:
    """
    mdファイルを解析してプロンプトのリストを返す。
    ## 見出し か ### 見出し を区切りとして分割。
    見出しがない場合はファイル全体を1プロンプトとして扱う。
    """
    prompts = []

    # H1/H2/H3 を区切りとして分割
    sections = re.split(r'\n(?=#{1,3} )', content.strip())

    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue

        # 見出し行を検出
        heading_match = re.match(r'^(#{1,3})\s+(.+)', lines[0])

        if heading_match:
            title = heading_match.group(2).strip()
            body_lines = lines[1:]
        else:
            # 見出しなし → ファイル名をタイトルに
            title = filepath.stem
            body_lines = lines

        body = "\n".join(body_lines).strip()
        if not body:
            continue

        # 最初の非空行を description に
        desc_match = re.search(r'^([^\n#`]{5,})', body)
        desc = desc_match.group(1).strip()[:80] if desc_match else ""

        # #タグ 抽出（日本語タグも対応）
        tags = re.findall(r'#([\w\u3040-\u9FFF\u4E00-\u9FFF]+)', body)

        prompts.append({
            "title": title,
            "desc": desc,
            "content": body,
            "tags": list(dict.fromkeys(tags)),  # 重複除去
            "file": str(filepath.relative_to(ROOT)),
        })

    return prompts


def build():
    data = []
    # 直下のmdファイル（フォルダ外のもの）
    root_prompts = []
    for md_file in sorted(ROOT.glob("*.md")):
        if md_file.name in EXCLUDE_FILES:
            continue
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        prompts = parse_md(content, md_file)
        root_prompts.extend(prompts)

    if root_prompts:
        data.append({
            "category": "ルート",
            "icon": "🏠",
            "prompts": root_prompts,
        })

    # サブフォルダ内のmdファイル
    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name in EXCLUDE_DIRS or folder.name.startswith("."):
            continue

        category_prompts = []
        # サブフォルダ内のmd（再帰的に検索）
        for md_file in sorted(folder.rglob("*.md")):
            if md_file.name in EXCLUDE_FILES:
                continue
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            prompts = parse_md(content, md_file)
            # サブフォルダが深い場合、ファイルのパスをタグに追加
            sub = md_file.relative_to(folder)
            if len(sub.parts) > 1:
                for p in prompts:
                    p["tags"].insert(0, sub.parts[0])
            category_prompts.extend(prompts)

        if category_prompts:
            data.append({
                "category": folder.name,
                "icon": get_icon(folder.name),
                "prompts": category_prompts,
            })

    # 出力
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    total = sum(len(c["prompts"]) for c in data)
    print(f"✅ 完了！  カテゴリ: {len(data)}  プロンプト: {total}  → {OUTPUT}")
    for cat in data:
        print(f"   {cat['icon']} {cat['category']}  ({len(cat['prompts'])}件)")


if __name__ == "__main__":
    build()
