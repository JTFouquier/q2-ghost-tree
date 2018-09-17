# q2-ghost-tree installation and testing instructions


This is a QIIME 2 plugin for 'ghost-tree: creating hybrid-gene phylogenetic
trees for diversity analysis.' The original ghost-tree repository can be found
[here](https://github.com/JTFouquier/ghost-tree), and the paper can be found
[here](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-016-0153-6).


## Plugin installation:

1)  Install the current version of QIIME 2 and activate it following the
    [directions on the QIIME 2 website](https://docs.qiime2.org/2018.8/install/).
    Always use the most recent version.

    Make sure you are now working inside the QIIME 2 virtual environment.
    The command prompt should include something like `qiime2-2018.8` with
    the current version of QIIME 2. You want to be working from within the
    QIIME 2 environment when you install the rest of the code so that
    your new tools are organized and installed in this software
    environment.

2)  Install the standalone, original *ghost-tree* tool from Conda:

    *ghost-tree* is hosted on Conda's Bioconda channel (channels are
    designated -c). You can install it using `conda install
    ghost-tree` or `conda install ghost-tree -c bioconda`.

    Typing `ghost-tree` should bring up help documentation about
    ghost-tree. If you do not see the help docs, something went wrong.

    *ghost-tree* has three software dependencies it relies on. These are
    Sumaclust, Muscle and FastTree. If you use Conda to install
    ghost-tree, it should have installed these for you!

3)  Next, you will install the *q2-ghost-tree* plugin with the command:

    `git clone https://github.com/JTFouquier/q2-ghost-tree.git`

    Find the setup.py file by navigating to the appropriate directory
    on the command line and do `pip install -e .` in the same way you
    did with the original *ghost-tree* tool.

    When you type `qiime` you should now see ghost-tree as an available plugin.

## Importing files as QIIME 2 data types using *small test files*:

Test that you can import the files in the
[small_test_files directory](https://github.com/JTFouquier/q2-ghost-tree/tree/master/small_test_files/original-non-qiime-files)

-- Extension sequences:

`qiime tools import
--input-path original-non-qiime-files/extension_seqs.fasta
--type FeatureData[Sequence]
--output-path extension_seqs.qza`

-- Extension taxonomy:

`qiime tools import
--input-path original-non-qiime-files/minitaxonomy.txt
--type FeatureData[Taxonomy]
--input-format HeaderlessTSVTaxonomyFormat
--output-path minitaxonomy.qza`

-- Extension OTUs

`qiime tools import
--input-path original-non-qiime-files/miniotus.txt
--type OtuMap
--output-path miniotus.qza`

-- Foundation sequences:

`qiime tools import
--input-path original-non-qiime-files/foundation_seqs.fasta
--type FeatureData[Sequence]
--output-path foundation_seqs.qza`

-- Foundation tree:

`qiime tools import
--input-path original-non-qiime-files/foundation_tree.nwk
--type Phylogeny[Rooted]
--output-path foundation_tree.qza`

f) Foundation taxonomy:

`qiime tools import
--input-path original-non-qiime-files/minitaxonomy_foundation.txt
--type FeatureData[Taxonomy]
--input-format HeaderlessTSVTaxonomyFormat
--output-path minitaxonomy_foundation.qza`

-- Foundation alignment:

`qiime tools import
--input-path original-non-qiime-files/silva_fungi_only.txt
--type FeatureData[AlignedSequence]
--input-format AlignedRNAFASTAFormat
--output-path silva_fungi_only.qza`

## Testing each subcommand in `qiime ghost-tree`

-- Group your rep seqs at 90% similarity. This handles the
abundant unidentified organisms.

`qiime ghost-tree extensions-cluster
--i-extension-sequences extension_seqs.qza
--p-similarity-threshold 0.90
--o-otu-map extensions_otu_map_90.qza`

-- Create a ghost tree using a foundation .nwk tree. Note the
subcommand used.

`qiime ghost-tree scaffold-hybrid-tree-foundation-tree
--i-otu-map extensions_otu_map_90.qza
--i-extension-taxonomy minitaxonomy.qza
--i-extension-sequences extension_seqs.qza
--i-foundation-tree foundation_tree.qza
--i-foundation-taxonomy minitaxonomy_foundation.qza
--o-ghost-tree ghost-tree-foundation-tree-90-otus.qza`

-- Create a ghost tree using a foundation .nwk tree, and using
*class*-level graft points instead of default *genus*.

`qiime ghost-tree scaffold-hybrid-tree-foundation-tree
--i-otu-map extensions_otu_map_90.qza --i-extension-taxonomy
minitaxonomy.qza --i-extension-sequences extension_seqs.qza
--i-foundation-tree foundation_tree.qza
--i-foundation-taxonomy minitaxonomy_foundation.qza
--o-ghost-tree ghost-tree-foundation-tree-90-otus-class-level-graft-points.qza
--p-graft-level c`

-- Create a ghost tree using aligned sequences instead of a tree as
your foundation. Note the subcommand used.

`qiime ghost-tree scaffold-hybrid-tree-foundation-alignment
--i-otu-map extensions_otu_map_90.qza
--i-extension-taxonomy minitaxonomy.qza
--i-extension-sequences extension_seqs.qza
--i-foundation-alignment silva_fungi_only.qza
--o-ghost-treeghost-tree-foundation-allignment-90-otus.qza`


## Using full size files (these are large and will take a while)

   SILVA (or the foundation)
   TODO
    https://www.arb-silva.de/no_cache/download/archive/release_132/Exports/taxonomy/

  `qiime tools import
  --input-path SILVA_132_SSURef_Nr99_tax_silva_full_align_trunc.fasta
  --type FeatureData[AlignedSequence]
  --input-format AlignedRNAFASTAFormat
  --output-path SILVA_132_SSURef_Nr99_tax_silva_full_align_trunc.qza`

  `qiime tools import
  --input-path tax_slv_ssu_132.txt
  --type SilvaTaxonomy
  --output-path tax_slv_ssu_132.qza
  --input-format SilvaTaxonomyFormat`

  `qiime tools import
  --input-path tax_slv_ssu_132.acc_taxid
  --type SilvaAccession
  --output-path tax_slv_ssu_132.acc_taxid.qza
  --input-format SilvaAccessionFormat`

  `qiime ghost-tree extract-fungi
  --i-aligned-silva-file SILVA_132_SSURef_Nr99_tax_silva_full_align_trunc.qza
  --i-accession-file tax_slv_ssu_132.acc_taxid.qza
  --i-taxonomy-file tax_slv_ssu_132.qza
  --o-aligned-seqs silva_fungi_only_full_aligned_132.qza`

  To import UNITE databases, use these links and follow the import
  instructions in the *small test files* section above.