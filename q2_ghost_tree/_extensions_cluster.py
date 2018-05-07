# ----------------------------------------------------------------------------
# Copyright (c) 2015--, ghost-tree development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------
import os
import tempfile
from shutil import copyfile

from q2_types.feature_data import DNAFASTAFormat

from ghosttree.extensions.cluster import preprocess_extension_tree_sequences

from ._otu_map import OtuMapFormat


def extensions_cluster(extension_sequences: DNAFASTAFormat,
                       similarity_threshold: str) -> OtuMapFormat:

    extension_sequences_fh = extension_sequences.open()

    with tempfile.TemporaryDirectory() as tmp:

        # need ghost_tree.nwk here otherwise file exists
        gt_path = os.path.join(tmp, 'otu_map')
        preprocess_extension_tree_sequences(
            str(extension_sequences_fh.name), str(similarity_threshold),
            gt_path)

        copyfile(gt_path, tmp + 'otu_map')

        return OtuMapFormat(tmp + 'otu_map', 'r')
