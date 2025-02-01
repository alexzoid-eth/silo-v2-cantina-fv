# Run from current difectory

# generate new 
python3 ./gen_hook.py
python3 ./gen_hook_ex.py

# move into configs
rm -rf ../../confs/hook
mv -f hook ../../confs

# remove trash 
rm -rf ./__pycache__