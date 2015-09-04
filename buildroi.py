#!/usr/bin/env python

#Creates a spherical ROI from a single coordinate
#

from __future__ import division
import argparse
import os
from subprocess import call

#parse command line arguments
parser = argparse.ArgumentParser(description="create spherical ROIs from coordinate")
parser.add_argument("x",help="x coordinate")
parser.add_argument("y",help="y coordinate")
parser.add_argument("z",help="z coordinate")
parser.add_argument("res",help="template resolution")
parser.add_argument("radius",help="radius in mm")
parser.add_argument("filename",help="output file name")
parser.add_argument("--vox",help="coordinates are voxel coordinates instead of MNI space",action="store_true")
parser.add_argument("-s",help="suppress FSL opening",action="store_true")
args = parser.parse_args()

def mmToVox(mmcoords):
	#function to convert mm coordinates into voxel coordinates

	voxcoords = ['','','']
	voxcoords[0] = str(int(round(int(mmcoords[0])/res))*-1+org[0])
	voxcoords[1] = str(int(round(int(mmcoords[1])/res))+org[1])
	voxcoords[2] = str(int(round(int(mmcoords[2])/res))+org[2])
	return voxcoords

org_05 = [180,252,144]
org_1 = [90,126,72]
org_2 = [45,63,36]

# set defaults:
org = org_2
template = "MNI152_T1_2mm_brain_mask"
res = float(2)

coords =[args.x,args.y,args.z]

if args.res == 0.5:
	org = org_05
	res = float(args.res)
	template = "MNI152_T1_0.5mm.nii.gz"
	suffix = "__0.5mm"
elif args.res == 1:
	org = org_1
	res = float(args.res)
	template = "MNI152_T1_2mm_brain_mask"
	suffix = "__1mm"
elif args.res == 2:
	org = org_2
	res = float(args.res)
	template = "MNI152_T1_2mm_brain_mask"
	suffix = "__2mm"
elif args.res == "avg":
	org = org_2
	res = float(2)
	template = "avg152T1_brain"
	suffix = "__avg152"
else:
	exit("\n\nERROR: template not known\n")

if args.vox:
	#convert from mm to voxel coords
	voxcoords = coords
else:
	voxcoords = mmToVox(coords)

outfile = args.filename + suffix


command = "fslmaths $FSLDIR/data/standard/%s -mul 0 -add 1 -roi %s 1 %s 1 %s 1 0 1 pytmp -odt float" % (template,voxcoords[0],voxcoords[1],voxcoords[2])
print command
call(command,shell=True)

command = "fslmaths pytmp -kernel sphere %s -fmean pytmp_un_bin -odt float" % (args.radius)
print command
call(command,shell=True)

command = "fslmaths pytmp_un_bin -bin %s" % outfile
print command
call(command,shell=True)

command = "rm pytmp.nii.gz"
call(command,shell=True)
command = "rm pytmp_un_bin.nii.gz"
call(command,shell=True)

if args.s:
	exit()
else:
	command = "fslview $FSLDIR/data/standard/%s %s -l Red&" % (template,outfile)
	call(command,shell=True)



