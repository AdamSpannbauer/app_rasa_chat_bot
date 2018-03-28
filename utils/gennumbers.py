import random


# function to gen ordinal numbers
# https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
def ordinal_nums_100():
    # https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    ords_out = [ordinal(rank) for rank in range(1, 101)]

    return ords_out


# function to gen 1-100 as words
def word_nums_100():
    word_nums_out = []
    first_nums = [
        "", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = [
        "ten", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety"]

    for num in range(1, 101):
        if num == 100:
            word_nums_out.append('one hundred')
        elif num < 20:
            word_nums_out.append(first_nums[num])
        elif num < 100 and num % 10 == 0:
            word_nums_out.append(tens[int(num / 10 - 1)])
        else:
            sep = random.choice([' ', '-'])
            word_nums_out.append(tens[int(num // 10 - 1)] + sep + first_nums[int(num % 10)])

    return word_nums_out
