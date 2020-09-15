from typing import Union, List
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
import csv
import sys
from multiprocessing import Pool

Molecule = Union[str, Chem.Mol]

from descriptastorus.descriptors import rdDescriptors, rdNormalizedDescriptors

def rdkit_2d_features_generator(mol: Molecule) -> np.ndarray:
    """
    Generates RDKit 2D normalized features for a molecule.

    :param mol: A molecule (i.e. either a SMILES string or an RDKit molecule).
    :return: A 1D numpy array containing the RDKit 2D normalized features.
    """
    smiles = Chem.MolToSmiles(mol, isomericSmiles=True) if type(mol) != str else mol
    generator = rdNormalizedDescriptors.RDKit2DNormalized()
    features = generator.process(smiles)[1:]

    return features


def get_features(infile, outfile, use_compound_names=False):
    with open(infile) as f:
        reader = csv.reader(f)
        next(reader)
        feat_list = []
        for line in reader:
            if use_compound_names:
                line = line[1:]
            smiles = line[0]
            feat = rdkit_2d_features_generator(smiles)
            feat_list.append(feat)
        feat_array = np.array(feat_list)
        np.save(outfile, feat_array)
        #print(feat_array.shape)

infile = sys.argv[1]
outfile = sys.argv[2]
withname = int(sys.argv[3])
if withname == 1:
    use_compound_names = True
else:
    use_compound_names = False
get_features(infile, outfile, use_compound_names)
