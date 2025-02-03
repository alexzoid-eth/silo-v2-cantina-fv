# Run from current difectory

# generate new 
python3 ./gen_silo.py

# move into configs
mkdir ../../confs/eip4626_collateral/
mv -f eip4626_collateral ../../confs

# remove trash 
rm -rf ./__pycache__