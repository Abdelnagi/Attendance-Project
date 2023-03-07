[app]

# (str) Title of your application
title = My App
version = 1.0
# (str) Package name
package.name = com.example.myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.myorg.myapp

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = kivy, pillow

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer

# (str) Path to the Python for android distribution to use
# Update this to the path of your Android SDK installation
android.sdk_path = /path/to/android/sdk

# (str) Path to the NDK directory
android.ndk_path = /path/to/android/ndk

# (str) Path to the Java JDK directory
android.jdk_path = /path/to/java/jdk

# (list) Permissions
android.permissions = INTERNET

# (str) Android API to use
android.api = 28

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 28

# (str) Android NDK version to use
android.ndk = 21.4.7075529

# (str) Android NDK version to use
android.gradle_version = 4.1.0

# (list) Android add-ons to use
android.addons = addon-google_apis-google-24

# (str) Android architecture
android.arch = armeabi-v7a

# (bool) Build with p4a instead of python-for-android
use_p4a = False
