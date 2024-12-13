"""
Lab 2 template
"""

from collections import deque


def get_inner(string: str) -> str:
    """
    gets inner string between partenthases

    :param string: the raw text from file
    :return: inner string

    >>> get_inner("digraph asf { 0 -> 1 }")
    ' 0 -> 1 '
    """
    split_by_left: list[str] = string.split("{")
    if len(split_by_left) < 2:
        raise ValueError()

    split_by_right: list[str] = split_by_left[1].split("}")
    if len(split_by_right) < 2:
        raise ValueError()

    inner = split_by_right[0]
    return inner


def two_d_list_to_matrix(lst: list[list], default=0) -> list[list]:
    """
    Transforms 2D list to a uniform matrix

    :param lst: 2D list
    :param default: the value to fill in (should be a "value" type)

    :return: uniform 2D matrix

    >>> two_d_list_to_matrix([[1], [0, 1]])
    [[1, 0], [0, 1]]
    """
    max_length = max(len(sublist) for sublist in lst)
    matrix = [sublist + [default] * (max_length - len(sublist)) for sublist in lst]

    return matrix


def nodes(filename: str):
    """
    :param filename: the
    """
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    connections = get_inner(content).split(";")[:-1]

    for connection in connections:
        first_node, second_node = connection.split("->")
        first_node = int(first_node.strip())
        second_node = int(second_node.strip())

        yield first_node, second_node


def read_incidence_matrix(filename: str) -> list[list[int]]:
    """
    :param str filename: path to file
    :returns list[list]: the incidence matrix of a given graph
    """
    result: list[list[int]] = []

    for first_node, second_node in nodes(filename):
        result.append([0] * max(first_node + 1, second_node + 1))

        if first_node == second_node:
            result[-1][first_node] = 2

        result[-1][first_node] = 1
        result[-1][second_node] = -1

    return two_d_list_to_matrix(result)


def read_adjacency_matrix(filename: str) -> list[list]:
    """
    Note: the veritices must be 0, 1, ... without skipping

    :param filename: path to file
    :returns list[list]: the adjacency matrix of a given graph
    """
    result: list[list[int]] = [[]]

    for first_node, second_node in nodes(filename):
        if len(result) < first_node + 1:
            result.extend([[] for _ in range(first_node + 1 - len(result))])

        if len(result[first_node]) < second_node + 1:
            result[first_node] += [0] * (second_node + 1 - len(result[first_node]))

        result[first_node][second_node] += 1

    return two_d_list_to_matrix(result)


def read_adjacency_dict(filename: str) -> dict[int, list[int]]:
    """
    :param str filename: path to file
    :returns dict: the adjacency dict of a given graph
    """
    result: dict[int, list[int]] = {}

    for first_node, second_node in nodes(filename):
        result.setdefault(first_node, []).append(second_node)

    return result


def iterative_adjacency_dict_dfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> iterative_adjacency_dict_dfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> iterative_adjacency_dict_dfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    ans = []
    stack = []
    stack.append(start)
    while stack:
        vertex = stack.pop()
        if vertex not in ans:
            ans.append(vertex)
            graph[vertex] = sorted(graph[vertex], reverse=True)
            for neighbor in graph[vertex]:
                if neighbor not in ans:
                    stack.append(neighbor)
    return ans


def iterative_adjacency_matrix_dfs(graph: list[list], start: int) -> list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> iterative_adjacency_matrix_dfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> iterative_adjacency_matrix_dfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    ans = []
    stack = []
    stack.append(start)
    while stack:
        vertex = stack.pop()
        if vertex not in ans:
            ans.append(vertex)
            for neighbor, edge in reversed(list(enumerate(graph[vertex]))):
                if edge:
                    if neighbor not in ans:
                        stack.append(neighbor)
    return ans


def recursive_adjacency_dict_dfs(
    graph: dict[int, list[int]], start: int, path: list[int] | None = None
) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> recursive_adjacency_dict_dfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> recursive_adjacency_dict_dfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    if path is None:
        path = []

    path += [start]

    for node in graph[start]:
        if node not in path:
            recursive_adjacency_dict_dfs(graph, node, path)

    return path


def recursive_adjacency_matrix_dfs(
    graph: list[list[int]], start: int, path: list[int] | None = None
) -> list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> recursive_adjacency_matrix_dfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> recursive_adjacency_matrix_dfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    if path is None:
        path = []

    path += [start]

    for i, node in enumerate(graph[start]):
        if i not in path and node == 1:
            recursive_adjacency_matrix_dfs(graph, i, path)

    return path


def iterative_adjacency_dict_bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the bfs traversal of the graph
    >>> iterative_adjacency_dict_bfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> iterative_adjacency_dict_bfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    ans = []
    q = deque()
    q.append(start)
    while q:
        vertex = q.popleft()
        if vertex not in ans:
            ans.append(vertex)
            graph[vertex] = sorted(graph[vertex])
            for neighbor in graph[vertex]:
                if neighbor not in ans:
                    q.append(neighbor)
    return ans


def iterative_adjacency_matrix_bfs(graph: list[list[int]], start: int) -> list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the bfs traversal of the graph
    >>> iterative_adjacency_matrix_bfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> iterative_adjacency_matrix_bfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    ans = []
    q = deque()
    q.append(start)
    while q:
        vertex = q.popleft()
        if vertex not in ans:
            ans.append(vertex)
            for neighbor, edge in enumerate(graph[vertex]):
                if edge:
                    if neighbor not in ans:
                        q.append(neighbor)
    return ans


def adjacency_matrix_radius(graph: list[list]) -> int:
    """
    :param list[list] graph: the adjacency matrix of a given graph
    :returns int: the radius of the graph
    >>> adjacency_matrix_radius([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    1
    >>> adjacency_matrix_radius([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    1
    """

    def find_max_distance(graph: list[list], start: int) -> int:
        # This function finds the biggest distance from given
        # vertex to any other vertex in a connected graph
        visited = []
        q = deque()
        q.append((start, 0))
        max_dist = -1
        while q:
            vertex, dist = q.popleft()
            if vertex not in visited:
                max_dist = max(max_dist, dist)
                visited.append(vertex)
                for neighbor, edge in enumerate(graph[vertex]):
                    if edge:
                        if neighbor not in visited:
                            q.append((neighbor, dist + 1))
        return max_dist

    radius = 1e9
    for vertex in range(len(graph)):
        max_dist = find_max_distance(graph, vertex)
        radius = min(radius, max_dist)
    return radius


def adjacency_dict_radius(graph: dict[int : list[int]]) -> int:
    """
    :param dict graph: the adjacency list of a given graph
    :returns int: the radius of the graph
    >>> adjacency_dict_radius({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    1
    >>> adjacency_dict_radius({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [1]})
    1
    """

    def find_max_distance(graph: dict[int : list[int]], start: int) -> int:
        # This function finds the biggest distance from given
        # vertex to any other vertex in a connected graph
        visited = []
        q = deque()
        q.append((start, 0))
        max_dist = -1
        while q:
            vertex, dist = q.popleft()
            if vertex not in visited:
                max_dist = max(max_dist, dist)
                visited.append(vertex)
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        q.append((neighbor, dist + 1))
        return max_dist

    radius = 1e9
    for vertex in graph.keys():
        max_dist = find_max_distance(graph, vertex)
        radius = min(radius, max_dist)
    return radius


if __name__ == "__main__":
    import doctest

    doctest.testmod()
