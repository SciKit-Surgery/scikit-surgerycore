scikit-surgerycore
===============================

.. image:: https://github.com/UCL/scikit-surgerycore /raw/master/project-icon.png 
   :height: 128px
   :width: 128px
   :target: https://github.com/UCL/scikit-surgerycore
   :alt: Logo

.. image:: https://github.com/UCL/scikit-surgerycore/workflows/.github/workflows/ci.yml/badge.svg
   :target: https://github.com/UCL/scikit-surgerycore/actions
   :alt: GitHub Actions CI status

.. image:: https://coveralls.io/repos/github/UCL/scikit-surgerycore/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/UCL/scikit-surgerycore?branch=master
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/scikit-surgerycore/badge/?version=latest
    :target: http://scikit-surgerycore.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


scikit-surgerycore implements algorithms and tools that are common to all scikit-surgery packages.

scikit-surgerycore is part of the `SNAPPY`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.

Features
--------

* A Configuration Manager to load parameters from a .json file
* A Transform Manager to manage combinations of 4x4 transformation matrices
* Corresponding point (i.e Landmark) based registration, based on `Arun et al., 1987`_.
* Validation functions, checking a numpy array is a camera matrix, rotation matrix, rigid transform etc.

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

    git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerycore


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
.. _`source code repository`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerycore
.. _`Documentation`: https://scikit-surgerycore.readthedocs.io
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerycore/blob/master/CONTRIBUTING.rst
.. _`license file`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerycore/blob/master/LICENSE
.. _`Arun et al., 1987`: http://doi.ieeecomputersociety.org/10.1109/TPAMI.1987.4767965

