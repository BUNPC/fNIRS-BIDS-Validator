import json
import os
import pprint
import pandas as pd

class fNIRS_BIDS():
    
    def __init__(self):
        f = open('BIDS_raw_folder.json')
        self.raw_folder_struture = json.load(f)
        
        f = open('BIDS_fNIRS_subject_folder.json')
        self.sub_folder_struture = json.load(f)
        
    def get_key_pos(self,key,file_folder_list):
            pos = -1
            for index, file_or_folder in enumerate(file_folder_list):
                if file_or_folder.endswith(key):
                    pos = index
                    break
                    
            return pos
        
    def get_key_path(self,key,file_folder_list):
        path = ''
        for index, file_or_folder in enumerate(file_folder_list):
            if file_or_folder.endswith(key):
                path = file_folder_list[index]
                break

        return path
        
    def get_key_paths(self, key, datset_path,sub_or_ses_folder):
        sub_ses_split = os.path.split(sub_or_ses_folder)
        paths = []
        if not sub_ses_split[0] == '':
            file_folder_list = os.listdir(os.path.join(datset_path,sub_ses_split[0]))
            path = self.get_key_path(key,file_folder_list)
            if path:
                paths.append(os.path.join(datset_path,sub_ses_split[0],path))
                        
        file_folder_list = os.listdir(os.path.join(datset_path,sub_or_ses_folder))
        path = self.get_key_path(key,file_folder_list)
        if path:
            paths.append(os.path.join(datset_path,sub_or_ses_folder,path))
                        
        file_folder_list = os.listdir(os.path.join(datset_path,sub_or_ses_folder,'nirs'))
        path = self.get_key_path(key,file_folder_list)
        if path:
            paths.append(os.path.join(datset_path,sub_or_ses_folder,'nirs',path))
                        
        return paths
        
        
    def validate_fNIRS_BIDS_dataset(self, datset_path):
        
        files_and_folders = os.listdir(datset_path)
        sub_folders = []
        
        # removes extensions for filenames for files othan than .json or .tsv files
        for index, file_or_folder in enumerate(files_and_folders):
            
            if os.path.isdir(os.path.join(datset_path, file_or_folder)):
                if file_or_folder.startswith('sub-'):
                    sub_folders.append(file_or_folder)
            else:
                ext = os.path.splitext(file_or_folder)[1]
                if not (ext == '.json' or ext == '.tsv'):
                    files_and_folders[index] = os.path.splitext(file_or_folder)[0]
                            
        
        raw_folder_keys = list(self.raw_folder_struture.keys())
        
        metadata_validation_info = {}
        for key in raw_folder_keys:
            key_ext = os.path.splitext(key)[1]
            if key in files_and_folders:
                ext = os.path.splitext(key)[1]
                temp_dict = {}
                __RequirementLevel__ = self.raw_folder_struture[key]['__RequirementLevel__']
                
                
                if ext == '.json':
                    f = open(os.path.join(datset_path, key))
                    json_data = json.load(f)
                    json_data_keys = list(json_data.keys())
                    sub_keys = list(self.raw_folder_struture[key].keys())
                    for sub_key in sub_keys:
                        if not sub_key == '__RequirementLevel__':
                            if not sub_key in json_data_keys:
                                temp_dict[sub_key] = {'__RequirementLevel__':self.raw_folder_struture[key][sub_key],
                                                      '__ErrorCode__':'MISSING',
                                                      '__ErrorMessage__' : sub_key+' field is missing'}
                                
                elif ext == '.tsv':
                    df = pd.read_csv(os.path.join(datset_path, key), sep='\t', keep_default_na=False, na_values=['',None])
                    sub_keys = list(self.raw_folder_struture[key].keys())
                    df_keys = list(df.keys())
                    for sub_key in sub_keys:
                        if not sub_key == '__RequirementLevel__':
                            if not sub_key in df_keys:
                                temp_dict[sub_key] = {'__RequirementLevel__':self.raw_folder_struture[key][sub_key],
                                                      '__ErrorCode__':'MISSING',
                                                      '__ErrorMessage__' : sub_key+' coulumn is missing'}
                            else:
                                row_numbers = df[df[sub_key].isna()].index.format()
                                temp_dict_2 = {}
                                for row_number in row_numbers:
                                    row_key = 'row_'+str(row_number)
                                    temp_dict_2[row_key] = {'__RequirementLevel__':self.sub_folder_struture[key][sub_key],
                                                         '__ErrorCode__': 'MISSING',
                                                         '__ErrorMessage__' : 'In '+sub_key+' column '+ 'row '+str(row_number)+ ' is empty'}
                                if temp_dict_2:
                                    temp_dict[sub_key] = temp_dict_2
                                    temp_dict[sub_key]['__RequirementLevel__'] = self.sub_folder_struture[key][sub_key]
                                    temp_dict[sub_key]['__ErrorCode__'] = 'INVALID'
                                    temp_dict[sub_key]['__ErrorMessage__'] = 'In '+sub_key+' column, some rows are empty'
                if temp_dict:          
                    temp_dict['__RequirementLevel__'] = __RequirementLevel__
                    temp_dict['__ErrorCode__'] = 'INVALID'
                    temp_dict['__ErrorMessage__'] = ''
                    metadata_validation_info[key] = temp_dict
                
            else:
                __RequirementLevel__ = self.raw_folder_struture[key]['__RequirementLevel__']
                metadata_validation_info[key] = {'__RequirementLevel__' : __RequirementLevel__,
                                                 '__ErrorCode__' : 'MISSING',
                                                 '__ErrorMessage__': 'File '+ key+ ' is missing'
                                                      }
        
        
        for sub_folder in sub_folders:
            BIDS_fNIRS_ses_folder_missing_metadata_list = []
            sub_folder_files_and_folders = os.listdir(os.path.join(datset_path,sub_folder))
            sub_or_ses_folders = []
            for sub_folder_file_and_folder in sub_folder_files_and_folders:
                if os.path.isdir(os.path.join(datset_path, sub_folder, sub_folder_file_and_folder)):
                    if sub_folder_file_and_folder.startswith('ses-'):
                        sub_or_ses_folders.append(sub_folder_file_and_folder)
                        
            if not sub_or_ses_folders:
                sub_or_ses_folders = [sub_folder]
            else:
                for index, value in enumerate(sub_or_ses_folders):
                    sub_or_ses_folders[index] = os.path.join(sub_folder, value)
                                
            for sub_or_ses_folder in sub_or_ses_folders:
                BIDS_sub_folder_missing_metadata = {}
                sub_or_ses_folder_files_and_folders = os.listdir(os.path.join(datset_path,sub_or_ses_folder,'nirs'))
                sub_folder_keys = list(self.sub_folder_struture.keys())
                
                for key in sub_folder_keys:
                    pos = self.get_key_pos(key,sub_or_ses_folder_files_and_folders)
                    paths = self.get_key_paths(key, datset_path, sub_or_ses_folder)

                    ###### This needs to be updated to get exact file location #####################
                    key_name = os.path.join(sub_or_ses_folder, os.path.basename(paths[0]))
                    if  paths: 
                        ext = os.path.splitext(key)[1]
                        temp_dict = {}
                        __RequirementLevel__ = self.sub_folder_struture[key]['__RequirementLevel__']
                        
                        if ext == '.json':
                            sub_keys = list(self.sub_folder_struture[key].keys())
                            json_data_keys = []
                            for u in range(len(paths)):
                                f = open(paths[u])
                                json_data = json.load(f)
                                json_data_keys.append(list(json_data.keys()))
    
                            json_data_keys = [x for sublist in json_data_keys for x in sublist]
                                                        
                            for sub_key in sub_keys:
                                if not sub_key == '__RequirementLevel__':
                                    if not sub_key in json_data_keys:
                                        temp_dict[sub_key] = {'__RequirementLevel__':self.sub_folder_struture[key][sub_key],
                                                             '__ErrorCode__': 'MISSING',
                                                             '__ErrorMessage__' : sub_key+' field is missing'}

                        elif ext == '.tsv':
                            df_keys = []
                            for u in range(len(paths)):
                                df = pd.read_csv(paths[u], sep='\t', keep_default_na=False, na_values=['',None])
                                df_keys.append(list(df.keys()))
    
                            df_keys = [x for sublist in df_keys for x in sublist]
                            
                            sub_keys = list(self.sub_folder_struture[key].keys())
                            for sub_key in sub_keys:
                                if not sub_key == '__RequirementLevel__':
                                    if not sub_key in df_keys:
                                        temp_dict[sub_key] = {'__RequirementLevel__':self.sub_folder_struture[key][sub_key],
                                                             '__ErrorCode__': 'MISSING',
                                                             '__ErrorMessage__' : sub_key+' coulumn is missing'}
                                    else:
                                        row_numbers = df[df[sub_key].isna()].index.format()
                                        temp_dict_2 = {}
                                        for row_number in row_numbers:
                                            row_key = 'row_'+str(row_number)
                                            temp_dict_2[row_key] = {'__RequirementLevel__':self.sub_folder_struture[key][sub_key],
                                                                 '__ErrorCode__': 'MISSING',
                                                                 '__ErrorMessage__' : 'In '+sub_key+' column '+ 'row '+str(row_number)+ ' is empty'}
                                        if temp_dict_2:
                                            temp_dict[sub_key] = temp_dict_2
                                            temp_dict[sub_key]['__RequirementLevel__'] = self.sub_folder_struture[key][sub_key]
                                            temp_dict[sub_key]['__ErrorCode__'] = 'INVALID'
                                            temp_dict[sub_key]['__ErrorMessage__'] = 'In '+sub_key+' column, some rows are empty'
                                            
                                        
                                        
                        BIDS_sub_folder_missing_metadata[key] = temp_dict
                        if temp_dict:
                            temp_dict['__RequirementLevel__'] = __RequirementLevel__
                            temp_dict['__ErrorCode__'] = 'INVALID'
                            temp_dict['__ErrorMessage__'] = ''
                            metadata_validation_info[key_name] = temp_dict
                       
                        
                    else:
                        __RequirementLevel__ = self.sub_folder_struture[key]['__RequirementLevel__']
                        metadata_validation_info[key_name] = {'__RequirementLevel__' : __RequirementLevel__,
                                                              '__ErrorCode__' : 'MISSING',
                                                              '__ErrorMessage__': 'File '+ key_name+ ' is missing'
                                                                }      
                        
        return metadata_validation_info