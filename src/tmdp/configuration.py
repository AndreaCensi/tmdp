
from conf_tools import ConfigMaster


__all__ = [
   'get_tmdp_config',
   'get_conftools_tmdp_smdps',
   'get_conftools_tmdp_smdp_solvers',
]


class TMDPConfig(ConfigMaster):

    def __init__(self):
        ConfigMaster.__init__(self, 'tmdp')
        from .mdp import SimpleMDP
        from .solver import SimpleMDPSolver

        self.smdps = \
            self.add_class_generic('smdps', '*.tmdp_smdps.yaml',
                                   SimpleMDP)
        self.smdp_solvers = \
            self.add_class_generic('smdp_solvers', '*.tmdp_smdp_solvers.yaml',
                                   SimpleMDPSolver)

        from gridmaps.map import GridMap
        self.gridmaps = self.add_class_generic('gridmaps', '*.tmdp_gridmaps.yaml',
                                               GridMap)

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("tmdp", "configs")


get_tmdp_config = TMDPConfig.get_singleton

def get_conftools_tmdp_gridmaps():
    return get_tmdp_config().gridmaps

def get_conftools_tmdp_smdps():
    return get_tmdp_config().smdps

def get_conftools_tmdp_smdp_solvers():
    return get_tmdp_config().smdp_solvers
