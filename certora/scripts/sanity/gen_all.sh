# Run from current difectory

# remove old
rm -rf ./config
rm -rf ./debt
rm -rf ./hook
rm -rf ./protected
rm -rf ./silo
rm -rf ../../confs/sanity/config
rm -rf ../../confs/sanity/debt
rm -rf ../../confs/sanity/hook
rm -rf ../../confs/sanity/protected
rm -rf ../../confs/sanity/silo

# generate new 
python3 ./gen_config.py
python3 ./gen_debt.py
python3 ./gen_hook.py
python3 ./gen_protected.py
python3 ./gen_silo.py

# move into configs
mv config debt hook protected silo ../../confs/sanity/

# remove trash 
rm -rf ./__pycache__