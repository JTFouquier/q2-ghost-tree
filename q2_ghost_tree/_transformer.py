from io import StringIO
from q2_ghost_tree.plugin_setup import plugin

from q2_types.feature_data import AlignedDNAFASTAFormat, \
    AlignedDNASequencesDirectoryFormat
from ._aligned_rna_sequences import AlignedRNAFASTAFormat
from q2_types.feature_data import FeatureData, Sequence, AlignedSequence


def parse_fasta(f, trim_desc=False):
    # TODO this is from Kyle B. Cite properly before release
    """Parse a FASTA format file.

    Parameters
    ----------
    f : File object or iterator returning lines in FASTA format.

    Returns
    -------
    An iterator of tuples containing two strings
        First string is the sequence description, second is the
        sequence.

    Notes
    -----
    This function removes whitespace in the sequence and translates
    "U" to "T", in order to accommodate FASTA files downloaded from
    SILVA and the Living Tree Project.
    """
    f = iter(f)
    desc = next(f).strip()[1:]
    if trim_desc:
        desc = desc.split()[0]
    seq = StringIO()
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            yield desc, seq.getvalue()
            desc = line[1:]
            if trim_desc:
                desc = desc.split()[0]
            seq = StringIO()
        else:
            seq.write(line.replace(" ", "").replace("U", "T"))
    yield desc, seq.getvalue()



def write_fasta(f, seqs):
    for desc, seq in seqs:
        f.write(">{0}\n{1}\n".format(desc, seq))


# TODO change silly function name
# The issue here is the wrong data format AND transformer does not work
# even with simple test like seq.write("ATCG")
@plugin.register_transformer
def _my_great_transformer(ff: AlignedRNAFASTAFormat) -> \
        AlignedDNAFASTAFormat:

    ff2 = AlignedDNAFASTAFormat()
    seqs = parse_fasta(ff)

    write_fasta(ff2, seqs)

    return ff2
    # convert RNA to DNA, output is a new instance of AlignedDNAFASTAFormat
