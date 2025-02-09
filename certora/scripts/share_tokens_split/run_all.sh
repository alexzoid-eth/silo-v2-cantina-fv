#!/bin/bash

# Use the first argument as the pattern. If no argument is provided, match all files.
pattern="${1:-}"

DIRS=(
  "certora/confs/share_tokens_split/debt"
  "certora/confs/share_tokens_split/silo"
  "certora/confs/share_tokens_split/protected"
)

for dir in "${DIRS[@]}"; do
  for file in "$dir"/*${pattern}*.conf; do
    if [[ -f "$file" ]]; then
      echo "Running certoraRun on $file"
      certoraRun "$file"
    fi
  done
done
