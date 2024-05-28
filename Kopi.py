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

def lihat_Update_kopi(role):
    clear()
    header()
    print("Data Kopi".center(49))
    a = Koneksi_db.read_all_table("Select * From jenis_kopi")
    kolom_a = list(a.columns)
    print(tabulate.tabulate(a,headers=kolom_a,showindex=False,tablefmt='grid'))
    if role == 1 :
        pilihan= input("[t] untuk kembali, [u] update:").lower()
        match pilihan:
            case 't':
                print('menu')
            case 'u':
                print('Update Harga dan PNBP')
                pilihan_update = input("Masukkan ID Kopi yang akan di Update:")
                kopi = Koneksi_db.read_all_table(f"SELECT * FROM jenis_kopi where id_jenis_kopi = {pilihan_update}",2)
                for a in kopi:
                    kopi = list(a)
                harga_baru = input("Masukkan Harga Baru :") or kopi[2]
                pnbp_baru = input("Masukkan PNBP Baru :") or kopi[3] 
                Koneksi_db.insert_to_db(f"Update jenis_kopi set harga_kopi = {harga_baru}, pnbp = {pnbp_baru} where id_jenis_kopi = {pilihan_update}")
                print("Data Berhasil Di Update")
                time.sleep(2)
                lihat_Update_kopi(role)
            case _ :
                lihat_Update_kopi(role)
    else:
        pilihan= input("[t] untuk kembali :")
        match pilihan:
            case 't':
                print('menu')
            case _:
                lihat_Update_kopi(role)

lihat_Update_kopi(2)