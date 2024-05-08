from Registration import *
import sys
import argparse

'''if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that register your sliced brain image to AllenCCF"
    )
    parser.add_argument("--path", type=str,
                        required=True,
                        help="Path to the directory that contains your slice images")
    parser.add_argument("--file_name", required=True, type=str, help="Name of the file")
    parser.add_argument("--path2ccf", type=str, required=True,
                        help="Path to the directory that contains your CCF")
    parser.add_argument("--direction", type=str, default='medial',
                        help="Is it medial or lateral?")
    parser.add_argument("--channel", type=int, default=3,
                        help="Which channel to use?")

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_usage()
        sys.exit()
    path = args.path
    file_name = args.file_name
    path2ccf = args.path2ccf
    direction = args.direction
    channel = args.channel
    print(af_registration(file_name, path, path2ccf, direction, channel))'''

files = ['Ab3D-E1-AC-04.czi', 'Ab3D-E1-AC-10.czi', 'Ab3D-E1-AC-12.czi']
for file_name in files:
    af_registration(file_name=file_name)
