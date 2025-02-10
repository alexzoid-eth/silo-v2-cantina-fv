#!/bin/bash

# Execute from root directory. Updates all configs.
# Find all .conf files in the conf directory and its subdirectories
find certora/confs -type f -name "*.conf" | while read -r conf_file; do
    echo "Executing certoraMutate on $conf_file"
    certoraMutate "$conf_file"
    if [ $? -ne 0 ]; then
        echo "Error executing certoraMutate on $conf_file"
    fi
done
