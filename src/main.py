# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 22:52:11 2014

@author: Andreea
"""
import profile
import os   # for speaking
from input_main import *


def main():
    implemented_exper_list = \
        ["SuperCDMS",  # 0
         "LUX2013zero", "LUX2013one", "LUX2013three", "LUX2013five", "LUX2013many",  # 1 - 5
         "SIMPLEModeStage2", "PICASSO", "KIMS2012", "XENON10", "XENON100",  # 6 - 10
         "CDMSlite2013CoGeNTQ", "CDMSSi2012", "CDMSSiGeArtif", "CDMSSiArtif", "CDMSSi2013",  # 11 - 15
         "DAMA2010NaSmRebinned", "DAMA2010ISmRebinned", "DAMA2010NaSmRebinned_TotRateLimit",  # 16 - 18
         "DAMA2010NaSmRebinned DAMA2010ISmRebinned", "DAMA2010ISmRebinned DAMA2010NaSmRebinned",  # 19 - 20
         "SHM_eta0", "SHM_eta1"]  # 21 - 22

    # Give input parameters

    EHI_METHOD = {}
    # EHI_METHOD['ResponseTables'] = T
    # EHI_METHOD['OptimalLikelihood'] = T
    # EHI_METHOD['ImportOptimalLikelihood'] = T
    # EHI_METHOD['ConstrainedOptimalLikelihood'] = T
    # EHI_METHOD['VminLogetaSamplingTable'] = T
    # EHI_METHOD['LogLikelihoodList'] = T
    # EHI_METHOD['ConfidenceBand'] = T
    EHI_METHOD['ConfidenceBandPlot'] = T

    HALO_DEP = F
    plot_dots = F
    RUN_PROGRAM = F
    MAKE_REGIONS = F
    MAKE_PLOT = T

    scattering_types = ['SI']
    input_indices = [1]
    exper_indices = [1, 2, 3, 4, 5, 10, 12, 21, 22]
    OUTPUT_MAIN_DIR = "../Output_Band/"
    filename_tail_list = [""]
    extra_tail = "_mix"

    inp = Input(HALO_DEP, implemented_exper_list, exper_indices=exper_indices,
                input_indices=input_indices, scattering_types=scattering_types,
                RUN_PROGRAM=RUN_PROGRAM, MAKE_REGIONS=MAKE_REGIONS, MAKE_PLOT=MAKE_PLOT,
                EHI_METHOD=EHI_METHOD, OUTPUT_MAIN_DIR=OUTPUT_MAIN_DIR,
                filename_tail_list=filename_tail_list, extra_tail=extra_tail,
                plot_dots=plot_dots)

    # Add additional parameters that will be passed to run_program as member variables
    # of the inp class

    # inp.initial_energy_bin = [3, 6]
    # inp.confidence_levels.extend([confidence_level(s) for s in [3, 5]])
    inp.log_sigma_p = -41

    try:
        plt.close()
        inp.RunProgram()
        if MAKE_PLOT or EHI_METHOD.get('ConfidenceBandPlot', F):
            plt.ylim([-28, -20])
            plt.show()

    finally:
        if inp.RUN_PROGRAM or inp.MAKE_REGIONS:
            os.system("say 'Finished running program'")
            # pass


if __name__ == '__main__':
    main()
    # profile.run("main()")
