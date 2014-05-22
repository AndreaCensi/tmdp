from conf_tools import GlobalConfig
from quickapp import iterate_context_names_pair
from tmdp.programs.show import instance_mdp

from .complicated_tests import cdtest_alt_obsmodel
from .simple_tests import cdtest_basic


def pomdp_tests(context):
    schedule(context,
             generator=get_simple_scenarios,
             testing_functions=[cdtest_alt_obsmodel, cdtest_basic])

def schedule(context, generator, testing_functions):
    generated = context.comp_dynamic(generator)
    context.comp_dynamic(schedule_, generated, testing_functions)

def schedule_(context, generated, testing_functions):
    for c, f, g in iterate_context_names_pair(context, testing_functions, generated):
        c.comp_dynamic(f, g)


def get_simple_scenarios(context):
    pomdp_scenarios = [
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

    from pkg_resources import resource_filename  # @UnresolvedImport
    dirs = [
        resource_filename("tmdp", "configs"),
        resource_filename("gridworld", "configs"),
    ]
    GlobalConfig.global_load_dirs(dirs)
    ts = []
    for t in pomdp_scenarios:
        t['pomdp'] = context.comp_config(instance_mdp, t['id_pomdp'])
        ts.append(t)
    return ts
    
