for file in certora/confs/eip20/silo/*.conf; do
    certoraRun "$file"
done