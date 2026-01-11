
import hashlib
_SECRET_SALT = "MISA_APP_2026_SECRET_KEY"
def generate_activation_key(hwid):
    """
    Hàm nhận vào HWID và trả về Key đã mã hóa.
    Logic ghép chuỗi và thuật toán nằm ẩn trong này.
    """
    if not hwid:
        return None
        
    try:
        # Logic tạo key (Giấu kín thuật toán ghép chuỗi ở đây)
        raw_data = f"{hwid}::{_SECRET_SALT}::PRO"
        
        # Tạo mã SHA256 và lấy 20 ký tự đầu, viết hoa
        key = hashlib.sha256(raw_data.encode()).hexdigest()[:20].upper()
        return key
    except Exception:
        return None