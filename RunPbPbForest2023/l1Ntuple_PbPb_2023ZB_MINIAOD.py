
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1Ntuple -s RAW2DIGI --no_exec --repacked --python_filename=l1Ntuple_PbPb_2023ZB.py -n 100 --no_output --era=Run3_pp_on_PbPb_2023 --data --conditions=132X_dataRun3_Prompt_v4 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU --customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParamsHI_2023_v0_4_2 --customise=L1Trigger/Configuration/customiseUtils.L1TGlobalMenuXML --filein=/store/hidata/HIRun2023A/HIZeroBias0/RAW/v1/000/375/703/00000/00745763-ee4b-4a6f-b0ff-bc1bb4123400.root
import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_2023_cff import Run3_pp_on_PbPb_2023
process = cms.Process('HiForest',Run3_pp_on_PbPb_2023)

# HiForest labeling info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 132X, data")


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.RawToDigi_DataMapper_cff')
#process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '132X_dataRun3_Prompt_v4', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

# ==================================================================
# ==================== modification needed for 2023 data ===========
from CondCore.CondDB.CondDB_cfi import *
process.es_pool = cms.ESSource("PoolDBESSource",
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string("HcalElectronicsMapRcd"),
            tag = cms.string("HcalElectronicsMap_2021_v2.0_data")
        )
    ),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
        authenticationMethod = cms.untracked.uint32(1)
    )

process.es_prefer = cms.ESPrefer('HcalTextCalibrations', 'es_ascii')
process.es_ascii = cms.ESSource(
    'HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(

            object = cms.string('ElectronicsMap'),
            file = cms.FileInPath("L1Trigger/L1TZDC/data/emap_2023_newZDC_v3.txt")

             )
        )
    )
# ===================================================================

# ===================================================================
# Set spike killer settings for emulation
process.GlobalTag.toGet.extend = cms.VPSet(
   cms.PSet(record = cms.string('EcalTPGFineGrainStripEERcd'),
        tag = cms.string('EcalTPGFineGrainStrip_7'),
        connect =cms.string('frontier://FrontierProd/CMS_CONDITIONS')
    ),
    cms.PSet(record = cms.string('EcalTPGSpikeRcd'),
        tag = cms.string('EcalTPGSpike_12'),
        connect =cms.string('frontier://FrontierProd/CMS_CONDITIONS')
    )
)
#===================================================================

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        'root://xrootd-cms.infn.it//store/hidata/HIRun2023A/HIEphemeralZeroBias0/MINIAOD/PromptReco-v2/000/374/961/00000/ff7fe782-046e-4be5-aa9b-b00ab50cedd3.root',
    ),
    secondaryFileNames = cms.untracked.vstring(
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/0a20eb74-55bc-4a26-9682-b825120bfa15.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/0ed92d96-a256-4600-8cec-b67479679621.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/39506fa1-9d5d-4724-aa60-d008a8e4230f.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/6eeb89e9-0156-414e-b6bc-d814b990cb32.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/6feb51ba-3bc7-424a-9e84-ec78da6fc18f.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/735ba4ad-4555-4674-921d-96d37a6942ae.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/7500a0cf-7da9-4197-bf0b-8d1d84b98f19.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/8af20b59-9d98-461c-ba30-5a34180234e9.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/8c6df2aa-746e-4a41-841a-0087c5c87515.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/a7facd3f-6a31-40cf-81fe-8b3f894b3afa.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/b4d3469d-f89e-483e-a9eb-ddb801667ae3.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/b6563d19-9e51-4ec4-a16d-88e2721fbe82.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/bb7309ea-db93-4bfe-ada4-d7ce84a9f873.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/caa12dfe-3c0d-4611-95c4-f4c8782037ee.root',
        '/store/hidata/HIRun2023A/HIEphemeralZeroBias0/RAW/v1/000/374/961/00000/da31b74e-7099-4053-9ef7-516522e6ec5a.root',
    ),
    dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_gtStage2Digis_*_RECO',
    )
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

# centralityBin
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

#####################################################################################
# Event analysis
#####################################################################################

process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

# process.hiEvtAnalyzer.doCentrality = cms.bool(False)
# process.hiEvtAnalyzer.doHFfilters = cms.bool(False)

from HeavyIonsAnalysis.EventAnalysis.hltobject_cfi import trigger_list_data_2023_skimmed
process.hltobject.triggerNames = trigger_list_data_2023_skimmed

process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')

#####################################################################################
# Photons, electrons, and muons
#####################################################################################

process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")

#########################
# Jets
#########################

process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.akPu4CaloJetSequence_pponPbPb_data_cff')
process.akPu4CaloJetAnalyzer.doHiJetID = True

#########################
# Tracks
#########################

process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")

#########################
# Forest list
#########################

process.forest = cms.Path(
    process.HiForestInfo +
    process.centralityBin +
    process.hiEvtAnalyzer +
    process.hltanalysis +
    process.hltobject +
    process.l1object +
    process.trackSequencePbPb +
    process.ggHiNtuplizer +
    process.unpackedMuons +
    process.muonAnalyzer +
    process.akPu4CaloJetAnalyzer
)

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.forest,process.raw2digi_step,process.endjob_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


#####################################################################################
# L1 emulation
#####################################################################################

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 

#call to customisation function L1TReEmulFromRAW imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulFromRAW(process)

# Automatic addition of the customisation function from L1Trigger.L1TNtuples.customiseL1Ntuple
from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleRAWEMU 

#call to customisation function L1NtupleRAWEMU imported from L1Trigger.L1TNtuples.customiseL1Ntuple
process = L1NtupleRAWEMU(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseSettings
from L1Trigger.Configuration.customiseSettings import L1TSettingsToCaloParamsHI_2023_v0_4_2 

#call to customisation function L1TSettingsToCaloParamsHI_2023_v0_4_2 imported from L1Trigger.Configuration.customiseSettings
process = L1TSettingsToCaloParamsHI_2023_v0_4_2(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseUtils
from L1Trigger.Configuration.customiseUtils import L1TGlobalMenuXML 

#call to customisation function L1TGlobalMenuXML imported from L1Trigger.Configuration.customiseUtils
process = L1TGlobalMenuXML(process)

#########################
# Customization
#########################

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("L1Forest.root"))


# =====================================================================
# add in the zdc analyzer - this writes the digi information to a tree
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018Producer_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.QWZDC2018RecHit_cfi')
process.load('HeavyIonsAnalysis.ZDCAnalysis.zdcanalyzer_cfi')

process.zdcanalyzer.doZDCRecHit = False
process.zdcanalyzer.doZDCDigi = True
process.zdcanalyzer.zdcRecHitSrc = cms.InputTag("QWzdcreco")
process.zdcanalyzer.zdcDigiSrc = cms.InputTag("hcalDigis", "ZDC")
process.zdcanalyzer.calZDCDigi = False
process.zdcanalyzer.verbose = False
process.zdcanalyzer_step = cms.Path(process.zdcanalyzer)
process.schedule.append(process.zdcanalyzer_step)
#=======================================================================

# ======================================================================
# ======================== add in the emulator =========================
# unpacked etsums
process.l1UpgradeTree.sumZDCTag = cms.untracked.InputTag("gtStage2Digis","EtSumZDC")
process.l1UpgradeTree.sumZDCToken = cms.untracked.InputTag("gtStage2Digis","EtSumZDC")

# l1 emulator sums
process.l1UpgradeEmuTree.sumZDCTag = cms.untracked.InputTag("etSumZdcProducer")
process.l1UpgradeEmuTree.sumZDCToken = cms.untracked.InputTag("etSumZdcProducer")

# do not change these settings
process.etSumZdcProducer = cms.EDProducer('L1TZDCProducer',
                                          zdcDigis = cms.InputTag("hcalDigis", "ZDC"),
                                          sampleToCenterBX = cms.int32(2),
                                          bxFirst = cms.int32(-2),
                                          bxLast = cms.int32(3)
)

process.etSumZdc = cms.Path(process.etSumZdcProducer)
process.schedule.append(process.etSumZdc)
#======================================================================

process.hcalDigis.saveQIE10DataNSamples = cms.untracked.vint32(6) 
process.hcalDigis.saveQIE10DataTags = cms.untracked.vstring( "MYDATA" )


from Configuration.Applications.ConfigBuilder import MassReplaceInputTag
# input tag replacement needed for Forward and ZeroBias data
MassReplaceInputTag(process, new="rawDataRepacker", old="rawDataCollector")

# input tag replacement needed for raw prime data
#MassReplaceInputTag(process, new="rawPrimeDataRepacker", old="rawDataCollector")
