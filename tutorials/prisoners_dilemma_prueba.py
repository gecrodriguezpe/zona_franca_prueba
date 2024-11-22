from pathlib import Path
import os

os.chdir(str((Path(__file__).resolve()).parent.parent))

import main

from util.plot_ipd import plot_iterated_prisoners_dilemma, plot_ipd_from_file
from fitness.game_theory_game import PrisonersDilemma
from typing import List, Tuple


'''
# Strategy for always cooperate
player_1 = lambda h, i: "C"
# Strategy for cooperate if opponent cooperated previous turn
player_2 = lambda h, i: "C" if h[i] == "C" else "D"
n_iterations = 5
memory_size = 1
# Setup a prisoners dilemma engagment
pd = PrisonersDilemma(n_iterations=n_iterations, memory_size=memory_size, store_stats=True, out_file_name=PrisonersDilemma.DEFAULT_OUT_FILE)
# Run the strategies against each other
sentences, histories = pd.run(player_1=player_1, player_2=player_2)
# Plot the choices and the payoffs from the engagement
plot_iterated_prisoners_dilemma(sentences, pd.revise_history(histories), out_path='.')
'''


# Set to use the configuration file and output directory
args = ["-o", "tmp", "-f", "tests/configurations/iterated_prisoners_dilemma.yml"]
provisional = main.main(args)

