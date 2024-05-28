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

def Fitur_data_pegawai(): ## nanti buat pemisah akses fitur 
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
                    print("create")
                case '2' : # Lihat
                    file = Koneksi_db.read_pegawai()
                    Fitur_read_pegawai(file)
                case '3' : # Update
                    #Fitur_Update_Petani()
                case '4' : # Delete
                    #Fitur_Delete_Petani()
                case 'x' :
                    main.menu_admin()
                case _ :
                    Fitur_data_pegawai()

def Fitur_read_pegawai(file): # Paginiation parameter berbentuk list
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
                    Fitur_data_pegawai()

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

def Fitur_Create_Petani(role):
    clear()
    header()
    while True:
        print("Tambahkan Petani? [Y/N] : ")
        pilihan = input('Pilihan : ')
        if pilihan.lower() == 'n':
            Fitur_data_pegawai()
        elif pilihan.lower() == 'y':
            nama_petani = input("Nama Petani :")
            luas_lahan = int(input("Masukkan Luas Lahan :"))

            # Tampilkan Nomor Petak
            nomor_petak = Koneksi_db.read_all_table('SELECT * FROM nomor_petak',1)
            kolom_petak = list(nomor_petak.columns)
            print(tabulate.tabulate(nomor_petak,headers=kolom_petak,showindex= False,tablefmt= 'grid'))
            nomor_petak = input("Masukkan Nomor Petak* :")

            estimasi_produksi = int(input("Masukkan Estimasi Produksi* :"))

            # Tampilkan Jenis Kopi
            kopi = Koneksi_db.read_all_table('SELECT * FROM jenis_kopi',1)
            kolom_kopi = list(kopi.columns)
            print(tabulate.tabulate(kopi,headers=kolom_kopi,showindex= False,tablefmt= 'grid'))
            jenis_kopi = int(input("Masukkan Jenis Kopi* (ID):"))

            # Masukkan Data Petani
            print("Masukkan Alamat (* wajib diisi):")
            jalan = input("Masukkan Jalan* :")
            desa = input("Masukkan Desa* :")
            kecamatan = input("Masukkan Kecamatan* :")
            kota = input("Masukkan Kota :")
            provinsi = input("Masukkan Provinsi :")
            kode_pos = input("Masukkan Kode Pos :")
            try:
                #Penentuan ID Alamat dan Insert
                id_alamat = Koneksi_db.read_all_table(f"SELECT count(id_alamat) FROM alamat",2)
                for a in id_alamat:
                    id_alamat = list(a)
                id_alamat = int('310' + str(id_alamat[0]+1))
                query_alamat= "INSERT INTO alamat(id_alamat,jalan,desa,kecamatan,kabupaten,provinsi,kode_pos)" 
                query_alamat = query_alamat + f" VALUES ({id_alamat},'{jalan}','{desa}','{kecamatan}','{kota}','{provinsi}',{kode_pos})"
                Koneksi_db.insert_to_db(query_alamat)

                #Penentuan ID Petani dan Insert
                baca_id = Koneksi_db.read_all_table(f"SELECT count(id_petani) FROM petani",2)
                for a in baca_id:
                    baca_id = list(a)
                id_petani = int('200' + str(baca_id[0]+1))
                query = "INSERT INTO petani(id_petani,nama_petani,luas_lahan,estimasi_produksi,id_bkph,id_alamat,id_nomor_petak,id_jenis_kopi)" 
                query = query + f" VALUES ({id_petani},'{nama_petani}',{luas_lahan},{estimasi_produksi},1,{id_alamat},{nomor_petak},{jenis_kopi})"
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
