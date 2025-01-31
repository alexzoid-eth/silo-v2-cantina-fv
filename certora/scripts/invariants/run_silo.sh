for file in certora/confs/invariants/silo/*.conf; do
    certoraRun "$file"
done