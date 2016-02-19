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

    parser.add_argument("-i", "--input", dest="input", metavar='FILE', required=True, help="Input path contained in a text file.")
    parser.add_argument("-png", "--png", dest="png", metavar='FILE', required=False, help="Output name to save a PNG screen-shot in")
    parser.add_argument("-svg", "--svg", dest="svg", metavar='FILE', required=False, help="Output name to save a SVG screen-shot in")

    args = parser.parse_args(argv)

    if not argv:
        parser.print_help()
        return

    if not args.input:
       print('Need an input file')
       parser.print_help()
       sys.exit(1)

    if not args.png and not args.svg:
       print('Need an output file')
       parser.print_help()
       sys.exit(1)

    ## read pvsm
    pvs.servermanager.LoadState(args.input)

    ## make all sources visible
    for px in pvs.GetSources().values():
        pvs.Show(px) # apparently essential

    rv= pvs.GetRenderView()#
    rv.ResetCamera()
    rv.ViewSize = [1920, 900] #image size for ss
    
    pvs.Render() #resets cam, without no OrientationAxes in ss
    
    rv.OrientationAxesVisibility= 0
    # rv.CenterAxesVisibility= 1
    
    if args.png:
        pvs.WriteImage(args.png)

        
    if args.svg:
        pvs.ExportView(args.svg, view= rv, Drawbackground= 0, Rasterize3Dgeometry= 1)

        ## save OrientationAxes only for separate positioning in SVG
        for px in pvs.GetSources().values():
            pvs.Hide(px)

        rv.OrientationAxesVisibility= 1
        pvs.WriteImage(args.svg+".ori-axes.png")


if __name__ == "__main__":
    main()

