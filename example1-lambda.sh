#! /bin/sh

mkdir -p results/example1-lambda/dnadiff/
memtime="results/example1-lambda/total.memtime"
/usr/bin/time --format "Command line: %C\nReal time: %e s\nCPU time: -1.0 s\nUser time: %U s\nSystem time: %S s\nMaximum RSS: %M kB\nExit status: %x" --quiet -o ${memtime} \
	./aracon test-data/lambda/reads.fastq results/example1-lambda/ --num-threads 4

mkdir -p results/example1-lambda/dnadiff
dnadiff -p results/example1-lambda/dnadiff/assembly.consensus.iter2 test-data/lambda/NC_001416.fa results/example1-lambda/assembly.consensus.iter2.fasta

grep "TotalBases" results/example1-lambda/dnadiff/assembly.consensus.iter2.report
grep "AlignedBases" results/example1-lambda/dnadiff/assembly.consensus.iter2.report
grep "AvgIdentity" results/example1-lambda/dnadiff/assembly.consensus.iter2.report
cat ${memtime}
