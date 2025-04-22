from flask import Flask, render_template, request, redirect, session, flash
from mysql.connector import connect, Error
import config
import uuid
from datetime import datetime
import re
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = config.MYSQL_CONN
except AttributeError:
    print("Lỗi: Không tìm thấy MYSQL_CONN trong config.py")
    exit(1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'
db = SQLAlchemy(app)

class KhachHang(db.Model):
    __tablename__ = 'khachhang'
    makhachhang = db.Column(db.String(50), primary_key=True)
    tendangnhap = db.Column(db.String(100), nullable=False)
    matkhau = db.Column(db.String(255), nullable=False)  # Cập nhật độ dài
    hoten = db.Column(db.String(100), nullable=False)
    gioitinh = db.Column(db.String(100), nullable=False)
    diachi = db.Column(db.String(100), nullable=False)
    diachinhanhang = db.Column(db.String(100))
    diachimuahang = db.Column(db.String(100))
    ngaysinh = db.Column(db.Date)
    sodienthoai = db.Column(db.String(100))
    email = db.Column(db.String(100))
    dangkinhanbangtin = db.Column(db.Boolean)

@app.route("/")
def home():
    return render_template("TrangChu.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("Received POST request to /register")
        print(f"Form data: {request.form}")

        hanh_dong = request.form.get("hanhDong")
        if hanh_dong != "dang-ky":
            flash("Hành động không hợp lệ!", "danger")
            return redirect("/register")

        ten_dang_nhap = request.form.get("tenDangNhap")
        mat_khau = request.form.get("matKhau")
        mat_khau_nhap_lai = request.form.get("matKhauNhapLai")
        ho_ten = request.form.get("hoVaTen")
        gioi_tinh = request.form.get("gioiTinh")
        ngay_sinh = request.form.get("ngaySinh")
        dia_chi = request.form.get("diaChiKhachHang")
        dia_chi_mua_hang = request.form.get("diaChiMuaHang")
        dia_chi_nhan_hang = request.form.get("diaChiNhanHang")
        dien_thoai = request.form.get("dienThoai")
        email = request.form.get("email")
        dong_y_nhan_mail = request.form.get("dongYNhanMail") == "on"

        errors = []
        
        if not ten_dang_nhap or len(ten_dang_nhap.strip()) < 3:
            errors.append("Tên đăng nhập phải có ít nhất 3 ký tự.")
        
        if KhachHang.query.filter_by(tendangnhap=ten_dang_nhap).first():
            errors.append("Tên đăng nhập đã tồn tại.")

        if not mat_khau or len(mat_khau) < 8:
            errors.append("Mật khẩu phải có ít nhất 8 ký tự.")
        elif mat_khau != mat_khau_nhap_lai:
            errors.append("Mật khẩu không khớp.")
        
        if not ho_ten or len(ho_ten.strip()) < 2:
            errors.append("Họ và tên không hợp lệ.")
        
        if not gioi_tinh or gioi_tinh not in ["Nam", "Nữ", "Khác"]:
            errors.append("Vui lòng chọn giới tính.")
        
        if not dia_chi or len(dia_chi.strip()) < 5:
            errors.append("Địa chỉ không hợp lệ.")
        
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not email or not re.match(email_regex, email):
            errors.append("Email không hợp lệ.")
        
        phone_regex = r'^\d{10,11}$'
        if not dien_thoai or not re.match(phone_regex, dien_thoai):
            errors.append("Số điện thoại không hợp lệ.")
        
        try:
            ngay_sinh_date = datetime.strptime(ngay_sinh, "%Y-%m-%d").date() if ngay_sinh else None
            if ngay_sinh_date and ngay_sinh_date > datetime.now().date():
                errors.append("Ngày sinh không được là ngày trong tương lai.")
        except ValueError:
            errors.append("Ngày sinh không hợp lệ.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect("/register")

        try:
            hashed_password = generate_password_hash(mat_khau)
            print(f"Hashed password length: {len(hashed_password)}")  # Debug
            new_customer = KhachHang(
                makhachhang=str(uuid.uuid4()),
                tendangnhap=ten_dang_nhap,
                matkhau=hashed_password,
                hoten=ho_ten,
                gioitinh=gioi_tinh,
                diachi=dia_chi,
                diachimuahang=dia_chi_mua_hang,
                diachinhanhang=dia_chi_nhan_hang,
                ngaysinh=ngay_sinh_date,
                sodienthoai=dien_thoai,
                email=email,
                dangkinhanbangtin=dong_y_nhan_mail
            )
            print("Adding new customer to database...")
            db.session.add(new_customer)
            db.session.commit()
            print("Customer added successfully!")
            flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {str(e)}")
            flash(f"Đã xảy ra lỗi khi đăng ký: {str(e)}", "danger")
            return redirect("/register")

    return render_template("DangKy.html")

if __name__ == "__main__":
    app.run(debug=True)