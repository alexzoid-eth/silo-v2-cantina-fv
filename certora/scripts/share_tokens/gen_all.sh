# Run from current difectory

#!/bin/bash
# Use the first argument as the pattern. If no argument is provided, match all files.
pattern="${1:-}"

# generate new 
python3 ./gen_debt.py
python3 ./gen_protected.py
python3 ./gen_silo.py

# move into configs
mkdir ../../confs/share_tokens
mv -f debt protected silo ../../confs/share_tokens/

# remove trash 
rm -rf ./__pycache__