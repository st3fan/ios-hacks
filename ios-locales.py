#!/usr/bin/env python3

#
# HACK HACK HACK / MAY STOP WORKING  / MAY NOT WORK / HORRIBLE CODE
#
# ios-locales.py
#
#  Stefan Arentz, February 2017
#
#  This scripts scans simulator runtimes and xcode installations and builds up a list
#  of supported locales per iOS version. It outputs the list in a HTML table.
#
#  Results up to 10.3b1 at https://people-mozilla.org/~sarentz/ios-locales.html
#
# HACK HACK HACK / MAY STOP WORKING / MAY NOT WORK / HORRIBLE CODE
#

import glob, os.path, plistlib, re, sys

XCODES = [
    "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform",
    "/Applications/Xcode-beta.app/Contents/Developer/Platforms/iPhoneSimulator.platform",
 ]

RUNTIMES="/Library/Developer/CoreSimulator/Profiles/Runtimes"

DEFAULT_LANGUAGE_ORDER="/System/Library/Frameworks/Foundation.framework/en.lproj/DefaultLanguageOrder-iOS.plist"

# Taken from http://stackoverflow.com/a/4836734
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def ios_runtimes():
    if os.path.exists(RUNTIMES):
        for path in glob.glob("%s/*.simruntime" % RUNTIMES):
            if "iOS 8." not in path:
                yield (os.path.splitext(os.path.basename(path))[0], path)
    for xcode_path in XCODES:
        if os.path.exists(xcode_path):
            for path in glob.glob("%s/Developer/Library/CoreSimulator/Profiles/Runtimes/*.simruntime" % xcode_path):
                yield (os.path.splitext(os.path.basename(path))[0], path)

def runtime_root(simruntime_path):
    if simruntime_path.startswith(RUNTIMES):
        return simruntime_path + "/Contents/Resources/RuntimeRoot"
    else:
        return simruntime_path + "/../../../../../SDKs/iPhoneSimulator.sdk"


def locales1_for_runtime(rt_path):
    with open(runtime_root(rt_path) + "/System/Library/Frameworks/Foundation.framework/en.lproj/DefaultLanguageOrder-iOS.plist", "rb") as fp:
        plist = plistlib.load(fp)
        return plist

def locales2_for_runtime(rt_path):
    with open(runtime_root(rt_path) + "/System/Library/PrivateFrameworks/IntlPreferences.framework/ISOLanguageCharSet.strings", "rb") as fp:
        plist = plistlib.load(fp)
        return plist.keys()

if __name__ == "__main__":

    #for rt in ios_runtimes():
    #    print(rt)
    #    print("    " + runtime_root(rt[1]))
    #sys.exit(0)

    # Tier 1

    locales1_per_runtime = dict()
    all_locales1 = set()
    for rt in ios_runtimes():
        rt_version, rt_path = rt
        locales1_per_runtime[rt_version] = locales1_for_runtime(rt_path)
        for locale in locales1_per_runtime[rt_version]:
            all_locales1.add(locale)

    print("<h1>iOS Locales</h1>")
    print("<p><i>Stefan Arentz, February 2017</i></p>")
    print('<p>Generated with <a href="https://github.com/st3fan/ios-hacks/blob/master/ios-locales.py">github.com/st3fan/ios-hacks/ios-locales.py</a></p>')

    print("<h2>iOS Tier-1 Locales (%d)</h2>" % len(all_locales1))
    print("<table width='75%'>")
    print("<tr>")
    print("<td></td>")
    for runtime_version in natural_sort(locales1_per_runtime.keys()):
        print("<td>%s</td>" % runtime_version)
    print("</tr>")
    for locale in sorted(all_locales1):
        print("<tr>")
        print("<td>%s</td>" % locale)
        for runtime_version in locales1_per_runtime.keys():
            if locale in natural_sort(locales1_per_runtime[runtime_version]):
                print("<td>%s</td>" % locale)
            else:
                print("<td>-</td>")
        print("</tr>")
    print("</table>")

    # Tier 2

    locales_per_runtime = dict()
    all_locales = set()
    for rt in ios_runtimes():
        rt_version, rt_path = rt
        locales_per_runtime[rt_version] = locales2_for_runtime(rt_path)
        for locale in locales_per_runtime[rt_version]:
            all_locales.add(locale)

    print("<h2>iOS Tier-2 Locales (%d)</h2>" % len(all_locales))
    print("<table width='75%'>")
    print("<tr>")
    print("<td></td>")
    for runtime_version in natural_sort(locales_per_runtime.keys()):
        print("<td>%s</td>" % runtime_version)
    print("</tr>")
    for locale in sorted(all_locales):
        print("<tr>")
        print("<td>%s</td>" % locale)
        for runtime_version in natural_sort(locales_per_runtime.keys()):
            if locale in locales_per_runtime[runtime_version]:
                print("<td>%s</td>" % locale)
            else:
                print("<td>-</td>")
        print("</tr>")
    print("</table>")

