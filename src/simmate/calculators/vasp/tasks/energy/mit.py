# -*- coding: utf-8 -*-

from simmate.calculators.vasp.tasks.relaxation.mit import MITRelaxation

from simmate.calculators.vasp.error_handlers.all import (
    TetrahedronMesh,
    Eddrmm,
    NonConvergingErrorHandler,
)


class MITStaticEnergy(MITRelaxation):

    # The settings used for this calculation are based on the MITRelaxation, but
    # we are updating/adding new settings here.
    # !!! we hardcode temperatures and time steps here, but may take these as inputs
    # in the future
    incar = MITRelaxation.incar.copy()
    incar.update(
        dict(
            ALGO="Normal",
            IBRION=-1,  # (optional) locks everything between ionic steps
            NSW=0,  # this is the main static energy setting
            ISMEAR=-5,  # was -5 for non-metals and 2 for metals
            SIGMA=0.05,  # was -0.05 for non-metals and 0.2 for metals
            KSPACING=0.4,  # was 0.5 # !!! This is where we are different from pymatgen right now
        )
    )
    # We set ISMEAR=0 and SIGMA above, so we no longer need smart_ismear
    incar.pop("multiple_keywords__smart_ismear")

    # We reduce the number of error handlers used on dynamics because many
    # error handlers are based on finding the global minimum & converging, which
    # not what we're doing with dynmaics
    error_handlers = [
        TetrahedronMesh(),
        Eddrmm(),
        NonConvergingErrorHandler(),
    ]
