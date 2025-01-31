for file in certora/confs/sanity/config/*.conf; do
    certoraRun "$file"
done