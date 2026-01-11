import os
from setuptools import setup, Extension
from Cython.Build import cythonize

# ---------------------------------------------------------
# CẤU HÌNH CHO DỰ ÁN TOOL_ADMIN
# ---------------------------------------------------------

# 1. Danh sách thư mục cần mã hóa
# Dựa trên ảnh của bạn, chỉ có thư mục 'helpers' là cần bảo vệ
target_folders = ["helpers"]

extensions = []

print("🚀 Đang quét file để mã hóa...")

for folder in target_folders:
    # Kiểm tra thư mục có tồn tại không
    if not os.path.exists(folder):
        print(f"⚠️  Không tìm thấy thư mục: {folder}")
        continue

    # Duyệt tất cả file trong thư mục
    for filename in os.listdir(folder):
        # Chỉ lấy file .py, bỏ qua __init__.py và các file khác
        if filename.endswith(".py") and filename != "__init__.py":
            
            # Đường dẫn file gốc: helpers/path_manager.py
            filepath = os.path.join(folder, filename)
            
            # Tên module cho Cython: helpers.path_manager
            module_name = filepath.replace(os.path.sep, ".").replace(".py", "")
            
            print(f"   -> Đã thêm: {filepath}")
            extensions.append(Extension(module_name, [filepath]))

# 2. Thực hiện Build
if extensions:
    setup(
        ext_modules=cythonize(
            extensions,
            compiler_directives={'language_level': "3"}, # Python 3
            build_dir="build_temp" # Thư mục chứa file tạm .c
        )
    )
    print("\n✅ Build thành công! Các file .py trong 'helpers' đã thành .pyd")
else:
    print("\n❌ Không tìm thấy file .py nào để mã hóa!")