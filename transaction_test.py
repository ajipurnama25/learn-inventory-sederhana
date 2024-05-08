from __future__ import print_function
from auth import spreadsheet_service

def read_stock():
    range_name = 'stock barang!A2:H'  # Baca data barang dari tab "stock barang"
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    return rows

def read_harga_barang():
    range_name = 'harga barang!A2:D'  # Baca data harga barang dari tab "harga barang"
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    return rows

def update_stock(new_stock):
    range_name = 'stock barang!A2:C'  # Update data barang di tab "stock barang"
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    value_input_option = 'USER_ENTERED'
    body = {'values': new_stock}
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    return result

def inpuser():
    inp = int(input("Masukkan jumlah data yang ingin dibeli: "))
    data = []
    for x in range(inp):
        nama_barang = input(f"Masukkan nama barang yang ingin dibeli {x+1}: ")
        jumlah_beli = int(input(f"Masukkan jumlah barang yang ingin dibeli untuk {nama_barang}: "))
        data.append([nama_barang, jumlah_beli])
    return data

def process_transaction():
    input_data = inpuser()
    stock_data = read_stock()
    harga_barang_data = read_harga_barang()  # Baca data harga barang
    total_pembayaran = 0  # Inisialisasi total pembayaran

    for nama_barang, jumlah_beli in input_data:
        for i, row in enumerate(stock_data):
            if row[1] == nama_barang:
                current_stock = int(row[2])
                if jumlah_beli <= current_stock:
                    stock_data[i][2] = str(current_stock - jumlah_beli)  # Kurangi stok
                    update_stock(stock_data)
                    
                    # Temukan harga barang yang sesuai
                    for harga_barang_row in harga_barang_data:
                        if harga_barang_row[1] == nama_barang:
                            harga_barang = int(harga_barang_row[3])
                            total_pembayaran += jumlah_beli * harga_barang  # Hitung total pembayaran
                            break
                    
                    print("Transaksi berhasil! Stok barang telah diperbarui.")
                    break
                else:
                    print(f"Maaf, stok barang {nama_barang} tidak mencukupi untuk jumlah yang diminta.")
                    break
            
        else:
            print(f"Barang {nama_barang} tidak ditemukan dalam stok.")
    
    # Cetak total pembayaran
    print(f"Total pembayaran yang anda lakukan: Rp.{total_pembayaran}")

if __name__ == '__main__':
    process_transaction()
