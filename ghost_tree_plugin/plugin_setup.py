import qiime.plugin

import ghost_tree_plugin

# These imports are only included to support the example methods and
# visualizers. Remove these imports when you are ready to develop your plugin.
from q2_dummy_types import IntSequence1, IntSequence2, Mapping
from ._dummy_method import concatenate_ints

plugin = qiime.plugin.Plugin(
    name='ghost-tree',
    version=ghost_tree_plugin.__version__,
    website='https://github.com/JTFouquier/ghost-tree',
    package='ghost_tree_plugin',
    # Information on how to obtain user support should be provided as a free
    # text string via user_support_text. If None is provided, users will
    # be referred to the plugin's website for support.
    user_support_text=None,
    # Information on how the plugin should be cited should be provided as a
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

# JF removed reference to QIIME visualizer