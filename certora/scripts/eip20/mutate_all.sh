#!/bin/bash

DIRS=(
  "certora/confs/eip20/debt"
  "certora/confs/eip20/silo"
  "certora/confs/eip20/protected"
)

for dir in "${DIRS[@]}"; do
  for file in "$dir"/*.conf; do
    if [[ -f "$file" ]]; then
      echo "Running certoraRun on $file"
      certoraMutate "$file"
    fi
  done
done
