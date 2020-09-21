#!python3
"""
main.py

a terminal program that is like desmos

By: Eoghan West | MIT Licence |
"""

import numpy as np
import scipy as sp
import plotille as plot
import argparse


parser = argparse.ArgumentParser(description="A terminal based graphing calculator!")
parser.add_argument("-f", "--function", dest="functions", type=str, help="the function(s) to be graphed")
parser.add_argument("-x", dest="x", nargs=2, type=float, default=(-2, 10), help="the range of x's to display")
parser.add_argument("-y", dest="y", nargs=2, type=float, default=(-1, 10), help="the range of y's to display")
#parser.add_argument("-v", dest="vars", nargs="+", help="the variables and their values.")

args = parser.parse_args()


CONVERT = {"sin": "np.sin", "^": "**", "cos": "np.cos", "tan": "np.tan", "pi": "np.pi"}


def plot_it(xs, ys, names):
    fig = plot.Figure()
    fig.width=60 #(min(args.y)+max(args.x)) * 10
    fig.height=20 #(min(args.y)+max(args.y)) * 10
    fig.set_x_limits(min_= min(args.x), max_= max(args.x))
    fig.set_y_limits(min_= min(args.y), max_= max(args.y))
    fig.color_mode="byte"
    #fig.plot([0, 10], [-1, 10], lc=25, label='First line')
    for i in range(len(names)):
        fig.plot(xs, ys[i], lc=50*(i+1), label=names[i])
    print(fig.show(legend=-True))


def get_y(xs, function):
    pass


def get_ys(xs, functions):
    names = []
    ys = []
    for i in range(len(functions)):
        name, function = functions[i].split("=")
        names.append(name.strip())
        ys.append([eval(function) for x in xs])
    return ys, names


def trigify(fs):
    triged = []
    for f in fs:
        f = f.replace(" ", "")
        for key in CONVERT.keys():
            f = f.replace(key, CONVERT.get(key)) if key in f else f
        triged.append(f)
    return triged


def parser(functs):
    """
    turns math jargen into python code.
    """
    functs = trigify(functs)
    parsed_fs = []
    for f in functs:
        if len(f) > 0:
            parsed = f[0]
        else:
            break
        begining = f.find("=")
        for i in range(1, len(f)):
            ch = f[i]
            if ((ch.isalpha() or ch == "(") and f[i-1].isnumeric()) and i > begining:
                foo = "*" + f[i]
            elif ((i < len(f) - 1) and (ch == ")" and f[i+1] not in {")", "+", "-", "*", "/"})) and i > begining:
                foo = f[i] + "*"
            else:
                foo = f[i]
            parsed += foo
        parsed_fs.append(parsed)
        print(parsed)
    return parsed_fs
    
    
def main(): 
    xs = np.arange(int(min(args.x)) + 1, int(max(args.x)) + 1, 0.125)
    functs = args.functions.split(",") if args.functions.split(",") else args.functions
    functs = parser(functs)
    ys, names = get_ys(xs,  functs)
    plot_it(xs, ys, names)

        
if __name__ == "__main__":
    main()
    
