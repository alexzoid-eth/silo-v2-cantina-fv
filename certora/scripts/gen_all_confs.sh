# Execute from current directory. Update all configs.

# Remove `confs` directory fist

mkdir ../confs

cd ./eip20
./gen_all.sh

cd ../eip4626
./gen_all.sh

cd ../hook
./gen_all.sh

cd ../invariants
./gen_all.sh

cd ../sanity
./gen_all.sh

cd ../silo
./gen_all.sh