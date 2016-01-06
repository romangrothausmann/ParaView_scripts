#!pvpython

## API: http://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/index.html


import paraview.simple as pvs

def run(fn="extent.mha", GUI= False):

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
            

    ## even works with pvpython and no CreateRenderView, from http://www.paraview.org/Wiki/Take_a_Screenshot_of_a_VTP_File
    # RenderView1 = pvs.GetActiveView()
    # if not RenderView1:
    #     # When using the ParaView UI, the View will be present, not otherwise.
    #     RenderView1 = pvs.CreateRenderView()
    RenderView1 = pvs.GetRenderView()
    RenderView1.ResetCamera()
    pvs.Render() #resets cam, without no OrientationAxes in ss

    RenderView1.LightSwitch= 1 # "Head Light"
    RenderView1.UseLight= 1 #"Light Kit"
    RenderView1.KeyLightIntensity= 1.0
    RenderView1.FillLightKFRatio= 1.0
    RenderView1.BackLightKBRatio= 1.0
    RenderView1.HeadLightKHRatio= 6.5
    #RenderView1.HeadLightWarmth= 0.5

    ## position camera
    ## read a pvcc: http://www.paraview.org/pipermail/paraview/2014-February/030490.html
    RenderView1.CameraPosition= [667, 1591, 718]
    RenderView1.CameraFocalPoint= [-295, -1053, 718]
    RenderView1.CameraViewUp= [0.939692620785909, -0.342020143325669, 2.22044604925031e-16]
    RenderView1.CameraViewAngle= 30
    RenderView1.CenterOfRotation= [82, 82, 718]
    RenderView1.RotationFactor= 1
    RenderView1.CameraParallelScale= 728
    RenderView1.CameraParallelProjection= 0

    ##set the background color
    RenderView1.Background = [1,1,1]  #white

    RenderView1.OrientationAxesVisibility= 1
    # RenderView1.CenterAxesVisibility= 1

    if GUI:
        pvs.Show()
        pvs.Render() #resets cam outside GUI, only needed for GUI
    else:
        RenderView1.ViewSize = [1920, 900] #image size for ss


def main():
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message

    argv = sys.argv

    if __file__ in argv:
        argv = argv[argv.index(__file__) + 1:]  # get all args after __file__


    usage_text =  "Run ParaView in background mode with this script:"
    usage_text += "  pvpython " + __file__ + " [options]"

    parser = argparse.ArgumentParser(description=usage_text)

    parser.add_argument("-i", "--input", dest="input", metavar='FILE', required=False, default="extent.mha",  help="Input path contained in a text file.")
    parser.add_argument("-o", "--output", dest="output", metavar='FILE', required=False, help="Output file to save the ParaView state in (*.pvsm)")
    parser.add_argument("-s", "--screen-shot", dest="ss", metavar='FILE', required=False, help="Output file to save a screen-shot in (*.png)")

    args = parser.parse_args(argv)

    if not argv:
        parser.print_help()
        return

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


    if args.ss:
        #save screenshot
        pvs.WriteImage(args.ss)



if __name__ == "__main__":
    main()
else:
    run(GUI= True) # run with default parameters, e.g. as a macro run from GUI

