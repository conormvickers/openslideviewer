import wsic

slidepath = r'Z:\3Dhistech\POROKERATOSIS VRRUCOUS DP19-13251.mrxs'

reader = wsic.readers.OpenSlideReader(slidepath)

writer = wsic.writers.JP2Writer(
    "jp2con.jp2", 
    verbose=True,
    shape=(5000, 5000)
)
writer.copy_from_reader(reader)