#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################
# Simple script to create graph paper (linear or log scale)
# with python3 and matplotlib
# J. Labbé, december 2019, mise à jour novembre 2026
##############################

# Import everything from matplotlib (numpy is accessible via 'np' alias)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

### Parameters ===================================

# Number of decades for log scale
# set to zero for linear scale
xdecades = 3
ydecades = 0

# Output filename
# One can use wildcards :
#   %x and %y are replaced by the value of xdecades and ydecades
#   %s is replaced by '_semilog_n-decades' or '_log_n-m-decades' (or nothing with linear scale)
save      = True
filename  = "Examples/Papier%s"
extension =".pdf"

# Paper and figure
landscape   = True  # if true, swap width and height
centimeters = True  # if false, length unit is inch (matplotlib default)
paperwidth  = 21.0
paperheight = 29.7
figwidth    = 16.0
figheight   = 24.0
rightmargin = 2.5
topmargin   = 2.5

# line styles
major_linestyle = '-'
major_linewidth = 0.5
major_color     = "black"
major_alpha     = 1.0

minor_linestyle = '-'
minor_linewidth = 0.25
minor_color     = 'black'
minor_alpha     = 0.7

# Whether to call show()
showfig = False

### End of parameters block ======================

# Axes formatting function
def format_lin_axis(axis):
    """Format linear axis."""
    axis.set_major_locator(ticker.MultipleLocator(1))
    axis.set_minor_locator(ticker.MultipleLocator(0.1))
    axis.set_major_formatter(ticker.NullFormatter())
    axis.set_minor_formatter(ticker.NullFormatter())

def format_log_axis(axis):
    """Format logarithmic axis."""
    axis.set_major_locator(ticker.LogLocator(subs=np.arange(1,10)))
    minorsubs = []
    minorsubs.extend(np.arange(1.,6.,0.1))
    minorsubs.extend(np.arange(6.,10.,0.2))
    axis.set_minor_locator(ticker.LogLocator(subs=minorsubs))
    axis.set_major_formatter(ticker.FuncFormatter(log_label))
    axis.set_minor_formatter(ticker.NullFormatter())
    axis.set_tick_params(labelsize=6,pad=0)

def log_label(value, index):
    """Return logarithmic label (empty for 1)."""
    pos = index % 9 + 1
    return pos if pos > 1 else ''

# Create figure
unit = 1/2.54 if centimeters else 1
if landscape:
    paperheight, paperwidth = paperwidth, paperheight
    figheight, figwidth = figwidth, figheight
    rightmargin, topmargin = topmargin, rightmargin
fig, ax = plt.subplots(figsize=(paperwidth * unit, paperheight * unit))

# x axis
xmin = 0
xmax = figwidth
if (xdecades > 0):
    xmin = 10
    xmax = xmin*10**xdecades
    ax.set_xscale('log')
    format_log_axis(ax.xaxis)
else:
    format_lin_axis(ax.xaxis)

# y axis
ymin = 0
ymax = figheight
if (ydecades > 0):
    ymin = 10
    ymax = ymin*10**ydecades
    ax.set_yscale('log')
    format_log_axis(ax.yaxis)
else:
    format_lin_axis(ax.yaxis)

# x and y scales
ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)

# no ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# grid
ax.set_axisbelow(True) # grille sous le tracé
ax.grid(True, which='minor', axis='both',linestyle=minor_linestyle,linewidth=minor_linewidth,color=minor_color,alpha=minor_alpha)
ax.grid(True, which='major', axis='both',linestyle=major_linestyle,linewidth=major_linewidth,color=major_color,alpha=major_alpha)

# Margins
# from https://stackoverflow.com/questions/29400116/using-matplotlib-how-can-i-print-something-actual-size
leftmargin = paperwidth - figwidth - rightmargin
bottommargin = paperheight - figheight - topmargin
fig.subplots_adjust(left   = leftmargin / paperwidth,
                    bottom = bottommargin / paperheight,
                    right  = 1. - rightmargin / paperwidth,
                    top    = 1. - topmargin   / paperheight,
                    )

### Show and save

if save:
    if xdecades == 0 and ydecades == 0:
        filename = filename.replace('%s',"")
    elif xdecades != 0 and ydecades != 0:
        filename = filename.replace('%s',"_log_%x-%y-decades")
    elif xdecades + ydecades == 1:
        filename = filename.replace('%s',"_semilog_1-decade")
    else :
        filename = filename.replace('%s',"_semilog_"+str(xdecades+ydecades)+"-decades")
    filename = filename.replace('%x',str(xdecades))
    filename = filename.replace('%y',str(ydecades))
    fig.savefig(filename+extension,dpi=600)
    print("File "+filename+extension+" created.")

if showfig:
    plt.show()
