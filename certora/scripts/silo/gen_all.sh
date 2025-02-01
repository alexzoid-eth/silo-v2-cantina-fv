# Run from current difectory

# generate new 
python3 ./gen_silo.py
python3 ./gen_silo_ex.py

# move into configs
mv -f silo ../../confs

# remove trash 
rm -rf ./__pycache__