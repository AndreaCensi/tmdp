from quickapp import iterate_context_names
from tmdp.programs.pomdp_list.alternate_observations import alternate_observersations_an
from tmdp.programs.pomdp_list.main import get_alternative_pomdp
from tmdp.programs.pomdp_list.meat import pomdp_list_states, find_minimal_policy


def cdtest_alt_obsmodel(context, t):
    """ In this test we look for alternative observations models. """
    # id_pomdp  = t['id_pomdp']
    pomdp = t['pomdp']

    results = []

    cc = context.child('original')
    res = cc.comp(pomdp_list_states, pomdp)
    res = cc.comp(find_minimal_policy, res, pomdp)
    results.append(('original', res))

    # normal agent
    horizons = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
#     horizons = [3, 2, 1, 0]
    for cc, horizon in iterate_context_names(context, horizons):
        pomdp2 = cc.comp(get_alternative_pomdp, pomdp, horizon)
        res2 = cc.comp(alternate_observersations_an, res, pomdp, pomdp2)
        desc = 'horizon = %d ' % horizon
        results.append((desc, res2))

    context.comp(cdtest_alt_obsmodel_check, results)


def cdtest_alt_obsmodel_check(results):
    nstates_all = []
    for desc, result in results:
        agent = result['agent']
        nstates = len(agent.get_all_states())
        nbits = agent.get_num_states_components()
        nstates_all.append(nstates)
        print('%10s: nstates = %4d nbits = %3d' % (desc, nstates, nbits))

    print('nstates:         %s' % nstates_all)
    print('sorted(nstates): %s' % nstates_all)
    if not sorted(nstates_all) == nstates_all:
        print('Something is wrong.')
        raise ValueError((nstates_all))
