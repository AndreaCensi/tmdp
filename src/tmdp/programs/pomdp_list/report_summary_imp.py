from reprep import Report



def report_summary(results):
    # results = tuple (name, res dict)
    r = Report()

    cols = ['scenario', 'number of bits', 'number of states']
    data = []
    for name, res in results:
        
        agent = res['agent']
        
        nstates = len(agent.get_all_states())
        nbits = agent.get_num_states_components()
        row = [name, nbits, nstates]
        data.append(row)

    r.table('summary', data=data, cols=cols)
        

    cols = [ 'number of bits', 'number of states']
    data = []
    rows = []
    for name, res in results:

        agent = res['agent']

        nstates = len(agent.get_all_states())
        nbits = agent.get_num_states_components()
        rows.append(name)
        data.append([nbits, nstates])

    r.table('summary2', data=data, cols=cols, rows=rows)


    return r
