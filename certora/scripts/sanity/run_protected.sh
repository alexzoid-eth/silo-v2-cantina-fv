for file in certora/confs/sanity/protected/*.conf; do
    certoraRun "$file"
done