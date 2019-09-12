import multiprocessing
import os
import sys
import commands
import re

def rm(path):
    if os.path.exists(path):
        os.remove(path)

def worker(n):
    path = "worker{0}".format(n)
    if not os.path.exists(path):
        os.makedirs(path)
        os.symlink("../Makefile", path + "/Makefile")
    else:
        rm(path + "/gen.log")
        rm(path + "/run.log")
        rm(path + "/log.txt")
    #print("{0}".format(path))
    i = 0
    total_instr = 0
    while True:
        i += 1
        status, output = commands.getstatusoutput('make -C .. gen OPTIONS="-d {0}"'.format(os.path.abspath(path)))
        if status != 0:
            print("\nWorker{0} fails to generate the {1}th test.\nThis may due to data race of the scala compilation results. Retrying".format(n, i))
            os.system('echo "{0}" > {1}/gen.log'.format(output, path))
            continue

        status, output = commands.getstatusoutput('make run PORT={0} -C {1}'.format(10000 + n, path))
        if status != 0:
            os.system('echo "{0}" > {1}/run.log'.format(output, path))
            break
        #print output
        line = re.search('total guest instructions = \d+', output).group()
        instr = int(re.search('\d+', line).group())
        total_instr += instr
        try:
            sys.stderr.write(".")
        finally:
            os.system('echo "pass {0} tests {1} total instructions" > {2}/log.txt'.format(i, total_instr, path))

    log = "Worker{0} fail to pass the {1}th test".format(n, i)
    os.system('echo "{0}" >> {1}/log.txt'.format(log, path))
    print(log)
    

if __name__ == "__main__":
    os.system("make -C .. gen")
    os.system("date")
    for i in range(0, 80):
        multiprocessing.Process(target = worker, args = (i,)).start()
        print i,
