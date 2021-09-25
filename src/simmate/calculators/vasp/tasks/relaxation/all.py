# -*- coding: utf-8 -*-

# This file sets up a shortcut for importing so that you can do...
#
#   from simmate.calculators.vasp.tasks.relaxation.all import (
#       Quality00RelaxationTask,
#       Quality01RelaxationTask,
#       Quality02RelaxationTask,
#       Quality03RelaxationTask,
#       Quality04RelaxationTask,
#       MITRelaxationTask,
#   )
#
# instead of what's written below. You should only use this shortcut if you are
# using ALL of the classes below or if you are running some quick interactive test.

from simmate.calculators.vasp.tasks.relaxation.quality_00 import Quality00RelaxationTask
from simmate.calculators.vasp.tasks.relaxation.quality_01 import Quality01RelaxationTask
from simmate.calculators.vasp.tasks.relaxation.quality_02 import Quality02RelaxationTask
from simmate.calculators.vasp.tasks.relaxation.quality_03 import Quality03RelaxationTask
from simmate.calculators.vasp.tasks.relaxation.quality_04 import Quality04RelaxationTask
from simmate.calculators.vasp.tasks.relaxation.third_party.mit import MITRelaxationTask
