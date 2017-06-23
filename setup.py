from setuptools import setup, find_packages
import re
import ast

# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('q2_ghost_tree/__init__.py', 'rb') as f:
    hit = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(hit))

setup(
    name="q2-ghost-tree",
    version=version,
    packages=find_packages(),
    # pandas, q2templates and q2-dummy-types are only required for the dummy
    # methods and visualizers provided as examples. Remove these dependencies
    # when you're ready to develop your plugin, and add your own dependencies
    # (if there are any).
    install_requires=['pandas', 'q2templates >= 0.0.6'],
    author="Jennifer Fouquier",
    author_email="jennietf@gmail.com",
    description="Tool for creating hybrid-gene phylogenetic trees",
    entry_points={
        "qiime2.plugins":
        ["q2-ghost-tree=q2_ghost_tree.plugin_setup:plugin"]
    },
)
