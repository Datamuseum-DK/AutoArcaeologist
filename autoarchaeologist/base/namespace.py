#!/usr/bin/env python3

'''
    AutoArchaeologist Namespace Class
    ---------------------------------

    `NameSpace` is for implementing the interior name spaces of
    filesystem and other directory-like structures.

    We represent namespaces as a directed graph identified by a
    single "root" Artifact, but impose no limitations on cycles
    in the graph or how NameSpace nodes map to Artifacts.

    Because all byte-identical Artifacts collapse into one, it is
    the rule rather than exception that Artifacts are present in
    multiple namespaces.

    Experience so far has shown that using NameSpace as a parent
    class does not make anything easier, but nontheless all attributes
    have been prefixed "ns_" to make it easier.

'''

class NameSpaceError(Exception):
    ''' ... '''

class NameSpace():

    '''
        NameSpace
        ---------

	A node in a NameSpace graph.

    '''

    def __init__(
        self,
        name = None,		# The leaf name of this node
        parent = None,		# The parent of this node
        this = None,		# The artifact named by this node
        separator = "/",	# The path separator for children of this node
        root = None,		# The artifact in which the name-space lives.
        priv = None,		# The artifact in which the name-space lives.
    ):
        self.ns_children = []
        self.ns_name = name
        self.ns_parent = None
        self.ns_separator = separator
        self.ns_this = None
        self.ns_root = None
        self.ns_priv = priv
        if root:
            self.ns_set_root(root)
        if parent:
            parent.ns_add_child(self)
        if this:
            assert parent
            self.ns_set_this(this)

    def __lt__(self, other):
        return self.ns_path() < other.ns_path()

    def __str__(self):
        return '<NS ' + str(self.ns_root) + " " + self.ns_path() + '>'

    def ns_set_root(self, root):
        ''' Set the root artifact '''
        if self.ns_root == root:
            return
        if self.ns_root:
            raise NameSpaceError("Root already set")
        if self.ns_parent:
            raise NameSpaceError("Root and Parent are exclusive")
        self.ns_root = root

    def ns_set_this(self, this):
        ''' Set this nodes artifact '''
        if self.ns_this == this:
            return
        assert self.ns_this is None
        self.ns_this = this
        this.add_namespace(self)

    def ns_path_recurse(self):
        ''' Get the parent path, including separator, to this node '''
        if not self.ns_parent:
            pfx = ""
        else:
            pfx = self.ns_parent.ns_path_recurse()
        return pfx + self.ns_name + self.ns_separator

    def ns_path(self):
        ''' Get the path to this node '''
        if not self.ns_parent:
            return  self.ns_name
        return self.ns_parent.ns_path_recurse() + self.ns_name

    def ns_render(self):
        ''' Return path and summary for interpretation table '''
        path = self.ns_path()
        if self.ns_this:
            return [ path, self.ns_this.summary(notes=True, descriptions=False, types=True) ]
        return [ path, None ]

    def ns_add_child(self, child):
        ''' Add an child under this node'''
        assert isinstance(child, NameSpace)
        self.ns_children.append(child)
        child.ns_parent = self
        child.ns_root = self.ns_root
        if child.ns_separator is None and self.ns_separator is not None:
            child.ns_separator = self.ns_separator

    def ns_recurse(self, level=0):
        ''' Recuse through the graph '''
        yield level, self
        for child in sorted(self.ns_children):
            yield from child.ns_recurse(level+1)

    def ns_html_plain(self, fo, _this):
        ''' Render recursively '''
        if not self.ns_children:
            return
        fo.write("<H3>" + self.KIND + "</H3>\n")
        fo.write("<div>")

        tbl = [x.ns_render() for y, x in self.ns_recurse() if y > 0]
        cols = max(len(x) for x in tbl)
        i = min(len(x) for x in tbl)
        if i != cols:
            print("WARNING: Namespace as uneven table", min, cols)

        fo.write('<table>\n')

        if self.TABLE:
            align = [x[0] for x in self.TABLE]
            hdr = [x[1] for x in self.TABLE]
            while len(align) < cols:
                align.append("l")
                hdr.append("-")
            fo.write('  <thead>\n')
            for a, h in zip(align, hdr):
                fo.write('      <th class="' + a + '">' + str(h) + '</th>\n')
            fo.write('  </thead>\n')
        else:
            align = ["l"] * cols

        fo.write('  <tbody>\n')
        for row in tbl:
            fo.write('    <tr>\n')
            for n, col in enumerate(row):
                if col is None:
                    col = '-'
                fo.write('      <td class="' + align[n] + '">' + str(col) + '</td>\n')
            fo.write('    </tr>\n')
        fo.write('  </tbody>\n')
        fo.write('</table>\n')
        fo.write("</div>")

    KIND = "Namespace"
    TABLE = None
