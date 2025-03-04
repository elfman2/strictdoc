.. _SDOC_FAQ:

F.A.Q.
$$$$$$

This document is a list of questions that people ask about StrictDoc.

Missing a question or an answer? Ask it here: :ref:`SDOC_UG_CONTACT`.

What is StrictDoc?
==================

StrictDoc is software for writing technical requirements specifications.

StrictDoc is a spare-time open-source project developed by Stanislav Pankevich (@stanislaw) and Maryna Balioura (@mettta) with contributions from the Open Source community.

The project exists since mid-2019.

Resources about StrictDoc
=========================

Blog posts:

- `Requirement Traceability with All Substance and No Fuss
  <https://www.bugseng.com/blog/requirement-traceability-all-substance-and-no-fuss>`_
  by BUGSENG.

- `Text-Based Requirement Management with StrictDoc
  <https://python.plainenglish.io/text-based-requirement-management-with-strictdoc-b03c1098a3c9>`_
  by Florian Kromer.

Screencasts/tutorials:

- `Automotive SPICE in opensource StrictDoc tool, with System Architecure ideas
  <https://www.youtube.com/watch?v=k2MCFWvCs7E>`_
  by Lukasz Juranek.

Which web server is recommended for StrictDoc documentation?
============================================================

Is your project public or private? If it is public, you could simply use `GitHub pages <https://pages.github.com>`_. See how one user of StrictDoc is doing it here: `nmfta-repo/vcr-experiment <https://github.com/nmfta-repo/vcr-experiment>`_ and the resulting static website: `nmfta-repo.github.io/vcr-experiment <https://nmfta-repo.github.io/vcr-experiment>`_.

If the project is private, you could use any server that reads HTML files from a folder. For example, Python has an embedded Web Server, see `this for example <https://pythonbasics.org/webserver>`_. Also you could try any web server based on Node.JS.

How did the SDoc text language become what it is?
=================================================

Shortly: The SDoc markup is a hybrid of TOML and YAML with some influence from HTML/XML and `ASN.1 <https://en.wikipedia.org/wiki/ASN.1>`_. Using each of these formats as-is, and also the JSON format, was considered but discarded during the design. The SDoc markup has been pretty stable since its inception but the flexibility of the TextX parser allows easy modifications of the language in case of future evolutions. Any feedback to the current design of the markup language is appreciated.

----

The main use case for SDoc is to model a structure of a technical document that consists of tens and hundreds of technical requirements. The following high-level requirements for the markup are therefore relevant:

- Encode documents of reasonable size (up to several hundreds or few thousands of A4-printed pages).
- Visualize large blocks of requirements text without too much markup noise.
- Support documents with nested (2-4 levels) or deeply nested structure (detailed technical specifications with up to 9-10 levels of chapter nesting).
- Support multiple fields for requirement meta information which makes a requirement look like "a text with some meta information around it".

SDoc format is inspired by several formats: TOML, YAML, ASN.1 and HTML/XML.

**TOML: Square bracket syntax**

From TOML, StrictDoc borrowed the ``[]`` bracket syntax to create the ``[REQUIREMENT]``, ``[SECTION]`` and other blocks but uses the YAML-like syntax for these blocks' fields, for example:

.. code-block::

    [REQUIREMENT]
    TITLE: Requirement ABC
    STATEMENT: The system A shall do B when C.

**TOML/YAML: Arrays/dictionaries**

StrictDoc has a rudimentary support of arrays and dictionaries. For example, the syntax for defining the document's ``[GRAMMAR]`` resembles what would look like an array of records in YAML:

.. code-block::

    [GRAMMAR]
    ELEMENTS:
    - TAG: REQUIREMENT
      FIELDS:
      - TITLE: UID
        TYPE: String
        REQUIRED: True
      - TITLE: LEVEL
        TYPE: String
        REQUIRED: False

**Capitalization of reserved keywords from ASN.1**

From ASN.1, StrictDoc borrows the idea of having all reserved fields capitalized. This helps to visually distinguish between the grammar content and user content.

**Nested sections**

From HTML, the idea of opening and closing tags is taken to avoid any nesting that would otherwise be required to support the deeply nested documents with up to 6 or 8 levels, e.g., 1.1.1.1.1.1.1...

.. code-block::

    [SECTION]
    TITLE: Section 1

    [SECTION]
    TITLE: Section 1.1

    ...

    [/SECTION]

    [/SECTION]

Taking HTML or XML as-is didn't seem like a good option because of the heavy visual noise that is produced around the actual content by the surrounding tags.

**Multiline strings**

The support of multiline strings is arranged by a custom solution which helps to avoid any nesting of multiline text as well as to visually indicate the start and end parts of the multiline string in a visually unambiguous way. This is how the multiline string is declared:

.. code-block::

    [REQUIREMENT]
    TITLE: Requirement ABC
    STATEMENT: >>>
    The multiline requirement statement
    without any nesting.
    >>>

**Discarded options**

Taking TOML or YAML as-is didn't seem like a good option because these formats are designed to be used for configuration files or data serialization and not for large documents with hundreds of requirements. The most obvious problems for reusing either of TOML or YAML directly would have been with encoding the deeply nested documents and supporting readable and non-nested multiline strings (see also about the multiline strings below).

How StrictDoc compares to other tools?
======================================

Doorstop
--------

The StrictDoc project is a close successor of another project called
`Doorstop <https://github.com/doorstop-dev/doorstop>`_.

    Doorstop is a requirements management tool that facilitates the storage of
    textual requirements alongside source code in version control.

The author of Doorstop has published a `paper about Doorstop <http://www.scirp.org/journal/PaperInformation.aspx?PaperID=44268#.UzYtfWRdXEZ>`_
where the rationale behind text-based requirements management is provided.

The first version of StrictDoc had started as a fork of the Doorstop project.
However, after a while, the StrictDoc was started from scratch as a separate
project. At this point, StrictDoc and Doorstop do not share any code but
StrictDoc still shares with Doorstop their common underlying design principles:

- Both Doorstop and StrictDoc are written using Python. Both are pip packages which are easy-to-install.
- Both Doorstop and StrictDoc provide a command-line interface.
- Both Doorstop and StrictDoc use text files for requirements management.
- Both Doorstop and StrictDoc encourage collocation of code and documentation.
  When documentation is hosted close to code it has less chances of diverging
  from the actual implementation or becoming outdated.
- As the free and open source projects, both Doorstop and StrictDoc seem to
  struggle to find resources for development of specialized GUI interfaces this
  is why both tools give a preference to supporting exporting documentation
  pages to HTML format as the primary export feature.

StrictDoc differs from Doorstop in a number of aspects:

- Doorstop stores requirements in YAML files, one separate file per requirement
  (`example <https://github.com/doorstop-dev/doorstop/blob/804153c67c7c5466ee94e9553118cc3df03a56f9/reqs/REQ001.yml>`_).
  The document in Doorstop is assembled from the requirements files into a
  single logical document during the document generation process.
  StrictDoc's documentation unit is one document stored in an .sdoc file. Such a
  document can have multiple requirements grouped by sections.
- In YAML files, Doorstop stores requirements properties such as
  ``normative: true`` or ``level: 2.3`` for which Doorstop provides validations.
  Such a design decision, in fact, assumes an existence of implicitly-defined
  grammar which is encoded "ad-hoc" in the parsing and validation rules of
  Doorstop.
  StrictDoc takes a different approach and defines its grammar explicitly using
  a tool for creating Domain-Specific Languages called `textX <https://github.com/textX/textX>`_.
  TextX support allows StrictDoc to encode a strict type-safe grammar in a
  `single grammar file <https://github.com/strictdoc-project/strictdoc/blob/93486a0e9fb30b141187587eae9e995cd86c6cbf/strictdoc/backend/dsl/grammar.py>`_
  that StrictDoc uses to parse the documentation files
  using the parsing capabilities provided by textX out of the box.

The roadmap of StrictDoc contains a work item for supporting the export/import
to/from Doorstop format.

Sphinx
------

Both Sphinx and StrictDoc are both documentation generators but StrictDoc is at
a higher level of abstraction: StrictDoc's specialization is requirements and
specifications documents. StrictDoc can generate documentation to a number of
formats including HTML format as well as the RST format which is a default
input format for Sphinx. A two stage generation is therefore possible:
StrictDoc generates RST documentation which then can be generated to HTML, PDF,
and other formats using Sphinx.

If you are reading this documentation at
https://strictdoc.readthedocs.io/en/latest
then you are already looking at the example: this documentation stored in
`strictdoc_02_faq <https://github.com/strictdoc-project/strictdoc/blob/main/docs/strictdoc_02_faq.sdoc>`_
is converted to RST format by StrictDoc which is further converted to the HTML
website by readthedocs which uses Sphinx under the hood. The
``StrictDoc -> RST -> Sphinx -> PDF`` example is also generated using readthedocs:
`StrictDoc <https://strictdoc.readthedocs.io/_/downloads/en/latest/pdf/>`_.

Sphinx-Needs
------------

`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_ is a
text-based requirements management system based on Sphinx. It is implemented
as a Sphinx extension which extends the
`reStructuredText (RST)
<https://docutils.sourceforge.io/docs/user/rst/quickref.html>`_
markup language with an additional syntax for writing requirements documents.

Sphinx-Needs was a great source of inspiration for the second version of
StrictDoc which was first implemented as a Sphinx extension and then as a more
independent library on top of `docutils <https://docutils.sourceforge.io/>`_
that Sphinx uses for the underlying RST syntax processing work.

The similarities between Sphinx-Needs and StrictDoc:

- In contrast to Doorstop, both Sphinx-Needs and StrictDoc do not split a
  document into many small files, one file per single requirement (see
  discussion
  `doorstop#401 <https://github.com/doorstop-dev/doorstop/issues/401>`_). Both
  tools follow the "file per document" approach.
- Sphinx-Needs has a
  `well-developed language
  <https://sphinxcontrib-needs.readthedocs.io/en/latest/directives/index.html>`_
  based on custom RST directives, such
  as ``req::``, ``spec::``, ``needtable::``, etc. The RST document is parsed
  by Sphinx/docutils into RST abstract syntax tree (AST) which allows creating
  an object graph out for the documents and their requirements from the RST
  document. StrictDoc uses textX for building an AST from a SDoc document.
  Essentially, both Sphinx-Needs and StrictDoc work in a similar way but use
  different markup languages and tooling for the job.

The difference between Sphinx-Needs and StrictDoc:

- RST tooling provided by Sphinx/docutils is very powerful, yet it can also be
  rather limiting. The RST syntax and underlying docutils tooling do not allow
  much flexibility needed for creating a language for defining requirements
  using a custom and explicit grammar, a feature that became a cornerstone of
  StrictDoc. This was a major reason why the third generation of
  StrictDoc started with a migration from docutils to
  `textX <https://github.com/textX/textX>`_ which is a
  dedicated tool for creating custom Domain-Specific Languages. After the
  migration to textX, StrictDoc is no longer restricted to the limitations of
  the RST document but it is still possible to generate SDoc files to RST
  using StrictDoc and then further generate RST to HTML/PDF and other formats
  using Sphinx.
- Sphinx-Needs has an impressive list of config options and features that
  StrictDoc is missing. Examples: Customizing the look of the requirements,
  `Roles <https://sphinxcontrib-needs.readthedocs.io/en/latest/roles.html>`_,
  `Services
  <https://sphinxcontrib-needs.readthedocs.io/en/latest/services/index.html>`_
  and
  `others
  <https://sphinxcontrib-needs.readthedocs.io/en/latest/index.html>`_.

FRET
----

`FRET <https://github.com/NASA-SW-VnV/fret>`_ is a framework for the
elicitation, specification, formalization and understanding of requirements.

    - Users enter system requirements in a specialized natural language.
    - FRET helps understanding and review of semantics by utilizing a variety of forms
      for each requirement: natural language description, formal mathematical logics,
      and diagrams.
    - Requirements can be defined in a hierarchical fashion and can be exported
      in a variety of forms to be used by analysis tools.

FRET has an impressive list of
`Publications <https://github.com/NASA-SW-VnV/fret/blob/master/PUBLICATIONS.md>`_.

FRET's user interface is built with Electron.

The detailed comparison is coming.

How long has the StrictDoc project been around?
===============================================

The first StrictDoc commit dates back to ``2019-08-10``. A short development chronology of StrictDoc is as follows:

**2019 – July – August**

StrictDoc is a result of several attempts to find a solution for working with
text-based requirements. The first version of StrictDoc had started as a fork of the Doorstop project. However, after a while, StrictDoc was started from scratch as a separate project.

**2019 – August**

StrictDoc, first generation, the first commit dates to ``2019-08-10``. Markdown-based C++ program. Custom requirements metadata in YAML.

**2020 – January**

StrictDoc, second generation: RST/Sphinx-based Python program. Using Sphinx extensions to manage meta information.

**2020 – May**

The current StrictDoc repository was created on GitHub: the first commit dates back ``2020-05-14``. The code still uses RST for parsing requirements meta information and PySide for GUI.

The result of these efforts was the realization that a text-based requirements and specifications management tool could be built on top of a domain-specific language (DSL) created specifically for the purpose of writing requirements and specifications documents. Such a language allows explicit definition of a document data model which is called "grammar".

**2020 – July**

The custom RST parser was replaced with a TextX-based DSL. Since then, StrictDoc has been using TextX for parsing SDoc files.

**2022 – November**

The FastAPI/Turbo/Stimulus-based Web interface prototype was created to complement the text-based interface with a graphical user interface (GUI). When the Web-based GUI is stable, StrictDoc may become useable by non-programmers too.

Which StrictDoc statistics are available?
=========================================

Most relevant GitHub statistics:

- `Contributors <https://github.com/strictdoc-project/strictdoc/graphs/contributors>`_

The `pip trends <https://piptrends.com>`_ helps to visualize the Pip package download stats. The ``reqif`` satellite project is included for comparison as well:
`strictdoc vs reqif <https://piptrends.com/compare/strictdoc-vs-reqif>`_.
