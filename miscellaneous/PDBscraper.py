"""
This script will submit a query to Protein Data Bank, download all PBD files associated
with the keywords and write a summary to a CSV file, which includes structure code, title,
resolution, reference DOI, etc.

To run it on command line:
$ python PDBscraper.py "query"

Example:
$ python PDBscraper.py "integrin alpha V beta 6"
"""

import argparse
from lxml import html
import os
import pandas as pd
import requests


def pdb_search(search_string):
    url = "https://www.rcsb.org/pdb/rest/search/"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = """
    <orgPdbQuery><queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
    <keywords>{}</keywords></orgPdbQuery>
    """.format(search_string)

    pdb_codes = requests.post(url, data=data, headers=header).text.split()
    return pdb_codes, search_string.replace(" ", "_")


class PDBObject:

    def __init__(self, code):
        self.code = code
        self.info_url = "https://www.rcsb.org/structure/{}".format(self.code)
        self.download_url = "https://files.rcsb.org/download/{}.pdb".format(self.code)

    def get_data(self):
        response = requests.get(self.info_url)
        tree = html.fromstring(response.content)
        self.title = tree.xpath("//span[@id='structureTitle']/text()")
        self.reference_title = tree.xpath("//div[@id='primarycitation']/h4/text()")
        self.reference_DOI = tree.xpath("//li[@id='pubmedDOI']/a/text()")
        self.resolution = tree.xpath("//ul[contains(@id,'exp_header')]/li[contains(@id,'resolution')]/text()")

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
        pdb.get_file(folder)


def write_csv(pdb_codes, folder="."):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    file = os.path.join(folder, "summary.csv")

    for code in pdb_codes:
        pdb = PDBObject(code)
        pdb.get_data()

        df = pd.DataFrame(
            {'PDB code': code,
             'Title': pdb.title if pdb.title else ["unknown"],
             'Resolution': [resolution.replace("Ã…", "Å").replace("&nbsp", "") for resolution in
                            pdb.resolution] if pdb.resolution else ["unknown"],
             'Reference Title': pdb.reference_title if pdb.reference_title else ["unknown"],
             'Reference DOI': pdb.reference_DOI if pdb.reference_DOI else ["unknown"]
             })
        df.to_csv(file, mode='a', header=True)

    return file


def main(search_string):
    pdb_codes, folder = pdb_search(search_string)
    print("Downloading structures...")
    download_structure(pdb_codes, folder)
    file = write_csv(pdb_codes, folder)
    print("Done! Summary available in {}.".format(file))


def add_args(parser):
    parser.add_argument('search_string', nargs=1, help="PDB query (string)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDB query')
    add_args(parser)
    args = parser.parse_args()
    main(str(args.search_string[0]))
