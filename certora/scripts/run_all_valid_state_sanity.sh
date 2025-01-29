for file in certora/confs/silo_single_valid_state/valid_state_sanity_*_verified.conf; do
    certoraRun "$file"
done