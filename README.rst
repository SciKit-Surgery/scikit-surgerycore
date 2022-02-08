scikit-surgerycore
===============================

.. image:: https://github.com/SciKit-Surgery/scikit-surgerycore/raw/master/skscore_logo.png
   :height: 200px
   :target: https://github.com/SciKit-Surgery/scikit-surgerycore
   :alt: Logo

| 

.. image:: https://github.com/SciKit-Surgery/scikit-surgerycore/workflows/.github/workflows/ci.yml/badge.svg
   :target: https://github.com/SciKit-Surgery/scikit-surgerycore/actions
   :alt: GitHub Actions CI status

.. image:: https://coveralls.io/repos/github/SciKit-Surgery/scikit-surgerycore/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/SciKit-Surgery/scikit-surgerycore?branch=master
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/scikit-surgerycore/badge/?version=latest
    :target: http://scikit-surgerycore.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/Cite-SciKit--Surgery-informational
   :target: https://doi.org/10.1007/s11548-020-02180-5
   :alt: The SciKit-Surgery paper

.. image:: https://img.shields.io/twitter/follow/scikit_surgery?style=social
   :target: https://twitter.com/scikit_surgery?ref_src=twsrc%5Etfw
   :alt: Follow scikit_surgery on twitter

Description
-----------

SciKit-SurgeryCore implements algorithms and tools that are common to all SciKit-Surgery packages.

SciKit-SurgeryCore is part of the `SciKit-Surgery`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.

.. features-start

Features
--------

* A `Configuration Manager <https://scikit-surgerycore.readthedocs.io/en/latest/module_ref.html#module-sksurgerycore.configuration.configuration_manager>`_ to load parameters from a .json file
* A `Transform Manager <https://scikit-surgerycore.readthedocs.io/en/latest/module_ref.html#module-sksurgerycore.transforms.transform_manager>`_ to manage combinations of 4x4 transformation matrices
* `Corresponding point <https://scikit-surgerycore.readthedocs.io/en/latest/module_ref.html#module-sksurgerycore.algorithms.procrustes>`_ (i.e Landmark) based registration, based on `Arun et al., 1987`_.
* `Rotaiton/translation Matrix construction <https://scikit-surgerycore.readthedocs.io/en/latest/module_ref.html#module-sksurgerycore.transforms.matrix>`_ and `validation functions <https://scikit-surgerycore.readthedocs.io/en/latest/module_ref.html#matrix-validation>`_, 
  checking a numpy array is a camera matrix, rotation matrix, rigid transform etc.

.. features-end

Citing
------
If you make use of SciKit-Surgery libraries in your work, please cite the following paper:


    | Thompson S, Dowrick T, Ahmad M, et al.
    | SciKit-Surgery: compact libraries for surgical navigation.
    | International Journal of Computer Assisted Radiology and Surgery. May 2020. 
    | DOI: 10.1007/s11548-020-02180-5


Installing
----------

You can pip install as follows:

::

    pip install scikit-surgerycore


Developing
----------

Cloning
^^^^^^^

You can clone the repository using the following command:

::

    git clone https://github.com/SciKit-Surgery/scikit-surgerycore.git


Running the tests
^^^^^^^^^^^^^^^^^

You can run the unit tests by installing and running tox:

::

    pip install tox
     tox


Contributing
^^^^^^^^^^^^

Please see the `contributing guidelines`_.

Useful links
^^^^^^^^^^^^

* `Source code repository`_
* `Documentation`_


Licensing and copyright
-----------------------

Copyright 2018 University College London.
scikit-surgerycore is released under the BSD-3 license. Please see the `license file`_ for details.


Acknowledgements
----------------

Supported by `Wellcome`_ and `EPSRC`_.


.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
.. _`source code repository`: https://github.com/SciKit-Surgery/scikit-surgerycore
.. _`Documentation`: https://scikit-surgerycore.readthedocs.io
.. _`SciKit-Surgery`: https://github.com/SciKit-Surgery/
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://github.com/SciKit-Surgery/scikit-surgerycore/blob/master/CONTRIBUTING.rst
.. _`license file`: https://github.com/SciKit-Surgery/scikit-surgerycore/blob/master/LICENSE
.. _`Arun et al., 1987`: http://doi.ieeecomputersociety.org/10.1109/TPAMI.1987.4767965
