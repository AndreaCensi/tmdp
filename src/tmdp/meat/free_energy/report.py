from reprep import Report
import numpy as np


def report_free_energy(mdp, fe_res):
    iterations = fe_res['iterations']
    last = iterations[-1]

    r = Report()
    r.text('params', str(fe_res['params']))

    policy = last['pi']
    from tmdp.programs.value_iteration import report_maze_policy

    report_maze_policy(r, mdp, policy)

    f = r.figure()
    with f.plot('z') as pylab:
        Z = last['Z']
        Zs = np.array(sorted(Z.values()))
        Zs = Zs / np.max(Zs)
        print('normlized: %s' % Zs)

        mdp.display_state_values(pylab, Z)
    return r
