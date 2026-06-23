from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymysql, os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="21mei26@AIEA",
        database="umc_tes_db"
    )

    cursor = connection.cursor()

    cursor.execute("select * from peserta")

    hasil = cursor.fetchall()

    print(f"Total peserta: {len(hasil)} orang")

    return render_template("home.html")

@app.route("/test-db")
def test_db():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="21mei26@AIEA",
        database="umc_tes_db"
    )

    cursor = connection.cursor()

    cursor.execute("select * from peserta")

    hasil = cursor.fetchall()

    return str(hasil)

@app.route("/daftar", methods=["GET", "POST"])
def daftar():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="21mei26@AIEA",
        database="umc_tes_db"
    )

    cursor = connection.cursor()

    if request.method == "GET":

        return render_template("daftar.html")

    if request.method == "POST":
        siswa_1 = request.form["siswa_1"]
        email_siswa_1 = request.form["email_siswa_1"]
        sekolah = request.form["asal_sekolah"]
        jenjang = request.form["jenjang"]
        
        cursor.execute(
            "insert into peserta (nama_siswa, email_siswa, asal_sekolah, jenjang) values (%s, %s, %s, %s)",
            (siswa_1, email_siswa_1, sekolah, jenjang)
        )

        connection.commit()
        
    return render_template(
        "sukses.html",
        siswa_1=siswa_1,
        email_siswa_1=email_siswa_1,
        asal_sekolah=sekolah,
        jenjang=jenjang
        )

@app.route("/admin")
def admin():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="21mei26@AIEA",
        database="umc_tes_db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "select * from peserta"
    )

    hasil = cursor.fetchall()

    return render_template(
        "admin.html",
        peserta=hasil
    )

app.run(debug=True)