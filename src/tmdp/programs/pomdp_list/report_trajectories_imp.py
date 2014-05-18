from reprep import Report
from tmdp.programs.pomdp_list.meat import get_decisions
from reprep.constants import MIME_PDF
from latex_gen.environment import MIME_PNG
from tmdp.programs.pomdp_list.agent import Namer


def report_trajectories(res):


    r = Report()

    import networkx as nx
#         # pos = nx.spectral_layout(G)
#         with f.plot('G', figsize=(5, 5)) as pylab:  # @UnusedVariable
#             # nx_draw_with_attrs(G, pos=pos, with_labels=True)
#             nx.draw(G)
    trajectories = res['trajectories']

    G1 = create_graph_trajectories(res['decisions'])
    d1 = nx.to_pydot(G1)  # d is a pydot graph object, dot options can be easily set

#     trajectories2 = res['trajectories2']
#     G2 = create_graph_trajectories(trajectories2)
#     d2 = nx.to_pydot(G2)  # d is a pydot graph object, dot options can be easily set

    # attributes get converted from networkx,
    # use set methods to control dot attributes after creation

    f = r.figure()

    # r.data('tree1', d.create_pdf(), mime=MIME_PDF)
#     f.data('tree1', d.create_png(), mime=MIME_PNG)
    f.data('tree1', d1.create_png(), mime=MIME_PNG)



    if 'decisions_dis' in res:
        G2 = create_graph_trajectories(res['decisions_dis'])
        d2 = nx.to_pydot(G2)  # d is a pydot graph object, dot options can be easily set
        f.data('tree2', d2.create_png(), mime=MIME_PNG)

    return r



def create_graph_trajectories(decisions):
#     decisions = get_decisions(trajectories)
    """
        The decisions that we had to do in the trajectories.
        This is a list of dictionaries.
        Each dict has fields
        "action":
        "state": dict(last=y) 
        "history": list of ys
    """
    namer = Namer('T%d')

    import networkx as nx
    G = nx.DiGraph()
    for d in decisions:
        y_prev = d['history']
        y = d['state']['last']
        y_history = y_prev + (y,)

        s1 = namer(y_prev)

#         if not s1 in G:
#             G.add_node(s1, label=d['action'])
#         if not s2 in G:
#             G.add_node(s1, label=d['action'])

        s2 = namer(y_history)
        G.add_edge(s1, s2)
        G.edge[s1][s2]['label'] = y

        if 'agent_state' in d:
            state = d['agent_state']
            label = '%s, %s' % (state, d['action'])
        else:
            label = d['action']
        G.node[s1]['label'] = label
    return G


