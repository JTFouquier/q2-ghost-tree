# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin.model as model

###############################################################################
#
# OtuMap
#
#     Groups of OTUs clustered by a similarity threshold. Each line contains
#     tab separated OTUs that are within the similarity threshold.
#
###############################################################################

class OtuMapFormat(model.TextFileFormat):

    def sniff(self):
        return True #  (TODO)
        with self.open() as fh:
            print('lalala')
            for line, _ in zip(fh, range(5)):
                print('line')
                try:
                    print('TESTING INSIDE OTU MAP SNIFFER')
                    int(line.rstrip('\n'))
                except (TypeError, ValueError):
                    return False
            return True

OtuMapDirectoryFormat = model.SingleFileDirectoryFormat(
    'OtuMapDirectoryFormat', 'otus.txt', OtuMapFormat)
