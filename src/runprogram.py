# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 15:32:34 2014

@author: Andreea
"""

from experiment_HaloIndep_Band import *
from collections import defaultdict
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, ScalarFormatter, FuncFormatter
linestyles = ['-', '--', '-.', ':']


class PlotData:
    ''' Class to plot the data.
    Input:
        exper_name: string
            Name of experiment.
        HALO_DEP: bool
            Whether the analysis is halo-dependent or halo-independent.
        plot_close: bool, optional
            Whether the plot should be cleared and started from scratch, or new limits
            should be added to a previous plot.
    '''
    count = defaultdict(lambda: -1)

    def __init__(self, exper_name, HALO_DEP, plot_close=True):
        self.exper_name = exper_name
        self.HALO_DEP = HALO_DEP

        if plot_close:
            plt.close()

        # set aspect ratio
        plt.rcParams["figure.figsize"][1] = plt.rcParams["figure.figsize"][0]

        self.set_axes_labels()
        self.set_ticks()

    def set_axes_labels(self):
        ''' Set axis labels, depending on whether it is for halo-dependent or not.
        '''
        if self.HALO_DEP:
            plt.xlabel('$m$ [GeV]')
            plt.ylabel(r'$\sigma_p$ [cm$^2$]')
            plt.axes().set_xscale('log')
            plt.axes().xaxis.set_major_formatter(ScalarFormatter())
        else:
            plt.minorticks_on()
            plt.xlabel('$v_{min}$ [km/s]')
            plt.ylabel(r'$\eta$ $\rho$ $\sigma_p / m$ $[$days$^{-1}]$')

    def set_ticks(self):
        # set major ticks on yaxis
        def major_formatter(x, pos):
            return "$10^{{{0}}}$".format(int(x))

        plt.axes().yaxis.set_major_formatter(FuncFormatter(major_formatter))

        # set minor ticks on yaxis
        minor_ticks = [np.log10(i) for i in range(2, 10)]
        minor_ticks = [i + j for i in minor_ticks for j in range(-100, 0)]
        plt.axes().yaxis.set_minor_locator(FixedLocator(minor_ticks))

    def plot_limits(self, upper_limit, kind, linewidth, linestyle, plot_dots):
        ''' Make a list of the x and y coordinates of the plots, and plot them.
        '''
        if upper_limit.size == 0:   # nothing to plot
            print("upper_limit is empty!")
            return None, None
        elif upper_limit.ndim == 1:  # only one point, so no interpolation
            if self.HALO_DEP:
                x = [10**upper_limit[0]]
            else:
                x = [upper_limit[0]]
            y = [upper_limit[1]]
            plt.plot(x, y, "o")
            return x, y
        else:   # more than one point, so decide on the interpolation order and plot
            if self.HALO_DEP:
                x = 10**upper_limit[:, 0]
            else:
                x = upper_limit[:, 0]
            y = upper_limit[:, 1]
            num_points = x.size
            if num_points == 2 or kind == "linear":
                interp_kind = "linear"
            elif num_points == 3 or kind == "quadratic":
                interp_kind = "quadratic"
            else:
                interp_kind = "cubic"
            interp = interp1d(x, y, kind=interp_kind)
            x1 = np.linspace(x[0], x[-1], 1000)
            if plot_dots:
                plt.plot(x, y, "o")
            plt.plot(x1, interp(x1), linestyle=linestyle,
                     linewidth=linewidth, color=Color[self.exper_name.split()[0]])
            return x1, interp(x1)

    def __call__(self, upper_limit, lower_limit=None, kind=None, linewidth=3,
                 fill=True, alpha=0.4, plot_dots=True, plot_show=True):
        ''' Make plots for the upper limits.
        Input:
            upper_limit: list of lists
                List of x and y coordinates for points representing the upper limit.
            lower_limit: list of lists, optional
                List of x and y coordinates for points representing the lower limit.
            kind: string, optional
                The interpolation kind: 'linear', 'quadratic' or 'cubic'.
            linewidth: float, optional
                Width of the plotted line.
            fill: bool, optional
                If there is a lower_limit, fill between the upper and lower limit.
            plot_dots: bool, optional
                Whether the plot should show the data points or just the interpolation.
            plot_show: bool, optional
                Whether the plot should be shown or not.
        '''
        PlotData.count[self.exper_name] += 1
        linestyle = linestyles[PlotData.count[self.exper_name] % len(linestyles)]

        if lower_limit is not None and fill:
            linewidth = 1

        x_upper, y_upper = self.plot_limits(upper_limit, kind, linewidth, linestyle,
                                            plot_dots)
        if lower_limit is not None:
            x_lower, y_lower = self.plot_limits(lower_limit, kind, linewidth, linestyle,
                                                plot_dots)
            if fill:
                plt.fill_between(x_lower, y_lower, y_upper,
                                 color=Color[self.exper_name.split()[0]], alpha=alpha)

        # if plot_show:
            # plt.show()


class RunProgram:
    ''' Class implementing the main run of the program.
    '''
    def init_experiment(self, exper_name, scattering_type, mPhi, delta, HALO_DEP,
                        EHI_METHOD, quenching):
        '''Select which experiment class we must use, depending on what statistical
        analysis we need, and initialize the experiment.
        '''
        print('name = ', exper_name)
        if HALO_DEP:
            print('Halo Dependent')
            if exper_name in MaximumGapLimit_exper:
                class_name = MaxGapExperiment
            elif exper_name in GaussianLimit_exper:
                class_name = GaussianExperiment
            elif exper_name in Poisson_exper:
                class_name = PoissonExperiment
            elif exper_name in BinnedSignal_exper:
                class_name = DAMAExperiment
            elif exper_name.split()[0] in BinnedSignal_exper:
                class_name = DAMAExperimentCombined
            elif exper_name in DAMALimit_exper:
                class_name = DAMATotalRateExperiment
            else:
                print("NotImplementedError: This experiment was not implemented!")
                return
        else:
            print('Halo Independent')
            if exper_name in EHImethod_exper and np.any(EHI_METHOD):
                print('EHI Method')
                class_name = Experiment_EHI
            elif exper_name in MaximumGapLimit_exper:
                class_name = MaxGapExperiment_HaloIndep
            elif exper_name in Poisson_exper:
                class_name = PoissonExperiment_HaloIndep
            elif exper_name in GaussianLimit_exper:
                class_name = GaussianExperiment_HaloIndep
            elif exper_name in BinnedSignal_exper:
                class_name = Crosses_HaloIndep
            elif exper_name.split()[0] in BinnedSignal_exper:
                class_name = Crosses_HaloIndep_Combined
            else:
                print("NotImplementedError: This experiment was not implemented!")
                return
            # if delta > 0 we have to use the integration in recoil energy ER
            if delta > 0:
                class_name.__bases__ = (Experiment_HaloIndep_ER,)

        self.exper = class_name(exper_name, scattering_type, mPhi, quenching)

    def compute_data(self, mx, fp, fn, delta, mx_range, vmin_range, initial_energy_bin,
                     logeta_guess, HALO_DEP, EHI_METHOD, vmin_EHIBand_range,
                     logeta_EHIBand_percent_range, steepness, confidence_levels,
                     vmin_index_list, logeta_index_range, extra_tail):
        '''(Re-)compute the data.
        '''
        output_file = self.output_file_no_extension + "_temp.dat"
        f_handle = open(output_file, 'w')   # clear the file first
        f_handle.close()

        if HALO_DEP:
            (mx_min, mx_max, num_steps) = mx_range
            upper_limit = self.exper.UpperLimit(fp, fn, delta, mx_min, mx_max, num_steps,
                                                output_file)
        else:
            (vmin_min, vmin_max, vmin_step) = vmin_range
            if not np.any(EHI_METHOD):
                upper_limit = \
                    self.exper.UpperLimit(mx, fp, fn, delta, vmin_min, vmin_max,
                                          vmin_step, output_file,
                                          initial_energy_bin=initial_energy_bin)
            else:
                if EHI_METHOD.ResponseTables:
                    self.exper.ResponseTables(vmin_min, vmin_max, vmin_step, mx, fp, fn,
                                              delta, self.output_file_no_extension)
                if EHI_METHOD.OptimalLikelihood:
                    self.exper.OptimalLikelihood(self.output_file_no_extension,
                                                 logeta_guess)
                if EHI_METHOD.ImportOptimalLikelihood:
                    self.exper.ImportResponseTables(self.output_file_no_extension,
                                                    plot=True)
                    self.exper.ImportOptimalLikelihood(self.output_file_no_extension,
                                                       plot=True)
                    self.exper.PlotOptimum()
                if EHI_METHOD.ConstrainedOptimalLikelihood:
                    # Tests for delta = 0:
                    (vminStar, logetaStar) = (500, -25)
                    # Tests for delta = -50:
#                    (vminStar, logetaStar) = (185.572266287, -19.16840262)
                    self.exper.ImportOptimalLikelihood(self.output_file_no_extension)
                    self.exper.ConstrainedOptimalLikelihood(vminStar, logetaStar,
                                                            plot=True)
                if np.any(EHI_METHOD[4:]):
                    if EHI_METHOD._fields[4] != 'VminLogetaSamplingTable':
                        raise AttributeError("EHI_METHOD's attribute is not as expected.")
                    (vmin_Band_min, vmin_Band_max, vmin_Band_numsteps) = \
                        vmin_EHIBand_range
                    (logeta_percent_minus, logeta_percent_plus, logeta_num_steps) = \
                        logeta_EHIBand_percent_range
                    if steepness is not None:
                        (steepness_vmin, steepness_vmin_center, steepness_logeta) = \
                            steepness
                        print("Steepness:", steepness_vmin, ",",
                              steepness_vmin_center, ",", steepness_logeta)
                        self.exper.VminSamplingList(self.output_file_no_extension,
                                                    vmin_Band_min, vmin_Band_max,
                                                    vmin_Band_numsteps,
                                                    steepness_vmin, steepness_vmin_center,
                                                    plot=not np.any(EHI_METHOD[5:]))
                        self.exper.VminLogetaSamplingTable(self.output_file_no_extension,
                                                           logeta_percent_minus,
                                                           logeta_percent_plus,
                                                           logeta_num_steps,
                                                           steepness_logeta,
                                                           plot=not np.any(EHI_METHOD[5:]))
                    else:
                        print("Steepness: Default")
                        self.exper.VminSamplingList(self.output_file_no_extension,
                                                    vmin_Band_min, vmin_Band_max,
                                                    vmin_Band_numsteps,
                                                    plot=not np.any(EHI_METHOD[5:]))
                        self.exper.VminLogetaSamplingTable(self.output_file_no_extension,
                                                           logeta_percent_minus,
                                                           logeta_percent_plus,
                                                           logeta_num_steps,
                                                           plot=not np.any(EHI_METHOD[5:]))
                if EHI_METHOD.LogLikelihoodList:
                    print("vmin_EHIBand_range =", vmin_Band_min, vmin_Band_max,
                          vmin_Band_numsteps)
                    print("logeta_EHIBand_percent_range =", logeta_percent_minus,
                          logeta_percent_plus, logeta_num_steps)
                    self.exper.LogLikelihoodList(self.output_file_no_extension,
                                                 extra_tail=extra_tail,
                                                 vmin_index_list=vmin_index_list,
                                                 logeta_index_range=logeta_index_range)
                if EHI_METHOD.ConfidenceBand:
                    self.exper.ImportOptimalLikelihood(self.output_file_no_extension)
                    interpolation_order = 2
                    delta_logL = [chi_squared1(c) for c in confidence_levels]
                    for d_logL in delta_logL:
                        multiplot = (d_logL == delta_logL[0]) and MAKE_PLOT
                        self.exper.ConfidenceBand(self.output_file_no_extension, d_logL,
                                                  interpolation_order,
                                                  extra_tail=extra_tail,
                                                  multiplot=multiplot)

        if HALO_DEP or not np.any(EHI_METHOD):
            print("upper_limit = ", upper_limit)
            print("diff response calls = ", self.exper.count_diffresponse_calls)
            print("response calls = ", self.exper.count_response_calls)
            output_file = self.output_file_no_extension + ".dat"
            print(output_file)  # write to file
            np.savetxt(output_file, upper_limit)

    def make_regions(self, delta, confidence_levels):
        ''' Make regions for halo-dependent analysis and experiments with potential DM
        signal.
        '''
        output_file = self.output_file_no_extension + ".dat"
        for CL in confidence_levels:
            output_file_regions = self.output_file_no_extension + \
                "_" + str(round(sigma_dev(CL), 2)) + "sigma"
            output_file_lower = output_file_regions + "_lower_limit.dat"
            output_file_upper = output_file_regions + "_upper_limit.dat"
            self.exper.Region(delta, CL, output_file, output_file_lower,
                              output_file_upper)

    def plot_limits(self, exper_name, confidence_levels, HALO_DEP, plot_dots):
        plot_limits = PlotData(exper_name, HALO_DEP, plot_close=False)
        if exper_name.split()[0] in BinnedSignal_exper:
            PlotData.count[exper_name] = -1
            for index, CL in enumerate(confidence_levels):
                output_file_regions = self.output_file_no_extension + \
                    "_" + str(round(sigma_dev(CL), 2)) + "sigma"
                output_file_lower = output_file_regions + "_lower_limit.dat"
                output_file_upper = output_file_regions + "_upper_limit.dat"
                lower_limit = np.loadtxt(output_file_lower)
                upper_limit = np.loadtxt(output_file_upper)
                plot_limits(upper_limit, lower_limit=lower_limit, fill=(index < 2),
                            plot_dots=plot_dots, plot_show=False)
                if index < 2:
                    PlotData.count[exper_name] -= 1
        else:
            output_file = self.output_file_no_extension + ".dat"
            upper_limit = np.loadtxt(output_file)
            # print("upper_limit = ", upper_limit)
            plot_limits(upper_limit, plot_dots=plot_dots, plot_show=False)

    def plot_EHI_band(self, exper_name, confidence_levels, HALO_DEP, extra_tail,
                      plot_dots):
        output_file = self.output_file_no_extension + ".dat"
        self.exper.ImportOptimalLikelihood(self.output_file_no_extension)
        interp_kind = 'linear'
        plot_limits = PlotData(exper_name, HALO_DEP, plot_close=False)

#        self.exper.PlotSamplingTable(self.output_file_no_extension,
#                                plot_close=False, plot_show=False, plot_optimum=False)
        delta_logL = [chi_squared1(c) for c in confidence_levels]
        print("delta_logL =", delta_logL)
        for d_logL in delta_logL:
            PlotData.count[exper_name] = -1
            self.exper.ImportConfidenceBand(self.output_file_no_extension, d_logL,
                                            extra_tail=extra_tail)
            first_vmin_low = self.exper.vmin_logeta_band_low[0, 0]
            first_vmin_up = self.exper.vmin_logeta_band_up[0, 0]
            last_eta_up = self.exper.vmin_logeta_band_up[-1, 1]
            self.exper.vmin_logeta_band_up = \
                np.vstack(([[first_vmin_low, -10], [first_vmin_up - 5, -10]],
                           self.exper.vmin_logeta_band_up,
                           [[1000, last_eta_up]]))
            last_vmin_low = self.exper.vmin_logeta_band_low[-1, 0]
            last_vmin_up = self.exper.vmin_logeta_band_up[-1, 0]
            self.exper.vmin_logeta_band_low = \
                np.vstack((self.exper.vmin_logeta_band_low,
                           [[last_vmin_low + 5, -40], [last_vmin_up, -40]]))
            print(self.exper.vmin_logeta_band_up)
            plot_limits(self.exper.vmin_logeta_band_up,
                        lower_limit=self.exper.vmin_logeta_band_low, kind=interp_kind,
                        fill=True, alpha=0.2, plot_dots=plot_dots, plot_show=False)

        self.exper.PlotOptimum(ylim_percentage=(1.2, 0.8),
                               color=Color[exper_name + '_EHI'],
                               linewidth=3, plot_close=False,  plot_show=False)

    def __call__(self, exper_name, scattering_type, mPhi, fp, fn, delta,
                 confidence_levels,
                 HALO_DEP, RUN_PROGRAM, MAKE_REGIONS, MAKE_PLOT, EHI_METHOD,
                 mx=None, mx_range=None, vmin_range=None, initial_energy_bin=None,
                 vmin_EHIBand_range=None, logeta_EHIBand_percent_range=None,
                 steepness=None, logeta_guess=None,
                 vmin_index_list=None, logeta_index_range=None,
                 OUTPUT_MAIN_DIR="Output/", filename_tail="", extra_tail="",
                 plot_dots=True, quenching=None):
        ''' Main run of the program.
        Input:
            exper_name: string
                Name of experiment.
            scattering_type: string
                Type of scattering. Can be
                - 'SI' (spin-independent)
                - 'SDAV' (spin-independent, axial-vector)
                - 'SDPS' (spin-independent, pseudo-scalar).
            mPhi: float
                Mass of mediator.
            fp and fn: float
                Couplings to proton and neutron.
            delta: float
                DM mass split.
            confidence_levels: list
                List of confidence levels.
            HALO_DEP: bool
                Whether the analysis is halo-dependent or halo-independent.
            RUN_PROGRAM: bool
                Whether the data should be (re-)computed.
            MAKE_REGIONS: bool
                Whether the regions should be (re-)computed in the case of halo-dependent
                analysis and experiments with potential DM signals.
            MAKE_PLOT: bool
                Whether the data should be plotted.
            EHI_Method: ndarray of bools
                Whether each step of the EHI Method is to be performed.
            mx: float, optional
                DM mass, only for halo-independent analysis.
            mx_range: tuple (float, float, int), optional
                (mx_min, mx_max, num_steps) = DM mass range and number or steps,
                only for halo-dependent analysis.
            vmin_range: tuple (float, float, float), optional
                (vmin_min, vmin_max, vmin_step) = vmin range and step size,
                only for halo-independent analysis.
            initial_energy_bin: sequence, optional
                Tuple or list of 2 elements, containing the starting energy bin.
                Only for DAMA combined analysis.
            vmin_EHIBand_range: tuple, optional
                (vmin_Band_min, vmin_Band_max, vmin_Band_numsteps) = vminStar range and
                number of steps, used for calculating the EHI confidence band.
                Only for EHI method.
            logeta_EHIBand_percent_range: tuple, optional
                (logeta_percent_minus, logeta_percent_plus, logeta_num_steps) = logetaStar
                percentage range and number of steps, used for calculating the EHI
                confidence band. The min and max logetaStar are calculated as a given
                percentage above and below the optimum value. Only for EHI method.
            steepness: tuple, optional
                (steepness_vmin, steepness_vmin_center, steepness_logeta) parameters used
                for nonlinear sampling in vminStar and logetaStar. The higher the
                steepnesses the more points are taken close to the steps in the piecewise
                constant best-fit logeta(vmin) function. Only for EHI method.
            logeta_guess: float, optional
                Guessing value of logeta for the best-fit piecewise-constant logeta(vmin)
                function. Only for EHI method.
            vmin_index_list: list, optional
                List of indices in the list of sampling vminStar points for which we
                calculate the optimal likelihood. If not given, the whole list of
                vminStars is used. Only for EHI method.
            logeta_index_range: tuple, optional
                A tuple (index0, index1) between which logetaStar will be considered.
                If not given, then the whole list of logetaStar is used. Only for EHI
                method.
            OUTPUT_MAIN_DIR: string, optional
                Name of main output directory.
            filename_tail: string, optional
                Tag to be added to the file name.
            extra_tail: string, optional
                Additional tail to be added to filenames for the EHI confidence band.
            plot_dots: bool, optional
                Whether the plot should show the data points or just the interpolation.
            quenching: float, optional
                quenching factor, needed for experiments that can have multiple options.
        '''
        # initialize the experiment class
        self.init_experiment(exper_name, scattering_type, mPhi, delta, HALO_DEP,
                             EHI_METHOD, quenching)

        # get the file name specific to the parameters used for this run
        self.output_file_no_extension = \
            Output_file_name(exper_name, scattering_type, mPhi, mx, fp, fn, delta,
                             HALO_DEP, filename_tail, OUTPUT_MAIN_DIR, quenching)

        # (re-)compute the data
        if RUN_PROGRAM:
            self.compute_data(mx, fp, fn, delta, mx_range, vmin_range, initial_energy_bin,
                              logeta_guess, HALO_DEP, EHI_METHOD, vmin_EHIBand_range,
                              logeta_EHIBand_percent_range, steepness, confidence_levels,
                              vmin_index_list, logeta_index_range, extra_tail)

        # make regions
        if MAKE_REGIONS and HALO_DEP and exper_name.split()[0] in BinnedSignal_exper:
            self.make_regions(delta, confidence_levels)

        # make plot
        if MAKE_PLOT and not np.any(EHI_METHOD[:-1]):
            self.plot_limits(exper_name, confidence_levels, HALO_DEP, plot_dots)

        # make band plot
        if EHI_METHOD.ConfidenceBandPlot and exper_name == "CDMSSi2012":
            self.plot_EHI_band(exper_name, confidence_levels, HALO_DEP, extra_tail,
                               plot_dots)
