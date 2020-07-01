"""
This script will submit a query to Protein Data Bank, download all PBD files associated
with the keywords and write a summary to a CSV file, which includes structure code, title,
resolution, reference DOI, etc.

To run it on command line:
$ python PDBscraper.py --query "..." --download ...

Example:
$ python PDBscraper.py --query "integrin alpha V beta 6" --download False
"""

import argparse
from lxml import html
import os
import pandas as pd
import requests


def pdb_search(search_string):
    search_string = search_string[0]
    url = "https://www.rcsb.org/pdb/rest/search/"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = """
    <orgPdbQuery><queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
    <keywords>{}</keywords></orgPdbQuery>
    """.format(search_string)

    pdb_codes = requests.post(url, data=data, headers=header).text.split()

    return pdb_codes, search_string.replace(" ", "_")


def filter_results(pdb_codes, included, excluded):
    filtered = []

    for code in pdb_codes:
        pdb = PDBObject(code)
        title = pdb.title[0].lower() if pdb.title else None
        included = included.lower() if included is not None else ""
        excluded = excluded.lower() if excluded else None

        if excluded:
            if included in title and excluded not in title:
                filtered.append(pdb)
        else:
            if included in title:
                filtered.append(pdb)

    return filtered


def substructure_search(substructure_file, inchi_keys):
    from rdkit import Chem
    sub = Chem.SDMolSupploer(substructure_file)
    matched = []

    for key in inchi_keys:
        ligand = Chem.MolFromInchi(key)

        if ligand.HasSubstructMatch(sub):
            matched.append(key)

    return matched


class PDBObject:

    def __init__(self, code):
        self.code = code
        self.info_url = "https://www.rcsb.org/structure/{}".format(self.code)
        self.download_url = "https://files.rcsb.org/download/{}.pdb".format(self.code)

        response = requests.get(self.info_url)
        tree = html.fromstring(response.content)

        self.title = tree.xpath("//span[@id='structureTitle']/text()")
        self.reference_title = tree.xpath("//div[@id='primarycitation']/h4/text()")
        self.reference_DOI = tree.xpath("//li[@id='pubmedDOI']/a/text()")
        self.resolution = tree.xpath("//ul[contains(@id,'exp_header')]/li[contains(@id,'resolution')]/text()")
        self.ligands = tree.xpath("//tr[contains(@id,'ligand_row')]//a[contains(@href, '/ligand/')]/text()")
        self.inchi_keys = tree.xpath("//tr[contains(@id, 'ligand_row')]//td[3]/text()")
        self.inchi_keys = [key for key in self.inchi_keys if len(key) == 27]

    def get_file(self, folder="."):
        file_content = requests.get(self.download_url).text
        file_name = os.path.join(folder, "{}.pdb".format(self.code))

        with open(file_name, "w") as PDB_file:
            PDB_file.write(file_content)


def download_structure(pdb_codes, folder="."):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    for code in pdb_codes:
        pdb = PDBObject(code)
        if pdb.title:
            pdb.get_file(folder)


def write_csv(pdb_codes, matched, folder="."):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    file = os.path.join(folder, "summary.csv")

    for pdb in pdb_codes:
        df = pd.DataFrame(
            {'PDB code': pdb.code,
             'Title': pdb.title if pdb.title else ["unknown"],
             'Resolution': [resolution.replace("Ã…", "Å").replace("&nbsp", "") for resolution in
                            pdb.resolution] if pdb.resolution else ["unknown"],
             'Reference Title': pdb.reference_title if pdb.reference_title else ["unknown"],
             'Reference DOI': pdb.reference_DOI if pdb.reference_DOI else ["unknown"],
             'Ligands': [", ".join(pdb.ligands)] if pdb.ligands else ["none"],
             'InChi keys': [", ".join(pdb.inchi_keys)] if pdb.inchi_keys else ["none"],
             'Matched substructures': [key for key in pdb.inchi_keys if key in matched]
             })
        df.to_csv(file, mode='a', header=False)

    return file


def main(search_string, download, included, excluded, substructure_file):
    pdb_codes, folder = pdb_search(search_string)
    filtered = filter_results(pdb_codes, included, excluded)

    for f in filtered:
        if download:
            print("Downloading structures...")
            download_structure(f, folder)

        if substructure_file:
            matched = substructure_search(substructure_file, f.inchi_keys)

    file = write_csv(filtered, matched, folder)

    print("Done! Summary available in {}.".format(file))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', nargs=1, required=True, help="PDB query (string)")
    parser.add_argument('--download', required=False, default=False,
                        help="Set to 'True', if you want to download associated PDB files")
    parser.add_argument('--included', required=False, help="PDB title must include...")
    parser.add_argument('--excluded', required=False, help="PDB title must not include...")
    parser.add_argument('--substructure', required=False, help="SD file with substructure")
    args = parser.parse_args()
    return args.query, args.download, args.included, args.excluded, args.substructure


if __name__ == "__main__":
    query, download, included, excluded, substructure = parse_args()
    main(query, download, included, excluded, substructure)
