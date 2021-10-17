# GSR_MIDAS

This script will download all data sets from [this repository](https://data.nist.gov/od/id/mds2-2476) and will upload them to Cordra.

## Requirements
* [zeppelingsr](https://github.com/camilovelezr/zeppelingsr)

## Usage
Run `python3 -i gsr_midas.py` and then run `z_all(max)`. If `max` is specified, it equals the first n particles to be uploaded from each data set. If `max` is not specified (running `z_all()`) it will upload all particles from all data sets.

Each time particles from a new data set get uploaded to Cordra, `uuid.json` will reflect the name of the sample along with the 4 digit string that identifies it.

`delcordra.py` and `delcordra.jl` delete all objects with the entry `/CamiloExplore:1` from Cordra. `delcordra.jl` is about TEN times faster.

## Warnings
Make sure `zeppelingsr` is at least v1.0.0
