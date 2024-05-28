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


#________________________________________________________________________
Kode_Registrasi_Admin = "PERHUTANI"
#________________________________________________________________________


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
    
        
    
def menu_admin(role=1): # Menu untuk Admin | 1 --> role
    clear()
    header()
    with open('UI\Menu Admin.txt','r',encoding='utf-8') as ui_admin:
        ui_admin = ui_admin.read()
        print(ui_admin)
    print(f"Selamat Datang".center(49))
    pilihan = input("Menu yang dituju :")
    match pilihan:
        case '1' :
            clear()
            Fitur_data_petani(1)
        case '2' :
            fitur_data_invoice(1)
        case '3' :
            lihat_Update_kopi(1)
        case '4' :
            Fitur_data_tim()
        case '5' :
            pesan_logout()
            time.sleep(2)
            clear()
            menu_Awal()
            
        case _ :
            menu_admin()

def menu_tim(): # Menu untuk tim | 2 -> role
    clear()
    header()
    with open('UI\Menu Tim.txt','r',encoding='utf-8') as ui_tim:
        ui_tim = ui_tim.read()
    print(ui_tim)
    print(f"Selamat Datang".center(49))
    pilihan = input("Menu yang dituju :")
    match pilihan:
        case '1' :
            Fitur_data_petani(2)
        case '2' :
            fitur_data_invoice(2)
        case '3' :
            lihat_Update_kopi(2)
        case '4' :
            pesan_logout()
            time.sleep(2)
            menu_Awal()
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
            registrasi_admin()
        case '3':
            pesan_logout()
            time.sleep(2)
            clear()
            exit()
        case _:
            menu_Awal()     


def registrasi_admin():
    id_default_tim = 1000
    clear()
    header()
    print("Registrasi Admin Kopi Perhutani".center(49))
    print("Untuk Perbaikan Data Admin Ketik [u]")
    input_opsi = input("Lakukan Registrasi? Y/N: ").lower()
    match input_opsi:
        case 'y':
            input_regis = input("Masukkan Kode Registrasi :")
            if input_regis == Kode_Registrasi_Admin:
                input_nama = input("Masukkan Nama Admin :")
                input_user = input("Masukkan Username   :")
                input_pass = input("Masukkan Password   :")
                id_bkph = 100
                try :
                    Koneksi_db.insert_to_db(f"INSERT INTO admin(id_admin,nama,username,password,id_bkph) VALUES(1000,'{input_nama}','{input_user}','{input_pass}',{id_bkph})")
                    print("ADMIN BERHASIL DIBUAT!")
                    time.sleep(2)
                    menu_Awal()
                except:
                    print("ADMIN GAGAL DIBUAT !")
                    time.sleep(0.5)
                    print("Silahkan Coba Lagi")
                    time.sleep(1)
                    registrasi_admin()
            else:
                print("Kode Salah!")
                time.sleep(1)
                registrasi_admin()

        case 'n':
            menu_Awal()
        case 'u':
            try:
                kode = input("Masukkan Kode Registrasi :")
                if kode == Kode_Registrasi_Admin:
                    data = Koneksi_db.read_all_table(f"Select * from admin where id_admin = {id_default_tim}",2)
                    for a in data:
                        detail = list(a)
                    print("Jika Tidak Ada Update Cukup Dikosongi")
                    nama_baru = input("Perbaiki Nama Lengkap : ") or detail[1]
                    user_baru = input("Masukkan Username Baru: ") or detail[2]
                    pass_baru = input("Masukkan Password Baru: ") or detail[3]
                    try:
                        Koneksi_db.insert_to_db(f"UPDATE admin SET nama = '{nama_baru}', username = '{user_baru}',password = '{pass_baru}'")
                        print("Data Berhasil Di Update")
                        time.sleep(2)
                        menu_Awal()
                    except:
                        print("Data Gagal Di Update")
                        time.sleep(0.5)
                        print("Silahkan Coba Lagi")
                        time.sleep(2)
                        registrasi_admin()
                else:
                    print("Kode Salah!")
                    time.sleep(1)
                    registrasi_admin()
            except:
                print("Akun Admin Belum Dibuat !")
                time.sleep(2)
                registrasi_admin()
        case _ : 
            registrasi_admin()
            


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

################################################################################ KOPI KOPI #####################################################################################
        
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
                menu_admin()
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
                menu_tim()
            case _:
                lihat_Update_kopi(role)

################################################################################ PETANI PETANI #####################################################################################
        
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
            # nama_kolom = list(file.columns)
            a = tabulate.tabulate(tampilkan_per_halaman(n),tablefmt="grid",showindex=False)
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
                try:
                    file = Koneksi_db.read_petani()
                    Fitur_read_petani(file,role)
                except:
                    print('Belum ada data')
                    Fitur_data_petani()
            case '3' : # Update
                Fitur_Update_Petani(role)
            case '4' : # Delete
                Fitur_Delete_Petani(role)
            case 'x' :
                if role == 1:
                    menu_admin()
                else:
                    menu_tim()
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
                    menu_admin()
                else:
                    menu_tim()
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
                try:
                    id_alamat = Koneksi_db.read_all_table(f"SELECT max(id_alamat) FROM alamat",2)
                    for a in id_alamat:
                        id_alamat = list(a)
                    id_alamat = id_alamat[0]+1
                except:
                    id_alamat = 3000
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

################################################################################ TIM TIM TIM TIM #####################################################################################
        
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
                    menu_admin()
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


################################################################################ INVOICE INVOICE  #####################################################################################

def fitur_data_invoice(role):
    clear()
    header()
    a = '''
|                1. Terbitkan Invoice           |
|                2. Update Status Tagihan       |
|                3. Hapus Invoice               |
|                4. Lihat Invoice               |
|                x. Kembali                     |
================================================='''
    b ='''
|                1. Update Status Tagihan       |
|                2. Lihat Invoice               |
|                x. Kembali                     |
================================================='''
    if role == 1:
        print(a)
        print("Kelola Invoice".center(49))
        pilihan = input("Masukkan Pilihan :")
        match pilihan:
            case '1': 
                Fitur_Create_invoice(role)
            case '2': 
                fitur_update_invoice(role)
            case '3': 
                fitur_delete_Invoice(role)
            case '4': 
                try:
                    file = Koneksi_db.read_invoice()
                    Fitur_read_invoice(file)
                except:
                    print("Belum ada data")
                    time.sleep(1)
                    fitur_data_invoice(role)
            case 'x':
                menu_admin()
            case _: 
                fitur_data_invoice(role)
    else :
        print(b)
        print("Kelola Invoice".center(49))
        pilihan = input("Masukkan Pilihan :")
        match pilihan:
            case '1': 
                fitur_update_invoice(role)
            case '2': 
                try:
                    file = Koneksi_db.read_invoice()
                    Fitur_read_invoice(file)
                except:
                    print("Belum ada data")
                    time.sleep(1)
                    fitur_data_invoice(role)
            case 'x':
                menu_tim()
            case _: 
                fitur_data_invoice(role)

def fitur_update_invoice(role):
   while True:
        clear()
        header()
        print("Update Status Tagihan? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            fitur_data_invoice(role)
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
                fitur_update_invoice(role)


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
                    fitur_data_invoice(role)

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

def Fitur_Create_invoice(role):
    clear()
    header()
    while True:
        print("Tambahkan Invoice? [Y/N] : ")
        pilihan = input('Pilihan : ')
        if pilihan.lower() == 'n':
            fitur_data_invoice(role)
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
                Fitur_Create_invoice(role)
        else:
            Fitur_Create_invoice(role)

def fitur_delete_Invoice(role):
     while True:
        clear()
        header()
        print("Hapus Petani? [Y/N] : ")
        pilihan = input("Masukkan Pilihan :")
        if pilihan.lower() == 'n':
            fitur_data_invoice(role)
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
                fitur_delete_Invoice(role)


if __name__ == "__main__":
    menu_Awal()
#     menu_admin('fabian')