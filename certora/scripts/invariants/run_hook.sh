for file in certora/confs/invariants/hook/*.conf; do
    certoraRun "$file"
done