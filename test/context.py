import sys
import os
import inspect

pathToHere = inspect.getfile(inspect.currentframe())
sys.path.insert(0, os.path.dirname(os.path.dirname(pathToHere)))

import montesniere
