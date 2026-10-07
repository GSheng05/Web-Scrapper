
import unittest
from crawl import normalize_url
from crawl import get_heading_from_html,get_first_paragraph_from_html
from crawl import get_urls_from_html, get_images_from_html, extract_page_data

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_query_params(self):
        input_url = "https://www.boot.dev/blog/path?utm_source=twitter"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_fragment(self):
        input_url = "https://www.boot.dev/blog/path#section"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_root_domain(self):
        input_url = "https://www.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_port(self):
        input_url = "https://www.boot.dev:8080/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)



class TestHTMLParsing(unittest.TestCase):
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>No heading here</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1_priority(self):
        input_body = "<html><body><h1>Primary</h1><h2>Secondary</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Primary"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_basic(self):
        input_body = "<html><body><p>First paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>No paragraphs</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_multiple_in_main(self):
        input_body = """<html><body>
            <main>
                <p>First in main.</p>
                <p>Second in main.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First in main."
        self.assertEqual(actual, expected)

class TestURLExtraction(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about">About</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/page1">Page 1</a><a href="/page2">Page 2</a><a href="https://external.com">External</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/page1", "https://crawler-test.com/page2", "https://external.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><p>No links here</p></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_missing_href(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a>No href</a><a href="/valid">Valid</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/valid"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://cdn.example.com/image.jpg" alt="Image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://cdn.example.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/img1.png"><img src="/img2.png"><img src="https://external.com/img3.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/img1.png", "https://crawler-test.com/img2.png", "https://external.com/img3.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><p>No images here</p></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="No src"><img src="/valid.png" alt="Valid"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/valid.png"]
        self.assertEqual(actual, expected)
class TestPageDataExtraction(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_content(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><p>Just a paragraph, no heading or links</p></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "Just a paragraph, no heading or links",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple_elements(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Secondary Heading</h2>
            <main>
                <p>Main paragraph content.</p>
                <p>Second paragraph.</p>
            </main>
            <a href="/page1">Page 1</a>
            <a href="https://external.com/page2">Page 2</a>
            <img src="/img1.png" alt="First">
            <img src="https://cdn.com/img2.png" alt="Second">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Secondary Heading",
            "first_paragraph": "Main paragraph content.",
            "outgoing_links": ["https://crawler-test.com/page1", "https://external.com/page2"],
            "image_urls": ["https://crawler-test.com/img1.png", "https://cdn.com/img2.png"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_html(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_relative_urls(self):
        input_url = "https://crawler-test.com/blog"
        input_body = """<html><body>
            <h1>Blog Post</h1>
            <p>Blog content here.</p>
            <a href="../home">Home</a>
            <img src="../images/header.jpg" alt="Header">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com/blog",
            "heading": "Blog Post",
            "first_paragraph": "Blog content here.",
            "outgoing_links": ["https://crawler-test.com/home"],
            "image_urls": ["https://crawler-test.com/images/header.jpg"],
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
	unittest.main()
