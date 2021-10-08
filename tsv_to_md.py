#!/usr/bin/env python
import os
import sys
from io import StringIO

import numpy as np
import xerox

# OVERVIEW:
# input: data in the clipboard with tsv format
# output: markdown formatted table on your clipboard

# HOW TO USE:
# run tsv_to_md.command from spotlight (Command + Space) while you have tsv data in your clipboard.
# Example Input:
# attach_effective_start_date	attach_effective_end_date	current_row_ind
# 2002-06-21	2016-04-12	1
# 2002-09-11	2016-02-29	1
# 2002-11-08		1
# 2002-11-13		1

# Example Output: Note output only looks good with monospace font. use ``` in slack to make it look nice there.
# | attach_effective_start_date | attach_effective_end_date | current_row_ind |
# |-----------------------------|---------------------------|-----------------|
# | 2002-06-21                  | 2016-04-12                | 1               |
# | 2002-09-11                  | 2016-02-29                | 1               |
# | 2002-11-08                  |                           | 1               |
# | 2002-11-13                  |                           | 1               |


# SETUP:
# to run script as executable on mac
# make sure to pip install xerox
# create duplicate of this file (it should be in your data tools folder already though).
# If the .command doesn't already exist replace ".py" -> ".command"
# run `chmod +x <full-file-path>.command` in the terminal
# terminal -> preferences. On general tab select the profile you want to use by default.
# on profiles tab select the profile you are using as your default profile -> shell -> When the Shell Exits = "close if shell exited cleanly"


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def format_as_table(input_string, use_del):
    c = StringIO(input_string)
    matrix = np.loadtxt(c, dtype='str', delimiter=use_del, skiprows=0)
    matrix = np.atleast_2d(matrix)
    cols = matrix.shape[1]
    rows = matrix.shape[0]
    max_col_length = [max([len(x) for x in matrix[:, i]]) for i in range(cols)]

    for i in range(cols):
        matrix[:, i] = [s.ljust(max_col_length[i], ' ') for s in matrix[:, i]]

    output_list = []
    separator = '|-' + "-|-".join(["".ljust(i, '-') for i in max_col_length]) + '-|' + '\n'

    for i in range(rows):
        output_list.append('| ' + " | ".join(matrix[i,]) + ' |' + '\n')

        if i == 0:
            output_list.append(separator)
    return ''.join(output_list)


delimiter = '\t'
input_foramtted = xerox.paste()

if input_foramtted and '\n' in input_foramtted:
    output = format_as_table(input_foramtted, delimiter)
    xerox.copy(output)
