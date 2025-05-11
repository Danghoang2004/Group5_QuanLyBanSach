from flask import Flask, jsonify, render_template, request, redirect, session, flash, url_for
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
    hoten = db.Column(db.String(100), nullable=True)
    gioitinh = db.Column(db.String(100), nullable=True)
    diachi = db.Column(db.String(100), nullable=True)
    diachinhanhang = db.Column(db.String(100), nullable=True)
    diachimuahang = db.Column(db.String(100), nullable=True)
    ngaysinh = db.Column(db.Date, nullable=True)
    sodienthoai = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    dangkinhanbangtin = db.Column(db.Boolean, nullable=True)

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

        ten_dang_nhap = request.form.get("tenDangNhap", "").strip()
        mat_khau = request.form.get("matKhau", "").strip()
        mat_khau_nhap_lai = request.form.get("matKhauNhapLai", "").strip()
        ho_ten = request.form.get("hoVaTen", "").strip() or None
        gioi_tinh = request.form.get("gioiTinh", "").strip() or None
        ngay_sinh = request.form.get("ngaySinh", "").strip() or None
        dia_chi = request.form.get("diaChiKhachHang", "").strip() or None
        dia_chi_mua_hang = request.form.get("diaChiMuaHang", "").strip() or None
        dia_chi_nhan_hang = request.form.get("diaChiNhanHang", "").strip() or None
        dien_thoai = request.form.get("dienThoai", "").strip() or None
        email = request.form.get("email", "").strip() or None
        dong_y_nhan_mail = request.form.get("dongYNhanMail") == "on"

        errors = []
        
        # Kiểm tra các trường bắt buộc
        if not ten_dang_nhap or len(ten_dang_nhap) < 3:
            errors.append("Tên đăng nhập phải có ít nhất 3 ký tự.")
        if KhachHang.query.filter_by(tendangnhap=ten_dang_nhap).first():
            errors.append("Tên đăng nhập đã tồn tại.")
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
            
            # Chuyển đổi ngày sinh nếu có
            ngay_sinh_date = None
            if ngay_sinh:
                try:
                    ngay_sinh_date = datetime.strptime(ngay_sinh, "%Y-%m-%d").date()
                    if ngay_sinh_date > datetime.now().date():
                        flash("Ngày sinh không được là ngày trong tương lai.", "danger")
                        return redirect("/register")
                except ValueError:
                    flash("Ngày sinh không hợp lệ.", "danger")
                    return redirect("/register")

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

        # Tài khoản cố định
        fixed_email = "admin@gmail.com"
        fixed_password = "admin123"

        if email == fixed_email and password == fixed_password:
            session["admin_id"] = 1
            session["admin_name"] = "Admin Cố Định"
            flash("Đăng nhập thành công!", "success")
            return redirect("/bangdieukhien")
        else:
            flash("Email hoặc mật khẩu không chính xác!", "danger")
            return redirect("/login-admin")

    return render_template("login_admin.html")

@app.route("/bangdieukhien")
def bang_dieu_khien():
    # Có thể kiểm tra đăng nhập tại đây nếu cần
    if "admin_id" not in session:
        flash("Bạn cần đăng nhập để truy cập.", "warning")
        return redirect("/login-admin")
    return render_template("bangdieukhien_admin.html")

@app.route("/quanlysanpham")
def quan_ly_san_pham():
    return render_template("quan_ly_SP.html")

@app.route("/quanlynguoidung")
def quan_ly_nguoi_dung():
    return render_template("quanlynguoidung_admin.html")

@app.route("/api/users", methods=["GET"])
def api_get_users():
    users = KhachHang.query.all()
    result = []
    for user in users:
        result.append({
            "makhachhang": user.makhachhang,
            "tendangnhap": user.tendangnhap,
            "hoten": user.hoten,
            "gioitinh": user.gioitinh,
            "diachi": user.diachi,
            "sodienthoai": user.sodienthoai,
            "email": user.email,
            "ngaysinh": user.ngaysinh.strftime('%Y-%m-%d') if user.ngaysinh else "",
            "dangkinhanbangtin": user.dangkinhanbangtin,
            "diachinhanhang": user.diachinhanhang
        })
    return jsonify(result)

@app.route("/api/users", methods=["POST"])
def api_add_user():
    data = request.json
    new_user = KhachHang(
        makhachhang=get_so_ngau_nhien(),
        tendangnhap=data["tendangnhap"],
        matkhau=generate_password_hash(data["matkhau"]),
        hoten=data["hoten"],
        gioitinh=data["gioitinh"],
        diachi=data["diachi"],
        diachinhanhang=data["diachinhanhang"],
        ngaysinh=datetime.strptime(data["ngaysinh"], "%Y-%m-%d") if data["ngaysinh"] else None,
        sodienthoai=data["sodienthoai"],
        email=data["email"],
        dangkinhanbangtin=data["dangkinhanbangtin"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/users/<makhachhang>", methods=["PUT"])
def api_update_user(makhachhang):
    data = request.json
    user = KhachHang.query.get(makhachhang)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    user.tendangnhap = data["tendangnhap"]
    user.hoten = data["hoten"]
    user.gioitinh = data["gioitinh"]
    user.diachi = data["diachi"]
    user.diachinhanhang = data["diachinhanhang"]
    user.ngaysinh = datetime.strptime(data["ngaysinh"], "%Y-%m-%d") if data["ngaysinh"] else None
    user.sodienthoai = data["sodienthoai"]
    user.email = data["email"]
    user.dangkinhanbangtin = data["dangkinhanbangtin"]
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/users/<makhachhang>", methods=["DELETE"])
def api_delete_user(makhachhang):
    user = KhachHang.query.get(makhachhang)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/quanlydonhang")
def quan_ly_don_hang():
    return render_template("quanlydonhang_admin.html")


@app.route("/logout")
def logout():
    session.pop('makhachhang', None)
    session.pop('tendangnhap', None)
    # flash("Đăng xuất thành công!", "success")
    return redirect(url_for('home'))

@app.route('/giohang')
def gio_hang():
    is_logged_in = 'makhachhang' in session
    if not is_logged_in:
        flash("Vui lòng đăng nhập để truy cập giỏ hàng.", "danger")
        return redirect(url_for('login'))
    
    username = session.get('tendangnhap') if is_logged_in else None
    return render_template("GioHang.html", is_logged_in=is_logged_in, username=username)
    

if __name__ == "__main__":
    app.run(debug=True)