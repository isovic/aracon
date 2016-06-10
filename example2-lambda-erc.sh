#! /bin/sh

mkdir -p results/example2-lambda-erc/dnadiff/
memtime="results/example2-lambda-erc/total.memtime"
/usr/bin/time --format "Command line: %C\nReal time: %e s\nCPU time: -1.0 s\nUser time: %U s\nSystem time: %S s\nMaximum RSS: %M kB\nExit status: %x" --quiet -o ${memtime} \
	./aracon test-data/lambda/reads.fastq results/example2-lambda-erc/ --num-threads 4 --erc

mkdir -p results/example2-lambda-erc/dnadiff
dnadiff -p results/example2-lambda-erc/dnadiff/assembly.consensus.iter2 test-data/lambda/NC_001416.fa results/example2-lambda-erc/assembly.consensus.iter2.fasta

grep "TotalBases" results/example2-lambda-erc/dnadiff/assembly.consensus.iter2.report
grep "AlignedBases" results/example2-lambda-erc/dnadiff/assembly.consensus.iter2.report
grep "AvgIdentity" results/example2-lambda-erc/dnadiff/assembly.consensus.iter2.report
cat ${memtime}
