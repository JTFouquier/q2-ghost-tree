
import skbio
from ghosttree.silva.filter import fungi_from_fasta

from ._silva_accession import SilvaAccessionFormat
from ._silva_taxonomy import SilvaTaxonomyFormat
from q2_types.feature_data import AlignedDNAFASTAFormat

def extract_fungi(
        aligned_silva_file: AlignedDNAFASTAFormat,
        accession_file: SilvaAccessionFormat,
        taxonomy_file: SilvaTaxonomyFormat,
        ) -> AlignedDNAFASTAFormat:

    aligned_silva_fh = aligned_silva_file.open()
    accession_fh = accession_file.open()
    taxonomy_fh = taxonomy_file.open()

    fasta_file = AlignedDNAFASTAFormat()
    skbio.write(fungi_from_fasta(aligned_silva_fh, accession_fh,
                taxonomy_fh), into=str(fasta_file), format='fasta')

    # TODO this code is a good example of pithy return for plugins
    # TODO redo other functions in the same way by instantiating a

    return fasta_file
