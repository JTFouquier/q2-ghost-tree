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
# SilvaAccession
#
#       A tab-separated file mapping accession numbers to a mapping number in
#       `taxonomy_map`. This file should contain exactly two columns:
#       accession number and mapping number.
#
###############################################################################


class SilvaAccessionFormat(model.TextFileFormat):

    def sniff(self):

        with self.open() as fh:

            for line, _ in zip(fh, range(5)):

                line_list = line.strip().split("\t")
                accession = line_list[0]
                taxid = line_list[1]

                # are there two items in each row?
                if len(line_list) == 2:
                    pass
                else:
                    return False

                # first item should not be an int; it contains chars
                try:
                    int(accession)
                    return False
                except ValueError:
                    pass

                # is the second item an int? (taxids must be ints)
                try:
                    int(taxid)
                    pass
                except ValueError:
                    return False

            # if nothing breaks from validation above, then return true
            return True


SilvaAccessionDirectoryFormat = model.SingleFileDirectoryFormat(
    'SilvaAccessionDirectoryFormat', 'silva_accession.txt',
    SilvaAccessionFormat)
