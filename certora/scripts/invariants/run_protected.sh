for file in certora/confs/invariants/protected/*.conf; do
    certoraRun "$file"
done