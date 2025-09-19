# compare-f1-f2

## Bamber19-icesheets
### Validation

We have so far compared the results of this module (`v.2`) to those of an equivalent `v.1` experiment. In the default configuration, a single `v.1` experiment runs the `bamber19` sea-level component twice, once with scenario 'ssp585' and once with 'rcp85', writing local and global sea level contribution projections for each ice sheet for both scenarios. 

We run two `v.2` bamber19-icesheets instances, one with scenario 'ssp585' and the FAIR climate output of the `v.1` run, and another with scenario 'rcp85' and no climate output. In testing, the `v.2` projections are identical to the `v.1` projections for both scenarios. 

Exact args for runs in this comparison:
#### `v.1` 
One run calls two scenarios
```shell
docker run -it --volume=$HOME/Desktop/facts_work/facts_v1:/opt/facts --volume=$HOME/Desktop/facts_work/facts_v1/tmp/radical.pilot.sandbox:/home/jovyan/radical.pilot.sandbox -w /opt/facts facts 
(factsVe) jovyan@6a02031ad96e:/opt/facts$ python3 facts/runFACTS.py facts/experiments/bamber19.ssp585/
```

#### `v.2`
Each run calls one scenario
##### scenario `ssp585`
```shell
uv run bamber19-icesheets --pipeline-id bamber19_ssp585_validation --climate-data-file $HOME/Desktop/facts_work/facts_v1/facts/experiments/bamber19.ssp585/output/bamber19.ssp585.temperature.fair.temperature_climate.nc --scenario 'ssp585' --pyear-start 2020 --pyear-end 2150 --nsamps 500
```
##### scenario `rcp85`
```shell
uv run bamber19-icesheets --pipeline-id bamber19_dummy_run_rcp85 --pyear-start 2020 --pyear-step 10  --pyear-end 2150 --nsamps 500 --baseyear 2000 --scenario 'rcp85'
```