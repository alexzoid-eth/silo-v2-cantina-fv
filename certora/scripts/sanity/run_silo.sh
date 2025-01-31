for file in certora/confs/sanity/silo/*.conf; do
    certoraRun "$file"
done