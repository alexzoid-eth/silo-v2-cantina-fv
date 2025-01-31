for file in certora/confs/eip20/protected/*.conf; do
    certoraRun "$file"
done