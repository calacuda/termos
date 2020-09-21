#!python3
"""
main.py

a terminal program that is like desmos

By: Calacuda | MIT Licence |
"""

import numpy as np
import scipy as sp
import plotille as plot
import argparse
import re


parser = argparse.ArgumentParser(description="A terminal based graphing calculator!")
parser.add_argument("-f", "--function", dest="functions", type=str, help="the function(s) to be graphed")
parser.add_argument("-x", dest="x", nargs=2, type=float, default=(-2, 10), help="the range of x's to display")
parser.add_argument("-y", dest="y", nargs=2, type=float, default=(-1, 10), help="the range of y's to display")
#parser.add_argument("-v", dest="vars", nargs="+", help="the variables and their values.")

args = parser.parse_args()


CONVERT = {"sin": "np.sin", "^": "**", "cos": "np.cos", "tan": "np.tan", "pi": "np.pi"}
TRIG_FS = set(CONVERT.keys())


def plot_it(xs, ys, names):
    fig = plot.Figure()
    fig.width=60 #(min(args.y)+max(args.x)) * 10
    fig.height=20 #(min(args.y)+max(args.y)) * 10
    fig.set_x_limits(min_= min(args.x), max_= max(args.x))
    fig.set_y_limits(min_= min(args.y), max_= max(args.y))
    fig.color_mode="byte"
    #fig.plot([0, 10], [-1, 10], lc=25, label='First line')
    for i in range(len(names)):
        #print(len(xs), len(ys)) 
        fig.plot(xs, ys[i], lc=50*(i+1), label=names[i])
        print(fig.show(legend=-True))


def get_y(xs, function):
    pass


def get_ys_old(xs, functions):
    names = []
    ys = []
    for i in range(len(functions)):
        name, function = functions[i].split("=")
        names.append(name.strip())
        ys.append([eval(function) for x in xs])
    return ys, names


def _get_ys(xs, f):
    #print(f"_get_ys(xs, {f}")
    try:
        ys = [eval(f) for x in xs]        
        #print(ys)
        return ys
    except NameError as msg:
        name = str(msg)[6]
        print(f)
        var = input(f"{str(msg)[6]} = ")
        operators = {"+", "-", "*", "/"}
        f = f.replace(" ", "")
        function = ""
        for i in range(len(f)):
            char = f[i]
            next_char = f[i+1] if i < len(f)-1 else None
            # print(f"{name}, {char}, {next_char}, {char == name and (f[i-1] in operators or next_char in operators)}")
            if char == name and (f[i-1] in operators or next_char in operators):
                function += var
            else:
                function += char
        return _get_ys(xs, function)


def get_ys(xs, functions):
    names = []
    ys = []
    for i in range(len(functions)):
        #print(functions[i])
        name = list(functions[i].keys())[0]
        #print(name)
        function = "".join(functions[i].get(name))
        names.append(name.strip())
        ys.append(_get_ys(xs, function))
    #print(ys)
    return ys, names


def trigify(fs):
    triged = []
    for f in fs:
        f = f.replace(" ", "")
        for key in CONVERT.keys():
            f = f.replace(key, CONVERT.get(key)) if key in f else f
            triged.append(f)
    return triged


def parser_old(functs):
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


def paren_split(functs):
    parsed = []
    for funct in functs:
        name, funct = funct.split("=")
        first_split = funct.split("(")
        second_split = []
        for chunk in first_split:
            if ")" in chunk:
                second_split += chunk.split(")")
            else:
                second_split.append(chunk)
                parsed.append({name: second_split})
    return parsed


def parse_trig(chunk):
    parsed = chunk
    for trig in CONVERT.keys():
        if trig in parsed:
            return parsed.replace(trig, CONVERT.get(trig)).replace(" ", "*")


def _parser(chunk):
    # print("chunk : ", chunk)
    parsed = chunk[0]
    for i in range(1, len(chunk)):
        if chunk[i].isalpha() and chunk[i-1].isalpha():
            parsed += "*" + chunk[i]
        else:
            parsed += chunk[i]
        # print(parsed)
    return parsed


def parser(funct):
    for name in funct.keys():
        f = funct.get(name)
        add_parens = False
        parsed_f = []
        for chunk in f:
            if len(chunk) == 0:
                break
            if len([_ for _ in TRIG_FS if _  in chunk]) > 0:
                parsed_chunk = parse_trig(chunk) if parse_trig(chunk) else chunk
                add_parens = True
            else:
                parsed_chunk = "(" + _parser(chunk) + ")" if add_parens else _parser(chunk)
                add_parens = False
            parsed_f.append(parsed_chunk)
            #print("appending : ", parsed_chunk)
        return {name: parsed_f}

        
def main_main(): 
    xs = np.arange(int(min(args.x)) + 1, int(max(args.x)) + 1, 0.125)
    functs = args.functions.split(",") if args.functions.split(",") else args.functions
    functs = parser(functs)
    print("parsed : ", functs)
    ys, names = get_ys(xs,  functs)
    plot_it(xs, ys, names)


def main():
    xs = np.arange(int(min(args.x)) + 1, int(max(args.x)) + 1, 0.125)
    functs = paren_split(args.functions.split(",") if args.functions.split(",") else args.functions)
    parsed = [parser(f) for f in functs]
    #print(parsed)
    ys, names = get_ys(xs, parsed)
    #print(ys)
    plot_it(xs, ys, names)
    
        
if __name__ == "__main__":
    main()
