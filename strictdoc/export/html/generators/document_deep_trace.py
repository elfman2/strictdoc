from strictdoc import __version__
from strictdoc.core.document_tree_iterator import DocumentTreeIterator
from strictdoc.export.html.document_type import DocumentType
from strictdoc.export.html.html_templates import HTMLTemplates
from strictdoc.export.html.renderers.link_renderer import LinkRenderer


class DocumentDeepTraceHTMLGenerator:
    env = HTMLTemplates.jinja_environment

    @staticmethod
    def export_deep(
        config,
        document,
        traceability_index,
        markup_renderer,
        link_renderer: LinkRenderer,
    ):
        output = ""

        document_tree_iterator = DocumentTreeIterator(
            traceability_index.document_tree
        )

        template = DocumentDeepTraceHTMLGenerator.env.get_template(
            "screens/document/traceability_deep/index.jinja"
        )

        document_iterator = traceability_index.get_document_iterator(document)

        output += template.render(
            config=config,
            document=document,
            traceability_index=traceability_index,
            renderer=markup_renderer,
            link_renderer=link_renderer,
            document_type=DocumentType.deeptrace(),
            standalone=False,
            document_iterator=document_iterator,
            strictdoc_version=__version__,
            document_tree=traceability_index.document_tree,
            document_tree_iterator=document_tree_iterator,
        )

        return output
