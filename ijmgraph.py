from pathlib import Path
from typing import Callable, List
from random import choice

import numpy as np
import matplotlib.pyplot as plt


class _Color:
    _colors = {
        "Crimson": False,
        "Orange": False, 
        "Gold": False, 
        "Maroon": False, 
        "Sienna": False, 
        "Olive": False, 
        "YellowGreen": False, 
        "DarkCyan": False,
        "MediumTurquoise": False, 
        "DarkBlue": False, 
        "RoyalBlue": False, 
        "Indigo": False, 
        "DarkMagenta": False
    }

    @classmethod
    def rand_color(cls):
        remaining = list(filter(lambda c: not cls._colors[c], cls._colors.keys()))
        color = np.random.choice(np.array(remaining))
        cls._colors[color] = True
        return color
    

    @classmethod
    def rand_colors(cls, count):
        return [cls.rand_color() for _ in range(count)]


def _gen_values(functions, width):
    x_values = np.linspace(0 - width / 2 - 1, width / 2 + 1, width * 100)
    y_values = [f(x_values) for f in functions]
    return x_values, y_values


def _gen_axes(fig, width, major, minor, grid):
    axes= fig.add_axes([0, 0, 1, 1])
    axes.spines['left'].set_position('center')
    axes.spines['bottom'].set_position('center')
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')

    mi_ticks = width / 2 - ((width / 2) % minor)
    ma_ticks = width / 2 - ((width / 2) % major)

    min_ticks = np.arange(-mi_ticks, mi_ticks + 0.5, minor)
    maj_ticks = np.arange(-ma_ticks, ma_ticks + 0.5, major)
    
    axes.set_xticks(maj_ticks)
    axes.set_yticks(maj_ticks)
    axes.set_xticks(min_ticks, minor=True)
    axes.set_yticks(min_ticks, minor=True)
        
    if grid:
        axes.grid(True, which="minor", color="0.6", lw=0.5)
        axes.grid(True, which="major", color="0.4", lw=1)
    
    axes.set_xlim(xmin=-width / 2 - 1, xmax=width / 2 + 1)
    axes.set_ylim(ymin=-width / 2 - 1, ymax=width / 2 + 1)

    return axes


def _plot(axes, width, x_values, func_y, graph_colors):
    for i, (y_values, color) in enumerate(zip(func_y,graph_colors)):
        axes.plot(x_values, y_values, label=f"f{i}(x)", color=color)
    axes.text(width / 2 * 1.03, width / 2 * 0.02, "x")
    axes.text(-width / 2 * 0.13, width / 2 * 1.05, "f(x)")
    axes.legend(loc=0)


def graph(*args: Callable, width: int=20, colors: List[str]=[], export: str=None, minor_grid: int=1, major_grid: int=5, grid: bool=True):
    """plot one or multiple functions (at most 13)

    Args:
        width (int, optional): Full Width of Plot. Defaults to 20.
        colors (list, optional): Given colors will be used to color the indivduall graphs. Defaults to random choice.
        export (str, optional): If given, the plot will be exported as <export>.png
        minor_grid (int, optional): Distance of minor ticks. Defaults to 1.
        major_grid (int, optional): Distance of major ticks. Defaults to 5.
        grid (bool, optional): Decides if the grid is drawn or not. Defaults to True.
    """    
    #Setup
    corrected_width = width // 2 * 2
    functions = args[:12]
    x_values, func_y = _gen_values(functions, corrected_width)
    graph_colors = _Color.rand_colors(len(functions)) if not colors else colors

    #Generating Figure
    figure = plt.figure(figsize=(5, 5), dpi=100)
    
    #Generating Axes (+ Grid)
    axes = _gen_axes(figure, corrected_width, major_grid, minor_grid, grid)

    #Plotting
    _plot(axes, corrected_width, x_values, func_y, graph_colors)
    
    #Displaying Plot
    plt.show()

    # Optional export
    if export:
        export_path = str(Path.home()) + export + ".png"
        plt.savefig(export_path, format="png", dpi=800, transparent=True)


def _test():
    def f1(x):
        return x ** 2
    
    def f2(x):
        return abs(x) * np.exp(x)
    
    def f3(x):
        return np.arcsin(np.sin(x))
    
    graph(f1, f2, f3, width=30)

if __name__ == "__main__":
    _test()