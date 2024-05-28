import psycopg2
import pandas as pd
import tabulate

connStr = psycopg2.connect(database='KopiKazz', user= 'postgres',password='010105',host='localhost',port=5432)
#cur = connStr.cursor()

def read_all_table(query,df = 1):
    cur = connStr.cursor()
    cur.execute(query=query)
    nama_kolom =[desc[0] for desc in cur.description]
    data = cur.fetchall()
    try:
        tabel_data = pd.DataFrame(data)
        tabel_data.columns = nama_kolom
    #tabel_data = tabulate.tabulate(data,headers=nama_kolom,tablefmt="grid",showindex=False)
    except :
        tabel_data = data
    cur.close()
    if df == 1:
        return tabel_data
    elif df == 2:
        return data

def read_petani(id=0): # Untuk Membaca Tabel Petani
    cur = connStr.cursor()
    query = """
    SELECT p.id_petani as "ID" ,p.nama as "Nama Petani", p.luas_lahan as "Luas Lahan",p.estimasi_produksi "Estimasi",
    b.nama_bkph BKPH,np.nomor_petak "Petak",concat(a.nama_jalan,' ',ds.nama_desa,' ',kc.nama_kecamatan,' ',kt.nama_kota) as Alamat, b.nama_bkph as BKPH
    FROM petani p 
    JOIN bkph b on(p.id_bkph = b.id_bkph)
    JOIN jenis_kopi jk on (p.id_kopi = jk.id_jenis_kopi)
    JOIN alamat a on(p.id_alamat = a.id_alamat)
    JOIN desa ds on(a.id_desa = ds.id_desa)
    JOIN kota kt on(a.id_kota = kt.id_kota)
    JOIN kecamatan kc on(a.id_kecamatan = kc.id_kecamatan)
    JOIN nomor_petak np on(p.id_nomor_petak = np.id_nomor_petak)"""
    if id > 0 :
        query = query + f" WHERE p.id_petani = {id}"
    cur.execute(query=query)
    nama_kolom =[desc[0] for desc in cur.description]
    data = cur.fetchall()
    
    tabel_data = pd.DataFrame(data)
    tabel_data.columns = nama_kolom
    # tabel_data = tabulate.tabulate(data,headers=nama_kolom,tablefmt="grid",showindex=False)
    cur.close()
    return tabel_data

def read_admin():
    cur = connStr.cursor()
    query = """
    SELECT a.id_admin as ID, a.nama as "Nama Lengkap", b.nama_bkph as BKPH
    FROM admin a JOIN bkph b on(a.id_bkph = b.id_bkph)"""
    cur.execute(query=query)
    nama_kolom =[desc[0] for desc in cur.description]
    data = cur.fetchall()
    tabel_data = pd.DataFrame(data)
    tabel_data.columns = nama_kolom
    # tabel_data = tabulate.tabulate(data,headers=nama_kolom,tablefmt="grid",showindex=False)
    cur.close()
    return tabel_data 

def read_tim(id=0):
    cur = connStr.cursor()
    query = """
    SELECT tt.id_tim_taksasi as ID, tt.nama as "Nama Lengkap", b.nama_bkph as BKPH
    FROM tim_taksasi tt JOIN bkph b on(tt.id_bkph = b.id_bkph)"""
    if id > 0 :
        query = query + f" WHERE tt.id_tim_taksasi = {id}"
    cur.execute(query)
    nama_kolom =[desc[0] for desc in cur.description]
    data = cur.fetchall()
    tabel_data = pd.DataFrame(data)
    tabel_data.columns = nama_kolom
    # tabel_data = tabulate.tabulate(data,headers=nama_kolom,tablefmt="grid",showindex=False)
    cur.close()
    return tabel_data 


def read_invoice(id=0):
    cur = connStr.cursor()
    query = """
    SELECT i.id_invoice "ID", i.tanggal_terbit "Terbit",i.jatuh_tempo "Jatuh Tempo",
    jk.jenis_kopi "Jenis Kopi",p.estimasi_produksi "Total Panen", sum(p.estimasi_produksi * 0.3) as "Tagihan (Kg)",
    sum(p.estimasi_produksi * 0.3 * jk.harga_kopi) as "Tagihan (Rp)",
    st.status_tagihan "Status Tagihan"
    FROM invoice i JOIN petani p on(i.id_petani = p.id_petani)
    JOIN admin a on(a.id_admin = i.id_admin) 
    JOIN status_tagihan st on(st.id_status_tagihan = i.id_status_tagihan)
    JOIN jenis_kopi jk on(p.id_kopi = jk.id_jenis_kopi)
    Group by p.id_petani,i.id_invoice,jk.id_jenis_kopi,st.id_status_tagihan"""
    if id>0:
        query = query + f" having i.id_invoice = {id}"
    cur.execute(query=query)
    nama_kolom =[desc[0] for desc in cur.description]
    data = cur.fetchall()
    tabel_data = pd.DataFrame(data)
    tabel_data.columns = nama_kolom
    # tabel_data = tabulate.tabulate(data,headers=nama_kolom,tablefmt="grid",showindex=False)
    cur.close()
    return tabel_data 

def create_invoice(id_invoice,id_petani,rentang_hari,id_admin,id_status_tagihan):
    cur = connStr.cursor()
    query = f"INSERT INTO invoice(id_invoice,tanggal_terbit,jatuh_tempo,id_petani,id_admin,id_status_tagihan) VALUES({id_invoice},now(),now()+'{rentang_hari} day',{id_petani},{id_admin},{id_status_tagihan})"
    cur.execute(query)
    connStr.commit()
    cur.close()
    # try:
    #     print((id_petani))
    # except:
    #     print("Data Gagal Ditambah")

def insert_to_db(query):
    cur = connStr.cursor()
    query = query 
    cur.execute(query)
    connStr.commit()
    cur.close()



