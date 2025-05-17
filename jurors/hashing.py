import sys
from pathlib import Path
from PIL import Image
import imagehash

def compute_hash_difference(png1: Path, png2: Path) -> str:
    if not png1.exists() or not png2.exists():
        return f" Screenshot(s) missing for: {png1}, {png2}"

    img1 = Image.open(png1)
    img2 = Image.open(png2)

    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)
    diff = hash1 - hash2

    verdict_line = f"{png1.stem}.html -> {png2.stem}.html = {diff}"
    return verdict_line

def main():
    if len(sys.argv) != 3:
        print("Usage: python hashing.py <screenshot1.png> <screenshot2.png>")
        sys.exit(1)

    screenshot1 = Path(sys.argv[1])
    screenshot2 = Path(sys.argv[2])

    verdict = compute_hash_difference(screenshot1, screenshot2)
    print(verdict)

if __name__ == "__main__":
    main()
