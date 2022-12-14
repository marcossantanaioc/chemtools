# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/utils.ipynb.

# %% auto 0
__all__ = ['convert_smiles']

# %% ../notebooks/utils.ipynb 2
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdchem

# %% ../notebooks/utils.ipynb 5
def convert_smiles(mol, sanitize=False):
    if isinstance(mol, str):
        try:
            mol = Chem.MolFromSmiles(mol, sanitize=sanitize)
            return mol
        except:
            return None
    elif isinstance(mol, rdchem.Mol):
        return mol
