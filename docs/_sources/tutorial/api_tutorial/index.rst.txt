From python API
=================


Search all molecules present in all sdf files
--------------------------------------------

::

  from rdkit import Chem
  from miscellaneous import search_molec_sdfs as sd 
  molecules = sd.search_molecule_in_all_sdf(sdf_files)
  w = Chem.SDWriter(output)
  for m in mols_in_all_sdfs: 
      w.write(m)



