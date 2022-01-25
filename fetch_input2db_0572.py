import requests, json
import mysql.connector
import os
import time
import sys
from tabulate import tabulate

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'api.abcfdab.cfd',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}
config=mysql.connector.connect(host="localhost", user="root", password="", database="db_akademik_0572")
def animate():
    #animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    print("Database terhubung dan menyiapkan API untuk diimport ke database")
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

def api2db():
    api_url="https://api.abcfdab.cfd/students/"
    response = requests.get(api_url, headers=headers).json()
    for id in range(0,50):
        data_response=response['data'][id]
        id=data_response['id']
        nim=data_response['nim']
        nama=data_response['nama']
        jk=data_response['jk']
        jurusan=data_response['jurusan']
        alamat=data_response['alamat']
        config.reconnect()
        cursor = config.cursor()
        cursor.execute("INSERT INTO tbl_students_0572 (id, nim, nama, jk, jurusan, alamat) VALUES (%s, %s, %s, %s, %s, %s)", (id, nim, nama, jk, jurusan, alamat))
        config.commit()
        print(f"\nData dengan NIM : {nim} telah berhasil diimport kedalam database!")
    print("\nSemua data berhasil diimport!\n")
    # print(f"Nama : {nama}\nNim : {nim}\nJenis Kelamin : {jk}\nJurusan : {jurusan}\nAlamat : {alamat}\n\n")
def menu():
    print("\n=== Main Menu ===")
    print("[1] Lihat Daftar Mahasiswa")
    print("[2] Buat Mahasiswa Baru")
    print("[3] Edit Mahasiswa")
    print("[4] Hapus Mahasiswa")
    print("[5] Cari Mahasiswa")
    print("[0] Exit")
    print("------------------------")
    pilihan_menu = input("Pilih menu> ")
    
    if(pilihan_menu == "1"):
        tampilkan_mahasiswa()
    elif(pilihan_menu == "2"):
        buat_mahasiswa()
    elif(pilihan_menu == "3"):
        edit_mahasiswa()
    elif(pilihan_menu == "4"):
        hapus_mahasiswa()
    elif(pilihan_menu == "5"):
        cari_mahasiswa()
    elif(pilihan_menu == "0"):
        exit()
    else:
        print("Inputan salah!")
        kembali_ke_menu()
def kembali_ke_menu():
    print("\n")
    input("Tekan Enter untuk kembali...")
    menu()
def tampilkan_mahasiswa():
    tampil=input("""
1. Tampilkan seluruh Mahasiswa
2. Tampilkan Mahasiswa berdasarkan limit
3. Tampilkan Mahasiswa berdasarkan kecocokan nama
input> """)
    if tampil=="1":

        config.reconnect()
        cursor = config.cursor()
        cursor.execute('SELECT * FROM tbl_students_0572')
        result = cursor.fetchall()
        cursor.close()
        table=[]

        for row in result:
            data=[row[0],row[1],row[2],row[3],row[4],row[5]]
            table.append(data)
        print(tabulate(table,headers=["ID","NIM","NAMA","Jenis Kelamin","Jurusan","Alamat"],tablefmt="pretty"))
        menu()
    elif tampil=="2":
        limit_set=input("Limit yang Anda inginkan : ")
        config.reconnect()
        cursor = config.cursor()
        cursor.execute('SELECT * FROM tbl_students_0572 LIMIT %s', (limit_set, ))
        result = cursor.fetchall()
        cursor.close()
        table=[]
        for row in result:
            data=[row[0],row[1],row[2],row[3],row[4],row[5]]
            table.append(data)
        print(tabulate(table,headers=["ID","NIM","NAMA","Jenis Kelamin","Jurusan","Alamat"],tablefmt="pretty"))
        menu()
    elif tampil=="3":
        nama_cari=input("Nama yang ingin Anda tampilkan :")
        config.reconnect()
        cursor = config.cursor()
        cursor.execute('SELECT * FROM tbl_students_0572 WHERE nama LIKE %s', ("%" + nama_cari + "%",))
        result = cursor.fetchall()
        cursor.close()
        table=[]
        for row in result:
            data=[row[0],row[1],row[2],row[3],row[4],row[5]]
            table.append(data)
        print(tabulate(table,headers=["ID","NIM","NAMA","Jenis Kelamin","Jurusan","Alamat"],tablefmt="pretty")) 
        menu()
    else:
        input("Inputan yang Anda masukkan salah\n\nTekan enter untuk kembali")
        tampilkan_mahasiswa()
def buat_mahasiswa():
    nim = input("NIM Mahasiswa (xx.xx.xxxx) : ")
    nama = input("Nama Mahasiswa : ")
    jk = input("Jenis Kelamin Mahasiswa (L/P) : ")
    jurusan = input("Jurusan Mahasiswa : ")
    alamat = input("Alamat Mahasiswa : ")
    config.reconnect()
    cur = config.cursor()
    cur.execute('INSERT INTO tbl_students_0572 (nim, nama, jk, jurusan, alamat) VALUES (%s, %s, %s, %s, %s)', (nim, nama, jk, jurusan, alamat))
    config.commit()
    print(f"\nData dengan NIM : {nim}\nTelah terinput!\n") 
    time.sleep(2)     
    menu()
def edit_mahasiswa():
    cari_nim=input("Cari NIM Mahasiswa yang ingin anda ganti : ")
    config.reconnect()
    cur = config.cursor()
    cur.execute('SELECT * FROM tbl_students_0572 WHERE nim LIKE %s', ("%" + cari_nim + "%",))
    res = cur.fetchall()
    cur.close()
    print(f"\nNIM yang sesuai dengan {cari_nim} : \n")
    table=[]
    for row in res:
        data=[row[0],row[1],row[2],row[3],row[4],row[5]]
        table.append(data)
    print(tabulate(table,headers=["ID","NIM","NAMA","Jenis Kelamin","Jurusan","Alamat"],tablefmt="pretty"))
    nim_cari=input("\nMasukkan NIM yang ingin di edit secara lengkap (xx.xx.xxxx) :")
    print(f"\nGanti data {nim_cari}\n")
    nim = input("NIM Mahasiswa baru (xx.xx.xxxx) : ")
    nama = input("Nama Mahasiswa baru : ")
    jk = input("Jenis Kelamin Mahasiswa baru (L/P) : ")
    jurusan = input("Jurusan Mahasiswa baru : ")
    alamat = input("Alamat Mahasiswa baru : ")
    config.reconnect()
    cur = config.cursor()
    cur.execute('UPDATE mahasiswa SET (nim, nama, jk, jurusan, alamat) VALUES (%s, %s, %s, %s, %s) WHERE nim_cari=%s', (nim, nama, jk, jurusan, alamat, nim_cari))
    config.commit()  
    print(f"\nData dengan NIM : {nim}\nTelah terupdate!\n") 
    time.sleep(2)
    menu()
def cari_mahasiswa():
    cari_nim=input("Cari NIM Mahasiswa yang ingin anda ganti : ")
    config.reconnect()
    cur = config.cursor()
    cur.execute('SELECT * FROM tbl_students_0572 WHERE nim LIKE %s', ("%" + cari_nim + "%",))
    res = cur.fetchall()
    cur.close()
    print(f"\nNIM yang sesuai dengan {cari_nim} : \n")
    table=[]
    for row in res:
        data=[row[0],row[1],row[2],row[3],row[4],row[5]]
        table.append(data)
    print(tabulate(table,headers=["ID","NIM","NAMA","Jenis Kelamin","Jurusan","Alamat"],tablefmt="pretty"))
    menu()
def hapus_mahasiswa():
    cari_nim=input("Cari NIM Mahasiswa yang ingin anda hapus : ")
    config.reconnect()
    cur = config.cursor()
    cur.execute('SELECT * FROM tbl_students_0572 WHERE nim LIKE %s', ("%" + cari_nim + "%",))
    res = cur.fetchall()
    cur.close()
    print(f"\nNIM yang sesuai dengan {cari_nim} : \n")
    table=[]
    for row in res:
        data=[row[0],row[1],row[2],row[3],row[4],row[5]]
        table.append(data)
    print(tabulate(table,headers=["ID","NIM","NAMA","Jenis Kelamin","Jurusan","Alamat"],tablefmt="pretty"))
    nim_cari=input("\nMasukkan NIM yang ingin di edit secara lengkap (xx.xx.xxxx) :")
    config.reconnect()
    cur = config.cursor()
    cur.execute('DELETE FROM tbl_students_0572 WHERE nim=%s', (nim_cari,))
    config.commit()
    print(f"\nData dengan NIM : {nim_cari}\nTelah terhapus!\n") 
    time.sleep(2)
    menu()
if __name__ == '__main__':
    if config.is_connected():
        print('Database sudah terhubung\n')
    cursor = config.cursor()
    sql = """SELECT count(*) as tot FROM tbl_students_0572"""
    cursor.execute(sql)
    data = cursor.fetchone()
    config.close()
    cek_table=data[0]
    if cek_table==0:
        animate()
        api2db()
        print("\nMemasuki menu utama")
        time.sleep(2)
        menu()      
    else:
        print("Data sudah ada, memasuki menu utama")
        time.sleep(2)
        menu()
    
#20.83.0572_Raihan Rinto Andiansyah
