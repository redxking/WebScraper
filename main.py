#!/usr/bin/python
__author__ = 'Angelis Pseftis'

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
import argparse
from termcolor import colored
import subprocess
import whois
from terminaltables import AsciiTable
import logging

# Initialize logging
logging.basicConfig(filename='script.log', level=logging.DEBUG)

def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    parser.add_argument('--element', '-e', type=str, action='append')
    return parser.parse_args()

def link_filter(link, parsed_url):
    link = link[1]
    parsed_link = urlparse(link)
    return parsed_link.netloc and parsed_link.scheme in ['http', 'https'] and parsed_link != parsed_url.netloc

def main():
    args = create_arg_parser()
    parsed_url = urlparse(args.url)
    try:
        r = urlopen(args.url).read()
    except Exception as e:
        logging.error(f"Unable to open URL: {e}")
        return

    soup = BeautifulSoup(r, "html.parser")
    links = set()
    links.update([(elem.name, elem.attrs.get('href')) for elem in soup.find_all(args.element or True, href=True)])
    links.update([(elem.name, elem.attrs.get('src')) for elem in soup.find_all(args.element or True, src=True)])
    links = sorted(filter(lambda link: link_filter(link, parsed_url), links), key=lambda e: [e[0], e[1]])

    links.insert(0, ['Type', 'Link'])

    table = AsciiTable(links, 'External Links')
    print(table.table)

    print('\n \n ')
    print(colored('-----------Above this line are all external links.----------', 'green'))
    print('\n')

    # Prepare the host data
    table = AsciiTable(links, 'Dig')
    table.inner_heading_row_border = False
    dig_data = []
    hosts = set([urlparse(link[1]).netloc for link in links if link])
    for host in hosts:
        try:
            dig_data.append(subprocess.check_output(['dig',"+multiline","+noall","+answer","ANY", host], text=True).split())
        except Exception as e:
            logging.error(f"Unable to get dig data for host {host}: {e}")
    print(table.table)
    print('\n \n ')
    print(colored('-----------Above is the information returned from Dig.----------', 'green'))
    print('\n')

    hosts = list(hosts)

    # Prepare the Whois data
    whois_data = [['Host', 'Expiration Date', 'Status']]
    while hosts:
        host, hosts = hosts[0], hosts[1:]
        try:
            result = whois.whois(host)
            d = colored(result.domain_name or host, 'red')
            if not isinstance(d, str):
                d = '\n'.join(map(lambda x: colored(x, 'red'), d))
            e = result.expiration_date
            if not e:
                e = []
            if not isinstance(e, list):
                e = [e]
            e = '\n'.join([colored(i, 'green') if isinstance(i, str) else colored(i.strftime('%d-%m-%y'), 'green') for i in e])
            s = result.status
            if not s:
                s = []
            if not isinstance(s, list):
                s = [s]
            s = '\n'.join([colored(x.split()[0] or 'unknown', 'blue') for x in s])
            if not isinstance(s, str):
                s = '\n'.join(map(lambda x: colored(x.split()[0], 'blue'), s))

            whois_data.append([d, e, s])
        except whois.parser.PywhoisError as e:
            logging.error(f"Unable to get whois data for host {host}: {e}")
            i = host.find('.')
            if i == -1:
                break
            host = host[i+1:]
            if host not in hosts:
                hosts.append(host)
    table = AsciiTable(whois_data, 'Whois')
    print(table.table)

if __name__ == "__main__":
    main()
