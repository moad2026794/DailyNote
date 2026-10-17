#!/usr/bin/env python3
"""يعدّل مشروع أندرويد الذي ينشئه Capacitor: الصلاحيات + أيقونة الإشعار."""
import pathlib, re, sys

root = pathlib.Path("android/app/src/main")
manifest = root / "AndroidManifest.xml"
if not manifest.exists():
    sys.exit("AndroidManifest.xml not found - did 'npx cap add android' run?")

text = manifest.read_text(encoding="utf-8")
perms = [
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.SCHEDULE_EXACT_ALARM",
    "android.permission.USE_EXACT_ALARM",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "android.permission.VIBRATE",
    "android.permission.WAKE_LOCK",
]
add = "".join(
    f'    <uses-permission android:name="{p}" />\n'
    for p in perms
    if p not in text
)
if add:
    text = re.sub(r"(\s*)<application", "\n" + add + r"\1<application", text, count=1)
manifest.write_text(text, encoding="utf-8")

# أيقونة الإشعار (جرس)
drawable = root / "res" / "drawable"
drawable.mkdir(parents=True, exist_ok=True)
(drawable / "ic_stat_icon_config_sample.xml").write_text(
    """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24">
  <path android:fillColor="#FFFFFFFF"
      android:pathData="M12,22c1.1,0 2,-0.9 2,-2h-4c0,1.1 0.9,2 2,2zM18,16v-5c0,-3.07 -1.63,-5.64 -4.5,-6.32V4c0,-0.83 -0.67,-1.5 -1.5,-1.5s-1.5,0.67 -1.5,1.5v0.68C7.64,5.36 6,7.92 6,11v5l-2,2v1h16v-1l-2,-2z"/>
</vector>
""",
    encoding="utf-8",
)
print("patched:", [p for p in perms])
