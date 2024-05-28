import Koneksi_db
import tabulate
import time
import os

def clear():
    os.system('cls')

def header():
    with open('UI\Header.txt','r',encoding='utf-8') as header:
        header = header.read()
        print(header)


def Fitur_read_petani(file,role): # Paginiation parameter berbentuk list
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
                    if role == 1:
                        Fitur_data_petani(1)
                    else:
                        Fitur_data_petani(2)
                
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

def Fitur_data_petani(role): ## nanti buat pemisah akses fitur 
    clear()
    header()
    a = '''
|                1. Tambah Petan                |
|                2. Lihat Data Petani           |
|                3. Update Data Petani          |
|                4. Hapus Data Petani           |
|                x. Kembali                     |
================================================='''
    b = '''
|                1. Tambah Petan                |
|                2. Lihat Data Petani           |
|                3. Update Data Petani          |
|                x. Kembali                     |
================================================='''
    if role == 1:
        print(a)
        pilihan = input("Menu yang dituju :")
        match pilihan:
            case '1' : # bua
                Fitur_Create_Petani(role)
            case '2' : # Lihat
                file = Koneksi_db.read_petani()
                Fitur_read_petani(file,role)
            case '3' : # Update
                Fitur_Update_Petani(role)
            case '4' : # Delete
                Fitur_Delete_Petani(role)
            case 'x' :
                if role == 1:
                    main.menu_admin()
                else:
                    main.menu_tim()
            case _ :
                Fitur_data_petani(role)

    else:
        print(b)
        pilihan_tim = input("Menu yang dituju :")
        match pilihan_tim:
            case '1' : # Create
                Fitur_Create_Petani(role)
            case '2' : # Read
                file = Koneksi_db.read_petani()
                Fitur_read_petani(file,role)
            case '3' : # Update
                Fitur_Update_Petani(role)
            case 'x' :
                if role == 1:
                    main.menu_admin()
                else:
                    main.menu_tim()
            case _ :
                Fitur_data_petani(role)
    
    
def Fitur_Create_Petani(role):
    clear()
    header()
    while True:
        print("Tambahkan Petani? [Y/N] : ")
        pilihan = input('Pilihan : ')
        if pilihan.lower() == 'n':
            Fitur_data_petani(role)
        elif pilihan.lower() == 'y':
            nama = input("Nama Petani :")
            luas_lahan = int(input("Masukkan Luas Lahan (Ha) :")) or 0.5

            # Tampilkan Nomor Petak
            nomor_petak = Koneksi_db.read_all_table('SELECT * FROM nomor_petak',1)
            kolom_petak = list(nomor_petak.columns)
            print(tabulate.tabulate(nomor_petak,headers=kolom_petak,showindex= False,tablefmt= 'grid'))
            nomor_petak = input("Masukkan Nomor Petak* (ID):") or 1

            estimasi_produksi = int(input("Masukkan Estimasi Produksi* (Kg):"))

            # Tampilkan Jenis Kopi
            kopi = Koneksi_db.read_all_table('SELECT * FROM jenis_kopi',1)
            kolom_kopi = list(kopi.columns)
            print(tabulate.tabulate(kopi,headers=kolom_kopi,showindex= False,tablefmt= 'grid'))
            jenis_kopi = int(input("Masukkan Jenis Kopi* (ID):")) or 1

            # Masukkan Data Petani
            print("Masukkan Alamat (*) wajib diisi):")
            jalan = input("Masukkan Jalan* :") or 'belum diisi'

            desa = Koneksi_db.read_all_table('SELECT * FROM desa',1)
            kolom_desa = list(desa.columns)
            print(tabulate.tabulate(desa,headers=kolom_desa,showindex= False,tablefmt= 'grid'))
            in_desa = input("Masukkan Desa* (ID):") or 1

            kecamatan = Koneksi_db.read_all_table('SELECT * FROM kecamatan',1)
            kolom_kecamatan = list(kecamatan.columns)
            print(tabulate.tabulate(kecamatan,headers=kolom_kecamatan,showindex= False,tablefmt= 'grid'))
            in_kecamatan = input("Masukkan Kecamatan* (ID):") or 1

            kota = Koneksi_db.read_all_table('SELECT * FROM kota',1)
            kolom_kota = list(kecamatan.columns)
            print(tabulate.tabulate(kota,headers=kolom_kota,showindex= False,tablefmt= 'grid'))
            in_kota = input("Masukkan Kota (ID):") or 1
            try:
                #Penentuan ID Alamat dan Insert
                id_alamat = Koneksi_db.read_all_table(f"SELECT max(id_alamat) FROM alamat",2)
                for a in id_alamat:
                    id_alamat = list(a)
                
                id_alamat = int(str(id_alamat[0]+1))
                query_alamat = "INSERT INTO alamat(id_alamat,nama_jalan,id_desa,id_kecamatan,id_kota)" 
                query_alamat = query_alamat + f" VALUES ({id_alamat},'{jalan}',{in_desa},{in_kecamatan},{in_kota})"
                Koneksi_db.insert_to_db(query_alamat)
              
                #Penentuan ID Petani dan Insert
                baca_id = Koneksi_db.read_all_table(f"SELECT count(id_petani) FROM petani",2)
                for a in baca_id:
                    baca_id = list(a)
                id_petani = int('200' + str(baca_id[0]+1))
                query = "INSERT INTO petani(id_petani,nama,luas_lahan,estimasi_produksi,id_bkph,id_alamat,id_nomor_petak,id_kopi)" 
                query = query + f" VALUES ({id_petani},'{nama}',{luas_lahan},{estimasi_produksi},100,{id_alamat},{nomor_petak},{jenis_kopi})"
                Koneksi_db.insert_to_db(query)

                print("Data Berhasil Dibuat!")
                time.sleep(2)

            except:
                print("Data Gagal Dibuat")
                time.sleep(1)
                print("Silahkan Masukkan Ulang Data")
                time.sleep(2)
                Fitur_Create_Petani(role)

        else:
            Fitur_Create_Petani(role)


def Fitur_Delete_Petani(role):
    while True:
        clear()
        header()
        print("Hapus Petani? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            Fitur_data_petani(role)
        elif pilihan.lower() == 'y':
            data = Koneksi_db.read_petani()
            data_kolom = list(data.columns)
            tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
            print(tabel)
            pilihan_hapus = input("Masukkan ID Petani yang akan dihapus : ")

            akan_dihapus = Koneksi_db.read_all_table(f"SELECT id_petani,nama FROM petani where id_petani = {pilihan_hapus}")
            kolom_dihapus = list(akan_dihapus.columns)
            print(tabulate.tabulate(akan_dihapus,headers=kolom_dihapus,showindex=False,tablefmt='grid'))

            konfirmasi = input("Yakin Hapus? Y/N :")
            if konfirmasi.lower() == 'y':
                try:
                    baca_tabel = Koneksi_db.read_all_table(f"select * from petani where id_petani = {pilihan_hapus}",2)
                    for a in baca_tabel:
                        data = list(a)

                    Koneksi_db.insert_to_db(f"DELETE FROM invoice where id_petani = {pilihan_hapus}")
                    Koneksi_db.insert_to_db(f"DELETE FROM petani where id_petani = {pilihan_hapus}")
                    Koneksi_db.insert_to_db(f"DELETE FROM alamat where id_alamat = {data[6]}")
                    time.sleep(0.5)
                    print("Data Berhasil Dihapus")
                    time.sleep(2)
                except:
                    print("Data Gagal Dihapus")
                    time.sleep(1)
                    print("Silahkan Coba Lagi")
                    time.sleep(2)
            else:
                Fitur_Delete_Petani(role)


def Fitur_Update_Petani(role):
    while True:
        clear()
        header()
        print("Update Petani? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            Fitur_data_petani(role)
        elif pilihan.lower() == 'y':
            data = Koneksi_db.read_petani()
            data_kolom = list(data.columns)
            tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
            print(tabel)
            pilihan_update = input("Masukkan ID Petani yang akan Diupdate : ")

            data = Koneksi_db.read_petani(int(pilihan_update))
            data_kolom = list(data.columns)
            print(tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid'))

            konfirmasi = input("Yakin Update? Y/N :")
            if konfirmasi.lower() == 'y':
                data = Koneksi_db.read_all_table(f"Select * from petani where id_petani = {pilihan_update}",2)
                for a in data:
                    detail = list(a)
                print("Jika Tidak Ada Update Cukup Dikosongi")
                kolom = Koneksi_db.read_all_table("select * from nomor_petak")
                nama_kolom = list(kolom.columns)
                print(tabulate.tabulate(kolom,headers=nama_kolom,showindex=False,tablefmt='grid'))
                nomor_petak = input("Nomor_petak :") or detail[1]

                
                luas_lahan_baru = input("Luas Lahan :") or detail[2]
                estimasi_produksi = input("Estimasi Produksi :") or detail[3]
                pilihan_up_alamat = input("Update Alamat? Y/N :").lower()
                try:
                    match pilihan_up_alamat:
                        case 'y':
                            data_alamat = Koneksi_db.read_all_table(f"Select * from alamat where id_alamat = {detail[6]}",2)
                            for a in data_alamat:
                                detail_alamat = list(a)
                            
                            jalan_baru = input("Jalan :") or f"'{detail_alamat[1]}'"

                            desa = Koneksi_db.read_all_table('SELECT * FROM desa',1)
                            kolom_desa = list(desa.columns)
                            print(tabulate.tabulate(desa,headers=kolom_desa,showindex= False,tablefmt= 'grid'))
                            desa_baru = input("desa :") or detail_alamat[2]

                            kecamatan = Koneksi_db.read_all_table('SELECT * FROM desa',1)
                            kolom_kc = list(desa.columns)
                            print(tabulate.tabulate(kecamatan,headers=kolom_kc,showindex= False,tablefmt= 'grid'))
                            kecamatan_baru = input("Kecamatan :") or detail_alamat[3]

                            kecamatan = Koneksi_db.read_all_table('SELECT * FROM desa',1)
                            kolom_kc = list(desa.columns)
                            print(tabulate.tabulate(kecamatan,headers=kolom_kc,showindex= False,tablefmt= 'grid'))
                            kecamatan_baru = input("Kecamatan :") or detail_alamat[4]


                            Koneksi_db.insert_to_db(f"UPDATE petani SET id_nomor_petak = {nomor_petak},luas_lahan = {luas_lahan_baru}, estimasi_produksi = {estimasi_produksi} where id_petani = {pilihan_update}")
                            Koneksi_db.insert_to_db(f"UPDATE alamat SET nama_jalan = '{jalan_baru}',id_desa = {desa_baru},id_kecamatan = {kecamatan_baru} where id_alamat = {detail[6]}")
                            print("Data Berhasil Di Update")
                            time.sleep(2)
                        case _:
                            Koneksi_db.insert_to_db(f"UPDATE petani SET id_nomor_petak = {nomor_petak},luas_lahan = {luas_lahan_baru}, estimasi_produksi = {estimasi_produksi} where id_petani = {pilihan_update}")
                            print("Data Berhasil Di Update")
                            time.sleep(2)
                except:
                    print("Data Gagal Di Update")
                    time.sleep(0.5)
                    print("Silahkan Coba Lagi")
                    time.sleep(2)

            else:
                Fitur_Update_Petani(role)

        else:
            Fitur_Update_Petani(role)

Fitur_data_petani(1)
            
# baca_tabel = Koneksi_db.read_all_table(f"select * from alamat where id_alamat = 1",2)
# for a in baca_tabel:
#     data = list(a)
# print(data)

# desa = Koneksi_db.read_all_table('SELECT * FROM desa',1)
# kolom_desa = list(desa.columns)
# print(tabulate.tabulate(desa,headers=kolom_desa,showindex= False,tablefmt= 'grid'))
# in_desa = input("Masukkan Desa* (ID):")
            

# id_alamat = Koneksi_db.read_all_table(f"SELECT count(id_alamat) FROM alamat",2)
# for a in id_alamat:
#     id_alamat = list(a)
# print(id_alamat)

# data = Koneksi_db.read_all_table(f"Select * from petani where id_petani = 1",2)
# for a in data:
#     detail = list(a)
# print(detail)
# data_alamat = Koneksi_db.read_all_table(f"Select * from alamat where id_alamat = {detail[6]}",2)
# for a in data_alamat:
#     detail_alamat = list(a)
# print(detail_alamat)

# Koneksi_db.insert_to_db(f"UPDATE petani SET id_nomor_petak = 1 ,luas_lahan = 3, estimasi_produksi = 3 where id_petani = 1 ")
# Koneksi_db.insert_to_db(f"UPDATE alamat SET nama_jalan = 'jalsalla',id_desa = 1 ,id_kecamatan = 1 where id_alamat = {detail[6]}")