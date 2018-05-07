# ----------------------------------------------------------------------------
# Copyright (c) 2015--, ghost-tree development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------
import tempfile
import os

from ghosttree.scaffold.hybridtree import extensions_onto_foundation
from q2_types.feature_data import DNAFASTAFormat, TSVTaxonomyFormat
from q2_types.tree import NewickFormat

from ._otu_map import OtuMapFormat

# created an additional function so as to keep naming convention the same
# as in the original ghost-tree tool.

_ghost_tree_defaults = {'graft_level': 'g'}


def scaffold_hybrid_tree_foundation_tree(
        otu_map: OtuMapFormat,
        extension_taxonomy: TSVTaxonomyFormat,
        extension_sequences: DNAFASTAFormat,
        foundation_tree: NewickFormat,
        foundation_taxonomy: TSVTaxonomyFormat,
        graft_level: str=_ghost_tree_defaults['graft_level'],
        ) -> NewickFormat:

    otu_map_fh = otu_map.open()
    extension_taxonomy_fh = extension_taxonomy.open()
    extension_sequences_fh = extension_sequences.open()
    foundation_alignment_fh = foundation_tree.open()
    if foundation_taxonomy:
        foundation_taxonomy_fh = foundation_taxonomy.open()
    else:
        foundation_taxonomy_fh = None

    with tempfile.TemporaryDirectory() as tmp:

        # need ghost_tree.nwk here otherwise file exists
        gt_path = os.path.join(tmp, 'ghost_tree')
        thetree = extensions_onto_foundation(otu_map_fh, extension_taxonomy_fh,
                                             extension_sequences_fh,
                                             foundation_alignment_fh,
                                             gt_path, graft_level,
                                             foundation_taxonomy_fh)[0]

        # write new file to tmp file; gets deleted when this block is done
        gt_temp_file = open(tmp + 'ghost_tree', 'w')
        gt_temp_file.write(thetree)
        gt_temp_file.close()

        return NewickFormat(tmp + 'ghost_tree', 'r')
