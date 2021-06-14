from unittest import TestCase
from classes.Aplication import *
from classes.AppClass import *


class SetUpClasses(TestCase):

    def setUp(self):
        self.app = App("/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF")
        self.appClasses = self.app.getClasses()
        dataClasses = ["/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/AelfCacheHelper.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/AelfDate.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/EpitreApi.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/Lecture.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/LecturesController.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/LectureVariants.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/Office.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/OfficeInformations.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/OfficeVariant.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/Validator.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/lectures/data/WhatWhen.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleBook.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleBookChapter.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleBookEntry.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleBookEntryType.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleBookList.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleController.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BiblePart.java",
                        "/Volumes/WanShiTong/Archive/UChile/Título/work/obfApps/AELF/co.epitre.aelf_lectures_69_src.tar.gz/app/src/main/java/co/epitre/aelf_lectures/bible/data/BibleVerse.java"]
        self.dataClasses = []
        for cls in dataClasses:
            self.dataClasses.append(AppClass(cls, self.app))


class test_dataClass_detection(SetUpClasses):

    def test_detection(self):
        print(self.appClasses[0].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[0].analyser.detectDataClass(), self.appClasses[0] in self.dataClasses)

    def test_detection1(self):
        print(self.appClasses[1].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[1].analyser.detectDataClass(), self.appClasses[1] in self.dataClasses)

    def test_detection2(self):
        print(self.appClasses[2].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[2].analyser.detectDataClass(), self.appClasses[2] in self.dataClasses)

    def test_detection3(self):
        print(self.appClasses[3].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[3].analyser.detectDataClass(), self.appClasses[3] in self.dataClasses)

    def test_detection4(self):
        print(self.appClasses[4].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[4].analyser.detectDataClass(), self.appClasses[4] in self.dataClasses)

    def test_detection5(self):
        print(self.appClasses[5].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[5].analyser.detectDataClass(), self.appClasses[5] in self.dataClasses)

    def test_detection6(self):
        print(self.appClasses[6].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[6].analyser.detectDataClass(), self.appClasses[6] in self.dataClasses)

    def test_detection7(self):
        print(self.appClasses[7].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[7].analyser.detectDataClass(), self.appClasses[7] in self.dataClasses)

    def test_detection8(self):
        print(self.appClasses[8].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[8].analyser.detectDataClass(), self.appClasses[8] in self.dataClasses)

    def test_detection9(self):
        print(self.appClasses[9].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[9].analyser.detectDataClass(), self.appClasses[9] in self.dataClasses)

    def test_detection10(self):
        print(self.appClasses[10].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[10].analyser.detectDataClass(), self.appClasses[10] in self.dataClasses)

    def test_detection11(self):
        print(self.appClasses[11].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[11].analyser.detectDataClass(), self.appClasses[11] in self.dataClasses)

    def test_detection12(self):
        print(self.appClasses[12].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[12].analyser.detectDataClass(), self.appClasses[12] in self.dataClasses)

    def test_detection13(self):
        print(self.appClasses[13].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[13].analyser.detectDataClass(), self.appClasses[13] in self.dataClasses)

    def test_detection14(self):
        print(self.appClasses[14].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[14].analyser.detectDataClass(), self.appClasses[14] in self.dataClasses)

    def test_detection15(self):
        print(self.appClasses[15].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[15].analyser.detectDataClass(), self.appClasses[15] in self.dataClasses)

    def test_detection16(self):
        print(self.appClasses[16].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[16].analyser.detectDataClass(), self.appClasses[16] in self.dataClasses)

    def test_detection17(self):
        print(self.appClasses[17].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[17].analyser.detectDataClass(), self.appClasses[17] in self.dataClasses)

    def test_detection18(self):
        print(self.appClasses[18].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[18].analyser.detectDataClass(), self.appClasses[18] in self.dataClasses)

    def test_detection19(self):
        print(self.appClasses[19].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[19].analyser.detectDataClass(), self.appClasses[19] in self.dataClasses)

    def test_detection20(self):
        print(self.appClasses[20].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[20].analyser.detectDataClass(), self.appClasses[20] in self.dataClasses)

    def test_detection21(self):
        print(self.appClasses[21].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[21].analyser.detectDataClass(), self.appClasses[21] in self.dataClasses)

    def test_detection22(self):
        print(self.appClasses[22].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[22].analyser.detectDataClass(), self.appClasses[22] in self.dataClasses)

    def test_detection23(self):
        print(self.appClasses[23].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[23].analyser.detectDataClass(), self.appClasses[23] in self.dataClasses)

    def test_detection24(self):
        print(self.appClasses[24].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[24].analyser.detectDataClass(), self.appClasses[24] in self.dataClasses)

    def test_detection25(self):
        print(self.appClasses[25].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[25].analyser.detectDataClass(), self.appClasses[25] in self.dataClasses)

    def test_detection26(self):
        print(self.appClasses[26].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[26].analyser.detectDataClass(), self.appClasses[26] in self.dataClasses)

    def test_detection27(self):
        print(self.appClasses[27].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[27].analyser.detectDataClass(), self.appClasses[27] in self.dataClasses)

    def test_detection28(self):
        print(self.appClasses[28].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[28].analyser.detectDataClass(), self.appClasses[28] in self.dataClasses)

    def test_detection29(self):
        print(self.appClasses[29].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[29].analyser.detectDataClass(), self.appClasses[29] in self.dataClasses)

    def test_detection30(self):
        print(self.appClasses[30].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[30].analyser.detectDataClass(), self.appClasses[30] in self.dataClasses)

    def test_detection31(self):
        print(self.appClasses[31].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[31].analyser.detectDataClass(), self.appClasses[31] in self.dataClasses)

    def test_detection32(self):
        print(self.appClasses[32].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[32].analyser.detectDataClass(), self.appClasses[32] in self.dataClasses)

    def test_detection33(self):
        print(self.appClasses[33].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[33].analyser.detectDataClass(), self.appClasses[33] in self.dataClasses)

    def test_detection34(self):
        print(self.appClasses[34].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[34].analyser.detectDataClass(), self.appClasses[34] in self.dataClasses)

    def test_detection35(self):
        print(self.appClasses[35].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[35].analyser.detectDataClass(), self.appClasses[35] in self.dataClasses)

    def test_detection36(self):
        print(self.appClasses[36].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[36].analyser.detectDataClass(), self.appClasses[36] in self.dataClasses)

    def test_detection37(self):
        print(self.appClasses[37].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[37].analyser.detectDataClass(), self.appClasses[37] in self.dataClasses)

    def test_detection38(self):
        print(self.appClasses[38].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[38].analyser.detectDataClass(), self.appClasses[38] in self.dataClasses)

    def test_detection39(self):
        print(self.appClasses[39].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[39].analyser.detectDataClass(), self.appClasses[39] in self.dataClasses)

    def test_detection40(self):
        print(self.appClasses[40].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[40].analyser.detectDataClass(), self.appClasses[40] in self.dataClasses)

    def test_detection41(self):
        print(self.appClasses[41].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[41].analyser.detectDataClass(), self.appClasses[41] in self.dataClasses)

    def test_detection42(self):
        print(self.appClasses[42].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[42].analyser.detectDataClass(), self.appClasses[42] in self.dataClasses)

    def test_detection43(self):
        print(self.appClasses[43].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[43].analyser.detectDataClass(), self.appClasses[43] in self.dataClasses)

    def test_detection44(self):
        print(self.appClasses[44].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[44].analyser.detectDataClass(), self.appClasses[44] in self.dataClasses)

    def test_detection45(self):
        print(self.appClasses[45].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[45].analyser.detectDataClass(), self.appClasses[45] in self.dataClasses)

    def test_detection46(self):
        print(self.appClasses[46].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[46].analyser.detectDataClass(), self.appClasses[46] in self.dataClasses)

    def test_detection47(self):
        print(self.appClasses[47].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[47].analyser.detectDataClass(), self.appClasses[47] in self.dataClasses)

    def test_detection48(self):
        print(self.appClasses[48].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[48].analyser.detectDataClass(), self.appClasses[48] in self.dataClasses)

    def test_detection49(self):
        print(self.appClasses[49].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[49].analyser.detectDataClass(), self.appClasses[49] in self.dataClasses)

    def test_detection50(self):
        print(self.appClasses[50].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[50].analyser.detectDataClass(), self.appClasses[50] in self.dataClasses)

    def test_detection51(self):
        print(self.appClasses[51].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[51].analyser.detectDataClass(), self.appClasses[51] in self.dataClasses)

    def test_detection52(self):
        print(self.appClasses[52].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[52].analyser.detectDataClass(), self.appClasses[52] in self.dataClasses)

    def test_detection53(self):
        print(self.appClasses[53].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[53].analyser.detectDataClass(), self.appClasses[53] in self.dataClasses)

    def test_detection54(self):
        print(self.appClasses[54].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[54].analyser.detectDataClass(), self.appClasses[54] in self.dataClasses)

    def test_detection55(self):
        print(self.appClasses[55].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[55].analyser.detectDataClass(), self.appClasses[55] in self.dataClasses)

    def test_detection56(self):
        print(self.appClasses[56].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[56].analyser.detectDataClass(), self.appClasses[56] in self.dataClasses)

    def test_detection57(self):
        print(self.appClasses[57].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[57].analyser.detectDataClass(), self.appClasses[57] in self.dataClasses)

    def test_detection58(self):
        print(self.appClasses[58].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[58].analyser.detectDataClass(), self.appClasses[58] in self.dataClasses)

    def test_detection59(self):
        print(self.appClasses[59].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[59].analyser.detectDataClass(), self.appClasses[59] in self.dataClasses)

    def test_detection60(self):
        print(self.appClasses[60].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[60].analyser.detectDataClass(), self.appClasses[60] in self.dataClasses)

    def test_detection61(self):
        print(self.appClasses[61].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[61].analyser.detectDataClass(), self.appClasses[61] in self.dataClasses)

    def test_detection62(self):
        print(self.appClasses[62].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[62].analyser.detectDataClass(), self.appClasses[62] in self.dataClasses)

    def test_detection63(self):
        print(self.appClasses[63].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[63].analyser.detectDataClass(), self.appClasses[63] in self.dataClasses)

    def test_detection64(self):
        print(self.appClasses[64].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[64].analyser.detectDataClass(), self.appClasses[64] in self.dataClasses)

    def test_detection65(self):
        print(self.appClasses[65].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[65].analyser.detectDataClass(), self.appClasses[65] in self.dataClasses)

    def test_detection66(self):
        print(self.appClasses[66].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[66].analyser.detectDataClass(), self.appClasses[66] in self.dataClasses)

    def test_detection67(self):
        print(self.appClasses[67].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[67].analyser.detectDataClass(), self.appClasses[67] in self.dataClasses)

    def test_detection68(self):
        print(self.appClasses[68].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[68].analyser.detectDataClass(), self.appClasses[68] in self.dataClasses)

    def test_detection69(self):
        print(self.appClasses[69].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[69].analyser.detectDataClass(), self.appClasses[69] in self.dataClasses)

    def test_detection70(self):
        print(self.appClasses[70].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[70].analyser.detectDataClass(), self.appClasses[70] in self.dataClasses)

    def test_detection71(self):
        print(self.appClasses[71].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[71].analyser.detectDataClass(), self.appClasses[71] in self.dataClasses)

    def test_detection72(self):
        print(self.appClasses[72].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[72].analyser.detectDataClass(), self.appClasses[72] in self.dataClasses)

    def test_detection73(self):
        print(self.appClasses[73].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[73].analyser.detectDataClass(), self.appClasses[73] in self.dataClasses)

    def test_detection74(self):
        print(self.appClasses[74].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[74].analyser.detectDataClass(), self.appClasses[74] in self.dataClasses)

    def test_detection75(self):
        print(self.appClasses[75].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[75].analyser.detectDataClass(), self.appClasses[75] in self.dataClasses)

    def test_detection76(self):
        print(self.appClasses[76].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[76].analyser.detectDataClass(), self.appClasses[76] in self.dataClasses)

    def test_detection77(self):
        print(self.appClasses[77].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[77].analyser.detectDataClass(), self.appClasses[77] in self.dataClasses)

    def test_detection78(self):
        print(self.appClasses[78].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[78].analyser.detectDataClass(), self.appClasses[78] in self.dataClasses)

    def test_detection79(self):
        print(self.appClasses[79].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[79].analyser.detectDataClass(), self.appClasses[79] in self.dataClasses)

    def test_detection80(self):
        print(self.appClasses[80].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[80].analyser.detectDataClass(), self.appClasses[80] in self.dataClasses)

    def test_detection81(self):
        print(self.appClasses[81].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[81].analyser.detectDataClass(), self.appClasses[81] in self.dataClasses)

    def test_detection82(self):
        print(self.appClasses[82].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[82].analyser.detectDataClass(), self.appClasses[82] in self.dataClasses)

    def test_detection83(self):
        print(self.appClasses[83].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[83].analyser.detectDataClass(), self.appClasses[83] in self.dataClasses)

    def test_detection84(self):
        print(self.appClasses[84].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[84].analyser.detectDataClass(), self.appClasses[84] in self.dataClasses)

    def test_detection85(self):
        print(self.appClasses[85].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[85].analyser.detectDataClass(), self.appClasses[85] in self.dataClasses)

    def test_detection86(self):
        print(self.appClasses[86].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[86].analyser.detectDataClass(), self.appClasses[86] in self.dataClasses)

    def test_detection87(self):
        print(self.appClasses[87].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[87].analyser.detectDataClass(), self.appClasses[87] in self.dataClasses)

    def test_detection88(self):
        print(self.appClasses[88].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[88].analyser.detectDataClass(), self.appClasses[88] in self.dataClasses)

    def test_detection89(self):
        print(self.appClasses[89].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[89].analyser.detectDataClass(), self.appClasses[89] in self.dataClasses)

    def test_detection90(self):
        print(self.appClasses[90].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[90].analyser.detectDataClass(), self.appClasses[90] in self.dataClasses)

    def test_detection91(self):
        print(self.appClasses[91].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[91].analyser.detectDataClass(), self.appClasses[91] in self.dataClasses)

    def test_detection92(self):
        print(self.appClasses[92].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[92].analyser.detectDataClass(), self.appClasses[92] in self.dataClasses)

    def test_detection93(self):
        print(self.appClasses[93].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[93].analyser.detectDataClass(), self.appClasses[93] in self.dataClasses)

    def test_detection94(self):
        print(self.appClasses[94].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[94].analyser.detectDataClass(), self.appClasses[94] in self.dataClasses)

    def test_detection95(self):
        print(self.appClasses[95].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[95].analyser.detectDataClass(), self.appClasses[95] in self.dataClasses)

    def test_detection96(self):
        print(self.appClasses[96].path.split('obfApps/')[1])
        self.assertEqual(self.appClasses[96].analyser.detectDataClass(), self.appClasses[96] in self.dataClasses)
