import glob
import pandas as pd
from miscellaneous import PDBscraper as scrape


def test_scraper():
    scrape.main("Integrin alpha-v beta-8 in complex with the Fabs C6-RGD3")
    n_files = len(glob.glob("Integrin_alpha-v_beta-8_in_complex_with_the_Fabs_C6-RGD3/*.pdb"))
    pdb_codes = pd.read_csv("Integrin_alpha-v_beta-8_in_complex_with_the_Fabs_C6-RGD3/summary.csv")
    pdb_codes = pdb_codes['PDB code'].tolist()

    assert '2KNC' in pdb_codes
    assert n_files == 100
