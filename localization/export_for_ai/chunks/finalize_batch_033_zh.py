# -*- coding: utf-8 -*-
"""Generate batch_033 *.zh.json from hand translations + MT for costume chunks."""
from __future__ import annotations

import importlib.util
import json
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator

CHUNK_DIR = Path(__file__).resolve().parent
STEMS = [f"batch_033_p{i:02d}" for i in range(6)]

# Load hand-crafted p00-p02 (partial p02 may be fixed below)
spec = importlib.util.spec_from_file_location("hand", CHUNK_DIR / "_write_batch_033_zh.py")
hand_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hand_mod)
T: dict[str, dict[str, str]] = dict(hand_mod.T)

GLOSSARY = [
    (r"\bPeashooter\b", "豌豆射手"),
    (r"\bSunflower\b", "向日葵"),
    (r"\bTwin Sunflower\b", "双子向日葵"),
    (r"\bWall-nut\b", "坚果墙"),
    (r"\bTall-nut\b", "高坚果"),
    (r"\bPrimal Wall-nut\b", "原始坚果墙"),
    (r"\bCherry Bomb\b", "樱桃炸弹"),
    (r"\bPotato Mine\b", "土豆地雷"),
    (r"\bChomper\b", "大嘴花"),
    (r"\bRepeater\b", "双发射手"),
    (r"\bSnow Pea\b", "寒冰射手"),
    (r"\bThreepeater\b", "三线射手"),
    (r"\bSplit Pea\b", "分裂豌豆"),
    (r"\bTorchwood\b", "火炬树桩"),
    (r"\bHypnoshroom\b", "魅惑菇"),
    (r"\bFume-shroom\b", "大喷菇"),
    (r"\bPuff-shroom\b", "小喷菇"),
    (r"\bScaredy-shroom\b", "胆小菇"),
    (r"\bMagnet-shroom\b", "磁力菇"),
    (r"\bSun-shroom\b", "阳光菇"),
    (r"\bSpikeweed\b", "地刺"),
    (r"\bSpikerock\b", "钢地刺"),
    (r"\bKernel-pult\b", "玉米投手"),
    (r"\bMelon-pult\b", "西瓜投手"),
    (r"\bCabbage-pult\b", "卷心菜投手"),
    (r"\bBlover\b", "三叶草"),
    (r"\bImitater\b", "模仿者"),
    (r"\bPower Lily\b", "能量百合"),
    (r"\bPlant Food\b", "植物食物"),
    (r"\bGargantuar\b", "巨人僵尸"),
    (r"\bImp\b", "小鬼僵尸"),
    (r"\bDr\. Zomboss\b", "僵王博士"),
    (r"\bZomboss\b", "僵王"),
    (r"\bGreen Shadow\b", "绿影侠"),
    (r"\bSolar Flare\b", "热情火焰"),
    (r"\bCaptain Combustible\b", "火爆队长"),
    (r"\bBeta-Carrotina\b", "贝塔-胡萝卜蒂娜"),
    (r"\bSpudow\b", "土豆雷"),
    (r"\bChompzilla\b", "吞吞兽"),
    (r"\bPiñata\b", "皮纳塔"),
    (r"\bPinata\b", "皮纳塔"),
    (r"\bPremium and World plants\b", "高级与世界植物"),
    (r"\bseed packets\b", "种子包"),
    (r"\bSeed Packets\b", "种子包"),
    (r"\bCoins\b", "金币"),
    (r"\bGems\b", "宝石"),
    (r"\bGauntlets\b", "手套"),
    (r"\bBONUS\b", "额外赠送"),
    (r"\bSavings\b", "优惠"),
    (r"\bLevel 2\b", "2 级"),
    (r"\bLevel 3\b", "3 级"),
]

HAS_LATIN = re.compile(r"[A-Za-z]{3,}")


def apply_glossary(text: str) -> str:
    for pat, repl in GLOSSARY:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text


def mt_translate(text: str, translator: GoogleTranslator) -> str:
    # Preserve explicit line breaks and placeholders
    text = text.replace("\r\n", "\n")
    parts = re.split(r"(\{[^}]+\}|%[sd]|%\d+\$[sd]|\{0\})", text)
    out: list[str] = []
    for part in parts:
        if not part or re.fullmatch(r"(\{[^}]+\}|%[sd]|%\d+\$[sd]|\{0\})", part):
            out.append(part)
            continue
        if not part.strip():
            out.append(part)
            continue
        try:
            zh = translator.translate(part)
        except Exception:
            time.sleep(0.5)
            zh = translator.translate(part)
        out.append(zh if zh else part)
    result = "".join(out)
    return apply_glossary(result)


def needs_retranslate(value: str) -> bool:
    # Allow short codes / stylized names
    for token in ("D.E.A.F.", "L.E.A.F.", "S795", "C.H.E.N", "3l3ctro", "MPea3", "M310N", "PU17"):
        value = value.replace(token, "")
    return bool(HAS_LATIN.search(value))


def main() -> None:
    translator = GoogleTranslator(source="en", target="zh-CN")
    report: list[str] = []

    for stem in STEMS:
        src_path = CHUNK_DIR / f"{stem}.json"
        src: dict[str, str] = json.loads(src_path.read_text(encoding="utf-8"))
        out_map: dict[str, str] = {}

        existing = T.get(stem, {})
        for key, en in src.items():
            if key in existing and not needs_retranslate(existing[key]):
                out_map[key] = existing[key]
            else:
                out_map[key] = mt_translate(en, translator)
                time.sleep(0.05)

        if set(out_map.keys()) != set(src.keys()):
            raise SystemExit(f"Key mismatch for {stem}")

        out_path = CHUNK_DIR / f"{stem}.zh.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(out_map, f, ensure_ascii=False, indent=2)
            f.write("\n")
        report.append(f"{stem}: {len(out_map)} keys -> {out_path.name}")

    print("\n".join(report))


if __name__ == "__main__":
    main()
