# Copyright (C) 2019 SuperDARN Canada, University of Saskatchewan
# Author: Marina Schmidt
# Description: This script is used to generate summary plots for all
#              SuperDARN radars and for each beam for a given date
from glob import glob
import pydarn
import matplotlib.pyplot as plt
from collections import deque
import sys
import bz2
import warnings
import os

def read_files(date, radar):
    year = date[0:4]
    month = date[4:6]
    data = deque()
    fitacf_files = glob('./{date}*{radar}.fitacf.bz2'.format(date=date, radar=radar,year=year,month=month))
    if fitacf_files == []:
        raise Exception('Error: No data for radar {}'.format(radar))

    fitacf_files.sort()
    print("Reading in {} for {} ...".format(radar, date))
    for fitacf_file in fitacf_files:
        with bz2.open(fitacf_file) as fp:
            fitacf_stream = fp.read()

        reader = pydarn.SDarnRead(fitacf_stream, True)
        records = reader.read_fitacf()
        data += records
    print("Reading complete...")
    return data

def plot_files(data, date, radar):
    year=date[0:4]
    month=date[4:6]
    beams = pydarn.SuperDARNRadars.radars[data[0]['stid']].beams
    for beam in range(0, beams):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pydarn.RTP.plot_summary(data, beam_num=beam)
        filename = 'pydarn_{date}_{radar}_bm{beam}.png'.format(year=year,
                                                            month=month,
                                                            date=date,
                                                            radar=radar,
                                                            beam=beam)
        plt.savefig(filename)
        plt.close()
    print("Saved {} Summary plots to {} ...".format(radar, filename))

if len(sys.argv) is not 3:
    print("Must supply one command line arguement")
    print("Example: python3 pydarn_generate_summary_plot.py 20190102")
    exit(1)

date = sys.argv[1]
radar = sys.argv[2]

data = read_files(date, radar)
plot_files(data, date, radar)

exit(0)

