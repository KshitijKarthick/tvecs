.. T-Vecs documentation master file, created by
   sphinx-quickstart on Thu Apr  7 14:21:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to T-Vecs's documentation!
==================================

The main documentation for the site is organized into a couple sections:

User Documentation
------------------

.. _user-docs:

.. toctree::

   README

Development Documentation
-------------------------

* :ref:`dev-developer-docs`
    * :ref:`dev-visualization-docs`
    * :ref:`dev-preprocessor-docs`
    * :ref:`dev-model-generation-docs`
    * :ref:`dev-bilingual-generation-docs`
    * :ref:`dev-vector-space-mapper-docs`
    * :ref:`dev-analysis-docs`


.. _dev-developer-docs:

.. toctree::
   :caption: Development Documentation
   :titlesonly:

.. _dev-visualization-docs:

.. toctree::
    :titlesonly:
    :caption: Visualization Developer Documentation
    :hidden:

.. automodule:: visualization.server
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-preprocessor-docs:

.. toctree::
    :maxdepth: 2
    :caption: Preprocessor Documentation
    :hidden:

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

.. automodule:: modules.preprocessor.leipzig_preprocessor
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
    :hidden:

.. automodule:: modules.model_generator.model_generation
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-bilingual-generation-docs:

.. toctree::
    :maxdepth: 2
    :caption: Bilingual Dictionary Generator Documentation
    :hidden:

.. automodule:: modules.bilingual_generator.clustering
    :members:
    :inherited-members:
    :show-inheritance:

.. automodule:: modules.bilingual_generator.bilingual_generator
    :members:
    :inherited-members:
    :show-inheritance:

.. _dev-vector-space-mapper-docs:

.. toctree::
    :maxdepth: 2
    :caption: Vector Space Mapper Documentation
    :hidden:

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
    :hidden:

.. automodule:: modules.analysis.multivariate
    :members:
    :inherited-members:
    :show-inheritance:


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
