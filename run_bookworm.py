import argparse
import json
from bookworm import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--path',
                        help='Path to the novel\'s .txt file',
                        required=True)

    parser.add_argument('--output_file',
                        help='The path+filename where the output will be stored')

    parser.add_argument('--d3',
                        help=('Output a dictionary which is interpretable by '
                              'the d3.js force directed graph script'),
                        action='store_true')

    parser.add_argument('--threshold',
                        help=('Threshold value for interaction inlclusion in '
                              'output interatcion_df'),
                        default=2)

    args = parser.parse_args()

    interaction_df = bookworm(args.path, threshold=int(args.threshold))

    if (args.d3 is True) and (args.output_file is None):
        with open('bookworm/d3/bookworm.json', 'w') as fp:
            json.dump(d3_dict(interaction_df), fp)
    elif (args.d3 is True) and (args.output_file is not None):
        with open(args.output_file, 'w') as fp:
            json.dump(d3_dict(interaction_df), fp)
    elif (args.d3 is False) and (args.output_file is not None):
        interaction_df.to_csv(args.output_file)
    elif (args.d3 is False) and (args.output_file is None):
        print(interaction_df)
