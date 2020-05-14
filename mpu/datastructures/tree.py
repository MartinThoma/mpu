class Tree:
    def __init__(self, x):
        self.value = x
        self.children = []


def dfs(node):  # Binary Search Tree
    if node:
        yield from dfs(node.left)
        yield node
        yield from dfs(node.right)


def find_kth_smallest(binary_search_tree, K):
    def dfs(node):
        if node:
            if len(node.children) > 0:
                yield from dfs(node.children[0])
            yield node.value
            yield from dfs(node.right)

    f = dfs(binary_search_tree)
    for _ in range(K):
        ans = next(f)
    return ans
