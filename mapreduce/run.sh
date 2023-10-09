#!/bin/bash

# Clean up stray files from previous run
rm -f hosts/europe/results/*.txt
rm -f hosts/america/results/*.txt
rm -f hosts/asia/results/*.txt
rm -f hosts/africa/results/*.txt
rm -f intermediate/*.txt
rm -f result/*.txt

# Run the map step on every host in parallel
HOST=europe node map.js &
HOST=america node map.js &
HOST=asia node map.js &
HOST=africa node map.js &

# Wait for them to every job be done
wait

# Run the suffle step
HOSTS=europe,america,asia,africa node shuffle.js

# Run the reduce step
node reduce.js

# View the final result of the MapReduce job
cat result/output.txt
