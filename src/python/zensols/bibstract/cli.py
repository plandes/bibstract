"""Command line entrance point to the application.

"""
__author__ = 'plandes'


from zensols.actioncli import OneConfPerActionOptionsCliEnv
from zensols.bibstract import Extractor


class ExtractorCli(object):
    def __init__(self, master_bib: str):
        self.ex = Extractor(master_bib)

    def print_ids(self):
        self.ex.tmp()


class ConfAppCommandLine(OneConfPerActionOptionsCliEnv):
    def __init__(self):
        masterbib_op = ['-m', '--masterbib', True,
                        {'dest': 'master_bib',
                         'metavar': 'FILE',
                         'default': 'master.bib',
                         'help': 'the directory to masterbib the website'}]
        cnf = {'executors':
               [{'name': 'exporter',
                 'executor': lambda params: ExtractorCli(**params),
                 'actions': [{'name': 'print',
                              'meth': 'print_ids',
                              'doc': 'print BibTex citation keys',
                              'opts': [masterbib_op]}]}],
               'whine': 1}
        super(ConfAppCommandLine, self).__init__(
            cnf, config_env_name='bibstractrc', pkg_dist='zensols.bibstract')


def main():
    cl = ConfAppCommandLine()
    cl.invoke()
