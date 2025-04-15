from datetime import date

class TacGia:
    def __init__(self, ma_tac_gia=None, ho_va_ten=None, ngay_sinh=None, tieu_su=None):
        self.ma_tac_gia = ma_tac_gia
        self.ho_va_ten = ho_va_ten
        self.ngay_sinh = ngay_sinh  # dạng date
        self.tieu_su = tieu_su

    def get_ma_tac_gia(self):
        return self.ma_tac_gia

    def set_ma_tac_gia(self, ma_tac_gia):
        self.ma_tac_gia = ma_tac_gia

    def get_ho_va_ten(self):
        return self.ho_va_ten

    def set_ho_va_ten(self, ho_va_ten):
        self.ho_va_ten = ho_va_ten

    def get_ngay_sinh(self):
        return self.ngay_sinh

    def set_ngay_sinh(self, ngay_sinh):
        self.ngay_sinh = ngay_sinh

    def get_tieu_su(self):
        return self.tieu_su

    def set_tieu_su(self, tieu_su):
        self.tieu_su = tieu_su

    def __eq__(self, other):
        if isinstance(other, TacGia):
            return self.ma_tac_gia == other.ma_tac_gia
        return False

    def __hash__(self):
        return hash((self.ma_tac_gia, self.ho_va_ten, self.ngay_sinh, self.tieu_su))

    def __str__(self):
        return f'TacGia(ma_tac_gia={self.ma_tac_gia}, ho_va_ten={self.ho_va_ten}, ngay_sinh={self.ngay_sinh}, tieu_su={self.tieu_su})'
