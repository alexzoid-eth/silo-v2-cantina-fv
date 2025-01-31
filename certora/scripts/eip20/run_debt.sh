for file in certora/confs/eip20/debt/*.conf; do
    certoraRun "$file"
done