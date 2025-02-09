# rad_msh_converter
python scripts to generate meshes by converting files from gmsh, abaqus or ls-dyna

## gmsh_label_to_radioss.py
Convert the mesh file (4-node shell elements) from gmsh in radioss format (.rad) by re-defining the scaling of coordinates and the labels of nodes and elements

## lspost_label_to_radioss.py
Convert the mesh file (4-node shell elements) from lsprepost in ls-dyna format (.k) by re-defining the keywords, 3-node shell, 4-node shell.
## lspost_label_to_radioss_solid_8node.py
Convert the mesh file (8-node solid elements) from lsprepost in ls-dyna format (.k) by re-defining the keywords, 8-node solid.