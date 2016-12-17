import qiime.plugin

import q2_ghost_tree

# These imports are only included to support the example methods and
# visualizers. Remove these imports when you are ready to develop your plugin.
from q2_dummy_types import IntSequence1, IntSequence2, Mapping
from q2_types.feature_table import ( FeatureTable, Frequency, RelativeFrequency, PresenceAbsence)
from q2_types.feature_data import (FeatureData, Sequence, Taxonomy, AlignedSequence)
from q2_types.tree import (Phylogeny, Rooted)
from ._dummy_method import concatenate_ints
from ._hybrid_tree import extensions_onto_foundation
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

# The next two code blocks are examples of how to register methods and
# visualizers. Replace them with your own registrations when you are ready to
# develop your plugin.

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
    function=extensions_onto_foundation,
    inputs={
        'otus_fh': FeatureTable[PresenceAbsence],
        'extension_taxonomy_fh': FeatureData[Taxonomy],
        'extension_seqs_fh': FeatureData[Sequence],
        'foundation_alignment_fh': FeatureData[AlignedSequence]
    },
    parameters={
    },
    outputs=[
        ('ghost_tree_newick', Phylogeny[Rooted]),
    ],
    name='hybrid-tree',
    description='This method creates a hybrid-gene phylogenetic tree.'
)