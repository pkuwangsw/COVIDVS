import csv
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--infile", type=str,
                    help='Path to CSV file that will be sorted')
parser.add_argument("--outfile", type=str,
                    help="Path to CSV file that the sorted results will be saved")
parser.add_argument("--reverse", action='store_true', default=False,
                    help="Use for descending sort. Default is ascending sort")
parser.add_argument("--column", type=int, default=2,
                    help="The number of column that will be sorted")
parser.add_argument("--headline", action="store_true", default=False,
                    help="Use for .csv files that contain a headline")


def sort_csv(args):
    data = csv.reader(open(args.infile), delimiter=',')
    data_list = [row for row in data]
    if args.headline is True:
        headrow = data_list[0]
        sortedlist = sorted(data_list[1:], key=lambda x: x[args.column-1], reverse=args.reverse)
    else:
        headrow = None
        sortedlist = sorted(data_list, key=lambda x: x[args.column-1], reverse=args.reverse)
    with open(args.outfile, "w") as f:
        fileWriter = csv.writer(f, delimiter=',')
        if headrow is not None:
            fileWriter.writerow(headrow)
        for row in sortedlist:
            fileWriter.writerow(row)


if __name__=='__main__':
    args = parser.parse_args()
    sort_csv(args)