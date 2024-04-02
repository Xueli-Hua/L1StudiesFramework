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

double rho(float vx, float vy, float vz) {
    float rho = TMath::Sqrt(vx*vx+vy*vy+vz*vz);
    return rho;
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

//

void FillChain(TChain& chain, vector<string>& files) {
    for (auto file : files) {
        chain.Add(file.c_str());
    }
}
//
int Efficiency(char const* input) {
    /* read in all files in the input folder */
    vector<string> files;
    GetFiles(input, files);

    /* read in reco mu information */
    TChain recoMuChain("muonAnalyzer/MuonTree");
    TChain trkChain("PbPbTracks/trackTree");
    FillChain(recoMuChain, files);
    FillChain(trkChain, files);
    TTreeReader recoMuReader(&recoMuChain);
    TTreeReader trkReader(&trkChain);
    TTreeReaderArray<bool> isFake(trkReader, "isFakeVtx");
    TTreeReaderArray<float> xVtx(trkReader, "xVtx");
    TTreeReaderArray<float> yVtx(trkReader, "yVtx");
    TTreeReaderArray<float> zVtx(trkReader, "zVtx");
    TTreeReaderValue<int> recomuN(recoMuReader, "nReco");
    TTreeReaderArray<float> recomuP(recoMuReader, "recoP");
    TTreeReaderArray<float> recomuPt(recoMuReader, "recoPt");
    TTreeReaderArray<float> recomuEta(recoMuReader, "recoEta");
    TTreeReaderArray<bool> recomuIsTrk(recoMuReader, "recoIsTracker");
    TTreeReaderArray<bool> recomuIDSoft(recoMuReader, "recoIDSoft");
    TTreeReaderValue<int> innermuN(recoMuReader, "nInner");
    TTreeReaderArray<int> innermuTrkL(recoMuReader, "innerTrkLayers");
    TTreeReaderArray<int> innermuPixL(recoMuReader, "innerPixelLayers");
    TTreeReaderArray<float> innerDxy(recoMuReader, "innerDxy");
    TTreeReaderArray<float> innerDz(recoMuReader, "innerDz");
    TTreeReaderArray<bool> innerIsHPTrk(recoMuReader, "innerIsHighPurityTrack");
    
    /* read in emulated mu information */
    TChain l1Chain("l1object/L1UpgradeFlatTree");
    FillChain(l1Chain, files);
    TTreeReader l1Reader(&l1Chain);
    TTreeReaderValue<vector<float>> l1muEt(l1Reader, "muonEt");
    TTreeReaderValue<vector<float>> l1muEta(l1Reader, "muonEta");
    TTreeReaderValue<vector<unsigned short>> l1muQual(l1Reader, "muonQual");
    
    string seed = "L1_SingleMuonOpen_NotMinimumBiasHF2_AND_BptxAND";

    /* create histograms for efficiency plots */
    int nbins = 25;
    float min = 0;
    float max = 10;

    TH1F l1muHist("l1muHist", "", nbins, min, max);
    TH1F l1MaxmuHist("l1MaxmuHist", "", 50, -10, 10);
    TH1F recomuHist("recomuHist", "", nbins, min, max);

    Long64_t totalEvents = l1Reader.GetEntries(true);
    
    /* read in information from TTrees */
    for (Long64_t i = 0; i < totalEvents; i++) {
        l1Reader.Next(); recoMuReader.Next(); trkReader.Next();

        if (i % 20000 == 0) { 
            cout << "Entry: " << i << " / " <<  totalEvents << endl; 
        }

        //bool softmuon = 0;
        int NtrkHP = 0;
        float l1MaxMuPt = -999;

        /* iterate through reco muons and do selection */
        for (int i = 0; i < *recomuN; ++i) {
            /*if(
                //glbmuon1 && 
                recomuIsTrk[i] &&
                innermuTrkL[i] > 5 &&
                innermuPixL[i] > 0 &&
                innerDxy[i] < 0.3 &&
                innerDz[i] < 20.
                ) softmuon = 1;*/
            if (recomuP[i]>2.5 && TMath::Abs(recomuEta[i]) < 2.4 && recomuIsTrk[i] && innerIsHPTrk[i]) NtrkHP++;
        }
        if (NtrkHP!=2) continue;

        /* iterate through l1object muons and find max et */
        for (size_t j = 0; j < (*l1muEt).size(); ++j) { if ((*l1muEt)[j] > l1MaxMuPt) { l1MaxMuPt = (*l1muEt)[j]; } }
        l1MaxmuHist.Fill(l1MaxMuPt);

        for (int i = 0; i < *recomuN; ++i) {
            if (recomuP[i]>2.5 && TMath::Abs(recomuEta[i]) < 2.4 && recomuIsTrk[i] && innerIsHPTrk[i] && recomuIDSoft[i]) { 
                recomuHist.Fill(recomuPt[i]); 
                if (l1MaxMuPt>0) l1muHist.Fill(recomuPt[i]);
            }
        }
    }
    //TGraphAsymmErrors RecoMuEff(&l1muHist, &recomuHist, "cl=0.683 b(1,1) mode");
    TGraphAsymmErrors RecoMuEff(&l1muHist, &recomuHist);

    /* plot the turn ons vs reco mu pt */
    TCanvas recoCanvas("recoCanvas", "", 0, 0, 500, 500);
    recoCanvas.cd();

    RecoMuEff.GetXaxis()->SetTitle("Reco #mu pT (GeV)");
    RecoMuEff.GetXaxis()->CenterTitle(true);
    RecoMuEff.GetYaxis()->SetTitle("Efficiency");
    RecoMuEff.GetYaxis()->CenterTitle(true);
    RecoMuEff.SetMinimum(0);

    RecoMuEff.SetMarkerColor(46);
    RecoMuEff.SetLineColor(46);
    RecoMuEff.SetMarkerSize(0.5);
    RecoMuEff.SetMarkerStyle(20);
    RecoMuEff.Draw("AP");

    TLegend recoLegend(0.13, 0.12 ,0.88, 0.2);
    recoLegend.SetBorderSize(0);
    recoLegend.SetFillStyle(0);
    recoLegend.SetTextSize(0.03);
    recoLegend.SetHeader(seed.c_str());
    //recoLegend.AddEntry(&RecoMuEff, "#DeltaR Matched", "lep");
    recoLegend.Draw();

    recoCanvas.SaveAs("RecomuEfficiency.pdf");

    /* save histograms to file so I can look at them */
    TFile* fout = new TFile("muhistograms.root", "recreate");

    l1muHist.Write();
    l1MaxmuHist.Write();
    recomuHist.Write();

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
