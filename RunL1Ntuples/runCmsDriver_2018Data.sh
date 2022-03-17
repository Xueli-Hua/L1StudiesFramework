#!/bin/bash

globaltag=123X_dataRun2_v1 # for Run 2 data reprocessing
era=Run2_2018_pp_on_AA # for Run 2
filein='file:/eos/cms/store/group/phys_heavyions/mitaylor/L1EmulatorTestFiles/MinimumBias.root' # change to desired test file
config=L1Ntuple_Data2018; # cmsRun config file name

cmsDriver.py l1Ntuple -s RAW2DIGI --no_exec --repacked --python_filename=${config}.py \
    -n 1000 --no_output --era=${era} --data --conditions=${globaltag} \
    --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW \
    --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU \
    --customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParams_2018_v1_4_1 \
    --customise=L1Trigger/Configuration/customiseUtils.L1TGlobalMenuXML \
    --filein=${filein}

echo '
process.hcalDigis.saveQIE10DataNSamples = cms.untracked.vint32(10) 
process.hcalDigis.saveQIE10DataTags = cms.untracked.vstring( "MYDATA" )
process.es_prefer_caloparams = cms.ESPrefer("PoolDBESSource","l1conddb")
MassReplaceInputTag(process, new="rawDataMapperByLabel", old="rawDataCollector")

process.HFAdcana = cms.EDAnalyzer("HFAdcToGeV",
    digiLabel = cms.untracked.InputTag("hcalDigis"),
    minimized = cms.untracked.bool(True)
)

process.HFAdc = cms.Path(process.HFAdcana)
process.schedule.append(process.HFAdc)
' >> ${config}.py