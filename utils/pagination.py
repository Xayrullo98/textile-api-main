import math


def pagination(form, page, limit):
    if page and limit:
        return {"current_page": page, "limit": limit, "pages": math.ceil ( form.count ( ) / limit ),
            "data": form.offset ( (page - 1) * limit ).limit ( limit ).all ( )}
    else:
        if page==0 or limit==0:
            return {"data": form.all()}
        # elif limit==0:
        #     return {"data": form.all()}
        else:
            return {"data": form.offset ((1) * limit).limit(limit).all()}




