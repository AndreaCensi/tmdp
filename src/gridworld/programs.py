#
# import os
#
# from gridworld.grids_examples import TishbyMaze
# from quickapp import QuickAppBase
# from reprep import Report
#
#
# __all__ = [
#     'gridworld_test_display',
# ]
#
# class TestDisplay(QuickAppBase):
#
#     def define_program_options(self, params):
#         pass
#
#     def go(self):
#
#         m = TishbyMaze()
#         p = {(1, 1): 1.0}
#         actions = ['u'] * 10
#
#         r = Report()
#         f = r.figure()
#         for i, a in enumerate(actions):
#             with f.plot('p%d' % i) as pylab:
#                 m.display_state_dist(pylab, p)
#             p = m.evolve(p, a)
#
#
#         od = 'out-gridworld_test_display'
#         if not os.path.exists(od):
#             os.makedirs(od)
#
#         r.to_html(os.path.join(od, 'p.html'))
#
#
# gridworld_test_display = TestDisplay.get_sys_main()
#
#
