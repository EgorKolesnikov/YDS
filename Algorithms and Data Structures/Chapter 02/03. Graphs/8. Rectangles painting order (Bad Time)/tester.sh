#!/bin/bash
g++ -std=c++11 test.cpp -o test
g++ -std=c++11 algo_pablo.cpp -o try

./test 'generate' 'test.output.txt'
./try 'test.output.txt' 'try.output.txt'
./test 'compare' 'test.output.txt' 'try.output.txt'
