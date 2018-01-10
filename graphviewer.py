import sys
from matrix import Matrix
from filetemplates import *

def invalid_args():
        print("Invalid arguments given")
        print("Expecting 1 file with whitespace delimited adjacency matrix data")

def generate_HTML(adjMatrix):
        adjMatrix.print()

def generate_CSS(adjMatrix):
        print(adjMatrix.get_dimen())

def generate_JS(adjMatrix):
        pass

print("parsing command line arguments")
args = sys.argv
if len(args) != 2:
        invalid_args()
        quit()

try:
        inputdata = open(args[1], "r").read()
except IOError:
        print('"' + args[1] + '"' + " is invalid file")
        quit()

#files for viewing graph in browser
html = open("index.html", "w")
css  = open("index.css" , "w")
js   = open("index.js"  , "w")

rawdata   = inputdata.split()
adjMatrix = ""
try:
        adjMatrix = Matrix(rawdata)
except ValueError:
        print("Invalid graph data: dimensions non-square")

htmlString = generate_HTML(adjMatrix)
cssString  = generate_CSS(adjMatrix)
jsString   = generate_JS(adjMatrix)