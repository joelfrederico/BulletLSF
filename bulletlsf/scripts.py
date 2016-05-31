import argparse
import shlex, subprocess
import os
import prompter
import pdb

def _bulletlsf():
    parser = argparse.ArgumentParser(description="Lies")

    add_argument(parser , '-q' , '--queue' , environ_var='BSUB_QUEUE' , help_str='the queue to submit the job to')
    add_argument(parser , '-b' , '--bin'   , environ_var='BSUB_BIN'   , help_str='path to the MPI binary to run')
    add_argument(parser , '-s' , '--sla'   , environ_var='BSUB_SLA'   , help_str='the SLA to submit to', required=False)
    parser.add_argument('-c' , '--config', default='', help='the config file to use', required=False)
    
    add_argument(parser , '-p' , '--ptile'   , environ_var='BSUB_PTILE'   , help_str='the number of processors per host')
    
    parser.add_argument('-n', required=True, type=int, help='the number of cores')
    parser.add_argument('-W', '--Wait', default=3, type=int, help='the number of minutes before termination')
    parser.add_argument('-l', '--log', default='log.log', help='the log file to write to')
    
    args = parser.parse_args()
    
    optional_cmd = ''
    
    bincmd = args.bin
    if args.config != '':
        bincmd = bincmd + ' --file=' + args.config
    
    if args.queue == "bullet":
    	queue    = "bulletmpi"
    	args.sla = None
    
    elif args.queue == "oak":
    	queue    = "beamphysics"
    	args.sla = None
    else:
    	queue = args.queue
    
    if args.sla is not None:
    	optional_cmd += ' -sla {sla}'.format(sla=args.sla)
    
    command = "bsub -a mympi -q {queue}{optional_cmd} -R \"span[ptile={ptile}]\" -W {Wait} -oo {log} -n {n} {bin}".format(queue=queue, optional_cmd=optional_cmd, sla=args.sla, Wait=args.Wait, log=args.log, n=args.n, bin=bincmd, ptile=args.ptile)
    
    print(command)
    
    if prompter.yesno('Is this command good?'):
    	subprocess.run(shlex.split(command))


def add_argument(parser, *args, environ_var=None, help_str='', required=True):
    if environ_var is not None:
    	try:
    	    parser.add_argument(*args, default=os.environ[environ_var],
                    help=help_str)
    	    return
    
    	except:
    	    pass
    
    parser.add_argument(*args, required=required,
            help=help_str)
