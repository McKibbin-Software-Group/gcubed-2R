"""
This module contains model specific constants.
"""

import os
import logging
import numpy as np
from gcubed.model_configuration import ModelConfiguration

PYTHON_FOLDER: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
MODEL_FOLDER: str = os.path.abspath(os.path.join(PYTHON_FOLDER, os.pardir))
ROOT_RESULTS_FOLDER: str = os.path.abspath(
    os.path.join(MODEL_FOLDER, os.pardir, os.pardir, "results")
)

# --------------------------------------------------------------------------------------------
# Changes are unlikely to be required before this line.
# --------------------------------------------------------------------------------------------

# Specify the name of the model configuration file (in the model root folder)
CONFIGURATION_FILE: str = os.path.join(MODEL_FOLDER, "configuration2R179.csv")

EXPERIMENT_1: str = "experiment_1/design.csv"

EXPERIMENT_2: str = "experiment_2/design.csv"

EXPERIMENT_3: str = "experiment_3/design.csv"

EXPERIMENT_4_A: str = "experiment_4/design_A.csv"
EXPERIMENT_4_B: str = "experiment_4/design_B.csv"

EXPERIMENT_5: str = "experiment_5/design.csv"

EXPERIMENT_6: str = "experiment_6/design.csv"

# Midterm essay experiments

EXPERIMENT_FISCAL_USA_1: str = "experiment_Fiscal_USA_1/design.csv"
EXPERIMENT_FISCAL_USA_2: str = "experiment_Fiscal_USA_2/design.csv"
EXPERIMENT_FISCAL_GLOBAL_1: str = "experiment_Fiscal_Global_1/design.csv"

# --------------------------------------------------------------------------------------------
# Changes are unlikely to be required after this line.
# --------------------------------------------------------------------------------------------

CONFIGURATION: ModelConfiguration = ModelConfiguration(
    configuration_file=CONFIGURATION_FILE,
)


def CONFIGURE_LOGGING(folder: str):
    """

    ### Overview

    Configure the logging system.

    ### Arguments

    - `folder`: The folder where logs will be saved.

    """

    # Configure logging of numeric values
    np.set_printoptions(suppress=True, linewidth=10000)
    np.set_printoptions(formatter={"float": lambda x: "{0:0.6f}".format(x)})

    # Configure the logging system
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - Line:%(lineno)d - %(message)s"
    )
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logging.getLogger().addHandler(stream_handler)
    log_file: str = os.path.join(folder, "run.log")
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    logging.info(f"Saving results and logs to {folder}.")


def EXPERIMENT_RESULTS_FOLDER(experiment_script_name: str) -> str:
    """
    ### Overview

    Create a sub-folder of the root results folder to contain the results of an experiment.

    ### Arguments

    - `experiment_script_name`: The name of the script used to run the experiment.

    ### Returns

    - The path to the folder where the results of the experiment will be saved.

    ### Exceptions

    - The experiment script name must end with '.py'.

    - The experiment results folder must be created before the function ends.

    """

    assert experiment_script_name.endswith(
        ".py"
    ), "The experiment script name must end with '.py'."

    experiment_results_folder: str = os.path.join(
        ROOT_RESULTS_FOLDER,
        CONFIGURATION.version,
        CONFIGURATION.build,
        f"{os.path.splitext(experiment_script_name)[0]}",
    )
    if not os.path.exists(experiment_results_folder):
        os.makedirs(experiment_results_folder)

    CONFIGURE_LOGGING(folder=experiment_results_folder)

    return experiment_results_folder
