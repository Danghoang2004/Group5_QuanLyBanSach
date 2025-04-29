from flask import Flask, render_template, request, redirect, session, flash, url_for
from mysql.connector import connect, Error
import config
import uuid
import random
from datetime import datetime
import re
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
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
    matkhau = db.Column(db.String(100), nullable=False)  # Cập nhật độ dài
    hoten = db.Column(db.String(100), nullable=False)
    gioitinh = db.Column(db.String(100), nullable=False)
    diachi = db.Column(db.String(100), nullable=False)
    diachinhanhang = db.Column(db.String(100))
    diachimuahang = db.Column(db.String(100))
    ngaysinh = db.Column(db.Date)
    sodienthoai = db.Column(db.String(100))
    email = db.Column(db.String(100))
    dangkinhanbangtin = db.Column(db.Boolean)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hodem = db.Column(db.String(100), nullable=False)
    ten = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    matkhau = db.Column(db.String(255), nullable=False)

@app.route("/")
def home():
    # Kiểm tra trạng thái đăng nhập
    is_logged_in = 'makhachhang' in session
    username = session.get('tendangnhap', None) if is_logged_in else None
    return render_template("TrangChu.html", is_logged_in=is_logged_in, username=username)

@app.route('/book_detail')
def book_detail():
    title = request.args.get('title')
    img = request.args.get('img')
    desc = request.args.get('desc')
    price = request.args.get('price')
    return render_template('book_detail.html', title=title, img=img, desc=desc, price=price)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.", "danger")
            return render_template("login.html", username=username, is_logged_in=False)

        user = KhachHang.query.filter_by(tendangnhap=username).first()
        
        if user and check_password_hash(user.matkhau, password):
            session["makhachhang"] = user.makhachhang
            session["tendangnhap"] = user.tendangnhap
            
            remember = request.form.get("remember")
            if remember:
                session.permanent = True
            
            # flash("Đăng nhập thành công!", "success")
            return redirect(url_for('home'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không chính xác.", "danger")
            return render_template("login.html", username=username, is_logged_in=False)

    is_logged_in = 'makhachhang' in session
    username = session.get('tendangnhap', None) if is_logged_in else None
    return render_template("login.html", is_logged_in=is_logged_in, username=username)

# Hàm sinh mã khách hàng ngẫu nhiên
def get_so_ngau_nhien():
    return 'KH' + ''.join(str(random.randint(0, 9)) for _ in range(6))

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
        # Tạo mã khách hàng ngẫu nhiên và đảm bảo không trùng
            while True:
                makhachhang = get_so_ngau_nhien()
                if not KhachHang.query.filter_by(makhachhang=makhachhang).first():
                    break

            hashed_password = generate_password_hash(mat_khau)
            print(f"Hashed password length: {len(hashed_password)}")
            
            new_customer = KhachHang(
                makhachhang=makhachhang,
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
            # flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
            return redirect("/login")

        except Exception as e:
            db.session.rollback()
            print(f"Database error: {str(e)}")
            flash(f"Đã xảy ra lỗi khi đăng ký: {str(e)}", "danger")
            return redirect("/register")

    return render_template("DangKy.html")

@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Vui lòng điền đầy đủ thông tin", "danger")
            return redirect("/login-admin")

        # Tìm admin theo email
        admin = Admin.query.filter_by(email=email).first()
        
        # So sánh mật khẩu thô (không mã hóa)
        if admin and admin.matkhau == password:
            session["admin_id"] = admin.id
            session["admin_name"] = f"{admin.hodem} {admin.ten}"
            flash("Đăng nhập thành công!", "success")
            return redirect("/book_detail")
        else:
            flash("Email hoặc mật khẩu không chính xác!", "danger")
            return redirect("/login-admin")

    return render_template("login_admin.html")
@app.route("/logout")
def logout():
    session.pop('makhachhang', None)
    session.pop('tendangnhap', None)
    # flash("Đăng xuất thành công!", "success")
    return redirect(url_for('home'))

@app.route("/cart")
def cart():
<<<<<<< HEAD
    return render_template('GioHang.html')
=======
    is_logged_in = 'makhachhang' in session
    if not is_logged_in:
        flash("Vui lòng đăng nhập để truy cập giỏ hàng.", "danger")
        return redirect(url_for('/login'))
    
    username = session.get('tendangnhap') if is_logged_in else None
    return render_template("GioHang.html", is_logged_in=is_logged_in, username=username)



>>>>>>> 8f3ce1e9b54244cbd13d0fe416e2dac54d708798
if __name__ == "__main__":
    app.run(debug=True)
