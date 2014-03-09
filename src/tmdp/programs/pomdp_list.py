from collections import defaultdict

from contracts import contract

import networkx as nx
from quickapp import CompmakeContext, QuickApp, iterate_context_names
from reprep import Report
from tmdp import get_conftools_tmdp_smdps
from tmdp.mdp_utils.mdps_utils import all_actions, mdp_stationary_dist
from tmdp.meat.value_it.vit_solver import VITMDPSolver
from tmdp.programs.show import instance_mdp
from tmdp.sampled_mdp import SampledMDP

from .main import TMDP
from matplotlib.colors import ColorConverter, colorConverter


__all__ = ['POMDPList']

class POMDPList(TMDP.get_sub(), QuickApp):
    """ Lists all reachable states of the POMDP. """

    cmd = 'pomdp-list'

    def define_options(self, params):
        params.add_string_list('mdps', help='POMDPS')

    @contract(context=CompmakeContext)
    def define_jobs_context(self, context):
        options = self.get_options()

        config_mdps = get_conftools_tmdp_smdps()
        id_mdps = config_mdps.expand_names(options.mdps)

        for cc, id_mdp in iterate_context_names(context, id_mdps):
            cc.add_extra_report_keys(id_mdp=id_mdp)
            pomdp = cc.comp_config(instance_mdp, id_mdp)

            res = cc.comp(pomdp_list_states, pomdp)
            res = cc.comp(find_minimal_policy, res)

            cc.add_report(cc.comp(report_sampled_mdp, res, pomdp), 'sampled_mdp')

class MDPBuilder():
    
    @contract(start_dist='ddist')
    def __init__(self, start_dist):
        
        self._state2id = {}
        self._id2state = {}
        self._transitions = []
        self.goals = set()
        
        self._start_dist = {}
        for state, p_state in start_dist.items():
            self._start_dist[self._get_id(state)] = float(p_state)
    
    def _get_id(self, state):
        if state in self._state2id:
            return self._state2id[state]
#         print('not creating different IDs')
        l = len(self._state2id)
        l = state
        self._state2id[state] = l
        self._id2state[l] = state
        return l

    def mark_goal(self, state):
        self.goals.add(self._get_id(state))
        
    def add_state(self, state):
        pass

    def add_transition(self, state, action, state2, probability, reward):
        s1 = self._get_id(state)
        s2 = self._get_id(state2)
        t = (s1, action, s2, probability, reward)
        self._transitions.append(t)
#
#     def get_graph(self):
#         G = nx.Graph()
#
#         for (s1, action, s2, p, reward) in self._transitions:
#             if s1 == s2:
#                 continue
#             action_node = '%s-%s' % (s1, action)
#
#             G.add_edge(s1, action_node)
#
#             G.add_edge(action_node, s2)
#
#             G.node[action_node]['type'] = 'action'
#             G.node[s1]['type'] = 'belief'
#             G.node[s2]['type'] = 'belief'
#         return G


    def get_sampled_mdp(self, goal_absorbing=True, stay=None):
        """ 
            If goal_absorbing = True, all actions of the goal states
            give the same state. 
        """

        state2actions = defaultdict(lambda: set())
        state2action2transition = defaultdict(lambda: defaultdict(lambda:{}))
        state2action2state2reward = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:{})))

        # create states self.states = set()
        states = set()
        for s1 in self._id2state:
            states.add(s1)

        actions = set()
        for (s1, action, s2, p, reward) in self._transitions:
            actions.add(action)
            state2actions[s1].add(action)
            state2action2transition[s1][action][s2] = float(p)  # += p
            state2action2state2reward[s1][action][s2] = reward  # += p
        
        if goal_absorbing:
            for g in self.goals:
                for a in actions:
                    state2actions[g].add(a)
                    state2action2transition[g][a][g] = 1.0
                    state2action2state2reward[g][a][g] = 0.0
        else:
            # for each goal state, we reset to the start distribution
            assert isinstance(stay, float)
            for g in self.goals:
                for a in actions:
                    state2actions[g].add(a)

                    state2action2transition[g][a] = {}
                    state2action2transition[g][a][g] = stay
                    state2action2state2reward[g][a][g] = 0.0
                    for s0 in self._start_dist:
                        state2action2transition[g][a][s0] = self._start_dist[s0] * (1.0 - stay)
                        state2action2state2reward[g][a][s0] = 0.0


        mdp = SampledMDP(states=states,
                         state2actions=state2actions,
                         state2action2transition=state2action2transition,
                         state2action2state2reward=state2action2state2reward,
                         start_dist=self._start_dist,
                         goals=self.goals)
        return mdp
    
    
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
            return [0,0,1]
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

    
def find_minimal_policy(res):
    builder = res['builder']
    mdp_absorbing = builder.get_sampled_mdp(goal_absorbing=True)
    solver = VITMDPSolver(least_committed=False)
    res = solver.solve(mdp_absorbing)
    policy = res['policy']

    mdp_non_absorbing = builder.get_sampled_mdp(goal_absorbing=False, stay=0.1)

    dist0 = mdp_stationary_dist(mdp_non_absorbing, mdp_non_absorbing.get_start_dist(), policy,
                                l1_threshold=1e-8)

    nonneg = [s  for s in dist0 if dist0[s] >= 1e-4]

    res['mdp_non_absorbing'] = mdp_non_absorbing
    res['mdp_absorbing'] = mdp_absorbing
    res['nonneg'] = nonneg
    res['policy'] = policy

    return res

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

    
def pomdp_list_states(pomdp, use_fraction=True):
    res = {}

    start_dist = pomdp.get_start_dist_dist()
    print('start: %s' % start_dist)

    builder = MDPBuilder(start_dist=start_dist)
    res['builder'] = builder


    nodes_open = list()
    nodes_closed = set()
    nodes_goal = set()

    for belief0, _ in start_dist.items():
        nodes_open.append(belief0)

    actions = all_actions(pomdp)
    while nodes_open:
        if len(nodes_closed) % 100 == 0:
            print('nopen: %5d nclosed: %5d ngoal: %5d' % (len(nodes_open), len(nodes_closed), len(nodes_goal)))
        belief = nodes_open.pop()

        # print('-- popping %s' % belief)
        # assert not belief in nodes_closed
        
        builder.add_state(belief)

        nodes_closed.add(belief)
        
        if pomdp.is_goal_belief(belief):
            nodes_goal.add(belief)
            builder.mark_goal(belief)

#             for action in actions:
#                 for belief0, p0 in start_dist.items():
#                     builder.add_transition(belief, action, belief0, p0, 0)

            # any action at the goal states makes it go randomly to the initial states
#             for action in actions:
#                 for belief0, p0 in start_dist.items():
#                     builder.add_transition(belief, action, belief0, p0, 0)

            # print('goal: %s' % belief)
        else:
            # for each action, evolve belief
            for action in actions:
                belief1 = pomdp.evolve(belief, action, use_fraction=use_fraction)
                for _, p_x in belief1.items():
                    assert p_x > 0

                # print('-- %s -> %s' % (action, belief1))
                # now sample observations
                for y, p_y in pomdp.get_observations_dist_given_belief(belief1, use_fraction=use_fraction).items():
                    assert p_y > 0
                        # Now, see what would be the belief for each possible observation
                    # p(y | x) * p(x) / p(y)
                    # Likelihood

                    # print('y = %s is generated with prob %s ' % (y, p_y))
                    belief2 = pomdp.inference(belief=belief1, observations=y, use_fraction=use_fraction)

                    builder.add_transition(belief, action, belief2, p_y, -1)

                    if belief2 in nodes_closed or belief2 in nodes_open:
                        pass
                    else:
                        nodes_open.append(belief2)

#             if np.random.rand() < 0.01:
#                 print('last opened: %s' % belief)

    return res
