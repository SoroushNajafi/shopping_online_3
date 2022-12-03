from django import template

register = template.Library()


@register.filter
def active_comments(comments):
    return comments.filter(active=True)


@register.filter
def number_to_word(number):
    numbers = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five'}
    return numbers[number]


@register.filter
def int_to_float(number):
    int_num = int(number)
    float_number = "{:.2f}".format(int_num)
    return float_number
