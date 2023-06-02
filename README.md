Here is a sample README.md file for your Python script:

---
# Python Web Scraper

This Python script scrapes a website for external links and retrieves data about them, such as their DNS records and WHOIS information. It then displays this data in the terminal.

## Prerequisites

To run this script, you need the following Python libraries:

* BeautifulSoup
* termcolor
* whois
* terminaltables

If not already installed, you can add them using pip:

```
pip install beautifulsoup4 termcolor python-whois terminaltables
```

## Usage

Run the script using the following command:

```
python3 script_name.py URL [-e ELEMENT]
```

Arguments:

* `URL`: The URL of the website to scrape.
* `-e`, `--element`: Optional. Specific HTML elements to look for. If not provided, the script will look for all elements.

## Output

The script will output three sets of information:

1. External Links: All the external links found on the website.
2. Dig Information: DNS records for each external link.
3. Whois Information: WHOIS information for each external link.

## Error Log

The script writes any errors encountered during its execution to a file named `script.log`.

## Note

This script should be used responsibly and in accordance with laws and regulations.

---

Remember to replace "script_name.py" with the actual name of your Python script.
