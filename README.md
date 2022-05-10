# BIDS-fNIRS-Validator
Validates that BIDS-fNIRS datasets and returns missing fileds of meta data files.

### Input
dataset_path : path to the BIDS-fNIRS dataset that needs to be validated

### Output
BIDS_raw_folder_missing_metadata : dictionary with missing fileds of raw folder meta data files <br>
BIDS_fNIRS_sub_folder_missing_metadata_list : list of dictionaries with missing fileds of subject folder meta data files

### Example
```

import json
import sys
from fNIRS_BIDS_Validator.fNIRS_BIDS import fNIRS_BIDS
fNIRS_BIdS_obj = fNIRS_BIDS()
dataset_path = 'BIDS-NIRS-Tapping'
metadata_validation_info = fNIRS_BIdS_obj.validate_fNIRS_BIDS_dataset(dataset_path)
sys.stdout.write(json.dumps(metadata_validation_info)) 

```


