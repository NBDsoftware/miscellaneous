import pytest
import os
import glob
from miscelanious import search_molec_sdfs as sms

DIR = os.path.dirname(__file__)
SDF_FILES = glob.glob(os.path.join(DIR, "data/sdf_file_intersec/test_HB*"))

def test_sdf_file_intersec(sdf_files=SDF_FILES, result=1):
    output = sms.main(sdf_files, output="similar.sdf")
    assert output == result
