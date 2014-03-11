
def report_minimization(mdp, solve_result):
    policy = solve_result['policy']
    value = solve_result['value']
    warnings.warn('fixing policy')
    for g in mdp.get_goal():
        policy[g] = _uniform_dist(mdp.actions(g))
    tension = get_tension_matrix(mdp, policy, value)

    pos = {}
    for s in mdp.states():
        pos[s] = np.array(s)


    spring_0 = {}
    spring_1 = {}
    Tmax = np.abs(np.array(tension.values())).max()
    for (s1, s2), T in tension.items():
        if s1 == s2:
            print('same state tension: %s' % (s1, s2))
            continue
        Tn = np.abs(T) / Tmax
        # natural distance
        d0 = np.linalg.norm(np.array(s1) - np.array(s2))
        spring_1[(s1, s2)] = Tn
        warnings.warn('temp policy')
        spring_0[(s1, s2)] = d0

    r = Report()

    f = f1
    f_gradient = f1_gradient

    f = f2
    f_gradient = f2_gradient

    plot_result(r, 'start', pos, spring_0)


    jsteps = 20
    alpha_steps = list(np.linspace(0.0, 1.0, jsteps))
    print alpha_steps
    for j, alpha in enumerate(alpha_steps):
        print j, alpha

        spring = average_spring(spring_0, spring_1, alpha)
        pos = gradient_descent(pos=pos, spring=spring,
                               f=f, f_gradient=f_gradient, max_iterations=400,
                               mean_dist_threshold=0.01, alpha=0.1)

        print('plot %s.. ' % str((j, alpha)))
        plot_result(r, j, pos, spring_1)
        print('...done')

    return r

def gradient_descent(pos, spring, f, f_gradient, max_iterations, mean_dist_threshold, alpha):
    # threshold:
    for i in range(1, max_iterations):
        obj = f(spring, pos)
#         print('iteration %3d: value: %10.4f' % (i, obj))
        g1 = f_gradient(spring, pos)
        pos1 = {}
        for s in pos:
            pos1[s] = pos[s] - alpha * g1[s]

        sum_dist = 0
        for s in pos:
            sum_dist += np.abs(pos1[s] - pos[s])
        mean_dist = np.mean(sum_dist)

        print('iteration %3d: value: %10.4f mean_change: %10.5f' % (i, obj, mean_dist))
        pos = pos1

        if mean_dist < mean_dist_threshold:
            break
    return pos

def average_spring(spring0, spring1, alpha):
    res = {}
    for s in spring0:
        res[s] = spring0[s] * (1 - alpha) + alpha * spring1[s]
    return res
# L2
def f2(spring, pos):
    res = 0.0
    for (s1, s2), T in spring.items():
        res += (np.linalg.norm(pos[s1] - pos[s2]) - T) ** 2
    return res

def f2_gradient(spring, pos):
    res = {}
    for s in pos:
        res[s] = f2_gradient_s(spring, pos, s)

    return res

def f2_gradient_s(spring, pos, s):
    """ Gradient with respect to s """
    res = np.array([0.0, 0.0])
    for (s1, s2), T in spring.items():
        if s1 != s:
            continue
        p1 = pos[s1]
        p2 = pos[s2]
        grad = (np.linalg.norm(p1 - p2) - T) * (p1 - p2)
        res += grad
    return res

# L1
def f1(spring, pos):
    res = 0.0
    for (s1, s2), T in spring.items():
        res += np.abs(np.linalg.norm(pos[s1] - pos[s2]) - T)
    return res

def f1_gradient(spring, pos):
    res = {}
    for s in pos:
        res[s] = f1_gradient_s(spring, pos, s)

    return res

def f1_gradient_s(spring, pos, s):
    """ Gradient with respect to s """
    res = np.array([0.0, 0.0])
    for (s1, s2), T in spring.items():
        if s1 != s:
            continue
        p1 = pos[s1]
        p2 = pos[s2]
        grad = np.abs(np.linalg.norm(p1 - p2) - T) * (p1 - p2)
        res += grad
    return res

def plot_result(r, i, pos, tension):
    values = np.abs(np.array(tension.values()))
    f = r.figure('it%s' % i)
    with f.plot('pos') as pylab:
        for s, y in pos.items():
            pylab.plot(y[0], y[1], '.')
        for (s1, s2), T in tension.items():
            Tn = np.abs(T) / values.max()
            y1 = pos[s1]
            y2 = pos[s2]
            pylab.plot((y1[0], y2[0]), [y1[1], y2[1]], '-',
                       color=[1 - Tn, 1 - Tn, 1 - Tn])
