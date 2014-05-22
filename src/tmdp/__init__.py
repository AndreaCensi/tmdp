from .configuration import *
from .mdp import *
from quickapp.quick_app import QuickApp



def get_comptests():
    from comptests import get_comptests_app
    apps = []
#     apps.append(get_comptests_app(get_tmdp_config()))

#     apps.append(get_comptests_app_dynamic(pomdp_tests))
    apps.append(ComptestApp)
    return apps


class ComptestApp(QuickApp):
    cmd = 'tmdp-tests'

    def define_options(self, params):
        pass

    def define_jobs_context(self, context):
        from tmdp.programs.pomdp_list.unittest.scenarios import pomdp_tests
        pomdp_tests(context)

#
# def get_comptests_app_dynamic(dynamic):
# #     ComptestApp.__name__ = 'ComptestApp%s' % cm.name
#     return ComptestApp
