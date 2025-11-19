from flask import Flask

calorie=Flask(__name__)

@calorie.route('/calculate')
def index():
    return "Hello, Flask!"

w = float #a=体重
h = float #b=身長
O = float #年齢
j = int#j=性別　１:男　２:女
c = w / (h * h)
rounded_c= round(c, 0)  # 小数第2位まで四捨五入
rounded_c_int = int(rounded_c) #roundedをint型に変換
i = int#食物繊維量(g)
a = int#基礎代謝量(kcal/kg/日)
k = int#身体活動レベル
o = int#鉄分量
p = int#ビタミンa(μgRAE/日)
q = float#ビタミンb₁(mg/日)
"性別、年代による基礎代謝量"
if 0 < O <3:
    k =1.40
    p =200
    q =0.4
    if j ==1:
        a =61
        o =4
    elif j ==2:
        a =59.7
        o =4
elif 2 < O < 6:
    k =1.50
    q =0.5
    if j ==1:
        a =54.8
        i =8
        o =5
    elif j == 2:
        a =52.2
        i =8
        o =5
elif 5 < O < 8:
    k = 1.60
    if j ==1:
        a =44.3
        i =10
        o =6
        p =450
        q =0.7
    elif j == 2:
        a =41.9
        i =9
        o =6
        p =400
        q =0.6
elif 7 < O < 10:
    k =1.70
    if j ==1:
        a =40.8
        i =11
        o =7.5
        p =500
        q =0.8
    elif j == 2:
        a =38.3
        i =11
        o =8
        p =500
        q =0.7
elif 9 < O < 12:
    k =1.70
    if j ==1:
        a =37.4
        i =13
        o =9.5
        p =600
        q =0.9
    elif j == 2:
        a =34.8
        i =13
        o =9.8
        p =550
        q =0.9
elif 11 < O < 15:
    k =1.70
    if j ==1:
        a =31.0
        i =17
        o =9
        p =750
        q =1.1
    elif j == 2:
        a =29.6
        i =16
        o =9.05
        p =700
        q =1.0
elif 14 < O < 18:
    k =1.75
    if j ==1:
        a =27.0
        i =19
        o =9
        p =900
        q =1.2
    elif j == 2:
        a =25.3
        i =18
        o =7.55
        p =650
        q =1.0
elif 17 < O < 30:
    k = 1.75
    if j ==1:
        a =24.0
        i =20
        o =7
        p =875
        q =1.1
    elif j == 2:
        a =23.6
        i =18
        o =6.9
        p =675
        q =0.8
elif 29 < O < 50:
    k =1.75
    if j ==1:
        a =22.3
        i =22
        o =7.5
        p =875
        q =1.2
    elif j == 2:
        a =21.7
        i =18
        o =7.05
        p =675
        q =0.9
elif 49 < O <70:
    if j ==1:
        a =21.5
        i =22
        o =7
        p =875
        q =1.0
    elif j == 2:
        a =20.7
        i =18
        o =7.05
        p =675
        q =0.8
elif 69 < O :
    k =1.50
    if j ==1:
        a =21.5
        i =21
        p =825
        q =1.0
    elif j == 2:
        a =20.7
        i =17
        p =675
        q =0.7
g = h * h * 22
rounded_g= round(g, 0)  # 小数第2位まで四捨五入
ih = g * a * k
rounded_ih= round(ih, 0)  # 小数第2位まで四捨五入
l = int#塩分摂取量 
if  j ==1:
    l =7.5
elif j == 2:
    l =6.5
m = (ih * 0.25) / 9#脂質量
r = rounded_ih * 0.575 /4 #炭水化物量
rounded_r= round(r, 0)  # 小数第2位まで四捨五入

if __name__ == '__main__':
    calorie.run(debug=True, port=5000)
