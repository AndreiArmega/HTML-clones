import sys
import subprocess
from pathlib import Path
import re

tier = sys.argv[1] if len(sys.argv) > 1 else "tier1"

group_dir = Path(f"./groups/{tier}")
comparison_scripts = {
    "ssim": Path("./jurors/ssim.py"),
    "orb": Path("./jurors/orb.py"),
    "histogram": Path("./jurors/histogram.py"),
}

# Helpers
def get_group_files():
    return sorted(group_dir.glob("group*.txt"), key=lambda p: p.stem)

def extract_group_name(path):
    match = re.search(r"group([A-Z])", path.stem)
    return match.group(1) if match else None

def run_script(script_path, file1, file2):
    try:
        result = subprocess.run(
            ["python", str(script_path), str(file1), str(file2)],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout.strip()
        return float(output)
    except Exception as e:
        print(f"Error running {script_path.name} on {file1} and {file2}: {e}")
        return 0

def compare_files(file1, file2):
    orb_score = run_script(comparison_scripts["orb"], file1, file2)
    if orb_score == 0:
        return 0

    ssim_score = run_script(comparison_scripts["ssim"], file1, file2)

    hist_score = run_script(comparison_scripts["histogram"], file1, file2)

    final_score = (ssim_score + hist_score) / 2
    return final_score

# Main logic
def regroup():
    group_files = get_group_files()
    if len(group_files) <= 5:
        print(" Already at or below minimum group count.")
        return

    target_group_count = max(5, len(group_files) - (ord(group_files[-1].stem[-1]) - ord('A')))

    index = len(group_files) - 1
    while index >= 0 and len(get_group_files()) > target_group_count:
        group_file = get_group_files()[index]
        group_name = extract_group_name(group_file)
        lines = group_file.read_text().splitlines()

        if len(lines) != 1:
            index -= 1
            continue  

        single_file = lines[0].strip()
        single_path = Path(f"./screenshots/{tier}") / Path(single_file).with_suffix(".png")

        best_score = -1
        best_group = None

        for earlier_group_file in get_group_files()[:index]:
            earlier_lines = earlier_group_file.read_text().splitlines()
            if not earlier_lines:
                continue

            group_scores = []
            
            for compare_filename in earlier_lines[:3]:  # Compare with up to 3 files
                compare_file = Path(f"./screenshots/{tier}") / Path(compare_filename).with_suffix(".png")
                score = compare_files(single_path, compare_file)
                group_scores.append(score)

            if group_scores:
                avg_score = sum(group_scores) / len(group_scores)

                if avg_score > best_score:
                    best_score = avg_score
                    best_group = earlier_group_file

        if best_group:
            with open(best_group, "a") as f:
                f.write(f"{single_file}\n")

            group_file.unlink()
        else:
            print(" No suitable group found. Skipping.")
        index -= 1


if __name__ == "__main__":
    regroup()
