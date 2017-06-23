# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


# copied from QIIME 2 dummy types example for defining a new semantic type
# https://github.com/qiime2/q2-dummy-types/blob/master/q2_dummy_types/
# _int_sequence.py
import qiime2.plugin
import qiime2.plugin.model as model

# from .plugin_setup import plugin

# Define semantic types

# Register semantic types on the plugin.

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
            for line, _ in zip(fh, range(5)):
                try:
                    print('TESTING INSIDE OTU MAP SNIFFER')
                    int(line.rstrip('\n'))
                except (TypeError, ValueError):
                    return False
            return True
#
# OtuMapDirectoryFormat = model.SingleFileDirectoryFormat(
#     'OtuMapDirectoryFormat', 'ints.txt', OtuMapFormat)
#
# plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)
#
# plugin.register_semantic_type_to_format(
#     OtuMap,
#     artifact_format=OtuMapDirectoryFormat)
