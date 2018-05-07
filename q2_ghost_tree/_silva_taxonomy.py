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
# SilvaTaxonomy
#
#     Taxonomy File for Silva Database.  A tab-separated file that identifes
#     the taxonomy and rank of a mapping number in `accession_fh`. This file
#     should contain exactly five columns beginning with taxonomy, mapping
#     number and rank. The last two columns are ignored.
#
###############################################################################


class SilvaTaxonomyFormat(model.TextFileFormat):

    def sniff(self):

        with self.open() as fh:

            for line, _ in zip(fh, range(5)):

                line_list = line.strip().split("\t")
                taxonomy = line_list[0]
                mapping_num = line_list[1]

                # taxonomy line needs to contain ';'
                if re.search(";", taxonomy):
                    pass
                else:
                    return False

                # mapping number must be an int (cast ok)
                try:
                    int(mapping_num)
                    pass
                except ValueError:
                    return False

                # there must be at least three columns in the file
                if len(line_list) >= 3:
                    pass
                else:
                    return False

            # if nothing breaks from validation above, then return true
            return True


SilvaTaxonomyDirectoryFormat = model.SingleFileDirectoryFormat(
    'SilvaTaxonomyDirectoryFormat', 'silva_taxonomy.txt',
    SilvaTaxonomyFormat)
