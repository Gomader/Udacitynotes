'''
1. 输入一个字符串然后把第一个字母和最后一个字母换个位置

思路：首先当然是接受字符，要用到input()函数，但是效果里有要求数字也要能实现这个功能，也就是说整数型也要当成字符串来看待
        这个时候可以用到一个函数是raw_input()   这个函数是input的子函数，可以把input得到的东西全部以str的格式来看待
            接下来就很简单了，先用for来循环一下整个input得到的东西，然后定义一个中间项（因为变量的赋值会被覆盖，需要中间项来保留变量值），之后就可以交换第一项和最后一项并输出了
                这里有个根本的思路就是输入进来的字符串不要想成整体，要拆开，把整个字符串当做每一个字符组成的列表
'''
a = input('Enter a string:')

#这里需要限制一下a的长度
if len(a)>=2:
    a = str(a)

    text = []

    #通过for循环，把a拆成单个字符组成的列表并添加到text列表里面
    for c in a:
        text.append(c)

    #这里是把第一个元素和最后一个元素交换位置
    x = text[-1]
    text[-1] = text[0]
    text[0] = x

    print ('New string:'+''.join(text))
else:
    print("The length of the string must be greater than 2 ")




'''
2.这道题整体思路与第一题一样只不过删除text的第nth项
    这里面唯一一个注意点是输入的n要有范围可以用if与len来限制n的大小

'''

a = input('Enter a nonempty string:')

while 1>0 :   #这里面我不知道例题上给的是可以不断实现还是只实现一次，说一下写了一个while循环，当数字大于字符串长度的时候会跳出
    text = []
    for word in a:   #这里为了每次都是从一个新的字符串里开始del，要覆盖上一次循环的数据
        text.append(word)
    b = input ("Enter a index number:")
    b = int(b)
    if b<len(a):   #判断b是否大于等于字符串的长度-1
        x = text
        del x[b]
        print("New string:"+''.join(x))
    else:
        print('Please enter a right number')
        break

'''
3.这道题很简单，就是用for去历遍输入的字符串，当历遍的元素为(a,e,i,o,u)的时候记录
'''

a = input('Enter a nonempty string:')

num = 0

for letter in a:
    if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
        num+=1

print('The number of vowel is:'+ str(num))#相加的时候需要把数字转换成字符


'''
4.这道题就是让输入三个字母然后把他们往前提三个。
    这道题说白了就是再考ASCII表的转换，可以通过int（字符串）来让字符串转换为数字，也可以通过chr（数字）来让数字转换为字符
        说是加密，其实是使用了全世界最通用的一种方式加密了，也就是说这种加密方式口算都能实现

'''

a = input("Enter three characters:")

text = []

for x in a:
    if int(ord(x))<120:
        text.append(chr(int(ord(x))+3))
    else:
        print("Please don't use 'x' 'y' 'z'")
        break

print(''.join(text))


'''
5.这题主要就是format函数使用和保留两位小数点的问题

'''

name = input('Enter the name of a student:')
pp = float(input('Enter the score of Python Programming(PP):'))
cw = float(input('Enter the score of Creative Writing(CW):'))
ew = float(input('Enter the score of English Writing(EW):'))
ave = float(pp)/3 + float(cw)/3 + float(ew)/3 #python平均数最好是单个处理之后再相加
data = [str(name),round(float(pp),2),round(float(cw),2),round(float(ew),2),round(float(ave),2)]  #round（改格式的数字，需要保留的小数点位数）

label = ['Student','PP','CW','EW','Average']
str_f = '{:^10} | {:^8} | {:^8} | {:^8} | {:^10} |'
for i in [label,data]:
    print(str_f.format(*i))

