# Execute from current directory, execute certoraMutate on all configs.

cd ./eip20
./mutate_all.sh

cd ../eip4626_collateral
./mutate_all.sh

cd ../eip4626_protected
./mutate_all.sh

cd ../hook
./mutate_all.sh

cd ../invariants
./mutate_all.sh

cd ../sanity
./mutate_all.sh

cd ../share_tokens
./mutate_all.sh

cd ../share_tokens_split
./mutate_all.sh

cd ../silo
./mutate_all.sh

cd ../silo_split
./mutate_all.sh