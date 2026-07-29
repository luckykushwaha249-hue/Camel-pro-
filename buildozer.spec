[app]
title = Camel Pro
package.name = camelpro
package.domain = com.camelpro.learning
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

android.minapi = 26
android.api = 34
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
