import qiime2.plugin

from q2_types.feature_data import FeatureData, Sequence, AlignedSequence, \
    Taxonomy
from q2_types.tree import Phylogeny, Rooted, Unrooted

import q2_ghost_tree

# import plugin 'wrapper' code to original ghost-tree code
from ._scaffold_hybrid_tree_foundation_alignment import \
    scaffold_hybrid_tree_foundation_alignment
from ._scaffold_hybrid_tree_foundation_tree import \
    scaffold_hybrid_tree_foundation_tree
from ._extensions_cluster import extensions_cluster
# from ._tip_to_tip_distances import tip_to_tip_distances
from ._silva import extract_fungi

# import custom semantic types
from ._otu_map import OtuMapFormat, OtuMapDirectoryFormat
from ._silva_taxonomy import SilvaTaxonomyFormat, SilvaTaxonomyDirectoryFormat
from ._silva_accession import SilvaAccessionFormat, \
    SilvaAccessionDirectoryFormat

# TODO Citations are not listed correctly here
# initiate Qiime2 plugin
plugin = qiime2.plugin.Plugin(
    name='ghost-tree',
    description='ghost-tree is a bioinformatics tool that combines sequence '
                'data from two genetic marker databases '
                'into one phylogenetic tree that can be used for diversity '
                'analyses. One database is used as a "foundation tree" '
                'because it provides better phylogeny across all phyla, '
                'and the other database provides finer taxonomic resolution.\n'
                ''
                '\nPlease cite: ghost-tree: creating hybrid-gene phylogenetic '
                'trees for diversity analyses. Fouquier J, Rideout JR, '
                'Bolyen E, Chase J, Shiffer A, McDonald D, Knight R, Caporaso '
                'JG, and Kelley ST',
    version=q2_ghost_tree.__version__,
    website='https://github.com/JTFouquier/ghost-tree',
    package='q2_ghost_tree',
    user_support_text=None,
    citation_text='ghost-tree: creating hybrid-gene phylogenetic trees for '
                  'diversity analyses. Fouquier J, Rideout JR, Bolyen E, '
                  'Chase J, Shiffer A, McDonald D, Knight R, Caporaso JG, and '
                  'Kelley ST',
    short_description='Plugin for creating hybrid-gene phylogenetic trees.',
)

OtuMap = qiime2.plugin.SemanticType('OtuMap')
plugin.register_formats(OtuMapFormat, OtuMapDirectoryFormat)
plugin.register_semantic_types(OtuMap)
plugin.register_semantic_type_to_format(OtuMap,
                                        artifact_format=OtuMapDirectoryFormat)

# Register all methods used by ghost-tree
# TODO add descriptions here... what is the point of name... redundant on help
# TODO pages

graft_level = qiime2.plugin
graft_level = graft_level.Str % \
              graft_level.Choices({'p', 'c', 'o', 'f', 'g'})

plugin.methods.register_function(
    function=scaffold_hybrid_tree_foundation_alignment,
    inputs={
        'otu_map': OtuMap,  # ghost-tree semantic type
        'extension_taxonomy': FeatureData[Taxonomy],
        'extension_sequences': FeatureData[Sequence],
        'foundation_alignment': FeatureData[AlignedSequence],
            },
    parameters={
        'graft_level': graft_level,
                },
    outputs=[
        ('ghost_tree', Phylogeny[Rooted]),
    ],
    input_descriptions={
        'otu_map': 'OtuMap. The output from the command "extensions-cluster". '
                   'Each line in an OtuMap contains sequences that are a '
                   'certain percent similar to one another.',
        'extension_taxonomy': 'FeatureData[Taxonomy] The taxonomy for the '
                              'extension sequences for a ghost tree.',
        'extension_sequences': 'FeatureData[Sequence] The extension sequences '
                               'for the ghost tree. The extensions are '
                               'grafted onto a foundation tree.',
        'foundation_alignment': 'FeatureData[AlignedSequence] Aligned '
                                'sequences that will be used as the '
                                'foundation tree for a ghost tree.',
    },
    parameter_descriptions={
        'graft_level': 'The taxonomic rank you would like to group extension '
                       'sequences by prior to having them grafted onto the '
                       'foundation. Rank choices are p: phylum, c: class, '
                       'o: order, f: family, g: genus. Please note grafting '
                       'at higher taxonomic ranks than genus is experimental, '
                       'but may be useful for marker-gene regions which have '
                       'less optimal taxonomic resolution.',
    },
    output_descriptions={
        'ghost_tree': 'Phylogeny[Rooted]. This is your final ghost tree output'
                      'as a .qza. Extracted it will be in Newick format.'
    },
    name='scaffold-hybrid-tree-foundation-alignment',
    description='Create a hybrid-gene phylogenetic tree using an '
                'alignment as a foundation.'
)

# Register all methods used by ghost-tree
plugin.methods.register_function(
    function=scaffold_hybrid_tree_foundation_tree,
    inputs={
        'otu_map': OtuMap,  # ghost-tree semantic type
        'extension_taxonomy': FeatureData[Taxonomy],
        'extension_sequences': FeatureData[Sequence],
        'foundation_tree': Phylogeny[Rooted | Unrooted],
        'foundation_taxonomy': FeatureData[Taxonomy],
            },
    parameters={
        'graft_level': graft_level,
                },
    outputs=[
        ('ghost_tree', Phylogeny[Rooted]),
    ],
    input_descriptions={
        'otu_map': 'OtuMap. The output from the command "extensions-cluster". '
                   'Each line in an OtuMap contains sequences that are a '
                   'certain percent similar to one another.',
        'extension_taxonomy': 'FeatureData[Taxonomy] The taxonomy for the '
                              'extension sequences for a ghost tree.',
        'extension_sequences': 'FeatureData[Sequence] The extension sequences '
                               'for the ghost tree. The extensions are '
                               'grafted onto a foundation tree.',
        'foundation_tree': 'Phylogeny[Rooted | Unrooted] The foundation tree '
                           'for your ghost tree. If you would like to use a '
                           'foundation alignment, you can use the command '
                           '"scaffold-hybrid-tree-foundation-alignment".',
        'foundation_taxonomy': 'FeatureData[Taxonomy] The taxonomy for the '
                               'foundation tree.',
    },
    parameter_descriptions={
        'graft_level': 'The taxonomic rank you would like to group extension '
                       'sequences by prior to having them grafted onto the '
                       'foundation. Rank choices are: p: phylum, c: '
                       'class, o: order, f: family, g: genus. Please note '
                       'grafting at higher taxonomic ranks than genus is '
                       'experimental, but may be useful for marker-gene '
                       'regions which have less optimal taxonomic resolution.',
    },
    output_descriptions={
        'ghost_tree': 'Phylogeny[Rooted]. This is your final ghost tree '
                      'output as a .qza. Extracted it will be in Newick '
                      'format.',
    },
    name='scaffold-hybrid-tree-foundation-tree',
    description='Create a hybrid-gene phylogenetic tree using '
                'a tree as a foundation.'
)

# setup similarity threshold
p = qiime2.plugin
p = p.Float % p.Range(0.00, 1.00, inclusive_end=True, inclusive_start=False)

plugin.methods.register_function(
    function=extensions_cluster,
    inputs={
        'extension_sequences': FeatureData[Sequence],
    },
    parameters={
        'similarity_threshold': p
    },
    outputs=[
        ('otu_map', OtuMap),
    ],
    input_descriptions={
        'extension_sequences': 'FeatureData[Sequence] The extension sequences '
                               'for the ghost tree. The extensions are '
                               'grafted onto a foundation tree, but should '
                               'be first clustered to address the large '
                               'amount of unclassified or unidentified '
                               'sequences in taxonomic databases.',
    },
    parameter_descriptions={
        'similarity_threshold': 'Value (float) greater than 0.00 and less '
                                'than or equal to 1.00. This is the '
                                'percent similarity you would like your '
                                'sequences clustered at. E.g., 0.90 means '
                                'that sequences in one group will be 90% '
                                'similar to one another',
    },
    output_descriptions={
         'otu_map': 'OtuMap. This returns an OtuMap where each line contains '
                    'sequences that are a certain percent similar to one '
                    'another as entered in the "--p-similarity-threshold" '
                    'parameter. ',
    },
    name='extensions-cluster',
    description='Groups sequences in .fasta file by similarity threshold'
)

# register semantic types specific to 'extract fungi' for Silva database

SilvaAccession = qiime2.plugin.SemanticType('SilvaAccession')
plugin.register_formats(SilvaAccessionFormat, SilvaAccessionDirectoryFormat)
plugin.register_semantic_types(SilvaAccession)
plugin.register_semantic_type_to_format(
    SilvaAccession, artifact_format=SilvaAccessionDirectoryFormat)

SilvaTaxonomy = qiime2.plugin.SemanticType('SilvaTaxonomy')
plugin.register_formats(SilvaTaxonomyFormat, SilvaTaxonomyDirectoryFormat)
plugin.register_semantic_types(SilvaTaxonomy)
plugin.register_semantic_type_to_format(
    SilvaTaxonomy, artifact_format=SilvaTaxonomyDirectoryFormat)

plugin.methods.register_function(
    function=extract_fungi,
    inputs={
        'aligned_fasta_file': FeatureData[AlignedSequence],
        'accession_file': SilvaAccession,  # Silva semantic type
        'taxonomy_file': SilvaTaxonomy,  # Silva semantic type
        },
    parameters={
        },
    outputs=[
        ('output_file', FeatureData[AlignedSequence]),
    ],
    name='extract-fungi',
    description='Extract fungi from a large Silva database',
)

# plugin.methods.register_function(
#     function=tip_to_tip_distances,
#     inputs={
#         'tree_1': Phylogeny[Rooted],
#         'tree_2': Phylogeny[Rooted],
#     },
#     parameters={'method': qiime2.plugin.Str,
#     },
#     outputs=[
#         ('printed_output', qiime2.plugin.Str),
#     ],
#     name='compare_trees',
#     description='Compare tip distances in two phylogenetic trees using '
#                 'Mantel test'
# )
