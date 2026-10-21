import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdFingerprintGenerator



"""Descriptor function"""

def compute_descriptors(smiles_series):
    # Collect descriptor names.
    descriptor_names = []

    for name, function in Descriptors.descList:
        descriptor_names.append(name)

    rows = []

    for smiles in smiles_series:
        # Convert the SMILES into a molecule.
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")

        # Calculate each descriptor for this molecule.
        values = []

        for name, function in Descriptors.descList:
            value = function(mol)
            values.append(value)

        rows.append(values)

    # Create a table: one row per molecule, one column per descriptor.
    descriptors = pd.DataFrame(
        rows,
        columns=descriptor_names,
        index=smiles_series.index
    )

    # Replace infinite values with missing values.
    descriptors = descriptors.replace([np.inf, -np.inf], np.nan)

    return descriptors



"""Morgan fingerprint function"""

def compute_morgan(smiles_series, radius=2, n_bits=2048):
    # Configure the fingerprint calculation.
    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=radius,
        fpSize=n_bits
    )

    rows = []

    for smiles in smiles_series:
        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")

        # Calculate a binary fingerprint for this molecule.
        fingerprint = generator.GetFingerprintAsNumPy(mol)
        rows.append(fingerprint)

    return pd.DataFrame(
        rows,
        index=smiles_series.index
    )