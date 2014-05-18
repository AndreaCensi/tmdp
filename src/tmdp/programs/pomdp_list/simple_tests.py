from tmdp.programs.show import instance_mdp
from tmdp.programs.pomdp_list.meat import pomdp_list_states, find_minimal_policy
from conf_tools.global_config import GlobalConfig
from numpy.ma.testutils import assert_equal





def simple_tests():
    from pkg_resources import resource_filename  # @UnresolvedImport
    dirs = [
        resource_filename("tmdp", "configs"),
        resource_filename("gridworld", "configs"),
    ]
    GlobalConfig.global_load_dirs(dirs)

    tests = [
            dict(id_pomdp='idec-test01',
                 expected_ntrajectories=2,
                 expected_nbits=0,
                 expected_nstates=1),
            dict(id_pomdp='idec-test02',
                 expected_ntrajectories=2,
                 expected_nbits=0,
                 expected_nstates=1),
            dict(id_pomdp='idec-test03',
                 expected_ntrajectories=4,
                 expected_nbits=1,
                 expected_nstates=2),
            dict(id_pomdp='idec-test04',
                 expected_ntrajectories=3,
                 expected_nbits=0,
                 expected_nstates=1),
             ]
    
    for t in tests:
        check_scenario(**t)
        
        
def check_scenario(id_pomdp, expected_nbits, expected_nstates,
                   expected_ntrajectories):
    pomdp = instance_mdp(id_pomdp)
    res = pomdp_list_states(pomdp)
    res = find_minimal_policy(res, pomdp)

#     print('policy: %s' % res['policy'])

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
