for file in certora/confs/silo_single_eip4626_compatibility/*.conf; do
    certoraRun "$file"
done