# Web Crawler

A concurrent web crawler that extracts structured data from websites, including headings, paragraphs, links, and images. Built with Python using asyncio for high-performance crawling.

## Features

- **Concurrent crawling** with configurable concurrency limits
- **Max pages limit** to control crawl scope
- **Same-domain restriction** to avoid crawling the entire internet
- **URL normalization** to detect duplicate pages
- **Rich data extraction**:
  - Page headings (h1/h2)
  - First paragraph content
  - Outgoing links
  - Image URLs
- **JSON report generation** for easy data analysis
- **Command-line interface** for easy configuration

## Installation

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Clone the Repository

```bash
git clone https://github.com/GSheng05/Web-Scrapper.git
cd Web-Scrapper

