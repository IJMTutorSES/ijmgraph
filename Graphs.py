from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt

first_run = True
all_colors = ["Crimson", "Orange", "Gold", "Maroon", "Sienna", "Olive", "YellowGreen", "DarkCyan",
              "MediumTurquoise", "DarkBlue", "RoyalBlue", "Indigo", "DarkMagenta"]
rem_colors = []


def rand_color():
    global first_run
    global rem_colors
    if first_run:
        rem_colors = all_colors.copy()
        first_run = False
    if len(rem_colors) == 0:
        rem_colors = all_colors.copy()
    ret_color = rem_colors[random.randint(0, len(rem_colors) - 1)]
    rem_colors.remove(ret_color)
    return ret_color


def graph(*args, width=20, color=[], export=None, minor_grid=1, major_grid=5, grid=True):
    width = int(width) // 2 * 2
    f = args

    # x and y values
    x_1 = np.linspace(0 - width / 2 - 1, width / 2 + 1, width * 100)
    y = [[] for _ in f]
    for idx, func in enumerate(f):
        for x in x_1:
            y[idx].append(func(x))
    # print("[Debug] x: " + str(min(x_1)) + "/" + str(max(x_1)))
    # print("[Debug] y[0]: " + str(min(y[0])) + "/" + str(max(y[0])))
    # print("[Debug] y[1]: " + str(min(y[1])) + "/" + str(max(y[1])))
    # print(y[0][0:20])
    # print(y[1][0:20])

    # Figure, Axes, Spines,
    fig_1 = plt.figure(figsize=(5, 5), dpi=100)
    axes_1 = fig_1.add_axes([0, 0, 1, 1])
    # axes_1.set_xlabel("x")
    # axes_1.set_ylabel("f(x)")
    axes_1.spines['left'].set_position('center')
    axes_1.spines['bottom'].set_position('center')
    axes_1.spines['right'].set_color('none')
    axes_1.spines['top'].set_color('none')
    max_ys = []  # only required for using the greatest f(x) values as ylim

    # Generating (random) colors for the functions
    if len(color) == 0:
        i = 1
        for func in f:
            color.append(rand_color())
            print("Farbe für f" + str(i) + ": " + color[-1])
            i += 1
    while len(color) < len(f):
        color.append("k")

    # Grid and ticks
    maj_ticks = np.arange(-width / 2 + ((width / 2) % major_grid), width / 2 - ((width / 2) % major_grid) + 0.5,
                          major_grid)
    min_ticks = np.arange(-width / 2 + ((width / 2) % minor_grid), width / 2 - ((width / 2) % minor_grid) + 0.5,
                          minor_grid)
    # maj_ticks = np.arange(-width / 2 + ((width / 2) % 5), width / 2 - ((width / 2) % 5) + 0.5, 5)
    # min_ticks = np.linspace(-width / 2, width / 2, width + 1)
    # print("[Debug] Ticks: " + maj_ticks, min_ticks)
    axes_1.set_xticks(maj_ticks)
    axes_1.set_yticks(maj_ticks)
    axes_1.set_xticks(min_ticks, minor=True)
    axes_1.set_yticks(min_ticks, minor=True)
    if grid:
        axes_1.grid(True, which="minor", color="0.5", lw=0.5)
        axes_1.grid(True, which="major", color="0.5", lw=1)
    axes_1.set_xlim(xmin=-width / 2 - 1, xmax=width / 2 + 1)
    axes_1.set_ylim(ymin=-width / 2 - 1, ymax=width / 2 + 1)
    # axes_1.set_ylim(ymin=-max(max_ys), ymax=max(max_ys))

    # Plotting the functions
    i = 1
    for y_func in y:
        axes_1.plot(x_1, y_func, label="f" + str(i) + "(x)", color=color[i - 1])
        max_ys.append(max(y_func))
        i += 1
    axes_1.text(width / 2 * 1.03, width / 2 * 0.02, "x")
    axes_1.text(-width / 2 * 0.13, width / 2 * 1.05, "f(x)")
    axes_1.legend(loc=0)

    # Optional export
    if export is not None:
        export = export.replace(".pdf", ".png")
        export = export.replace(".PDF", ".png")
        export = export.replace(".svg", ".png")
        export = export.replace(".SVG", ".png")
        export = export.replace(".jpg", ".png")
        export = export.replace(".JPG", ".png")
        export = export.replace(".jpeg", ".png")
        export = export.replace(".JPEG", ".png")
        if not export.endswith(".png"):
            export = export + ".png"
        plt.savefig(str(Path.home()) + "\\Desktop\\" + export, format="png", dpi=800, transparent=True)

    plt.show()
