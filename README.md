chemtools
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## How to use

Chemtools offer a collection of cheminformatics scripts for daily tasks.
Currently supported tasks include:

    1 - Standardization of chemical structures

    2 - Calculation of molecular descriptors

    3 - Filtering datasets using predefined alerts (e.g. PAINS, Dundee, Glaxo)

# Standardization

A dataset of molecules can be standardize in just 1 line of code!

``` python
import pandas as pd
import numpy as np
from chemtools.tools.sanitizer import MolCleaner
from chemtools.tools.featurizer import MolFeaturizer
from chemtools.tools.filtering import MolFiltering
from rdkit import Chem
import json
```

``` python
data = pd.read_csv('../data/example_data.csv')
```

# Sanitizing

The
[`MolCleaner`](https://marcossantanaioc.github.io/chemtools/sanitizer.html#molcleaner)
class performs sanitization tasks following the steps implemented on
[chembl_structure_pipeline](https://github.com/chembl/ChEMBL_Structure_Pipeline)

        1. Standardize unknown stereochemistry (Handled by the RDKit Mol file parser)
            i) Fix wiggly bonds on sp3 carbons - sets atoms and bonds marked as unknown stereo to no stereo
            ii) Fix wiggly bonds on double bonds – set double bond to crossed bond
        2. Clears S Group data from the mol file
        3. Kekulize the structure
        4. Remove H atoms (See the page on explicit Hs for more details)
        5. Normalization:
            Fix hypervalent nitro groups
            Fix KO to K+ O- and NaO to Na+ O- (Also add Li+ to this)
            Correct amides with N=COH
            Standardise sulphoxides to charge separated form
            Standardize diazonium N (atom :2 here: [*:1]-[N;X2:2]#[N;X1:3]>>[*:1]) to N+
            Ensure quaternary N is charged
            Ensure trivalent O ([*:1]=[O;X2;v3;+0:2]-[#6:3]) is charged
            Ensure trivalent S ([O:1]=[S;D2;+0:2]-[#6:3]) is charged
            Ensure halogen with no neighbors ([F,Cl,Br,I;X0;+0:1]) is charged
        6. The molecule is neutralized, if possible. See the page on neutralization rules for more details.
        7. Remove stereo from tartrate to simplify salt matching
        8. Normalise (straighten) triple bonds and allenes
        
        
        
        The curation steps in ChEMBL structure pipeline were augmented with additional steps to identify duplicated entries
        9. Find stereo centers
        10. Generate inchi keys
        11. Find duplicated SMILES. If the same SMILES is present multiple times, two outcomes are possible.
            i. The same compound (e.g. same ID and same SMILES)
            ii. Isomers with different SMILES, IDs and/or activities
            
            In case i), the compounds are merged by taking the median values of all numeric columns in the dataframe. 
            For case ii), the compounds are further classified as 'to merge' or 'to keep' depending on the activity values.
                a) Compounds are considered for mergining (to merge) if the difference in acvitities is less than 1log unit.
                b) Compounds are considered for keeping as individual entries (to keep) if the difference in activities is larger than 1log unit. In this case, the user can
                select which compound to keep - the one with highest or lowest activity.

``` python
processed_data = MolCleaner.from_df(data, smiles_col='smiles', act_col='pIC50', id_col='molecule_chembl_id')
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>processed_smiles</th>
      <th>molecule_chembl_id</th>
      <th>IC50</th>
      <th>units</th>
      <th>smiles</th>
      <th>pIC50</th>
      <th>molecular_weight</th>
      <th>n_hba</th>
      <th>n_hbd</th>
      <th>logp</th>
      <th>ro5_fulfilled</th>
      <th>inchi</th>
      <th>Stereo</th>
      <th>duplicate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5347</td>
      <td>N#Cc1cnc(Nc2cccc(Br)c2)c2cc(NC(=O)c3ccco3)ccc12</td>
      <td>CHEMBL1641996</td>
      <td>55600.0</td>
      <td>nM</td>
      <td>N#Cc1cnc(Nc2cccc(Br)c2)c2cc(NC(=O)c3ccco3)ccc12</td>
      <td>4.254925</td>
      <td>432.022188</td>
      <td>5</td>
      <td>2</td>
      <td>5.45788</td>
      <td>True</td>
      <td>GRAWSTNUDRSLLQ-UHFFFAOYSA-N</td>
      <td></td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2985</td>
      <td>COc1cccc(-c2cn(-c3ccc(CNCCO)cc3)c3ncnc(N)c23)c1</td>
      <td>CHEMBL424375</td>
      <td>300.0</td>
      <td>nM</td>
      <td>COc1cccc(-c2cn(-c3ccc(CNCCO)cc3)c3ncnc(N)c23)c1</td>
      <td>6.522879</td>
      <td>389.185175</td>
      <td>7</td>
      <td>3</td>
      <td>2.76020</td>
      <td>True</td>
      <td>QGPSFIYTQAONCS-UHFFFAOYSA-N</td>
      <td></td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2828</td>
      <td>Cc1ncc([N+](=O)[O-])n1CC(=NNC(=O)c1ccc(O)cc1)c...</td>
      <td>CHEMBL3088220</td>
      <td>210.0</td>
      <td>nM</td>
      <td>Cc1ncc([N+](=O)[O-])n1C/C(=N/NC(=O)c1ccc(O)cc1...</td>
      <td>6.677781</td>
      <td>457.038566</td>
      <td>7</td>
      <td>2</td>
      <td>3.40212</td>
      <td>True</td>
      <td>XBPATCWTKVXDPF-UHFFFAOYSA-N</td>
      <td></td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3898</td>
      <td>C1CCC(C(CC2CCCCN2)C2CCCCC2)CC1</td>
      <td>CHEMBL75880</td>
      <td>1485.2</td>
      <td>nM</td>
      <td>C1CCC(C(CC2CCCCN2)C2CCCCC2)CC1</td>
      <td>5.828215</td>
      <td>277.276950</td>
      <td>1</td>
      <td>1</td>
      <td>5.29540</td>
      <td>True</td>
      <td>CYXKNKQEMFBLER-UHFFFAOYSA-N</td>
      <td>6_?</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2896</td>
      <td>Cc1cc2cc(Nc3ccnc4cc(-c5ccc(CNCCN6CCNCC6)cc5)sc...</td>
      <td>CHEMBL79060</td>
      <td>250.0</td>
      <td>nM</td>
      <td>Cc1cc2cc(Nc3ccnc4cc(-c5ccc(CNCCN6CCNCC6)cc5)sc...</td>
      <td>6.602060</td>
      <td>496.240916</td>
      <td>6</td>
      <td>4</td>
      <td>5.49142</td>
      <td>True</td>
      <td>MEAHQSFATRAJHG-UHFFFAOYSA-N</td>
      <td></td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>

# Filtering

The
[`MolFiltering`](https://marcossantanaioc.github.io/chemtools/filtering.html#molfiltering)
class is responsible for removing compounds that match defined
substructural alerts, including PAINS and rules defined by different
organizations, such as GSK and University of Dundee.

``` python
with open('../data/libraries/Glaxo_alerts.json') as f:
    alerts_dict = json.load(f)['structural_alerts']
    structural_alerts = alerts_dict.get('structural_alerts', None)
```

``` python
alerts_data = MolFiltering.from_df(processed_data, smiles_col='processed_smiles', alerts_dict=alerts_dict)
```

``` python
alerts_data.head(10)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_smiles</th>
      <th>Alert_SMARTS</th>
      <th>Alert_description</th>
      <th>Alert_rule_set</th>
      <th>Alert_num_hits</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Cc1ncc([N+](=O)[O-])n1CC(=NNC(=O)c1ccc(O)cc1)c...</td>
      <td>[N;R0][N;R0]C(=O)</td>
      <td>R17 acylhydrazide</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>0</th>
      <td>O=NN(CCCl)C(=O)Nc1ccc2ncnc(Nc3cccc(Cl)c3)c2c1</td>
      <td>[Br,Cl,I][CX4;CH,CH2]</td>
      <td>R1 Reactive alkyl halides</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>O=NN(CCCl)C(=O)Nc1ccc2ncnc(Nc3cccc(Cl)c3)c2c1</td>
      <td>[N;R0][N;R0]C(=O)</td>
      <td>R17 acylhydrazide</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>O=NN(CCCl)C(=O)Nc1ccc2ncnc(Nc3cccc(Cl)c3)c2c1</td>
      <td>[N&amp;D2](=O)</td>
      <td>R21 Nitroso</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>0</th>
      <td>CS(=O)(=O)O[C@H]1CN[C@H](C#Cc2cc3ncnc(Nc4ccc(O...</td>
      <td>COS(=O)(=O)[C,c]</td>
      <td>R5 Sulphonates</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Cc1cccc(Nc2ncnc3ccc(N(C)C(=O)N(CCCl)N=O)cc23)c1</td>
      <td>[Br,Cl,I][CX4;CH,CH2]</td>
      <td>R1 Reactive alkyl halides</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cc1cccc(Nc2ncnc3ccc(N(C)C(=O)N(CCCl)N=O)cc23)c1</td>
      <td>[N;R0][N;R0]C(=O)</td>
      <td>R17 acylhydrazide</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cc1cccc(Nc2ncnc3ccc(N(C)C(=O)N(CCCl)N=O)cc23)c1</td>
      <td>[N&amp;D2](=O)</td>
      <td>R21 Nitroso</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>0</th>
      <td>C=COC(=O)N(CCN(C)C)N=Nc1ccc2ncnc(Nc3cccc(Cl)c3...</td>
      <td>[N;R0][N;R0]C(=O)</td>
      <td>R17 acylhydrazide</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>0</th>
      <td>O=C(CCl)Nc1ccc2ncnc(Nc3cccc(I)c3)c2c1</td>
      <td>[Br,Cl,I][CX4;CH,CH2]</td>
      <td>R1 Reactive alkyl halides</td>
      <td>Glaxo</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

#### Quinone

``` python
mol = Chem.MolFromSmiles('COC1/C=C\OC2(C)Oc3c(C)c(O)c4c(c3C2=O)C(=O)C=C(NC(=O)/C(C)=C\C=C/C(C)C(O)C(C)C(O)C(C)C(OC(C)=O)C1C)C4=O')
mol.GetSubstructMatches(Chem.MolFromSmarts('O=C1[#6]~[#6]C(=O)[#6]~[#6]1'))
mol
```

![](index_files/figure-gfm/cell-10-output-1.png)

#### Cynamide

``` python
mol1 = Chem.MolFromSmiles('Cc1cccc(C[C@H](NC(=O)c2cc(C(C)(C)C)nn2C)C(=O)NCC#N)c1')
mol1.GetSubstructMatches(Chem.MolFromSmarts('N[CH2]C#N'))
mol1
```

![](index_files/figure-gfm/cell-11-output-1.png)

#### R18 Quaternary C, Cl, I, P or S

``` python
mol = Chem.MolFromSmiles('CC[C@H](NC(=O)c1c([S+](C)[O-])c(-c2ccccc2)nc2ccccc12)c1ccccc1')
mol.GetSubstructMatches(Chem.MolFromSmarts('[C+,Cl+,I+,P+,S+]'))
mol
```

![](index_files/figure-gfm/cell-12-output-1.png)

# Featurization

The
[`MolFeaturizer`](https://marcossantanaioc.github.io/chemtools/featurizer.html#molfeaturizer)
class converts SMILES into molecular descriptors. The current version
supports Morgan fingerprints, Atom Pairs, Torsion Fingerprints, RDKit
fingerprints and 200 constitutional descriptors, and MACCS keys.

``` python
fingerprinter = MolFeaturizer('morgan')
```

``` python
X = fingerprinter.process_smiles_list(processed_data['processed_smiles'].values)
```

<style>
    /* Turns off some styling */
    progress {
        /* gets rid of default border in Firefox and Opera. */
        border: none;
        /* Needs to be in here for Safari polyfill so background images work as expected. */
        background-size: auto;
    }
    progress:not([value]), progress:not([value])::-webkit-progress-bar {
        background: repeating-linear-gradient(45deg, #7e7e7e, #7e7e7e 10px, #5c5c5c 10px, #5c5c5c 20px);
    }
    .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
        background: #F44336;
    }
</style>

    <div>
      <progress value='500' class='' max='500' style='width:300px; height:20px; vertical-align: middle;'></progress>
      100.00% [500/500 00:00&lt;00:00]
    </div>
    

``` python
X[0:5]
```

    array([[0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           [0, 1, 1, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 1]], dtype=uint8)
