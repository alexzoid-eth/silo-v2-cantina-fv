# Update all configs. Run from current directory

# generate new 
python3 ./gen_debt.py
python3 ./gen_hook_ex.py
python3 ./gen_protected.py
python3 ./gen_silo_ex.py

# move into configs
mkdir ../../confs/invariants/
mv -f debt hook protected silo ../../confs/invariants/

# remove trash 
rm -rf ./__pycache__