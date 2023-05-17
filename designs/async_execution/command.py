class TreeNode:
    def __init__(self, data, root=True, parent=None, is_leaf=False):
        self.data = data

        self.root = root
        self.parent = parent
        self.is_leaf = is_leaf
        self.leafs = []

        self.as_key_name = None
        self.depth = 0

    def set_parent(self, parent):
        self.root = False
        self.parent = parent
        self.depth = parent.depth + 1
        self.is_leaf = True

    def add_leaf(self, leaf):
        leaf.set_parent(self)
        self.leafs.append(leaf)

    def add_leafs(self, *args):
        for arg in args:
            self.add_leaf(arg)

        return self

    def as_key(self, key: str):
        self.as_key_name = key

    def run(self, context=None):
        context = context if context else {}

        if self.leafs:
            for leaf in self.leafs:
                leaf.run(context)

        return context


tree_root_struction = TreeNode("A1")

result = tree_root_struction.add_leafs(
    TreeNode("B1"), TreeNode("B2").add_leafs(TreeNode("C1").add_leafs(TreeNode("D1")))
).run()
