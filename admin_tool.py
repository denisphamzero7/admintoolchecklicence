import hashlib
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from helpers.path_manager import apply_window_icon 
# ============================================================================
# [QUAN TRỌNG] MÃ BÍ MẬT - PHẢI GIỐNG HỆT FILE helpers/license_manager.py
# Nếu bên kia bạn đổi, bên này cũng phải đổi theo thì Key mới khớp.
# ============================================================================
SECRET_SALT = "MISA_APP_2026_SECRET_KEY" 

class AdminKeyGen(ttk.Window):
    def __init__(self):
        super().__init__(title="Admin Key Generator (Cấp Bản Quyền)", themename="superhero")
        self.geometry("500x400")
        
        # Căn giữa màn hình
        self.place_window_center()
        apply_window_icon(self)
        # --- TIÊU ĐỀ ---
        ttk.Label(self, text="CÔNG CỤ TẠO KEY BẢN QUYỀN", 
                  font=("Segoe UI", 16, "bold"), bootstyle="info").pack(pady=20)

        # --- KHUNG NHẬP MÃ MÁY ---
        frame_input = ttk.Labelframe(self, text="1. Nhập Mã Máy (HWID) của khách", padding=15)
        frame_input.pack(fill=X, padx=20, pady=5)
        
        self.ent_hwid = ttk.Entry(frame_input, font=("Consolas", 11))
        self.ent_hwid.pack(fill=X, pady=(0, 10))
        self.ent_hwid.focus() # Tự focus để paste cho lẹ

        # Nút Tạo Key
        ttk.Button(frame_input, text="⚡ TẠO KEY NGAY", bootstyle="warning", 
                   command=self.generate_key, width=20).pack(fill=X)

        # --- KHUNG KẾT QUẢ ---
        frame_output = ttk.Labelframe(self, text="2. Key Kích Hoạt (Gửi cho khách)", padding=15)
        frame_output.pack(fill=X, padx=20, pady=15)
        
        self.ent_key = ttk.Entry(frame_output, font=("Consolas", 12, "bold"), bootstyle="success")
        self.ent_key.pack(fill=X, pady=(0, 10))

        # Nút Copy
        self.btn_copy = ttk.Button(frame_output, text="📋 Copy Key", bootstyle="success-outline", 
                                   command=self.copy_key, state="disabled")
        self.btn_copy.pack(fill=X)

        # Label trạng thái
        self.lbl_status = ttk.Label(self, text="Sẵn sàng...", font=("Segoe UI", 9, "italic"), bootstyle="secondary")
        self.lbl_status.pack(side=BOTTOM, pady=10)

    def generate_key(self, event=None):
        hwid = self.ent_hwid.get().strip()
        
        if not hwid:
            self.lbl_status.config(text="❌ Lỗi: Vui lòng nhập Mã máy!", bootstyle="danger")
            return

        try:
            # --- LOGIC TẠO KEY (GIỐNG HỆT APP CHÍNH) ---
            # Công thức: SHA256( HWID + SALT + TYPE ) -> Lấy 20 ký tự đầu
            raw_data = f"{hwid}::{SECRET_SALT}::PRO"
            key = hashlib.sha256(raw_data.encode()).hexdigest()[:20].upper()
            
            # Hiển thị
            self.ent_key.delete(0, tk.END)
            self.ent_key.insert(0, key)
            
            # Update UI
            self.btn_copy.config(state="normal")
            self.lbl_status.config(text=f"✅ Đã tạo key cho mã: {hwid[:10]}...", bootstyle="success")
            
            # Tự động copy luôn cho tiện
            self.copy_key()
            
        except Exception as e:
            self.lbl_status.config(text=f"Lỗi: {str(e)}", bootstyle="danger")

    def copy_key(self):
        key = self.ent_key.get()
        if key:
            self.clipboard_clear()
            self.clipboard_append(key)
            self.update() # Giữ clipboard sau khi tắt app
            self.lbl_status.config(text="✅ Đã copy Key vào bộ nhớ tạm!", bootstyle="success")

if __name__ == "__main__":
    app = AdminKeyGen()
    app.mainloop()