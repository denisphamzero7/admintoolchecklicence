import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from helpers.path_manager import apply_window_icon

# --- QUAN TRỌNG: Import logic tạo key từ file bảo mật ---
# (File này sẽ được Cython mã hóa thành .pyd để giấu code)
from helpers.security import generate_activation_key

class AdminKeyGen(ttk.Window):
    def __init__(self):
        super().__init__(title="Admin Key Generator (Cấp quyền sử dụng)", themename="superhero")
         
        apply_window_icon(self)
        
        # --- CẤU HÌNH VĂN BẢN (2 DÒNG) ---
        self.line1 = "UỶ BAN BẦU CỬ THÀNH PHỐ ĐÀ NẴNG"
        self.line2 = "CÔNG CỤ TẠO KEY SỬ DỤNG"
        
        # Ghép lại để hiển thị (thêm \n để xuống dòng)
        self.full_title = f"{self.line1}\n{self.line2}"
        
        # Font chữ
        self.title_font_cfg = ("Segoe UI", 16, "bold")

        # --- TÍNH TOÁN CHIỀU RỘNG MÀN HÌNH ---
        measure_font = font.Font(family=self.title_font_cfg[0], size=self.title_font_cfg[1], weight=self.title_font_cfg[2])
        
        # Đo chiều rộng của cả 2 dòng, lấy dòng nào dài hơn làm chuẩn
        w1 = measure_font.measure(self.line1)
        w2 = measure_font.measure(self.line2)
        max_text_width = max(w1, w2)
        
        # Cộng thêm padding (mỗi bên 50px cho rộng rãi)
        window_width = max_text_width + 100
        window_height = 480 # Tăng nhẹ chiều cao vì tiêu đề giờ là 2 dòng
        
        self.geometry(f"{window_width}x{window_height}")
        self.place_window_center()

        # --- TIÊU ĐỀ (ĐÃ CĂN GIỮA) ---
        # justify="center": Quan trọng để dòng trên và dòng dưới thẳng hàng nhau ở giữa
        ttk.Label(self, text=self.full_title, 
                  font=self.title_font_cfg, 
                  bootstyle="info", 
                  justify="center").pack(pady=20)

        # --- KHUNG NHẬP MÃ MÁY ---
        frame_input = ttk.Labelframe(self, text="1. Nhập Mã Máy (HWID) của khách", padding=15)
        frame_input.pack(fill=X, padx=50, pady=5) # padx khớp với padding tính toán ở trên
        
        self.ent_hwid = ttk.Entry(frame_input, font=("Consolas", 11))
        self.ent_hwid.pack(fill=X, pady=(0, 10))
        self.ent_hwid.focus()

        ttk.Button(frame_input, text="⚡ TẠO KEY NGAY", bootstyle="warning", 
                   command=self.generate_key).pack(fill=X)

        # --- KHUNG KẾT QUẢ ---
        frame_output = ttk.Labelframe(self, text="2. Key Kích Hoạt (Gửi cho khách)", padding=15)
        frame_output.pack(fill=X, padx=50, pady=15)
        
        self.ent_key = ttk.Entry(frame_output, font=("Consolas", 12, "bold"), bootstyle="success", justify="center")
        self.ent_key.pack(fill=X, pady=(0, 10))

        self.btn_copy = ttk.Button(frame_output, text="📋 SAO CHÉP KEY", bootstyle="success-outline", 
                                   command=self.copy_key, state="disabled")
        self.btn_copy.pack(fill=X)

        self.lbl_status = ttk.Label(self, text="Sẵn sàng...", font=("Segoe UI", 9, "italic"), bootstyle="secondary")
        self.lbl_status.pack(side=BOTTOM, pady=10)

    def generate_key(self, event=None):
        hwid = self.ent_hwid.get().strip()
        if not hwid:
            self.lbl_status.config(text="❌ Lỗi: Vui lòng nhập Mã máy!", bootstyle="danger")
            return

        # --- THAY ĐỔI Ở ĐÂY: Gọi hàm bảo mật thay vì tính toán trực tiếp ---
        key = generate_activation_key(hwid)
        
        if key:
            self.ent_key.delete(0, tk.END)
            self.ent_key.insert(0, key)
            self.btn_copy.config(state="normal")
            self.lbl_status.config(text=f"✅ Đã tạo key xong!", bootstyle="success")
            self.copy_key()
        else:
            self.lbl_status.config(text="❌ Lỗi xử lý (Kiểm tra security module)!", bootstyle="danger")

    def copy_key(self):
        key = self.ent_key.get()
        if key:
            self.clipboard_clear()
            self.clipboard_append(key)
            self.update()
            self.lbl_status.config(text="✅ Đã copy Key!", bootstyle="success")

if __name__ == "__main__":
    app = AdminKeyGen()
    app.mainloop()