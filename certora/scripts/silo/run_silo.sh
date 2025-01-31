for file in certora/confs/silo/*.conf; do
    certoraRun "$file"
done