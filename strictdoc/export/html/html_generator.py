import os
from functools import partial
from pathlib import Path

from strictdoc.backend.sdoc.models.document import Document
from strictdoc.cli.cli_arg_parser import ExportCommandConfig, ExportMode
from strictdoc.core.document_meta import DocumentMeta
from strictdoc.core.project_config import ProjectConfig, ProjectFeature
from strictdoc.core.source_tree import SourceTree
from strictdoc.core.traceability_index import TraceabilityIndex
from strictdoc.export.html.generators.document import DocumentHTMLGenerator
from strictdoc.export.html.generators.document_deep_trace import (
    DocumentDeepTraceHTMLGenerator,
)
from strictdoc.export.html.generators.document_table import (
    DocumentTableHTMLGenerator,
)
from strictdoc.export.html.generators.document_trace import (
    DocumentTraceHTMLGenerator,
)
from strictdoc.export.html.generators.document_tree import (
    DocumentTreeHTMLGenerator,
)
from strictdoc.export.html.generators.requirements_coverage import (
    RequirementsCoverageHTMLGenerator,
)
from strictdoc.export.html.generators.source_file_coverage import (
    SourceFileCoverageHTMLGenerator,
)
from strictdoc.export.html.generators.source_file_view_generator import (
    SourceFileViewHTMLGenerator,
)
from strictdoc.export.html.renderers.link_renderer import LinkRenderer
from strictdoc.export.html.renderers.markup_renderer import MarkupRenderer
from strictdoc.export.html.tools.html_embedded import HTMLEmbedder
from strictdoc.helpers.file_system import sync_dir
from strictdoc.helpers.timing import measure_performance


class HTMLGenerator:
    @staticmethod
    def export_tree(
        *,
        project_config: ProjectConfig,
        config: ExportCommandConfig,
        traceability_index: TraceabilityIndex,
        parallelizer,
    ):  # pylint: disable=too-many-arguments,too-many-statements
        # Export document tree.
        HTMLGenerator.export_document_tree(
            config=config, traceability_index=traceability_index
        )

        # Export StrictDoc's own assets.
        output_html_static_files = os.path.join(
            config.output_html_root, config.dir_for_sdoc_assets
        )
        sync_dir(config.get_static_files_path(), output_html_static_files)

        # Export MathJax
        if (
            project_config.is_feature_activated(ProjectFeature.MATHJAX)
            or config.enable_mathjax
        ):
            output_html_mathjax = os.path.join(
                config.output_html_root, config.dir_for_sdoc_assets, "mathjax"
            )
            Path(output_html_mathjax).mkdir(parents=True, exist_ok=True)
            mathjax_src = os.path.join(
                config.get_extra_static_files_path(), "mathjax"
            )
            sync_dir(mathjax_src, output_html_mathjax)

        # Export project's assets.
        for asset_dir in traceability_index.asset_dirs:
            source_path = asset_dir["full_path"]
            output_relative_path = asset_dir["relative_path"]
            destination_path = os.path.join(
                config.output_html_root, output_relative_path
            )
            sync_dir(source_path, destination_path)

        export_binding = partial(
            HTMLGenerator._export_with_performance,
            project_config,
            config,
            traceability_index=traceability_index,
        )

        parallelizer.map(
            traceability_index.document_tree.document_list, export_binding
        )

        # Export requirements coverage.
        if (
            project_config.is_feature_activated(
                ProjectFeature.REQUIREMENTS_COVERAGE_SCREEN
            )
            or config.enable_mathjax
        ):
            requirements_coverage_content = (
                RequirementsCoverageHTMLGenerator.export(
                    config,
                    traceability_index,
                )
            )
            output_html_requirements_coverage = os.path.join(
                config.output_html_root, "requirements_coverage.html"
            )
            with open(
                output_html_requirements_coverage, "w", encoding="utf8"
            ) as file:
                file.write(requirements_coverage_content)

        # Export source coverage.
        if (
            project_config.is_feature_activated(
                ProjectFeature.REQUIREMENT_TO_SOURCE_TRACEABILITY
            )
            or config.experimental_enable_file_traceability
        ):
            assert isinstance(
                traceability_index.document_tree.source_tree, SourceTree
            ), traceability_index.document_tree.source_tree
            print("Generating source files:")  # noqa: T201
            for (
                source_file
            ) in traceability_index.document_tree.source_tree.source_files:
                if not source_file.is_referenced:
                    continue

                with measure_performance(
                    f"File: {source_file.in_doctree_source_file_rel_path}"
                ):
                    Path(source_file.output_dir_full_path).mkdir(
                        parents=True, exist_ok=True
                    )
                    document_content = SourceFileViewHTMLGenerator.export(
                        config,
                        source_file,
                        traceability_index,
                    )
                    with open(
                        source_file.output_file_full_path, "w", encoding="utf-8"
                    ) as file:
                        file.write(document_content)

            source_coverage_content = SourceFileCoverageHTMLGenerator.export(
                config=config,
                traceability_index=traceability_index,
            )
            output_html_source_coverage = os.path.join(
                config.output_html_root, "source_coverage.html"
            )
            with open(
                output_html_source_coverage, "w", encoding="utf8"
            ) as file:
                file.write(source_coverage_content)

        print(  # noqa: T201
            "Export completed. Documentation tree can be found at:\n"
            f"{config.output_html_root}"
        )

    @staticmethod
    def _export_with_performance(
        project_config: ProjectConfig,
        config: ExportCommandConfig,
        document,
        traceability_index,
    ):
        if not config.is_running_on_server and not document.ng_needs_generation:
            with measure_performance(f"Skip: {document.title}"):
                return
        with measure_performance(f"Published: {document.title}"):
            HTMLGenerator.export_single_document(
                project_config,
                config,
                document,
                traceability_index,
            )

    @staticmethod
    def export_single_document(
        project_config: ProjectConfig,
        config: ExportCommandConfig,
        document: Document,
        traceability_index,
    ):
        export_mode = config.get_export_mode()
        assert document.meta is not None

        document_meta: DocumentMeta = document.meta

        document_output_folder = document_meta.output_document_dir_full_path
        Path(document_output_folder).mkdir(parents=True, exist_ok=True)

        root_path = document.meta.get_root_path_prefix()
        link_renderer = LinkRenderer(
            root_path=root_path, static_path=config.dir_for_sdoc_assets
        )
        markup_renderer = MarkupRenderer.create(
            document.config.markup,
            traceability_index,
            link_renderer,
            document,
        )

        if export_mode in (
            ExportMode.DOCTREE,
            ExportMode.DOCTREE_AND_STANDALONE,
        ):
            # Single Document pages
            document_content = DocumentHTMLGenerator.export(
                config,
                document,
                traceability_index,
                markup_renderer,
                link_renderer,
                standalone=False,
            )
            document_out_file = document_meta.get_html_doc_path()
            with open(document_out_file, "w", encoding="utf8") as file:
                file.write(document_content)

            # Single Document Table pages
            if project_config.is_feature_activated(ProjectFeature.TABLE_SCREEN):
                document_content = DocumentTableHTMLGenerator.export(
                    config,
                    document,
                    traceability_index,
                    markup_renderer,
                    link_renderer,
                )
                document_out_file = document_meta.get_html_table_path()
                with open(document_out_file, "w", encoding="utf8") as file:
                    file.write(document_content)

            # Single Document Traceability pages
            if project_config.is_feature_activated(
                ProjectFeature.TRACEABILITY_SCREEN
            ):
                document_content = DocumentTraceHTMLGenerator.export(
                    config,
                    document,
                    traceability_index,
                    markup_renderer,
                    link_renderer,
                )
                document_out_file = document_meta.get_html_traceability_path()
                with open(document_out_file, "w", encoding="utf8") as file:
                    file.write(document_content)

            # Single Document Deep Traceability pages
            if project_config.is_feature_activated(
                ProjectFeature.DEEP_TRACEABILITY_SCREEN
            ):
                document_content = DocumentDeepTraceHTMLGenerator.export_deep(
                    config,
                    document,
                    traceability_index,
                    markup_renderer,
                    link_renderer,
                )
                document_out_file = (
                    document_meta.get_html_deep_traceability_path()
                )
                with open(document_out_file, "w", encoding="utf8") as file:
                    file.write(document_content)

        if project_config.is_feature_activated(
            ProjectFeature.STANDALONE_DOCUMENT_SCREEN
        ) or export_mode in (
            ExportMode.STANDALONE,
            ExportMode.DOCTREE_AND_STANDALONE,
        ):
            # Single Document pages (standalone)
            document_content = DocumentHTMLGenerator.export(
                config,
                document,
                traceability_index,
                markup_renderer,
                link_renderer,
                standalone=True,
            )
            document_out_file = document_meta.get_html_doc_standalone_path()
            document_content_with_embedded_assets = HTMLEmbedder.embed_assets(
                document_content, document_out_file
            )
            with open(document_out_file, "w", encoding="utf8") as file:
                file.write(document_content_with_embedded_assets)

        return document

    @staticmethod
    def export_document_tree(
        *,
        config: ExportCommandConfig,
        traceability_index: TraceabilityIndex,
    ):
        output_file = os.path.join(config.output_html_root, "index.html")
        writer = DocumentTreeHTMLGenerator()
        output = writer.export(config, traceability_index=traceability_index)
        with open(output_file, "w", encoding="utf8") as file:
            file.write(output)
