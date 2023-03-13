#!/usr/bin/env python3

# husk --renderer Karma -f 25 -n 5 -o "H:\husk_plugin_dev\houdini\render\test_render\test_render_$F4.exr" "H:\husk_plugin_dev\houdini\usd\usd_export_v001.usd_rop1.usd"

from __future__ import absolute_import
from System.IO import Path
from System.Text.RegularExpressions import Regex

from Deadline.Plugins import DeadlinePlugin, PluginType
from Deadline.Scripting import FrameUtils, RepositoryUtils, FileUtils, SystemUtils, StringUtils

import os, sys


def GetDeadlinePlugin():
    return HuskPlugin()

def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()
    
class HuskPlugin(DeadlinePlugin):
    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
    
    def Cleanup(self):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback
        
        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
    
    def InitializeProcess(self):
        self.SingleFramesOnly=False
        self.StdoutHandling=True
        self.PopupHandling=True
        
        self.AddStdoutHandlerCallback("ALF_PROGRESS ([0-9]+)").HandleCallback += self.HandleStdoutProgress
        self.AddStdoutHandlerCallback("Error:(.*)").HandleCallback += self.HandleStdoutError
        
        # self.AddPopupHandler( ".*Houdini DSO Error.*", "OK" )

    def isRezEnabled(self):
        job = self.GetJob()
        for k in ['DEADLINE_REZ_REQUEST_PACKAGES', 'DEADLINE_REZ_TOOLS']:
            if job.GetJobExtraInfoKeyValue(k):
                return True
        return False
    
    def RenderExecutable(self):
        huskpath = self.GetPluginInfoEntry("HuskPath")
        huskexe = self.GetPluginInfoEntry("HuskExecutable")

        if self.isRezEnabled():
            print('Rez enabled - will try and find "husk" in tools')
            try:
                return self.GetRenderExecutable("Husk_Executable")
            except:
                print('Failed to find husk in DEADLINE_REZ_TOOLS - will use "{}"'.format(huskexe))
                return huskexe
        else:
            if huskpath:
                huskpath = RepositoryUtils.CheckPathMapping(huskpath)
                huskpath += '/'

            if sys.platform == 'win32':
                return huskpath + huskexe + '.exe'
            return huskpath + huskexe
        
    def RenderArgument(self):
        # get usd file
        usdFile = self.GetPluginInfoEntryWithDefault( "SceneFile",self.GetDataFilename())
        usdFile = RepositoryUtils.CheckPathMapping( usdFile )
        usdFile = usdFile.replace( "\\", "/" )
        
        if SystemUtils.IsRunningOnWindows():
            usdFile = usdFile.replace( "/", "\\" )
            if usdFile.startswith( "\\" ) and not usdFile.startswith( "\\\\" ):
                usdFile = "\\" + usdFile
        else:
            usdFile = usdFile.replace( "\\", "/" )
    
        self.LogInfo( "Rendering USD file: " + usdFile )
        
        # Get output file.
        outputFile = self.GetPluginInfoEntryWithDefault( "Output", "" )
        outputFile = RepositoryUtils.CheckPathMapping( outputFile )

        if SystemUtils.IsRunningOnWindows():
            outputFile = outputFile.replace( "/", "\\" )
            if outputFile.startswith( "\\" ) and not outputFile.startswith( "\\\\" ):
                outputFile = "\\" + outputFile
        else:
            outputFile = outputFile.replace( "\\", "/" )

        self.LogInfo( "Rendering output to " + outputFile )

        duration = (self.GetEndFrame() - self.GetStartFrame()) + 1
        
        # set arguments
        arguments = '--renderer "{}"'.format(self.GetPluginInfoEntryWithDefault( "HuskRenderer", "Karma" ))
        arguments += ' -f {}'.format(self.GetStartFrame()) 
        arguments += ' -n {}'.format(duration)
        arguments += ' -Va2' # alf progress
        arguments += ' --make-output-path'
        arguments += ' -o "{}"'.format(outputFile)

        # allow user to override arguments
        additionalargs = self.GetPluginInfoEntryWithDefault( "CommandLineOptions", "" )
        if additionalargs:
            arguments += ' {} '.format(additionalargs)

        # add usd input file argument
        arguments += ' "{}"'.format(usdFile)
        
        return arguments
        
    def HandleStdoutProgress(self):
        self.SetStatusMessage(self.GetRegexMatch(0))
        self.SetProgress(float(self.GetRegexMatch(1)))
        #self.SuppressThisLine()
        
    def HandleStdoutError(self):
        self.FailRender(self.GetRegexMatch(0))