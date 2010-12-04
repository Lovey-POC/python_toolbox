import garlicsim

from .state import State

ENDABLE = False
CONSTANT_CLOCK_INTERVAL = None
HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
DEFAULT_STEP_FUNCTION = State.step
DEFAULT_STEP_FUNCTION_TYPE = \
    garlicsim.misc.simpack_grokker.step_types.SimpleStep
CRUNCHERS_LIST = [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher]