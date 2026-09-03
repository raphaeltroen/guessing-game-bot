import numpy as np
import pandas as pd

import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
import guess_bot as gb

#as of now this is totally empty data, will actually implement later and load the data from online
countries = np.arange(195)
attributes = np.array(["continent", "population", "landlocked", "average tempature", "religion"])
df = pd.DataFrame(index=countries, columns=attributes)

class geodle_bot(gb.guess_bot):
    def __init__(self):
        gb.guess_bot.__init__(self, countries, countries, 2**6)

    def get_bucket(self, ans, guess) ->int:
        bools = np.zeros(6)
        bools[0] = df[guess]["continent"]==df[ans]["continent"]
        bools[1] = df[guess]["population"]>=df[ans]["population"]
        bools[2] = df[guess]["landlocked"]>=df[ans]["landlocked"]
        bools[3] = df[guess]["average tempature"]>=df[ans]["average tempature"]
        bools[4] = df[guess]["religion"] == df[ans]["religion"]
        bools[5] = df[guess]["religion"] == df[ans]["religion"]

        return self.input_to_bucket(bools)

    def input_to_bucket(self, info) -> int:
        ans = 0
        for x in info:
            ans = 2*ans + int(x)
        return ans