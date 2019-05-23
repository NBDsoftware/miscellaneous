import argparse
import os
from tqdm import tqdm
from rdkit import Chem
from rdkit.Chem.Fingerprints import FingerprintMols



def search_molecule_in_all_sdf(sdf_files):
    print("Searchin for molecules in all sdf files...")
    sdf_file_ref = sdf_files.pop()
    found = [False] * len(sdf_files)
    molecules = [False] * len(sdf_files)
    for m_ref in tqdm(Chem.SDMolSupplier(sdf_file_ref)):
        fp = FingerprintMols.FingerprintMol(m_ref)
        for i, sdf in enumerate(sdf_files):
            for m in Chem.SDMolSupplier(sdf):
                if FingerprintMols.FingerprintMol(m) == fp:
                    found[i] = True
                    molecules[i] = m
                else:
                    pass
        if all(found):
            yield m_ref, molecules

def main(sdf_files):
    output = os.path.basename(sdf_files[-1].rsplit(".", 1)[0]) + "_output.sdf"
    mols_in_all_sdfs = search_molecule_in_all_sdf(sdf_files)
    w = Chem.SDWriter(output)
    n_mols = 0
    for m, molecules in mols_in_all_sdfs: 
        w.write(m)
        n_mols += 1
        # Output other sdfs
        for i, (m2, sdf_file) in enumerate(zip(molecules, sdf_files)):
            output_name = os.path.basename(sdf_file.rsplit(".",1)[0]) + "_output.sdf"
            with open(output_name, 'a') as f:
                f.write(Chem.MolToMolBlock(m2))
    print("Found {} common molecules in all sdf files".format(n_mols))
    return n_mols


def add_args(parser):
    parser.add_argument('sdfs', nargs="+", help="sdf files to check")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for molecules in all sdf files')
    add_args(parser)
    args = parser.parse_args()
    main(args.sdfs)
