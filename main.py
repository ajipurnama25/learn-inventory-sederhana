from __future__ import print_function
from auth import spreadsheet_service
from gui2 import get_user_input, show_info_message, show_error_message

def read_stock():
    range_name = 'master item!A2:H'  # Read data from the "stock barang" sheet
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    return rows

def read_price():
    range_name = 'item price!A2:H'  # Read data from the "harga barang" sheet
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    return rows

def update_stock(new_stock):
    range_name = 'master item!A2:H'  # Update data in the "stock barang" sheet
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    value_input_option = 'USER_ENTERED'
    body = {'values': new_stock}
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    return result

def process_transaction():
    nama_user, input_data = get_user_input()
    stock_data = read_stock()
    price_data = read_price()
    harga_total = 0
    transaction_data = []
    
    for nama_barang, jumlah_beli in input_data:
        found = False
        for i, row in enumerate(stock_data):
            if row[1] == nama_barang:
                found = True
                current_stock = int(row[2])
                if jumlah_beli <= current_stock:
                    stock_data[i][2] = str(current_stock - jumlah_beli)  # Update stock
                    update_stock(stock_data)
                    show_info_message("Success", "Transaksi berhasil! Stok barang telah diperbarui.")
                    
                    # Find the price of the item
                    for price_row in price_data:
                        if price_row[1] == nama_barang:
                            harga_barang = float(price_row[3].replace(',', ''))  # Remove comma and convert to float
                            total_harga = jumlah_beli * harga_barang
                            harga_total += total_harga
                            
                            # Add transaction data to the list
                            transaction_data.append([nama_user, nama_barang, jumlah_beli, harga_barang, total_harga])
                            break
                    else:
                        show_error_message("Error", f"Harga barang untuk {nama_barang} tidak ditemukan.")
                    
                    break
                else:
                    show_error_message("Error", f"Maaf, stok barang {nama_barang} tidak mencukupi untuk jumlah yang diminta.")
                    break
        
        if not found:
            show_error_message("Error", f"Barang {nama_barang} tidak ditemukan dalam stok.")
    
    return transaction_data, harga_total

def save_transaction(transaction_data):
    range_name = 'transaction!A2:E'  # Update transaction data in the "transaction" sheet
    spreadsheet_id = '10YgWzGWXBtVvlLRnPyZAZ-xmt0cNZZwRu_23wgqyccw'
    value_input_option = 'USER_ENTERED'
    body = {'values': transaction_data}
    result = spreadsheet_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    return result

if __name__ == '__main__':
    transaction_data, total_harga = process_transaction()
    show_info_message("Total Pembayaran", f"Total pembayaran yang anda lakukan: Rp.{total_harga}")
    
    # Add transaction data to Google Sheets
    save_transaction(transaction_data)
