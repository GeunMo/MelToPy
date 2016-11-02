# Embedded file name: \\ALFREDSTORAGE\Alfred_asset\Maya_Shared_Environment\2016\scripts\python\MayaMenuTool\Apps\Common\MelToPy\MelToPy_run.py


def run():
    try:
        filePath = __file__
        appPath = filePath.rpartition('\\')[0]
    except:
        print 'Application`s path not exist.'
    else:
        import sys
        path = appPath
        if path not in sys.path:
            sys.path.append(path)
        import melToPyWindow
        reload(melToPyWindow)
        melToPyWindow.main()