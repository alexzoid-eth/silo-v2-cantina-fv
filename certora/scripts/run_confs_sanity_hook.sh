for file in certora/confs/sanity/hook/*.conf; do
    certoraRun "$file"
done