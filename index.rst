.. T-Vecs documentation master file, created by
   sphinx-quickstart on Thu Apr  7 14:21:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to T-Vecs's documentation!
==================================

The main documentation for the site is organized into a couple sections:

* :ref:`user-docs`
* :ref:`dev-developer-docs`

Development documentation is categorized into:

* :ref:`dev-visualization-docs`
* :ref:`dev-preprocessor-docs`
* :ref:`dev-model-generation-docs`
* :ref:`dev-bilingual-generation-docs`
* :ref:`dev-vector-space-mapper-docs`
* :ref:`dev-analysis-docs`

.. _user-docs:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   README

.. _dev-developer-docs:
.. toctree::
   :maxdepth: 2
   :caption: Development Documentation


.. _dev-visualization-docs:

.. toctree::
    :maxdepth: 2
    :caption: Visualization Developer Documentation

.. automodule:: visualization.server
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-preprocessor-docs:

.. toctree::
    :maxdepth: 2
    :caption: Preprocessor Documentation

.. automodule:: modules.preprocessor.base_preprocessor
    :members:
    :inherited-members:
    :show-inheritance:

.. automodule:: modules.preprocessor.hccorpus_preprocessor
    :members:
    :inherited-members:
    :show-inheritance:

.. automodule:: modules.preprocessor.emille_preprocessor
    :members:
    :inherited-members:
    :show-inheritance:

.. automodule:: modules.preprocessor.yandex_api
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-model-generation-docs:

.. toctree::
    :maxdepth: 2
    :caption: Model Generator Documentation

.. automodule:: modules.model_generator.model_generation
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-bilingual-generation-docs:

.. toctree::
    :maxdepth: 2
    :caption: Bilingual Dictionary Generator Documentation

.. automodule:: modules.bilingual_generator.clustering
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-vector-space-mapper-docs:

.. toctree::
    :maxdepth: 2
    :caption: Vector Space Mapper Documentation

.. automodule:: modules.vector_space_mapper.vector_space_mapper
    :members:
    :inherited-members:
    :show-inheritance:

.. automodule:: modules.evaluation.evaluation
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-analysis-docs:

.. toctree::
    :maxdepth: 2
    :caption: Multivariate Analysis Documentation

.. automodule:: modules.analysis.multivariate
    :members:
    :inherited-members:
    :show-inheritance:


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
