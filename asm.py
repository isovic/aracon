#! /usr/bin/python

import os
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__));
import sys;
# sys.path.append(SCRIPT_PATH + '/../codebase/samscripts/src/');

import subprocess;
import operator;

import copy;

DRY_RUN = False;

MINIASM_BIN = '%s/components/miniasm/miniasm' % (SCRIPT_PATH);
GRAPHMAP_BIN = '%s/components/graphmap/bin/graphmap-not_release' % (SCRIPT_PATH);
SAMSCRIPTS_PATH = '%s/components/racon/codebase/samscripts' % (SCRIPT_PATH);
MINIMAP_PATH = '%s/components/racon/tools/minimap/minimap' % (SCRIPT_PATH);
RACON_BIN = '%s/components/racon/bin/racon' % (SCRIPT_PATH);
PAF2MHAP_BIN = '%s/components/racon/scripts/paf2mhap.pl' % (SCRIPT_PATH);



import traceback;
from time import gmtime, strftime
### Logs messages to STDERR and an output log file if provided (opened elsewhere).
def log(message, fp_log, silent=False):
    if (silent == True): return;

    timestamp = strftime("%Y/%m/%d %H:%M:%S", gmtime());
    if (message != ''):
    	prefix = '[%s] ' % (timestamp);
    else:
    	prefix = '';

    sys.stderr.write('%s%s\n' % (prefix, message));
    sys.stderr.flush();
    if (fp_log != None and fp_log != sys.stderr):
        fp_log.write('%s%s\n' % (prefix, message));
        fp_log.flush();
def execute_command(command, fp_log, dry_run=True):
    if (dry_run == True):
        log('Executing (dryrun): "%s".' % (command), fp_log);
        log('\n', fp_log);
        return 0;
    if (dry_run == False):
        log('Executing: "%s".' % (command), fp_log);
        rc = subprocess.call(command, shell=True);
        if (rc != 0):
            log('ERROR: subprocess call returned error code: %d.' % (rc), fp_log);
            log('Traceback:', fp_log);
            traceback.print_stack(fp_log);
            exit(1);
        return rc;

def execute_command_with_ret(dry_run, command, silent=False):
	if (silent == False):
		sys.stderr.write('Executing command: "%s"\n' % command);
	if (dry_run == False):
		p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
	[output, err] = p.communicate()
	rc = p.returncode
	if (silent == False):
		sys.stderr.write('\n');
	return [rc, output, err];

def main():
	if (len(sys.argv) < 3):
		sys.stderr.write('A de novo genome assembler for third generation sequencing data which does not requrie error correction.\n');
		sys.stderr.write('Usage:\n');
		sys.stderr.write('\t%s <reads.fastq> <working_folder> [options]\n' % (sys.argv[0]));
		sys.stderr.write('\n');
		sys.stderr.write('Options:\n');
		sys.stderr.write('\t--threads INT\n');
		sys.stderr.write('\n');
		exit(1);

	reads_fastq = sys.argv[1];
	working_folder = os.path.abspath(sys.argv[2]);

	num_threads = 4;

	i = 3;
	while (i < len(sys.argv)):
		arg = sys.argv[i];
		if (arg == '--num-threads'):
			num_threads = int(sys.argv[i+1]);
			i += 1;
		else:
			sys.stderr.write('Unknown option "%s". Exiting.\n' % (arg));
			exit(1);
		i += 1;

	if (not os.path.exists(working_folder)):
		os.makedirs(working_folder);

	log_path = '%s/assembly.log' % (working_folder);
	try:
		fp_log = open(log_path, 'w');
	except Exception, e:
		sys.stderr.write('ERROR: Could not open log file "%s" for writing! Exiting.\n' % (log_path));
		sys.stderr.write('\n');
		sys.stderr.write(str(e));
		exit(1);

	reads_fasta = '%s/reads.fasta' % (working_folder);
	overlaps_mhap = '%s/overlaps.mhap' % (working_folder);
	overlaps_paf = '%s/overlaps.paf' % (working_folder);
	assembly_raw_gfa = '%s/assembly.raw.gfa' % (working_folder);
	assembly_iter0_fasta = '%s/assembly.raw.fasta' % (working_folder);
	assembly_iter1_fasta = '%s/assembly.consensus.iter1.fasta' % (working_folder);
	assembly_iter2_fasta = '%s/assembly.consensus.iter2.fasta' % (working_folder);
	mapping_iter1_paf = '%s/mapping.iter1.paf' % (working_folder);
	mapping_iter1_mhap = '%s/mapping.iter1.mhap' % (working_folder);
	mapping_iter2_paf = '%s/mapping.iter2.paf' % (working_folder);
	mapping_iter2_mhap = '%s/mapping.iter2.mhap' % (working_folder);

	commands = [];

	commands.append('%s owler -t %d -r %s -d %s -L paf -o %s' % (GRAPHMAP_BIN, num_threads, reads_fastq, reads_fastq, overlaps_paf));
	# commands.append('components/racon/tools/minimap/minimap -Sw5 -L100 -m0 -t %d %s %s > %s' % (num_threads, reads_fastq, reads_fastq, overlaps_paf));	

	# commands.append('components/miniasm/miniasm -i 0.0 -m 500 -s 100 -I 0.3 -f %s %s > %s' % (reads_fastq, overlaps_paf, assembly_raw_gfa));
	commands.append('%s -f %s %s > %s' % (MINIASM_BIN, reads_fastq, overlaps_paf, assembly_raw_gfa));
	commands.append("awk '$1 ~/S/ {print \">\"$2\"\\n\"$3}' %s > %s" % (assembly_raw_gfa, assembly_iter0_fasta));

	commands.append('%s/src/fastqfilter.py fastq2fasta %s > %s' % (SAMSCRIPTS_PATH, reads_fastq, reads_fasta));	

	commands.append('%s %s %s > %s' % (MINIMAP_PATH, assembly_iter0_fasta, reads_fasta, mapping_iter1_paf));	
	commands.append('%s %s %s %s > %s' % (PAF2MHAP_BIN, assembly_iter0_fasta, reads_fasta, mapping_iter1_paf, mapping_iter1_mhap));
	commands.append('%s -M 5 -X -4 -G -8 -E -6 --bq 10 -t %d --mhap --reads %s %s %s %s' % (RACON_BIN, num_threads, reads_fastq, assembly_iter0_fasta, mapping_iter1_mhap, assembly_iter1_fasta))

	commands.append('%s %s %s > %s' % (MINIMAP_PATH, assembly_iter1_fasta, reads_fasta, mapping_iter2_paf));	
	commands.append('%s %s %s %s > %s' % (PAF2MHAP_BIN, assembly_iter1_fasta, reads_fasta, mapping_iter2_paf, mapping_iter2_mhap));
	commands.append('%s -M 5 -X -4 -G -8 -E -6 --bq 10 -t %d --mhap --reads %s %s %s %s' % (RACON_BIN, num_threads, reads_fastq, assembly_iter1_fasta, mapping_iter2_mhap, assembly_iter2_fasta))

	for command in commands:
		execute_command(command, fp_log, dry_run=False);

	sys.stderr.write('Done!\n');
	sys.stderr.write('Final assembly written to file: "%s"\n' % (assembly_iter2_fasta));

	fp_log.close();

if __name__ == "__main__":
	main();
