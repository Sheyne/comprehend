#! /bin/bash

for file in *.neato ; do
	neato $file -Tpdf -O
done
for file in *.dot ; do
	dot $file -Tpdf -O
done