import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report

async def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = args[1]

    max_concurrency = 5
    max_pages = 100
    
    if len(sys.argv) >= 3:
        max_concurrency = int(sys.argv[2])
    
    if len(sys.argv) >= 4:
        max_pages = int(sys.argv[3])
    
    print(f"starting crawl of: {base_url}")
    print(f"max_concurrency: {max_concurrency}, max_pages: {max_pages}")
    
    # Crawl the website
    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    # Print summary
    print(f"\nCrawl complete! Found {len(page_data)} pages.")

    # Write JSON report
    write_json_report(page_data)

if __name__ == "__main__":
    asyncio.run(main())
