# q2-ghost-tree installation and testing instructions

This is a QIIME 2 plugin for 'ghost-tree: creating hybrid-gene phylogenetic
trees for diversity analysis.' The original ghost-tree repository can be found
[here](https://github.com/JTFouquier/ghost-tree), and the paper can be found
[here](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-016-0153-6).

This README is **NOT** the standard QIIME 2 plugin documentation. It is
written to guide developers on how to install and test ghost-tree prior to
officially releasing it for QIIME 2 use as this is my first time developing
a plugin! :)

To use and test this plugin you will need to work in command line
and follow these instructions:

1)  Install the current version of QIIME 2 and activate it following the
    [directions on the QIIME 2 website](https://docs.qiime2.org/2018.4/install/). 

    Make sure you are now working inside the QIIME 2 virtual environment.
    The command prompt should include something like '(qiime2-2018.6)' with
    the current version of QIIME 2. You want to be working from within the 
    QIIME 2 environment when you install the rest of the code.

2)  Clone and install original ghost-tree:

    `git clone https://github.com/JTFouquier/ghost-tree.git`

    Then, make sure you install ghost-tree from withinusing:
    `pip install -e .`

    Typing ghost-tree should bring up some help documentation about ghost-tree.
    If you do not see the help docs, something went wrong.

    The reason you first install ghost-tree in addition to the plugin code
    is because by nature the QIIME 2 plugin will access the original ghost-tree
    code so that you do not have to rewrite all the code inside your new
    plugin. The plugin just reuses most of the original code. Very convenient!

3)  ghost-tree has three software dependencies it relies on. You will need to
    install these tools.

    1)  fasttree:
        
        This is already installed in QIIME 2! If you were using
        ghost-tree standalone, you would need to install this, but because
        you installed QIIME 2, it comes with it.

        `conda install fasttree -c bioconda
        
    2)  sumaclust:

        sumaclust is now on Bioconda!
        `conda install -c bioconda sumaclust` will install it for you
        inside your QIIME 2 environment.

    3)  muscle:
        `conda install muscle -c bioconda` should quickly install muscle.

    To make sure these tools are correctly installed, you will test by
    typing their name and making sure you see something indicating it is
    installed.

4)  Next, you will install the *q2-ghost-tree* plugin with the command:

    `git clone https://github.com/JTFouquier/q2-ghost-tree.git`

    Find the setup.py file by navigating to the appropriate directory
    on the command line and do `pip install -e .` in the same way you
    did with the original ghost-tree tool.

    This should install the plugin! To make sure that QIIME 2 recognizes the
    plugin, you should enter `qiime dev refresh-cache` This basically
    refreshes the QIIME 2 environment and allows it to look for the entry
    points that were created in the q2-ghost-tree plugin. These entry points
    just tell QIIME 2 that a new plugin exists, and that is ready to use in 
    QIIME 2.

    When you type `qiime` you should now see ghost-tree as an available plugin.

5) Importing files as QIIME 2 data types:

    Test that you can import the files in the
    [small_test_files directory](https://github.com/JTFouquier/q2-ghost-tree/tree/master/small_test_files/original-non-qiime-files)

    a) Extension sequences:

    `qiime tools import --input-path
    original-non-qiime-files/extension_seqs.fasta --type
    FeatureData[Sequence] --output-path extension_seqs.qza`

    b) Extension taxonomy:

    `qiime tools import --input-path
    original-non-qiime-files/minitaxonomy.txt --type
    FeatureData[Taxonomy] --output-path minitaxonomy.qza
    --source-format HeaderlessTSVTaxonomyFormat`

    c) Extension OTUs

    `qiime tools import --input-path
    original-non-qiime-files/miniotus.txt --type OtuMap
    --output-path miniotus.qza`

    d) Foundation sequences:

    `qiime tools import --input-path
    original-non-qiime-files/foundation_seqs.fasta --type
    FeatureData[Sequence] --output-path foundation_seqs.qza`

    e) Foundation tree:

    `qiime tools import --input-path
    original-non-qiime-files/foundation_tree.nwk --type
    Phylogeny[Rooted] --output-path foundation_tree.qza`


6) Testing each subcommand in `qiime ghost-tree` (note extract fungi is
currently unavailable)

    a) Group your rep seqs at 90% similarity. This handles the
    abundant unidentified organisms.

    `qiime ghost-tree extensions-cluster --i-extension-sequences
    extension_seqs.qza --p-similarity-threshold 0.90 --o-otu-map
    extensions_otu_map_90.qza`

    b) Create a ghost tree using a foundation .nwk tree.

    `qiime ghost-tree scaffold-hybrid-tree-foundation-tree
    --i-otu-map extensions_otu_map_90.qza --i-extension-taxonomy
    minitaxonomy.qza --i-extension-sequences extension_seqs.qza
    --i-foundation-tree foundation_tree.qza --i-foundation-taxonomy
    minitaxonomy_foundation.qza --o-ghost-tree
    ghost-tree-foundation-tree-90-otus.qza`

    c) Create a ghost tree using a foundation .nwk tree, and using
    class level graft points instead of default genus.

    `qiime ghost-tree scaffold-hybrid-tree-foundation-tree
    --i-otu-map extensions_otu_map_90.qza --i-extension-taxonomy
    minitaxonomy.qza --i-extension-sequences extension_seqs.qza
    --i-foundation-tree foundation_tree.qza --i-foundation-taxonomy
    minitaxonomy_foundation.qza --o-ghost-tree
    ghost-tree-foundation-tree-90-otus-class-level-graft-points.qza
    --p-graft-level c`

    d) Create a ghost tree using aligned sequences instead of a tree as
    your foundation.

    Coming soon. Need to work on transformer :)