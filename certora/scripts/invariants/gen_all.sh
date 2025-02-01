# Run from current difectory

# remove old
rm -rf ./config
rm -rf ./debt
rm -rf ./hook
rm -rf ./protected
rm -rf ./silo
rm -rf ../../confs/invariants/config
rm -rf ../../confs/invariants/debt
rm -rf ../../confs/invariants/hook
rm -rf ../../confs/invariants/protected
rm -rf ../../confs/invariants/silo

# generate new 
python3 ./gen_config.py
python3 ./gen_debt.py
python3 ./gen_hook.py
python3 ./gen_protected.py
python3 ./gen_silo_ex.py

# move into configs
mv config debt hook protected silo ../../confs/invariants/

# remove trash 
rm -rf ./__pycache__