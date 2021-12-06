# -*- coding: utf-8 -*-

import os
import json

from pymatgen.core.structure import Structure

from simmate.workflow_engine.error_handler import ErrorHandler
from simmate.calculators.vasp.inputs.incar import Incar


class RealOptlay(ErrorHandler):
    """
    This handler addresses a series of warning messages that each have the same
    attempted fixes. Note that this affect how we handle correcting the error!

    NOTE: I call this RealOptlay but don't have a good understanding of what
    the error exactly is. This is simply a conversion from Custodian of the
    following errors: ["rspher", "real_optlay", "nicht_konv"]
    """

    # run this while the VASP calculation is still going
    is_monitor = True

    # we assume that we are checking the vasp.out file
    filename_to_check = "vasp.out"

    # These are the error messages that we are looking for in the file
    possible_error_messages = [
        "ERROR RSPHER",
        "REAL_OPTLAY: internal error",
        "REAL_OPT: internal ERROR",
        "ERROR: SBESSELITER : nicht konvergent",
    ]

    # Number of atoms in a lattice to consider this a large cell. This affects
    # how we treat the error and correct it.
    natoms_large_cell = 100

    def correct(self, directory):

        # load the INCAR file to view the current settings
        incar_filename = os.path.join(directory, "INCAR")
        incar = Incar.from_file(incar_filename)

        # load the error-count file if it exists
        error_count_filename = os.path.join(directory, "simmate_error_counts.json")
        if os.path.exists(error_count_filename):
            with open(error_count_filename) as error_count_file:
                error_counts = json.load(error_count_file)
        # otherwise we are starting with an empty dictionary
        else:
            error_counts = {}

        # The fix is based on the number of times we've already tried to
        # fix this. So let's make sure it's in our error_count dictionary.
        # If it isn't there yet, set the count to 0 and we'll update it below.
        error_counts["real_optlay"] = error_counts.get("real_optlay", 0)

        poscar_filename = os.path.join(directory, "POSCAR")
        structure = Structure.from_file(poscar_filename)

        if structure.num_sites < self.natoms_large_cell:
            incar["LREAL"] = False
            correction = "set LREAL to False"

        else:
            # for large supercell, try an in-between option LREAL = True
            # prior to LREAL = False
            if error_counts["real_optlay"] == 0:
                # use real space projectors generated by pot
                incar["LREAL"] = True
                correction = "set LREAL to True"
            elif error_counts["real_optlay"] == 1:
                incar["LREAL"] = False
                correction = "set LREAL to False"
            # increase our attempt count
            error_counts["real_optlay"] += 1

        # rewrite the INCAR with new settings
        incar.to_file(incar_filename)

        # rewrite the new error count file
        with open(error_count_filename, "w") as file:
            json.dump(error_counts, file)

        # now return the correction made for logging
        return correction
