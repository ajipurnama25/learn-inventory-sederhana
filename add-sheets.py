from __future__ import print_function
from auth import spreadsheet_service

def read_range():
    range_name = 'add harga!A1:H'  # Baca seluruh data yang ada
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))
    print('{0} rows retrieved.'.format(rows))
    return rows

def inpuser():
    new_data = []
    n = int(input("Masukkan jumlah baris data yang ingin dimasukkan: "))
    for i in range(n):  
        id_barang = input(f"Masukkan ID untuk baris ke-{i+1}: ")
        nama_barang = input(f"Masukkan Nama Barang untuk baris ke-{i+1}: ")
        harga_barang = input(f"Masukkan Harga Barang untuk baris ke-{i+1}: ")
        new_data.append([id_barang, nama_barang, harga_barang])
    return new_data

def write_range(new_data):
    last_row = len(read_range()) + 1  # Baris terakhir yang terisi + 1
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    range_name = f'add stock!A{last_row}:H'  # Menulis data baru mulai dari baris terakhir yang kosong
    value_input_option = 'USER_ENTERED'
    body = {'values': new_data}
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    new_data = inpuser()  # Mendapatkan input data dari pengguna
    write_range(new_data)
    read_range()  # Membaca data yang ada setelah penambahan data baru
