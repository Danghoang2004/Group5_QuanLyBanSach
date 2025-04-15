from datetime import date

class DonHang:
    def __init__(self, ma_don_hang=None, khach_hang=None, dia_chi_mua_hang=None, dia_chi_nhan_hang=None,
                 trang_thai=None, hinh_thuc_thanh_toan=None, trang_thai_thanh_toan=None,
                 so_tien_da_thanh_toan=0.0, so_tien_con_thieu=0.0, ngay_dat_hang=None, ngay_giao_hang=None):
        self.ma_don_hang = ma_don_hang
        self.khach_hang = khach_hang  # đối tượng KhachHang
        self.dia_chi_mua_hang = dia_chi_mua_hang
        self.dia_chi_nhan_hang = dia_chi_nhan_hang
        self.trang_thai = trang_thai
        self.hinh_thuc_thanh_toan = hinh_thuc_thanh_toan
        self.trang_thai_thanh_toan = trang_thai_thanh_toan
        self.so_tien_da_thanh_toan = so_tien_da_thanh_toan
        self.so_tien_con_thieu = so_tien_con_thieu
        self.ngay_dat_hang = ngay_dat_hang  # date object
        self.ngay_giao_hang = ngay_giao_hang  # date object

    def get_ma_don_hang(self):
        return self.ma_don_hang

    def set_ma_don_hang(self, ma_don_hang):
        self.ma_don_hang = ma_don_hang

    def get_khach_hang(self):
        return self.khach_hang

    def set_khach_hang(self, khach_hang):
        self.khach_hang = khach_hang

    def get_dia_chi_mua_hang(self):
        return self.dia_chi_mua_hang

    def set_dia_chi_mua_hang(self, dia_chi_mua_hang):
        self.dia_chi_mua_hang = dia_chi_mua_hang

    def get_dia_chi_nhan_hang(self):
        return self.dia_chi_nhan_hang

    def set_dia_chi_nhan_hang(self, dia_chi_nhan_hang):
        self.dia_chi_nhan_hang = dia_chi_nhan_hang

    def get_trang_thai(self):
        return self.trang_thai

    def set_trang_thai(self, trang_thai):
        self.trang_thai = trang_thai

    def get_hinh_thuc_thanh_toan(self):
        return self.hinh_thuc_thanh_toan

    def set_hinh_thuc_thanh_toan(self, hinh_thuc_thanh_toan):
        self.hinh_thuc_thanh_toan = hinh_thuc_thanh_toan

    def get_trang_thai_thanh_toan(self):
        return self.trang_thai_thanh_toan

    def set_trang_thai_thanh_toan(self, trang_thai_thanh_toan):
        self.trang_thai_thanh_toan = trang_thai_thanh_toan

    def get_so_tien_da_thanh_toan(self):
        return self.so_tien_da_thanh_toan

    def set_so_tien_da_thanh_toan(self, so_tien_da_thanh_toan):
        self.so_tien_da_thanh_toan = so_tien_da_thanh_toan

    def get_so_tien_con_thieu(self):
        return self.so_tien_con_thieu

    def set_so_tien_con_thieu(self, so_tien_con_thieu):
        self.so_tien_con_thieu = so_tien_con_thieu

    def get_ngay_dat_hang(self):
        return self.ngay_dat_hang

    def set_ngay_dat_hang(self, ngay_dat_hang):
        self.ngay_dat_hang = ngay_dat_hang

    def get_ngay_giao_hang(self):
        return self.ngay_giao_hang

    def set_ngay_giao_hang(self, ngay_giao_hang):
        self.ngay_giao_hang = ngay_giao_hang

    def __eq__(self, other):
        if isinstance(other, DonHang):
            return self.ma_don_hang == other.ma_don_hang
        return False

    def __hash__(self):
        return hash(self.ma_don_hang)
