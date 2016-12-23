import qiime.plugin
import q2_ghost_tree
import importlib

from q2_dummy_types import IntSequence1, IntSequence2
from q2_types.feature_data import FeatureData, Sequence, Taxonomy, AlignedSequence
from q2_types.tree import Phylogeny, Rooted


from ._dummy_method import concatenate_ints
from ._scaffold_hybrid_tree import scaffold_hybrid_tree
from ._extensions_cluster import extensions_cluster


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

print (plugin.__dict__)

importlib.import_module('q2_ghost_tree._otu_map')

from q2_ghost_tree._otu_map import OtuMap


print (plugin.__dict__)

print (plugin.types['OtuMap'])

print (OtuMap.__dict__)
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
        'otus_fh': str, # ghost-tree semantic type
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
#(TODO) make this an OtuMap
#(TODO) make int a float
plugin.methods.register_function(
    function=extensions_cluster,
    inputs={
        'extensions_sequences_fp': FeatureData[Sequence],
    },
    parameters={ 'similarity_threshold': qiime.plugin.Int
    },
    outputs=[
        ('otu_formatted_fp', OtuMap),
    ],
    name='extensions_cluster',
    description='Groups sequences in .fasta file by similarity threshold'
)