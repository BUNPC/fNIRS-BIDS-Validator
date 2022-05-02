import json
import os
import pprint
import pandas as pd
import sys
from fNIRS_BIDS import fNIRS_BIDS

fNIRS_BIdS_obj = fNIRS_BIDS()
dataset_path = 'BIDS-NIRS-Tapping'
metadata_validation_info = fNIRS_BIdS_obj.validate_fNIRS_BIDS_dataset(dataset_path)
sys.stdout.write(json.dumps(metadata_validation_info))
# print(json.dumps(metadata_validation_info, indent=4, sort_keys=True))