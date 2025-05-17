#!/bin/bash

set -euo pipefail


python ss_maker.py


tiers=("tier1" "tier2" "tier3" "tier4")

for tier in "${tiers[@]}"; do
  python initial_verdicts.py "$tier"
  python initial_groupings.py "$tier"
done

for tier in "${tiers[@]}"; do
  python final_groupings.py "$tier"
done

