

import skbio

from q2_types.feature_data import AlignedDNAFASTAFormat

from ghosttree.filter import filter_positions

def filter_alignment_positions(aligned_sequences_file: AlignedDNAFASTAFormat,
                               maximum_gap_frequency: str,
                               maximum_position_entropy: str) -> \
        AlignedDNAFASTAFormat:
    aligned_sequences_fh = aligned_sequences_file.open()

    fasta_file = AlignedDNAFASTAFormat()

    skbio.write(filter_positions(aligned_sequences_fh, maximum_gap_frequency,
                maximum_position_entropy), into=str(fasta_file),
                format='fasta')

    return fasta_file
