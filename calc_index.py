import sys, os
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from astropy.stats import rayleightest
from astropy import units as u

def cal_pi (angle_list):
    a = math.pow(sum([math.cos(a) for a in angle_list]),2)
    b = math.pow(sum([math.sin(b) for b in angle_list]),2)
    N = len(angle_list)
    return math.sqrt((a+b)/math.pow(N,2))

def read_angle_csv (input_fname):
    angles = []
    f = open(input_fname, 'r', encoding='utf-8-sig')
    lines = csv.reader(f)
    for line in lines:
        if line:
            angles.append(float(line[0]))
#        else:
#            print("{} has wrong data".format(input_fname))
    f.close()
    return [math.radians(a) for a in angles], angles

def read_file_list(fname):
    with open(fname, 'r') as fp:
        lines = fp.readlines()

    return [line.strip() for line in lines]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('$ python3 calc_index.py file.scp')
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('[ERR] Failed to find {} file'.format(sys.argv[1]))
        sys.exit(1)
    
    file_list = read_file_list (sys.argv[1])

    for fname in file_list:
        if not os.path.isfile(fname):
            print('[ERR] Failed to find {} file'.format(fname))
            sys.exit(1)

        radian_list, degree_list = read_angle_csv (fname)
        print("FILE: {}, Data #: {}".format(fname, len(radian_list)))
        print("PI:  {}". format(cal_pi(radian_list)))

        degree_np = np.array(degree_list)*u.deg
        result = rayleightest(degree_np)
        print("RAY: {}". format(result.to_value()))
        print("")

