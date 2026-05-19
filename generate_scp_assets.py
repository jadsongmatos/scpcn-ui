#!/usr/bin/env python3
"""
Gerador de assets SCP para conversao warcraftcn-ui → scpcn-ui.
Gera imagens SCP-themed via OpenRouter (Gemini) para substituir assets Warcraft.

Classificacoes SCP (substituindo faccoes Warcraft):
  default → safe     (verde clinico)
  human   → euclid   (ambar/cautela)
  orc     → keter    (vermelho perigo)
  elf     → thaumiel (roxo esoterico)
  undead  → apollyon (vermelho-escuro/existencial)
"""

import requests
import base64
import json
import time
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemini-3.1-flash-image-preview"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

ASSETS_DIR = Path(__file__).parent / "components" / "ui" / "warcraftcn" / "assets_scp"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SCP_CLASSIFICATIONS = ["safe", "euclid", "keter", "thaumiel", "apollyon"]

SCP_COLORS = {
    "safe":     "green clinical #33cc33",
    "euclid":   "amber caution #ccaa33",
    "keter":    "red danger #cc3333",
    "thaumiel": "purple esoteric #9933cc",
    "apollyon": "dark crimson existential #660011",
}

STYLE_BASE = (
    "SCP Foundation UI component asset. Dark bureaucratic institutional aesthetic. "
    "Clinical, sterile, ominous. Black/dark gray base with SCP classification color accents. "
    "No text, no letters, no words. No people. Seamless tileable border/frame texture. "
    "WebP quality, clean edges for border-image-slice usage."
)

ASSETS = []

def _add(id_name, filename, prompt, aspect_ratio="1:1"):
    ASSETS.append({"id": id_name, "filename": filename, "prompt": prompt, "aspect_ratio": aspect_ratio})

# --- BUTTON BACKGROUNDS ---
_add("button-bg", "button-bg.webp",
    f"{STYLE_BASE} A wide horizontal button border frame. Dark steel gray background with thin red border lines. "
    "Industrial metal texture with rivets along the edges. SCP containment facility door style. "
    "Border-frame texture suitable for CSS border-image-slice:16. Dimensions roughly 1552x249. Horizontal elongated rectangle.",
    aspect_ratio="16:9")

_add("button-bg-sm", "button-bg-sm.webp",
    f"{STYLE_BASE} A smaller horizontal button border frame. Same style as the full button but compact. "
    "Dark steel gray with red accent lines. Industrial containment door style. "
    "Border-frame texture for CSS border-image-slice. Dimensions roughly 776x239.",
    aspect_ratio="4:1")

_add("button-bg-with-frame", "button-bg-with-frame.webp",
    f"{STYLE_BASE} A wide horizontal button border frame with an outer decorative frame/border. "
    "Dark metal with raised border, red accent stripe inside. Containment protocol button style. "
    "Border-frame texture for CSS border-image-slice:16. Dimensions roughly 2048x512.",
    aspect_ratio="4:1")

_add("button-bg-with-frame-sm", "button-bg-with-frame-sm.webp",
    f"{STYLE_BASE} A smaller horizontal button with outer decorative frame. "
    "Compact version of the framed button. Dark metal, red accent. "
    "Border-frame texture for CSS border-image-slice. Dimensions roughly 1500x500.",
    aspect_ratio="4:1")

# --- CARD BACKGROUND ---
_add("card-bg", "card-bg.webp",
    f"{STYLE_BASE} A card/document border frame. Dark gray bureaucratic document folder texture. "
    "Red thin border lines with corner marks like a classified document. "
    "Clean edges for border-image-slice:24. Rectangular frame. Dimensions roughly 560x720.",
    aspect_ratio="3:4")

# --- INPUT/TEXTAREA/DROPDOWN FRAMES ---
_add("input-frame", "input-frame.webp",
    f"{STYLE_BASE} A horizontal input field border frame. Dark recessed panel with thin red border. "
    "Industrial console input style, like a containment facility terminal. "
    "Border-frame for CSS border-image-slice. Elongated horizontal. Dimensions roughly 2048x400.",
    aspect_ratio="4:1")

_add("textarea-bg", "textarea-bg.webp",
    f"{STYLE_BASE} A rectangular text area border frame. Dark panel with red border lines. "
    "Multi-line terminal input style. Containment facility document form. "
    "Border-frame for CSS border-image-slice. Dimensions roughly 949x494.",
    aspect_ratio="4:3")

_add("dropdown-menu-bg", "dropdown-menu-bg.webp",
    f"{STYLE_BASE} A dropdown menu panel border frame. Dark dropdown panel with red accent border. "
    "List menu background, institutional style. "
    "Border-frame for CSS border-image-slice. Dimensions roughly 949x494.",
    aspect_ratio="4:3")

# --- ACCORDION ---
_add("accordion-header", "accordion-header.webp",
    f"{STYLE_BASE} A horizontal accordion header bar. Dark panel header with red left accent stripe. "
    "Classified document section header style. Clean bottom edge. "
    "Dimensions roughly 2716x406.",
    aspect_ratio="8:1")

_add("accordion-content-bg", "accordion-content-bg.webp",
    f"{STYLE_BASE} A rectangular accordion content area background. Dark panel with subtle border. "
    "Document content section background, institutional. "
    "Dimensions roughly 2256x1136.",
    aspect_ratio="4:3")

# --- AVATAR FRAMES (5 classifications) ---
for cls in SCP_CLASSIFICATIONS:
    color_desc = SCP_COLORS[cls]
    _add(f"avatar-{cls}", f"avatar-{cls}.webp",
        f"{STYLE_BASE} A square avatar frame border. {color_desc} accent color border/frame. "
        f"SCP classification level frame. Dark center area for portrait photo. "
        f"Classified personnel badge style. Ornate corners with classification symbol. "
        f"1024x1024 square.",
        aspect_ratio="1:1")

# --- CHECKBOX IMAGES (5 classifications × 2 states = 10) ---
for cls in SCP_CLASSIFICATIONS:
    color_desc = SCP_COLORS[cls]
    _add(f"checkbox-{cls}", f"checkbox-{cls}.webp",
        f"{STYLE_BASE} A small unchecked checkbox. {color_desc} accent. "
        f"Dark square with thin border, empty inside. Institutional form checkbox. "
        f"Small icon 160x160.",
        aspect_ratio="1:1")
    _add(f"checkbox-{cls}-checked", f"checkbox-{cls}-checked.webp",
        f"{STYLE_BASE} A small checked checkbox. {color_desc} accent. "
        f"Dark square with border, contains a checkmark or classification stamp mark inside. "
        f"Institutional form checkbox. Small icon 160x160.",
        aspect_ratio="1:1")

# --- TAB IMAGES (5 classifications × 3 types = 15) ---
for cls in SCP_CLASSIFICATIONS:
    color_desc = SCP_COLORS[cls]
    _add(f"tab-list-{cls}", f"tabs/tab-list-{cls}.webp",
        f"{STYLE_BASE} A horizontal tab button background. {color_desc} accent color. "
        f"Inactive/unselected tab. Dark panel with thin colored top border. "
        f"Institutional folder tab style. 300x100.",
        aspect_ratio="4:1")
    _add(f"tab-list-active-{cls}", f"tabs/tab-list-active-{cls}.webp",
        f"{STYLE_BASE} A horizontal tab button background, ACTIVE/SELECTED state. {color_desc} accent color. "
        f"Active tab with brighter color, highlighted. Bottom edge open (connects to content). "
        f"Institutional folder tab style. 300x100.",
        aspect_ratio="4:1")
    _add(f"tab-content-{cls}", f"tabs/tab-content-{cls}.webp",
        f"{STYLE_BASE} A tab content panel background. {color_desc} accent border on top edge. "
        f"Dark document panel with subtle classification color accent. "
        f"Institutional document viewer style. 612x408.",
        aspect_ratio="3:2")

# --- TOAST IMAGES (5 classifications × 2 types = 10) ---
for cls in SCP_CLASSIFICATIONS:
    color_desc = SCP_COLORS[cls]
    _add(f"toast-content-{cls}", f"toast/scroll-content-{cls}.webp",
        f"{STYLE_BASE} A horizontal notification/document strip background. {color_desc} accent. "
        f"Dark notification panel with colored top stripe. "
        f"SCP alert/document slip style. 300x100.",
        aspect_ratio="4:1")
    _add(f"toast-handle-{cls}", f"toast/scroll-handle-{cls}.png",
        f"{STYLE_BASE} A very narrow vertical handle/edge piece. {color_desc} accent. "
        f"Thin vertical strip, dark with colored accent line. "
        f"Document edge/handle. 20x100.",
        aspect_ratio="1:4")


def generate_image(prompt: str, aspect_ratio: str = "1:1") -> str | None:
    messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": MODEL,
        "messages": messages,
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": aspect_ratio,
            "image_size": "1K",
        },
    }

    import socket
    original_getaddrinfo = socket.getaddrinfo

    def _force_ipv4(*args, **kwargs):
        host = args[0] if len(args) >= 1 else kwargs.get('host')
        port = args[1] if len(args) >= 2 else kwargs.get('port')
        type_ = args[3] if len(args) >= 4 else kwargs.get('type', 0)
        proto = args[4] if len(args) >= 5 else kwargs.get('proto', 0)
        flags = args[5] if len(args) >= 6 else kwargs.get('flags', 0)
        return original_getaddrinfo(host, port, socket.AF_INET, type_, proto, flags)

    for attempt in range(3):
        try:
            socket.getaddrinfo = _force_ipv4
            resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=180)
            socket.getaddrinfo = original_getaddrinfo

            resp.raise_for_status()
            result = resp.json()

            if "choices" in result and len(result["choices"]) > 0:
                msg = result["choices"][0]["message"]
                if "images" in msg and len(msg["images"]) > 0:
                    img_data = msg["images"][0]["image_url"]["url"]
                    if "base64," in img_data:
                        return img_data.split("base64,", 1)[1]
                    return img_data

            socket.getaddrinfo = original_getaddrinfo

            print(f"  No image in response.", flush=True)
            if "error" in result:
                print(f"  API Error: {result['error']}", flush=True)

        except requests.exceptions.HTTPError as e:
            socket.getaddrinfo = original_getaddrinfo
            print(f"  HTTP Error (attempt {attempt+1}): {e}", flush=True)
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response: {e.response.text[:300]}", flush=True)
        except Exception as e:
            socket.getaddrinfo = original_getaddrinfo
            print(f"  Error (attempt {attempt+1}): {e}", flush=True)

        if attempt < 2:
            socket.getaddrinfo = original_getaddrinfo
            wait = 15 * (attempt + 1)
            print(f"  Retrying in {wait}s...", flush=True)
            time.sleep(wait)

    socket.getaddrinfo = original_getaddrinfo
    return None


def save_image(b64_data: str, filepath: Path) -> bool:
    try:
        img_bytes = base64.b64decode(b64_data)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(img_bytes)
        size_kb = len(img_bytes) / 1024
        print(f"  Saved: {filepath} ({size_kb:.0f} KB)", flush=True)
        return True
    except Exception as e:
        print(f"  Failed to save {filepath}: {e}", flush=True)
        return False


def process_asset(asset: dict) -> tuple[str, bool]:
    aid = asset["id"]
    filename = asset["filename"]
    prompt = asset["prompt"]
    aspect = asset["aspect_ratio"]

    outpath = ASSETS_DIR / filename
    if outpath.exists():
        existing_kb = outpath.stat().st_size / 1024
        if existing_kb > 5:
            print(f"[{aid}] SKIP (exists, {existing_kb:.0f}KB): {outpath}", flush=True)
            return (aid, True)

    print(f"[{aid}] Generating {filename}...", flush=True)
    img_b64 = generate_image(prompt, aspect)

    if img_b64:
        ok = save_image(img_b64, outpath)
        return (aid, ok)
    else:
        print(f"[{aid}] FAILED", flush=True)
        return (aid, False)


def main():
    print(f"SCP Asset Generator")
    print(f"===================")
    print(f"Total assets to generate: {len(ASSETS)}")
    print(f"Output dir: {ASSETS_DIR}")
    print()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "tabs").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "toast").mkdir(parents=True, exist_ok=True)

    results = {}
    sequential_assets = []
    batch_assets = []

    for a in ASSETS:
        outpath = ASSETS_DIR / a["filename"]
        if outpath.exists() and outpath.stat().st_size > 5000:
            sequential_assets.append(a)
        else:
            batch_assets.append(a)

    for a in sequential_assets:
        aid, ok = process_asset(a)
        results[aid] = ok

    max_workers = 2
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_asset, a): a for a in batch_assets}
        for future in as_completed(futures):
            try:
                aid, ok = future.result()
                results[aid] = ok
            except Exception as e:
                a = futures[future]
                print(f"[{a['id']}] Exception: {e}", flush=True)
                results[a["id"]] = False

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    ok_count = sum(1 for v in results.values() if v)
    fail_count = sum(1 for v in results.values() if not v)
    print(f"\nGenerated: {ok_count}/{len(ASSETS)}")

    if fail_count > 0:
        failed = [aid for aid, ok in results.items() if not ok]
        print(f"Failed: {fail_count} — {failed}")
    else:
        print("All assets generated successfully!")


if __name__ == "__main__":
    main()
