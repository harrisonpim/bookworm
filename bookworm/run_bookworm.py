import argparse
from bookworm import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--path',
                        help='Path to the novel\'s .txt file',
                        required=True)

    parser.add_argument('--d3',
                        help='Output a dictionary which is interpretable by ',
                        action='store_true')

    args = parser.parse_args()
    interaction_df = bookworm(args.path)

    if args.d3 is True:
        print(d3_dict(interaction_df))
    else:
        print(interaction_df)
