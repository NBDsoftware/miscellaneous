From python API
=================


Search all molecules present in all sdf files
-------------------------------------------------

::
  
  # Load Molecule and look for commound compound and its different
  # conformations in the different sdf files
  
  from rdkit import Chem
  import glob
  from miscellaneous import search_molec_sdfs as sd
  
  output="output.sdf"
  sdf_files = glob.glob("../tests/data/sdf_file*/test_*.sdf")
  mols_in_all_sdfs = sd.search_molecule_in_all_sdf(sdf_files)
    # Load Molecule and look for commound compound and its different
    # conformations in the different sdf files
  
    from rdkit import Chem
    from miscellaneous import search_molec_sdfs as sd 
    sdf_files = glob.glob("miscellaneous/tests/data/test_*.sdf")
    allsdf_molecule_conformations = sd.search_molecule_in_all_sdf(sdf_files)
    
    #Output molecules and all conformations
    w = Chem.SDWriter(output)
    for m, conformations in mols_in_all_sdfs: 
        w.write(m)
        for conformation in conformations:
            w.write(conformation)
    
  
  
  
