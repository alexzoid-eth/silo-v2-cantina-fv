#!/bin/bash

DIRS=(
  "certora/confs/sanity/config"
  "certora/confs/sanity/debt"
  "certora/confs/sanity/silo"
  "certora/confs/sanity/protected"
  #"certora/confs/sanity/hook"
)

for dir in "${DIRS[@]}"; do
  for file in "$dir"/*.conf; do
    if [[ -f "$file" ]]; then
      echo "Running certoraRun on $file"
      certoraRun "$file"
    fi
  done
done
