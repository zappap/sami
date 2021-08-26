import tabula
import pandas as pd
import zipfile
import easygui
import xlwings as xw
import datetime
import os

filename = easygui.fileopenbox(msg="Birlestirilmis Listeyi (PDF) Seciniz", filetypes="*.pdf")
path = os.sep.join(filename.split(os.sep)[:-1])
belge_no = easygui.enterbox("Belge No Giriniz: (Ör: 21351900IM000008)")
# belge_tur = easygui.enterbox("Belge Türü Giriniz: (Ör: Detaylı Beyan için 3)")
tables = tabula.read_pdf(filename, pages='all', multiple_tables=False)
df = tables[0].dropna()

entry_exit = pd.DataFrame(df['kinci Tartim Tarih'].str.split(expand=True))
# entry_exit.rename(columns={0: 'date', 1:'time'}, inplace=True)
entry_exit.insert(0, 'YÖN', 'Ç')
entry_exit.insert(1, 'BELGE_TÜRÜ', int(3))
entry_exit.insert(2, 'BELGE_NO', str(belge_no))
entry_exit.insert(3, 'PLAKA', df['Araç Plaka'])
entry_exit.insert(4, 'DORSE1', '')
entry_exit.insert(5, 'DORSE2', '')
entry_exit = entry_exit.set_index('YÖN')

with zipfile.ZipFile('{}\Arac_Giris_Cikis_Aktarim_Sablon.zip'.format(path), 'r') as zip_ref:
    zip_ref.extractall(path)

book = xw.Book(r'{}\Arac_Giris_Cikis_Aktarim_Sablon.xls'.format(path))
sheet = book.sheets[0]
sheet['A2'].options(header=False).value = entry_exit
book.save(r'{}\Sami-{}.xls'.format(path, datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')))
book.close()