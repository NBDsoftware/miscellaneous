import argparse
from tqdm import tqdm
from rdkit import Chem
from rdkit.Chem.Fingerprints import FingerprintMols



def search_molecule_in_all_sdf(sdf_files):
    print("Searchin for molecules in all sdf files...")
    sdf_file_ref = sdf_files.pop()
    found = [False] * len(sdf_files)
    for m_ref in tqdm(Chem.SDMolSupplier(sdf_file_ref)):
        fp = FingerprintMols.FingerprintMol(m_ref)
        for i, sdf in enumerate(sdf_files):
            for m in Chem.SDMolSupplier(sdf):
                if FingerprintMols.FingerprintMol(m) == fp:
                    found[i] = True
                else:
                    pass
        if all(found):
            yield m_ref

def main(sdf_files, output):
    mols_in_all_sdfs = search_molecule_in_all_sdf(sdf_files)
    w = Chem.SDWriter(output)
    n_mols = 0
    for m in mols_in_all_sdfs: 
        w.write(m)
        n_mols += 1
    return n_mols


def add_args(parser):
    parser.add_argument('sdfs', nargs="+", help="sdf files to check")
    parser.add_argument('--output', type=str, help="output_file", default="molecules.sdf")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for molecules in all sdf files')
    add_args(parser)
    args = parser.parse_args()
    main(args.sdfs, args.output)
