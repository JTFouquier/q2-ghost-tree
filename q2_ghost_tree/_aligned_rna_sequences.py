# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

###############################################################################
#
# AlignedRNAFASTAFormat
#
#     Aligned sequences for RNA (sequences containing 'U')
#
###############################################################################

import qiime2.plugin.model as model
import skbio


class AlignedRNAFASTAFormat(model.TextFileFormat):
    def sniff(self):
        filepath = str(self)
        sniffer = skbio.io.io_registry.get_sniffer('fasta')
        if sniffer(filepath)[0]:
            generator = skbio.io.read(filepath, constructor=skbio.RNA,
                                      format='fasta', verify=False)
            try:
                initial_length = len(next(generator))
                for seq, _ in zip(generator, range(4)):
                    if len(seq) != initial_length:
                        return False
                return True
            # ValueError raised by skbio if there are invalid RNA chars.
            except (StopIteration, ValueError):
                pass
        return False


AlignedRNAFASTADirectoryFormat = model.SingleFileDirectoryFormat(
    'AlignedRNAFASTADirectoryFormat', 'aligned-rna.fasta',
    AlignedRNAFASTAFormat)
