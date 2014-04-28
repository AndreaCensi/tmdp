from matplotlib.colors import colorConverter

import networkx as nx
from reprep import Report
from tmdp.mdp_utils import all_actions

__all__ = [
           'report_sampled_mdp',
]

def report_sampled_mdp(res, pomdp):
    mdp_absorbing = res['mdp_absorbing']
    nonneg = res['nonneg']
    policy = res['policy']
    G = nx_graph_from_mdp(mdp_absorbing, skip_self=True, only_states=None)
    Gmin = nx_graph_from_mdp(mdp_absorbing, skip_self=True, only_states=nonneg,
                             only_policy=policy)



    print('layout...')

    def layout(G0):
        pos0 = nx.spectral_layout(G)
#         pos = nx.fruchterman_reingold_layout(G, pos=pos0)
        return pos0
#         return pos0

    import numpy as np
    def my_layout(G0):


        def pos_belief(b):
            robot = list(b.keys())[0][0]
            return np.array(robot)

        belief2pos = {}
        occupied = set()
        def place_belief(b, guess):
            if b in belief2pos:
                return belief2pos[b]

            for x in [  # [1, 0], [-1, 0], [0, 1], [0, -1],
                      [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                alpha = 0.5
                p = np.array(guess) * 1.0 + np.array([1.0, 1.0]) * x * alpha
                if not tuple(p) in occupied:
                    occupied.add(tuple(p))
                    belief2pos[b] = np.array(p)
                    return belief2pos[b]

            raise ValueError()

        res = {}
        for n in G0:
            if G.node[n]['type'] == 'belief':
                belief = n

                res[n] = place_belief(n, pos_belief(belief))

            elif G.node[n]['type'] == 'action':
                belief1 = G.node[n]['from_belief']
                belief2 = G.node[n]['to_belief']

                res[n] = place_belief(n, 0.5 * pos_belief(belief1) +
                                        + 0.5 * pos_belief(belief2))

        print belief2pos

        return res

    pos = layout(G)
    r = Report()
    f = r.figure(cols=2)
    print('plotting G')
    with f.plot('G', figsize=(5, 5)) as pylab:
        nx_draw_with_attrs(G, pos=pos)


    add_aliasing_edges(Gmin, nonneg, mdp_absorbing, pomdp)

    pos_spectral = my_layout(Gmin)
    pos_neato = nx.graphviz_layout(Gmin, prog="neato")
    pos_dot = nx.graphviz_layout(Gmin, prog="dot")


    size2 = (3, 3)
    print('plotting Gmin')
    with f.plot('Gmin', figsize=size2) as pylab:
        nx_draw_with_attrs(Gmin, pos=pos, with_labels=False)

    print('plotting Gmin again with better coords')


    with f.plot('Gmin2', figsize=size2) as pylab:
        nx_draw_with_attrs(Gmin, pos=pos_spectral, with_labels=False)

    print('plotting Gmin again with better coords')

    with f.plot('Gmin3', figsize=size2) as pylab:
        nx_draw_with_attrs(Gmin, pos=pos_neato, with_labels=False)

    with f.plot('Gmin_dot', figsize=size2) as pylab:
        nx_draw_with_attrs(Gmin, pos=pos_dot, with_labels=False)

    return r

def nx_draw_with_attrs(G, pos, with_labels=False):
    """ Draws G using 'node_color', 'node_size' attributes. """

#     edge_styles = [G[a][b]['edge_style'] for a, b in G.edges()]
#
#
#     for style in set(edge_styles):
#         edgelist = [(a, b) for (a, b) in G.edges() if G[a][b]['edge_style'] == style]
#         nx.draw_networkx_edges(G, pos=pos,
#                                style=style,
#                                arrows=True,
#                                edgelist=edgelist
#                                )
#
    edge_colors = [G[a][b]['edge_color'] for a, b in G.edges()]
    nx.draw(G,
            pos=pos,
            node_color=[G.node[v]['node_color'] for v in G],
            node_size=[G.node[v]['node_size'] for v in G],
            arrows=True,
            edge_color=edge_colors,
            with_labels=with_labels)
#


# def report_list(res):
#     builder = res['builder']
#     G = builder.get_graph()
#     r = Report()
#     f = r.figure()
#     print('layout...')
#     pos = nx.graphviz_layout(G, prog="neato", root=0)
#     print('done')
#     with f.plot('nx', figsize=(10, 10)) as pylab:
#
#         def node_color(v):
#             t = G.node[v]['type']
#             if v in builder.goals:
#                 return [0, 1.0, 0]
#             else:
#
#                 if t == 'action':
#                     return [1.0 , 0, 0]
#                 else:
#                     return [0.5, 0.5, 0.5]
#
#         def node_size(v):
#             t = G.node[v]['type']
#             if t == 'action':
#                 return 10
#             if t == 'belief':
#                 return 20
#             raise ValueError()
#
#         def node_shape(v):  #  so^>v<dph8
#             t = G.node[v]['type']
#             if t == 'action':
#                 return 's'
#             if t == 'belief':
#                 return 'o'
#             raise ValueError()
#
#         print('draw')
#         nx.draw(G,
#                 with_labels=False,
#                 pos=pos,
#                 node_color=[node_color(v) for v in G],
#                 node_size=[node_size(v) for v in G],
# #                 node_shape=[node_shape(v) for v in G],
# #                 with_labels=False,
#                 alpha=0.5)
#         print('done')
#     return r



def nx_graph_from_mdp(mdp, skip_self=True, only_states=None, only_policy=None,
                      original_pomdp=None):
    """ 
        Creates an NX graph.
    
        There are nodes for both states and actions. 
        
        if only_states is not None, only those states are considered.
        
        if only_policy is not None, only the actions that are nonzero given
        the policy are considered.
    """

    G = nx.Graph()

    edge_color_action = colorConverter.to_rgb('#000000')
    edge_color_result = colorConverter.to_rgb('#a0a0a0')
    actions = all_actions(mdp)
    colors = [ '#9E0B0F', '#662D91', '#007236', '#0076A3',
              '#F26522', '#FFF200', '#00AEEF', '#C4DF9B']
    colors = map(colorConverter.to_rgb, colors)
    if len(colors) < len(actions):
        print('warning: not enough colors for actions')
    action2color = {}
    for i, a in enumerate(actions):
        action2color[a] = colors[i % len(colors)]

    def color_of(s):
        if s in mdp.get_start_dist():
            return [0, 0, 1]
        if mdp.is_goal(s):
            return [0, 1, 0]
        else:
            return [0.5, 0.5, 0.5]

    if only_states is not None:
        states = only_states
    else:
        states = list(mdp.states())
    for s in states:
        for a in mdp.actions(s):

            if only_policy is not None:
                p = only_policy[s].get(a, 0)
                if p == 0:
                    continue


            action_node = '%s-%s' % (s, a)

            G.add_node(s)
            G.node[s]['type'] = 'belief'
            G.node[s]['node_size'] = 20


            G.node[s]['node_color'] = color_of(s)

            at_least_one = False
            for s2, _ in mdp.transition(s, a).items():

                if skip_self:
                    if s == s2:
                        continue

                at_least_one = True
                G.add_edge(action_node, s2)  # probability

                G.edge[action_node][s2]['edge_color'] = edge_color_result
                G.edge[action_node][s2]['type'] = 'result'
                G.edge[action_node][s2]['edge_style'] = 'dashed'

                G.node[s2]['type'] = 'belief'
                G.node[s2]['node_size'] = 20
                G.node[s2]['node_color'] = color_of(s2)

            if at_least_one:
                G.add_edge(s, action_node)

                G.edge[s][action_node]['edge_color'] = edge_color_action
                G.edge[s][action_node]['type'] = 'action'
                G.edge[s][action_node]['edge_style'] = 'solid'

                G.node[action_node]['type'] = 'action'
                G.node[action_node]['from_belief'] = s
                G.node[action_node]['to_belief'] = s2

                G.node[action_node]['node_size'] = 10

                G.node[action_node]['node_color'] = action2color[a]
    return G


def add_aliasing_edges(G, only_states, belief_mdp, pomdp):
    for s1 in only_states:
        for s2 in only_states:
            if s1 == s2:
                continue

            obs1 = pomdp.get_observations_dist_given_belief(s1)
            obs2 = pomdp.get_observations_dist_given_belief(s2)

            can_distinguish = len(set(obs1) & set(obs2)) == 0

#             if not len(obs1) == 0 or not len(obs2) == 0:
#                 print('not deterministic, %s , %s , %s , %s ' % (s1, obs1, s2, obs2))
#                 continue

            if not can_distinguish:
                # aliasing!
                G.add_edge(s1, s2)
                G.edge[s1][s2]['type'] = 'aliasing'
                G.edge[s1][s2]['edge_color'] = colorConverter.to_rgb('y')
                G.edge[s1][s2]['edge_style'] = 'dotted'



    return G
