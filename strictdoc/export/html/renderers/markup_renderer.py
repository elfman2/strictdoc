from typing import Optional, Type, Union

from strictdoc.backend.sdoc.models.document import Document
from strictdoc.backend.sdoc.models.inline_link import InlineLink
from strictdoc.backend.sdoc.models.requirement import (
    Requirement,
)
from strictdoc.backend.sdoc.models.section import FreeText
from strictdoc.core.traceability_index import TraceabilityIndex
from strictdoc.export.html.renderers.html_fragment_writer import (
    HTMLFragmentWriter,
)
from strictdoc.export.html.renderers.link_renderer import LinkRenderer
from strictdoc.export.html.renderers.text_to_html_writer import TextToHtmlWriter
from strictdoc.export.rst.rst_to_html_fragment_writer import (
    RstToHtmlFragmentWriter,
)
from strictdoc.helpers.rst import truncated_statement_with_no_rst


class MarkupRenderer:
    @staticmethod
    def create(
        markup,
        traceability_index: TraceabilityIndex,
        link_renderer: LinkRenderer,
        context_document: Optional[Document],
    ) -> "MarkupRenderer":
        html_fragment_writer: Union[
            RstToHtmlFragmentWriter,
            Type[HTMLFragmentWriter],
            Type[TextToHtmlWriter],
        ]
        if not markup or markup == "RST":
            html_fragment_writer = RstToHtmlFragmentWriter(
                context_document=context_document
            )
        elif markup == "HTML":
            html_fragment_writer = HTMLFragmentWriter
        else:
            html_fragment_writer = TextToHtmlWriter
        return MarkupRenderer(
            html_fragment_writer,
            traceability_index,
            link_renderer,
            context_document,
        )

    def __init__(
        self,
        fragment_writer,
        traceability_index: TraceabilityIndex,
        link_renderer: LinkRenderer,
        context_document: Optional[Document],
    ):
        assert isinstance(traceability_index, TraceabilityIndex)
        assert isinstance(link_renderer, LinkRenderer)
        assert context_document is None or isinstance(
            context_document, Document
        ), context_document

        self.fragment_writer = fragment_writer
        self.traceability_index = traceability_index
        self.link_renderer: LinkRenderer = link_renderer
        self.context_document: Optional[Document] = context_document

        self.cache = {}
        self.rationale_cache = {}

    def render_requirement_statement(self, requirement):
        assert isinstance(requirement, Requirement)
        assert self.context_document is not None

        if requirement in self.cache:
            return self.cache[requirement]
        output = self.fragment_writer.write(requirement.reserved_statement)
        self.cache[requirement] = output

        return output

    def render_truncated_requirement_statement(self, requirement):
        assert isinstance(requirement, Requirement), requirement
        assert requirement.reserved_statement is not None
        assert self.context_document is not None

        statement_to_render = truncated_statement_with_no_rst(
            requirement.reserved_statement
        )

        output = self.fragment_writer.write(statement_to_render)
        self.cache[requirement] = output

        return output

    def render_requirement_rationale(self, requirement):
        assert isinstance(requirement, Requirement)
        assert self.context_document is not None

        if requirement in self.rationale_cache:
            return self.rationale_cache[requirement]
        output = self.fragment_writer.write(requirement.rationale)
        self.rationale_cache[requirement] = output
        return output

    def render_comment(self, comment):
        assert isinstance(comment, str)
        assert self.context_document is not None

        if comment in self.cache:
            return self.cache[comment]
        output = self.fragment_writer.write(comment)
        self.cache[comment] = output
        return output

    def render_free_text(self, document_type, free_text):
        assert isinstance(free_text, FreeText)
        assert self.context_document is not None

        if (document_type, free_text) in self.cache:
            return self.cache[free_text]

        parts_output = ""
        for part in free_text.parts:
            if isinstance(part, str):
                parts_output += part
            elif isinstance(part, InlineLink):
                node = self.traceability_index.get_node_by_uid(part.link)
                href = self.link_renderer.render_requirement_link(
                    node, self.context_document, document_type
                )
                parts_output += self.fragment_writer.write_link(
                    node.title, href
                )
        output = self.fragment_writer.write(parts_output)
        self.cache[(document_type, free_text)] = output

        return output

    def render_meta_value(self, meta_field_value):
        assert isinstance(meta_field_value, str)
        assert self.context_document is not None

        if meta_field_value in self.cache:
            return self.cache[meta_field_value]

        output = self.fragment_writer.write(meta_field_value)
        self.cache[meta_field_value] = output

        return output
