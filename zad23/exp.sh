#!/usr/bin/env sh
cmake cmake-build-debug
for i in 1024 4096 16384; do
  ./cmake-build-debug/server &
  fp=$!
  ./cmake-build-debug/client $i > "log${i}" &
  sp=$!

  sleep 60
  echo "time to kill ${i}!"

  kill $fp
  kill $sp
done

python3 ./analyze.py