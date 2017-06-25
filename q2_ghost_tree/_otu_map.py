# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import re

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
        with self.open() as fh:

            for line, _ in zip(fh, range(5)):

                # (NOTE) unsure how to validate an OTU file!

                # check that it's a string
                try:
                    if type(line) == str:
                        pass
                    else:
                        return False
                except:
                    return False

                # shouldn't contain special chars
                try:
                    if not re.search(';', line):
                        pass
                except:
                    pass

            return True

OtuMapDirectoryFormat = model.SingleFileDirectoryFormat(
    'OtuMapDirectoryFormat', 'otus.txt', OtuMapFormat)
