import Koneksi_db
import time
import tabulate

# print("Hapus Petani? [Y/N] : ")
# pilihan = input("Masukkan Pilihan :")
# if pilihan.lower() == 'n':
#     print('batal')
# elif pilihan.lower() == 'y':
#     data = Koneksi_db.read_petani()
#     data_kolom = list(data.columns)
#     tabel = tabulate.tabulate(data,headers=data_kolom,showindex=False,tablefmt='grid')
#     print(tabel)
#     pilihan_hapus = input("Masukkan ID Petani yang akan dihapus : ")

#     akan_dihapus = Koneksi_db.read_all_table(f"SELECT id_petani,nama FROM petani where id_petani = {pilihan_hapus}")
#     kolom_dihapus = list(akan_dihapus.columns)
#     print(tabulate.tabulate(akan_dihapus,headers=kolom_dihapus,showindex=False,tablefmt='grid'))

#     konfirmasi = input("Yakin Hapus? Y/N :")
#     if konfirmasi.lower() == 'y':
#         # try:
#         baca_tabel = Koneksi_db.read_all_table(f"select * from petani where id_petani = {pilihan_hapus}",2)
#         for a in baca_tabel:
#                     data = list(a)
#         Koneksi_db.insert_to_db(f"DELETE FROM invoice where id_petani = {pilihan_hapus}")
#         Koneksi_db.insert_to_db(f"DELETE FROM petani where id_petani = {pilihan_hapus}")
#         Koneksi_db.insert_to_db(f"DELETE FROM alamat where id_alamat = {data[6]}")
#         time.sleep(0.5)
#         print("Data Berhasil Dihapus")
#         time.sleep(2)
#         # except:
#         #     print("Data Gagal Dihapus")
#         #     time.sleep(1)
#         #     print("Silahkan Coba Lagi")
#         #     time.sleep(2)
#     else:
#         print(';a')




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
    if True:
                #Penentuan ID Alamat dan Insert
        
        id_alamat = Koneksi_db.read_all_table(f"SELECT max(id_alamat) FROM alamat",2)
        for a in id_alamat:
            id_alamat = list(a)
        id_alamat = int('310' + str(id_alamat[0]+1))
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