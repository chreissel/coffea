import sys
import os
import os.path as osp

import pytest

from coffea import hist, processor

if sys.platform.startswith("win"):
    pytest.skip("skipping tests that only function in linux", allow_module_level=True)


def template_analysis(executor, flatten):
    from coffea.processor import run_uproot_job
    
    filelist = {
        'ZJets': [osp.abspath('tests/samples/nano_dy.root')],
        'Data': [osp.abspath('tests/samples/nano_dimuon.root')]
    }
    treename='Events'

    from coffea.processor.test_items import NanoTestProcessor

    exe_args = {'workers': 1,
                'pre_workers': 1,
                'function_args': {'flatten': flatten}}

    hists = run_uproot_job(filelist, treename, NanoTestProcessor(), executor,
                           executor_args = exe_args)

    assert( hists['cutflow']['ZJets_pt'] == 4 )
    assert( hists['cutflow']['ZJets_mass'] == 1 )
    assert( hists['cutflow']['Data_pt'] == 15 )
    assert( hists['cutflow']['Data_mass'] == 5 )


def test_iterative_executor():
    from coffea.processor import iterative_executor
    template_analysis(iterative_executor, True)
    template_analysis(iterative_executor, False)


def test_futures_executor():
    from coffea.processor import futures_executor
    template_analysis(futures_executor, True)
    template_analysis(futures_executor, False)

