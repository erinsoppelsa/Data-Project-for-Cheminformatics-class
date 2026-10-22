from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold


"""Sacaffold function"""


def get_scaffold(smiles):
    
    mol = Chem.MolFromSmiles(smiles)

    # Stop if RDKit cannot interpret the structure.
    if mol is None:
        return None

    # Extract the Murcko scaffold as a molecule object.
    scaffold_mol = MurckoScaffold.GetScaffoldForMol(mol)

    # Convert the scaffold into a SMILES string.
    scaffold_smiles = Chem.MolToSmiles(scaffold_mol)

    # If the scaffold is empty, use the original SMILES.
    if scaffold_smiles == "":
        return smiles
    else:
        return scaffold_smiles





