# Execute from current directory. Updates all configs.

# !!! Remove `confs` directory fist !!! 
rm -rf ../confs

mkdir ../confs

cd ./eip20
./gen_all.sh

cd ../eip4626_collateral
./gen_all.sh

cd ../eip4626_protected
./gen_all.sh

# Nothing implemented
#cd ../hook
#./gen_all.sh

cd ../invariants
./gen_all.sh

cd ../sanity
./gen_all.sh

cd ../share_tokens
./gen_all.sh

cd ../share_tokens_split
./gen_all.sh

cd ../silo
./gen_all.sh

cd ../silo_split
./gen_all.sh