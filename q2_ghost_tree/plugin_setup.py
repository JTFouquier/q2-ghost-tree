import qiime2.plugin
from q2_types.feature_data import FeatureData, Sequence, Taxonomy, AlignedSequence
from q2_types.tree import Phylogeny, Rooted

import q2_ghost_tree
from ._scaffold_hybrid_tree import scaffold_hybrid_tree
from ._extensions_cluster import extensions_cluster
from ._otu_map import OtuMapFormat, OtuMapDirectoryFormat

# initiate Qiime2 plugin
plugin = qiime2.plugin.Plugin(
    name='ghost-tree',
    description='ghost-tree is a bioinformatics tool that combines sequence data from two genetic marker databases '
                'into one phylogenetic tree that can be used for diversity analyses. One database is used as a '
                '"foundation tree" because it provides better phylogeny across all phyla, and the other database '
                'provides finer taxonomic resolution.',
    version=q2_ghost_tree.__version__,
    website='https://github.com/JTFouquier/ghost-tree',
    package='q2_ghost_tree',
    user_support_text=None,
    citation_text='ghost-tree: creating hybrid-gene phylogenetic trees for diversity analyses. Fouquier J, '
                  'Rideout JR, Bolyen E, Chase J, Shiffer A, McDonald D, Knight R, Caporaso JG, and Kelley ST',
    short_description='Plugin for creating hybrid-gene phylogenetic trees',
)

OtuMap = qiime2.plugin.SemanticType('OtuMap')

plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)

plugin.register_semantic_types(OtuMap)

plugin.register_semantic_type_to_format(
    OtuMap,
    artifact_format=OtuMapDirectoryFormat)


# Register all methods used by ghost-tree
plugin.methods.register_function(
    function=scaffold_hybrid_tree,
    inputs={
        'otu_map': OtuMap, # ghost-tree semantic type
        'extension_taxonomy': FeatureData[Taxonomy],
        'extension_seq': FeatureData[Sequence],
        'foundation_alignment': FeatureData[AlignedSequence]
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