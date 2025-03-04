from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.helpers.constants import BROKEN_RST_MARKUP
from tests.end2end.helpers.screens.document.form_edit_requirement import (
    Form_EditRequirement,
)
from tests.end2end.helpers.screens.project_index.screen_project_index import (
    Screen_ProjectIndex,
)
from tests.end2end.server import SDocTestServer


class Test_UC06_G1_T02_MalformedRSTStatement(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            screen_project_index = Screen_ProjectIndex(self)

            screen_project_index.assert_on_screen()
            screen_project_index.assert_contains_document("Document 1")

            screen_document = screen_project_index.do_click_on_first_document()

            screen_document.assert_on_screen_document()
            screen_document.assert_header_document_title("Document 1")

            screen_document.assert_text("Hello world!")

            root_node = screen_document.get_root_node()
            root_node_menu = root_node.do_open_node_menu()
            form_edit_requirement: Form_EditRequirement = (
                root_node_menu.do_node_add_requirement_first()
            )

            form_edit_requirement.do_fill_in_field_title("Requirement title")

            form_edit_requirement.do_fill_in_field_statement(BROKEN_RST_MARKUP)

            form_edit_requirement.do_form_submit_and_catch_error(
                "RST markup syntax error on line 4: "
                "Bullet list ends without a blank line; unexpected unindent."
            )

        assert test_setup.compare_sandbox_and_expected_output()
