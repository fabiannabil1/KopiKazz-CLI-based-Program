import Koneksi_db
import os
import time
import tabulate
# import Petani

def clear():
    os.system('cls')

def header():
    with open('UI\Header.txt','r',encoding='utf-8') as header:
        header = header.read()
        print(header)


def verifikasi_user_dgn_db(username,password):
    query = f"SELECT username,password FROM admin WHERE username = '{username}' and password = '{password}'"
    data = Koneksi_db.read_all_table(query,2)
    check = False
    for a in data:
        data = list(a)
    if data == []:
        query_tim = f"SELECT username,password FROM tim_taksasi WHERE username = '{username}' and password = '{password}'"
        data_tim = Koneksi_db.read_all_table(query_tim,2)
        for a in data_tim:
            data_tim = list(a)
        if data_tim == [] :
            return check
        else:
            check = True
            return [check,2]
    else :
        check = True
        return [check,1]
    
        
    
def menu_admin(nama_admin='a'): # Menu untuk Admin
    clear()
    header()
    with open('UI\Menu Admin.txt','r',encoding='utf-8') as ui_admin:
        ui_admin = ui_admin.read()
        print(ui_admin)
    print(f"Selamat Datang {(nama_admin).upper()}".center(49))
    pilihan = input("Menu yang dituju :")
    match pilihan:
        case '1' :
            clear()
            Petani.Fitur_data_petani(1)
        case '2' :
            print('Invoice')
        case '3' :
            print('Kopi')
        case '4' :
            print('Pegawai')
        case '5' :
            pesan_logout()
            time.sleep(2)
            clear()
        case _ :
            menu_admin()

def menu_tim(nama_tim='a'): # Menu untuk tim 
    clear()
    header()
    print(f"Selamat Datang {(nama_tim).upper()}".center(49))
    pilihan = input("Menu yang dituju :")
    match pilihan:
        case '1' :
            print('Data Petani')
        case '2' :
            print('Invoice')
        case '3' :
            pesan_logout()
            time.sleep(2)
            clear()
        case _ :
            menu_tim()

def pesan_logout():
    with open('UI\Pesan Logout.txt','r',encoding='utf-8') as pesan:
        pesan = pesan.read()
        print(pesan.center(49))

def menu_Awal():# Menu awal pembuka 
    clear()
    header()
    with open('UI\Tampilan Awal.txt','r',encoding='utf-8') as ui_awal:
        ui_awal = ui_awal.read()
        print(ui_awal)
    input_user = input("Pilihan Anda :")
    match input_user:
        case '1':
            menu_login()
        case '2':
            print('registrasi')
        case '3':
            pesan_logout()
            time.sleep(2)
            exit()
        case _:
            menu_Awal()     

coba_login = 1
def menu_login():
    global coba_login
    clear()
    header()
    print((f"MASUKKAN USERNAME DAN PASSWORD\nPercobaan Login ke {coba_login}").center(49))

    username = input("USERNAME :")
    if username == '':
        print('Username kosong!')
        time.sleep(1)
        menu_login()
    password = input("PASSWORD :")
    if password == '':
        print("Password  kosong!")
        time.sleep(1)
        menu_login()

    check = verifikasi_user_dgn_db(username,password)
    pesan = "Login Berhasil!"
    if coba_login < 3:
        try:
            if check[1] == 1:
                print(pesan)
                time.sleep(1)
                menu_admin(username)

            elif check[1] == 2:
                menu_tim()
                time.sleep(1)
                menu_tim(username)
        except:
            print('Login Gagal\nUsername/Password tidak ditemukan\nSilahkan Login Ulang')
            time.sleep(2)
            coba_login += 1
            menu_login()
    else:
        print('Kesalahan Login Sebanyak 3 Kali\nSilahkan Coba Beberapa Saat Lagi!'.center(49))
        for a in range(30):
            time.sleep(1)
            print(str(a).center(49))
        coba_login = 0
        menu_Awal()

if __name__ == "__main__":
    menu_Awal()
#     menu_admin('fabian')