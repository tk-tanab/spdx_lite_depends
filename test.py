# def next_iter(any_iter):
#     for b in any_iter:
#         print("in next_iter", b)
#         if b == 4:
#             break

# alist = [1,2,3,4,5,6]
# alist_iter = iter(alist)

# for a in alist_iter:
#     next_iter(alist_iter)
#     print(a)
import os
import glob
os.chdir(os.path.dirname(__file__))
deb_files = glob.glob("./package_for_analyze/*.deb")


print(deb_files)