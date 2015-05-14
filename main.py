#!/usr/bin/env python

import os
import random
import itertools
import shutil
import struct
import uuid
import sys

import config
from BitmapTarget import BitmapTarget


def random_byte(dummy):
    return random.randint(0, 255)

def flip_byte(val):
    assert val >= 0 and val <= 255, "Invalid byte"
    return val ^ 255

# by default the range r will be the whole filee
def mutate_file(path, r=None, mutations=1, byte_mutator=flip_byte):
    if r == None:
        orig = open(path, 'rb')
        r = (0, file_size(orig) - 1)
        orig.close()
    
    shutil.copy(path, path + config.fuzz_ext)
    f = open(path + config.fuzz_ext, 'rb+')
    
    # a list to record the changed bytes
    changes = []
    
    # The actual mutation loop
    for _ in itertools.repeat(None, mutations):
        byte_to_change = random.randrange(r[0], r[1])
        f.seek(byte_to_change)
        old_byte = ord(f.read(1))
        new_byte = byte_mutator(old_byte)
        f.seek(byte_to_change)
        f.write(struct.pack('B', new_byte))
        f.seek(0)
        changes.extend([byte_to_change, new_byte])
        
    f.flush()
    f.close()
    
    #rename file to mark it
    new_path = config.fuzz_out + path.split('/')[1].split('.')[0] + '_' + str(uuid.uuid4())[0:8] + '.' + path.split('/')[1].split('.')[1]
    shutil.move(path + config.fuzz_ext, new_path)
    return new_path

# pass a file object
def file_size(f):
    f.seek(0,2)
    size = f.tell()
    f.seek(0)
    return size

def list_samples():
    samples = os.listdir(config.samples_dir)
    return map(lambda p: '/'.join([config.samples_dir, p]), samples)

def main():
    iters = 100
    errors = dict()
    
    samples = list_samples()
    fuzzed_task = BitmapTarget(config.bin_directory + 'bitmap')
    
    print("Running %d iterations on %s, using each %d base samples." % (iters, fuzzed_task, len(samples))) 
    
    for i in xrange(0, iters):
        for s in samples:
            duv = mutate_file(s, mutations=random.randrange(1, 5))
            err = fuzzed_task.run(duv)
            if err != None:
                if err in errors:
                    errors[err] += 1
                else:
                    errors[err] = 1
        if i % (iters / 30) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
    
    print('')    
    for k in sorted(errors):
        print("%d\t->\t %d hits" % (k, errors[k]))

if __name__ == '__main__':
    main()
