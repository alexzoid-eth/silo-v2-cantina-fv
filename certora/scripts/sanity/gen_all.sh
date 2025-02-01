# Run from current difectory

# generate new 
python3 ./gen_config.py
python3 ./gen_debt.py
python3 ./gen_hook.py
python3 ./gen_protected.py
python3 ./gen_silo.py

# move into configs
mkdir ../../confs/sanity
mv -f config debt hook protected silo ../../confs/sanity/

# remove trash 
rm -rf ./__pycache__