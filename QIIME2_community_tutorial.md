# *q2-ghost-tree* is a plugin for creating hybrid trees within the QIIME 2 environment.

*ghost-tree* is a bioinformatics tool that combines sequence data from two
genetic marker databases into one hybrid phylogenetic tree (a ghost tree, not
hyphenated and not italicized) that can be used for diversity analyses. One
database is used as a "foundation tree" because it better describes genetic
relationships across all phyla, and the other database (the "extensions" or
tips of the tree) provides finer taxonomic resolution.

The most popular application of this method is for fungal microbiome analysis
using ITS sequences which provide great species identification, but make poor
quality multiple sequence aligments and subsequently poor phylogenetic trees.

Here is an example of results you can achieve with ghost-tree:

Saliva (blue) and restroom (red) ITS sequences compared using
binary jaccard, unweighted UniFrac with Muscle aligned ITS sequences,
and unweighted UniFrac with a *ghost-tree* tree.


*If you are doing 16S microbiome analysis or analysis using a marker-gene region
that makes good quality trees, then you likely do not need to proceed with
this tutorial.*


## You can use ghost-tree in **two** ways:

1)  Use pre-built ghost trees to analyze your data **without** installing
*q2-ghost-tree*. See options below.

2) Install and use the *q2-ghost-tree* plugin
    - This has more features including the ability to graft at different levels
    (i.e. phylum, class, order, family). Default is genus.

## 1) To use pre-built ghost trees for fungal ITS amplicon sequence analysis in QIIME 2 (*most popular*)

### In addition to your own sequences, you will need:

1) a ghost tree built using the same UNITE database you use for closed-reference clustering.

2) a UNITE ITS database and

### Import your ghost tree into QIIME 2 as a .qza file:

#### Find the ghost tree you need

You can use one of the [pre-built
ghost trees found here](https://github.com/JTFouquier/ghost-tree-trees)
(for older trees, look
[here](https://github.com/JTFouquier/ghost-tree/tree/master/trees)), because
you really just need the "extension" IDs in the tree to match the IDs inside
your feature table .qza file (.biom table).

These were recently added to a new repository (*ghost-tree-trees*) so that a
clone of the *ghost-tree* or *q2-ghost-tree* does not fill your computer with
unnecessary large files.

Find the ghost tree which corresponds to the UNITE ITS DB you are using.


#### Import the ghost tree

Note, the ghost trees *are already* rooted by midpoint from *ghost-tree*, but
apparently there's additional magic in QIIME 2. :) So we quickly import as
"Unrooted" and then root it again.

`qiime tools import --input-path ghost_tree.nwk --type Phylogeny[Unrooted]
--output-path ghost-tree-unrooted.qza`

#### Root your ghost tree by midpoint in QIIME 2

`qiime phylogeny midpoint-root --i-tree ghost-tree-unrooted.qza
--o-rooted-tree ghost-tree-midpoint-root.qza`

### Import the UNITE database you wish to use for clustering into QIIME 2:

#### Find the appropriate UNITE ITS database

You can find [the UNITE ITS databases here](https://unite.ut.ee/repository.php).
Select the one appropriate for your analysis and import it as a QIIME 2 type.

This will be the database you use to cluster your sequences against.

`qiime tools import --type FeatureData[Sequence] --input-path
sh_refs_qiime.fasta --output-path
sh_refs_qiime.qza`

### Recluster your high quality amplicon sequence variants (ASVs) using the vsearch plugin

ASVs (your representative sequences) of type `FeatureData[Sequence]` come
from [Dada2](https://docs.qiime2.org/2018.6/plugins/available/dada2/) or
[Deblur](https://docs.qiime2.org/2018.6/plugins/available/deblur/).

Once you have these sequences, you will need to cluster them using `qiime
vsearch`. This is necessary because the tips of the tree must match your
feature table for `qiime diversity` phylogenetic analyses to work. Hash values
will not work for default ghost trees.


[See directions here for otu clustering](https://docs.qiime2.org/2018.6/tutorials/otu-clustering/)
to dereplicate sequences. Briefly, you will:
1) Use the `qiime vsearch dereplicate-sequences` command.
2) Then cluster your seqs with the UNITE database you selected using
`qiime vsearch cluster-features-closed-reference`.


### Now you have a feature table with IDs that match the pre-built ghost tree!

The tips of the tree match your feature table because you selected the
corresponding databases earlier. You performed closed-reference
clustering with the same databse that was used to build an ITS - 18S
ghost tree.

You can use the feature table and the ghost tree (your phylogenetic tree) for
phylogenetic `qiime diversity` commands.


## Using q2-ghost-tree to create your own hybrid tree

For custom trees, regions other than ITS, or different graft levels, you
will need to experiment.

TODO See other readme.

## ~Examples~ of some related QIIME 1 -> QIIME 2 imports (creating a .qza)

For more information see the
[QIIME 2 docs on importing data](https://docs.qiime2.org/2018.6/tutorials/importing/#importing-seqs).

#### Import a seqs.fna file:
`qiime tools import --type FeatureData[Sequence] --input-path seqs.fna
--output-path seqs.qza`

#### Import a UNITE ITS sequence database:

`qiime tools import --type FeatureData[Sequence] --input-path
sh_refs_qiime_ver7_dynamic_01.12.2017.fasta --output-path
sh_refs_qiime_ver7_dynamic_01.12.2017.qza `

#### Import a Biom table:

`qiime tools import --input-path otu_table.biom --type FeatureTable[Frequency]
--output-path feature_table.qza --source-format BIOMV100Format`

--source-format will be one of several formats



