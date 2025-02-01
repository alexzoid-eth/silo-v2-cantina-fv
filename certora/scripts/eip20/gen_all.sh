# Run from current difectory

# remove old
rm -rf ./debt
rm -rf ./protected
rm -rf ./silo
rm -rf ../../confs/eip20/debt
rm -rf ../../confs/eip20/protected
rm -rf ../../confs/eip20/silo

# generate new 
python3 ./gen_debt.py
python3 ./gen_protected.py
python3 ./gen_silo.py

# move into configs
mv debt protected silo ../../confs/eip20/

# remove trash 
rm -rf ./__pycache__