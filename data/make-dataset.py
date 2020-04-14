from more_itertools import collapse

import pkg_resources
import json, os, re
import argparse


# OpenNMT has a fancy pipe
DELIM = "￨"

# for each entry we add 3 values. each entry has utmost 30 values and then 3 values at end
ENT_SIZE = 94

"""
Final form for each entry:
<ent>|<ent> <str>|household_income <str>|geography <str>|year
End: <str>|1_year_growth <str>|city_state <str>|city_name
"""
def process_table(entry):
    nEntries = len(entry['chart_items']['household_income'])
    records = [DELIM.join(['<ent>', '<ent>'])]
    for i in range(nEntries):
        records.append(DELIM.join([
            entry['chart_items']['household_income'][str(i)], 'HOUSEHOLD_INCOME'
        ]))
        records.append(DELIM.join([
            entry['chart_items']['geography'][str(i)].replace(' ', '_').replace(',',''), 'GEOGRAPHY'
        ]))
        records.append(DELIM.join([
            entry['chart_items']['year'][str(i)], 'YEAR'
        ]))

    # TODO: append growth percentage
    records.append(DELIM.join([
        entry['1_year_growth'], '1_year_growth'
    ]))
    records.append(DELIM.join([
        entry['city_state'].replace(' ', '_'), 'city_state'
    ]))
    records.append(DELIM.join([
        entry['city_name'].replace(' ', '_').replace(',',''), 'city_name'
    ]))
    # TODO: The following did not work. Check why. no <blank> token were seen in input
    # pad the entity to size ENT_SIZE with OpenNMT <blank> token
    records.extend([DELIM.join(['<blank>', '<blank>'])] * (ENT_SIZE - len(records)))

    return list(collapse(records))


def _clean_summary(summary, tokens):
    """
    In here, we slightly help the copy mechanism.
    For the source sequence, we took all multi-word values
    and repalaced spaces by underscores. We do the same for 
    summaries, so that the copy mechanism knows it was a copy.
    
    """
    summary = ' '.join(summary)
    for token in tokens:
        val = token.split(DELIM)[0]
        if '_' in val:
            val_no_underscore = val.replace('_', ' ')
            summary = summary.replace(val_no_underscore, val)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', dest='folder', required=True,
                        help='Save the preprocessed dataset to this folder')
    parser.add_argument('--keep-na', dest='keep_na', action='store_true',
                        help='Activate to keep NA in the dataset')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.folder): 
        print('Creating folder to store preprocessed dataset at:')
        print(args.folder)
        os.mkdir(args.folder)
        
    for setname in ['train', 'valid', 'test']:
        filename = f'household_income/{setname}.json'
        filename = pkg_resources.resource_filename(__name__, filename)
        with open(filename, encoding='utf8', mode='r') as f:
            data = json.load(f)
        
        input_filename = os.path.join(args.folder, f'{setname}_input.txt')
        output_filename = os.path.join(args.folder, f'{setname}_output.txt')
        with open(input_filename, mode='w', encoding='utf8') as inputf:
            with open(output_filename, mode='w', encoding='utf8') as outputf:
                for entry in data:
                    input = process_table(entry)
                    inputf.write(' '.join(input) + '\n')
                    outputf.write(_clean_summary(entry['summary'], input) + '\n')
