import datetime
from random import *
import matplotlib.pyplot as plt
from tkinter import *


def percolationSolver(size,showGrid,density):
    # Definition of the quick weighted union find begins here
    origin = {}
    weight = {}
    for i in range(size + 2):
        for j in range(size):
            origin[(i, j)] = (i, j)
            weight[(i, j)] = 1
    grid = [[0 for i in range(size)] for j in range(size + 2)]
    for j in range(size):
        grid[-1][j]=1
        grid[0][j]=1

    def root(a):
        dupe=a
        while(origin[dupe]!=dupe):
            dupe=origin[dupe]
        while(a!=dupe):
            temp=origin[a]
            origin[a]=dupe
            a=temp
        a=dupe
        return a

    def union(a,b):
        a=root(a)
        b=root(b)
        if(a==b):
            return
        if(weight[a]>=weight[b]):
            origin[b]=a
            weight[a]+=weight[b]
        else:
            origin[a]=b
            weight[b]+=weight[a]
    # Definition of the quick weighted union find ends here

    # Populating the grid based on given occupation probabilities.
    for i in range(size):
        for j in range(size):
            x=random()
            if(x<=density):
                grid[i+1][j]=1

    # Union every pair of adjacent open cells.
    for i in range(size+2):
        for j in range(size):
            if(grid[i][j]==1):
                if(i!=size+1)and(grid[i+1][j]==1):
                    union((i,j),(i+1,j))
                if(j!=size-1)and(grid[i][j+1]==1):
                    union((i,j),(i,j+1))

    # Tool to visualize the percolation.
    if (showGrid == True):
        rooter = Tk()
        rooter.title()
        C = Canvas(rooter, bg="white",
                   height=750, width=700)
        x=700/size
        C.pack()
        for i in range(size + 2):
            for j in range(size):
                if (grid[i][j] == 1):
                    C.create_rectangle(j * x, i * x, j * x + x, i * x + x, fill="white")
                else:
                    C.create_rectangle(j * x, i * x, j * x + x, i * x + x, fill="black")

        def showPercolates():
            for i in range(size + 2):
                for j in range(size):
                    if (root((i, j)) == root((0, 0))):
                        C.create_rectangle(j * x, i * x, j * x + x, i * x + x, fill="#1E90FF")

        C.after(3000, showPercolates)

        mainloop()
    # Used to count the number of iterations that percolation occurs for the given values.
    if(root((0,0))==root((size+1,size-1))):
        return 1
    else:
        return 0
print("Welcome to percolation visualizer! Here are some commands to follow:\n")
print("Run with 2 arguments of the format int float, the first being the size,")
print("the second being the occupation probability p of the lattice for a full demonstration. Eg 50 0.6\n")
print("Run with 3 arguments to plot a graph to determine the percolation threshold,")
print("the first argument being the size, the second being the number of iterations of occupation probabilities,")
print("the third being the number of iterations of each iterations of percolation densities. Eg 50 100 100")

readline=input()
inputs=readline.split()
start = datetime.datetime.now()

# Percolation Visualizer.
if(len(inputs)==2):
    size=int(inputs[0])
    density=float(inputs[1])
    visualize=True
    result=percolationSolver(size, visualize, density)
    if(result==1):
        print("Percolation Occurs!")
    else:
        print("Percolation does not occur")
    exit(0)
# Percolation threshold determination.
elif(len(inputs)==3):
    size = int(inputs[0])
    iterations = int(inputs[1])
    iter_per_iterations=int(inputs[2])
    visualize = False
else:
    print("Invalid number of arguments! Please try again.")
indices=[]

for i in range(iterations+1):
    d=0
    for j in range(iter_per_iterations):
        d+=percolationSolver(size,visualize,i/(iterations+1))
    indices.append(d*100//iter_per_iterations)
end = datetime.datetime.now()
plt.plot([(i*100)//len(indices) for i in range(0,len(indices))],indices)
plt.show()

end = datetime.datetime.now()
delta=end-start

print("Runtime for the program is :",delta.total_seconds(),"seconds.")

