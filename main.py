import parse.grammar as prs
import parse.vgrammar as vprs
import argparse
global s

def openfile(url):
    with open(url, 'r') as f:
        s = f.readlines()
        s = list(map(lambda s: s.strip(), s))
        s = ' '.join(s)
    return s

if __name__ == '__main__':

    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', help="파싱과정 생략, 변수 출력",  action="store_true")
    parser.add_argument('txtfile', help="location of txtfile")
    args = parser.parse_args()

    # get txt
    global s
    s = openfile(args.txtfile)

    # option v
    if args.v:
        vprs.program(s)
    # none option
    else:
        prs.program(s)