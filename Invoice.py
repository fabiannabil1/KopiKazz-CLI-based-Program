import pandas as pd
import time
import tabulate
import Koneksi_db
import os

def clear():
    os.system('cls')

def header():
    with open('UI\Header.txt','r',encoding='utf-8') as header:
        header = header.read()
        print(header)

def fitur_data_invoice():
    clear()
    header()
    a = '''
|                1. Terbitkan Invoice           |
|                2. Update Status Tagihan       |
|                3. Hapus Invoice               |
|                4. Lihat Invoice               |
|                x. Kembali                     |
================================================='''
    print(a)
    print("Kelola Invoice".center(49))
    pilihan = input("Masukkan Pilihan :")
    match pilihan:
        case '1': 
            Fitur_Create_invoice()
        case '2': 
            fitur_update_invoice()
        case '3': 
            fitur_delete_Invoice()
        case '4': 
            try:
                file = Koneksi_db.read_invoice()
                Fitur_read_invoice(file)
            except:
                print("Belum ada data")
                time.sleep(1)
                fitur_data_invoice()
        case 'x':
            print('kembali ke menu awal')
        case _: 
            fitur_data_invoice()

def fitur_update_invoice():
   while True:
        clear()
        header()
        print("Update Status Tagihan? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            fitur_data_invoice()
        elif pilihan.lower() == 'y':
            data = Koneksi_db.read_invoice()
            data_kolom = list(data.columns)
            tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
            print(tabel)
            pilihan_update = input("Masukkan ID invoice yang akan diupdate : ")

            akan_diup = Koneksi_db.read_invoice(int(pilihan_update))
            kolom_diup = list(akan_diup.columns)
            print(tabulate.tabulate(akan_diup,headers=kolom_diup,showindex=False,tablefmt='grid'))

            konfirmasi = input("Yakin Update? Y/N :")
            if konfirmasi.lower() == 'y':
                try:
                    s_t = Koneksi_db.read_all_table("select * from status_tagihan",1)
                    kolom_s_t = list(s_t.columns)
                    print(tabulate.tabulate(s_t, headers= kolom_s_t, showindex= False, tablefmt= 'grid'))
                    st = input("Status Tagihan :")

                    Koneksi_db.insert_to_db(f"UPDATE invoice SET id_status_tagihan = {st} where id_invoice = {pilihan_update}")
                    time.sleep(0.5)
                    print("Data Berhasil Diupdate")
                    time.sleep(2)
                except:
                    print("Data Gagal Diupdate")
                    time.sleep(1)
                    print("Silahkan Coba Lagi")
                    time.sleep(2)
            else:
                fitur_update_invoice()


def Fitur_read_invoice(file): # Paginiation parameter berbentuk list
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
                    fitur_data_invoice()

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

def Fitur_Create_invoice():
    clear()
    header()
    while True:
        print("Tambahkan Invoice? [Y/N] : ")
        pilihan = input('Pilihan : ')
        if pilihan.lower() == 'n':
            fitur_data_invoice()
        elif pilihan.lower() == 'y':
            id = 1

            petani = Koneksi_db.read_all_table(f"SELECT id_petani,nama FROM petani")
            kolom_petani = list(petani.columns)
            print(tabulate.tabulate(petani,headers=kolom_petani,showindex=False,tablefmt='grid'))

            petani  = input("ID Petani             :")
            rentang = input("Rentang Hari (angka)  :") or '60'
            id_admin = 1000

            st = Koneksi_db.read_all_table("select * from status_tagihan",1)
            kolom_st = list(st.columns)
            print(tabulate.tabulate(st, headers= kolom_st, showindex= False, tablefmt= 'grid'))
            status_tagihan = input("Status Tagihan :")

            try:
                try:
                    id_invoice = Koneksi_db.read_all_table(f"SELECT max(id_invoice) FROM invoice",2)
                    for a in id_invoice:
                        id_invoice = list(a)
                    id_invoice = id_invoice[0] + 1
                except :
                    id_invoice = 10

                Koneksi_db.create_invoice(id_invoice,petani,rentang,id_admin,status_tagihan)
                print("Data Berhasil Dibuat!")
                time.sleep(2)
            except :
                print("Data Gagal Dibuat !")
                time.sleep(2)
                Fitur_Create_invoice
        else:
            Fitur_Create_invoice()

def fitur_delete_Invoice():
     while True:
        clear()
        header()
        print("Hapus Petani? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            fitur_data_invoice()
        elif pilihan.lower() == 'y':
            data = Koneksi_db.read_invoice()
            data_kolom = list(data.columns)
            tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
            print(tabel)
            pilihan_hapus = input("Masukkan ID invoice yang akan dihapus : ")

            akan_dihapus = Koneksi_db.read_invoice(int(pilihan_hapus))
            kolom_dihapus = list(akan_dihapus.columns)
            print(tabulate.tabulate(akan_dihapus,headers=kolom_dihapus,showindex=False,tablefmt='grid'))

            konfirmasi = input("Yakin Hapus? Y/N :")
            if konfirmasi.lower() == 'y':
                try:
                    Koneksi_db.insert_to_db(f"DELETE FROM invoice where id_invoice = {pilihan_hapus}")
                    time.sleep(0.5)
                    print("Data Berhasil Dihapus")
                    time.sleep(2)
                except:
                    print("Data Gagal Dihapus")
                    time.sleep(1)
                    print("Silahkan Coba Lagi")
                    time.sleep(2)
            else:
                fitur_delete_Invoice()
