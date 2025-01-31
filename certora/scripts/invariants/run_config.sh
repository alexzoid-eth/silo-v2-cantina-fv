for file in certora/confs/invariants/config/*.conf; do
    certoraRun "$file"
done