import Koneksi_db
import tabulate
import time
import os
import main

def clear():
    os.system('cls')

def header():
    with open('UI\Header.txt','r',encoding='utf-8') as header:
        header = header.read()
        print(header)

def Fitur_data_tim(): ## nanti buat pemisah akses fitur 
    clear()
    header()
    a = '''
|                1. Tambah Petugas              |
|                2. Lihat Data Petugas          |
|                3. Update Data Petugas         |
|                4. Hapus Data Petugas          |
|                x. Kembali                     |
================================================='''
    print(a)
    pilihan = input("Menu yang dituju :")
    match pilihan:
                case '1' : # bua
                    Fitur_Create_Tim()
                case '2' : # Lihat
                    try:
                        file = Koneksi_db.read_all_table("select * from tim_taksasi")
                        Fitur_read_tim(file)
                    except :
                        Fitur_data_tim()
                case '3' : # Update
                    fitur_update_tim()
                case '4' : # Delete
                    fitur_delete_tim()
                case 'x' :
                    main.menu_admin()
                case _ :
                    Fitur_data_tim()

def Fitur_read_tim(file): # Paginiation parameter berbentuk list
    jumlah_data_per_page = 2
    def lihat_halaman(file):
        def lihat_banyak_halaman(file):
            df = file
            banyak_halaman = len(df)%jumlah_data_per_page
            if banyak_halaman == 0:
                banyak_halaman = len(df)/jumlah_data_per_page
            else:
                banyak_halaman = int(len(df)/jumlah_data_per_page+1)  
            return banyak_halaman
        
        def tampilkan_per_halaman(halaman_ke):
            df = file
            batas_bawah = 0
            batas_atas = jumlah_data_per_page
            for a in range(0,halaman_ke-1):
                batas_atas += jumlah_data_per_page
                batas_bawah += jumlah_data_per_page
            list_halaman = df.iloc[batas_bawah:batas_atas]
            return list_halaman

        def pilihan_halaman(n=1,pesan=""):
            clear()
            header()
            nama_kolom = list(file.columns)
            a = tabulate.tabulate(tampilkan_per_halaman(n),headers=nama_kolom,tablefmt="grid",showindex=False)
            print(a)
            if pesan == "":
                print(f"Halaman {n}/{int(lihat_banyak_halaman(file))}")
            else:
                print(pesan)
            pilihan = input('Ketikkan halaman yang ingin dituju [t] untuk kembali:')
            if len(pilihan) < 1:
                pilihan_halaman(n,"Pilihan anda melebihi jumlah data....")
                pilihan_halaman()
            else:
                if pilihan == "t":
                    Fitur_data_tim()

                else:
                    pilihan = int(pilihan)
                    if pilihan <= lihat_banyak_halaman(file):
                        n = pilihan
                        pilihan_halaman(n)
                    else:
                        pilihan_halaman(n,"Pilihan anda melebihi jumlah data....")
                        pilihan_halaman()
                clear()
        pilihan_halaman()
    lihat_halaman(file)

def Fitur_Create_Tim():
    clear()
    header()
    while True:
        print("Tambahkan Tim? [Y/N] : ")
        pilihan = input('Pilihan : ')
        if pilihan.lower() == 'n':
            Fitur_data_tim()
        elif pilihan.lower() == 'y':
            nama_tim = input("Nama Tim      :")
            username = input("Buat Username :")
            password = input("Buat Password :")
            id_bkph = 100

            try:
                #Penentuan ID Alamat dan Insert
                try:
                    id_tim_taksasi = Koneksi_db.read_all_table(f"SELECT max(id_tim_taksasi) FROM tim_taksasi",2)
                    for a in id_tim_taksasi:
                        id_tim_taksasi = list(a)
                    id_tim_taksasi = int(id_tim_taksasi[0]+1)
                except:
                    id_tim_taksasi = 1000
                query = "INSERT INTO tim_taksasi(id_tim_taksasi,nama,username,password,id_bkph)" 
                query = query + f" VALUES ({id_tim_taksasi},'{nama_tim}','{username}','{password}',{id_bkph})"
                Koneksi_db.insert_to_db(query)
                print("Data Berhasil Dibuat!")
                time.sleep(2)

            except:
                print("Data Gagal Dibuat")
                time.sleep(1)
                print("Silahkan Masukkan Ulang Data")
                time.sleep(2)
                Fitur_Create_Tim()

        else:
            Fitur_Create_Tim()

def fitur_update_tim():
    while True:
        clear()
        header()
        print("Update Petani? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            Fitur_data_tim()
        elif pilihan.lower() == 'y':
            data = Koneksi_db.read_tim()
            data_kolom = list(data.columns)
            tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
            print(tabel)
            pilihan_update = input("Masukkan ID Tim yang akan Diupdate : ")

            data = Koneksi_db.read_tim(int(pilihan_update))
            data_kolom = list(data.columns)
            print(tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid'))

            konfirmasi = input("Yakin Update? Y/N :").lower()
            match konfirmasi:
                case "y":
                    data = Koneksi_db.read_all_table(f"Select * from tim_taksasi where id_tim_taksasi = {pilihan_update}",2)
                    for a in data:
                        detail = list(a)
                    print("Jika Tidak Ada Update Cukup Dikosongi")
                    nama_baru = input("Perbaiki Nama Lengkap :") or f"{detail[1]}"
                    user_baru = input("Masukkan Username Baru:") or f"{detail[2]}"
                    pass_baru = input("Masukkan Password Baru:") or f"{detail[3]}"
                    try:
                        Koneksi_db.insert_to_db(f"UPDATE tim_taksasi SET nama = '{nama_baru}', username = '{user_baru}',password = '{pass_baru}' where id_tim_taksasi = {pilihan_update}")
                        print("Data Berhasil Di Update")
                        time.sleep(2)
                    except:
                        print("Data Gagal Di Update")
                        time.sleep(0.5)
                        print("Silahkan Coba Lagi")
                        time.sleep(2)
                case _ :
                    fitur_update_tim()

def fitur_delete_tim():
     while True:
        clear()
        header()
        print("Hapus Petani? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            Fitur_data_tim()
        elif pilihan.lower() == 'y':
            data = Koneksi_db.read_tim()
            data_kolom = list(data.columns)
            tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
            print(tabel)
            pilihan_hapus = input("Masukkan ID Tim yang akan dihapus : ")

            akan_dihapus = Koneksi_db.read_all_table(f"SELECT id_tim_taksasi,nama FROM tim_taksasi where id_tim_taksasi = {pilihan_hapus}")
            kolom_dihapus = list(akan_dihapus.columns)
            print(tabulate.tabulate(akan_dihapus,headers=kolom_dihapus,showindex=False,tablefmt='grid'))

            konfirmasi = input("Yakin Hapus? Y/N :")
            if konfirmasi.lower() == 'y':
                try:
                    Koneksi_db.insert_to_db(f"DELETE FROM tim_taksasi where id_tim_taksasi = {pilihan_hapus}")
                    time.sleep(0.5)
                    print("Data Berhasil Dihapus")
                    time.sleep(2)
                except:
                    print("Data Gagal Dihapus")
                    time.sleep(1)
                    print("Silahkan Coba Lagi")
                    time.sleep(2)
            else:
                fitur_delete_tim()



