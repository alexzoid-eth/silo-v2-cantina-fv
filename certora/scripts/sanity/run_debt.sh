#!/bin/bash
# Use the first argument as the pattern. If no argument is provided, match all files.
pattern="${1:-}"

for file in certora/confs/sanity/debt/*${pattern}*.conf; do
    certoraRun "$file"
done
