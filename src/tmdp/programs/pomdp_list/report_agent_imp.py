from reprep import Report


def report_agent(res, pomdp):
    agent = res['agent']


    r = Report()

    with r.subsection('states') as sub:
        agent.report_states(sub)

    return r
