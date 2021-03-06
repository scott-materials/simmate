# -*- coding: utf-8 -*-

import os

from simmate.workflow_engine.error_handler import ErrorHandler
from simmate.calculators.vasp.inputs.incar import Incar


class Eddrmm(ErrorHandler):
    """
    ???
    """

    # run this while the VASP calculation is still going
    is_monitor = True

    # we assume that we are checking the vasp.out file
    filename_to_check = "vasp.out"

    # These are the error messages that we are looking for in the file
    possible_error_messages = ["WARNING in EDDRMM: call to ZHEGV failed"]

    def correct(self, directory):

        # load the INCAR file to view the current settings
        incar_filename = os.path.join(directory, "INCAR")
        incar = Incar.from_file(incar_filename)

        # RMM algorithm is not stable for this calculation
        if incar.get("ALGO", "Normal") in ["Fast", "VeryFast"]:
            incar["ALGO"] = "Normal"
            correction = "switched ALGO to Normal"
        else:
            # Halve the POTIM
            current_potim = incar.get("POTIM", 0.5)
            new_potim = current_potim / 2
            incar["POTIM"] = new_potim
            correction = f"switch POTIM from {current_potim} to {new_potim}"

        # Check the current ICHARG setting, where default is 0
        # If the ICHARG is less than 10, then we want to delete the CHGCAR
        # and WAVECAR to ensure the next run is a clean start.
        current_icharg = incar.get("ICHARG", 0)
        if current_icharg < 10:
            os.remove(os.path.join(directory, "CHGCAR"))
            os.remove(os.path.join(directory, "WAVECAR"))
            correction += " and deleted CHGCAR + WAVECAR"

        # rewrite the INCAR with new settings
        incar.to_file(incar_filename)

        return correction
