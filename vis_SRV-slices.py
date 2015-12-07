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
    #pvs.servermanager.LoadState(args.input)

    ## read a vtp
    #reader = pvs.XMLPolyDataReader(FileName=args.input)

    ## read a MetaImage (there is a MetaImageWriter but no MetaImageReader)
    reader = pvs.OpenDataFile(args.input)

    #reader.UpdatePipelineInformation()
    reader.UpdatePipeline()

    bds= reader.GetDataInformation().GetBounds() # needs UpdatePipeline
    print bds
    
    pvs.Delete(reader)
    del reader

    (minX, maxX, minY, maxY, minZ, maxZ) = [x for x in bds] 
    center = map(lambda x,y : (x+y)/2, bds[0:6:2], bds[1:6:2]) #center

    # ##center xy-slice
    # p0= [0, 0, center[2]]
    # p1= [0, maxY, center[2]]
    # p2= [maxX, 0, center[2]]

    ##center xz-slice
    p0= [0, center[1], 0]
    p1= [0, center[1], maxZ]
    p2= [maxX, center[1], 0]

    plane1 = pvs.Plane(guiName="xz-plane")
    plane1.Origin= p0
    plane1.Point1= p1
    plane1.Point2= p2

    ##center yz-slice
    p0= [center[0], 0, 0]
    p1= [center[0], 0, maxZ]
    p2= [center[0], maxY, 0]

    plane2 = pvs.Plane(guiName="yz-plane")
    plane2.Origin= p0
    plane2.Point1= p1
    plane2.Point2= p2

    plane= []
    scale= 0.331662
    z_list = [129, 640, 1131, 1533, 1601, 1773, 2156, 2190, 2389, 2497, 2578, 2692, 2945, 3041, 3250, 4046]
    for i, z in enumerate(z_list):
        ##center xy-slice
        p0= [0, 0,    z*scale]
        p1= [0, maxY, z*scale]
        p2= [maxX, 0, z*scale]

        plane.append(pvs.Plane(guiName="xy-plane_%04d"%z))
        plane[i].Origin= p0
        plane[i].Point1= p1
        plane[i].Point2= p2



    # plane1Display = pvs.Show(plane1)
    # #plane1Display.Texture = reader
    # dp = pvs.GetDisplayProperties(plane1)
    # dp.Representation = 'Surface With Edges'
    # #dp.Texture = reader

    ## make all sources visible
    for px in pvs.GetSources().values():
        pvs.Show(px)
        dp= pvs.GetDisplayProperties(px)
        dp.Representation = 'Surface'
        dp.Opacity= 1.0


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

