import qiime.plugin
import q2_ghost_tree

from q2_dummy_types import IntSequence1, IntSequence2
from q2_types.feature_data import FeatureData, Sequence, Taxonomy, AlignedSequence
from q2_types.tree import Phylogeny, Rooted


from ._dummy_method import concatenate_ints
from ._scaffold_hybrid_tree import scaffold_hybrid_tree
from ._extensions_cluster import extensions_cluster


import qiime.plugin.model as model


# (TODO) need to register all code here

plugin = qiime.plugin.Plugin(
    name='ghost-tree',
    version=q2_ghost_tree.__version__,
    website='https://github.com/JTFouquier/ghost-tree',
    package='q2_ghost_tree',
    # Information on how to obtain user support should be provided as a free
    # text string via user_support_text. If None is provided, users will
    # be referred to the plugin's website for support.
    user_support_text=None,
    # (TODO) Information on how the plugin should be cited should be provided as a
    # free text string via citation_text. If None is provided, users
    # will be told to use the plugin's website as a citation.
    citation_text=None
)

"""
Below Semantic Types that are ghost-tree specific are defined.
"""

# Define semantic types.
OtuMap = qiime.plugin.SemanticType('OtuMap')

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
OtuMapDirectoryFormat = model.SingleFileDirectoryFormat('OtuMapDirectoryFormat', 'ints.txt', OtuMapFormat)

# Register the formats defined above. Formats must be unique across all
# plugins installed on a users system.
plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)

# Register the directory format with the semantic types defined above. A
# directory format can be registered to multiple semantic types. Currently, a
# semantic type can only have a single directory format associated with it.
plugin.register_semantic_type_to_format(OtuMap, artifact_format=OtuMapDirectoryFormat)

# (TODO): FIX function and definition
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

# (TODO) FIX function and definition... otus groups are in lines/lists
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


# The next two code blocks are examples of how to register methods and
# visualizers. Replace them with your own registrations when you are ready to
# develop your plugin.

'''
Register the methods used by ghost-tree
'''

# Example method:
plugin.methods.register_function(
    function=concatenate_ints,
    inputs={
        'ints1': IntSequence1 | IntSequence2,
        'ints2': IntSequence1,
        'ints3': IntSequence2
    },
    parameters={
        'int1': qiime.plugin.Int,
        'int2': qiime.plugin.Int
    },
    outputs=[
        ('concatenated_ints', IntSequence1)
    ],
    name='Concatenate integers',
    description='This method concatenates integers into a single sequence in '
                'the order they are provided.'
)

plugin.methods.register_function(
    function=scaffold_hybrid_tree,
    inputs={
        'otus_fh': OtuMap, # ghost-tree semantic type
        'extension_taxonomy_fh': FeatureData[Taxonomy],
        'extension_seq_fh': FeatureData[Sequence],
        'foundation_alignment_fh': FeatureData[AlignedSequence]
    },
    parameters={
    },
    outputs=[
        ('ghost_tree_fp', Phylogeny[Rooted]),
    ],
    name='scaffold-hybrid-tree',
    description='This method creates a hybrid-gene phylogenetic tree.'
)

#(TODO) clarify parameter vs inputs here (example above)
plugin.methods.register_function(
    function=extensions_cluster,
    inputs={
        'extensions_sequences_fp': FeatureData[Sequence],
    },
    parameters={ 'similarity_threshold': float
    },
    outputs=[
        ('otu_formatted_fp', OtuMap),
    ],
    name='extensions_cluster',
    description='Groups sequences in .fasta file by similarity threshold'
)