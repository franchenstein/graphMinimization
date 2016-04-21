from PyQt4 import QtGui
import sys
import generatr
import json
sys.path.insert(1, '../')
import test_generated_graph as tgg

class ExampleApp(QtGui.QMainWindow, generatr.Ui_Generatr):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        #System Types:
        self.type = {}
        self.type['binary'] = False
        self.type['even'] = False
        self.type['tri'] = False
        self.type['ternary'] = False
        self.type['henon'] = False
        self.type['10dbq1'] = False
        self.type['10dbq2'] = False
        self.type['15dbq1'] = False
        #D-Markov Configs:
        self.dmark = {}
        self.dmark['Enable'] = False
        self.dmark['ini'] = 0
        self.dmark['end'] = 0
        #Mk1 Configs:
        self.mk1 = {}
        self.mk1['Enable'] = False
        self.mk1['old'] = False
        self.mk1['new'] = False
        self.mk1['dmark'] = False
        #Mk2 Configs:
        self.mk2 = {}
        self.mk2['Enable'] = False
        self.mk2['old'] = False
        self.mk2['new'] = False
        self.mk2['dmark'] = False
        #L Configs:
        self.L = {}
        self.L['multi'] = False
        self.L['ini'] = 0
        self.L['fin'] = 0
        self.L['single'] = 8
        #Alpha Configs:
        self.alpha = {}
        self.alpha['multi'] = False
        self.alpha['ini'] = 0
        self.alpha['fin'] = 0
        self.alpha['single'] = 0.95
        #Button actions:
        self.saveconf.clicked.connect(self.saveConfiguration)
        self.check_binary.clicked.connect(self.toggleBinary)
        self.check_even.clicked.connect(self.toggleEven)
        self.check_ternary.clicked.connect(self.toggleTernary)
        self.check_tri.clicked.connect(self.toggleTri)
        self.check_10dbq1.clicked.connect(self.toggle10dbq1)
        self.check_10dbq2.clicked.connect(self.toggle10dbq2)
        self.check_henon.clicked.connect(self.toggleHenon)
        self.check_15dbq1.clicked.connect(self.toggle15dbq1)
        self.check_dmarkov.clicked.connect(self.toggleDMark)
        self.check_mk1.clicked.connect(self.toggleMk1)
        self.check_mk1_old.clicked.connect(self.toggleMk1Old)
        self.check_mk1_new.clicked.connect(self.toggleMk1New)
        self.check_mk1_dmark.clicked.connect(self.toggleMk1DMark)
        self.check_mk2.clicked.connect(self.toggleMk2)
        self.check_mk2_old.clicked.connect(self.toggleMk2Old)
        self.check_mk2_new.clicked.connect(self.toggleMk2New)
        self.check_mk2_dmark.clicked.connect(self.toggleMk2DMark)
        self.check_multL.clicked.connect(self.toggleMultL)
        self.check_multi_alpha.clicked.connect(self.toggleMultiAlpha)
        self.gengraph.clicked.connect(self.generateGraphs)
        self.genseq.clicked.connect(self.generateSequences)
        self.analyze.clicked.connect(self.analyzeSequences)
        self.plot.clicked.connect(self.plotGraphs)
        
    def saveConfiguration(self):
        f = open('config.json', 'w')
        if self.dmark['Enable']:
            self.dmark['ini'] = int(self.line_d_ini.text())
            self.dmark['end'] = int(self.line_d_fin.text())
        if self.mk1['Enable'] or self.mk2['Enable']:
            if self.L['multi']:
                self.L['ini'] = int(self.line_L_ini.text())
                self.L['fin'] = int(self.line_L_fin.text())
            else:
                self.L['single'] = int(self.line_single_L.text())
            if self.alpha['multi']:
                self.alpha['ini'] = float(self.line_alpha_ini.text())
                self.alpha['fin'] = float(self.line_alpha_fin.text())
            else:
                self.alpha['single'] = float(self.line_single_alpha.text())
        configs = {}
        configs['type'] = self.type
        configs['dmark'] = self.dmark
        configs['mk1'] = self.mk1
        configs['mk2'] = self.mk2
        configs['L'] = self.L
        configs['alpha'] = self.alpha
        json.dump(configs, f)
        f.close()
    
    def toggleBinary(self):
        self.type['binary'] = not self.type['binary'] 
       
    def toggleEven(self):
        self.type['even'] = not self.type['even']
    
    def toggleTernary(self):
        self.type['ternary'] = not self.type['ternary'] 
       
    def toggleTri(self):
        self.type['tri'] = not self.type['tri']  
    
    def toggle10dbq1(self):
        self.type['10dbq1'] = not self.type['10dbq1'] 
       
    def toggle10dbq2(self):
        self.type['10dbq2'] = not self.type['10dbq2']   
    
    def toggleHenon(self):
        self.type['henon'] = not self.type['henon'] 
       
    def toggle15dbq1(self):
        self.type['15dbq1'] = not self.type['15dbq1'] 
       
    def toggleDMark(self):
        self.dmark['Enable'] = not self.dmark['Enable'] 
       
    def toggleMk1(self):
        self.mk1['Enable'] = not self.mk1['Enable']
        
    def toggleMk1Old(self):
        self.mk1['old'] = not self.mk1['old']  
        
    def toggleMk1New(self):
        self.mk1['new'] = not self.mk1['new']  
        
    def toggleMk1DMark(self):
        self.mk1['dmark'] = not self.mk1['dmark']  
       
    def toggleMk2(self):
        self.mk2['Enable'] = not self.mk2['Enable'] 
        
    def toggleMk2Old(self):
        self.mk2['old'] = not self.mk2['old']  
        
    def toggleMk2New(self):
        self.mk2['new'] = not self.mk2['new']  
        
    def toggleMk2DMark(self):
        self.mk2['dmark'] = not self.mk2['dmark'] 
       
    def toggleMultL(self):
        self.L['multi'] = not self.L['multi'] 
       
    def toggleMultiAlpha(self):
        self.alpha['multi'] = not self.alpha['multi'] 
        
    def generateGraphs(self):
        self.bar_gengraph.setValue(0)
        types, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin = self.readConfigs()
        barMaxPerIteration = 1/len(types)
        for t in types:
            if dmark['Enable']:
                tgg.genDMarkovGraphs(t, dmark['ini'], dmark['end'])
            self.bar_gengraph.setValue(self.bar_gengraph.value() + 10*barMaxPerIteration)
            if mk1['Enable']:
                if mk1['old']:
                    tgg.genMk1Graphs(t, L_ini, L_fin, alpha_ini, alpha_fin, 'old') 
                if mk1['new']:
                    tgg.genMk1Graphs(t, L_ini, L_fin, alpha_ini, alpha_fin, 'new')
                if mk1['dmark']:
                    tgg.genMk1Graphs(t, L_ini, L_fin, alpha_ini, alpha_fin, 'dmark')            
            self.bar_gengraph.setValue(self.bar_gengraph.value() + 45*barMaxPerIteration)
            if mk2['Enable']:
                if mk2['old']:
                    tgg.genMk2Graphs(t, L_ini, L_fin, alpha_ini, alpha_fin, 'old') 
                if mk2['new']:
                    tgg.genMk2Graphs(t, L_ini, L_fin, alpha_ini, alpha_fin, 'new')
                if mk2['dmark']:
                    tgg.genMk2Graphs(t, L_ini, L_fin, alpha_ini, alpha_fin, 'dmark')
            self.bar_gengraph.setValue(self.bar_gengraph.value() + 45*barMaxPerIteration)
            
    def generateSequences(self):
        original = self.check_original.checkState()
        l = int(self.line_length.text())
        types, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin = self.readConfigs()
        self.bar_genseq.setValue(0)
        barMaxPerIteration = 1/len(types)
        for t in types:
            if original:
                if t == 'even' or t == 'tri':
                    tgg.genSequences(t, orig, 'x', l)
            self.bar_genseq.setValue(self.bar_genseq.value() + 5*barMaxPerIteration)
            if dmark['Enable']:
                tgg.genSequences(t, False, 'dmark', l, dmark['ini'], dmark['end']) 
            self.bar_genseq.setValue(self.bar_genseq.value() + 5*barMaxPerIteration)
            if mk1['Enable']:
                if mk1['old']:
                    tgg.genSequences(t, False, 'mk1', l, L_ini,
                                          L_fin, alpha_ini, alpha_fin, 'old') 
                if mk1['new']:
                    tgg.genSequences(t, False, 'mk1', l, L_ini,
                                          L_fin, alpha_ini, alpha_fin, 'new') 
                if mk1['dmark']:
                    tgg.genSequences(t, False, 'mk1', l, L_ini,
                                          L_fin, alpha_ini, alpha_fin, 'dmark')
            self.bar_genseq.setValue(self.bar_genseq.value() + 45*barMaxPerIteration) 
            if mk2['Enable']:
                if mk2['old']:
                    tgg.genSequences(t, False, 'mk2', l, L_ini,
                                          L_fin, alpha_ini, alpha_fin, 'old') 
                if mk2['new']:
                    tgg.genSequences(t, False, 'mk2', l, L_ini,
                                          L_fin, alpha_ini, alpha_fin, 'new') 
                if mk2['dmark']:
                    tgg.genSequences(t, False, 'mk2', l, L_ini,
                                          L_fin, alpha_ini, alpha_fin, 'dmark')
            self.bar_genseq.setValue(self.bar_genseq.value() + 45*barMaxPerIteration) 
            
    def analyzeSequences(self):
        types, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin = self.readConfigs()
        self.bar_an_seq.setValue(0)
        barMaxPerIteration = 1/len(types)
        e = self.check_entropy.checkState()
        a = self.check_autocorr.checkState()
        k = self.check_kld.checkState()
        l1 = self.check_l1metric.checkState()
        km = self.check_kldmetric.checkState()
        if e:
            Le = int(self.line_entropy.text())
        else:
            Le = 15
        if a:
            La = int(self.line_autocorr.text())
        if k:
            Lk = int(self.line_kld.text())
        if l1:
            Ll1 = int(self.line_l1metric.text())
        if km:
            Lkm = int(self.line_kldmetric.text())
        for t in types:
            if e or k:
                tgg.calcProbs(t, True, 'original', Le, expn = '')
                if dmark['Enable']:
                    tgg.calcProbs(t, False, 'dmark', Le, dmark['ini'], dmark['end']) 
                if mk1['Enable']:
                    if mk1['old']:
                        tgg.calcProbs(t, False, 'mk1', Le, L_ini,
                                              L_fin, alpha_ini, alpha_fin, 'old') 
                    if mk1['new']:
                        tgg.calcProbs(t, False, 'mk1', Le, L_ini,
                                              L_fin, alpha_ini, alpha_fin, 'new') 
                    if mk1['dmark']:
                        tgg.calcProbs(t, False, 'mk1', Le, L_ini,
                                              L_fin, alpha_ini, alpha_fin, 'dmark')
                if mk2['Enable']:
                    if mk2['old']:
                        tgg.calcProbs(t, False, 'mk2', Le, L_ini,
                                              L_fin, alpha_ini, alpha_fin, 'old') 
                    if mk2['new']:
                        tgg.calcProbs(t, False, 'mk2', Le, L_ini,
                                              L_fin, alpha_ini, alpha_fin, 'new') 
                    if mk2['dmark']:
                        tgg.calcProbs(t, False, 'mk2', Le, L_ini,
                                              L_fin, alpha_ini, alpha_fin, 'dmark')
             
            self.bar_an_seq.setValue(self.bar_an_seq.value() + 35*barMaxPerIteration)
            if e: 
                tgg.calcEntropies(t, 'original', Le, '')
                if dmark['Enable']:
                    tgg.calcEntropies(t, 'dmark', Le, '') 
                if mk1['Enable']:
                    if mk1['old']:
                        tgg.calcEntropies(t, 'mk1', Le, 'old') 
                    if mk1['new']:
                        tgg.calcEntropies(t, 'mk1', Le, 'new') 
                    if mk1['dmark']:
                        tgg.calcEntropies(t, 'mk1', Le, 'dmark') 
                if mk2['Enable']:
                    if mk2['old']:
                        tgg.calcEntropies(t, 'mk2', Le, 'old') 
                    if mk2['new']:
                        tgg.calcEntropies(t, 'mk2', Le, 'new') 
                    if mk2['dmark']:
                        tgg.calcEntropies(t, 'mk2', Le, 'dmark') 
            
            self.bar_an_seq.setValue(self.bar_an_seq.value() + 15*barMaxPerIteration)
            if k: 
                if dmark['Enable']:
                    tgg.calcKLD(t, 'dmark', Lk, '') 
                if mk1['Enable']:
                    if mk1['old']:
                        tgg.calcKLD(t, 'mk1', Lk, 'old') 
                    if mk1['new']:
                        tgg.calcKLD(t, 'mk1', Lk, 'new') 
                    if mk1['dmark']:
                        tgg.calcKLD(t, 'mk1', Lk, 'dmark') 
                if mk2['Enable']:
                    if mk2['old']:
                        tgg.calcKLD(t, 'mk2', Lk, 'old') 
                    if mk2['new']:
                        tgg.calcKLD(t, 'mk2', Lk, 'new') 
                    if mk2['dmark']:
                        tgg.calcKLD(t, 'mk2', Lk, 'dmark') 
            if l1: 
                if dmark['Enable']:
                    tgg.calc_l1_metric(t, 'dmark', Ll1, '') 
                if mk1['Enable']:
                    if mk1['old']:
                        tgg.calc_l1_metric(t, 'mk1', Ll1, 'old') 
                    if mk1['new']:
                        tgg.calc_l1_metric(t, 'mk1', Ll1, 'new') 
                    if mk1['dmark']:
                        tgg.calc_l1_metric(t, 'mk1', Ll1, 'dmark') 
                if mk2['Enable']:
                    if mk2['old']:
                        tgg.calc_l1_metric(t, 'mk2', Ll1, 'old') 
                    if mk2['new']:
                        tgg.calc_l1_metric(t, 'mk2', Ll1, 'new') 
                    if mk2['dmark']:
                        tgg.calc_l1_metric(t, 'mk2', Ll1, 'dmark')
            if km: 
                if dmark['Enable']:
                    tgg.calc_kld_metric(t, 'dmark', Lkm, '') 
                if mk1['Enable']:
                    if mk1['old']:
                        tgg.calc_kld_metric(t, 'mk1', Lkm, 'old') 
                    if mk1['new']:
                        tgg.calc_kld_metric(t, 'mk1', Lkm, 'new') 
                    if mk1['dmark']:
                        tgg.calc_kld_metric(t, 'mk1', Lkm, 'dmark') 
                if mk2['Enable']:
                    if mk2['old']:
                        tgg.calc_kld_metric(t, 'mk2', Lkm, 'old') 
                    if mk2['new']:
                        tgg.calc_kld_metric(t, 'mk2', Lkm, 'new') 
                    if mk2['dmark']:
                        tgg.calc_kld_metric(t, 'mk2', Lkm, 'dmark')
            self.bar_an_seq.setValue(self.bar_an_seq.value() + 15*barMaxPerIteration)
                    
            if a:
                tgg.calcAutoCorr(t, 'orig', La, True, L_ini, L_fin, alpha_ini, alpha_fin, '')
                if dmark['Enable']:
                    tgg.calcAutoCorr(t, 'dmark', La, False, dmark['ini'], dmark['end'], alpha_ini, alpha_fin, '')
                if mk1['Enable']:
                    if mk1['old']:
                        tgg.calcAutoCorr(t, 'mk1', La, False, L_ini, L_fin, alpha_ini, alpha_fin, 'old') 
                    if mk1['new']:
                        tgg.calcAutoCorr(t, 'mk1', La, False, L_ini, L_fin, alpha_ini, alpha_fin, 'new') 
                    if mk1['dmark']:
                        tgg.calcAutoCorr(t, 'mk1', La, False, L_ini, L_fin, alpha_ini, alpha_fin, 'dmark') 
                if mk2['Enable']:
                    if mk2['old']:
                        tgg.calcAutoCorr(t, 'mk2', La, False, L_ini, L_fin, alpha_ini, alpha_fin, 'old') 
                    if mk2['new']:
                        tgg.calcAutoCorr(t, 'mk2', La, False, L_ini, L_fin, alpha_ini, alpha_fin, 'new') 
                    if mk2['dmark']:
                        tgg.calcAutoCorr(t, 'mk2', La, False, L_ini, L_fin, alpha_ini, alpha_fin, 'dmark') 
            
            self.bar_an_seq.setValue(self.bar_an_seq.value() + 35*barMaxPerIteration)
            
    def plotGraphs(self):
        types, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin = self.readConfigs()
        e = self.plot_entropy.checkState()
        eByNoStates = self.plot_entropy_bynostates.checkState()
        a = self.plot_autocorr.checkState()
        k = self.plot_kld.checkState()      
        kByNoStates = self.plot_kld_bynostates.checkState()
        l1 = self.plot_l1metric.checkState()
        l1ByNoStates = self.plot_l1metric_bynostate.checkState()
        km = self.plot_kldmetric.checkState()
        kmByNoStates = self.plot_kldmetric_bynostates.checkState()
        for t in types:
            if e:
                if eByNoStates:
                    tgg.plotEntropiesByNoStates(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, dmark['ini'], dmark['end'], 14)
                else:
                    tgg.plotEntropies(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, dmark['ini'], dmark['end'])
            if k:
                tgg.plotKLD(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, dmark['ini'], dmark['end'], kByNoStates)
            if l1:
                tgg.plotL1Metric(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, dmark['ini'], dmark['end'], l1ByNoStates)
            if km:
                tgg.plotKLDMetric(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, dmark['ini'], dmark['end'], kmByNoStates)
            if a:
                tgg.plotAutocorr(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, dmark['ini'], dmark['end'])
    
    def readConfigs(self):   
        f = open('config.json', 'r')
        configs = json.load(f)
        f.close()
        cTypes = configs['type']
        dmark = configs['dmark']
        mk1 = configs['mk1']
        mk2 = configs['mk2']
        L = configs['L']
        if L['multi']:
            L_ini = L['ini']
            L_fin = L['fin']
        else:
            L_ini = L_fin = L['single']
        alpha = configs['alpha']
        if alpha['multi']:
            alpha_ini = alpha['ini']
            alpha_fin = alpha['fin']
        else:
            alpha_ini = alpha_fin = alpha['single']
        types = [x for x in cTypes.keys() if cTypes[x] == True]
        return types, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin                                   
        
def main():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
