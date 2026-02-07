#!/bin/bash
# Benchmark script for Exercise 4 - Greedy benchmarking

echo "=========================================="
echo "Exercise 4: Greedy Benchmarking"
echo "=========================================="
echo ""

levels=(
    "SAsoko1_04.lvl"
    "SAsoko1_08.lvl"
    "SAsoko1_16.lvl"
    "SAsoko1_32.lvl"
    "SAsoko1_64.lvl"
    "SAsoko1_128.lvl"
    "SAsoko2_04.lvl"
    "SAsoko2_08.lvl"
    "SAsoko2_16.lvl"
    "SAsoko2_32.lvl"
    "SAsoko2_64.lvl"
    "SAsoko2_128.lvl"
    "SAsoko3_04.lvl"
    "SAsoko3_05.lvl"
    "SAsoko3_06.lvl"
    "SAsoko3_07.lvl"
    "SAsoko3_08.lvl"
    "SAsoko3_16.lvl"
    "SAsoko3_32.lvl"
    "SAsoko3_64.lvl"
    "SAsoko3_128.lvl"
    "SAFirefly.lvl"
    "SACrunch.lvl"
    "SALazarus.lvl"
    "SApushing.lvl"
)

for level in "${levels[@]}"; do
    echo ""
    echo "=========================================="
    echo "Testing: $level with Greedy"
    echo "=========================================="
    
    java -jar ../server.jar \
        -l "../levels/$level" \
        -c "python -m searchclient.searchclient -greedy" \
        -s 180 -t 180
    
    echo ""
    echo "Press Enter to continue to next level..."
    read
done

echo ""
echo "=========================================="
echo "Greedy Benchmarking Complete!"
echo "=========================================="