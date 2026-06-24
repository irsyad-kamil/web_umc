from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import pymysql, os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():

    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    cursor.execute("select * from peserta")

    hasil = cursor.fetchall()

    print(f"Total peserta: {len(hasil)} orang")

    return render_template("home.html")

@app.route("/test-db")
def test_db():

    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    cursor.execute("select * from peserta")

    hasil = cursor.fetchall()

    return str(hasil)

@app.route("/daftar", methods=["GET", "POST"])
def daftar():

    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
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
            "insert into peserta (nama, email, asal_sekolah, jenjang) values (%s, %s, %s, %s)",
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
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
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

@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    if request.method == "GET":
        cursor.execute(
            "select * from peserta where id = %s",
            (id,)
        )
        hasil = cursor.fetchone()
        return render_template(
            "edit.html",
            peserta=hasil
        )
    
    if request.method == "POST":
        nama_baru = request.form["siswa_1"]
        email_baru = request.form["email_siswa_1"]
        sekolah_baru = request.form["asal_sekolah"]
        jenjang_baru = request.form["jenjang"]
        cursor.execute(
            "update peserta " \
            "set nama=%s, " \
            "email=%s, " \
            "asal_sekolah=%s, " \
            "jenjang=%s " \
            "where id=%s",
            (nama_baru, email_baru, sekolah_baru, jenjang_baru, id)
        )
        connection.commit()
        return redirect(
            "/admin"
        )

@app.route("/hapus/<id>")
def hapus(id):

    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    cursor.execute(
        "delete from peserta where id = (%s)",
        (id,)
    )
    connection.commit()

    return redirect("/admin")

app.run(debug=True)