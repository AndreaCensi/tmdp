from conf_tools import GlobalConfig
import numpy as np
from quickapp import QuickMultiCmdApp


__all__ = ['TMDP']


class TMDP(QuickMultiCmdApp):
    """ Main TMDP program """

    cmd = 'tmdp'

    def define_multicmd_options(self, params):
        pass

    def get_config_dirs(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        config_dir = resource_filename("tmdp", "configs")
        return [config_dir]

    def initial_setup(self):
        config_dirs = self.get_config_dirs()
        GlobalConfig.global_load_dirs(config_dirs)


        np.seterr(all='raise')
