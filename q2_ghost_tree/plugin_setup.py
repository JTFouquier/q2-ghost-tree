import qiime2.plugin
import q2_ghost_tree
import importlib

from q2_types.feature_data import FeatureData, Sequence, Taxonomy, AlignedSequence
from q2_types.feature_table import FeatureTable

from q2_types.tree import Phylogeny, Rooted
from qiime2.plugin import (Str, Int, Choices, MetadataCategory, Plugin)
import qiime2.plugin.model as model

from ._scaffold_hybrid_tree import scaffold_hybrid_tree
from ._extensions_cluster import extensions_cluster
# from q2_ghost_tree import OtuMap
# from ._type import OtuMap
from ._otu_map import OtuMapFormat
import qiime2.plugin.model as model


plugin = qiime2.plugin.Plugin(
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

OtuMap = qiime2.plugin.SemanticType('OtuMap')
OtuMapDirectoryFormat = model.SingleFileDirectoryFormat(
    'OtuMapDirectoryFormat', 'ints.txt', OtuMapFormat)
#
#
# plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)

plugin.register_semantic_type_to_format(
    OtuMap,
    artifact_format=OtuMapDirectoryFormat)

print (plugin.__dict__)

# print (plugin.types['OtuMap'])

print (OtuMap.__dict__)

'''
Register the methods used by ghost-tree
'''

plugin.methods.register_function(
    function=scaffold_hybrid_tree,
    inputs={
        'otu_file_fh': OtuMap, # ghost-tree semantic type
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

plugin.methods.register_function(
    function=extensions_cluster,
    inputs={
        'extensions_sequences_fp': FeatureData[Sequence],
    },
    parameters={'similarity_threshold': qiime2.plugin.Int
    },
    outputs=[
        ('otu_formatted_fp', OtuMap),
    ],
    name='extensions_cluster',
    description='Groups sequences in .fasta file by similarity threshold'
)
