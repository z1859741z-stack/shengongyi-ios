#!/usr/bin/env python3
"""生成 Shengongyi.xcodeproj（最小 WKWebView 壳：App.swift + index.html + LaunchScreen）。
用法：python3 tools/gen_project.py（在仓库根目录运行）。UUID 按路径确定性生成。"""
import os
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT, "Shengongyi")
PROJ_DIR = os.path.join(ROOT, "Shengongyi.xcodeproj")
SCHEME_DIR = os.path.join(PROJ_DIR, "xcshareddata", "xcschemes")

TARGET_NAME = "Shengongyi"
BUNDLE_ID = "com.z1859741z.shengongyi"


def uid(key: str) -> str:
    return uuid.uuid5(uuid.NAMESPACE_URL, "shengongyi-ios:" + key).hex[:24].upper()


FILES = {
    "App.swift": ("sourcecode.swift", "Shengongyi/App.swift"),
    "index.html": ("text.html", "Shengongyi/index.html"),
    "LaunchScreen.storyboard": ("file.storyboard", "Shengongyi/LaunchScreen.storyboard"),
    "Info.plist": ("text.plist.xml", "Shengongyi/Info.plist"),
}

ids = {}
for name in FILES:
    ids["buildfile:" + name] = uid("buildfile:" + name)
    ids["fileref:" + name] = uid("fileref:" + name)
ids["fileref:WebKit.framework"] = uid("fileref:WebKit.framework")
ids["buildfile:WebKit.framework"] = uid("buildfile:WebKit.framework")
ids["fileref:product"] = uid("fileref:product")
for key in ["sources-phase", "frameworks-phase", "resources-phase",
            "target", "project", "group-main", "group-app", "group-products",
            "configlist-project", "configlist-target",
            "config-project-debug", "config-project-release",
            "config-target-debug", "config-target-release"]:
    ids[key] = uid(key)

TARGET_UID = ids["target"]


def main():
    os.makedirs(SCHEME_DIR, exist_ok=True)
    pbx = """// !$*UTF8*$!
{
\tarchiveVersion = 1;
\tclasses = {
\t};
\tobjectVersion = 77;
\tobjects = {
"""
    # PBXBuildFile
    for name, (ftype, _path) in FILES.items():
        if name == "Info.plist":
            continue
        pbx += f"\t\t{ids['buildfile:' + name]} /* {name} in {'Sources' if name == 'App.swift' else 'Resources'} */ = {{isa = PBXBuildFile; fileRef = {ids['fileref:' + name]} /* {name} */; }};\n"
    pbx += f"\t\t{ids['buildfile:WebKit.framework']} /* WebKit.framework in Frameworks */ = {{isa = PBXBuildFile; fileRef = {ids['fileref:WebKit.framework']} /* WebKit.framework */; }};\n"
    # PBXFileReference
    for name, (ftype, path) in FILES.items():
        pbx += f"\t\t{ids['fileref:' + name]} /* {name} */ = {{isa = PBXFileReference; lastKnownFileType = {ftype}; path = {name}; sourceTree = \"<group>\"; }};\n"
    pbx += f"\t\t{ids['fileref:WebKit.framework']} /* WebKit.framework */ = {{isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = WebKit.framework; path = System/Library/Frameworks/WebKit.framework; sourceTree = SDKROOT; }};\n"
    pbx += f"\t\t{ids['fileref:product']} /* Shengongyi.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = Shengongyi.app; sourceTree = BUILT_PRODUCTS_DIR; }};\n"
    # Phases
    pbx += f"""\t\t{ids['sources-phase']} /* Sources */ = {{isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = (
\t\t\t{ids['buildfile:App.swift']} /* App.swift in Sources */,
\t\t); runOnlyForDeploymentPostprocessing = 0; }};
\t\t{ids['frameworks-phase']} /* Frameworks */ = {{isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (
\t\t\t{ids['buildfile:WebKit.framework']} /* WebKit.framework in Frameworks */,
\t\t); runOnlyForDeploymentPostprocessing = 0; }};
\t\t{ids['resources-phase']} /* Resources */ = {{isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (
\t\t\t{ids['buildfile:index.html']} /* index.html in Resources */,
\t\t\t{ids['buildfile:LaunchScreen.storyboard']} /* LaunchScreen.storyboard in Resources */,
\t\t); runOnlyForDeploymentPostprocessing = 0; }};
"""
    # Groups
    pbx += f"""\t\t{ids['group-app']} /* Shengongyi */ = {{isa = PBXGroup; children = (
\t\t\t{ids['fileref:App.swift']} /* App.swift */,
\t\t\t{ids['fileref:index.html']} /* index.html */,
\t\t\t{ids['fileref:Info.plist']} /* Info.plist */,
\t\t\t{ids['fileref:LaunchScreen.storyboard']} /* LaunchScreen.storyboard */,
\t\t); path = Shengongyi; sourceTree = "<group>"; }};
\t\t{ids['group-main']} = {{isa = PBXGroup; children = (
\t\t\t{ids['group-app']} /* Shengongyi */,
\t\t\t{ids['group-products']} /* Products */,
\t\t); sourceTree = "<group>"; }};
\t\t{ids['group-products']} /* Products */ = {{isa = PBXGroup; children = (
\t\t\t{ids['fileref:product']} /* Shengongyi.app */,
\t\t); name = Products; sourceTree = "<group>"; }};
"""
    # Target
    pbx += f"""\t\t{TARGET_UID} /* Shengongyi */ = {{isa = PBXNativeTarget; buildConfigurationList = {ids['configlist-target']} /* Build configuration list for PBXNativeTarget "Shengongyi" */; buildPhases = (
\t\t\t{ids['sources-phase']} /* Sources */,
\t\t\t{ids['frameworks-phase']} /* Frameworks */,
\t\t\t{ids['resources-phase']} /* Resources */,
\t\t); buildRules = (
\t\t); dependencies = (
\t\t); name = Shengongyi; productName = Shengongyi; productReference = {ids['fileref:product']} /* Shengongyi.app */; productType = "com.apple.product-type.application"; }};
"""
    # Project
    pbx += f"""\t\t{ids['project']} /* Project object */ = {{isa = PBXProject; attributes = {{
\t\t\tLastUpgradeCheck = 2600;
\t\t\tTargetAttributes = {{
\t\t\t\t{TARGET_UID} = {{
\t\t\t\t\tCreatedOnToolsVersion = 26.0;
\t\t\t\t}};
\t\t\t}};
\t\t}}; buildConfigurationList = {ids['configlist-project']} /* Build configuration list for PBXProject "Shengongyi" */; compatibilityVersion = "Xcode 14.0"; developmentRegion = zh_CN; hasScannedForEncodings = 0; knownRegions = (
\t\t\ten,
\t\t\tBase,
\t\t\tzh_CN,
\t\t); mainGroup = {ids['group-main']}; productRefGroup = {ids['group-products']} /* Products */; projectDirPath = ""; projectRoot = ""; targets = (
\t\t\t{TARGET_UID} /* Shengongyi */,
\t\t); }};
"""
    # Configurations
    def target_settings():
        return """{
\t\t\t\tCODE_SIGN_IDENTITY = "";
\t\t\t\tCODE_SIGN_STYLE = Automatic;
\t\t\t\tCODE_SIGNING_ALLOWED = NO;
\t\t\t\tCODE_SIGNING_REQUIRED = NO;
\t\t\t\tCURRENT_PROJECT_VERSION = 1;
\t\t\t\tGENERATE_INFOPLIST_FILE = NO;
\t\t\t\tINFOPLIST_FILE = Shengongyi/Info.plist;
\t\t\t\tIPHONEOS_DEPLOYMENT_TARGET = 16.0;
\t\t\t\tLD_RUNPATH_SEARCH_PATHS = (
\t\t\t\t\t"$(inherited)",
\t\t\t\t\t"@executable_path/Frameworks",
\t\t\t\t);
\t\t\t\tMARKETING_VERSION = 1.0;
\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = com.z1859741z.shengongyi;
\t\t\t\tPRODUCT_NAME = "$(TARGET_NAME)";
\t\t\t\tSDKROOT = iphoneos;
\t\t\t\tSWIFT_EMBED_LIBRARIES_WITH_INSTALL = YES;
\t\t\t\tSWIFT_VERSION = 5.0;
\t\t\t\tTARGETED_DEVICE_FAMILY = 1;
\t\t\t}"""
    for key, name, settings in [
        ("config-project-debug", "Debug", "{\n\t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;\n\t\t\t\tCLANG_ANALYZER_NONNULL = YES;\n\t\t\t\tDEBUG_INFORMATION_FORMAT = dwarf;\n\t\t\t\tGCC_DYNAMIC_NO_PIC = NO;\n\t\t\t\tGCC_OPTIMIZATION_LEVEL = 0;\n\t\t\t\tGCC_PREPROCESSOR_DEFINITIONS = (\n\t\t\t\t\t\"DEBUG=1\",\n\t\t\t\t\t\"$(inherited)\",\n\t\t\t\t);\n\t\t\t\tSWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;\n\t\t\t\tSWIFT_OPTIMIZATION_LEVEL = \"-Onone\";\n\t\t\t}"),
        ("config-project-release", "Release", "{\n\t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;\n\t\t\t\tCLANG_ANALYZER_NONNULL = YES;\n\t\t\t\tDEBUG_INFORMATION_FORMAT = \"dwarf-with-dsym\";\n\t\t\t\tGCC_OPTIMIZATION_LEVEL = s;\n\t\t\t\tSWIFT_OPTIMIZATION_LEVEL = \"-O\";\n\t\t\t}"),
        ("config-target-debug", "Debug", target_settings()),
        ("config-target-release", "Release", target_settings()),
    ]:
        pbx += f"\t\t{ids[key]} /* {name} */ = {{isa = XCBuildConfiguration; buildSettings = {settings}; name = {name}; }};\n"
    pbx += f"""\t\t{ids['configlist-project']} /* Build configuration list for PBXProject "Shengongyi" */ = {{isa = XCConfigurationList; buildConfigurations = (
\t\t\t{ids['config-project-debug']} /* Debug */,
\t\t\t{ids['config-project-release']} /* Release */,
\t\t); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; }};
\t\t{ids['configlist-target']} /* Build configuration list for PBXNativeTarget "Shengongyi" */ = {{isa = XCConfigurationList; buildConfigurations = (
\t\t\t{ids['config-target-debug']} /* Debug */,
\t\t\t{ids['config-target-release']} /* Release */,
\t\t); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; }};
\t}};
\trootObject = {ids['project']} /* Project object */;
}}
"""
    os.makedirs(PROJ_DIR, exist_ok=True)
    with open(os.path.join(PROJ_DIR, "project.pbxproj"), "w", encoding="utf-8") as f:
        f.write(pbx)

    scheme = f"""<?xml version="1.0" encoding="UTF-8"?>
<Scheme
   LastUpgradeVersion = "2600"
   version = "1.7">
   <BuildAction
      parallelizeBuildables = "YES"
      buildImplicitDependencies = "YES"
      buildArchitectures = "Automatic">
      <BuildActionEntries>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{TARGET_UID}"
               BuildableName = "Shengongyi.app"
               BlueprintName = "Shengongyi"
               ReferencedContainer = "container:Shengongyi.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
   <TestAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.Debugger.Foundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.Debugger.Foundation.Launcher.LLDB"
      shouldUseLaunchSchemeArgsEnv = "YES"
      shouldAutocreateTestPlan = "YES">
   </TestAction>
   <LaunchAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.Debugger.Foundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.Debugger.Foundation.Launcher.LLDB"
      launchStyle = "0"
      useCustomWorkingDirectory = "NO"
      ignoresPersistentStateOnLaunch = "NO"
      debugDocumentVersioning = "YES"
      debugServiceExtension = "internal"
      allowLocationSimulation = "YES">
   </LaunchAction>
   <ProfileAction
      buildConfiguration = "Release"
      shouldUseLaunchSchemeArgsEnv = "YES"
      savedToolIdentifier = ""
      useCustomWorkingDirectory = "NO"
      debugDocumentVersioning = "YES">
   </ProfileAction>
   <AnalyzeAction
      buildConfiguration = "Debug">
   </AnalyzeAction>
   <ArchiveAction
      buildConfiguration = "Release"
      revealArchiveInOrganizer = "YES">
   </ArchiveAction>
</Scheme>
"""
    with open(os.path.join(SCHEME_DIR, "Shengongyi.xcscheme"), "w", encoding="utf-8") as f:
        f.write(scheme)
    print("wrote", os.path.join(PROJ_DIR, "project.pbxproj"))
    print("target UID:", TARGET_UID)


if __name__ == "__main__":
    main()
