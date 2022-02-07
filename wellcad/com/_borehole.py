from ._dispatch_wrapper import DispatchWrapper
from ._log import Log
from ._depth import Depth
from ._header import Header
from ._title import Title
from ._page import Page
from ._workspace import Workspace
from ._odbc import Odbc


class Borehole(DispatchWrapper):
    _DISPATCH_METHODS = ("Log", "ApplyStructureTrueToApparentCorrection", "ApplyStructureApparentToTrueCorrection",
                         "RemoveStructuralDip", "ExtractStructureIntervalStatistic", "ColorClassification",
                         "RepresentativePicks", "ImageComplexityMap", "NormalizeImage", "OrientImageToNorth",
                         "FilterImageLog", "ApplyConditionalTesting", "RQD", "GrainSizeSorting", "StackTraces", 
                         "FilterFWSLog", "AverageFilterFWSLog", "FreqFilterFwsLog","ApplyStandOffCorrection",
                         "CompensatedVelocity", "ApplySemblanceProcessing", "ProcessReflectedTubeWave", "PickFirstArrival",
                         "PickE1Arrival", "ExtractE1Amplitude", "AdjustPickToExtremum","ExtractWindowPeakAmplitude",
                         "ApplyNaturalGammaBoreholeCorrection", "ApplyTotalGammaCalibration", "CorrectDeadSensor", 
                         "CalculateFluidVelocity", "CalculateApparentMetalLoss",)

    @property
    def name(self):
        """Returns the title of a borehole document."""
        return self._dispatch.Name

    @name.setter
    def name(self, name):
        """Sets the title of a borehole document.
        
        Arguments:
            name -- String specifying the new name of the document.
        """

        self._dispatch.Name = name

    @property
    def version_major(self):
        """Returns the major version number of WellCAD."""
        return self._dispatch.VersionMajor

    @property
    def version_minor(self):
        """Returns the major version number of WellCAD."""
        return self._dispatch.VersionMinor

    @property
    def version_build(self):
        """Returns the build number of WellCAD."""
        return self._dispatch.VersionBuild

    @property
    def auto_update(self):
        """Returns True if the auto update of the document is enabled."""
        return self._dispatch.AutoUpdate

    @auto_update.setter
    def auto_update(self, flag):
        """Sets the auto update status of the borehole document.
        
        Arguments:
            flag -- set to True to enable the auto update or tp False
                    to disable the automatic refresh.

        """

        self._dispatch.AutoUpdate = flag

    def refresh_window(self):
        """Performs a one time refresh of the borehole view"""
        self._dispatch.RefreshWindow()

    def set_draft_mode(self, display_mode=0):
        """Toggles the view of the borehole document.
        
        A borehole document can be displayed in the following modes:
        0 - Page Layout
        1 - Draft and fit
        2 - Draft

        Arguments:
            display_mode -- Integer specifying the document viewing mode
        """

        self._dispatch.SetDraftMode(display_mode)

    def minimize_document_window(self):
        """Shrinks the document window to an icon.
        
        Works only if document windows are not tabbed.
        """

        self._dispatch.MinimizeWindow()

    def maximize_document_window(self):
        """Enlarges the document window to fit the WellCAD frame.
        
        Works only if document windows are not tabbed.
        """

        self._dispatch.MaximizeWindow()

    @property
    def bottom_depth(self):
        """Returns the bottom of the document in actual depth units."""
        return self._dispatch.BottomDepth

    @property
    def top_depth(self):
        """Returns the top of the document in actual depth units."""
        return self._dispatch.TopDepth

    def set_visible_depth_range(self, top_depth, bottom_depth):
        """Adjusts the depth range displayed in a borehole view.
        
        Arguments:
            top_depth -- Depth at which the data display should start.
            bottom_depth -- Depth at which the data display terminates.
        """

        self._dispatch.SetVisibleDepthRange(top_depth, bottom_depth)

    @property
    def depth(self):
        """Depth: The reference/master vertical axis. Can be in depth or time."""
        return Depth(self._dispatch.Depth)

    @property
    def header(self):
        """Header: The document header for this borehole document."""
        return Header(self._dispatch.Header)

    @property
    def page(self):
        """Page: A page object for the borehole document."""
        return Page(self._dispatch.Page)

    def create_new_workspace(self, workspace_type, config=None):
        """Creates a new workspace and return the corresponding object.

        For a full description of the parameters to be used in the
        configuration file refer to the WellCAD help documentation.

        Parameters
        ----------
            workspace_type : int
                Available workspace types are:
                    * 1 = ISI workspace
                    * 2 = Casing integrity
                    * 3 = NMR
            config : str
                Path and name of the .ini file containing the
                workspace initialization parameters.

        Returns
        -------
        Workspace
            The specified workspace object.
        """
        return Workspace(self._dispatch.CreateNewWorkspace(workspace_type, config))


    def workspace(self,index_or_name):
        """ Retrieve a workspace (e.g. Image & Structure Processing Workspace)
        that has been already setup and is part of the borehole document.
        
        Parameters
        ----------
        index_or_name : int or str
            The name (string) or index (zero based index) of the
            workspace to be retrieved.

        Returns
        -------
        Workspace
            The specified workspace object.
        """
        return Workspace(self._dispatch.Workspace(index_or_name))

    @property
    def odbc(self):
        """Odbc: An ODBC object that allows interaction with a database."""
        return Odbc(self._dispatch.ODBC)

    def connect_to(self, server_name, server_address, port_number="1600"):
        """Connect WellCAD to the ALT logging system.
        
        Arguments:
            server_name -- Must be set to 'TFD'.
            server_address -- IP address of the computer to connect to.
            port_number -- Part number used (default is 1600).
        
        """

        self._dispatch.ConnectTo(server_name, server_address, port_number)

    def disconnect_from(self, server_name, server_address):
        """Cuts the connection between WellCAD and the logging system.
        
        Arguments:
            server_name -- Must be set to 'TFD'.
            server_address -- IP address of the computer to connect to.
        """

        self._dispatch.DisconnectFrom(server_name, server_address)

    def save_as(self, file_name):
        """Saves the borehole document as WCL file.
        
        Arguments:
            file_name -- Path and file name (e.g. C:\Temp\Well1.wcl)

        Returns:
            True if the saving process was successfull. 
        """

        return self._dispatch.SaveAs(file_name)

    def file_export(self,
                    file_name,
                    prompt_user=True,
                    config="",
                    logfile=""):
        """Exports the document to the specified file.
        
        Supported file formats are LAS, DLIS, EMF, CGM, JPG, PNG, TIF,
        BMP, WCL and PDF. Please refer to the WellCAD help file for a
        desciption of the export parameters to be used in the
        configuration file and parameter string.

        Arguments:
            file_name -- Path and name of the file to export.
            prompt_user -- If set to False no dialog box will be
                           displayed.
            config -- Path and name of the .ini file containing the
                      export parameters.
            logfile -- Path and name of the file to log error messages.
            
        """
        self._dispatch.FileExport(file_name,
                                  prompt_user,
                                  config,
                                  logfile)

    def print(self,
              enable_dialog,
              top_depth,
              bottom_depth,
              nb_of_copies):
        """Sends the current document to the printer.

        If the print dialog box is displayed the user can select the
        printer otherwise the printer installed as default is used.
        
        Arguments:
            enable_dialog -- Displays the print dialog box if True.
            top_depth -- Start depth of the interval to print.
            bottom_depth -- Base of the printed depth interval.
            nb_of_copies -- Defines the number of copies to be printed.
        """

        self._dispatch.DoPrint(self,
                               enable_dialog,
                               top_depth,
                               bottom_depth,
                               nb_of_copies)

    # Methods for general log handling

    @property
    def nb_of_logs(self):
        """Number of logs present in the borehole document."""
        return self._dispatch.NbOfLogs

    def log(self, index_or_name):
        """Gets a log by name or by index.

        Parameters
        ----------
        index_or_name : int or str
            The index or the name of the log

        Returns
        -------
        Log
            The Log object.
        """
        return Log(self._dispatch.Log(index_or_name))

    def title(self, log_name):
        """Gets the title object for the specified log.

        Parameters
        ----------
        log_name : str
            The name of the log to get the title for.

        Returns
        -------
        Title
            The Title object.
        """
        return Title(self._dispatch.Title(log_name))

    def insert_new_log(self, log_type):
        """Creates a new log and log object.
        
        The log type that will be created depends on the
        log_type parameter which can take the following values:
        1 - Well Log
        2 - Formula Log
        3 - Mud Log
        4 - FWS Log
        5 - Image Log
        6 - Structure Log
        7 - Litho Log
        8 - Comment Log
        9 - Engineering Log
        10 - RGB Log
        13 - Interval Log
        14 - Analysis Log
        15 - Percent Log
        16 - CoreDesc Log
        17 - Depth Log
        18 - Strata Log
        19 - Satcking Pattern Log
        20 - Polar and Rose Log
        21 - Cross Section Log
        22 - OLE Log
        23 - Shading Log
        24 - Marker Log
        25 - Breakout Log
        26 - Bio Log
        
        Arguments:
            log_type -- Integer specifying the type of log. 

        Returns:
            A log object.
        """

        obLog = self._dispatch.InsertNewLog(log_type)
        return Log(obLog)

    def convert_log_to(self,
                       log,
                       log_type,
                       prompt_user=True,
                       config=""):
        """New log object by converting one log type into another.
        
        Please refer to the WellCAD documentation about which log type
        conversions are possible. Dialog boxes will be displayed if
        available when the bPromptUser flag is set to True. If set to
        False default parameters will be used or the conversion
        parameters will be taken from a configuration file or parameter
        string. The Automation Module chapter of the WellCAD help file
        provides a description of the file format and all parameters to
        be used in the configuration file / parameter string. 

        Arguments:
            log 		-- Title (string) or zero based index (Integer)
                              of the log to convert.
            log_type 	-- Integer specifying the type of log to be created.
            prompt_user -- (Optional) If set to True dialog boxes
                           will be displayed.
            config		-- (Optional) Path and filename of the
                           configuration file or parameter string.  

        Returns:
            The object of the new log.
        """

        self._dispatch._FlagAsMethod("ConvertLogTo")
        obLog = self._dispatch.ConvertLogTo(log, log_type, prompt_user, config)
        return Log(obLog)

    def copy_log(self, oblog):
        """Copy and pastes a log.
        
        Copies a log within the same or between two borehole documents.

        Arguments:
            oblog -- An object of the log to copy.

        Returns:
            An object of the copied log.
        """

        self._dispatch._FlagAsMethod("AddLog")
        oblog_copy = self._dispatch.AddLog(oblog.dispatch)
        return Log(oblog_copy)

    def remove_log(self, log):
        """Deletes the specified log from the borehole document.
        
        Arguments:
            log -- Zero based index (integer) or title (string)
                   of the log to delete.
        """

        self._dispatch.RemoveLog(log)

    def clear_log_contents(self, log):
        """Removes the data from a log and leaves the log empty.
        
        Arguments:
            log -- Zero based index (integer) or title (string).
        """

        self._dispatch.ClearLogContents(log)

    def apply_template(self,
                       path,
                       prompt_if_not_found=True,
                       create_new_logs=False,
                       create_new_layers=False,
                       apply_annotation_settings=False,
                       replace_header=False,
                       keep_charts=True,
                       new_charts=False,
                       overwrite_workspaces=False,
                       new_workspaces=False,
                       config=""):
        """Loads and applies a document layout template (.WDT)

        For a more detailed description of all available parameters
        in the configuration file refer to the WellCAD help file.
        
        Arguments:
            path -- Path and name of the .WDT file.
            prompt_if_not_found -- If True a dialog box will be
                                  displayed for each log not found.
            create_new_layers -- If True new annotation layers will be
                                 loaded from the template.
            apply_annotation_settings -- Loads the layout settings for
                                         operational symbols.
            replace_header -- If True the current document header will
                              be replaced.
            keep_charts -- If True cross-plot charts will be kept in
                           the document.
            new_charts -- If True cross-plot charts will be loaded from
                          the template.
            overwrite_workspaces -- If True work spaces in the document
                                    will be overwritten.
            new_workspaces -- If True work spaces will be loaded from
                              the template.
            config -- Path and name of the configuraion file
                      or parameter string.
        """

        self._dispatch.ApplyTemplate(path,
                                     prompt_if_not_found,
                                     create_new_logs,
                                     create_new_layers,
                                     apply_annotation_settings,
                                     replace_header,
                                     keep_charts,
                                     new_charts,
                                     overwrite_workspaces,
                                     new_workspaces,
                                     config)

    # Common log edition

    def slice_log(self,
                  log,
                  slice_depth,
                  create_top=True,
                  create_bottom=True,
                  keep_original=True):
        """Cuts the specified log at the given depth.

        Arguments:
            log -- Zero based index (integer) or title (string) of the
                   log to slice.
            slice_depth -- Depth at which the cut will be made.
            create_top -- If set to True the upper part of the log will
                          be kept in the document. 
            create_bottom -- If set to True the lower part of the log
                             will remain in the document.
            keep_original -- If set to True the original log will
                             remain in the document.
        """

        self._dispatch.SliceLog(log,
                                slice_depth,
                                create_top,
                                create_bottom,
                                keep_original)

    def merge_logs(self,
                   log_a,
                   log_b,
                   ave_overlap=True,
                   create_new=True):
        """Merges two logs of the same type.

        Arguments:
            log_a -- Zero based index (integer) or title (string) of
                     the log.
            log_b -- Zero based index (integer) or title (string) of
                     the log.
            ave_overlap -- If set to False log_a will overwrite log_b.
            create_new -- If set to False log_b will be pushed
                          into log_a.
        """

        self._dispatch.MergeLogs(log_a, log_b, ave_overlap, create_new)

    def merge_same_log_items(self, log):
        """Merges data intervals with same litho codes or text.
        
        Arguments:
            log -- Zero based index (integer) or title (string) of
                   the Litho log.
        """

        self._dispatch.MergeSameLogItems(log)

    def extend_log(self, log, top_depth, bottom_depth):
        """Extends the depth range of a Well log type.
        
        Call this method to allocate the memory for the additional
        depth range of the Well Log.

        Arguments:
            log -- Zero based index (integer) or title (string) of
                   the Well log.
            top_depth -- Top of the final depth range.
            bottom_depth -- Base of the final depth range.
        """

        self._dispatch.ExtendLog(log, top_depth, bottom_depth)

    def depth_shift_log(self,
                        log,
                        shift,
                        top_depth="",
                        bottom_depth=""):
        """Performs a bulk shift to all the log's data.

        If top_depth and bottom_depth are specified the depth shift
        will be restricted to this interval.

        Arguments:
            log -- Zero based index (integer) or title (string) of
                   the log.
            shift -- Amount of the depth shift (positive = down,
                     negative = up).
            top_depth -- Upper depth limit of the shifted interval.
            bottom_depth -- Lower depth limit of the shifted interval.
        """

        self._dispatch.DepthShiftLog(log,
                                     shift,
                                     top_depth,
                                     bottom_depth)

    def depth_match_log(self, log="", depth_log=""):
        """Perfoms a depth matching using a shift table.

        The shift table will be provided as a Depth Log and the process
        of shifting is equivalent to the DepthMatcher in WellCAD. If
        the parameter list is empty or if no depth_log has been
        specified the DepthMatcher dialog box will be displayed.

        Arguments:
            log -- Zero based index (integer) or title (string) of
                   the log to match.
            depth_log -- Zero based index (integer) or title (string) of
                   the Depth Log containing the shift table.
        
        """

        self._dispatch.DepthMatchLog(log, depth_log)

    def fill_log(self,
                 log,
                 top_depth,
                 bottom_depth,
                 step,
                 thickness,
                 user_defined_intervals=True,
                 interval_log=""):
        """Creates intervals in Cross-section and Polar & Rose logs.
        
        Arguments:
            log -- Zero based index (integer) or title (string) of
                   the log to fill with intervals.
            top_depth -- Start depth of the first interval.
            bottom_depth -- Start depth of the last interval.
            step -- Interval frequency (enter 5 for an interval
                    starting every 5 meter or ft).
            thickness -- Interval thickness (in depth units).
            user_defined_intervals = If set to False the intervals
                                     will be loaded from a reference
                                     log.
            interval_log -- Zero based index (integer) or title
                            (string) of the log containing the
                            reference intervals.
        """

        self._dispatch.FillLog(log,
                               top_depth,
                               bottom_depth,
                               step,
                               thickness,
                               user_defined_intervals,
                               interval_log)

    # Common log processes

    def filter_log(self, log, prompt_user=True, config=""):
        """Applies a user selected filter to Well Logs.

        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation. 
        
        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        Returns:
            An object of the filtered log.
        """

        self._dispatch._FlagAsMethod("FilterLog")
        oblog = self._dispatch.FilterLog(log, prompt_user, config)
        return Log(oblog)

    def filter_log_average(self, log, filter_width, circular_data=False, data_unit="degrees"):
        """Applies an average filter to a well log.
            
        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            filter_width -- Interger defining the length of the filter
                            window in samples.
            circular_data -- Boolean defining whether the log contain angular data.
            data_unit -- Either 'degrees' or 'radians'. 

        Returns:
            An object of the filtered log.
        """

        # compose in-line parameter string
        circular_data_flag = "no"
        if circular_data:
            circular_data_flag = "yes"
        config = "FilterType=MovingAverage, MaxDepthRange=yes,\
                  FilterWidth=" + str(max(1, filter_width)) \
                 + ",CircularData=" + circular_data_flag \
                 + ",DataUnit=" + data_unit
        # call method
        self._dispatch._FlagAsMethod("FilterLog")
        oblog = self._dispatch.FilterLog(log, False, config)
        return Log(oblog)

    def filter_log_median(self, log, filter_width, circular_data=False, data_unit="degrees"):
        """Applies a median filter to a well log.
            
        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            filter_width -- Interger defining the length of the filter
                            window in samples.
            circular_data -- True if the log contains angular data
                             (default = False).
            data_unit -- Either 'degrees' or 'radians'
                         (default = 'degrees'). 

        Returns:
            An object of the filtered log.
        """

        # compose in-line parameter string
        circular_data_flag = "no"
        if circular_data:
            circular_data_flag = "yes"
        config = "FilterType=Median, MaxDepthRange=yes,\
                  FilterWidth=" + str(max(1, filter_width)) \
                 + ",CircularData=" + circular_data_flag \
                 + ",DataUnit=" + data_unit
        # call method
        self._dispatch._FlagAsMethod("FilterLog")
        oblog = self._dispatch.FilterLog(log, False, config)
        return Log(oblog)

    def filter_log_weighted_ave(self, log, filter_width, circular_data=False, data_unit="degrees"):
        """Applies a weighted average filter to a well log.
            
        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            filter_width -- Interger defining the length of the filter
                            window in samples.
            circular_data -- True if the log contains angular data
                             (default = False).
            data_unit -- Either 'degrees' or 'radians'
                         (default = 'degrees'). 

        Returns:
            An object of the filtered log.
        """

        # compose in-line parameter string
        circular_data_flag = "no"
        if circular_data:
            circular_data_flag = "yes"
        config = "FilterType=WeightedAverage, MaxDepthRange=yes,\
                  FilterWidth=" + str(max(1, filter_width)) \
                 + ",CircularData=" + circular_data_flag \
                 + ",DataUnit=" + data_unit
        # call method
        self._dispatch._FlagAsMethod("FilterLog")
        oblog = self._dispatch.FilterLog(log, False, config)
        return Log(oblog)

    def block_log(self, log, prompt_user=True, config=""):
        """Calculates statistics for log data per depth interval.
        
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation. 

        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        """
        self._dispatch.BlockLog(log, prompt_user, config)

    def multi_log_statistics(self, logs, prompt_user=True, config=""):
        """Calculates statistical values from multiple logs.
        
        Statistical values are derived from multiple logs at the
        same depth.
        E.g. an avege density from two density logs.
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation.

        Arguments:
            logs -- Title (string) or list of the log(s) to process.
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.
        """

        self._dispatch.ExtractWellLogStatistics(logs, prompt_user, config)

    def normalize_perc_log(self, log, prompt_user=True, config=""):
        """Normalizes the data in a Percentage or Analysis Log.

        For a full list of prcessing parameters please refer to the
        WellCAD help documentation.

        Arguments:
            log -- Zero based index (integer) or title (string) of
                   the log to normalize.
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.
        
        """

        self._dispatch.Normalize(log, prompt_user, config)

    def resample_log(self, log, prompt_user=True, config=""):
        """Resamples a data set using the new sample step provided.
        
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation. 

        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        """

        self._dispatch._FlagAsMethod("ResampleLog")
        oblog = self._dispatch.ResampleLog(log, prompt_user, config)
        return Log(oblog)

    def interpolate_log(self, log, prompt_user=True, config=""):
        """Applies a linear interpolation across gaps in a data set.
        
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation. 

        Arguments:
            log	-- Zero based index (integer) or title (string) of
                   the log to process.
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        Returns:
            An object of the interpolated log.
        """

        self._dispatch._FlagAsMethod("InterpolateLog")
        oblog = self._dispatch.InterpolateLog(log, prompt_user, config)
        return Log(oblog)

    def borehole_deviation(self, prompt_user=True, config=""):
        """Computes Azimuth, Tilt and RBR.
        
        The method uses accelerometer and inclinometer x,y,z components
        of an orientation sensor to compute borhole azimuth, tilt and
        relative bearing (RBR). The input logs are specified int the
        config file or in-line as part of the config string.
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation. 

        Arguments:
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        """

        self._dispatch.CalculateBoreholeDeviation(prompt_user, config)

    def borehole_coordinates(self, prompt_user=True, config=""):
        """Creates Northing, Easting and TVD data.
        
        Using borehole azimuth and tilt as input data this method
        calculates northing, easting and tvd coordinates and outputs
        them in well / mud logs.
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation.

        Arguments:
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        """

        self._dispatch.CalculateBoreholeCoordinates(prompt_user, config)

    def borehole_closure(self, prompt_user=True, config=""):
        """Derives closure distance, closure angle and dog-leg data.
        
        Using borehole azimuth, tilt, northing and easting as input
        data this method calculates the drift distance (closure), 
        drift angle (cllosure angle) and the dog-leg-severity and
        outputs the data in well / mud logs.
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation.

        Arguments:
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        """

        self._dispatch.CalculateBoreholeClosure(prompt_user, config)

    def elog_correction(self, prompt_user=True, config=""):
        """ Environmental corrections for normal resisitivity data.
        
        A full description of the method and its parameters is given
        in the Automation Module chapter of the WellCAD help
        documentation.

        Arguments:
            prompt_user -- If set to False the processing parameters
                           will be taken from the config file/string.
            config -- Path and name of the configuration file or
                      a parameter string.

        Returns:
            An object of the last corrected log.
        """

        self._dispatch._FlagAsMethod("ElogCorrection")
        oblog = self._dispatch.ElogCorrection(prompt_user, config)
        return Log(oblog)

    def correct_bad_traces(self, log=None):
        """Replaces NULL data traces in Image, RGB and FWS logs.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box
            displaying a list of available logs will be displayed.
        """
        self._dispatch.CorrectBadTraces(log)

    def stack_traces(self, is_spectrum=None, log=None, prompt_user=None, config=None):
        """Stacks multiple FWS traces to create and average trace.
        Parameters
        ----------
        is_spectrum : bool, optional
            Whether the log is a spectrum or not.
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini
                [StackTraces]
                NumberOfStacks = 5
        Returns
        -------
        Log
            The resulting log.
        """

        return Log(self._dispatch.StackTraces(is_spectrum, log, prompt_user, config))

    def apply_conditional_testing(self, log_if=None, log_then=None, prompt_user=None, config=None):
        """Applies conditional testing (If-Then-Else) to image log
        values.

        Parameters
        ----------
        log_if : str or int, optional
            Zero based index (integer) or title (string) of
            the log used for the 'If' clause.
        log_then : str or int, optional
            Zero based index (integer) or title (string) of
            the log used for the 'Then' clause.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ApplyConditionalTesting]
                Condition = != / <= / >= / > / < / ==
                ConditionValue = 100.0
                IsSecondCondition = yes / no
                SecondLogTest = <title of second log to test>
                OperatorSecondCondition = AND / OR
                SecondCondition = != / <= / >= / > / < / ==
                SecondConditionValue = 120.0
                ThenValue = NULL
                ElseValue = Amplitude

        Returns
        -------
        Log
            A newly created log.
        """
        return Log(self._dispatch.ApplyConditionalTesting(log_if, log_then, prompt_user, config))

    def filter_image_log(self, log=None, prompt_user=None, config=None):
        """Average, median and clipping filter for image logs.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [FilterImageLog]
                FilterType = Average / Median / Despiking
                FilterWidth = 3
                FilterHeight = 3
                HighCutLimit = 75
                LowCutLimit = 15

        Returns
        -------
        Log
            The computed log.
        """
        return Log(self._dispatch.FilterImageLog(log, prompt_user, config))

    def mirror_image(self, log=None):
        """Rearranges the data within an image log so that the data
        appears mirrored when compared to the original image.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        """
        self._dispatch.MirrorImage(log)

    def rotate_image(self, log=None, prompt_user=None, config=None):
        """Rotate the image data by adding an angle (clockwise
        rotation) or subtracting it (counterclockwise rotation).

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [RotateImage]
                RotateBy= 1.2 / Log
                RotateClockwise = yes / no
        """
        self._dispatch.RotateImage(log, prompt_user, config)

    def orient_image_to_highside(self, log=None, prompt_user=None, config=None):
        """Rotates an image log to high side according to the
        deviation channels provided.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [OrientImageToHighside]
                InclX = Acc X
                InclY = Acc Y
                InclZ =
                InclXPositive = yes / no
                InclYPositive = yes / no
                InclZPositive = yes / no
                IsAccelerometer = yes / no
                MarkerPosition = 180.2
        """
        self._dispatch.OrientImageToHighside(log, prompt_user, config)

    def orient_image_to_north(self, log=None, prompt_user=None, config=None):
        """Rotates an image log to magnetic north according to the
        deviation channels provided.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
                        Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [OrientImageToNorth]
                MagX = Mag X
                MagY = Mag Y
                MagZ = Mag Z
                InclX = Acc X
                InclY = Acc Y
                InclZ =
                MagXPositive = yes / no
                MagYPositive = yes / no
                MagZPositive = yes / no
                InclXPositive = yes / no
                InclYPositive = yes / no
                InclZPositive = yes / no
                IsAccelerometer = yes / no
                MarkerPosition = 180.2
        """
        self._dispatch.OrientImageToNorth(log, prompt_user, config)

    def extract_image_log_image_statistics(self, log=None, prompt_user=None, config=None):
        """Extracts minimum, maximum, average, median and other
        statistical values fulfilling an optional condition from each
        image log trace.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini
                [ExtractImageLogStatistics]
                Minimum = yes / no
                Maximum = yes / no
                Mode = yes / no
                Average = yes / no
                Median = yes / no
                StandardDeviation = yes / no
                Percentage = yes / no
                MeanAbsoluteDeviation = yes / no
                GeometricMean = yes / no
                GeometricStandardDeviation = yes / no
                Skewness = yes / no
                Kurtosis = yes / no
                Quartiles = yes / no
                RMS = yes / no
                RMSD = yes / no
                Condition = 0 (None) / 1 (lower than Value 1) / 2 (larger than Value1) / 3 (lower and equal)
                / 4 (larger and equal) / 5 (equal) / 6 (not equal) / 7 (between Value1 and Value2)
                / 8 (between and equal to Value1 and Value2)
                Value1 = 50
                Value2 = 100
                OneOutputlogPerImageLog = yes / no
                DepthRange = Maximum / UserDefined / Zones / LogZones
                TopDepth = 1.0
                BottomDepth = 200.0
                ZonesDepthRange = 10.0, 20.0, 50.0, 80.0 (top1, bottom1,...,topN, bottomN)
                LogZonesDepthRange=Litho,06,05 (log name, interval code 1, interval code 2,...)
        """
        self._dispatch.ExtractImageLogStatistics(log, prompt_user, config)

    def normalize_image(self, log=None, prompt_user=None, config=None):
        """Applies Static or Dynamic normalization to image logs

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [NormalizeImage]
                Mode = Static /Dynamic_1D / Dynamic_2D / HighPass
                WindowHeight = 0.3
                WindowWidth = 5


        Returns
        -------
        Log
            The normalized log.
        """
        return Log(self._dispatch.NormalizeImage(log, prompt_user, config))

    def image_complexity_map(self, log=None, prompt_user=None, config=None):
        """Computes the complexity map from an RGB or image log.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ImageComplexityMap]
                LogType=1
                ;RGB OTV image: 0,
                ;Greyscale OTV image: 1,
                ;Diamond-drilled hole, ATV image: 2,
                ;RC-drilled hole, ATV image: 3,
                ;FMI image: 4,
                Palette=0,0,0,255,56,255,0,0,12,64,224,208,21,50,205,50,31,255,255,0,39,255,215,0,47,255,104,32


        Returns
        -------
        Log
            The computed log.
        """
        return Log(self._dispatch.ImageComplexityMap(log, prompt_user, config))
    
    def apply_structure_apparent_to_true_correction(self, log=None, prompt_user=None, config=None):
        """Corrects the apparent azimuth and dip angles in a
        Structure log

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

            [ApplyStructureApparentToTrueCorrection]
            AzimuthLog = azimuth log name
            TiltLog = tilt log name
            ReferenceIsNorth = yes / no

        Returns
        -------
        Log
            The corrected log.
        """
        return Log(self._dispatch.ApplyStructureApparentToTrueCorrection(log, prompt_user, config))

    def apply_structure_true_to_apparent_correction(self, log=None, prompt_user=None, config=None):
        """Recalculates the apparent azimuth and dip angles in a
        Structure log from the true structure angles.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ApplyStructureApparentToTrueCorrection]
                AzimuthLog = azimuth log name
                TiltLog = tilt log name
                ReferenceIsNorth = yes / no

        Returns
        -------
        Log
            The computed log.
        """
        return Log(self._dispatch.ApplyStructureTrueToApparentCorrection(log, prompt_user, config))

    def recalculate_structure_azimuth(self, log=None, prompt_user=None, config=None):
        """Adds or subtracts a value from all Azimuth data within a
        structure log.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [RecalculateStructureAzimuth]
                Angle = 45 / Log
                RotateClockwise = yes / no
                MaxDepthRange = yes / no
                TopDepth = 0.0
                BottomDepth = 1.0

        """
        self._dispatch.RecalculateStructureAzimuth(log, prompt_user, config)

    def recalculate_structure_dip(self, log=None, prompt_user=None, config=None):
        """Correct the dip angle data within a structure log for new
        caliper settings.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [RecalculateStructureDip]
                Caliper = Log / 200.0
                CaliperUnit = mm / in
                MaxDepthRange = yes / no
                TopDepth = 0
                BottomDepth = 1

        """
        self._dispatch.RecalculateStructureDip(log, prompt_user, config)

    def remove_structural_dip(self, log=None, prompt_user=None, config=None):
        """Removes a given regional dip and azimuth from the data in
        a structure log and recalculates new Dip and Azimuth angles.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [RemoveStructuralDip]
                Azimuth = Log /45
                Dip = Log /10
                MaxDepthRange = yes / no
                TopDepth = 0.0
                BottomDepth = 1.0

        Returns
        -------
        Log
            The computed log.
        """
        return Log(self._dispatch.RemoveStructuralDip(log, prompt_user, config))

    def extract_color_components(self, log=None, method=None, color_model=None, prompt_user=None):
        """Allows the extraction of color data from an RGB Log.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        method : int, optional
            The methode used.
            Available models are:

            * 0 = Average
            * 1 = Mode
            * 2 = Image Log
        color_model : int, optional
            The color model used.
            Available models are:

            * 0 = RGB
            * 1 = HSV
            * 2 = YUV
            * 3 = CIELAB
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        """
        self._dispatch.ExtractColorComponents(log, method, color_model, prompt_user)

    def color_classification(self, log=None, prompt_user=None, config=None):
        """Builds color classes from an RGB Log based on user
        specified reference colors.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the RGB log to process.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ColorClassification]
                OutputImage = yes
                OutputAnalysis = yes
                NoiseReduction = 10
                Class1="Class 1";"0,255,0";58;50;"166,143,81"
                Class2="Class 2";"255,0,255";37;50;"44,42,34"
                Class3="Class 3";"255,255,0";34;50;"251,165,75"

        Returns
        -------
        Log
            One of the computed log.  #TODO figure out which log is returned
        """
        return Log(self._dispatch.ColorClassification(log, prompt_user, config))

    def adjust_image_brightness_and_contrast(self, log=None, prompt_user=None):  #TODO you can't specify the parameters in the function call ?
        """Adjusts the brightness and contrast in RGB logs

        Parameters
        ----------
        log : str or int, optional
            A string specifying the log name or an integer
            representing the index of the log to be processed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to False, the new brightness and
            contrast values will be determined automatically.
        """
        self._dispatch.AdjustImageBrightnessAndContrast(log, prompt_user)

    def extract_structure_interval_statistics(self, log=None, prompt_user=None, config=None):
        """Allows determination of statistical values (e.g. frequency
        of dips) per interval from a structure log.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ExtractStructureIntervalStatistic]
                Reference = 5.0 / Log
                OutputMinAzimuth = yes / no
                OutputMaxAzimuth = yes / no
                OutputAverageAzimuth = yes / no
                OutputMinDip = yes / no
                OutputMaxDip = yes / no
                OutputAverageDip = yes / no
                OutputMinTilt = yes / no
                OutputMaxTilt = yes / no
                OutputAverageTilt = yes / no
                OutputMinAperture = yes / no
                OutputMaxAperture = yes / no
                OutputAverageAperture = yes / no
                OutputMinLength = yes / no
                OutputMaxLength = yes / no
                OutputAverageLength = yes / no
                OutputMinOpening = yes / no
                OutputMaxOpening = yes / no

        Returns
        -------
        Log
            One of the computed log.  #TODO figure out which
        """
        return Log(self._dispatch.ExtractStructureIntervalStatistic(log, prompt_user, config))
    
    def rqd(self, log=None, prompt_user=None, config=None):
        """Computes the Rock Quality Designation from the structure
        picks in a Structure Log.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [RQD]
                CorePieceLength = 0.1
                CoreLength = 1
                AttributeName1 = Defect Type
                AttributeValues1 = JT-MAJ, JT-MED, JT-MIN,
                AttributeName2 = Defect Condition
                AttributeValues2 = cont, part
                DepthRange = Maximum / UserDefined / Zones
                'UserDefined
                TopDepth=25
                BottomDepth=30
                'Zones
                ZonesDepthRange = 20,26, 24,30

        Returns
        -------
        Log
            The computed log.
        """
        return Log(self._dispatch.RQD(log, prompt_user, config))

    def representative_picks(self, log=None, prompt_user=None, config=None):
        """Used to derive the most representative picks from a
        Structure log given user defined classification limits.

        Parameters
        ----------
        log : str or int, optional
            Zero based index (integer) or title (string) of
            the log to process. If not provided, a dialog box 
            displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with
            the user. If set to  ``False`` the processing parameters
            will be retrieved from the specified configuration
            file. If no configuration file has been specified,
            default values will be used.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [RepresentativePicks]
                TopDepth=0.0
                BottomDepth=10.0
                TiltWindow=5.0 (structural dip angle interval, here +/- 5 degrees)
                AzimuthWindow=15.0 (structural azimuth angle interval, here +/- 15 degrees)
                DepthWindow=0.5
                KeepFeaturesUngrouped=TRUE / FALSE

        Returns
        -------
        Log
            The computed log.
        """
        return Log(self._dispatch.RepresentativePicks(log, prompt_user, config))



    def correct_dead_sensor(self, log=None, prompt_user=None, config=None):
        """Corrects the Null and invalid data columns in Image logs.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns ''None''.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [DeadSensor]
                ; Method : Automatic, Range, Columns
                ; ReplaceBy : Null, Average, Median, Interpolate, LogName or a numerical value
                Method = Automatic
                ReplaceBy = Average
                ; If Method = Automatic
                WindowHeight = 0
                Discrimination = 0.125
                MinDataHeight = 0
                ; If Method = Range
                WindowHeight = 0
                Low = 0
                High = 0
                ; If Method = Columns
                ; Columns : single index value or range like 15-20
                Columns = 1
        Returns
        -------
        Log
            A log with the corrected data.
        """
        return Log(self._dispatch.CorrectDeadSensor(log, prompt_user, config))

    def shift_correction(self, log=None, prompt_user=None, config=None):
        """Corrects the drift of data (e.g. MFC) in Image logs.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns ''None''.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ShiftCorrection]
                ; Zone1 : name, top, bottom, value
                OutputCorrections = yes / no
                ExtendTrends = yes / no
                Zone1=ref1, 25.0, 26.0, 101.2
                Zone2=ref2, 45.0, 47.0, 125.3

        Returns
        -------
        Log
            A log that has been corrected.
        """
        return Log(self._dispatch.ShiftCorrection(log, prompt_user, config))

    def calculate_fluid_velocity(self, log=None, prompt_user=None, config=None):
        """Estimates the fluid velocity from travel time measurements and given calibration points.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [CalculateFluidVelocity]
                ; If the AutoFill option is used the CalibrationPoints are not used.
                ; ToolRadius : in mmm
                ; TimeWindow : log name or value
                ; CalibrationPoint1 : depth, diameter in mm
                ; AutoFillFrom : depth value or 'Top'
                 ; AutoFillTo : depth value or 'Bottom'
                TravelTimeUnit = 0.1
                ToolRadius = 19
                TimeWindow = TimeWndLog / 74
                CalibrationPoint1 = 20.44, 96
                CalibrationPoint2 = 36.85, 96
                CalibrationPoint3 = ...
                ExtendTrends = yes / no
                AutoFillFrom = 0 / Top
                AutoFillTo = 0 / Bottom
                AutoFillCaliper = 0 / Log Name
                AutoFillStepSize = 1.0

        Returns
        -------
        Log
            A log giving the fluid velocity.
        """
        return Log(self._dispatch.CalculateFluidVelocity(log, prompt_user, config))

    def centralize(self, log=None, prompt_user=None, config=None):
        """Corrects travel time or multi-finger-caliper data for de-centralization effects
        and outputs a new image log.
        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns ''None''.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [Centralize]
                ; UseRange : use clipping range
                UseRange = yes / no
                CaliperLow = 0
                CaliperHigh = 0
                OutputEccentricity = yes / no
                OutputEccentricityDir = yes / no

        Returns
        -------
        Log
            A log with the data corrected for decentralization.
        """
        return Log(self._dispatch.Centralize(log, prompt_user, config))

    def calculate_acoustic_caliper(self, log=None, prompt_user=None, config=None):
        """Calculates borehole radius and caliper values from acoustic travel time measurements.

       Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [CalculateAcousticCaliper]
                ; CaliperUnit : mm, cm, in
                ; FluidVelocityUnit : m/s, km/s, m/ms, m/us, ft/s, ft/ms, ft/us, s/km, s/m, us/m, s/ft, us/ft
                ; ToolRadius : in mm
                TravelTimeUnit = 0.1
                CaliperUnit = mm
                ToolRadius = 19
                TimeWindow = TimeWndLog / 74
                FluidVelocity = VelocityLog / 1440
                FluidVelocityUnit= m/s
                CurveOutput = yes / no
                ImageOutput  = yes / no
        """
        self._dispatch.CalculateAcousticCaliper(log, prompt_user, config)

    def calculate_casing_thickness(self, log=None, prompt_user=None, config=None):
        """Calculates thickness values for a casing pipe from acoustic thickness travel time measurements.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [CalculateCasingThickness]
                ; ThicknessUnit : mm, cm, in
                ; SteelVelocityUnit : m/s, km/s, m/ms, m/us, ft/s, ft/ms, ft/us, s/km, s/m, us/m, s/ft, us/ft
                ; CurveOutput : output min, max, average thickness
                ; ImageOutput  : output the thickness as an image log
                TravelTimeUnit = 0.01
                SteelVelocity = VelocityLog / 5200
                SteelVelocityUnit= m/s
                CurveOutput = yes / no
                ImageOutput = yes / no
        """
        self._dispatch.CalculateCasingThickness(log, prompt_user, config)

    def calculate_apparent_metal_loss(self, log=None, prompt_user=None, config=None):
        """Calculates an apparent metal loss value for each trace of radius values stored in an image log.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [CalculateApparentMetalLoss]
                ; The units of the internal / external pipe radius values must be the same as the unit
                ; of the radius values in the image log.
                InternalPipeRadius = 1.9
                ExternalPipeRadius = 2.2
        Returns
        -------
        Log
            A log giving the metal loss.
        """
        return Log(self._dispatch.CalculateApparentMetalLoss(log, prompt_user, config))

    def radius_to_from_diameter(self, log=None, prompt_user=None, config=None):
        """Converts values data in an Image log from radius to diameter values or vice versa.

        Parameters
        ----------
        log : int or str
            Zero based index or title of the log to process.
            If not provided, the process returns ''None''.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [RadiusToFromDiameter]
                ;  Method : TwoTimesRadius, OppositeValues, HalfDiameter
                Method = TwoTimesRadius
        Returns
        -------
        Log
            A log giving diameter/radius.
        """
        return Log(self._dispatch.RadiusToFromDiameter(log, prompt_user, config))

    def outer_inner_radius_diameter(self, log=None, prompt_user=None, config=None):
        """The process takes an Image, Well or Mud log as input and computes from radius/diameter
        and thickness values an outer radius/diameter value.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns ''None''.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [OuterInnerRadiusDiameter]
                ; InputType : InnerRadius, OuterRadius, InnerDiameter, OuterDiameter
                ; OutputType : InnerRadius, OuterRadius, InnerDiameter, OuterDiameter
                ; Thickness = log name or value
                Thickness = THK
                InputType = InnerRadius
                OutputType = OuterDiameter
        Returns
        -------
        Log
            A log giving the outer radius/diameter.
        """
        return Log(self._dispatch.OuterInnerRadiusDiameter(log, prompt_user, config))

    def cased_hole_normalization(self, log=None, prompt_user=None, config=None):
        """Subtracts the trace average, median, min, max or a custom value from all data points
        of the same trace.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns ''None''.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [Path to a configuration file or a parameter string. The
            configuration file can contain the following options:
            .. code-block:: ini

                [CasedHoleNormalization]
                ; Method : Mean, Median, Min, Max, Other
                ; The Value parameter is used when the Method has been set to Other
                ; Value : log name or constant numerical value
                Method = Mean
                Value = 10.5

        Returns
        -------
        Log
            The resulting log.
        """
        return Log(self._dispatch.CasedHoleNormalization(log, prompt_user, config))

    def reverse_amplitude(self, log=None):
        """Inverts the amplitudes in a FWS log.
        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, a dialog box displaying a list of available logs will be displayed.
        """

        self._dispatch.ReverseAmplitude(log)

    def average_filter_fws_log(self, log=None, filter_width=None, filter_type=None):
        """Applies a moving average filter to the traces of an FWS log.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.  If not provided, the process returns None.
        filter_width : float, optional
            Length of the filter window in us.  If not provided, default value will be used.
        filter_type : int, optional
            If not provided, default value will be used.
            Type of the filter :
                * 0 = moving average
                * 1 = weighted average

        Returns
        -------
        Log
            The resulting log.
        """

        return Log(self._dispatch.AverageFilterFWSLog(log, filter_width, filter_type))

    def freq_filter_fws_log(self, log, low_cut, low_pass, high_pass, high_cut):
        """Applies a frequency filter to the traces of an FWS log.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.  If not provided, the process returns None.
        low_cut : float
            The low cut-off frequency of filter in kHz. If not provided, default value will be used.
        low_pass : float
            The low pass frequency of filter in kHz. If not provided, default value will be used.
        high_pass : float
            The high pass frequency of filter in kHz. If not provided, default value will be used.
        high_cut : float
            The high cut-off frequency of filter in kHz. If not provided, default value will be used.

        Returns
        -------
        Log
            Object of the filtered FWS log.
        """

        return Log(self._dispatch.FreqFilterFwsLog(log, low_cut, low_pass, high_pass, high_cut))

    def apply_stand_off_correction(self, log=None, prompt_user=None, config=None):
        """Corrects intercept times for the stand-off of tool and formation.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog settings will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ApplyStandOffCorrection]
                ; LogUnit : s, ms, msec, us, usec, sec
                ; ToolSpacingUnit, ToolDiameterUnit, HoleDiameterUnit : m, mm, inch, cm, ft
                ; FluidVelocityUnit : us/ft, us/m, ft/us, m/s
                ; VelocityUnit : us/ft, us/m, ft/us, m/s
                ; HoleDiameter, FluidVelocity : log name or constant
                LogUnit=us
                ToolSpacing=0.6
                ToolSpacingUnit=m ; m, mm, inch, cm, ft
                ToolDiameter=50
                ToolDiameterUnit=mm
                HoleDiameter=100
                HoleDiameterUnit=mm
                FluidVelocity=1500
                FluidVelocityUnit=m/s
                VelocityUnit=m/s

        Returns
        -------
        Log
            The resulting log.
        """

        return Log(self._dispatch.ApplyStandOffCorrection(log, prompt_user, config))

    def compensated_velocity(self, log=None, prompt_user=None, config=None):
        """Slowness or velocity computed from two receiver arrival times.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log containing the travel times to the first receiver.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [FwsCompensatedVelocity]
                ; RX1Log, RX2Log : log name
                ; RX1LogUnit, RX2LogUnit : s, ms, msec, us, usec, sec
                ; SpacingUnit : m, mm, inch, ft, cm
                ; VelocityUnit : us/ft, us/m, ft/us, m/s
                RX1Log =RX1 - dt
                RX2Log = RX2 - dt
                RX1LogUnit = us
                RX2LogUnit = us
                Spacing = 0.2
                SpacingUnit = m
                VelocityUnit =us/m

        Returns
        -------
        Log
            The resulting log.
        """

        return Log(self._dispatch.CompensatedVelocity(log, prompt_user, config))

    def apply_semblance_processing(self, prompt_user=None, config=None):
        """Performs a velocity analysis for the multiple receivers.

        Parameters
        ----------
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file.
            The configuration file can contain the following options:

            .. code-block:: ini

                [ApplySemblanceProcessing]
                Rx1_Log = RX1
                Rx1_Offset = 0.0
                Rx1_TxDistance = 0.6
                Rx1_Unit = m
                Rx2_Log = RX2
                Rx2_Offset = 0.0
                Rx2_TxDistance = 0.8
                Rx2_Unit = m
                Rx3_Log= ...

                [FwsVelocityAnalysis]
                EnableFilter=false
                FreqFilterLowPass=2.5 ; in kHz
                FreqFilterLowPass=5.0
                FreqFilterHighPass=30.0
                FreqFilterHighCut=35.0
                ToolDiameter=50.0
                ToolDiameterUnit=mm ;mm, cm, inch
                BoreholeDiameter=100.0
                BoreholeDiameterUnit=mm ;mm, cm, inch
                FluidSlowness=666.67
                FluidSlownessUnit=us/m ; us/ft, us/m, ft/us, m/s, us/m

        Returns
        -------
        Log
            The log containing the semblance results.
        """

        return Log(self._dispatch.ApplySemblanceProcessing(prompt_user, config))

    def process_reflected_tube_wave(self, log=None, prompt_user=None, config=None):
        """Extracts the cumulative energy from reflected tube wave arrivals.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog settings will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ProcessReflectedTubeWave]
                ; Side : both,  upper, lower
                Side = both
                Offset = 25.0 'measured in us
                Blanking = 50.0 'measured in us
                FluidSlowness = 696.0 'measured in us/m
                TxFrequency = 15000.0 'measured in Hz

        Returns
        -------
        Log
            The resulting log containing the cumulative energy.
        """

        return Log(self._dispatch.ProcessReflectedTubeWave(log, prompt_user, config))

    def pick_first_arrival(self, log=None, prompt_user=None, config=None):
        """Picks the first arrival time using the standard threshold or advanced method.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.  If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file.
            The configuration file can contain the following options:

            .. code-block:: ini

                [FwsFirstArrival]
                ;Method=Standard Threshold Pickup Algorithm
                Method=Advanced Threshold Pickup Algorithm

                [Standard Threshold Pickup Algorithm]
                Blanking=100.0
                Threshold=15.0
                BackInterpolation=yes
                LockToSampling=yes
                ; the next two are advanced settings
                BaseLine=0.0
                AutoAdjustThreshold=no

                [Advanced Threshold Pickup Algorithm]
                Blanking=0.0
                Threshold=3.0
                LargeWidth=120.0
                SmallWidth=40.0

        Returns
        -------
        Log
            The resulting log containing the first arrival times.
        """

        return Log(self._dispatch.PickFirstArrival(log, prompt_user, config))

    def cement_bond(self, log=None, prompt_user=None, config=None):
        """Determines the cement bond based on the Standard Gate Method.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [CementBondProcess]
                ; Logs : comma-separated FWS log names of the receivers to be processed
                Logs=WVFS1,WVFS2,WVFS3
                AreRadiiSectors=no
                EnableT0Gate=yes
                EnableTXGate=no
                T0GateStart=237.4
                T0GateLength=40
                TXGateBlanking=0
                TXGateThreshold=15
                EnableCalibration=no
                BLGateStart=50
                BLGateLength=25
                FreePipeTargetAmplitude=100
                FreePipeTargetAmplitudeUnits=mV
                FreePipeTopDepth=0
                FreePipeBotDepth=0
        """

        self._dispatch.CementBond(log, prompt_user, config)

    def pick_e1_arrival(self, fws_log=None, dt_log=None, prompt_user=None, config=None):
        """Determines the arrival time of the E1 amplitude.

        Parameters
        ----------
        fws_log : int or str, optional
            Zero based index or title of the FWS log to process.
            If not provided, the process dialog box will be displayed.
        dt_log : int or str, optional
            Zero based index or title of the arrival time log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [PickE1Arrival]
                PickPositivPolarity = yes
                FilterWidth = 5

        Returns
        -------
        Log
            The resulting log containing the E1 arrival times.
        """

        return Log(self._dispatch.PickE1Arrival(fws_log, dt_log, prompt_user, config))

    def extract_e1_amplitude(self, fws_log=None, arrival_log=None, prompt_user=None):
        """Uses the E1 arrival time to extract the E1 amplitude.

        Parameters
        ----------
        fws_log : int or str, optional
            Zero based index or title of the log to process.
        arrival_log : int, str or float, optional
            int, str : Zero based index or title of the log containing the first E1 arrival times.
            float : constant E1 arrival time
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.

        Returns
        -------
        Log
            The resulting log containing the E1 amplitude.
        """

        return Log(self._dispatch.ExtractE1Amplitude(fws_log, arrival_log, prompt_user))

    def adjust_pick_to_extremum(self, fws_log=None, arrival_log=None, prompt_user=None, config=None):
        """Adjusts the pick given in arrival_log to the next maximum or minimum amplitude in fws_log.

        Parameters
        ----------
        fws_log : int or str, optional
            Zero based index or title of the fws log.
            If not provided, the process dialog box will be displayed.
        arrival_log : int or str, optional
            Zero based index or title of the arrival time log.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [AdjustPickToExtremum]
                PickPositivPolarity = yes
                FilterWidth = 5

        Returns
        -------
        Log
            Object of the log containing the pick times shifted to the nearest amplitude extremum.
        """

        return Log(self._dispatch.AdjustPickToExtremum(fws_log,arrival_log, prompt_user, config))

    def extract_window_peak_amplitude(self, log=None, prompt_user=None, config=None):
        """Extracts the maximum amplitude found in a time window of a FWS log trace.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [ExtractWindowPeakAmplitude]
                ; WindowStart : value or log name, units : us
                ; WindowLength : value, units : us
                ; PickType : 0 = peak, 1 = max, 2 = average
                WindowStart=0
                WindowLength=15
                PickMax=yes
                PickPos=yes
                PickType=1
                EnableResampling=yes

        Returns
        -------
        Log
            The resulting log containing the amplitude.
        """

        return Log(self._dispatch.ExtractWindowPeakAmplitude(log, prompt_user, config))

    def calculate_mechanical_properties(self, p_slowness=None, s_slowness=None, density=None):
        """Computes a set of rock mechanical parameters from the input data.

        Parameters
        ----------
        p_slowness : int or str, optional
            Zero based index or title of the log containing the p-slowness data.
            If not provided, the process dialog box will be displayed.
        s_slowness : int or str, optional
            Zero based index or title of the log containing the s-slowness data.
            If not provided, the process dialog box will be displayed.
        density :int or str, optional
            Zero based index or title of the log containing the density data.
        """

        self._dispatch.CalculateMechanicalProperties(p_slowness, s_slowness, density)

    def integrated_travel_time(self, log=None, prompt_user=None, config=None):
        """Computes the integrated travel time from slowness or velocity data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [IntegratedTravelTime]
                TimeOffset = 0 'in us
                TWT = Yes/No

        Returns
        -------
        Log
            The resulting log containing the integrated times.
        """

        return Log(self._dispatch.IntegratedTravelTime(log, prompt_user, config))

    def bond_index(self, log=None, prompt_user=None, config=None):
        """Computes the bond index of the cement behind the casing.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [FwsBondIndex]
                CementAmplitude = 2 'in mV
                FreePipeAmplitude = 62.2 'in mV

        Returns
        -------
        Log
            The resulting log containing the bond index.
        """

        return Log(self._dispatch.BondIndex(log, prompt_user, config))

    def compressive_strength(self, log=None, prompt_user=None, config=None):
        """Computes the compressive strength of the cement behind a casing.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.  A cement bond amplitude log (Well or Mud log type)
            or amplitude map (Image log) can be used.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [FwsCompressiveStrength]
                CasingOD = 7 ' in inch
                CasingWeight = 23 ' in lbs/ft

        Returns
        -------
        Log
            The resulting log containing the compressive strength.
        """

        return Log(self._dispatch.CompressiveStrength(log, prompt_user, config))



    def apply_natural_gamma_borehole_correction(self, log=None, prompt_user=None, config=None):
        """Applies borehole corrections to FWS and Well logs

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [BoreholeConditionCorrections]
                DeadTime = 7.2 ' in us
                EnableDeadTime = yes
                EnableFactors = yes
                FactorName1 = Water Factor
                FactorName2 = Pipe Factor
                Top1 = 0.0
                Bot1 = 2.85
                Factor1-1 = 1
                Factor1-2 = 1.49
                Top2 = 2.85
                Bot2 = bot
                Factor2-1 = 1.12
                Factor2-2 = 1

        Returns
        -------
        Log
            A log containing the corrected count rates.
        """

        return Log(self._dispatch.ApplyNaturalGammaBoreholeCorrection(log, prompt_user, config))

    def apply_total_gamma_calibration(self, log=None, prompt_user=None, config=None):
        """Applies a calibration factor or equation to the values in the specified Well Log

       Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [BoreholeConditionCorrections]
                K-Factor=2*0.00001028

        Returns
        -------
        Log
            A log containing the modified gamma values.
        """

        return Log(self._dispatch.ApplyTotalGammaCalibration(log, prompt_user, config))

    def calculate_spectrum_total_count(self, log=None, prompt_user=None, config=None):
        """Extracts the total count, min, max, average or median from each spectrum trace of the specified log

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [SpectralGamma_Statistic]
                ; WinLow, WinHigh expressed in channel number or keV according to Channel
                Total = yes
                Min = yes
                Max = yes
                Ave = yes
                Median = yes
                UseWindow = yes
                Channel = yes
                WinLow = 410
                WinHigh = 2850
        """

        self._dispatch.CalculateSpectrumTotalCount(log, prompt_user, config)

    def spectrometric_ratios(self, log_a=None, log_b=None, log_c=None, prompt_user=None, config=None):
        """Computes spectrometric ratios like U/Th or U/k
        
        By default, the ratios log_b/log_a, log_b/log_c and log_c/log_a
        will be computed.

        Parameters
        ----------
        log_a : int or str, optional
            Zero based index or title of the log to process.
        log_b : int or str, optional
            Zero based index or title of the log to process.
        log_c : int or str, optional
            Zero based index or title of the log to process.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [SpectrometricRatios]
                ; ratio : A / B
                A=K
                B=U
        """

        self._dispatch.SpectrometricRatios(log_a, log_b, log_c, prompt_user, config)

    def process_medusa_spectrum_data(self, log_spectrum=None, log_time=None, prompt_user=None, config=None):
        """Performs a full spectrum analysis using a calibration after Medusa

        Parameters
        ----------
        log_spectrum : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        log_time : int or str, optional
            Zero based index or title of the log with the live time data.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [SpectralGammaMedusaProcess]
                CalibrationFilePath = C:\\Temp\\NSG1234.mcf
                EnableFittedSpectrum = yes
                EnableConcentrationErrors = yes
                EnableStabilizationFactor = yes
                DeadTime = 5 (in us/pulse)
                HoleDiameter = 96 / Caliper (fixed value or data from log in mm)
                CasingThickness = 8 / Thickness (fixed value or data from log mm)
                CasingType = 0 (Steel) / 1 (PVC)
                FluidDensity = 1.1 / RHOFL (fixed value or data from log in g/ccm)
                FluidK = 0.0 / K (Potassium concentration in the fluid; fixed value or data from log in Bq/kg)
                FluidU = 0.0 / U (eq Uranium concentration in the fluid; fixed value or data from log in Bq/kg)
                FluidTh = 0.0 / Th (Thorium concentration in the fluid; fixed value or data from log in Bq/kg)
                ToolPosition = 0 (Alongside) / 1 (Centered)
                """

        self._dispatch.ProcessMedusaSpectrumData(log_spectrum, log_time, prompt_user, config)

    def process_spectrum_data(self, log=None, prompt_user=None, config=None):
        """Performs a windows stripping based on a calibration model

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [SpectralGamma]
                OutputWindowCounts = yes / no
                ProcessModel = "C:\Temp\Test.sgm"
        """

        self._dispatch.ProcessSpectrumData(log, prompt_user, config)

    def compute_gr(self, log_k=None, log_u=None, log_th=None, prompt_user=None, config=None):
        """Computes total gamma ray from K, U and Th isotope concentrations using the MEDUSA
        calibration file

        Parameters
        ----------
        log_k : int or str, optional
            Zero based index or title of the log containing the concentrations of K.
        log_u : int or str, optional
            Zero based index or title of the log containing the concentrations of U.
        log_th : int or str, optional
            Zero based index or title of the log containing the concentrations of Th.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [SpectralGammaMedusaCGR]
                CalibrationFilePath=C:\Tools\Calibrations\QL40-SGR-154904.mcf

        Returns
        -------
        Log
            A log containing the gamma ray values.
        """

        return Log(self._dispatch.ComputeGR(log_k, log_u, log_th, prompt_user, config))


    def process_nmrsa_data(self, log=None, prompt_user=None, config=None):
        """Performs a post-processing of NMRSA's BMR tool raw data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path and name of the configuration file or a parameter string.  The configuration file or
            string can contain the following options:

            .. code-block:: ini

                [NMRSA]
                UseDefaultOutputs = yes / no
                MasterCalibrationFile=
                ProcessingConfigurationFile=
                DepthRange=Maximum / UserDefined / Zones /LogZones
                TopDepth=20
                BottomDepth=22
                LogZones : top1, bot1, top2, bot2, ... topN, botN
                LogZonesDepthRange=logname, depthsectionName1, depthsectionName2, ....depthsectionname3
        """

        self._dispatch.ProcessNMRSAData(log, prompt_user, config)

    def nmr_total_porosity(self, log=None, prompt_user=None, config=None):
        """Computes the total porosity from a T2 distribution.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path and name of the configuration file or a parameter string.  The configuration file
            or string can contain the following options:

            .. code-block:: ini

                [NMRTotalPorosity]
                MaxCutoffValue=-1
                UseTimeMaxCutoff= yes / no

                DepthRange=Maximum / UserDefined / Zones /LogZones
                TopDepth=20
                BottomDepth=22
                LogZones : top1, bot1, top2, bot2, ... topN, botN
                LogZonesDepthRange=logname, depthsectionName1, depthsectionName2, ....depthsectionname3

        Returns
        -------
        Log
            The resulting log object
        """

        return Log(self._dispatch.NMRTotalPorosity(log, prompt_user, config))

    def nmr_permeability(self, log=None, prompt_user=None, config=None):
        """Computes the permeability from a T2 distribution.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path and name of the configuration file or a parameter string.  The configuration file
            or string can contain the following options:

            .. code-block:: ini

            [NMRPermeability]
            T2DistributionTraceUnit= seconds / milliseconds
            UseTimeMaxCutoff= yes / no
            MaxCutoffValue=-1
            DisplayTIMModel= yes / no
            VariableCforTIMModel=1
            ExponentMforTIMModel=4
            BFVCutoffForTIMModel=2
            BFVCutoffForTIMModel=0.3
            UseTimeMaxForFFVCutoff= yes / no
            FFVCutoffForTIMModel=0
            DisplaySDRModel= yes / no
            VariableCforSDRModel=4
            ExponentMforSDRModel=4
            ExponentNforSDRModel=2
            DisplayT2LogMean= yes / no
            DepthRange=Maximum / UserDefined / Zones /LogZones
            TopDepth=20
            BottomDepth=22
            LogZones : top1, bot1, top2, bot2, ... topN, botN
            LogZonesDepthRange=logname, depthsectionName1, depthsectionName2, ....depthsectionname3
        """

        self._dispatch.NMRPermeability(log, prompt_user, config)

    def nmr_fluid_volumes(self, log=None, prompt_user=None, config=None):
        """Computes the fluid volumes from a T2 distribution.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log to process.
            If not provided, the process dialog box will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path and name of the configuration file or a parameter string.  The configuration file
            or string can contain the following options:

            .. code-block:: ini

            [NMRFluidVolumes]
            LithoDatabase=
            UseLithoDatabaseAssociatedColor= yes/no
            Components=
            Cutoff=
            DepthRange=Maximum / UserDefined / Zones /LogZones
            TopDepth=20
            BottomDepth=22
            LogZones : top1, bot1, top2, bot2, ... topN, botN
            LogZonesDepthRange=logname, depthsectionName1, depthsectionName2, ....depthsectionname3

        Returns
        -------
        Log
            The resulting log object
        """

        return Log(self._dispatch.NMRFluidVolumes(log, prompt_user, config))


    def water_salinity(self, log=None, prompt_user=None, config=None):
        """Salinity estimation from fluid conductivity.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the fluid conductivity log to process.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : str, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [WaterSalinity]
                Temperature = log name or constant value
                TemperatureUnit = degC / degF / degK

        Returns
        -------
        Log
            A log of the resulting salinity.
        """

        return Log(self._dispatch.WaterSalinity(log, prompt_user, config))

    def water_resistivity(self, log=None, prompt_user=None, config=None):
        """Temperature correction for fluid conductivity or resistivity.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log containing the conductivity or resistivity values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

             .. code-block:: ini

                [WaterResistivity]
                Temperature = log name or constant value
                TemperatureUnit = degC / degF / degK
                RefTemperature = log name or constant value
                RefTemperatureUnit = degC / degF / degK
                Method = 0 (Arp) / 1 (Hilchie)

        Returns
        -------
        Log
            A log of the corrected conductivity or resistivity.
        """

        return Log(self._dispatch.WaterResistivity(log, prompt_user, config))

    def shale_volume(self, log=None, prompt_user=None, config=None):
        """Estimates the shale volume from Gamma Ray or SP data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the Gamma Ray or SP values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

             .. code-block:: ini

                [ShaleVolume]
                Equation = 0
                ; 0 = Linear (default), 1 = Larionov (Tertiary), 2 = Steiber, 3 = Clavier, 4 = Larionov (older rocks)
                Shale=150
                ShaleValueType=1
                ; ...Type: 0 = value, 1 = minmax, 2 = avginterval
                ShaleTopDepth=0
                ShaleBotDepth=0
                Sandstone=75
                SandstoneValueType=1
                ; ...Type: 0 = value, 1 = minmax, 2 = avginterval
                SandstoneTopDepth=0
                SandstoneBotDepth=0

        Returns
        -------
        Log
            A log of the resulting shale volume.
        """

        return Log(self._dispatch.ShaleVolume(log, prompt_user, config))

    def porosity_sonic(self, log=None, prompt_user=None, config=None):
        """Computes porosity from transit time data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the formation resistivity (Rt) values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [PorositySonic]
                ; Method : 0 = Wylie, 1 = WylieCompaction, 2 = AbbreviatedRaymerHunt, 3 = RaymerHunt
                ; Slowness units: us/ft, us/m, ft/us, m/s
                Method = 1
                MatrixSlowness = log name or constant value
                MatrixSlownessUnit = us/ft
                FluidSlowness= = log name or constant value
                FluidSlownessUnit = us/ft
                Compaction= = log name or constant value
                C = 0.67

        Returns
        -------
        Log
            A log of the resulting porosity.
        """

        return Log(self._dispatch.PorositySonic(log, prompt_user, config))

    def porosity_archie(self, log=None, prompt_user=None, config=None):
        """Computes porosity from formation resistivity data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the formation resistivity (Rt) values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [PorosityArchie]
                ; Method : 0 = Standard, 1 = FreshWater, 2 = shale, 3= shaleAndFreshWater
                ; Rw and Rsh units: ohm.m, ohm.ft
                Method = 1
                Vsh = log name or constant value
                Rw = log name or constant value
                RwUnit=ohm.m
                Rsh = 30.0
                RshUnit=ohm.m
                CementationFactor = 1.0
                CementationExponent = 2.0
                Cs = 1.0

        Returns
        -------
        Log
            A log of the resulting porosity.
        """

        return Log(self._dispatch.PorosityArchie(log, prompt_user, config))

    def porosity_density(self, log=None, prompt_user=None, config=None):
        """Computes porosity from density data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the  density values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [PorosityDensity]
                ; Method : 0 = Standard, 1 = Shale
                ; MatrixDensity, FluidDensity, ShaleVolume : value or log
                ; Density units: g/cc or kg/m3
                MatrixDensity=2.7
                MatrixDensityUnit=g/cc
                FluidDensity=1.0
                FluidDensityUnit=g/cc
                ShaleVolume=0
                ShaleDensity=1.5
                ShaleDensityUnit=g/cc

        Returns
        -------
        Log
            A log of the resulting porosity.
        """

        return Log(self._dispatch.PorosityDensity(log, prompt_user, config))

    def porosity_neutron(self, log=None, prompt_user=None, config=None):
        """Applies a shale correction to neutron porosity data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the neutron porosity values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [PorosityNeutron]
                ; Vsh : log name
                ; ShaleNPhi = value
                Vsh=VSh
                ShaleNPhi=50

        Returns
        -------
        Log
            A log of the resulting corrected porosity.
        """

        return Log(self._dispatch.PorosityNeutron(log, prompt_user, config))

    def permeability(self, log=None, prompt_user=None, config=None):
        """Estimates permeability from porosity data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the neutron porosity values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [Permeability]
                CementationFactor=1.0

        Returns
        -------
        Log
            A log of the resulting permeability.
        """

        return Log(self._dispatch.Permeability(log, prompt_user, config))

    def hydraulic_conductivity(self, log=None, prompt_user=None, config=None):
        """Computes the hydraulic conductivity from permeability data.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the well or mud log containing the permeability values.
            If not provided, the process returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

            .. code-block:: ini

                [HydraulicConductivity]
                ; Density, Viscosity, DensityTemperature, ViscosityTemperature : log name or value
                ; Temperature units : degC, degF, degK
                ; Permeability units : m2, Darcy, mD, sq.ft
                ; Density units : kg/m3, g/m3, g/cc, lb/in3, lb/ft3
                ; Viscosity units : Pa.s, cP, p, dyn.s/cm2
                Density=1000
                DensityUnit= kg/m3
                Viscosity=0.000890439
                ViscosityUnit=Pa.s
                DensityTemperature=25
                DensityTemperatureUnit=degC
                ViscosityTemperature=25
                ViscosityTemperatureUnit=degC

        Returns
        -------
        Log
            A Log object of the resulting hydraulic conductivity.
        """

        return Log(self._dispatch.HydraulicConductivity(log, prompt_user, config))

    # CoreCAD processes

    def extract_grain_size_statistics(self, log=None, prompt_user=None, config=None):
        """Computes statistics from a grain size distribution curve.

        Parameters
        ----------
        log : int or str, optional
            Zero based index or title of the log containing the grain size values.
            If not provided, a dialog box displaying a list of available logs will be displayed.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

             .. code-block:: ini

                [GrainSizeStatistics]
                ; Method : 0 = Logarithmic (original Folk and Ward; default), 1 = Geometric (modified Folk and Ward),\
                2 = Logarithmic method of moments, 3= Geometric method of moments
                Mean = yes
                Median = yes
                Sorting = yes
                Skewness = yes
                Kurtosis = yes
                Histo = yes
        """

        self._dispatch.ExtractGrainSizeStatistics(log, prompt_user, config)

    def grain_size_sorting(self, log_min, log_max, prompt_user=None, config=None):
        """Classifies grain size values based on min and max logs.
        
        Parameters
        ----------
        log_min : int or str, optional
            Zero based index or title of the log containing logged minimum grain size value.
            If not provided, the method returns None.
        log_max : int or str, optional
            Zero based index or title of the log containing logged maximum grain size value.
            If not provided, the method returns None.
        prompt_user : bool, optional
            Whether dialog boxes are displayed to interact with the user.
            If set to ``False`` the processing parameters will be retrieved from the specified
            configuration.  If no configuration has been specified, default values will be used.
            Default is True.
        config : bool, optional
            Path to a configuration file or a parameter string. The
            configuration file can contain the following options:

             .. code-block:: ini

                [GrainSizeSorting]
                ; Method : 0 = Logarithmic (original Folk and Ward; default), 1 = Geometric (modified Folk and Ward),\
                2 = Logarithmic method of moments, 3= Geometric method of moments
                BlockedAverage = yes

        Returns
        -------
        Log
            A log containing the sorted values
        """

        return Log(self._dispatch.GrainSizeSorting(log_min, log_max, prompt_user, config))

    # Protection options

    def enable_protection(self, enable, password):
        """Changes the protection status of a document using a password

        Parameters
        ----------
        enable : bool
            Set to True to protect the borehole document.
        password : str
            The password used to allow this option.
        """

        self._dispatch.EnableProtection(enable, password)

    def allow_insert_log(self, enable, password):
        """Changes the protection status for inserting new logs.

        Parameters
        ----------
        enable : bool
            Set to True to allow adding new logs to the borehole document.
        password : str
            The password used to allow this option.
        """

        self._dispatch.AllowInsertLog(enable, password)

    def allow_save_template(self, enable, password):
        """Changes the protection status for saving layout templates.

        Parameters
        ----------
        enable : bool
            Set to True to allow saving layout templates of the borehole document.
        password : str
            The password used to allow this option.
        """

        self._dispatch.AllowSaveTemplate(enable, password)

    def allow_export_file(self, enable, password):
        """Changes the protection status for exporting data.

        Parameters
        ----------
        enable : bool
            Set to True to allow the export of data from the borehole document.
        password : str
            The password used to allow this option.
        """

        self._dispatch.AllowExportFile(enable, password)

    def allow_modify_annotation(self, enable, password):
        """Changes the protection status to modify annotations.

        Parameters
        ----------
        enable : bool
            Set to True to allow editing existing annotations in the borehole document.
        password : str
            The password used to allow this option.
        """

        self._dispatch.AllowModifyAnnotation(enable, password)

    def allow_insert_annotation(self, enable, password):
        """Changes the protection status for inserting annotations.

        Parameters
        ----------
        enable : bool
            Set to True to allow adding new annotations in the borehole document.
        password : str
            The password used to allow this option.
        """

        self._dispatch.AllowInsertAnnotation(enable, password)

    def allow_modify_headers_content(self, enable, password):
        """Changes the protection status of the header content.

        Parameters
        ----------
        enable : bool
            Set to True to allow edition of the document header data.
        password : str
            The password used to allow this option.
        """

        self._dispatch.AllowModifyHeadersContent(enable, password)
