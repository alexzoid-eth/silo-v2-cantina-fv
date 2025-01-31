for file in certora/confs/eip4626/*.conf; do
    certoraRun "$file"
done