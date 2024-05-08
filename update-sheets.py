from __future__ import print_function
from auth import spreadsheet_service

def read_range():
    range_name = 'stock barang!A1:H'  # Baca baris kosong untuk data baru
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))
    print('{0} rows retrieved.'.format(rows))
    return rows

def inpuser():
    new_data = []
    n = int(input("Masukkan jumlah data yang ingin dimasukkan: "))
    for i in range(n):  
        # id_barang = input(f"Masukkan ID untuk baris ke-{i+1}: ")
        # nama_barang = input(f"Masukkan Nama Barang untuk baris ke-{i+1}: ")
        jumlah_barang = input(f"Masukkan jumlah stock untuk baris ke-{i+1}: ")
        # new_data.append([id_barang, nama_barang, jumlah_barang])
        new_data.append([jumlah_barang])
    return new_data

if __name__ == '__main__':
    read_range()  # Membaca data yang ada sebelumnya
    new_data = inpuser()  # Mendapatkan input data dari pengguna
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    range_name = 'stock barang!A2:H'  # Menulis data baru mulai dari baris kedua
    value_input_option = 'USER_ENTERED'
    body = {'values': new_data}
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
