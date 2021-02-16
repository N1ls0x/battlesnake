import heapq

def aStar(self, grid, start, end):
    openList = set()
    closedList = set()

    def retracePath(c):
        def parentgen(c):
             while c:
                 yield c
                 c = c.parent
        result = [element for element in parentgen(c)]
        result.reverse()
        return result

    openList.add(start)
    while openList:
        start = sorted(openList, key=lambda inst:inst.H)[0]
        if start == end:
            return retracePath(start)
        openList.remove(start)
        closedList.add(start)
        for tile in grid[start]:
            if tile not in closedList:
                tile.H = (abs(end.x-tile.x)+abs(end.y-tile.y))*10 
                openList.add(tile)
                tile.parent = start
    return []