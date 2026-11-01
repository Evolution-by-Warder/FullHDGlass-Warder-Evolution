class fAzez(HTMLComponent, GUIComponent):

    def __init__(self, hIWLzKD=None, DTkMZWjfksusYP=None, OjuoZayNpvXj=120, cJDuPzBwJ=False):
        GUIComponent.__init__(self)
        self.l = eListboxPythonMultiContent()
        self.iKSEU = []
        self.HKxWrFqAZuPvj = 0
        self.LQjUmOZmPIjeC = 0
        self.HIUKuTtncR = None
        self.YoGIhzCiYcDA = None
        self.lYvKfeYm = None
        self.qqgzRbDCMIHzu = None
        self.vYLCDUlXdXha = None
        self.fXhRDlotxRaaApq = None
        self.DTkMZWjfksusYP = DTkMZWjfksusYP
        self.hhTZmF = time()
        if hIWLzKD is not None:
            self.iKSEU.append(hIWLzKD)
        self.Qqfnb = 50
        self.l.setBuildFunc(self.ZiGNvxobF)
        self.rSOMAOuiujeAG(cJDuPzBwJ)
        self.YHXJHM = eServiceCenter.getInstance()
        self.gyYjWuIgdYzdkTB = eEPGCache.getInstance()
        self.fxPPBoocO = ePicLoad()
        self.WKsQysaraX = 29
        self.wScHxPkcqaqNq = None
        self.YUHtPAXQxxbT = 0
        self.ULWIgmQmKjXByL = 16777215
        self.RvXhJbBKzCQpBmn = 0
        self.OuChfvEOnOYRWtZ = 16777215
        self.WjigOIYvJz = 0
        self.XqUptWUF = 16777215
        self.XsyRNaWcHMF = 2966878
        self.ITcoDz = 16777215
        self.nIkMGeICtFsxHt = 13587283
        self.bXFFKE = 16766976
        self.VWDYhRoQC = 10420224
        self.QbsADNDhDlAR = 33375
        self.fNKmwvD = 16777215
        self.xOfMVIvggqMID = 0
        self.klWPPb = 12632256
        self.ygBmGjCaJVg = 0
        self.KTJTIbtUJyi = 12632256
        self.FmLXAfR = 5335958
        self.AJCHjiyKFeubDoA = 16777215
        self.pwVpg = 16777215
        self.lrwMFzGG = None
        return
        return

    def rSOMAOuiujeAG(self, cJDuPzBwJ):
        if cJDuPzBwJ:
            self.l.setSelectableFunc(self.BxhoYESWacEOoJR)

    def ZiGNvxobF(self, IqrIaLhRyZcv, iwAZefm, events):
        try:
            TcqUNIQumjBr = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
            SxedwZ = TcqUNIQumjBr.toString()
            iKTxNkFRzSA = self.ANtzjtpk(eServiceReference(IqrIaLhRyZcv), eServiceReference(SxedwZ))
        except:
            iKTxNkFRzSA = 1
        bHxqjPOEXK = self.LeBQcwaTReuWiRb
        lMqxDyEMegTUWs = self.lYvKfeYm
        vTERCGMRZwb = self.ULWIgmQmKjXByL
        gIrEsKRp = self.RvXhJbBKzCQpBmn
        PVsmp = False
        vvUTc = self.vtOhhFwtL
        HLjfPn = [None]
        if self.Qqfnb <= 50:
            AldThCpUcp = 2
            if config.CTVG.C38.value:
                PVsmp = findCoolPicon(IqrIaLhRyZcv, iwAZefm)
            if PVsmp:
                cCNSY = MultiContentEntryPixmapAlphaBlend(pos=(bHxqjPOEXK.x, bHxqjPOEXK.y), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), png=loadPNG(PVsmp), backcolor=self.wScHxPkcqaqNq, backcolor_sel=0)
                wURAYRZd = list(cCNSY)
                wURAYRZd[8] = 4
                cCNSY = tuple(wURAYRZd)
                HLjfPn.append(cCNSY)
            elif not PVsmp and config.CTVG.C29.value != 'No':
                if self.fXhRDlotxRaaApq is not None:
                    if self.fXhRDlotxRaaApq.toString() == IqrIaLhRyZcv:
                        vvUTc = self.GmNmJ
                    else:
                        vvUTc = self.vtOhhFwtL
                HLjfPn.append(MultiContentEntryPixmapAlphaTest(pos=(bHxqjPOEXK.x + 1, bHxqjPOEXK.y + 1), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), png=vvUTc))
                HLjfPn.append(MultiContentEntryText(pos=(bHxqjPOEXK.x + 1, bHxqjPOEXK.y + 1), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=iwAZefm, color=self.XqUptWUF, border_width=1, border_color=self.ygBmGjCaJVg))
            else:
                HLjfPn.append(MultiContentEntryText(pos=(bHxqjPOEXK.x + 1, bHxqjPOEXK.y + 1), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=iwAZefm, color=self.XqUptWUF, border_width=1, border_color=self.KTJTIbtUJyi, backcolor=self.YUHtPAXQxxbT, backcolor_sel=self.FmLXAfR))
        elif self.Qqfnb > 50:
            AldThCpUcp = 1
            if config.CTVG.C37.value:
                PVsmp = findCoolPicon(IqrIaLhRyZcv, iwAZefm)
            if PVsmp:
                cCNSY = MultiContentEntryPixmapAlphaBlend(pos=(bHxqjPOEXK.x, bHxqjPOEXK.y), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), png=loadPNG(PVsmp), backcolor=self.wScHxPkcqaqNq, backcolor_sel=0)
                wURAYRZd = list(cCNSY)
                wURAYRZd[8] = 4
                cCNSY = tuple(wURAYRZd)
                HLjfPn.append(cCNSY)
            elif not PVsmp and config.CTVG.C29.value != 'No':
                if self.fXhRDlotxRaaApq is not None:
                    if self.fXhRDlotxRaaApq.toString() == IqrIaLhRyZcv:
                        vvUTc = self.GmNmJ
                    else:
                        vvUTc = self.vtOhhFwtL
                HLjfPn.append(MultiContentEntryPixmapAlphaTest(pos=(bHxqjPOEXK.x + 1, bHxqjPOEXK.y + 1), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), png=vvUTc))
                HLjfPn.append(MultiContentEntryText(pos=(bHxqjPOEXK.x + 1, bHxqjPOEXK.y + 1), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=iwAZefm, color=self.XqUptWUF, border_width=1, border_color=self.ygBmGjCaJVg))
            else:
                HLjfPn.append(MultiContentEntryText(pos=(bHxqjPOEXK.x + 1, bHxqjPOEXK.y + 1), size=(bHxqjPOEXK.w - 2, bHxqjPOEXK.h - 2), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=iwAZefm, color=self.XqUptWUF, border_width=1, border_color=self.KTJTIbtUJyi, backcolor=self.YUHtPAXQxxbT, backcolor_sel=self.FmLXAfR))
        if events:
            xuEQJ = self.HIUKuTtncR + self.HKxWrFqAZuPvj * config.CTVG.C44.value * 60
            GKhvupuNOqqKzk = xuEQJ + config.CTVG.C44.value * 60
            KjcslCZtFpSYhn = int(time())
            KLeUdchiAVv = lMqxDyEMegTUWs.x
            bxIfiTh = lMqxDyEMegTUWs.y
            XHMCU = lMqxDyEMegTUWs.w
            SiVMbhoHNhlMBpX = lMqxDyEMegTUWs.h
            HARPniflzAqg = None
            GAjnLPlQ = RT_HALIGN_LEFT | RT_VALIGN_CENTER
            YMrTyagd = '   '
            if self.Qqfnb > 40:
                if config.CTVG.C56.value:
                    GAjnLPlQ = RT_HALIGN_CENTER | RT_VALIGN_CENTER | RT_WRAP
                    YMrTyagd = ''
                else:
                    GAjnLPlQ = RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP
                    YMrTyagd = ''
            vmJEvBg = self.lrwMFzGG
            rOhOwnsOfrXlo = self.AJCHjiyKFeubDoA
            vTERCGMRZwb = self.pwVpg
            gIrEsKRp = self.WjigOIYvJz
            risOb = self.yUmvpTyfVpboUQ
            for HARPniflzAqg in events:
                IuxjcZEFCt = HARPniflzAqg[2]
                VZrihgm = HARPniflzAqg[3]
                SFYTvo, uhjuaQAyByUAwqw = self.tdFZINDIiyzUx(IuxjcZEFCt, VZrihgm, xuEQJ, GKhvupuNOqqKzk, XHMCU)
                wkaxoQpymhyYt = self.aIVrvgXXkshxzE(IqrIaLhRyZcv, IuxjcZEFCt, VZrihgm, HARPniflzAqg[0])
                if wkaxoQpymhyYt:
                    vmJEvBg = self.nIkMGeICtFsxHt
                    rOhOwnsOfrXlo = self.VWDYhRoQC
                    risOb = self.khOVCJjlEWtnj
                elif wkaxoQpymhyYt is False:
                    vmJEvBg = self.bXFFKE
                    rOhOwnsOfrXlo = self.bXFFKE
                    risOb = self.VuJemfthhYALMi
                elif not iKTxNkFRzSA and IuxjcZEFCt <= self.LQjUmOZmPIjeC and (IuxjcZEFCt + VZrihgm > KjcslCZtFpSYhn):
                    vmJEvBg = self.lrwMFzGG
                    rOhOwnsOfrXlo = self.AJCHjiyKFeubDoA
                    vTERCGMRZwb = self.pwVpg
                    gIrEsKRp = self.WjigOIYvJz
                    risOb = self.yUmvpTyfVpboUQ
                elif self.fXhRDlotxRaaApq is not None:
                    if self.fXhRDlotxRaaApq.toString() == IqrIaLhRyZcv:
                        vmJEvBg = self.FmLXAfR
                        rOhOwnsOfrXlo = self.AJCHjiyKFeubDoA
                        risOb = self.gYwsMLhtIoZLNTn
                    elif IuxjcZEFCt <= KjcslCZtFpSYhn and IuxjcZEFCt + VZrihgm > KjcslCZtFpSYhn:
                        vTERCGMRZwb = self.OuChfvEOnOYRWtZ
                        gIrEsKRp = self.WjigOIYvJz
                        vmJEvBg = self.QbsADNDhDlAR
                        rOhOwnsOfrXlo = self.fNKmwvD
                        risOb = self.dwkjjaLTcrvTF
                    else:
                        vmJEvBg = self.XsyRNaWcHMF
                        rOhOwnsOfrXlo = self.ITcoDz
                        risOb = self.zHGsNjqgOnBifL
                if config.CTVG.C29.value != 'No':
                    HLjfPn.append(MultiContentEntryPixmapAlphaTest(pos=(KLeUdchiAVv + SFYTvo, bxIfiTh), size=(uhjuaQAyByUAwqw, SiVMbhoHNhlMBpX), png=risOb, backcolor=vmJEvBg, backcolor_sel=rOhOwnsOfrXlo))
                    HLjfPn.append(MultiContentEntryText(pos=(KLeUdchiAVv + SFYTvo, bxIfiTh), size=(uhjuaQAyByUAwqw, SiVMbhoHNhlMBpX), font=AldThCpUcp, flags=GAjnLPlQ, text=YMrTyagd + HARPniflzAqg[1], color=vTERCGMRZwb, color_sel=gIrEsKRp, backcolor_sel=rOhOwnsOfrXlo, border_width=2, border_color=self.xOfMVIvggqMID))
                else:
                    HLjfPn.append(MultiContentEntryText(pos=(KLeUdchiAVv + SFYTvo, bxIfiTh), size=(uhjuaQAyByUAwqw, SiVMbhoHNhlMBpX), font=AldThCpUcp, flags=GAjnLPlQ, text=YMrTyagd + HARPniflzAqg[1], color=vTERCGMRZwb, color_sel=gIrEsKRp, backcolor=vmJEvBg, backcolor_sel=rOhOwnsOfrXlo, border_width=1, border_color=self.klWPPb))
        return HLjfPn
        return

    def tdFZINDIiyzUx(self, CeSogtSMHnaYAcJ, duration, start, Ende, width):
        SFYTvo = int((CeSogtSMHnaYAcJ - start) * width // (Ende - start))
        uhjuaQAyByUAwqw = int((CeSogtSMHnaYAcJ + duration - start) * width // (Ende - start) + 1)
        uhjuaQAyByUAwqw -= SFYTvo
        if SFYTvo < 0:
            uhjuaQAyByUAwqw += SFYTvo
            SFYTvo = 0
        if SFYTvo + uhjuaQAyByUAwqw > width:
            uhjuaQAyByUAwqw = width - SFYTvo
        return (SFYTvo, uhjuaQAyByUAwqw)

    def aIVrvgXXkshxzE(self, xrefstr, TtFJjgRfyVbpBW, duration, hoHTHNT):
        for blEDeARvcOLlhQw in self.DTkMZWjfksusYP.timer_list:
            if blEDeARvcOLlhQw.service_ref.ref.toString() == xrefstr:
                Ccrtvwst = TtFJjgRfyVbpBW + duration
                CSMFqyfTEMEICvu = blEDeARvcOLlhQw.begin
                GKhvupuNOqqKzk = blEDeARvcOLlhQw.end
                if self.LQjUmOZmPIjeC == 0 or self.LQjUmOZmPIjeC > GKhvupuNOqqKzk:
                    self.LQjUmOZmPIjeC = GKhvupuNOqqKzk
                BfRRiZXxxd = CSMFqyfTEMEICvu + int((GKhvupuNOqqKzk - CSMFqyfTEMEICvu) // 4)
                if blEDeARvcOLlhQw.eit == hoHTHNT:
                    if TtFJjgRfyVbpBW < CSMFqyfTEMEICvu or Ccrtvwst > GKhvupuNOqqKzk:
                        return False
                    else:
                        return True
                elif TtFJjgRfyVbpBW <= BfRRiZXxxd <= Ccrtvwst:
                    if TtFJjgRfyVbpBW < CSMFqyfTEMEICvu or Ccrtvwst > GKhvupuNOqqKzk:
                        return False
                    return True
        for blEDeARvcOLlhQw in self.DTkMZWjfksusYP.processed_timers:
            if blEDeARvcOLlhQw.disabled and blEDeARvcOLlhQw.service_ref.ref.toString() == xrefstr:
                if blEDeARvcOLlhQw.eit == hoHTHNT:
                    return False
