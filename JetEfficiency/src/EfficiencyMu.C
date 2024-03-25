/*
Input: Folder of L1Ntuples
Output: A plot of the jet turn-ons with and with out L1 dR matching vs calo jet pT
*/

#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"

#include "TDirectory.h"
#include "TSystemDirectory.h"
#include "TSystemFile.h"
#include "TChain.h"

#include "TMath.h"
#include "TH1F.h"
#include "TGraphAsymmErrors.h"
#include "TCanvas.h"
#include "TLegend.h"

#include <string>
#include <vector>
#include <iostream>

using namespace std;

double dr(float eta1, float phi1, float eta2, float phi2) {
    float deta = TMath::Abs(eta1 - eta2);
    float dphi = TMath::Abs(phi1 - phi2);
    if (dphi > TMath::Pi()) dphi = TMath::Abs(dphi - 2*TMath::Pi());

    return TMath::Sqrt(dphi*dphi + deta*deta);
}

void GetFiles(char const* input, vector<string>& files) {
    TSystemDirectory dir(input, input);
    TList *list = dir.GetListOfFiles();

    if (list) {
        TSystemFile *file;
        string fname;
        TIter next(list);
        while ((file = (TSystemFile*) next())) {
            fname = file->GetName();

            if (file->IsDirectory() && (fname.find(".") == string::npos)) {
                string newDir = string(input) + fname + "/";
                GetFiles(newDir.c_str(), files);
            }
            else if ((fname.find(".root") != string::npos)) {
                files.push_back(string(input) + fname);
                cout << files.back() << endl;
            }
        }
    }

    return;
}

void FillChain(TChain& chain, vector<string>& files) {
    for (auto file : files) {
        chain.Add(file.c_str());
    }
}

int Efficiency(char const* input) {
    /* read in all files in the input folder */
    vector<string> files;
    GetFiles(input, files);

    /* read in reco mu information */
    TChain offChain("muonAnalyzer/MuonTree");
    FillChain(offChain, files);
    TTreeReader offReader(&offChain);
    TTreeReaderValue<int>   muN(offReader, "nReco");
    TTreeReaderArray<float> muPt(offReader, "recoPt");
    TTreeReaderArray<float> muEta(offReader, "recoEta");
    TTreeReaderArray<float> muPhi(offReader, "recoPhi");

    /* read in emulated mu information */
    TChain emuChain("l1UpgradeEmuTree/L1UpgradeTree");
    FillChain(emuChain, files);
    TTreeReader emuReader(&emuChain);
    TTreeReaderValue<vector<float>> emumuPt(emuReader, "muonEt");
    TTreeReaderValue<vector<float>> emumuEta(emuReader, "muonEta");
    TTreeReaderValue<vector<float>> emumuPhi(emuReader, "muonPhi");

    string seed = "L1_SingleMu3_BptxAND";
    float threshold = 3;

    /* create histograms for efficiency plots */
    int nbins = 25;
    float min = 0;
    float max = 200;

    TH1F emuHist("emuHist", "", nbins, min, max);
    TH1F emuMatchedHist("emuMatchedHist", "", nbins, min, max);
    TH1F recoHist("recoHist", "", nbins, min, max);

    Long64_t totalEvents = emuReader.GetEntries(true);

    /* read in information from TTrees */
    for (Long64_t i = 0; i < totalEvents; i++) {
        emuReader.Next(); offReader.Next();

        if (i % 20000 == 0) { 
            cout << "Entry: " << i << " / " <<  totalEvents << endl; 
        }

        float maxmuPt = -999;
        float emuMaxmuPt = -999;

        /* iterate through muons and find the muon with max pT */
        for (int i = 0; i < *muN; ++i) {
            if (TMath::Abs(muEta[i]) > 2) { continue; }

            if (muPt[i] > maxmuPt) {
                maxmuPt = muPt[i];
            }
        }

        if (maxmuPt >= threshold) {
            recoHist.Fill(maxmuPt);

            /* iterate through emu mus and find matched and unmatched mus with max pT */
            for (size_t i = 0; i < (*emumuPt).size(); ++i) {
                if ((*emumuPt)[i] > emuMaxmuPt) {
                    emuMaxmuPt = (*emumuPt)[i];
                }
            }

            if (emuMaxmuPt >= threshold) {
                emuHist.Fill(maxmuPt);
            }
        }
    }

    TGraphAsymmErrors emuRecoEff(&emuHist, &recoHist, "cl=0.683 b(1,1) mode");
    TGraphAsymmErrors emuRecoMatchedEff(&emuMatchedHist, &recoHist, "cl=0.683 b(1,1) mode");

    /* plot the turn ons vs reco mu pt */
    TCanvas recoCanvas("recoCanvas", "", 0, 0, 500, 500);
    recoCanvas.cd();

    emuRecoMatchedEff.GetXaxis()->SetTitle("Reco #mu pT (GeV)");
    emuRecoMatchedEff.GetXaxis()->CenterTitle(true);
    emuRecoMatchedEff.GetYaxis()->SetTitle("Efficiency");
    emuRecoMatchedEff.GetYaxis()->CenterTitle(true);

    emuRecoMatchedEff.SetMarkerColor(46);
    emuRecoMatchedEff.SetLineColor(46);
    emuRecoMatchedEff.SetMarkerSize(0.5);
    emuRecoMatchedEff.SetMarkerStyle(20);
    emuRecoMatchedEff.Draw();

    emuRecoEff.SetMarkerColor(30);
    emuRecoEff.SetLineColor(30);
    emuRecoEff.SetMarkerSize(0.5);
    emuRecoEff.SetMarkerStyle(20);
    emuRecoEff.Draw("LP SAME");

    TLegend recoLegend(0.53, 0.12 ,0.88, 0.3);
    recoLegend.SetTextSize(0.03);
    recoLegend.SetHeader(seed.c_str());
    recoLegend.AddEntry(&emuRecoEff, "Not #DeltaR Matched", "lep");
    recoLegend.AddEntry(&emuRecoMatchedEff, "#DeltaR Matched", "lep");
    recoLegend.Draw();

    recoCanvas.SaveAs("RecomuEfficiency.pdf");

    /* save histograms to file so I can look at them */
    TFile* fout = new TFile("muhistograms.root", "recreate");

    emuHist.Write();
    emuMatchedHist.Write();
    recoHist.Write();

    fout->Close();
   
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc == 2)
        return Efficiency(argv[1]);
    else {
        cout << "ERROR" << endl;
        return -1;
    }
}
