import heapq
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Define cities and coordinates
cities = {
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Nagpur": (21.1458, 79.0882),
    "Nashik": (20.0059, 73.7649),
    "Aurangabad": (19.8762, 75.3433),
    "Solapur": (17.6599, 75.9064),
    "Amravati": (20.9374, 77.7796),
    "Thane": (19.2183, 72.9781),
    "Kolhapur": (16.7050, 74.2433),
    "Latur": (18.4088, 76.5604)
}

edges = [
    ("Mumbai", "Pune"), ("Mumbai", "Thane"),
    ("Pune", "Nashik"), ("Pune", "Solapur"),
    ("Nashik", "Aurangabad"), ("Aurangabad", "Nagpur"),
    ("Nagpur", "Amravati"), ("Thane", "Nashik"),
    ("Solapur", "Latur"), ("Latur", "Nagpur"),
    ("Kolhapur", "Pune"), ("Kolhapur", "Solapur")
]

# Graph setup
graph = nx.Graph()
for city, coord in cities.items():
    graph.add_node(city, pos=coord)
for u, v in edges:
    dist = geodesic(cities[u], cities[v]).km
    graph.add_edge(u, v, weight=round(dist, 2))

def compute_heuristic(goal):
    return {city: geodesic(cities[city], cities[goal]).km for city in cities}

# Algorithms
def bfs(start, goal):
    from collections import deque
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None

def dfs(start, goal, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    if start == goal:
        return path
    visited.add(start)
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            new_path = dfs(neighbor, goal, path + [neighbor], visited)
            if new_path:
                return new_path
    return None

def best_first(start, goal, h):
    queue = [(h[start], start, [start])]
    visited = set()
    while queue:
        _, node, path = heapq.heappop(queue)
        if node == goal:
            return path
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                heapq.heappush(queue, (h[neighbor], neighbor, path + [neighbor]))
    return None

def a_star(start, goal, h):
    queue = [(h[start], 0, start, [start])]
    visited = set()
    while queue:
        _, cost, node, path = heapq.heappop(queue)
        if node == goal:
            return path
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                g = cost + graph.edges[node, neighbor]['weight']
                f = g + h[neighbor]
                heapq.heappush(queue, (f, g, neighbor, path + [neighbor]))
    return None

def hill_climb(start, goal, h):
    path = [start]
    current = start
    while current != goal:
        neighbors = list(graph.neighbors(current))
        if not neighbors:
            return None
        next_node = min(neighbors, key=lambda n: h[n])
        if h[next_node] >= h[current]:
            return None
        path.append(next_node)
        current = next_node
    return path

def find_path(start, end, algo):
    h = compute_heuristic(end)
    if algo == 'BFS':
        return bfs(start, end)
    elif algo == 'DFS':
        return dfs(start, end)
    elif algo == 'Best-First':
        return best_first(start, end, h)
    elif algo == 'A*':
        return a_star(start, end, h)
    elif algo == 'Hill Climbing':
        return hill_climb(start, end, h)
    return None

def draw_graph(path, start, end):
    pos = nx.get_node_attributes(graph, 'pos')
    path_edges = list(zip(path, path[1:]))

    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_size=1000, node_color="lightblue")
    nx.draw_networkx_edges(graph, pos, edge_color='gray')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=3)
    plt.title(f"Route from {start} to {end}")
    plt.savefig("static/route.png")
    plt.close()

    return sum(graph.edges[path[i], path[i + 1]]['weight'] for i in range(len(path) - 1))
