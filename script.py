# -*- coding: utf-8 -*-
# Description: A template script for performing multiple different RCA analyses
# Author: Nicholas W. M. Ritchie
# Modified: 2-Mar-2017

analyst = "Nicholas W. M. Ritchie" # Replace with your analyst = "your name"! 

beamEnergy = 25.0 # keV (Checked, not set, used to select standards)
ruleFile = "generic.zrr" # or you can specify one in 'basicRCA', 'highZRCA' etc.
realTime = 0.3 # seconds per particle
randomize = True

# Define the elements and the associated standards in the vector file
stds = { 
	"C": "C std.msa", "Al": "Al std.msa", "Cu":"Cu std.msa", "Ni":"Ni std.msa", 
	"Na": "NaF std.msa", "O": "MgO std.msa", "Si": "Si std.msa", # "Cl": "NaCl std.msa",
	"Fe": "Fe std.msa", "Ca": "CaF2 std.msa", "Cr": "Cr std.msa", "Ni":"Ni std.msa", 
	"Cu": "Cu std.msa", "Ti": "Ti std.msa", "Mg": "Mg std.msa", 
	"S" : "FeS2 std.msa", "Zn" : "Zn std.msa", "Ba":"BaF2 std.msa", "Mo": "Mo std.msa",
	"Ge": "Ge std.msa", "Bi" : "Bi std.msa", "U" : "U std.msa"
}

#Set these to point to the directory contain your standard spectra and rules
stdsPath = "%s\\standards\\Combined\\%g keV" % (rootPath, beamEnergy)
rulePath = "%s\\standards\\Rules" % (rootPath, )

# Default APA settings
def basicRCA(project, sample, tiling, stageZ):
	maxFields = 0 # 0 to analyze all in order otherwise >0 to randomize field selection (slower...)
	fov = 0.256 # mm
	maxPartPerField = 1000 #
	maxParticles = 100000
	seed = None # or an integer value (randomizes field selection for maxFields)
	measureThreshold = (32, 255) # lower, upper
	measureDwell = 4 # microseconds
	searchThreshold = (64, 255) # lower, upper
	searchDwell = 1 # microseconds

	vecs = buildVectors(stds,strip=["C","O"],path=stdsPath)
	rules = graf.BasicRuleSet("%s\\%s" % (rulePath, ruleFile))

	# Create the RCA object, initialize and execute the analysis
	rca=buildRCA(project, sample, vecs, rules, realTime=realTime, analyst=analyst)
	rca.setStageZ(stageZ)
	rca.setFieldOfView(fov, overlap = 1.0)
	rca.setMeasureThreshold(low=measureThreshold[0], high = measureThreshold[1], dwell = int(measureDwell*1000), measureStep = 8)
	rca.setSearchThreshold(low=searchThreshold[0], high = searchThreshold[1], dwell = int(searchDwell*1000), maxPartPerField=maxPartPerField, maxPart=maxParticles)
	try:
		if maxFields>0:
			rca.perform(randomSubSetOfATiling(tiling, maxFields, seed=seed))
		elif randomize:
			rca.perform(randomizedTiling(tiling, seed=seed))
		else:
			rca.perform(tiling)
	except jl.Throwable, ex:
		print "Error analyzing %s" % sample
		print str(ex)
	finally:
		rca.postSummary(jl.System.out)
	return rca.getZeppelin()

# APA settings biased towards high Z particles	
def highZRCA(project, sample, tiling, stageZ):
	maxFields = 0 # 0 to analyze all in order otherwise >0 to randomize field selection (slower...)
	fov = 0.256 # mm
	maxPartPerField = 1000 #
	maxParticles = 10000
	seed = None # or an integer value (randomizes field selection for maxFields)
	measureThreshold = (96, 255) # lower, upper
	measureDwell = 4 # microseconds
	searchThreshold = (128, 255) # lower, upper
	searchDwell = 1 # microseconds

	vecs = buildVectors(stds,strip=["C","O"],path=stdsPath)
	rules = graf.BasicRuleSet("%s\\%s" % (rulePath, ruleFile))

	# Create the RCA object, initialize and execute the analysis
	rca=buildRCA(project, sample, vecs, rules, realTime=realTime, analyst=analyst)
	rca.setStageZ(stageZ)
	rca.configEDS(vecs, rules, realTime=realTime, mode=POINT_MODE)
	rca.setFieldOfView(fov, overlap = 1.0)
	rca.setMeasureThreshold(low=measureThreshold[0], high = measureThreshold[1], dwell = int(measureDwell*1000), measureStep = 8)
	rca.setSearchThreshold(low=searchThreshold[0], high = searchThreshold[1], dwell = int(searchDwell*1000), maxPartPerField=maxPartPerField, maxPart=maxParticles)
	try:
		if maxFields>0:
			rca.perform(randomSubSetOfATiling(tiling, maxFields, seed=seed))
		elif randomize:
			rca.perform(randomizedTiling(tiling, seed=seed))
		else:
			rca.perform(tiling)
	except jl.Throwable, ex:
		print "Error analyzing %s" % sample
		print str(ex)
	finally:
		rca.postSummary(jl.System.out)
	return rca.getZeppelin()
	
# APA settings biased towards large particles
def basicRCALowMag(project, sample, tiling, stageZ):
	maxFields = 0 # 0 to analyze all in order otherwise >0 to randomize field selection (slower...)
	fov = 1.024 # mm
	maxPartPerField = 1000 #
	maxParticles = 100000
	seed = None # or an integer value (randomizes field selection for maxFields)
	measureThreshold = (32, 255) # lower, upper
	measureDwell = 4 # microseconds
	searchThreshold = (128, 255) # lower, upper
	searchDwell = 1 # microseconds

	vecs = buildVectors(stds,strip=["C","O"],path=stdsPath)
	rules = graf.BasicRuleSet("%s\\%s" % (rulePath, ruleFile))

	# Create the RCA object, initialize and execute the analysis
	rca=buildRCA(project, sample, vecs, rules, realTime=realTime, analyst=analyst)
	rca.setStageZ(stageZ)
	rca.setFieldOfView(fov, overlap = 1.0)
	rca.setMeasureThreshold(low=measureThreshold[0], high = measureThreshold[1], dwell = int(measureDwell*1000), measureStep = 8)
	rca.setSearchThreshold(low=searchThreshold[0], high = searchThreshold[1], dwell = int(searchDwell*1000), maxPartPerField=maxPartPerField, maxPart=maxParticles)
	try:
		if maxFields>0:
			rca.perform(randomSubSetOfATiling(tiling, maxFields, seed=seed))
		elif randomize:
			rca.perform(randomizedTiling(tiling, seed=seed))
		else:
			rca.perform(tiling)
	except jl.Throwable, ex:
		print "Error analyzing %s" % sample
		print str(ex)
	finally:
		rca.postSummary(jl.System.out)
	return rca.getZeppelin()

# A search setting for the smallest particles (A = 0.05 to 10 sq micrometers)
def basicHighMagRCA(project, sample, tiling, stageZ):
	maxFields = 10000 # 0 to analyze all in order otherwise >0 to randomize field selection (slower...)
	fov = 0.100 # mm
	maxPartPerField = 1000 #
	maxParticles = 10000
	seed = 0xBADF00D # or an integer value (randomizes field selection for maxFields)
	measureThreshold = (32, 255) # lower, upper
	measureDwell = 8 # microseconds
	searchThreshold = (64, 255) # lower, upper
	searchDwell = 4 # microseconds

	vecs = buildVectors(stds,strip=["C","O"],path=stdsPath)
	rules = graf.BasicRuleSet("%s\\%s" % (rulePath, ruleFile))

	# Create the RCA object, initialize and execute the analysis
	rca=buildRCA(project, sample, vecs, rules, realTime=realTime, analyst=analyst)
	rca.setStageZ(stageZ)
	rca.setFieldOfView(fov, overlap = 1.0)
	rca.setMeasureThreshold(low=measureThreshold[0], high = measureThreshold[1], dwell = int(measureDwell*1000), measureStep = 8)
	rca.setSearchThreshold(low=searchThreshold[0], high = searchThreshold[1], dwell = int(searchDwell*1000), maxPartPerField=maxPartPerField, maxPart=maxParticles)
	rca.setMorphologyCriterion(semtr.RcaTranslator.AreaCriterion(0.05, 1.0e4))
	try:
		if maxFields>0:
			rca.perform(randomSubSetOfATiling(tiling, maxFields, seed=seed))
		elif randomize:
			rca.perform(randomizedTiling(tiling, seed=seed))
		else:
			rca.perform(tiling)
	except jl.Throwable, ex:
		print "Error analyzing %s" % sample
		print str(ex)
	finally:
		rca.postSummary(jl.System.out)
	return rca.getZeppelin()
	
# Begin: CONFIGURATION SECTION
# This section contains most of the items that should be changed from analysis set to analysis set.
# 1.  Create pts1, pts2, ..., ptsN outlining the N samples
# 2.  Modify 'analyses' to describe the various different analyses 
#     a. You can perform multiple analyses per sample
#     b. Choices of tilings inlude 'circularTiling', 'rectangularTiling' and 'boundaryTiling'
#     c. The broad definition of the analysis is defined by 'highZRCA', 'basicRCA', 'basicRCALowMag' (You can create your own or modified these.)

pts2 = parseCoords("[{X:10.968,Y:-12.584,Z:24.991,Rotate:-0.00,Tilt:-0.00}, {X:16.378,Y:-4.281,Z:24.991,Rotate:-0.00,Tilt:-0.00}, {X:6.576,Y:-3.287,Z:24.991,Rotate:-0.00,Tilt:-0.00}]")

#pts3 = parseCoords("[{X:11.277,Y:1.332,Z:25.228,Rotate:-0.00,Tilt:-0.00}, {X:16.509,Y:8.821,Z:25.228,Rotate:-0.00,Tilt:-0.00}, {X:6.475,Y:10.680,Z:25.228,Rotate:-0.00,Tilt:-0.00}]")

pts4 = parseCoords("[{X:-0.761,Y:7.850,Z:24.991,Rotate:-0.00,Tilt:-0.00}, {X:5.306,Y:15.848,Z:24.991,Rotate:-0.00,Tilt:-0.00}, {X:-5.089,Y:16.658,Z:24.991,Rotate:-0.00,Tilt:-0.00}]")

#pts5 = parseCoords("[{X:-11.875,Y:1.111,Z:25.104,Rotate:-0.00,Tilt:-0.00}, {X:-6.220,Y:8.521,Z:25.104,Rotate:-0.00,Tilt:-0.00}, {X:-16.660,Y:9.973,Z:25.104,Rotate:-0.00,Tilt:-0.00}]")

pts6 = parseCoords("[{X:-11.307,Y:-12.112,Z:24.991,Rotate:-0.00,Tilt:-0.00}, {X:-5.632,Y:-4.546,Z:24.991,Rotate:-0.00,Tilt:-0.00}, {X:-15.450,Y:-2.430,Z:24.991,Rotate:-0.00,Tilt:-0.00}]")

#pts7 = parseCoords("[{X:-0.016,Y:-6.318,Z:24.197,Rotate:-0.00,Tilt:-0.00}, {X:5.688,Y:1.503,Z:24.197,Rotate:-0.00,Tilt:-0.00}, {X:-4.112,Y:2.755,Z:24.197,Rotate:-0.00,Tilt:-0.00}]")

#tilt = parseCoords("[{X:-13.415,Y:-0.563,Z:24.644,Rotate:-0.00,Tilt:-0.00}, {X:-8.546,Y:-14.643,Z:25.483,Rotate:-0.00,Tilt:-0.00}, {X:-15.691,Y:-14.878,Z:25.444,Rotate:-0.00,Tilt:-0.00}]")

# WARNING: Working distance has been replaced by stageZ.  Now a stage motion instead of a change in focal distance.
analyses = (
   # ( "project", "sample", tiling, stageZ, rcaFunc ),
   ( "Amy's GSR", "Roman Candles - Post-handling, pre-ignition", circularTiling(pts2), 25.234, basicRCA ),
   # ( "Amy's GSR", "Spinners - Post-ignition", circularTiling(pts3), 25.074, basicRCA ),
   ( "Amy's GSR", "Roman Candles - Debris from JWC", circularTiling(pts4), 25.142, basicRCALowMag ),
   ( "Amy's GSR", "Roman Candles - Post cleanup", circularTiling(pts6), 25.179, basicRCA ),
   #( "Background Swipes", "Blank", boundaryTiling(pts4), 24.581, highZRCA ),
   #( "Background Swipes", "BS3307", circularTiling(pts5), 24.679, highZRCA ),
   #( "Background Swipes", "BS3308", circularTiling(pts6), 24.644, highZRCA ),
   #( "Background Swipes", "BS3309", circularTiling(pts7), 24.605, highZRCA ),
   #( "", "", circularTiling(pts7), 24.861, basicRCA ),
)

# End: CONFIGURATION SECTION

# Begin: RUN SECTION 
# Avoid modification
run = True
if jl.Math.abs(_ts.hvGetVoltage()-beamEnergy*1.0e3)>100.0:
	print "ERROR: Instrument not configured for %0.1f keV" % beamEnergy
	run = False
if _ts.hvGetBeam()<>1:
	print "ERROR: Electron beam not on!"
	run = False

# Check Z motions to reduce risk of collision

if run:
	results=[]
	try:
		for project, sample, tiling, stageZ, rcaFunc in analyses:
			try:
				result = rcaFunc(project, sample, tiling, stageZ)
				results.append(result)
			except jl.Throwable, ex:
				print "Error analyzing %s - %s" % (project, sample)
				print str(ex)
			if terminated:
				all = (jop.showConfirmDialog(MainFrame, "Terminate all analyses?", "multiRCA", jop.YES_NO_OPTION) == jop.YES_OPTION)
				if all:
					break
				else:
					terminated=False
	finally:
		if not terminated:
			turnOff()
			#if defaultArchivePath:
			#	for r in results:
			#		r.archive()
else:
	print "Correct the problems and re-run."
# END: RUN SECTION
