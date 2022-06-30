import bsdiff4
import hashlib
import os


def get_file_md5(file_path):
  md5 = None
  if os.path.isfile(file_path):
    f = open(file_path,'rb')
    md5_obj = hashlib.md5()
    md5_obj.update(f.read())
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
  return md5

old_apk = '/Users/afirez/Desktop/old.apk'
new_apk = '/Users/afirez/Desktop/new.apk'
patch = '/Users/afirez/Desktop/patch.patch'

gen_apk = '/Users/afirez/Desktop/gen.apk'

# 将 old_apk 与 new_apk 生成差异包， 输出到 patch
# bsdiff4.file_diff(old_apk, new_apk, patch)

# 将 old_apk 与 patch 合成， 输出到 gen_apk
bsdiff4.file_patch(old_apk, gen_apk, patch)

old_md5 = get_file_md5(old_apk)
new_md5 = get_file_md5(new_apk)

patch_md5 = get_file_md5(patch)
gen_md5 = get_file_md5(gen_apk)

print("old_md5 " + old_md5)
print("new_md5 " + new_md5)

print("patch_md5 " + patch_md5)
print("gen_md5 " + gen_md5)

if gen_md5 == new_md5:
  print("gen apk success")
else:
  print("gen apk failed")

