#!pvpython

## API: http://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/index.html


import paraview.simple as pvs

def run(fn="extent.mha", GUI= False):


    layerList= ['G', 'A', 'B']
    for j, s in enumerate(layerList):

        reader1 = pvs.OpenDataFile("yz-plane.vtp", guiName="plane-"+s+"_x@0250")
        reader2 = pvs.OpenDataFile("xz-plane.vtp", guiName="plane-"+s+"_y@0250")

        plane= []
        scale= 0.331662
        zList = [129, 640, 1131, 1533, 1601, 1773, 2156, 2190, 2389, 2497, 2578, 2692, 2945, 3041, 3250, 4046]
        #zList = [129, 640, 1131, 2692, 3250, 4046]
        for i, z in enumerate(zList):
            plane.append(pvs.OpenDataFile("xy-plane_%04d.vtp"%(z), guiName="plane-%s_z@%04d"%(s,z)))


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
        #pvs.ColorBy(rep=dp, value=None) #solid color, does not work
        dp.ColorArrayName = [None, ''] #solid color, works
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

    RenderView1.LightSwitch= 1 # "Head Light"
    RenderView1.UseLight= 1 #"Light Kit"
    RenderView1.KeyLightIntensity= 1.0
    RenderView1.FillLightKFRatio= 1.0
    RenderView1.BackLightKBRatio= 1.0
    RenderView1.HeadLightKHRatio= 6.5
    #RenderView1.HeadLightWarmth= 0.5

    ## position camera
    ## read a pvcc: http://www.paraview.org/pipermail/paraview/2014-February/030490.html
    RenderView1.CameraPosition= [-844, 741, 249]
    RenderView1.CameraFocalPoint= [766, 515, 206]
    RenderView1.CameraViewUp= [-0.0453896982204987, -0.135307884021876, -0.989763381731702]
    RenderView1.CameraViewAngle= 20
    RenderView1.CenterOfRotation= [424, 586, 197]
    RenderView1.RotationFactor= 1
    RenderView1.CameraParallelScale= 421
    RenderView1.CameraParallelProjection= 0

    ##set the background color
    RenderView1.Background = [1,1,1]  #white

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

    parser.add_argument("-o", "--output", dest="output", metavar='FILE', required=False, help="Output file to save the ParaView state in (*.pvsm)")
    parser.add_argument("-s", "--screen-shot", dest="ss", metavar='FILE', required=False, help="Output file to save a screen-shot in (*.png)")

    args = parser.parse_args(argv)

    if not argv:
        parser.print_help()
        return

    run()

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

