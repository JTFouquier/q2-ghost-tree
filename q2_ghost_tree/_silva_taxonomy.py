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
# SilvaTaxonomy
#
#     Taxonomy File for Silva Database. Unique file to Silva database
#       containing taxonomy information
#
###############################################################################

class SilvaTaxonomyFormat(model.TextFileFormat):

    def sniff(self):

        with self.open() as fh:
            return True
            # TODO add validation here
            for line, _ in zip(fh, range(5)):

                line = line.strip()
                # check that it's a string
                try:
                    if type(line) == str:
                        pass
                    else:
                        return False
                except:
                    return False

                # check that first two items match (Sumaclust standard)
                try:
                    check_list = line.split('\t')
                    if check_list[0] == check_list[1]:
                        pass
                    else:
                        return False
                except:
                    return False

                # (TODO) shouldn't contain special chars

            # if nothing breaks from validation above, then return true
            return True

SilvaTaxonomyDirectoryFormat = model.SingleFileDirectoryFormat(
    'SilvaTaxonomyDirectoryFormat', 'silva_taxonomy.txt',
    SilvaTaxonomyFormat)