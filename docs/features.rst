Features
--------

* A `Configuration Manager <module_ref.html#module-sksurgerycore.configuration.configuration_manager>`_ to load parameters from a .json file
* A `Transform Manager <module_ref.html#module-sksurgerycore.transforms.transform_manager>`_ to manage combinations of 4x4 transformation matrices
* `Corresponding point <module_ref.html#module-sksurgerycore.algorithms.procrustes>`_ (i.e Landmark) based registration, based on `Arun et al., 1987`_.
* `Rotaiton/translation Matrix construction <module_ref.html#module-sksurgerycore.transforms.matrix>`_ and `validation functions <module_ref.html#matrix-validation>`_, 
  checking a numpy array is a camera matrix, rotation matrix, rigid transform etc.

  `Source code <https://github.com/UCL/scikit-surgerycore/>`_ is avaialble on GitHub.