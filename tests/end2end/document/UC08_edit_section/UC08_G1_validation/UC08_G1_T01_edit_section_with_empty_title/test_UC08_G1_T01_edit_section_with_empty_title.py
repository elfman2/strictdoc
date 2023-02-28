from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.server import SDocTestServer


class Test_UC08_G1_T01_EditSectionWithEmptyTitle(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            self.assert_text("Document 1")
            self.assert_text("PROJECT INDEX")

            self.click_xpath('//*[@data-testid="tree-file-link"]')

            self.assert_text("Hello world!")

            self.hover_and_click(
                hover_selector="(//sdoc-node)[2]",
                click_selector=(
                    '(//sdoc-node)[2]//*[@data-testid="node-edit-action"]'
                ),
                hover_by=By.XPATH,
                click_by=By.XPATH,
            )

            # HACK: The only way the field is actually cleared.
            self.type("#section_title", "X")
            section_title_field = self.find_element("//*[@id='section_title']")
            section_title_field.click()
            section_title_field.send_keys(Keys.BACKSPACE)

            self.type("#section_content", "Modified statement.")

            self.click_xpath('//*[@data-testid="form-submit-action"]')

            self.assert_text("Section title must not be empty.")

        assert test_setup.compare_sandbox_and_expected_output()
