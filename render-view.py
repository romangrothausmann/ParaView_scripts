#!pvpython

## API: http://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/index.html


import paraview.simple as pvs
import os


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
    parser.add_argument("-s", "--size", dest="size", type=int, required=False, help="desired size of screen-shot", nargs=2)
    parser.add_argument("-hq", "--highQVRender", dest="HQvr", default=False, action='store_true', required=False, help="Use high quality for volume rendering.")
    parser.add_argument("-LE", "--leftEye", dest="LE", default=False, action='store_true', required=False, help="Render left eye for a pair of stereo images.")
    parser.add_argument("-RE", "--rightEye", dest="RE", default=False, action='store_true', required=False, help="Render right eye for a pair of stereo images.")
    parser.add_argument("-oa", "--oriAxes", dest="oriAxes", default=False, action='store_true', required=False, help="Render the orientation axes.")
    parser.add_argument("-oao", "--oriAxesOnly", dest="oriAxesOnly", default=False, action='store_true', required=False, help="Render only the orientation axes.")
    parser.add_argument("-r", "--resetCam", dest="reset", default=False, action='store_true', required=False, help="Reset render camera (\"view-all\")")
    parser.add_argument("-p", "--plugin", dest="plugin", metavar='FILE', required=False, help="Plug-In to load")

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


    print pvs.GetParaViewSourceVersion() # should create a ProxyManager, still getting the warning: ProxyManager is not set. Can not perform operation: Begin()

    ## load plugin if given
    if args.plugin:
        pvs.LoadPlugin(args.plugin, False, globals())
    
    ## read pvsm
    pvs.LoadState(args.input)

    rv= pvs.GetRenderView()

    for px in pvs.GetSources().values():
        dp= pvs.GetDisplayProperties(px)
        if args.oriAxesOnly:
            pvs.Hide(px)
        if args.HQvr:
            if dp.Representation == 'Volume':
                print dp.Representation, dp.VolumeRenderingMode
                dp.VolumeRenderingMode= 'Ray Cast Only'
                print dp.Representation, dp.VolumeRenderingMode


    if args.size:
        rv.ViewSize= args.size #image size for ss


    if args.oriAxes or args.oriAxesOnly:
        rv.OrientationAxesVisibility= 1
    else:
        rv.OrientationAxesVisibility= 0

    #pvs.Render() # calls rv.ResetCamera(), instead:
    rv.MakeRenderWindowInteractor(True) # makes ori-axes visible
    
    if args.LE or args.RE: # https://cmake.org/pipermail/paraview/2011-June/022012.html
        rv.StereoRender= 1
        if args.LE:
            rv.StereoType= "Left"
        if args.RE:
            rv.StereoType= "Right"

    if args.reset:
        rv.ResetCamera()

    if pvs.servermanager.vtkSMProxyManager.GetVersionMajor() <= 5 and pvs.servermanager.vtkSMProxyManager.GetVersionMinor() < 6: # hasattr not available for rv https://public.kitware.com/pipermail/paraview/2014-May/031174.html
        rv.UseOffscreenRendering= 1 # deprecated with PV-5.6.0 # needed for stable checksums???

    rv.StillRender() # needed for StereoRender to take effect (at least for hq)!

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

