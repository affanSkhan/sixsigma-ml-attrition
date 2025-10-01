# reproducible_seed.py snippet
import os
import random
import numpy as np


SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)


# scikit-learn uses random_state parameters in model constructors
# xgboost / lightgbm also accept seed hyperparameters