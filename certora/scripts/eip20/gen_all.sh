# Run from current difectory

# generate new 
python3 ./gen_debt.py
python3 ./gen_protected.py
python3 ./gen_silo.py

# move into configs
mkdir ../../confs/eip20/
mv -f debt protected silo ../../confs/eip20/

# remove trash 
rm -rf ./__pycache__