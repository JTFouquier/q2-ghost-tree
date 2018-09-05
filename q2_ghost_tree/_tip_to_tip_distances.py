
from ghosttree.util import compare_tip_to_tip_distances

from q2_types.tree import NewickFormat

import pandas as pd
import os

_ghost_tree_defaults = {'method': 'pearson'}


def tip_to_tip_distances(output_dir: str, tree_1: NewickFormat,
                         tree_2: NewickFormat,
                         method: str=_ghost_tree_defaults['method']):

    tree1_fh = tree_1.open()
    tree2_fh = tree_2.open()

    stats_results = compare_tip_to_tip_distances(
        tree1_fh, tree2_fh, method)

    data_dict = {
        'Correlation Coefficient': str(round(stats_results[0], 5)),
        'p-value': str(stats_results[1]),
        'Number of Overlapping Tips': str(stats_results[2]),
    }

    df = pd.Series(data=data_dict).to_frame()
    df.columns = ['Tree Comparison Statistics']

    index = os.path.join(output_dir, 'index.html')
    with open(index, 'w') as fh:
        fh.write(df.to_html())
