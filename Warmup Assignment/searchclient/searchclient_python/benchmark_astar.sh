#!/bin/bash
# Benchmark script for Exercise 4 - A* benchmarking

echo "=========================================="
echo "Exercise 4: A* Benchmarking"
echo "=========================================="
echo ""

levels=(
    "MAPF00.lvl"
    "MAPF01.lvl"
    "MAPF02.lvl"
    "MAPF02C.lvl"
    "MAPF03.lvl"
    "MAPF03C.lvl"
    "MAPFslidingpuzzle.lvl"
    "MAPFreorder2.lvl"
    "BFSfriendly.lvl"
)

for level in "${levels[@]}"; do
    echo ""
    echo "=========================================="
    echo "Testing: $level with A*"
    echo "=========================================="
    
    java -jar ../server.jar \
        -l "../levels/$level" \
        -c "python -m searchclient.searchclient -astar" \
        -s 180 -t 180
    
    echo ""
    echo "Press Enter to continue to next level..."
    read
done

echo ""
echo "=========================================="
echo "A* Benchmarking Complete!"
echo "=========================================="