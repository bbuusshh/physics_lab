#!/usr/bin/env python
# coding: utf-8

from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import os.path
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib import rc, font_manager, gridspec

PARAMS = {
    "title_font_size": 20,
    "grid_linewidth": 1,
    "grid_color":"orange",
    "grid_linestyle": "--",
    "ticks_lenght": 4,
    "ticks_lenght_minor": 2.5,
    "ticks_width": 2,
    "grid_alpha": 0.4,
    "labels_font_size": 20,
    "saveDir": ".",
    "fontsize":20,
    "fontStyle":'Arial',
    "plot_name":'default_name'
}


class plotting:
    def __init__(self, parameters=PARAMS):
        """
    Default parameters
    PARAMS = {
        "title_font_size": 25,
        "grid_linewidth": 1,
        "grid_color":"orange",
        "grid_linestyle": "--",
        "ticks_lenght": 4,
        "ticks_lenght_minor": 2.5,
        "ticks_width": 2,
        "grid_alpha": 0.4,
        "labels_font_size": 25,
        "saveDir": ".",
        "fontsize":15,
        "fontStyle":'Arial',
        "plot_name":'default_name'
    }

        """
        self.__dict__.update(parameters)
        self.plot_name = "ein_plot"
        fontProperties = {'family':'Arial',
            'weight' : 'normal', 'size' : self.fontsize}
        ticks_font = font_manager.FontProperties(family=self.fontStyle, style='normal',
            size=self.fontsize, weight='normal', stretch='normal')
        #rc('text', usetex=True)
        rc('font',**fontProperties)

    def plot(
        self,
        xData,
        yData,
        xLabel="X",
        yLabel="Y",
        nrows=1,
        xUnits=None,
        yUnits=None,
        title=None,
        line="o",
        figsize=(10, 6),
        logy=False,
        logx=False,
        fill=None,
        tick_step_x=None,
        tick_step_y=None,
        ticks_in_between=2,
        dpi=100
    ):
        self.plot_name = title
#         fig = plt.figure()
#         # set height ratios for sublots
#         gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1]) 
#         ax0 = plt.subplot(gs[0])
#         ax1 = plt.subplot(gs[1], sharex = ax0)
#         plt.subplots_adjust(hspace=.0)
#         plt.show()
        
        fig, ax = plt.subplots(nrows, sharex=True, figsize=figsize, dpi=dpi, constrained_layout=True)
#         fig.subplots_adjust(left=0, bottom=0, right=5, top=5, wspace=0, hspace=0)
#         ax=ax[0]
        if fill:
            ax.fill_between(xData, 0, yData, alpha=fill)

        if logy and logx:
            plt.loglog(xData, yData, line, clip_on=True)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        elif logx:
            plt.semilogx(xData, yData, line, clip_on=False)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        elif logy:
            plt.semilogy(xData, yData, line, clip_on=False)
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))

        else:
            plt.plot(xData, yData, line, clip_on=False)

        plt.grid(linestyle=self.grid_linestyle, linewidth=self.grid_linewidth)
                
        if title:
            plt.title(title, fontsize=self.title_font_size)
        if xUnits:
            plt.xlabel(f"{xLabel} ({xUnits})", fontsize=self.labels_font_size)
        else:
            plt.xlabel(f"{xLabel}", fontsize=self.labels_font_size)
        if yUnits:
            plt.ylabel(f"{yLabel} ({yUnits})", fontsize=self.labels_font_size)
        else:
            plt.ylabel(f"{yLabel}", fontsize=self.labels_font_size)
        # plt.legend()
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
            ax.spines[axis].set_color("black")
            ax.spines[axis].set_zorder(0)

        ax.yaxis.set_ticks_position('both')
        ax.tick_params()       
#         ax.yaxis.set_ticklabels()
#         ax.axes.get_xaxis().set_visible(False)
#         ax.axes.get_yaxis().set_visible(False)
        ax.xaxis.set_ticks_position('both')
        plt.tick_params(axis='both', which='both',
            direction="in",
            length=self.ticks_lenght,
            width=self.ticks_width,
            grid_color=self.grid_color,
            labelsize=self.fontsize,
            grid_alpha=self.grid_alpha, 
            labeltop=False, labelright=False,
        )
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        if tick_step_x:
            ax.xaxis.set_major_locator(MultipleLocator(tick_step_x))
            ax.xaxis.set_minor_locator(MultipleLocator(tick_step_x/(ticks_in_between + 1)))
        if tick_step_y:
            ax.yaxis.set_major_locator(MultipleLocator(tick_step_y))
            ax.yaxis.set_minor_locator(MultipleLocator(tick_step_y/(ticks_in_between + 1)))
        
        return fig, ax

    def plotAx(
        self,
        xData,
        yData,
        ax,
        xLabel="X",
        yLabel="Y",
        xUnits=None,
        yUnits=None,
        title=None,
        line="o",
#         figsize=(10, 6),
        logy=False,
        logx=False,
        fill=None,
        grid=True,
        clip_on=False,
        tick_step_x=None,
        tick_step_y=None,
        ticks_in_between=2,
#         dpi=100
    ):
        self.plot_name = title
        if fill:
            ax.fill_between(xData, 0, yData, alpha=fill)

        if logy and logx:
            plt.loglog(xData, yData, line, clip_on=True)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        elif logx:
            plt.semilogx(xData, yData, line, clip_on=False)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        elif logy:
            plt.semilogy(xData, yData, line, clip_on=False)
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))

        else:
            plt.plot(xData, yData, line, clip_on=clip_on)
        if grid:
            plt.grid(linestyle=self.grid_linestyle, linewidth=self.grid_linewidth, c=self.grid_color)
                
        if title:
            plt.title(title, fontsize=self.title_font_size)
        if xUnits:
            plt.xlabel(f"{xLabel} ({xUnits})", fontsize=self.labels_font_size, family=self.fontStyle)
        else:
            plt.xlabel(f"{xLabel}", fontsize=self.labels_font_size, family=self.fontStyle)
        if yUnits:
            plt.ylabel(f"{yLabel} ({yUnits})", fontsize=self.labels_font_size, family=self.fontStyle)
        else:
            plt.ylabel(f"{yLabel}", fontsize=self.labels_font_size, family=self.fontStyle)
        # plt.legend()
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
            ax.spines[axis].set_color("black")
            ax.spines[axis].set_zorder(0)

        ax.yaxis.set_ticks_position('both')
        ax.tick_params()       
#         ax.yaxis.set_ticklabels()
#         ax.axes.get_xaxis().set_visible(False)
#         ax.axes.get_yaxis().set_visible(False)
        ax.xaxis.set_ticks_position('both')
        plt.tick_params(axis='both', which='both',
            direction="in",
            length=self.ticks_lenght,
            width=self.ticks_width,
            labelsize=self.fontsize, 
            labeltop=False, labelright=False,
        )
        ax.tick_params(axis='both', which='minor',
                       direction='in', 
                       length=self.ticks_lenght_minor
                      )
        
        plt.xticks(fontsize=self.fontsize, family=self.fontStyle)
        plt.yticks(fontsize=self.fontsize, family=self.fontStyle)
        if tick_step_x:
            ax.xaxis.set_major_locator(MultipleLocator(tick_step_x))
            ax.xaxis.set_minor_locator(MultipleLocator(tick_step_x/(ticks_in_between + 1)))
        if tick_step_y:
            ax.yaxis.set_major_locator(MultipleLocator(tick_step_y))
            ax.yaxis.set_minor_locator(MultipleLocator(tick_step_y/(ticks_in_between + 1)))
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
            ax.spines[axis].set_color("black")
            ax.spines[axis].set_zorder(0)
        return ax
    
#         ax.add_patch(plt.Rectangle((0,0),1,1, color="w", transform=ax.transAxes))

    def save(self, name=None, extension='pdf'):
        if name:
            self.plot_name=name
        if not os.path.isfile(f"{self.plot_name}_0.{extension}"):
            plt.savefig(f"{self.saveDir}/{self.plot_name}_0.{extension}")
        else:
            count = 0
            while os.path.isfile(f"{self.plot_name}_{count}.{extension}"):
                count += 1
            plt.savefig(f"{self.saveDir}/{self.plot_name}_{count}.{extension}")
        plt.show()