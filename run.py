from flask import Flask, jsonify, render_template, request
app = Flask(__name__, static_folder='static')

from data import Interactions

ii = Interactions("data/significant_means.txt")

@app.route('/expand')
def expand_node():
    global ii
    gene = request.args.get('gene')
    result = ii.expand_node(gene)
    return jsonify(result)

@app.route('/genes')
def get_genes():
    global ii
    genes = ii.get_genes()
    return jsonify(genes=genes)

@app.route('/expands')
def expand_nodes():
    global ii
    genes = request.args.get('genes').split(",")
    result = ii.expand_nodes(genes)
    return jsonify(result)