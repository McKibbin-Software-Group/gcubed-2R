"""
Simulation experiment
"""

import os
import pickle
import logging
import gcubed
import gcubed.projections
from gcubed.model import Model
from gcubed.projections.baseline_projections import BaselineProjections
from gcubed.projections.projections import Projections
from gcubed.linearisation.solved_model import SolvedModel
from gcubed.runners.simulation_runner import SimulationRunner
from model_constants import (
    CONFIGURATION,
    EXPERIMENT_RESULTS_FOLDER,
    EXPERIMENT_6 as EXPERIMENT,
)

# Determine where the results will be saved.
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

# Load the previously saved baseline projections, if they exist.
baseline_projections_pickle_file: str = os.path.join(
    results_folder, "baseline_projections.pickle"
)
if os.path.exists(baseline_projections_pickle_file):
    logging.info(
        f"Loading previously generated baseline projections from {baseline_projections_pickle_file}"
    )
    with open(baseline_projections_pickle_file, "rb") as file:
        baseline_projections: BaselineProjections = pickle.load(file)


# Solve the model and regenerate the baseline if not already done.
if not (
    "baseline_projections" in globals()
    and isinstance(baseline_projections, BaselineProjections)
):
    # Load or create the solved model first
    solved_model_pickle_file: str = os.path.join(results_folder, "solved_model.pickle")
    if os.path.exists(solved_model_pickle_file):
        logging.info(f"Loading previously solved model from {solved_model_pickle_file}")
        with open(solved_model_pickle_file, "rb") as file:
            solved_model: SolvedModel = pickle.load(file)

    if not ("solved_model" in globals() and isinstance(solved_model, SolvedModel)):
        model: Model = Model(configuration=CONFIGURATION)
        solved_model: SolvedModel = SolvedModel(model=model)
        with open(solved_model_pickle_file, "wb") as file:
            pickle.dump(solved_model, file)
        logging.info(f"Saved the solved model for later reuse.")

    baseline_projections: BaselineProjections = BaselineProjections(
        solved_model=solved_model
    )
    with open(baseline_projections_pickle_file, "wb") as file:
        pickle.dump(baseline_projections, file)
    logging.info(f"Saved the baseline projections for later reuse.")


# Set up the simulation runner.
runner: SimulationRunner = SimulationRunner(
    baseline_projections=baseline_projections,
    experiment_design_file=EXPERIMENT,
)

# Run the simulation experiment.
runner.run()

# Save the raw baseline projections
baseline_projections: Projections = runner.baseline_projections
baseline_projections.charting_projections.to_csv(
    os.path.join(
        results_folder,
        f"{baseline_projections.name}.csv",
    )
)

# Save final projections
final_projections: Projections = runner.final_projections
final_projections.charting_projections.to_csv(
    os.path.join(
        results_folder,
        f"{final_projections.name}.csv",
    )
)

# Calculate the deviations
deviations = gcubed.projections.deviations(
    new_projections=final_projections,
    original_projections=baseline_projections,
)
deviations.to_csv(
    os.path.join(
        results_folder,
        f"deviations of {final_projections.name} from {baseline_projections.name}.csv",
    )
)
