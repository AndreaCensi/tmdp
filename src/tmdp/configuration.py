
from conf_tools import ConfigMaster


__all__ = [
   'get_tmdp_config',
   'get_conftools_tmdp_smdps',
]


class TMDPConfig(ConfigMaster):

    def __init__(self):
        ConfigMaster.__init__(self, 'tmdp')
        from .mdp import SimpleMDP
        self.smdps = \
            self.add_class_generic('smdps', '*.tmdp_smdps.yaml',
                                   SimpleMDP)

    def get_default_dir(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        return resource_filename("tmdp", "configs")


get_tmdp_config = TMDPConfig.get_singleton


def get_conftools_tmdp_smdps():
    return get_tmdp_config().smdps
