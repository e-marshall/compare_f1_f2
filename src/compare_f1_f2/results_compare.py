from pathlib import Path 
import os
import xarray as xr
import numpy as np
from collections import defaultdict
from typing import DefaultDict, Tuple, Type

#specific to bamber19 ice sheets for now 

class Facts1Results:
    
    def __init__(self, 
                 module:str, 
                 scenario:str,
                 gen_dir:str,
                 dir_name:str = 'output',
                 ):
        self.module = module 
        self.scenario = scenario
        self.gen_dir = gen_dir
        self.dir_name = dir_name
        self.local_global_options = ['local', 'global']
        self.raw_processed_options = ['raw', 'processed']
        self.region_options = ['AIS', 'EAIS', 'WAIS', 'GIS']
        self._get_experiment_output_dir()
        self._get_results_files()
        self.grouped_files = self._group_result_files(self.results_files)
        self.make_ind_ds_objs()
    def _get_experiment_output_dir(self) -> Path:
        """
        Get the path to the output directory for a given module.
        
        Parameters:
        module (str): Name of the module.
        scenario (str): Scenario name.
        results_dir (str): Base directory. This should be the base directory for f1 (ie. that holds the 'experiments' folder).
        
        Returns:
        """ 
        experiment_name = f"{self.module}.{self.scenario}"
        
        # Output dir for specified module & scenario
        results_path = Path(Path(self.gen_dir) /'experiments'/experiment_name/ self.dir_name).glob('*.nc')
        self.results_dir = results_path

    def _get_results_files(self):

        results_files = [f for f in self.results_dir if f.is_file()]
        self.results_files = results_files 

    @staticmethod
    def _parse_file_info(fname:str) -> Tuple[str,str,str]:
        # Prefix: 'raw' if 'raw' appears before the first underscore, else 'processed'
        stem = fname.split('_')[0]  # get the part before the first underscore
        prefix = 'raw' if 'raw' in stem else 'processed'
        # 'global' or 'local' (region)
        if 'global' in fname.lower():
            region = 'global'
        elif 'local' in fname.lower():
            region = 'local'
        else:
            region = 'unknown'
        # Ice sheet or temperature
        if '_GIS' in fname:
            ice_sheet = 'GIS'
        elif '_AIS' in fname:
            ice_sheet = 'AIS'
        elif '_WAIS' in fname:
            ice_sheet = 'WAIS'
        elif '_EAIS' in fname:
            ice_sheet = 'EAIS'
        elif 'temperature' in fname.lower():
            ice_sheet = 'temperature'
        else:
            ice_sheet = 'unknown'
        return prefix, region, ice_sheet
    
    def _group_result_files(self, results_files: list) -> DefaultDict[str, DefaultDict[str, DefaultDict[str, list]]]:
        grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for f in results_files:
            fname = f.name
            prefix, region, ice_sheet = self._parse_file_info(fname)
            grouped[prefix][region][ice_sheet].append(f)
        return grouped
    
    def read_group_ds(self, region: str,
                      raw_processed:str = 'processed',
                      local_global: str = 'local',
                      ) -> xr.Dataset: 
        
        file = self.grouped_files[raw_processed][local_global][region]
        ds = xr.open_dataset(file[0])
        ds.attrs.update({'source_file': str(file[0])})
        return ds
    
    def make_ind_ds_objs(self):
        """
        For each combination of raw_processed, local_global, and region, check if a file exists.
        If so, call read_group_ds and assign the resulting xr.Dataset as an attribute of self.
        """
        for raw_processed in self.raw_processed_options:
            for local_global in self.local_global_options:
                for region in self.region_options:
                    # Check if this combination exists in grouped_files
                    files = self.grouped_files.get(raw_processed, {}).get(local_global, {}).get(region, [])
                    if files:
                        ds = self.read_group_ds(region=region, raw_processed=raw_processed, local_global=local_global)
                        attr_name = f"ds_{raw_processed}_{local_global}_{region}"
                        setattr(self, attr_name, ds)
                    else:
                        pass

class Facts2Results:
    def __init__(self, 
                 results_dir: str,
                 pipeline_id:str,
                 module:str = 'bamber19',
                 scenario:str = 'ssp585',
                 region_options = ['AIS','EAIS','WAIS','GIS']
                 )-> None:
        self.module = module
        self.scenario = scenario
        self.results_dir = Path(results_dir)
        self.pipeline_id = pipeline_id
        self.region_options = region_options
        self._get_results_files()
        self.grouped_files = self._group_result_files(self.results_files)
        self.make_ind_ds_objs() 
        
    def _get_results_files(self):
        results_files = [f for f in Path(self.results_dir).glob(f'{self.pipeline_id}*.nc') if f.is_file()]
        self.results_files = results_files
    
    def _parse_file_info(self, fname:str) -> Tuple[str,str]:
        #local or global (region)
        if 'global' in fname.lower():
            region = 'global'
        elif 'local' in fname.lower():
            region = 'local'
        else:
            region = 'unknown'
        # Ice sheet or temperature
        if '_GIS' in fname:
            ice_sheet = 'GIS'
        elif '_AIS' in fname:
            ice_sheet = 'AIS'
        elif '_WAIS' in fname:
            ice_sheet = 'WAIS'
        elif '_EAIS' in fname:
            ice_sheet = 'EAIS'
        elif 'temperature' in fname.lower():
            ice_sheet = 'temperature'
        else:
            ice_sheet = 'unknown'
        return region, ice_sheet
    
    def _group_result_files(self, results_files: list) -> DefaultDict[str, DefaultDict[str, list]]:
        grouped = defaultdict(lambda: defaultdict(list))
        for f in results_files:
            fname = f.name
            region, ice_sheet = self._parse_file_info(fname)
            grouped[region][ice_sheet].append(f)
        return grouped
    
    def read_result_ds(self, local_global:str, region:str) -> xr.Dataset:

        file = self.grouped_files[local_global][region]
        
        ds = xr.open_dataset(file[0])
        ds.attrs.update({'source_file': str(file[0])})
        return ds
    
    def make_ind_ds_objs(self):
        
        for local_global in ['local','global']:
            for region in self.region_options:
                
                files = self.grouped_files.get(local_global, []).get(region, [])
                if files:
                    ds = self.read_result_ds(local_global = local_global, 
                                             region=region)
                    attr_name = f"ds_{local_global}_{region}"
                    setattr(self, attr_name, ds)
                else:
                    pass


def check_ice_sheet_projections(facts1_obj: Facts1Results, 
                                facts2_obj: Facts2Results, 
                                local_global: str,
                                icesheet: str) -> None:
        if local_global == 'global':
            if icesheet == 'AIS':
                facts1_global = facts1_obj.ds_processed_global_AIS['sea_level_change'].data
                facts2_global = facts2_obj.ds_global_AIS['sea_level_change'].data
            elif icesheet == 'GIS':
                facts1_global = facts1_obj.ds_processed_global_GIS['sea_level_change'].data
                facts2_global = facts2_obj.ds_global_GIS['sea_level_change'].data
            elif icesheet == 'WAIS':
                facts1_global = facts1_obj.ds_processed_global_WAIS['sea_level_change'].data
                facts2_global = facts2_obj.ds_global_WAIS['sea_level_change'].data
            elif icesheet == 'EAIS':
                facts1_global = facts1_obj.ds_processed_global_EAIS['sea_level_change'].data
                facts2_global = facts2_obj.ds_global_EAIS['sea_level_change'].data
            else:
                raise ValueError(f'Ice sheet {icesheet} not recognized. Must be one of AIS, GIS, WAIS, EAIS.')
            
            assert np.array_equal(facts1_global, facts2_global), f'The global {icesheet} sea level projections for FACTS v.1 and FACTS v.2 do not match!'
            print(f'The global {icesheet} sea level projections for FACTS v.1 and FACTS v.2 match!')
        elif local_global == 'local':

            if icesheet == 'AIS':
                facts1_local = facts1_obj.ds_processed_local_AIS['sea_level_change'].data
                facts2_local = facts2_obj.ds_local_AIS['sea_level_change'].data
            elif icesheet == 'GIS':
                facts1_local = facts1_obj.ds_processed_local_GIS['sea_level_change'].data
                facts2_local = facts2_obj.ds_local_GIS['sea_level_change'].data
            elif icesheet == 'WAIS':
                facts1_local = facts1_obj.ds_processed_local_WAIS['sea_level_change'].data
                facts2_local = facts2_obj.ds_local_WAIS['sea_level_change'].data
            elif icesheet == 'EAIS':
                facts1_local = facts1_obj.ds_processed_local_EAIS['sea_level_change'].data
                facts2_local = facts2_obj.ds_local_EAIS['sea_level_change'].data
            else:
                raise ValueError(f'Ice sheet {icesheet} not recognized. Must be one of AIS, GIS, WAIS, EAIS.')
            
            assert np.array_equal(facts1_local, facts2_local), f'The local {icesheet} sea level projections for FACTS v.1 and FACTS v.2 do not match!'
            print(f'The local {icesheet} sea level projections for FACTS v.1 and FACTS v.2 match!')