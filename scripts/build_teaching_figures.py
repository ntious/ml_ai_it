"""Original explanatory figures from the explicitly authored hand examples.

These values are not measured model performance. Each lesson supplies the same
numbers in a readable table. No external figures or course text are copied.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'docs/assets/teaching'


def build():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.size': 12, 'svg.fonttype': 'none', 'svg.hashsalt': 'applied-ml-teaching',
                         'axes.spines.top': False, 'axes.spines.right': False})
    figures = []
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    ax.plot([1, 2], [110, 125], 'o', color='#303030', label='Actual')
    ax.plot([1, 2], [100, 140], 's', markerfacecolor='white', color='#17658b', label='Prediction')
    for x, actual, predicted in [(1, 110, 100), (2, 125, 140)]:
        ax.plot([x, x], [actual, predicted], ':', color='#a65c00')
        ax.text(x + .07, (actual + predicted) / 2, f'Residual {actual-predicted:+d}', va='center')
    ax.set(xlim=(.65, 2.8), ylim=(0, 160), xticks=[1, 2], xticklabels=['Example 1', 'Example 2'],
           ylabel='Count units', title='Authored examples: signed errors can cancel')
    ax.legend(loc='upper left'); figures.append(('regression-residuals', fig))
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    x = np.arange(3)
    ax.bar(x-.18, [0, 1, 1], width=.36, color='#17658b', label='Missed positives (FN)')
    ax.bar(x+.18, [1, 1, 0], width=.36, color='#a65c00', hatch='//', label='False alarms (FP)')
    ax.set(xticks=x, xticklabels=['0.3', '0.5', '0.7'], yticks=[0, 1, 2], ylim=(0, 2.1),
           xlabel='Decision threshold', ylabel='Number of records (4 authored cases)', title='A threshold changes the errors, not the fitted scores')
    ax.legend(); figures.append(('classification-thresholds', fig))
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    ax.plot([1, 2, 3, 4], [.65, .5, .38, .3], 'o-', color='#17658b', label='Training loss')
    ax.plot([1, 2, 3, 4], [.69, .51, .48, .55], 's--', color='#a65c00', label='Validation loss')
    ax.axvline(3, color='#303030', linestyle=':', label='Selected epoch 3')
    ax.set(xticks=[1, 2, 3, 4], ylim=(0, .85), xlabel='Epoch', ylabel='Illustrative binary cross-entropy',
           title='Authored loss history: select using validation')
    ax.legend(loc='lower left'); figures.append(('neural-checkpoint', fig))
    for name, fig in figures:
        fig.savefig(DESTINATION / (name+'.svg'), metadata={'Date': None})
        source = DESTINATION / (name+'.svg')
        source.write_text('\n'.join(line.rstrip() for line in source.read_text().splitlines()) + '\n')
        # Local review PNGs are generated evidence, not additional source assets.
        evidence = ROOT / 'runs/teaching-review'; evidence.mkdir(parents=True, exist_ok=True)
        fig.savefig(evidence / (name+'.png'), dpi=140)
        plt.close(fig)
    print('Built three original teaching figures and PNG review copies; lesson tables retain the exact values.')


if __name__ == '__main__':
    build()
