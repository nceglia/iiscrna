import json
import networkx as nx
import pickle

class Interactions(object):
    
    def __init__(self, filename):
        MG = pickle.load( open( "interaction_network_occ_tcell.p", "rb" ) )
        self.rl = nx.get_node_attributes(MG,'type')
        self.nodes = list()
        self.edges = list()
        for node in MG.nodes():
            print(node)
            self.nodes.append({"id":node,"type":self.rl[node]})
        for edge in MG.edges(keys=True):
            edge_count = 0
            for oedge in MG.edges(keys=True):
                if edge[:2] == oedge[:2]:
                    edge_count += 1
            new_edge = { "source": edge[0], "target": edge[1], "value": edge_count}
            if not self.check_dup(new_edge):
                self.edges.append(new_edge)
        
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

    def check_dup(self, edge):
        for _edge in self.edges:
            if _edge["source"] == edge["source"] and _edge["target"] == edge["target"]:
                return True
        return False 

    def check_edge(self, edges, edge):
        for _edge in edges:
            if _edge["source"] == edge["source"] and _edge["target"] == edge["target"]:
                return True
        return False 

    def check_edge(self, edge):
        for _edge in edges:
            if _edge["source"] == edge["source"] and _edge["target"] == edge["target"]:
                return True
        return False 

    def node_data(self):
        rl_type = dict()
        for node in self.nodes:
            rl_type[node] = self.rl[node["id"]]
        return rl_type

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
