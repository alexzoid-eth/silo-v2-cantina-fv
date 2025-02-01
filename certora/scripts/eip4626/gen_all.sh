# Run from current difectory

# generate new 
python3 ./gen_silo.py

# move into configs
mkdir ../../confs/eip4626/
mv -f eip4626 ../../confs

# remove trash 
rm -rf ./__pycache__