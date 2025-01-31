for file in certora/confs/sanity/debt/*.conf; do
    certoraRun "$file"
done