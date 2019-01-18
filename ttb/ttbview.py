# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:00:00 2019
@author: Aaron Carlton

import export functions for TTB files.
Useful for Merlin II LS Telesis Laser
output_ttb('circles.ttb', make_circles())
output_ttb('hatch.ttb', make_hatch())
"""

import sys
import numpy as np

tools = ['TOOL_LINE_2P', 'TOOL_ELLIPSE', 'TOOL_ARC']
end_tools = ['END_'+tool for tool in tools]
properties = ['ANGLE', 'LENGTH', 'RADIUS', 'MAJOR_RADIUS', 'MINOR_RADIUS', 'START_ANGLE', 'END_ANGLE'] # properties are names that are followed by a value
special_properties = ['ANCHOR_XY', 'ANCHOR_END'] # special_properties have their own xy values

def get_arc(x, y, radius, angle, start, stop):
	arc = {'NAME': 'TOOL_ARC',
		'ANCHOR_XYX': x,
		'ANCHOR_XYY': y,
		'ANGLE': angle,
		'RADIUS': radius,
		'START_ANGLE': start,
		'END_ANGLE': stop, }
	return arc

def get_ellipse(x, y, major_radius, minor_radius, angle, start, stop):
	ellipse = {'NAME': 'TOOL_ELLIPSE',
		'ANCHOR_XYX': x,
		'ANCHOR_XYY': y,
		'ANGLE': angle,
		'MAJOR_RADIUS': major_radius,
		'MINOR_RADIUS': minor_radius,
		'START_ANGLE': start,
		'END_ANGLE': stop, }
	return ellipse

def get_line2p(x, y, length, angle, fx, fy):
	line = {'NAME': 'TOOL_LINE_2P',
		'ANCHOR_XYX': x,
		'ANCHOR_XYY': y,
		'ANGLE': angle,
		'LENGTH': length,
		'ANCHOR_ENDX': fx,
		'ANCHOR_ENDY': fy, }
	return line


def encode_ttb(objs):
	"""TTB encoding
	objs: list of dicts
	"""
	ttbfile = []
	ttbfile.append('TOOLS')
	for item in objs:
		if item['NAME'] == 'TOOL_LINE_2P':
			ttbfile.append('TOOL_LINE_2P')
			ttbfile.append('TOOL_LINE')
			ttbfile.append('TOOL')
			ttbfile.append('ANCHOR_XY')
			ttbfile.append('X')
			ttbfile.append(item['ANCHOR_XYX']) #0.000000000
			ttbfile.append('Y')
			ttbfile.append(item['ANCHOR_XYY']) #0.000000000
			ttbfile.append('END_ANCHOR_XY')
			ttbfile.append('ANGLE')
			ttbfile.append(item['ANGLE']) #0.000000000
			ttbfile.append('END_TOOL')
			ttbfile.append('LENGTH')
			ttbfile.append(item['LENGTH']) #0.000000000
			ttbfile.append('END_TOOL_LINE')
			ttbfile.append('ANCHOR_END')
			ttbfile.append('X')
			ttbfile.append(item['ANCHOR_ENDX']) # 1.343799705
			ttbfile.append('Y')
			ttbfile.append(item['ANCHOR_ENDY']) #0.000000000
			ttbfile.append('END_ANCHOR_END')
			ttbfile.append('END_TOOL_LINE_2P')
		if item['NAME'] == 'TOOL_ELLIPSE':
			ttbfile.append('TOOL_ELLIPSE')
			ttbfile.append('TOOL')
			ttbfile.append('ANCHOR_XY')
			ttbfile.append('X')
			ttbfile.append(item['ANCHOR_XYX'])
			ttbfile.append('Y')
			ttbfile.append(item['ANCHOR_XYY'])
			ttbfile.append('END_ANCHOR_XY')
			ttbfile.append('ANGLE')
			ttbfile.append(item['ANGLE'])
			ttbfile.append('END_TOOL')
			ttbfile.append('MAJOR_RADIUS')
			ttbfile.append(item['MAJOR_RADIUS'])
			ttbfile.append('MINOR_RADIUS')
			ttbfile.append(item['MINOR_RADIUS'])
			ttbfile.append('START_ANGLE')
			ttbfile.append(item['START_ANGLE'])
			ttbfile.append('END_ANGLE')
			ttbfile.append(item['END_ANGLE'])
			ttbfile.append('END_TOOL_ELLIPSE')
		if item['NAME'] == 'TOOL_ARC':
			ttbfile.append('TOOL_ARC')
			ttbfile.append('TOOL')
			ttbfile.append('ANCHOR_XY')
			ttbfile.append('X')
			ttbfile.append(item['ANCHOR_XYX']) # 0.660017701
			ttbfile.append('Y')
			ttbfile.append(item['ANCHOR_XYY']) # 0.273203134
			ttbfile.append('END_ANCHOR_XY')
			ttbfile.append('ANGLE')
			ttbfile.append(item['ANGLE']) # 0.000000000
			ttbfile.append('END_TOOL')
			ttbfile.append('RADIUS')
			ttbfile.append(item['RADIUS']) # 0.041358353
			ttbfile.append('START_ANGLE')
			ttbfile.append(item['START_ANGLE']) # 89.999690782
			ttbfile.append('END_ANGLE')
			ttbfile.append(item['END_ANGLE']) # 180.057529056
			ttbfile.append('END_TOOL_ARC')
	ttbfile.append('END_TOOLS')
	# convert everything to str:
	ttbfile = map(str, ttbfile)
	
	ttbtextfile = '\n'.join(ttbfile) # separate the lines
	#ttbtextfile = '\x00'.join(ttbtextfile) # interleave with \x00
	#ttbtextfile = ttbtextfile + '\x00' # add the final missing \x00
	# this turned out to be un-necessary
	return ttbtextfile

def decode_ttb(fname):
	alllines = []
	allobjects = []
	flines=open(fname, 'r').read().split()
	for line in flines:
		line = line.replace('\x00','') #Every other character in the file is '\x00'
		line = line.replace('\n', '') #Some lines are nothing because \r \n encoding.
		if line:
			alllines.append(line)
	obj = {}
	print('processing data structures.')
	while alllines: # process lines, parse out data objects.
		what = alllines.pop(0)
		if what in tools:
			obj['NAME'] = what
			continue
		if what in properties:
			value = float(alllines.pop(0))
			obj[what] = value
			continue
		if what in special_properties:
			#find x then y
			which = alllines.pop(0) # x or y
			value = float(alllines.pop(0))
			obj['{}{}'.format(what, which)] = value
			which = alllines.pop(0) # x or y
			value = float(alllines.pop(0))
			obj['{}{}'.format(what, which)] = value
			continue
		if what in end_tools:
			allobjects.append(obj)
			obj = {}
			continue
	return allobjects

def output_ttb(fname, allobjects):
	t=encode_ttb(allobjects)
	f=open(fname, 'w')
	f.write(t)
	f.close()


if __name__ == '__main__':
	if len(sys.argv) > 1:
		fname = sys.argv[-1]
		print(f'working on {fname}.')
		allobjects = decode_ttb(fname)

		# write the file back out to compare with the original.
		ofname = fname.replace('.', '_out.')
		print(f'writing {ofname}.')
		output_ttb(ofname, allobjects)

		print('done!')

	else:
		print('Nothing to do')
		print('try something like this:')
		print('python ttbview.py "10001400503 - outline.TTB')
pass

def make_circles():
	circles = []
	for x in np.arange(-1.0, 1.0, .1):
		for y in np.arange(-1.0, 1.0, .1):
			radius = np.random.random() * 0.1
			this_circle = get_ellipse(x, y, radius, radius, 0.0, 0.0, 0.0)
			circles.append(this_circle)
	return circles

def make_hatch():
	hatch = []
	for x in np.arange(-1.0, 1.0, .1):
		for y in np.arange(-1.0, 1.0, .1):
			this_line = get_line2p(x, y, 0.5, 0.0, x+.1, y+.1)
			hatch.append(this_line)
			this_line = get_line2p(x, y, 0.5, 0.0, x-.1, y+.1)
			hatch.append(this_line)
	return hatch

def make_diamonds(loose=True):
	step = 0.2 if loose else 0.1
	diamonds = []
	for x in np.arange(-1.0, 1.0, .1):
		for y in np.arange(-1.0, 1.0, step):
			this_line = get_line2p(x-.05, y, 0.5, 0.0, x, y+.1)
			diamonds.append(this_line)
			this_line = get_line2p(x+.05, y, 0.5, 0.0, x, y+.1)
			diamonds.append(this_line)
			this_line = get_line2p(x-.05, y, 0.5, 0.0, x, y-.1)
			diamonds.append(this_line)
			this_line = get_line2p(x+.05, y, 0.5, 0.0, x, y-.1)
			diamonds.append(this_line)
	return diamonds
