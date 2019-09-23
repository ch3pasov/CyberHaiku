#CyberHaiku converter, Anatoliy Ch, 2019. Version 0.1

f=open('input','r')
intext=f.read().split('\n')
f.close()

if intext[-1]=='':
	intext.pop(-1)

line=len(intext)
length=max(len(intext[i]) for i in range(line))

for i in range(line):
	intext[i]=intext[i].lower()
	intext[i]+=(length-len(intext[i])) * (' ')

outtext=''
for i in range(length):
	if i != 0:
		outtext+='\n'
	for j in range(line):
		if j != 0:
			outtext+=(' ')
		outtext += intext[j][i]

f=open('output', 'w')
f.write(outtext)
f.close()
