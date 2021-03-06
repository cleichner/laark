#!/usr/bin/env python

'''
faux-snap --
Reads files from a directory matching a pattern and PUSHes them over the
network as raw data. The matched files will be indefinitely served as
a cyclic list of files so as to simulate the ``snap'' program with
contrived local data.
'''

from glob import glob
from laark.decorator.pipeline import pipeline
import argparse
import cv
import itertools
import os
import sys

parser = argparse.ArgumentParser(
        description='Reads files from a directory matching a pattern '
                    'and PUSHes them over the network as raw data streams. '
                    'See cv.LoadImage for the list of supported formats.')

parser.add_argument('-f', '--file', default='/tmp/images/*.png', nargs='?',
        help='The path and glob for the files to serve.')

parser.add_argument('-p', '--port', default=6000, type=int, nargs='?',
        help='The port to push to on localhost.')

args = parser.parse_args()
files = itertools.cycle(glob(args.file))

def get_image_bytes(filename):
    print 'sending', os.path.basename(filename),'...'
    return cv.LoadImage(filename).tostring()

@pipeline(out_port=args.port)
def worker():
    return get_image_bytes(next(files))

worker.run()
