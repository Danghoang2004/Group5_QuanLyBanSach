from flask import Flask, render_template, request, redirect, session
from mysql.connector import connect, Error
import config

app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(16)

def get_db_connection():
    return connect(
        host=config.MYSQL_CONFIG['localhost'],
        user=config.MYSQL_CONFIG['root'],
        password=config.MYSQL_CONFIG['123456'],
        database=config.MYSQL_CONFIG['quanlybansach'],
        port=config.MYSQL_CONFIG['3306']
    )

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['tendangnhap']
        password = request.form['matkhau']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Kiểm tra thông tin đăng nhập
            cursor.execute("""
                SELECT * FROM khachhang 
                WHERE tendangnhap = %s AND matkhau = %s
            """, (username, password))
            
            user = cursor.fetchone()
            
            if user:
                session['logged_in'] = True
                session['tendangnhap'] = username
                return redirect('/dashboard')
            else:
                return render_template('login.html', error="Sai thông tin đăng nhập")
                
        except Error as e:
            print(f"Lỗi MySQL: {e}")
            return render_template('login.html', error="Lỗi hệ thống")
        finally:
            cursor.close()
            conn.close()
            
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM khachhang")
        customers = cursor.fetchall()
        return render_template("TrangChu.html", data=customers)
        
    except Error as e:
        print(f"Lỗi MySQL: {e}")
        return "Lỗi khi truy vấn dữ liệu"
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
