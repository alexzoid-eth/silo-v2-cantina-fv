#!/bin/bash

# Use the first argument as the pattern. If no argument is provided, match all files.
pattern="${1:-}"

DIRS=(
  "certora/confs/sanity/debt"
  "certora/confs/sanity/silo"
  "certora/confs/sanity/protected"
  "certora/confs/sanity/hook"
)

for dir in "${DIRS[@]}"; do
  for file in "$dir"/*${pattern}*.conf; do
    if [[ -f "$file" ]]; then
      echo "Running certoraRun on $file"
      certoraMutate "$file"
    fi
  done
done
