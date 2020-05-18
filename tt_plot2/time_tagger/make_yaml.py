import yaml
import io

# Define data
PARAMS = {'saveDir': '/fastdata/measurements/fiber_raman',
          'dataChans': [1,2,3,4,5],
          'allChans': [1,2,3,4,5,6,7,8],    # channels to be dumped
          'apdChans': [1,2,3,4],                # photoclicks on APD A and B
	      'corr_apdChans_start': {1:False, 2:False, 3:False, 4:False},
          'corr_apdChans_stop': {1:False, 2:False, 3:False, 4:False},
          'corr_apdChans': [1,4],
          'trigChans': [5],                 # DTG trigger
          'binWidth': 1000,                 # width of Histogram bins in picoseconds
          'numBins': 1000,                   # histogram length = binWidth*numBins
          'maxDumps': 10**10,                # total maximum dump clicks (limited by disk space)
          'currentChan': [1],
          'numBinsCounter': 300,
          'binWidthCounter': 4*10**10,
          'delayTimes': [0,0,0,0,0,0,0,0,0,0],
          'maxStream': 10**9,
          'refreshTime': 0,
         }

# Write YAML file
with io.open('params.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(PARAMS, outfile, default_flow_style=True, allow_unicode=True)

# Read YAML file
