from pathlib import Path
import os

os.chdir(str((Path(__file__).resolve()).parent.parent))

import main

from util.plot_ipd import plot_iterated_prisoners_dilemma, plot_ipd_from_file
from fitness.game_theory_game import PrisonersDilemma
from typing import List, Tuple

# Set to use the configuration file and output directory
args = ["-o", "tmp", "-f", "tests/configurations/lark_new_yaml/iterated_prisoners_dilemma_lark.yml"]
provisional = main.main(args)
