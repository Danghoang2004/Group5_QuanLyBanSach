import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='quanlybansach'
    )

    if conn.is_connected():
        print("Kết nối MySQL thành công!")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM khachhang")  # Thay tên bảng thật vào
        for row in cursor.fetchall():
            print(row)

        cursor.close()
        conn.close()

except mysql.connector.Error as err:
    print(f"Lỗi kết nối: {err}")
