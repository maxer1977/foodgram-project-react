def filter_it(queryset, request, value, param):
    """Механизм фильтра по признакам."""
    author = request.user
    if author.is_anonymous or value == 0:
        return queryset
    elif value == 1:
        filter_kwargs = {param: author}
        print(queryset.filter(**filter_kwargs))
        return queryset.filter(**filter_kwargs)


def favorited_or_shopping(context, obj, param):
    """Механизм признаков favorited и shopping."""

    user = context.get("request").user
    if user.is_anonymous:
        return False
    expression = "obj.{}.all().exists()".format(param)
    result = eval(expression)
    return result
