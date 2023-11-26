# scripts for ovito 2.9.0 stable version
# Usage: ovitos cfg2bin.py ccc.cfg xxx.txt xbin ybin
import argparse
from ovito.io import import_file
from ovito.io import export_file
from ovito.data import *
from ovito.modifiers import *
import numpy as np

# Define input and output
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="input file")
parser.add_argument("output", type=str, help="output file")
parser.add_argument("xbin", type=str, help="x bin number")
parser.add_argument("ybin", type=str, help="y bin number")
parser.add_argument("vname", type=str, help="variable name")

args = parser.parse_args()
input_filename = args.input
output_filename = args.output
x_bin_num = int(args.xbin)
y_bin_num = int(args.ybin)
var_name = args.vname

var_namer= 'R'+var_name

# Modifiers
node = import_file(input_filename)

expr=var_name+'*Mass/Mass'

calvname = ComputePropertyModifier(output_property = var_namer, expressions = [ expr ])
node.modifiers.append(calvname)


bar = BinAndReduceModifier(property= var_namer, direction=BinAndReduceModifier.Direction.Vectors_1_2, reduction_operation = BinAndReduceModifier.Operation.Mean, bin_count_x=x_bin_num, bin_count_y=y_bin_num)
node.modifiers.append(bar)

node.compute()

# Save file
np.savetxt(output_filename, bar.bin_data, delimiter=' ')

with open(output_filename, 'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write('# '+bar.property+' bin size X: '+str(bar.bin_count_x)+', bin size Y: '+str(bar.bin_count_y)+'\n'+content)
