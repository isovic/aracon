# Aracon - Assembly with Rapid Consensus

This is an integrative project of a de novo assembler capable of assemblin raw noisy long reads, and correcting errors at the end of the process, in the consensus phase.  
The results after consensus are comparable or better than those obtained with full-blown pipelines utilizing both error-correction and consensus.  

Components integrated into Aracon:  
1. GraphMap owler - for read overlapping.
2. Miniasm layout - for now we utilize Miniasm's layout module just in the proof-of-concept stage. Later layout will be implemented.
3. Racon - for a rapid consensus of the raw contigs.

Although intended for assembling reads without error correction, there is an option ```--erc``` in Aracon which allows utilization of the error-correction step.  
When using error correction, the pipeline is modified as follows:  
1. Racon on raw reads - to produce error-corrected reads.
2. GraphMap owler - for read overlapping.
3. Miniasm layout - for now we utilize Miniasm's layout module just in the proof-of-concept stage. Later layout will be implemented.
4. Racon - for a rapid consensus of the contigs.

## Installation
Type:  
```
make
```
All submodules should be fetched and installed automatically.

## Usage  
To run Aracon on raw noisy reads:  
```  
./aracon test-data/lambda/reads.fastq results/example1-lambda/ --num-threads 4
```  
Aracon also has an error-correction option, to use it add the ```--erc``` option at the end:  
```  
./aracon test-data/lambda/reads.fastq results/example1-lambda/ --num-threads 4 --erc
```  
