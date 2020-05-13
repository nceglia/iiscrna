import json

class Interactions(object):
    
    def __init__(self, filename):
        rows = open(filename,"r").read().splitlines()
        self.header = rows.pop(0).split("\t")
        celltypes = self.header.index("rank") + 1
        self.nodes = list()
        self.edges = list()
        self.visisted = set()
        for row in rows:
            row = row.split("\t")
            wrappedrow = dict(zip(self.header,row))
            if str(wrappedrow["gene_b"]).strip() == "": continue
            if str(wrappedrow["gene_a"]).strip() == "": continue
            if str(wrappedrow["gene_a"]).strip() not in self.visisted:
                self.nodes.append({ "id": str(wrappedrow["gene_a"]), "group": 0 })
                self.visisted.add(str(wrappedrow["gene_a"]).strip())
            if str(wrappedrow["gene_b"]).strip() not in self.visisted:
                self.nodes.append({ "id": str(wrappedrow["gene_b"]), "group": 0 })
                self.visisted.add(str(wrappedrow["gene_b"]).strip())
            for i, interaction in enumerate(row[celltypes:]):
                if interaction.strip() != "":
                    edge_label = self.header[i+celltypes].replace("|"," - ").replace("."," ") 
                    edge_label = edge_label.replace("cell","").replace("Vascular","").replace("Exhausted","Exh").replace("Activated", "Act").replace("Mesothelial","Meso").replace("Ovarian","").replace("Monocyte Macrophage","Macr")
                    edge_label = edge_label.replace(" cancer", "Canc").replace(" ","")
                    print(edge_label.strip())
                    self.edges.append({ "source": wrappedrow["gene_a"], "target": wrappedrow["gene_b"], "value": edge_label},)
    
    def expand_node(self, gene_name):
        _nodes = list()
        _edges = list()
        for edge in self.edges:
            if edge["source"] == gene_name or edge["target"] == gene_name:
                _edges.append(edge)
                if edge["source"] not in _nodes:
                    _nodes.append(edge["source"])
                if edge["target"] not in _nodes:
                    _nodes.append(edge["target"])
        return {"nodes": _nodes, "links": _edges}

    def check_edge(self, edges, edge):
        for _edge in edges:
            if _edge == edge:
                return True
        return False 

    def expand_nodes(self, gene_names):
        _nodes = list()
        _edges = list()
        for gene_name in gene_names:
            print(gene_name)
            for edge in self.edges:
                if edge["source"] == gene_name or edge["target"] == gene_name:
                    if not self.check_edge(_edges, edge):
                        _edges.append(edge)
                    if edge["source"] not in _nodes:
                        _nodes.append(edge["source"])
                    if edge["target"] not in _nodes:
                        _nodes.append(edge["target"])
        return {"nodes": _nodes, "links": _edges}

    def get_genes(self):
        return [node["id"] for node in self.nodes]

    def js_format(self, filename):
        data = {"nodes": self.nodes, "links": self.edges}
        output = open(filename,"w")
        output.write("export const data = {\n")
        output.write("  nodes: [\n")
        for node in self.nodes:
            output.write("\t\t"+str(node).replace("'id'","id").replace("'group'","group") + ",\n")
        output.write("  ], links: [\n")
        for edge in self.edges:
            output.write("\t\t"+str(edge).replace("'id'","id").replace("'group'","group").replace("'value'",'value').replace("'source'",'source').replace("'target'","target") + ",\n")
        output.write("\n  ] };\n")
        output.close()
