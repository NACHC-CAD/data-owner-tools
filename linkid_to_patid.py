import csv
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Tool for translating LINK_IDs back into PATIDs')
parser.add_argument('--source', nargs=1, required=True, help='Source PII CSV file')
parser.add_argument('--links', nargs=1, required=True, help='LINK_ID CSV file from linkage agent')
parser.add_argument('--hh_source', nargs=1, required=False, help='Household *_hid_mapping.csv generated by testing-and-tuning/answer_key_map.py')
parser.add_argument('--hh_links', nargs=1, required=False, help='Household LINK_ID CSV file from linkage agent')
args = parser.parse_args()

source_file = Path(args.source[0])

headers = ['LINK_ID', 'PATID']
hh_headers = ['LINK_ID', 'HH_ID']
pii_lines = []

with open(source_file) as source:
  source_reader = csv.reader(source)
  pii_lines = list(source_reader)

links_file = Path(args.links[0])

with open('output/linkid_to_patid.csv', 'w', newline='', encoding='utf-8') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(headers)
  with open(links_file) as links:
    links_reader = csv.reader(links)
    next(links_reader)
    for row in links_reader:
      link_id = row[0]
      patid = pii_lines[int(row[1])+1][0]
      writer.writerow([link_id, patid])

if args.hh_links[0] and args.hh_source[0]:
  hh_source_file = Path(args.hh_source[0])
  hh_links_file = Path(args.hh_links[0])
  with open(hh_source_file) as source:
    source_reader = csv.reader(source)
    hid_map = list(source_reader)

  with open('output/linkid_to_hid.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(hh_headers)
    with open(hh_links_file) as links:
      links_reader = csv.reader(links)
      next(links_reader)
      for row in links_reader:
        link_id = row[0]
        hid = hid_map[int(row[1])+1][1]
        writer.writerow([link_id, hid])
