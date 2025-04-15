class TheLoai:
    def __init__(self, ma_the_loai=None, ten_the_loai=None):
        self.ma_the_loai = ma_the_loai
        self.ten_the_loai = ten_the_loai

    def get_ma_the_loai(self):
        return self.ma_the_loai

    def set_ma_the_loai(self, ma_the_loai):
        self.ma_the_loai = ma_the_loai

    def get_ten_the_loai(self):
        return self.ten_the_loai

    def set_ten_the_loai(self, ten_the_loai):
        self.ten_the_loai = ten_the_loai

    def __str__(self):
        return f"TheLoai(ma_the_loai={self.ma_the_loai}, ten_the_loai={self.ten_the_loai})"
