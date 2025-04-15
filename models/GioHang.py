from models import ChiTietDonHang


class GioHang:
    def __init__(self):
        self.ds_chi_tiet = []

    def them_san_pham(self, san_pham, so_luong):
        # Tính giá bán sau giảm giá và thuế
        gia_goc = san_pham.giaGoc
        giam_gia = san_pham.giaGoc - san_pham.giaBan
        gia_ban = san_pham.giaBan
        thue_vat = gia_ban * 0.1  # giả định VAT 10%
        tong_tien = (gia_ban + thue_vat) * so_luong

        chi_tiet = ChiTietDonHang(
            ma_chi_tiet_don_hang=None,
            don_hang=None,
            san_pham=san_pham,
            so_luong=so_luong,
            gia_goc=gia_goc,
            giam_gia=giam_gia,
            gia_ban=gia_ban,
            thue_vat=thue_vat,
            tong_tien=tong_tien
        )

        self.ds_chi_tiet.append(chi_tiet)

    def xoa_san_pham(self, ma_san_pham):
        self.ds_chi_tiet = [ct for ct in self.ds_chi_tiet if ct.san_pham.maSanPham != ma_san_pham]

    def tinh_tong_tien(self):
        return sum(ct.tong_tien for ct in self.ds_chi_tiet)

    def hien_thi_gio_hang(self):
        for ct in self.ds_chi_tiet:
            print(f"Sản phẩm: {ct.san_pham.tenSanPham}, SL: {ct.so_luong}, Tổng: {ct.tong_tien:.2f}")

    def xoa_tat_ca(self):
        self.ds_chi_tiet.clear()
