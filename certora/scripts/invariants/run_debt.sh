for file in certora/confs/invariants/debt/*.conf; do
    certoraRun "$file"
done