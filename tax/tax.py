from functools import reduce


def tax():
    try:
        goodsNum = int(input("输入订单商品种数:"))
        print("---------------->当前略过关税和保价")
        print("---------------->当前税收折扣为0.7")
        print("---------------->当前增值税率为0.17")
        i = 0
        goodPrices = []
        saleRates = []
        while i < goodsNum:
            i += 1
            goodPrice = float(input("输入第%d种商品价格    : " % i))
            goodPrices.append(goodPrice)
            saleRate = float(input("输入第%d种商品消费税率: " % i))
            saleRates.append(saleRate)
        wayPrice = float(input("输入订单总运费       : "))
        goodPriceTotal = reduce(lambda x, y: x + y, goodPrices)
        customerTax1 = 0
        for j in range(len(saleRates)):
            temCustomerTax = (goodPrices[j] + goodPrices[j] / goodPriceTotal * wayPrice) * saleRates[j] / (1 - saleRates[j])
            customerTax1 += temCustomerTax
        customerTax2 = customerTax1 * 0.7  # 折后
        addTax = (goodPriceTotal + wayPrice + customerTax1) * 0.17 * 0.7
        totalTax = customerTax2 + addTax
        print("消费税:%f,增值税:%f,总税值:%f" % (customerTax2, addTax, totalTax))
    except Exception as e:
        print(e, "\n输入有误,请重新输入!")

if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        print('<====================进入第%d次计算===================>' % i)
        tax()
        print('<=========================结束=======================>\n')
