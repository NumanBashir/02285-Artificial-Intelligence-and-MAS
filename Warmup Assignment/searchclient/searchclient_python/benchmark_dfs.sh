#!/bin/bash
# Benchmark script for Exercise 3 - DFS vs BFS comparison

echo "=========================================="
echo "Exercise 3: DFS Benchmarking"
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
)

for level in "${levels[@]}"; do
    echo ""
    echo "=========================================="
    echo "Testing: $level with DFS"
    echo "=========================================="
    
    java -jar ../server.jar \
        -l "../levels/$level" \
        -c "python -m searchclient.searchclient -dfs" \
        -g -s 180 -t 180
    
    echo ""
    echo "Press Enter to continue to next level..."
    read
done

echo ""
echo "=========================================="
echo "DFS Benchmarking Complete!"
echo "=========================================="
