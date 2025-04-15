class ChiTietDonHang:
    def __init__(self, ma_chi_tiet_don_hang=None, don_hang=None, san_pham=None,
                 so_luong=0.0, gia_goc=0.0, giam_gia=0.0, gia_ban=0.0,
                 thue_vat=0.0, tong_tien=0.0):
        self.ma_chi_tiet_don_hang = ma_chi_tiet_don_hang
        self.don_hang = don_hang
        self.san_pham = san_pham
        self.so_luong = so_luong
        self.gia_goc = gia_goc
        self.giam_gia = giam_gia
        self.gia_ban = gia_ban
        self.thue_vat = thue_vat
        self.tong_tien = tong_tien

    def get_ma_chi_tiet_don_hang(self):
        return self.ma_chi_tiet_don_hang

    def set_ma_chi_tiet_don_hang(self, value):
        self.ma_chi_tiet_don_hang = value

    def get_don_hang(self):
        return self.don_hang

    def set_don_hang(self, value):
        self.don_hang = value

    def get_san_pham(self):
        return self.san_pham

    def set_san_pham(self, value):
        self.san_pham = value

    def get_so_luong(self):
        return self.so_luong

    def set_so_luong(self, value):
        self.so_luong = value

    def get_gia_goc(self):
        return self.gia_goc

    def set_gia_goc(self, value):
        self.gia_goc = value

    def get_giam_gia(self):
        return self.giam_gia

    def set_giam_gia(self, value):
        self.giam_gia = value

    def get_gia_ban(self):
        return self.gia_ban

    def set_gia_ban(self, value):
        self.gia_ban = value

    def get_thue_vat(self):
        return self.thue_vat

    def set_thue_vat(self, value):
        self.thue_vat = value

    def get_tong_tien(self):
        return self.tong_tien

    def set_tong_tien(self, value):
        self.tong_tien = value

    def __str__(self):
        return (f"ChiTietDonHang(ma_chi_tiet_don_hang={self.ma_chi_tiet_don_hang}, "
                f"don_hang={self.don_hang}, san_pham={self.san_pham}, "
                f"so_luong={self.so_luong}, gia_goc={self.gia_goc}, giam_gia={self.giam_gia}, "
                f"gia_ban={self.gia_ban}, thue_vat={self.thue_vat}, tong_tien={self.tong_tien})")
