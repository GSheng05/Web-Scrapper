import sys
from crawl import get_html,crawl_page

def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = args[1]

    print(f"starting crawl of: {base_url}...")
    page_data = crawl_page(base_url)

    # Print summary
    print(f"\nCrawl complete! Found {len(page_data)} pages.")
    print("\nPage data:")
    for url, data in page_data.items():
        print(f"\nURL: {url}")
        print(f"  Heading: {data['heading']}")
        print(f"  First paragraph: {data['first_paragraph'][:100]}...")
        print(f"  Outgoing links: {len(data['outgoing_links'])}")
        print(f"  Images: {len(data['image_urls'])}")



if __name__ == "__main__":
    main()
