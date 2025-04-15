class KhachHang:
    def __init__(self, ma_khach_hang, ten_dang_nhap, mat_khau, ho_va_ten, gioi_tinh,
                 dia_chi, dia_chi_nhan_hang, dia_chi_mua_hang, ngay_sinh,
                 so_dien_thoai, email, dang_ky_nhan_bang_tin):
        self.ma_khach_hang = ma_khach_hang
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.ho_va_ten = ho_va_ten
        self.gioi_tinh = gioi_tinh
        self.dia_chi = dia_chi
        self.dia_chi_nhan_hang = dia_chi_nhan_hang
        self.dia_chi_mua_hang = dia_chi_mua_hang
        self.ngay_sinh = ngay_sinh
        self.so_dien_thoai = so_dien_thoai
        self.email = email
        self.dang_ky_nhan_bang_tin = dang_ky_nhan_bang_tin

    def get_ma_khach_hang(self):
        return self.ma_khach_hang

    def set_ma_khach_hang(self, ma_khach_hang):
        self.ma_khach_hang = ma_khach_hang

    def get_ten_dang_nhap(self):
        return self.ten_dang_nhap

    def set_ten_dang_nhap(self, ten_dang_nhap):
        self.ten_dang_nhap = ten_dang_nhap

    def get_mat_khau(self):
        return self.mat_khau

    def set_mat_khau(self, mat_khau):
        self.mat_khau = mat_khau

    def get_ho_va_ten(self):
        return self.ho_va_ten

    def set_ho_va_ten(self, ho_va_ten):
        self.ho_va_ten = ho_va_ten

    def get_gioi_tinh(self):
        return self.gioi_tinh

    def set_gioi_tinh(self, gioi_tinh):
        self.gioi_tinh = gioi_tinh

    def get_dia_chi(self):
        return self.dia_chi

    def set_dia_chi(self, dia_chi):
        self.dia_chi = dia_chi

    def get_dia_chi_nhan_hang(self):
        return self.dia_chi_nhan_hang

    def set_dia_chi_nhan_hang(self, dia_chi_nhan_hang):
        self.dia_chi_nhan_hang = dia_chi_nhan_hang

    def get_dia_chi_mua_hang(self):
        return self.dia_chi_mua_hang

    def set_dia_chi_mua_hang(self, dia_chi_mua_hang):
        self.dia_chi_mua_hang = dia_chi_mua_hang

    def get_ngay_sinh(self):
        return self.ngay_sinh

    def set_ngay_sinh(self, ngay_sinh):
        self.ngay_sinh = ngay_sinh

    def get_so_dien_thoai(self):
        return self.so_dien_thoai

    def set_so_dien_thoai(self, so_dien_thoai):
        self.so_dien_thoai = so_dien_thoai

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def is_dang_ky_nhan_bang_tin(self):
        return self.dang_ky_nhan_bang_tin

    def set_dang_ky_nhan_bang_tin(self, dang_ky_nhan_bang_tin):
        self.dang_ky_nhan_bang_tin = dang_ky_nhan_bang_tin