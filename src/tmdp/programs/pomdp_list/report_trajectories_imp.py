from latex_gen.environment import MIME_PNG
from reprep import Report
from tmdp.programs.pomdp_list.agent import Namer
from collections import defaultdict


def report_trajectories(res, name_obs=False):
    r = Report()

    f = r.figure()

    import networkx as nx

    G0 = create_graph_trajectories0(res['trajectories'], label_state=False,
                                    name_obs=name_obs)
    f.data('tree0', nx.to_pydot(G0).create_png(), mime=MIME_PNG)

    G0 = create_graph_trajectories0(res['trajectories'], label_state=True,
                                    name_obs=name_obs)
    f.data('tree1', nx.to_pydot(G0).create_png(), mime=MIME_PNG)

#
#     G1 = create_graph_trajectories(res['decisions'])
#     d1 = nx.to_pydot(G1)  # d is a pydot graph object, dot options can be easily set
#     # r.data('tree1', d.create_pdf(), mime=MIME_PDF)
#     f.data('tree1', d1.create_png(), mime=MIME_PNG)
#
#
#
#     if 'decisions_dis' in res:
#         G2 = create_graph_trajectories(res['decisions_dis'])
#         d2 = nx.to_pydot(G2)  # d is a pydot graph object, dot options can be easily set
#         f.data('tree2', d2.create_png(), mime=MIME_PNG)

    return r

def create_graph_trajectories0(trajectories, label_state=False, name_obs=False):
    assert len(trajectories) >= 1
    import networkx as nx
    G = nx.DiGraph()
    namer = Namer('T%d')

    if name_obs:
        obs_namer = Namer('y%d')
    else:
        obs_namer = lambda x: x

    # Count the number of times we see the same observations

    obs2count = defaultdict(lambda: 0)

    def format_state(x):
        return ''.join(str(x[comp]) for comp in sorted(x.keys()))

    for traj in trajectories:
        for i, t in enumerate(traj):
            obs = t['obs']
            action = t['action']
            agent_state = t['agent_state']
            agent_state_next = t['agent_state_next']
            
            # nodes are indexed with sequence of observations
            history = tuple([x['obs'] for x in traj[:i + 1]])

            assert len(history) == i + 1

            prev = history[:-1]
            s1 = namer(prev)
            s2 = namer(history)

            if not G.has_edge(s1, s2):
                G.add_edge(s1, s2)
                obs2count[obs] += 1
                obs_label = obs_namer(obs)
                if obs2count[obs] > 1:
                    obs_label = '%s (%s)' % (obs_label, obs2count[obs])
                G.edge[s1][s2]['label'] = obs_label

                # let's label the node with a command
                if label_state:
                    label = format_state(agent_state_next)  # + '->' + format_state(agent_state_next)

                    if agent_state != agent_state_next:
                        G.node[s2]['color'] = '#FF0000'
                        G.edge[s1][s2]['color'] = '#FF0000'

                else:
                    label = action

                G.node[s2]['label'] = label

    if label_state:
        state0 = trajectories[0][0]['agent_state']
        label0 = format_state(state0)
    else:
        label0 = '-'
    G.node[namer(())]['label'] = label0
    return G
#
# def create_graph_trajectories(decisions):
# #     decisions = get_decisions(trajectories)
#     """
#         The decisions that we had to do in the trajectories.
#         This is a list of dictionaries.
#         Each dict has fields
#         "action":
#         "state": dict(last=y)
#         "history": list of ys
#     """
#     namer = Namer('T%d')
#
#     import networkx as nx
#     G = nx.DiGraph()
#     for d in set(decisions):
#         print d
#         y_prev = d['history']
#         y = d['state']['last']
#         y_history = y_prev + (y,)
#
#         s1 = namer(y_prev)
# #         if not s1 in G:
# #             G.add_node(s1, label=d['action'])
# #         if not s2 in G:
# #             G.add_node(s1, label=d['action'])
#
#         s2 = namer(y_history)
# #         print('prev: %s = %s' % (s1, y_prev))
# #         print('cur:  %s = %s' % (s2, y_history))
#
#         G.add_edge(s1, s2)
#         G.edge[s1][s2]['label'] = y
#
#         if 'agent_state' in d:
#             state = d['agent_state']
#             label = '%s, %s' % (state, d['action'])
#         else:
#             label = d['action']
#         G.node[s1]['label'] = label
#     return G


