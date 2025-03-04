.. _SDOC_BL:

Backlog
$$$$$$$

This document outlines the future work items for StrictDoc.

The following items are listed in descending order of priority, with the topmost items either currently in progress or scheduled to be implemented next.

While this backlog overlaps with StrictDoc's `GitHub issues tracker <https://github.com/strictdoc-project/strictdoc/issues>`_ by more than 50%, it includes more strategic items compared to the GitHub issues, which are primarily focused on actual implementation work.

.. _SDOC_BL_WEB:

Backlog: Web-based user interface
=================================

- Uploading images via Web interface.

- Deleting sections recursively. Correct clean-up of all traceability information.

- Editing remaining document options: Inline/Table, Requirements in TOC, etc.

- Requirement form:

  - Adding/editing parent/child requirements: validation of cycles.

- Integration with Git repository. Make the server commit changes to .sdoc files automatically. To a user, provide visibility to what happens under the hood.

- Section form:

  - ``UID``
  - Show incoming/outgoing links.
  - Links between sections and documents.

- User support - Sign In, Sign Out, Register.

- Option to keep all multi-line text fields to 80 symbols width.

- Moving node up/down/left/right. For example, move a node of level 2 to level 1.

  - Follow-up feature: moving nodes between documents.

- TBL view:

  - Column filters to show/hide columns.
  - Completely empty columns are hidden by default.

- All forms:

  - Contextual help about the RST markup.
  - How to edit tables conveniently?

- What to do with web content going out of sync with the server/file system state?

- Issue when adding a child section from a nested section. The child
  section appears right after the nested section, not after its farthest
  descendant child.

- ReqIF:

  - Export complete documentation tree or a single document to ReqIF.
  - Import complete documentation tree or a single document from ReqIF.

- Other:

  - Focused editing of document sections: dedicated and focused ``/sections/`` resource.
  - Non-RST markup formats.

Backlog: Nice to have
=====================

- Configuration file options:

  - CLI command to dump default config file
  - Project prefix?
  - Explicit or wildcard paths to sdoc files.
  - Exclude folders when searching \*.sdoc.
  - Paths to dirs with source files.
  - Config options for presenting requirements.
    - Include/exclude requirements in TOC

- Diff for requirements documents and documentation trees.

- Impact analysis. Most likely a separate screen that shows which requirements a given requirements affects.

- StrictDoc as a Python library.

  - Such a use allows a more fine-grained access to the StrictDoc's modules, such as Grammar, Import, Export classes, etc.

- Data exchange with Capella tool.

  - Note: The current idea would be to implement this using ReqIF export/import features.

- Language Server Protocol.

  - The LSP can enable editing of SDoc files in IDEs like Eclipse, Visual Studio, PyCharm. A smart LSP can enable features like syntax highlighting, autocompletion and easy navigation through requirements.

  - The promising base for the implementation: https://github.com/openlawlibrary/pygls.

- StrictDoc shall support rendering text/code blocks into Markdown syntax.

- Fuzzy requirements search.

  - This feature can be implemented in the CLI as well as in the future GUI. A fuzzy requirements search can help to find existing requirements and also identify relevant requirements when creating new requirements.

- Support creation of FMEA/FMECA safety analysis documents.

- Calculation of checksums for requirements.

  - This feature is relatively easy to implement, but the implementation is postponed until the linking between requirements and files is implemented.

- Filtering of requirements by tags.

- Import/export: Excel, CSV, PlantUML, Confluence, Tex, Doorstop.

- Partial evaluation of Jinja templates

  - Many of the template variables could be made to be evaluated once, for example, config object's variables.

- UI version for mobile devices (at least some basic tweaks)

Backlog: Technical debt
=======================

- When a document is added, the whole documentation is rebuilt from the file system from scratch. A more fine-grained re-indexing of documentation tree can be implemented. The current idea is to introduce a layer of pickled cached data: preserve the whole in-memory traceability graph in a cache, and then use the cached data for making decisions about what should be regenerated.
- The "no framework" approach with FastAPI and Turbo/Stimulus allows writing almost zero Javascript, however some proto-framework conventions are still needed. Currently, all code is written in the ``main_controller`` which combines all responsibilities, such as parsing HTTP request fields, accessing traceability graph, validations, rendering back the updated AJAX templates. A lack of abstraction is better than a poor abstraction, but some solution has to be found.
- Request form object vs Response form object. The workflow of form validations is not optimal.
- For Web development, the responsibilities of the ``TraceabilityIndex`` class compared to the ``ExportAction``, ``MarkupRenderer``, ``LinkRenderer`` classes are unstable. A more ecological composition of classes has to be found. ``Traceability`` index is rightfully a "god object" because it contains all information about the in-memory documentation graph.

Backlog: Known issues
=====================



HTML rendering using docutils is a performance bottleneck
---------------------------------------------------------

The overall generation process is still fast enough but in case some improvements were to be made:

- It could be measured what takes more time: parsing RST tree or actually rendering HTML
- Simplified RST parser and rendered can be written and their performance can be compared with that of docutils API.

.. code-block:: bash

    python -m cProfile -s cumulative strictdoc/cli/main.py export --no-parallelization docs/ > report.txt

See also: https://docs.python.org/3/library/profile.html#instant-user-s-manual

Document archetypes
===================

StrictDoc shall support the following document archetypes: **requirements document**
and **specification** document. For both archetypes, StrictDoc shall further
support the following options.

.. list-table:: Table: Requirements and specification document
   :widths: 20 40 40
   :header-rows: 1

   * -
     - Requirements document
     - Specification document
   * - Examples
     - Most typical: requirements lists split by categories (e.g., Functional
       Requirements, Interface Requirements, Performance Requirements, etc.)
     - Often: a standard document
   * - Structure
     - Not nested or not too deeply nested
     - Nested
   * - Visual presentation
     - Requirements are often presented as table cells. Cells can be standalone
       or the whole section or document can be a long table with cells.
     - Requirements are rather presented as header + text
   * - Unique requirement identifiers (UID)
     - Most always
     - - Present or not
       - **NOT SUPPORTED YET:** Can be missing, the chapter headers are used instead.
         The combination "Number + Title" becomes a reference-able identifier.
         A possible intermediate solution when modeling such a document is to
         make the UIDs map to the section number.
   * - Requirement titles
     - - Often
       - **NOT SUPPORTED YET:** But maybe absent (ex: NASA cFS SCH). If absent,
         the grouping is provided by sections.
     - Requirement titles are most often section titles
   * - Real-world examples
     - - NASA cFE Functional Requirements
       - MISRA C coding guidelines,
       - NASA Software Engineering Requirements NPR 7150.2
     - - ECSS Software ECSS-E-ST-40C

**Comment:** This draft requirement is the first attempt to organize this information.

Open questions
==============

One or many input sdoc trees
----------------------------

StrictDoc supports this for HTML already but not for RST.

When passed
``strictdoc export ... /path/to/doctree1, /path/to/doctree2, /path/to/doctree3``,
the following is generated:

.. code-block:: text

    output folder:
    - doctree1/
      - contents
    - doctree2/
      - contents
    - doctree3/
      - contents

and all three doctrees' requirements are merged into a single documentation
space with cross-linking possible.

The question is if it is worth supporting this case further or StrictDoc should
only work with one input folder with a single doc tree.
