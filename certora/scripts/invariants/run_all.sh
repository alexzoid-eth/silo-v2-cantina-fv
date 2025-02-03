#!/bin/bash

DIRS=(
  "certora/confs/invariants/config"
  "certora/confs/invariants/debt"
  "certora/confs/invariants/silo"
  "certora/confs/invariants/protected"
  "certora/confs/invariants/hook"
)

for dir in "${DIRS[@]}"; do
  for file in "$dir"/*.conf; do
    if [[ -f "$file" ]]; then
      echo "Running certoraRun on $file"
      certoraRun "$file"
    fi
  done
done
