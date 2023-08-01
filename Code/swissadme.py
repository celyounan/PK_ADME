#!/usr/bin/env python3
"""Downloads SwissADME information for a list of chemicals."""

# Written by Celin Younan (celinyounan@u.boisestate.edu)
# and Robert Greenhalgh (robert.greenhalgh@utah.edu)

# Last updated: 2023.06.21

import argparse
import os
import sys
import pubchempy as pcp

from urllib.request import urlopen
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def arg_file(in_file):
    """Checks that a file is present, unless read from a pipe."""
    if in_file[:5] != '/dev/' and not os.path.isfile(in_file):
        sys.stderr.write('Error: User-specified input file ({}) does not '
                         'exist.\n'.format(in_file))
        sys.exit()
    return in_file

def parse_args():
    """Parse user-supplied arguments."""
    parser = argparse.ArgumentParser(
        description='Downloads SwissADME information for a list of chemicals.'
    )
    parser.add_argument(
        '-i', '--input', type=arg_file, nargs='?', required=True,
        help='Input file. (Required)'
    )
    parser.add_argument(
        '-o', '--output', nargs='?', default=None,
        help='Output TSV. (Optional, defaults to standard out)'
    )
    parser.add_argument(
        '-l', '--log', action = 'store_true',
        help='Log Selenium information for debugging. (Optional)'
    )
    args = parser.parse_args()
    return args

def read_chem_file(args):
    """Reads in a list of chemical compounds."""
    chems = []
    with open(args.input, 'r') as in_handle:
        for line in in_handle:
            if line[0] != '#':
                chem = line.rstrip()
                if chem:
                    chems.append(chem)
    return(chems)

def get_chem_smile(chems):
    """Uses PubChempy to obtain the SMILE for each chemical."""
    smile_dict = {}
    sys.stderr.write('Retrieving SMILEs from PubChempy.\n')
    for chem in chems:
        chem_ids = pcp.get_cids(chem)
        if chem_ids:
            prop_dict = pcp.get_properties('CanonicalSMILES', chem_ids[0])[0]
            smile_dict[chem] = prop_dict['CanonicalSMILES']
    sys.stderr.write('SMILEs retrieved.\n')
    return smile_dict

def get_swissadme_info(args, smile_dict):
    """Uses SwissADME to obtain chemical information."""
    swissadme_dict = {}
    keys = []
    name = 'smiles'
    button = 'submitButton'
    path = '//*[@id="sib_body"]/div[7]/a[1]'
    website = 'http://www.swissadme.ch'
    sys.stderr.write('Retrieving information from SwissADME.\n')
    for chem in smile_dict:
        options = Options()
        options.add_argument('--headless')
        if args.log:
            service = Service()
        else:
            service = Service(log_path=os.devnull)
        driver = Firefox(options=options, service=service)
        wait = WebDriverWait(driver, 40)
        driver.get(website)
        wait.until(EC.presence_of_element_located((By.NAME, name)))
        driver.find_element(By.NAME, name).send_keys(smile_dict[chem]) 
        wait.until(EC.presence_of_element_located((By.ID, button)))
        driver.find_element(By.ID, button).submit()
        wait.until(EC.visibility_of_element_located((By.ID, 'mol-cell-1')))
        chem_csv = driver.find_element(By.XPATH, path).get_property('href')
        for line in urlopen(chem_csv):
            line = line.decode('utf-8').rstrip().split(',')
            if chem not in swissadme_dict:
                keys = line
                swissadme_dict[chem] = {}
            else:
                for key, val in zip(keys, line):
                    swissadme_dict[chem][key] = val
        driver.close()
    keys = [k for k in keys if k != 'Molecule']
    sys.stderr.write('SwissADME information retrieved.\n')
    return(swissadme_dict, keys)

def write_output(args, chems, swissadme_dict, keys):
    """Writes SwissADME data to a TSV."""
    if args.output:
        out_handle = open(args.output, 'w')
    else:
        out_handle = sys.stdout
    out_header = ['# Chemical']
    for key in keys:
        out_header.append(key)
    out_handle.write('{}\n'.format('\t'.join(out_header)))
    for chem in chems:
        out_line = [chem]
        if chem in swissadme_dict:
            for key in keys:
                out_line.append(swissadme_dict[chem][key])
        else:
            out_line.extend(len(keys) * ['NA'])
        out_handle.write('{}\n'.format('\t'.join(out_line)))
    if args.output:
        out_handle.close()

def main():
    """Run the script when called from the command line."""
    args = parse_args()
    chems = read_chem_file(args)
    smile_dict = get_chem_smile(chems)
    swissadme_dict, keys = get_swissadme_info(args, smile_dict)
    write_output(args, chems, swissadme_dict, keys)

if __name__ == "__main__":
    main()
