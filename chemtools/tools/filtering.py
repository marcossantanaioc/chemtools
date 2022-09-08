# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/filtering.ipynb.

# %% auto 0
__all__ = ['MolFiltering']

# %% ../../notebooks/filtering.ipynb 2
import json
from collections import defaultdict
import multiprocessing as mp
import pandas as pd
import numpy as np
from rdkit import Chem
from .sanitizer import convert_smiles, normalize_mol, MolCleaner
from rdkit.Chem import AllChem,rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from typing import List, Collection, Tuple

from fastprogress.fastprogress import master_bar, progress_bar
from time import sleep

# %% ../../notebooks/filtering.ipynb 5
class MolFiltering:
    
    """Filter a molecular dataset from unwanted structures
    
        Use  factory methods `MolFiltering.from_list`, `MolFiltering.from_df` or `MolFiltering.from_csv` instead of accessing the class directly.
       
    """
    
    @classmethod
    def get_mol_alerts(cls, smi, alerts_dict:dict) -> pd.DataFrame:

        """
        Find structural alerts for a single SMILES.

        Arguments:
        
            smi : str
                A SMILES representing a molecule.

            alerts_dict : dict
                A dict with alerts definitions.

        Returns:
        
            rule_sets : pandas.DataFrame
                A `pandas.DataFrame` with substructure alerts for `smi`.

        """
        _columns = ['_smiles','Alert_SMARTS','Alert_description','Alert_rule_set','Alert_num_hits']
        try:
            mol = normalize_mol(smi)
            rule_sets = []
            for alert, (rule_set, description, max_value) in alerts_dict.items():
                hits = len(mol.GetSubstructMatches(Chem.MolFromSmarts(alert)))
                if hits > max_value:
                    rule_sets.append((smi, alert, description, rule_set, hits))
            rule_sets = pd.DataFrame(rule_sets, columns=_columns)
            return rule_sets
        except:
            return None

    @classmethod
    def get_alerts(cls, smiles_list, alerts_dict:dict, n_jobs:int=None) -> pd.DataFrame:
        
        """
        Find structural alerts for a list of SMILES.

        Arguments:
        
            smiles_list : Collection
                A collection of SMILES.

            alerts_dict : dict
                A dict with alerts definitions.

            n_jobs : int
                The number of jobs to run in parallel.

        Returns:
        
            alerts_df : `pandas.DataFrame`
            

                A `pandas.DataFrames` with flagged molecules.

        """

            
        from functools import partial
        
        filtering_func = partial(cls.get_mol_alerts, alerts_dict=alerts_dict)


        if n_jobs is None: n_jobs = mp.cpu_count()
            
        #try:
        with mp.Pool(n_jobs) as mp_pool:
            all_alerts = pd.concat(list(progress_bar(mp_pool.imap(filtering_func, smiles_list), total=len(smiles_list))))
            
        if all_alerts.empty: 
            print('No compounds were flagged.')
        
        return all_alerts

            

    @classmethod
    def from_list(cls, smiles_list,alerts_dict:dict=None,n_jobs:int=1, **kwargs) -> pd.DataFrame:
        
        """Factory method to process a list of SMILES.

        Arguments:

            smiles : A List, Array, or any Iterable (except strings)
                SMILES ready for sanitization

        Returns:
        
            alerts_df : `pandas.DataFrame`
            

                A `pandas.DataFrames` with flagged molecules.

        """
        
        id_col = 'ID'
        smiles_col = 'smiles'

        df = pd.DataFrame({smiles_col:smiles_list, id_col:[f'mol{idx}' for idx in range(len(smiles_list))]})


        return cls.from_df(df, smiles_col=smiles_col, alerts_dict=alerts_dict, n_jobs=n_jobs)


    @classmethod
    def from_df(cls,
                df: pd.DataFrame, 
                smiles_col:str,
               alerts_dict:dict=None,
                n_jobs:int=1) -> pd.DataFrame:
        
        """Factory method to process a `pandas.DataFrame`

        Arguments:
        
            df : pd.DataFrame
                A pandas Dataframe with molecular data for sanitization.

            smiles_col : str
                The name of the column with SMILES for each molecule.


        Returns:
        
            alerts_df : `pandas.DataFrame`
            

                A `pandas.DataFrames` with flagged molecules.

        """     
        

        
        _data = df.copy()
        _data.reset_index(drop=True,inplace=True)
        
        if not isinstance(alerts_dict, dict) and alerts_dict is not None:
            raise TypeError('Please provide a valid dictionary of structural alerts')
        
        if alerts_dict is None:
            with open('../data/libraries/Glaxo_alerts.json') as f:
                alerts_dict = json.load(f)['structural_alerts']

        return cls.get_alerts(smiles_list=_data[smiles_col].values, alerts_dict=alerts_dict, n_jobs=n_jobs)

    @classmethod
    def from_csv(cls,
                 data_path: str,
                 smiles_col: str,
                 alerts_dict:dict=None,
                 n_jobs:int=1,
                 sep: str = ',') -> pd.DataFrame:
        
        """Factory method to process a CSV file.

        Arguments:

            data_path : str
                Path to CSV file

            smiles_col : str
                The name of the column with SMILES for each molecule.

 
        Returns:
        
            alerts_df : `pandas.DataFrame`
            

                A `pandas.DataFrames` with flagged molecules.
            
        """
        
        return cls.from_df(pd.read_csv(data_path, sep=sep), 
                           smiles_col=smiles_col,alerts_dict=alerts_dict)

