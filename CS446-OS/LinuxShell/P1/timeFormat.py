time = float(input())
secsleft = time
days = int(secsleft // (3600*24))
secsleft -= days * 3600 *24
hours = int(secsleft//3600)
secsleft -= hours * 3600
mins = int(secsleft // 60)
secsleft -= mins * 60
returntime = secsleft + mins*60 + hours*3600 + days*3600*24
print(str(days), str(hours), str(mins), str(int(secsleft)), sep=':')
print(time)
print(returntime)
