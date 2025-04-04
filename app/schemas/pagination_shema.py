from flask import request


class PaginatedResponse:
    PAGINA_POR_DEFECTO = 1
    CANTIDAD_ITEMS_DEFECTO = 5

    #PARA CANTIDADES GRANDES
    DEFAULT_ITEM_PAGE = 10
    MAX_ITEM_PAGE=20

    @classmethod
    def paginate(cls, query, schema):
        pagina = request.args.get('pagina', cls.PAGINA_POR_DEFECTO, type=int)

        #funcion para validar que el valor que le demos de la cantida de items no sobrepase el maximo
        item_page =min(
            request.args.get('items', cls.CANTIDAD_ITEMS_DEFECTO, type=int),
            cls.MAX_ITEM_PAGE)

        paginated = query.paginate(page=pagina, per_page=item_page, error_out=False)
        
        return {
            'data': schema().dump(paginated.items, many=True),
            'pagination': {
                'total': paginated.total,#total de marcas existentes
                'pages': paginated.pages,#total de paginas existentes
                'current_page': paginated.page,#pagina actual
                'per_page': paginated.per_page,#item por pagina
                'next': paginated.next_num if paginated.has_next else None,
                'prev': paginated.prev_num if paginated.has_prev else None
            }
        }
