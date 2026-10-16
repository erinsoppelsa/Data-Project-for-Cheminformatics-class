from rdkit import Chem


def canonicalize_smiles(smiles):
    """Return a canonical SMILES, or None if the structure is invalid."""
    molecule = Chem.MolFromSmiles(smiles)
    return Chem.MolToSmiles(molecule) if molecule is not None else None