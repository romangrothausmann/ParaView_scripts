#!pvpython

## API: http://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/index.html


import paraview.simple as pvs


def main():
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message

    argv = sys.argv

    if __file__ in argv:
        argv = argv[argv.index(__file__) + 1:]  # get all args after __file__


    usage_text =  "Run ParaView in background mode with this script:"
    usage_text += "  pvpython " + __file__ + " [options]"

    parser = argparse.ArgumentParser(description=usage_text)

    parser.add_argument("-i", "--input", dest="input", metavar='FILE', nargs='+', required=True, help="Input PVSMs to combine.")
    parser.add_argument("-o", "--output", dest="output", metavar='FILE', required=True, help="Output file to save the ParaView state in (*.pvsm)")

    args = parser.parse_args(argv)

    if not argv:
        parser.print_help()
        return

    if not args.input:
       print('Need an input file')
       parser.print_help()
       sys.exit(1)

    if not args.output:
       print('Need an output file')
       parser.print_help()
       sys.exit(1)

    ## read pvsm
    for f in args.input:
        pvs.LoadState(f)


    if args.output:
        try:
            f = open(args.output, 'w')
            f.close()
            ok = True
        except:
            print("Cannot save to path %r" % save_path)

            import traceback
            traceback.print_exc()

        if ok:
            pvs.servermanager.SaveState(args.output)





if __name__ == "__main__":
    main()

