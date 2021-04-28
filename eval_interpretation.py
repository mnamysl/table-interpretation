import io
import os
import glob
import json
import re

import numpy as np
import networkx as nx



def load_json_files(dir_path: str):

    results = dict() # key: file-path; value: file-content
    pattern = f"{dir_path}/**/*interpretation.json"
    #print(pattern)

    cnt_loaded = 0
    for file_path in glob.glob(pattern, recursive=True): 
         
        basename = os.path.basename(file_path)
        m = re.match("(.*)_page(\d+)_table(\d+)_interpretation.json", basename)

        if m:
            name, pageNr, tableNr = m.group(1), m.group(2), m.group(3)
            print(f"[OK] file:'{file_path}' name:'{name}' page:{pageNr} table:{tableNr}")

            with open(file_path) as f:
                data = json.load(f)

                if data:
                    #print(data)
                    items = results.get(name, list())
                    # converting the list of dicts to the list of tuples (which can be hashed as keys in a dictionary)
                    #items.append([tuple((k, v) for k,v in d.items()) for d in data])
                    items.append([tuple((k.replace(" ", ""), v.replace(" ", "")) for k,v in d.items()) for d in data])
                    
                    results[name] = items
                    cnt_loaded += 1
                else:
                    print(f"[FAILED] '{file_path}' cannot be parsed! Content: {data}")
    
    print(f"Summary: loaded {cnt_loaded} files.")

    return results


def count_tuples(data, verbose):
    
    total = 0
    for k,v in data.items():
        cnt = 0
        for idx, item in enumerate(v):
            cnt += len(item)

        total += cnt
        if verbose:
            print(f"'{k}': {cnt}")

    return total

def print_dict(data):
    
    for k,v in data.items():
        print(f"key: '{k}'")
        for idx, item in enumerate(v):
            print(f"  #{idx:02d}: {item}")

def print_line(n: int = 50, prefix="", c='-'):
    print(f"{prefix}{c * n}")

def _calc_scores(TP, FN, FP):

    TPFP = TP + FP
    TPFN = TP + FN
    precision = TP / TPFP if TPFP > 0.0 else 0.0
    recall = TP / TPFN if TPFN > 0 else 0.0

    prec_rec = precision + recall
    F1 = 2 * precision * recall / prec_rec if prec_rec > 0.0 else 0.0

    return precision, recall, F1


def _eval_pair(gt_data, res_data, TP, FN, FP):

    gt_set = set(gt_data)
    res_set = set(res_data)

    TP += len(gt_set & res_set)
    FN += len(gt_set - res_set)
    FP += len(res_set - gt_set)

    return TP, FN, FP

def _create_graph_dummy():

    # init a (bipartite) graph
    G = nx.Graph()
    gt_nodes, res_nodes, edges = set(), set(), set()
    scores = dict()
    
    gt_nodes.add("gt_x1")
    gt_nodes.add("gt_x2")
    gt_nodes.add("gt_x3")

    res_nodes.add("res_y1")
    res_nodes.add("res_y2")
    res_nodes.add("res_y3")
    res_nodes.add("res_y4")
   
    weights = dict()
    weights[("gt_x1", "res_y1")] = 0.9
    weights[("gt_x1", "res_y2")] = 0.7
    weights[("gt_x1", "res_y3")] = 0.1
    weights[("gt_x1", "res_y4")] = 0.3

    weights[("gt_x2", "res_y1")] = 0.3
    weights[("gt_x2", "res_y2")] = 0.1
    weights[("gt_x2", "res_y3")] = 0.6
    weights[("gt_x2", "res_y4")] = 0.2

    weights[("gt_x3", "res_y1")] = 0.5
    weights[("gt_x3", "res_y2")] = 0.4
    weights[("gt_x3", "res_y3")] = 0.2
    weights[("gt_x3", "res_y4")] = 0.1

    for gt_idx, gt_node in enumerate(gt_nodes):
        for res_idx, res_node in enumerate(res_nodes):
            weight = weights[(gt_node, res_node)]
            scores[(gt_node, res_node)] = (0, 0, 0, 0, 0, weight)
            edges.add((gt_node, res_node, weight))

    G.add_nodes_from(gt_nodes, bipartite=0)
    G.add_nodes_from(res_nodes, bipartite=1)
    G.add_weighted_edges_from(edges)

    print(f"\tgt_nodes:  {gt_nodes}")
    print(f"\tres_nodes: {res_nodes}")
    print(f"\tedges: {edges}")

    return G, gt_nodes, res_nodes, {}, scores

def _create_graph(gt_items, res_items):

    # init a (bipartite) graph
    G = nx.Graph()
    gt_nodes, res_nodes, edges = set(), set(), set()
    node2item = dict()
    scores = dict()
    
    for gt_idx, gt_item in enumerate(gt_items):
        gt_node = f"gt_{gt_idx}"
        gt_nodes.add(gt_node)
        node2item[gt_node] = gt_item

        for res_idx, res_item in enumerate(res_items):
            res_node = f"res_{res_idx}"
            res_nodes.add(res_node)
            node2item[res_node] = res_item
            
            pair_TP, pair_FN, pair_FP = _eval_pair(gt_item, res_item, 0, 0, 0)
            pair_P, pair_R, pair_F1 = _calc_scores(pair_TP, pair_FN, pair_FP)
            score = pair_F1

            edges.add((gt_node, res_node, score))

            scores[(gt_node, res_node)] = (pair_TP, pair_FN, pair_FP, pair_P, pair_R, pair_F1)

            print(f"\tedge:  {gt_node} -> {res_node} : {score}")

    print_line(n=30, prefix="\t")
    
    # create a bipartite graph from the pairs and run maximum weighted matching
    #gt_nodes = sorted(gt_nodes)
    #res_nodes = sorted(res_nodes)
    G.add_nodes_from(gt_nodes, bipartite=0)
    G.add_nodes_from(res_nodes, bipartite=1)
    G.add_weighted_edges_from(edges)

    print(f"\tgt_nodes:  {gt_nodes}")
    print(f"\tres_nodes: {res_nodes}")
    #print(f"\tedges:     {edges}")

    return G, gt_nodes, res_nodes, node2item, scores

def _eval_pairs_on_page(gt_items, res_items, TP, FN, FP):
    
    # calculate all scores for each pair of tables in the GT and RES data
    cnt_gt, cnt_res = len(gt_items), len(res_items)

    G, gt_nodes, res_nodes, node2item, scores = _create_graph(gt_items, res_items)
    #G, gt_nodes, res_nodes, node2item, scores = _create_graph_dummy()

    matches = nx.max_weight_matching(G)
    print(f"MATCHES:   {matches}")

    print_line(n=30, prefix="\t")

    page_TP, page_FN, page_FP = 0, 0, 0

    for n1, n2 in matches:
        gt_node = n1 if n1.startswith("gt_") else n2
        res_node = n1 if n1.startswith("res_") else n2

        pair_TP, pair_FN, pair_FP, pair_P, pair_R, pair_F1 = scores[(gt_node, res_node)] 
        print(f"\tmatch: {gt_node} -> {res_node} : {pair_F1}")

        page_TP += pair_TP
        page_FN += pair_FN
        page_FP += pair_FP

        gt_nodes.remove(gt_node)
        res_nodes.remove(res_node)

    #print(f"REMAINING GT nodes:  {gt_nodes}")
    #print(f"REMAINING RES nodes: {res_nodes}")

    if len(node2item) > 0:
        for n in gt_nodes:
            fn = len(set(node2item[n]))
            print(f"\tMatching for '{n}' not found in the results [MISS]! FN += {fn}")
            page_FN += fn

        for n in res_nodes:
            fp = len(set(node2item[n]))
            print(f"\tMatching for '{n}' not found in the references [FALSE-ALARM]! FP += {fp}")
            page_FP += fp
     
    print_line(n=30, prefix="\t")

    page_P, page_R, page_F1 = _calc_scores(page_TP, page_FN, page_FP)

    print(f"[item-stats] TP:{page_TP} FP:{page_FP} FN:{page_FN} PRECISION={page_P:.4f} RECALL={page_R:.4f} F1={page_F1:.4f}")
    
    TP += page_TP
    FN += page_FN
    FP += page_FP

    return TP, FN, FP


def eval_data(gt_files, res_files, include_missed_tables):

    TP, FP, FN = 0, 0, 0

    print_line(c='=', n=100)
    
    for key, gt_items in gt_files.items():
        if key in res_files:
            res_items = res_files[key]
            print(f"'{key}' found in both references and results.")
            #print_line()
            TP, FN, FP = _eval_pairs_on_page(res_items, gt_items, TP, FN, FP)
            del res_files[key]
        else:
            fn = 0
            for item in gt_items:
                n = len(set(item))
                fn += n

            if include_missed_tables:
                print(f"'{key}' not found in the results [MISS]! FN += {fn}")
                FN += fn
            else:
                print(f"'{key}' not found in the results [MISS]!")

        print_line(c='=')

    # count remaining FP's
    for key, res_items in res_files.items():
        fp = 0
        for item in res_items:
            n = len(set(item))
            fp += n

        print(f"'{key}' not found in the reference [FALSE-ALARM]! FP += {fp}")
        FP += fp

    precision, recall, F1 = _calc_scores(TP, FN, FP)

    #print_line(n=100, c='=')
    print(f"TP:{TP} FP:{FP} FN:{FN} PRECISION={precision:.4f} RECALL={recall:.4f} F1={F1:.4f}")


if __name__ == "__main__":

    verbose = False
    gt_dir = "gt"
    res_dir = "res"
    include_missed_tables = False
    
    gt_files = load_json_files(gt_dir)
    print_line(n=100)
    res_files = load_json_files(res_dir)

    if verbose:
        print("GT-DATA:")
        print_dict(gt_files)
        print("RES-DATA:")
        print_dict(res_files)

    gt_tuples = count_tuples(gt_files, verbose)
    res_tuples = count_tuples(res_files, verbose)
    
    print(f"GT tuples:  {gt_tuples}")
    print(f"RES tuples: {res_tuples}")
    
    eval_data(gt_files, res_files, include_missed_tables)

