class SanPham:
    def __init__(self, ma_san_pham=None, ten_san_pham=None, tac_gia=None, nam_xuat_ban=None,
                 gia_nhap=None, gia_goc=None, gia_ban=None, so_luong=None, the_loai=None,
                 ngon_ngu=None, mo_ta=None):
        self.ma_san_pham = ma_san_pham
        self.ten_san_pham = ten_san_pham
        self.tac_gia = tac_gia  # Đây có thể là một đối tượng TacGia
        self.nam_xuat_ban = nam_xuat_ban
        self.gia_nhap = gia_nhap
        self.gia_goc = gia_goc
        self.gia_ban = gia_ban
        self.so_luong = so_luong
        self.the_loai = the_loai  # Đây có thể là một đối tượng TheLoai
        self.ngon_ngu = ngon_ngu
        self.mo_ta = mo_ta

    def get_ma_san_pham(self):
        return self.ma_san_pham

    def set_ma_san_pham(self, ma_san_pham):
        self.ma_san_pham = ma_san_pham

    def get_ten_san_pham(self):
        return self.ten_san_pham

    def set_ten_san_pham(self, ten_san_pham):
        self.ten_san_pham = ten_san_pham

    def get_tac_gia(self):
        return self.tac_gia

    def set_tac_gia(self, tac_gia):
        self.tac_gia = tac_gia

    def get_nam_xuat_ban(self):
        return self.nam_xuat_ban

    def set_nam_xuat_ban(self, nam_xuat_ban):
        self.nam_xuat_ban = nam_xuat_ban

    def get_gia_nhap(self):
        return self.gia_nhap

    def set_gia_nhap(self, gia_nhap):
        self.gia_nhap = gia_nhap

    def get_gia_goc(self):
        return self.gia_goc

    def set_gia_goc(self, gia_goc):
        self.gia_goc = gia_goc

    def get_gia_ban(self):
        return self.gia_ban

    def set_gia_ban(self, gia_ban):
        self.gia_ban = gia_ban

    def get_so_luong(self):
        return self.so_luong

    def set_so_luong(self, so_luong):
        self.so_luong = so_luong

    def get_the_loai(self):
        return self.the_loai

    def set_the_loai(self, the_loai):
        self.the_loai = the_loai

    def get_ngon_ngu(self):
        return self.ngon_ngu

    def set_ngon_ngu(self, ngon_ngu):
        self.ngon_ngu = ngon_ngu

    def get_mo_ta(self):
        return self.mo_ta

    def set_mo_ta(self, mo_ta):
        self.mo_ta = mo_ta
