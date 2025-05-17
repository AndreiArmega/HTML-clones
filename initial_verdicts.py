import sys
import subprocess
from pathlib import Path
from itertools import combinations
from tqdm import tqdm  


screenshots_root = Path("./screenshots")
verdicts_root = Path("./verdicts")

# Threshold to decide whether DL result is very good
DL_THRESHOLD = 0.95

def run_hashing(png1: Path, png2: Path) -> int:
    result = subprocess.run(
        ["python", "./jurors/hashing.py", str(png1), str(png2)],
        capture_output=True,
        text=True,
    )
    for line in result.stdout.strip().splitlines():
        if "->" in line and "=" in line:
            try:
                return int(line.strip().split(" = ")[-1])
            except ValueError:
                return None
    return None

def run_deep_learning(png1: Path, png2: Path) -> float:
    result = subprocess.run(
        ["python", "./jurors/deeplearn.py", str(png1), str(png2)],
        capture_output=True,
        text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0  

def process_tier(tier_dir: Path):
    tier_name = tier_dir.name
    screenshots = sorted(tier_dir.glob("*.png"))

    if len(screenshots) < 2:
        return

    verdict_path = verdicts_root / tier_name / "hashing"
    verdict_path.mkdir(parents=True, exist_ok=True)
    verdict_file = verdict_path / "verdict.txt"

    all_pairs = list(combinations(screenshots, 2))

    with open(verdict_file, "a") as vf:
        for img1, img2 in tqdm(all_pairs, desc=f"{tier_name} progress", unit="pair"):
            hash_diff = run_hashing(img1, img2)
            if hash_diff is None:
                continue

            dl_score = run_deep_learning(img1, img2)

            if dl_score >= DL_THRESHOLD:
                adjusted_diff = round(hash_diff / 2)
            else:
                adjusted_diff = hash_diff

            vf.write(f"{img1.stem}.html -> {img2.stem}.html = {adjusted_diff}\n")

def main():
    tier_arg = sys.argv[1] if len(sys.argv) > 1 else None

    if tier_arg:
        tier_path = screenshots_root / tier_arg
        if tier_path.exists() and tier_path.is_dir():
            process_tier(tier_path)

    else:
        for tier_dir in screenshots_root.iterdir():
            if tier_dir.is_dir():
                process_tier(tier_dir)

if __name__ == "__main__":
    main()
