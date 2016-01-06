#!pvpython

## API: http://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/index.html


import paraview.simple as pvs

def run(fn="extent.mha"):

    ## read a MetaImage (there is a MetaImageWriter but no MetaImageReader)
    reader = pvs.OpenDataFile(fn)
    reader.UpdatePipeline()

    bds= reader.GetDataInformation().GetBounds() # needs UpdatePipeline
    print bds
    
    pvs.Delete(reader)
    del reader

    (minX, maxX, minY, maxY, minZ, maxZ) = [x for x in bds] 
    center = map(lambda x,y : (x+y)/2, bds[0:6:2], bds[1:6:2]) #center

    layerList= ['G', 'A', 'B']
    for j, s in enumerate(layerList):

        ##center yz-slice, x-normal
        p0= [0, center[1], 0]
        p1= [0, center[1], maxZ]
        p2= [maxX, center[1], 0]

        plane1 = pvs.Plane(guiName="plane-"+s+"_x@0250")
        plane1.Origin= p0
        plane1.Point1= p1
        plane1.Point2= p2

        ##center xz-slice, y-normal
        p0= [center[0], 0, 0]
        p1= [center[0], 0, maxZ]
        p2= [center[0], maxY, 0]

        plane2 = pvs.Plane(guiName="plane-"+s+"_y@0250")
        plane2.Origin= p0
        plane2.Point1= p1
        plane2.Point2= p2

        plane= []
        scale= 0.331662
        zList = [129, 640, 1131, 1533, 1601, 1773, 2156, 2190, 2389, 2497, 2578, 2692, 2945, 3041, 3250, 4046]
        for i, z in enumerate(zList):
            ##center xy-slice
            p0= [0, 0,    z*scale]
            p1= [0, maxY, z*scale]
            p2= [maxX, 0, z*scale]

            plane.append(pvs.Plane(guiName="plane-%s_z@%04d"%(s,z)))
            plane[i].Origin= p0
            plane[i].Point1= p1
            plane[i].Point2= p2


    ## make all sources visible
    for px in pvs.GetSources().values():
        pvs.Show(px)

        guiName= pvs.servermanager.ProxyManager().GetProxyName("sources", px)
        fnPNG= guiName + ".png"
        print fnPNG

        ## http://www.paraview.org/pipermail/paraview/2012-March/024261.html
        ## http://www.paraview.org/pipermail/paraview/2009-March/011544.html
        texProxy = pvs.servermanager.CreateProxy("textures", "ImageTexture")
        texProxy.GetProperty("FileName").SetElement(0, fnPNG)
        texProxy.UpdateVTKObjects()

        dp= pvs.GetDisplayProperties(px)
        dp.Representation = 'Surface'
        dp.Texture= texProxy 
        if 'G' in guiName:
            dp.Opacity= 1.0
        else:
            dp.Opacity= 0.95 # color gradient not visible below .95
            

    # pvs.Render()
    # wait = input("PRESS ENTER TO CONTINUE.")

    RenderView1 = pvs.GetRenderView()
    RenderView1.ResetCamera()

    RenderView1.LightSwitch= 1 # "Head Light"
    RenderView1.UseLight= 1 #"Light Kit"
    RenderView1.KeyLightIntensity= 1.0
    RenderView1.FillLightKFRatio= 1.0
    RenderView1.BackLightKBRatio= 1.0
    RenderView1.HeadLightKHRatio= 6.5
    #RenderView1.HeadLightWarmth= 0.5

    # r = pvs.GetDisplayProperties()
    # r.Ambient = 1.0


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

    run(args.input)

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
else:
    run() # run with default parameters, e.g. as a macro run from GUI

