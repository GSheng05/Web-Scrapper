from urllib.parse import urlsplit
import requests

def get_heading_from_html(html: str) -> str:
    from bs4 import BeautifulSoup, Tag
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try h1 first
    h_tag = soup.find('h1')
    
    # If no h1, try h2
    if h_tag is None:
        h_tag = soup.find('h2')
    
    # Return text if found, otherwise empty string
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    from bs4 import BeautifulSoup, Tag
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try to find main tag first
    main_tag = soup.find('main')
    
    if main_tag:
        # Look for first p within main
        p_tag = main_tag.find('p')
    else:
        # Fallback to first p anywhere
        p_tag = soup.find('p')
    
    # Return text if found, otherwise empty string
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""

def normalize_url(url):
    # Parse the URL
    parsed = urlsplit(url)
    
    # Get the domain (netloc) and path
    domain = parsed.netloc
    path = parsed.path
    
    # Remove port number if present
    if ":" in domain:
        domain = domain.split(":")[0]
    
    # Remove trailing slash from path
    if path.endswith("/"):
        path = path[:-1]
    
    # Combine domain and path
    normalized = domain + path
    
    return normalized

def get_urls_from_html(html, base_url):
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    
    # Find all anchor tags
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href:
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    
    return urls


def get_images_from_html(html, base_url):
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    
    # Find all image tags
    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, src)
            images.append(absolute_url)
    
    return images

def extract_page_data(html: str, page_url: str):
    # Get all the data using our existing functions
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    outgoing_links = get_urls_from_html(html, page_url)
    image_urls = get_images_from_html(html, page_url)
    
    # Return as a dictionary
    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links,
        "image_urls": image_urls,
    }

def get_html(url):
    
    # Set User-Agent header to avoid being blocked
    headers = {"User-Agent": "BootCrawler/1.0"}
    
    # Fetch the webpage
    response = requests.get(url, headers=headers)
    
    # Raise error for HTTP error status codes (400+)
    if response.status_code >= 400:
        raise Exception(f"HTTP error: {response.status_code}")
    
    # Check content-type is text/html
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise Exception(f"Expected HTML content, got: {content_type}")
    
    # Return the HTML content
    return response.text

def crawl_page(base_url, current_url=None, page_data=None):
    from urllib.parse import urlparse
    
    # Initialize on first call
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}
    
    # Check if current_url is on the same domain as base_url
    base_domain = urlparse(base_url).netloc
    current_domain = urlparse(current_url).netloc
    
    if base_domain != current_domain:
        return page_data
    
    # Normalize the current URL
    normalized_url = normalize_url(current_url)
    
    # Check if we've already crawled this page
    if normalized_url in page_data:
        return page_data
    
    # Get the HTML from the current URL
    print(f"Crawling: {current_url}")
    try:
        html = get_html(current_url)
    except Exception as e:
        print(f"Error crawling {current_url}: {e}")
        return page_data
    
    # Extract page data
    data = extract_page_data(html, current_url)
    
    # Add to page_data dictionary
    page_data[normalized_url] = data
    
    # Recursively crawl each outgoing link
    for link in data["outgoing_links"]:
        crawl_page(base_url, link, page_data)
    
    return page_data
