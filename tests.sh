#!/bin/sh

for file in $(ls example_expected_results); do
  result=$(./run.sh examples/$file.lisp)
  expected_result=$(cat example_expected_results/$file)
  if [[ "$result" != "$expected_result" ]]; then
    echo "FAILED: $file"
    echo "Expected: $expected_result"
    echo "Got: $result"
  else
    echo "PASSED: $file"
  fi
done
