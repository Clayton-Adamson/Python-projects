# PE 15 COMPLETE!
# how many routes (down + right only) make it through a 20X20 grid
# Proud of solving it, but the code itself is not impressive.

grid_hell = []

for x in range(0,21):
    grid_hell.append([])
    for y in range(0,21):
        grid_hell[x].append(0)

for x in range(0,21):
    grid_hell[0][x] = 1
    grid_hell[x][0] = 1

for x in range(1,21):
    for y in range(1,21):
        if(grid_hell[y][x] == 0):
            grid_hell[y][x] = grid_hell[y][x-1] + grid_hell[y-1][x]

for x in range(0,21):
    print(grid_hell[x])

# bottom right corner is answer
