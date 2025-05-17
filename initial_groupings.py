import sys
from pathlib import Path
from collections import defaultdict, deque

tier = sys.argv[1] if len(sys.argv) > 1 else "tier1"

verdict_path = Path(f"verdicts/{tier}/hashing/verdict.txt")
group_output_dir = Path(f"groups/{tier}")
group_output_dir.mkdir(parents=True, exist_ok=True)

# Threshold for similarity
THRESHOLD = 10

similarity_graph = defaultdict(set)
all_files = set()

with open(verdict_path, "r") as f:
    for line in f:
        if "->" not in line:
            continue
        parts = line.strip().split(" = ")
        if len(parts) != 2:
            continue
        files_part, diff_str = parts
        file1, file2 = [s.strip().replace(".html", "") for s in files_part.split("->")]
        all_files.update([file1, file2])  
        try:
            diff = int(diff_str)
        except ValueError:
            continue
        if diff < THRESHOLD:
            similarity_graph[file1].add(file2)
            similarity_graph[file2].add(file1)

ungrouped_files = set(similarity_graph.keys())
groups = []
group_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
file_to_group = {}

while ungrouped_files:
    current_group = set()
    queue = deque()
    seed = ungrouped_files.pop()
    current_group.add(seed)
    queue.append(seed)

    while queue:
        node = queue.popleft()
        for neighbor in similarity_graph[node]:
            if neighbor in ungrouped_files:
                ungrouped_files.remove(neighbor)
                current_group.add(neighbor)
                queue.append(neighbor)

    groups.append(sorted(current_group))

connected_files = set(file for group in groups for file in group)
singleton_files = all_files - connected_files

for singleton in singleton_files:
    groups.append([singleton])

for idx, group in enumerate(groups):
    group_letter = group_names[idx] if idx < len(group_names) else f"group{idx+1}"
    group_file = group_output_dir / f"group{group_letter}.txt"

    with open(group_file, "w") as f:
        for filename in group:
            f.write(f"{filename}.html\n")
            file_to_group[filename] = group_letter

for filename, group_letter in sorted(file_to_group.items()):
    print(f"{filename}.html -> Group {group_letter}")

print(f"\n Grouping complete. {len(groups)} groups saved to {group_output_dir}")
