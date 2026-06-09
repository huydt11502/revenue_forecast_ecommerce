from pathlib import Path
import matplotlib.pyplot as plt

ROOT_DIR = Path.cwd().parent
BASE_FIG_DIR = ROOT_DIR / 'outputs' / 'figures'

_counter = {}

def save_fig(name, *folders, dpi=300):
    fig_dir = BASE_FIG_DIR.joinpath(*folders)
    fig_dir.mkdir(parents=True, exist_ok=True)

    key = "/".join(folders)
    _counter[key] = _counter.get(key, 0) + 1

    filename = f"{_counter[key]:02d}_{name}.png"

    plt.savefig(
        fig_dir / filename,
        dpi=dpi,
        bbox_inches='tight'
    )

def save_master(name):
    save_fig(name, 'eda', 'master')

def save_operations(name):
    save_fig(name, 'eda', 'operations')

def save_business(name):
    save_fig(name, 'business')