import networkx as nx


def jaccard_wt(graph, node):
  """
  The weighted jaccard score, defined above.
  Args:
  graph....a networkx graph
  node.....a node to score potential new edges for.
  Returns:
  A list of ((node, ni), score) tuples, representing the
          score assigned to edge (node, ni)
          (note the edge order)
  """
  A = set(graph.neighbors(node))
  deg_a = graph.degree(A)
  tot_a = sum(deg_a.values())
  scores = []
  for n in graph.nodes():
    if n not in A and n != node:
        B = set(graph.neighbors(n))
        deg_B = graph.degree(B)
        tot_b = sum(deg_B.values())
        inter = A & B
        deg_int = graph.degree(inter)
        tot_d_i = 0
        for i in deg_int:
            tot_d_i += 1/deg_int[i]
        jac = tot_d_i / ((1/tot_a) + (1/tot_b))
        scores.append(((node,n), jac))
  return sorted(scores, key=lambda x: x[1], reverse=True)
