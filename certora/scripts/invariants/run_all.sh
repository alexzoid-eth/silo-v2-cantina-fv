#!/bin/bash
# Use the first argument as the pattern. If no argument is provided, match all files.
pattern="${1:-}"

DIRS=(
  "certora/confs/invariants/debt"
  "certora/confs/invariants/silo"
  "certora/confs/invariants/protected"
  "certora/confs/invariants/hook"
)

for dir in "${DIRS[@]}"; do
  for file in "$dir"/*${pattern}*.conf; do
    if [[ -f "$file" ]]; then
      echo "Running certoraRun on $file"
      certoraRun "$file"
    fi
  done
done
