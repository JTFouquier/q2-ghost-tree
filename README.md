# *q2-ghost-tree* is a plugin for creating hybrid trees within the QIIME 2 environment

*ghost-tree* is a bioinformatics tool that combines sequence data from
two genetic marker databases into one hybrid phylogenetic tree that can
be used for diversity analyses. One database is used as a "foundation
tree" because it better describes genetic relationships across all
phyla, and the other database (the "extensions" or tips of the tree)
provides finer taxonomic resolution.

The most popular application of this method is for fungal microbiome
analysis using ITS sequences which provide great species identification,
but make poor quality multiple sequence aligments (MSAs) and
subsequently poor phylogenetic trees.

Here is an example of results you can achieve with ghost-tree:

![](https://github.com/JTFouquier/q2-ghost-tree/blob/master/images/Picture1.png)

Fig 1. Saliva (blue) and restroom (red) ITS sequences compared using
A) binary jaccard, B) unweighted UniFrac with Muscle aligned ITS sequences,
and C) unweighted UniFrac with a *ghost-tree* produced tree.

This is a QIIME 2 plugin. The original *ghost-tree* repository can be found
[here](https://github.com/JTFouquier/ghost-tree), and the paper can be found
[here](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-016-0153-6).

## You can use *ghost-tree* in **two** ways:

Expanded examples and directions follow.

### METHOD 1: Use a pre-built ghost tree for analysis (recommended if pre-built tree is available)

#### OR

### METHOD 2: Install and use the *q2-ghost-tree* plugin
- This has more features including the ability to graft at different levels
(i.e. phylum, class, order, family). Default is genus.

## METHOD 1: Use a pre-built ghost tree for analysis

### In addition to your own sequences or feature table with accession IDs, you will need:

1) a ghost tree built using the same database you use for closed-reference clustering (i.e., UNITE for ITS seqs)

2) a database related to your region of interest (i.e., UNITE for ITS seqs)

### Import your ghost tree into QIIME 2 as a .qza file:

#### Find the ghost tree you need for your ITS sequences

You can use one of the newer [pre-built
ghost trees found here](https://github.com/JTFouquier/ghost-tree-trees)
(for older trees, look
[here](https://github.com/JTFouquier/ghost-tree/tree/master/trees)), because
you really just need the "extension IDs" in the tree to match the IDs inside
your feature table .qza file. Find the ghost tree which corresponds to
the accession IDs in the database you are using.

You can also use a ghost tree that you built using the plugin.



#### Import the ghost tree you would like to use

Note, the ghost trees *are already* rooted by midpoint from
*ghost-tree*, but apparently there's additional magic in QIIME 2. :) So
we quickly import as "Unrooted" and then root it again.

```sh
qiime tools import \
--input-path ghost_tree.nwk \
--type Phylogeny[Unrooted] \
--output-path ghost-tree-unrooted.qza
```

#### Root your ghost tree by midpoint in QIIME 2

```sh
qiime phylogeny midpoint-root \
--i-tree ghost-tree-unrooted.qza \
--o-rooted-tree ghost-tree-midpoint-root.qza
```

### Import the UNITE database you wish to use for clustering your sequences in QIIME 2:

You can find [the UNITE ITS databases here](https://unite.ut.ee/repository.php).
Select the one appropriate for your analysis and import it as a QIIME 2 type.

This will be the database you use to cluster your sequences against.

```sh
qiime tools import \
--type FeatureData[Sequence] \
--input-path sh_refs_qiime.fasta \
--output-path sh_refs_qiime.qza
```

### Recluster your high quality amplicon sequence variants (ASVs) using the vsearch plugin

ASVs (your high quality representative sequences) of type
`FeatureData[Sequence]` come from
[Dada2](https://docs.qiime2.org/2018.6/plugins/available/dada2/) or
[Deblur](https://docs.qiime2.org/2018.6/plugins/available/deblur/).

Once you have these sequences, you will need to cluster them using
`qiime vsearch`. This is necessary because the IDs in the ghost tree
must match your feature table for `qiime diversity` phylogenetic
analyses to work. Hash values (common for ASVs) will *not* work here.

[See directions here for closed-reference otu clustering](https://docs.qiime2.org/2018.8/tutorials/otu-clustering/)
to dereplicate sequences. Briefly, you will:
1) Use the `qiime vsearch dereplicate-sequences` command.
2) Then cluster your seqs with the UNITE database you selected using
`qiime vsearch cluster-features-closed-reference`.

#### Now you have a feature table with IDs that match the pre-built ghost tree!

The tips of the tree match your feature table because you selected the
corresponding databases earlier. You performed closed-reference
clustering with the same database that was used to build an ITS+18S
ghost tree.

If you used a pre-built ghost tree, you just need to filter your feature
table to contain only IDs that match the ghost tree. There is a file
provided that you can use to filter your table.

You can then use the feature table and the ghost tree for
phylogenetic `qiime diversity` analysis.


## METHOD 2: plugin installation

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
    *ghost-tree*. If you do not see the help docs, something went wrong.

    *ghost-tree* has three software dependencies it relies on. These are
    Sumaclust, Muscle and FastTree. If you use Conda to install
    *ghost-tree*, it should have installed these for you!

3)  Next, you will install *q2-ghost-tree* plugin:

    You must have Git installed.

    `git clone https://github.com/JTFouquier/q2-ghost-tree.git`

    Find the setup.py file by navigating to the appropriate directory
    on the command line and enter `pip install -e .`

    When you type `qiime` you should now see *ghost-tree* as an available plugin.

    You can also type `qiime ghost-tree` to see the subcommands in *q2-ghost-tree*

    Typing `--help` will show you *ghost-tree* docs and subcommand docs.

## Importing small test files as QIIME 2 data types:

Test that you can import some test files in the
[small_test_files directory](https://github.com/JTFouquier/q2-ghost-tree/tree/master/small_test_files/original-non-qiime-files)

#### Extension sequences:

```sh
qiime tools import \
--input-path extension_seqs.fasta \
--type FeatureData[Sequence] \
--output-path extension_seqs.qza
```

#### Extension taxonomy:

```sh
qiime tools import \
--input-path minitaxonomy.txt \
--type FeatureData[Taxonomy] \
--input-format HeaderlessTSVTaxonomyFormat \
--output-path minitaxonomy.qza
```

#### Extension OTUs

```sh
qiime tools import \
--input-path miniotus.txt \
--type OtuMap \
--output-path miniotus.qza
```

#### Foundation sequences:

```sh
qiime tools import \
--input-path foundation_seqs.fasta \
--type FeatureData[Sequence] \
--output-path foundation_seqs.qza
```

#### Foundation tree:

```sh
qiime tools import \
--input-path foundation_tree.nwk \
--type Phylogeny[Rooted] \
--output-path foundation_tree.qza
```

#### Foundation taxonomy:

```sh
qiime tools import \
--input-path minitaxonomy_foundation.txt \
--type FeatureData[Taxonomy] \
--input-format HeaderlessTSVTaxonomyFormat \
--output-path minitaxonomy_foundation.qza
```

#### Foundation alignment:

This is pre filtered, and extracted to only contain fungi.

```sh
qiime tools import \
--input-path silva_fungi_only.txt \
--type FeatureData[AlignedSequence] \
--output-path silva_fungi_only.qza
```

## Testing subcommands in *q2-ghost-tree*

#### Group your rep seqs at 90% similarity.

This handles the abundant 'unidentified' organisms.

```sh
qiime ghost-tree extensions-cluster \
--i-extension-sequences extension_seqs.qza \
--p-similarity-threshold 0.90 \
--o-otu-map extensions_otu_map_90.qza
```

#### Create a ghost tree using a foundation .nwk tree

*Note the subcommand used is for a foundation TREE.*

```sh
qiime ghost-tree scaffold-hybrid-tree-foundation-tree \
--i-otu-map extensions_otu_map_90.qza \
--i-extension-taxonomy minitaxonomy.qza \
--i-extension-sequences extension_seqs.qza \
--i-foundation-tree foundation_tree.qza \
--i-foundation-taxonomy minitaxonomy_foundation.qza \
--o-ghost-tree ghost-tree-foundation-tree-90-otus.qza
```

#### Create a ghost tree using a foundation .nwk tree, and using *class*-level graft points instead of default *genus*.

```sh
qiime ghost-tree scaffold-hybrid-tree-foundation-tree \
--i-otu-map extensions_otu_map_90.qza \
--i-extension-taxonomy minitaxonomy.qza \
--i-extension-sequences extension_seqs.qza \
--i-foundation-tree foundation_tree.qza \
--i-foundation-taxonomy minitaxonomy_foundation.qza \
--o-ghost-tree ghost-tree-foundation-tree-90-otus-class-level-graft-points.qza \
--p-graft-level c
```

#### Create a ghost tree using aligned sequences instead of a tree as your foundation

*Note the subcommand used is for a foundation ALIGNMENT.*

```sh
qiime ghost-tree scaffold-hybrid-tree-foundation-alignment \
--i-otu-map extensions_otu_map_90.qza \
--i-extension-taxonomy minitaxonomy.qza \
--i-extension-sequences extension_seqs.qza \
--i-foundation-alignment silva_fungi_only.qza \
--o-ghost-tree ghost-tree-foundation-allignment-90-otus.qza
```

## Working with full size files

This walkthrough is specific to UNITE ITS and SILVA 18S trees for fungal
ITS analysis.

These are large and steps may take a few minutes to a few *hours*.

### SILVA (or the foundation)

Using the most recent release
[of SILVA](https://www.arb-silva.de/no_cache/download/archive/release_132/Exports/)

#### Import a SILVA DB and transform from RNA to DNA upon import

```sh
qiime tools import \
--input-path SILVA_132_SSURef_Nr99_tax_silva_full_align_trunc.fasta \
--type FeatureData[AlignedSequence] \
--input-format AlignedRNAFASTAFormat \
--output-path SILVA_132_SSURef_Nr99_tax_silva_full_align_trunc.qza
```

#### Silva Taxonomy File

```sh
qiime tools import \
--input-path tax_slv_ssu_132.txt \
--type SilvaTaxonomy \
--output-path tax_slv_ssu_132.qza \
--input-format SilvaTaxonomyFormat
```

#### Silva Accession ID Map

```sh
qiime tools import \
--input-path tax_slv_ssu_132.acc_taxid \
--type SilvaAccession \
--output-path tax_slv_ssu_132.acc_taxid.qza \
--input-format SilvaAccessionFormat
```

#### Extract fungi only from Silva

```sh
qiime ghost-tree extract-fungi \
--i-aligned-silva-file SILVA_132_SSURef_Nr99_tax_silva_full_align_trunc.qza \
--i-accession-file tax_slv_ssu_132.acc_taxid.qza \
--i-taxonomy-file tax_slv_ssu_132.qza \
--o-aligned-seqs silva_fungi_only_full_aligned_132.qza
```

#### Filter alignment positions

```sh
qiime ghost-tree filter-alignment-positions \
--i-aligned-sequences-file silva_fungi_only_full_aligned_132.qza \
--p-maximum-gap-frequency 0.9 \
--p-maximum-position-entropy 0.8 \
--o-aligned-seqs silva_fungi_only_full_aligned_132_FILTERED.qza
```

#### Import a UNITE ITS sequence database:

```sh
qiime tools import \
--input-path sh_refs_qiime_ver7_dynamic_01.12.2017.fasta \
--type FeatureData[Sequence] \
--output-path sh_refs_qiime_ver7_dynamic_01.12.2017.qza
```

## Making a ghost tree

With the small and large file examples above, you should now have
examples of most of the commands in *ghost-tree*. This
combined with reading the `--help` docs in *ghost-tree* should give you
enough information to make your own ghost tree.

After you get a ghost tree, see METHOD 1 for using ghost trees in your
analysis.

### Please don't hesitate to post on the QIIME 2 forum with questions.

## Examples of misc. imports

#### Import a seqs.fna file:
```sh
qiime tools import \
--type FeatureData[Sequence] \
--input-path seqs.fna \
--output-path seqs.qza
```

#### Import a Biom table:

```sh
qiime tools import \
--input-path otu_table.biom \
--type FeatureTable[Frequency] \
--output-path feature_table.qza \
--input-format BIOMV100Format
```


