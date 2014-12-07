from math import *
class Graph:
        def __init__(self):
                self.graph = {}
                self.heuristic = None
                pass;
        def addVertice(self, node): #Add a vertice with no edges
                self.graph[node] = []

        def addEdge(self, node, edge):
                #Add a edge to a vertice
                self.graph[node] = self.graph[node] + [edge]
        
        def removeEdge(self, node, edge):
                #Remove a edge from a graph
                        #Search for a edge
                l = self.graph[node]
                i = 0
                for e in l:
                        if( e == edge):
                                break;
                        i+=1
                #Remove from the list of edges
                self.graph[node] = l[:i-1] + l[i+1:]

        def removeVertice(self,node):
                self.removeAllEdgesFromNode(node)
                del self.graph[node]

        def removeAllEdgesFromNode(self, node):
                vertices = self.graph.keys()
                for v in vertices:
                        if node in self.graph[v]:
                                self.graph[v].remove(node)


        def loadGrid(self, verticeInit, verticeEnd):
                initI = verticeInit[0]
                initJ = verticeInit[1]
                endI  = verticeEnd[0]
                endJ  = verticeEnd[1]

                for i in range(initI,endI):
                        for j in range(initJ, endJ):
                                self.addVertice((i,j))
                                if(i != initI):
                                        self.addEdge((i,j),(i-1,j))
                                elif(i != endI):
                                        self.addEdge((i,j),(i+1,j))

                                if(j != initJ):
                                        self.addEdge((i,j),(i,j-1))

                                elif(j != endJ):
                                        self.addEdge((i,j),(i,j+1))

        def aStar(self, start, goal):
                if self.heuristic == None:
                    self.heuristic = self.manhattanDistance
                closed = []
                openList = [start]
                cameFrom = {}
                gScore = {}
                fScore = {}
                gScore[start] = 0
                fScore[start] = self.heuristic(start,goal)
                fScore[-1] = 99999999
                while(openList):
                  current = self.chooseDestiny(openList,fScore)
                  if( current == goal):
                          return self.reconstructPath(cameFrom,goal)
                        
                  openList.remove(current)
                  closed.append(current)
                  neighborVertices = self.graph[current]
                  for n in neighborVertices:
                          if( n in closed):
                                  continue
                          tentative = gScore[current] + 1
                          if( not( n in openList) or tentative < gScore[n]):
                                cameFrom[n] = current
                                gScore[n] = tentative
                                fScore[n] = gScore[n] + self.heuristic(n,goal)
                                if( not ( n in openList)):
                                        openList = openList + [ n ]
                                        
                if(current == goal):
                  return self.reconstructPath(cameFrom,goal)
                                
                return False
        
        def manhattanDistance(self, start, goal):
                dx = abs(start[0] - goal[0])
                dy = abs(start[1] - goal[1])
                return 0.5 * sqrt((dx *dx + dy*dy))

        def chooseDestiny(self,openList, fScore):
                destiny = -1
                for d in openList:
                        if (fScore[destiny] > fScore[d]):
                                destiny = d
                return destiny

        def reconstructPath(self, cameFrom, currentNode):
                if(currentNode in cameFrom):
                        p = self.reconstructPath(cameFrom, cameFrom[currentNode])
                        return p + [currentNode]
                else:
                        return [(currentNode)]
