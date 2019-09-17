import multiprocessing
import os
import sys
import commands
import re

def myrm(path):
    if os.path.exists(path):
        os.remove(path)

def mysymlink(path, file):
    # link -s ../$file $path/$file
    os.symlink(os.path.abspath("../" + file), path + "/" + file)

def prepare(n):
    path = "worker{0}".format(n)
    if not os.path.exists(path):
        print("Preparing workspace for worker{0}...".format(n))

        os.makedirs(path)

        os.makedirs(path + "/generator")
        mysymlink(path, "generator/src")

        os.makedirs(path + "/project")
        mysymlink(path, "project/build.properties")
        mysymlink(path, "project/build.scala")

        mysymlink(path, "config")
        mysymlink(path, "env")
        os.makedirs(path + "/output")

        os.symlink(os.path.abspath("Makefile"), path + "/Makefile")
        mysymlink(path, "build.sc")

        status, output = commands.getstatusoutput('make -C {0} gen OPTIONS="-d ."'.format(path))

        print("Finishing preparing workspace for worker{0} with status = {1}...".format(n, status))
    else:
        print("Workspace for worker{0} already exists".format(n))

        myrm(path + "/gen.log")
        myrm(path + "/run.log")
        myrm(path + "/log.txt")

def worker(n):
    path = "worker{0}".format(n)
    i = 0
    total_instr = 0
    while True:
        i += 1
        status, output = commands.getstatusoutput('make -C {0} gen OPTIONS="-d ."'.format(path))
        if status != 0:
            print("Worker{0} fails to generate the {1}th test. Retrying".format(n, i))
            os.system('echo "{0}" > {1}/gen.log'.format(output, path))
            continue

        status, output = commands.getstatusoutput('make -C {0} run PORT={1}'.format(path, 10000 + n))
        if status != 0:
            os.system('echo "{0}" > {1}/run.log'.format(output, path))
            break
        #print output
        #line = re.search('total guest instructions = \d+', output).group()
        line = re.search('instrCnt = \d+', output).group()
        instr = int(re.search('\d+', line).group())
        total_instr += instr
        os.system('echo "pass {0} tests {1} total instructions" > {2}/log.txt'.format(i, total_instr, path))

    log = "Worker{0} fail to pass the {1}th test".format(n, i)
    os.system('echo "{0}" >> {1}/log.txt'.format(log, path))
    print(log)
    

if __name__ == "__main__":
    n = int(sys.argv[1])
    os.system("date")
    print("#worker = {0}".format(n))
    for i in range(0, n):
        prepare(i)
        multiprocessing.Process(target = worker, args = (i,)).start()
