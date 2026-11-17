#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################
# Simple script to create graph paper (linear or log scale)
# with python3 and matplotlib
# J. Labbé, december 2019, mise à jour novembre 2026
##############################

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

### Parameters ===================================

# Number of decades for log scale
# set to zero for a linear scale
XDECADES        = 3
YDECADES        = 2

# Output filename
# One can use wildcards :
#   %x and %y are replaced by the value of xdecades and ydecades
#   %s is replaced by '_semilog_n-decades' or '_log_n-m-decades' (or nothing with linear scale)
SAVE            = True
FILE_NAME       = "Examples/Papier%s"
EXTENSION       = ".pdf"

# Paper and figure
LANDSCAPE       = True
CENTIMETERS     = True  # if false, length unit is inch (matplotlib default)
PAPER_WIDTH     = 21.0
PAPER_HEIGHT    = 29.7
FIG_WIDTH       = 16.0
FIG_HEIGHT      = 24.0
RIGHT_MARGIN    = 2.5
TOP_MARGIN      = 2.5

# line styles
MAJOR_LINESTYLE = '-'
MAJOR_LINEWIDTH = 0.4
MAJOR_COLOR     = "black"
MAJOR_ALPHA     = 1.0

MINOR_LINESTYLE = '-'
MINOR_LINEWIDTH = 0.2
MINOR_COLOR     = 'black'
MINOR_ALPHA     = 1.0

# Whether to call show()
SHOWFIG = False

### End of parameters block ======================

X_DEC, Y_DEC = (YDECADES, XDECADES) if LANDSCAPE else (XDECADES, YDECADES)

# Axes formatting function
def format_lin_axis(axis):
    """Format linear axis."""
    axis.set_major_locator(ticker.MultipleLocator(1))
    axis.set_minor_locator(ticker.MultipleLocator(0.1))
    axis.set_major_formatter(ticker.NullFormatter())
    axis.set_minor_formatter(ticker.NullFormatter())

def format_log_axis(axis):
    """Format logarithmic axis."""
    majorsubs = np.arange(1, 10)
    axis.set_major_locator(ticker.LogLocator(subs=majorsubs, numticks=999))
    minorsubs = []
    minorsubs.extend(np.arange(1., 6., 0.1))
    minorsubs.extend(np.arange(6., 10., 0.2))
    axis.set_minor_locator(ticker.LogLocator(subs=minorsubs, numticks=999))
    axis.set_major_formatter(ticker.FuncFormatter(log_label))
    axis.set_minor_formatter(ticker.NullFormatter())
    axis.set_tick_params(labelsize=6, pad=0)

def log_label(value, _index):
    """Return logarithmic label (empty for 1)."""
    if value <= 0:
        return ''
    digit = int(round(value / (10 ** np.floor(np.log10(value)))))
    return str(digit) if 1 < digit < 10 else ''

# Create figure
UNIT = 1/2.54 if CENTIMETERS else 1
fig, ax = plt.subplots(figsize=(PAPER_WIDTH * UNIT, PAPER_HEIGHT * UNIT))

# x axis
xmin = 0
xmax = FIG_WIDTH
if X_DEC > 0:
    xmin = 10
    xmax = xmin * 10**X_DEC
    ax.set_xscale('log')
    format_log_axis(ax.xaxis)
else:
    format_lin_axis(ax.xaxis)

# y axis
ymin = 0
ymax = FIG_HEIGHT
if Y_DEC > 0:
    ymin = 10
    ymax = ymin * 10**Y_DEC
    ax.set_yscale('log')
    format_log_axis(ax.yaxis)
else:
    format_lin_axis(ax.yaxis)

# x and y scales
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# no ticks
ax.tick_params(
    axis='both', which='both',
    bottom=False, top=False,
    left=False, right=False,
)

# grid
ax.set_axisbelow(True) # grille sous le tracé
ax.grid(
    True, which='minor', axis='both',
    linestyle=MINOR_LINESTYLE, linewidth=MINOR_LINEWIDTH,
    color=MINOR_COLOR, alpha=MINOR_ALPHA,
)
ax.grid(
    True, which='major', axis='both',
    linestyle=MAJOR_LINESTYLE, linewidth=MAJOR_LINEWIDTH,
    color=MAJOR_COLOR, alpha=MAJOR_ALPHA,
)

# Highlight decades
frame_spine = ax.spines['left']
decade_lw = frame_spine.get_linewidth()
decade_color = frame_spine.get_edgecolor()
decade_ls = frame_spine.get_linestyle()

if X_DEC > 0:
    for exp in range(2, X_DEC + 1):
        ax.axvline(
            10**exp,
            linestyle=decade_ls,
            linewidth=decade_lw,
            color=decade_color,
        )

if Y_DEC > 0:
    for exp in range(2, Y_DEC + 1):
        ax.axhline(
            10**exp,
            linestyle=decade_ls,
            linewidth=decade_lw,
            color=decade_color,
        )

# Landscape
if LANDSCAPE:
    ax.invert_xaxis()
    ax.tick_params(
        axis='both', labelrotation=90,
        labelbottom=True, labelright=True,
        labeltop=False, labelleft=False
    )

# Margins
# from https://stackoverflow.com/questions/29400116/using-matplotlib-how-can-i-print-something-actual-size
if LANDSCAPE:
    top_margin = RIGHT_MARGIN
    right_margin = PAPER_WIDTH - FIG_WIDTH - TOP_MARGIN
else:
    top_margin = TOP_MARGIN
    right_margin = RIGHT_MARGIN
left_margin = PAPER_WIDTH - FIG_WIDTH - right_margin
bottom_margin = PAPER_HEIGHT - FIG_HEIGHT - top_margin
fig.subplots_adjust(
    left=left_margin / PAPER_WIDTH,
    bottom=bottom_margin / PAPER_HEIGHT,
    right=1. - right_margin / PAPER_WIDTH,
    top=1. - top_margin / PAPER_HEIGHT,
)

### Show and save

if SAVE:
    output_file = FILE_NAME + EXTENSION
    if XDECADES == 0 and YDECADES == 0:
        output_file = output_file.replace('%s', "")
    elif XDECADES != 0 and YDECADES != 0:
        output_file = output_file.replace('%s', "_log_%x-%y-decades")
    elif XDECADES + YDECADES == 1:
        output_file = output_file.replace('%s', "_semilog_1-decade")
    else:
        output_file = output_file.replace(
            '%s', "_semilog_" + str(XDECADES + YDECADES) + "-decades"
        )
    output_file = output_file.replace('%x', str(XDECADES))
    output_file = output_file.replace('%y', str(YDECADES))

    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    fig.savefig(output_file, dpi=None if EXTENSION == '.pdf' else 600)
    print("File " + output_file + " created.")

if SHOWFIG:
    plt.show()
