import pandas as pd 

def remove_data_leakage(train_df, valid_df, col = ""):

    # if the col is empty then return a message and end 
    if col == "":
        print("Please specify the column name!")
        return
    
    ids_train = set(train_df[col].values)
    ids_valid = set(valid_df[col].values)

    patient_overlap = list(ids_train.intersection(ids_valid))
    print(f"There are {len(patient_overlap)} patients in both train and valid set.")

    train_overlap_idxs = []
    valid_overlap_idxs = []
    for idx in patient_overlap:
        train_overlap_idxs.extend(train_df.index[train_df[col] == idx].to_list())
        valid_overlap_idxs.extend(valid_df.index[valid_df[col] == idx].to_list())
        
    print(f'These are the indices of overlapping patients in the training set: ')
    print(f'{train_overlap_idxs}')
    print(f'These are the indices of overlapping patients in the validation set: ')
    print(f'{valid_overlap_idxs}')

    # Drop the overlapping patients from the validation set
    valid_df.drop(valid_overlap_idxs, inplace=True)
    print(f'After removing overlapping patients, there are {valid_df.shape[0]} samples in the validation set.')

    # Sanity check
    assert len(set(train_df[col].values).intersection(set(valid_df[col].values))) == 0

    return train_df, valid_df

def check_for_leakage(df1 : pd.DataFrame , df2: pd.DataFrame, patient_col:str)-> bool:
    """
    Return True if there any patients are in both df1 and df2.

    Args:
        df1 (dataframe): dataframe describing first dataset
        df2 (dataframe): dataframe describing second dataset
        patient_col (str): string name of column with patient IDs
    
    Returns:
        leakage (bool): True if there is leakage, otherwise False
    """
    
    df1_patients_unique =set(df1[patient_col].values)
    df2_patients_unique = set(df2[patient_col].values)
    
    patients_in_both_groups = df1_patients_unique.intersection(df2_patients_unique)

    # leakage contains true if there is patient overlap, otherwise false.
    if len(patients_in_both_groups) > 0 :
        leakage = True 
    else : 
        leakage = False
    # boolean (true if there is at least 1 patient in both groups)
   
    return leakage


