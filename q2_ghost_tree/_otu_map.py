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

from .plugin_setup import plugin

# Define semantic types
OtuMap = qiime2.plugin.SemanticType('OtuMap')

# Register semantic types on the plugin.
plugin.register_semantic_types(OtuMap)


###############################################################################
#
# OtuMap
#
#     Groups of OTUs clustered by a similarity threshold. Each line contains
#     tab separated OTUs that are within the similarity threshold.
#
###############################################################################

# Define a file format for use in the directory format defined below.
class OtuMapFormat(model.TextFileFormat):
    # Sniffers are used when reading and writing data from a file. A sniffer
    # determines whether a file appears to conform to its file format. Sniffers
    # should only read a small piece of the file to determine membership and
    # should not rely on file extension.
    def sniff(self):
        with self.open() as fh:
            for line, _ in zip(fh, range(5)):
                try:
                    print ('TESTING INSIDE OTU MAP SNIFFER')
                    int(line.rstrip('\n'))
                except (TypeError, ValueError):
                    return False
            return True

# Define a directory format. A directory format is a directory structure
# composed of one or more files (nested directories are also supported). Each
# file has a specific file format associated with it.  This directory format
# only has a single file, ints.txt, with file format `IntSequenceFormat`.
OtuMapDirectoryFormat = model.SingleFileDirectoryFormat(
    'OtuMapDirectoryFormat', 'ints.txt', OtuMapFormat)

# Register the formats defined above. Formats must be unique across all
# plugins installed on a users system.
plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)

# Register the directory format with the semantic types defined above. A
# directory format can be registered to multiple semantic types. Currently, a
# semantic type can only have a single directory format associated with it.
plugin.register_semantic_type_to_format(
    OtuMap,
    artifact_format=OtuMapDirectoryFormat)

# (TODO)
# Define a transformer for converting a file format (`IntSequenceFormat`) into
# a view type (`list` in this case). To indicate that only the QIIME 2
# Framework should interact with a transformer, a non-meaningful name is used.
# The convention is `_<int counter>`, but anything is acceptable. The aim is to
# draw the reader to the function annotations, which convey precisely what the
# transformer is responsible for.
@plugin.register_transformer
def _1(ff: OtuMapFormat) -> list:
    with ff.open() as fh:
        data = [] # becomes a list of lists (otus in one similarity threshold)
        for line in fh:
            otus = line.split('\t')
            data.append(otus)
        return data

# (TODO)
# Define a transformer for converting a view type (`list` in this case) to the
# file format (`IntSequenceFormat`). To indicate that only the QIIME 2
# Framework should interact with a transformer, a non-meaningful name is used.
# The convention is `_<int counter>`, but anything is acceptable. The aim is to
# draw the reader to the function annotations, which convey precisely what the
# transformer is responsible for.
@plugin.register_transformer
def _2(data: list) -> OtuMapFormat:
    otu_map = OtuMapFormat()
    with otu_map.open() as fh:
        for otu_list in data:
            fh.write('%d\n' % '\t'.join(otu_list))
    return otu_map
