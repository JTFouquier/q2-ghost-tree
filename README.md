# q2-ghost-tree

This is a QIIME 2 plugin for 'ghost-tree: creating hybrid-gene phylogenetic
trees for diversity analysis.' The original ghost-tree repository can be found
[here](https://github.com/JTFouquier/ghost-tree), and the paper can be found
[here](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-016-0153-6).

This README is **NOT** the standard QIIME 2 plugin documentation. It is
written to guide developers on how to install and test ghost-tree prior to
officially releasing it for QIIME 2 use as this is my first time developing
a plugin! :)

To use and test this plugin you will need to work in command line and follow
these instructions:

1)  Install the current version of QIIME 2 and activate it following the
    [directions on the QIIME 2 website](https://docs.qiime2.org/2018.4/install/). 

    Make sure you are now working inside the QIIME 2 virtual environment.
    The command prompt should include something like '(qiime2-2018.4)' with
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
        
    2)  sumaclust: 
        
        See [the install directions](https://git.metabarcoding.org/obitools/sumaclust/wikis/home).
        This install can be challenging, and in the future I plan to get this 
        put into conda so it can be more quickly installed. For now, this
        is the way we do it.

    3)  muscle:
        `conda install -c bioconda muscle` should quickly install muscle.

    To make sure these tools are correctly installed, you will test by
    typing their name and making sure you see something indicating it is
    installed.

4)  Next, you will install the q2-ghost-tree plugin with the command:

    `git clone https://github.com/JTFouquier/q2-ghost-tree.git`

    This will install the plugin! To make sure that QIIME 2 recognizes the
    plugin, you should enter `qiime dev refresh-cache` This basically
    refreshes the QIIME 2 environment and allows it to look for the entry
    points that were created in the q2-ghost-tree plugin. These entry points
    just tell QIIME 2 that a new plugin exists, and that is ready to use in 
    QIIME 2.

    When you type `qiime` you should now see ghost-tree as an available plugin.

5) Importing files: TODO (test imports)

6) Testing: 
    
   






