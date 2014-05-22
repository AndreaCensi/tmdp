from numpy.ma.testutils import assert_equal

from tmdp.programs.pomdp_list.meat import pomdp_list_states, find_minimal_policy


def cdtest_basic(context, t):
    pomdp = t['pomdp']
    res = context.comp(pomdp_list_states, pomdp)
    res = context.comp(find_minimal_policy, res, pomdp)
    context.comp(cdtest_basic_check, t, res)

def cdtest_basic_check(t, res):
    # id_pomdp = t['id_pomdp']
    expected_nbits = t['expected_nbits']
    expected_nstates = t['expected_nstates']
    expected_ntrajectories = t['expected_ntrajectories']

    ntrajs = len(res['trajectories'])
    print('ntrajs:  %s  (exp: %s)' % (ntrajs, expected_ntrajectories))


    for j, traj in enumerate(res['trajectories']):
        for k, t in enumerate(traj):
            u = t['action']
            y = t['obs']
            print('traj %d | k = %d | obs_k = %20s ->  cmd_k = %6s ' % (j, k, y, u))
        print()

    assert_equal(ntrajs, expected_ntrajectories)

    agent = res['agent']

    nstates = len(agent.get_all_states())
    nbits = agent.get_num_states_components()
     
    print('nstates: %s  (exp: %s)' % (nstates, expected_nstates))
    print('nbits:   %s  (exp: %s)' % (nbits, expected_nbits))
    
    assert_equal(nstates, expected_nstates)
    assert_equal(nbits, expected_nbits)
