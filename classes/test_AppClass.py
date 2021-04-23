from unittest import TestCase
from classes.Aplication import *


class SetUpApp(TestCase):

    def setUp(self):
        self.obApp1 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/SimpleFileManagerPro")
        self.obApp2 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/SimpleExplorer")
        self.obApp3 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/")
        self.obApp4 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/BatteryFu")

        self.unObApp1 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/CardGameScores")
        self.unObApp2 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/LocalGsmNlpBackend")
        self.unObApp3 = App("/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/TheItalianSaid")


class TestApp(SetUpApp):

    def test_isObfuscated(self):
        self.assertEqual(self.obApp1.isObfuscated(), True)
        self.assertEqual(self.obApp2.isObfuscated(), True)
        self.assertEqual(self.obApp3.isObfuscated(), True)
        self.assertEqual(self.obApp4.isObfuscated(), True)

        self.assertEqual(self.unObApp1.isObfuscated(), False)
        self.assertEqual(self.unObApp2.isObfuscated(), False)
        self.assertEqual(self.unObApp3.isObfuscated(), False)

    def test_classes(self):
        classes = []
        for cls in self.obApp1.classes:
            classes.append(cls.name)

        expected = ["App.kt", "FavoritesActivity.kt", "MainActivity.kt", "ReadTextActivity.kt", "SettingsActivity.kt",
                    "SimpleActivity.kt", "SplashActivity.kt", "ItemsAdapter.kt", "ManageFavoritesAdapter.kt",
                    "ChangeSortingDialog.kt", "CompressAsDialog.kt", "CreateNewItemDialog.kt", "SaveAsDialog.kt",
                    "Activity.kt", "Context.kt", "String.kt", "ItemsFragment.kt", "Config.kt", "Constants.kt",
                    "RootHelpers.kt", "ItemOperationsListener.kt", "ListItem.kt", "GestureEditText.kt"]

        self.assertEqual(classes, expected)

    def test_proguardRuleFiles(self):
        files = []
        for pg in self.obApp2.proguardRuleFiles:
            files.append(pg.path)
        expected = [
            "/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/SimpleExplorer/com.dnielfe.manager_67_src.tar.gz/explorer/proguard-android.txt"]

        self.assertEqual(files, expected)

        files2 = []
        for pg in self.obApp3.proguardRuleFiles:
            files2.append(pg.path)
        expected2 = ['/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/app/proguard-rules.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/commonproviders/proguard-rules.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/data/proguard-rules.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/domain/proguard-rules.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/network/proguard-rules.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/workers/proguard-rules.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/app/proguard-rules/coroutines.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/app/proguard-rules/moshi-kotlin.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/app/proguard-rules/moshi.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/app/proguard-rules/okhttp3.pro',
 '/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/GameDealz/de.r4md4c.gamedealz_14_src.tar.gz/app/proguard-rules/okio.pro']

        self.assertEqual(files2, expected2)

    def test_descriptorFiles(self):
        gradlePath = self.obApp1.buildGradleFiles
        prpertiesPath = self.obApp1.propertiesPaths

        gradleExpected = [
            "/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/SimpleFileManagerPro/com.simplemobiletools.filemanager.pro_90_src.tar.gz/build.gradle",
            "/Volumes/WanShiTong/Archive/UChile/Título/work/fdroidapps/SimpleFileManagerPro/com.simplemobiletools.filemanager.pro_90_src.tar.gz/app/build.gradle"]
        propertiesExpected = []

        self.assertEqual(gradlePath, gradleExpected)
        self.assertEqual(prpertiesPath, propertiesExpected)


class TestAppClass(SetUpApp):

    def test_findImports(self):
        cls = self.obApp1.classes[0].imports
        expected = ["android.app.Application",
                    "com.github.ajalt.reprint.core.Reprint",
                    "com.simplemobiletools.commons.extensions.checkUseEnglish"]

        self.assertEqual(cls, expected)


class TestProGuard(SetUpApp):

    def test_findFileRules(self):
        rules = self.obApp1.proguardRuleFiles[0].rules.rules
        expected = ["dontnote android.net.http.* ", "dontnote org.apache.http.** ",
                    "keep class com.simplemobiletools.** { *; } ",
                    "dontwarn com.simplemobiletools.**"]

        rules2 = self.obApp3.proguardRuleFiles[0].rules.rules
        expected2 = ["keepclassmembers class * extends androidx.lifecycle.ViewModel { <init>(...); } ",
                     "keep class androidx.appcompat.graphics.** { *; }"]
        self.assertEqual(rules, expected)
        self.assertEqual(rules2, expected2)
