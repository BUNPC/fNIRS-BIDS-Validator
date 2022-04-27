import json
import os
import pprint
import pandas as pd
from fNIRS_BIDS import fNIRS_BIDS

fNIRS_BIdS_obj = fNIRS_BIDS()
dataset_path = 'BIDS-NIRS-Tapping'
metadata_validation_info = fNIRS_BIdS_obj.validate_fNIRS_BIDS_dataset(dataset_path)
sys.stdout.write(json.dumps(metadata_validation_info))
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(metadata_validation_info)