import math
import heapq

class DjikstraGraph(object):

    EPSILON = 0.01

    @staticmethod
    def euclidean(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    @staticmethod
    def from_voronoi(voronoi_result):
        ''' assume voronoi_result is a list of cells that have faces, vertices, adjacency'''
        verts = {}
        edges = {}
        vert_idx = 0
        for cell_idx, cell in enumerate(voronoi_result):
            local_edges = [(edge['vertices'], edge['adjacent_cell']) for edge in cell['faces']]
            local_start_vert_idx = vert_idx
            local_dups = {}
            # loop through and grab verts
            for vert in cell['vertices']:
                verts[vert_idx] = vert
                vert.append(vert_idx) # for finding dups later
                vert_idx += 1
            # loop through once, find duplicates
            for edge, adjacent_cell in local_edges:
                if adjacent_cell >= 0 and adjacent_cell < cell_idx:
                    # we have seen these verts before, need to merge
                    e_0_idx = edge[0] + local_start_vert_idx
                    e_1_idx = edge[1] + local_start_vert_idx
                    possible_verts = voronoi_result[adjacent_cell]['vertices']
                    e_0_dup_idx = -1
                    e_1_dup_idx = -1
                    for possible_vert in possible_verts:
                        if abs(possible_vert[0] - verts[e_0_idx][0]) < DjikstraGraph.EPSILON \
                            and abs(possible_vert[1] - verts[e_0_idx][1]) < DjikstraGraph.EPSILON:
                            # we know these two verts are the same by position, need to merge
                            e_0_dup_idx = possible_vert[2]
                        elif abs(possible_vert[0] - verts[e_1_idx][0]) < DjikstraGraph.EPSILON \
                            and abs(possible_vert[1] - verts[e_1_idx][1]) < DjikstraGraph.EPSILON:
                            e_1_dup_idx = possible_vert[2]
                    # now we have the two real vertex indicies for this edge
                    # store them for when we add to the edge map (local to this face)
                    local_dups[e_0_idx] = e_0_dup_idx
                    local_dups[e_1_idx] = e_1_dup_idx
                    
            for edge, adjacent_cell in local_edges:
                e_0_idx = edge[0] + local_start_vert_idx
                e_1_idx = edge[1] + local_start_vert_idx
                if e_0_idx in local_dups:
                    e_0_idx = local_dups[e_0_idx]
                if e_1_idx in local_dups:
                    e_1_idx = local_dups[e_1_idx]
                dist = DjikstraGraph.euclidean(verts[e_0_idx], verts[e_1_idx])
                if e_0_idx not in edges:
                    edges[e_0_idx] = [(e_1_idx, dist)]
                elif (e_1_idx, dist) not in edges[e_0_idx]:
                    edges[e_0_idx].append((e_1_idx, dist))
                if e_1_idx not in edges:
                    edges[e_1_idx] = [(e_0_idx, dist)]
                elif (e_0_idx, dist) not in edges[e_1_idx]:
                    edges[e_1_idx].append((e_0_idx, dist)) 
        return DjikstraGraph(verts, edges)

    def __init__(self, nodes, edge_weights, duplicate_list = []):
        self.node = nodes
        self.duplicate_list = duplicate_list
        self._edgeMap = edge_weights

    def get_adjacency(self, node_idx):
        ''' returns node index and edge weight as a tuple'''
        assert node_idx < len(self._edgeMap)
        return self._edgeMap[node_idx]

    def shortest_path(self, start, end):
        pq = [(0, start, [])]
        visited = set()
        while len(pq) > 0:
            (dist, vert, path) = heapq.heappop(pq)
            if vert not in visited:
                visited.add(vert)
                path.append(vert)
                if vert == end:
                    return (dist, path)
                for vert_other, next_dist in self.get_adjacency(vert):
                    if vert_other not in visited:
                        heapq.heappush(pq, (dist + next_dist, vert_other, path))
        return (-1, ())