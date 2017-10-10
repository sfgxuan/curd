import logging

from ..errors import ProgrammingError


logger = logging.Logger('curd')

DEFAULT_FILTER_LIMIT = 100
CREATE_MODE = ('INSERT', 'IGNORE', 'REPLACE')
FILTER_OP = ('<', '>', '>=', '<=', '=', '!=', 'IN')
CURD_FUNCTIONS = (
    'create', 'update', 'get', 'delete', 'filter', 'exist', 'execute'
)


class BaseConnection(object):
    def _check_filters(self, filters):
        new_filters = []
        for op, k, v in filters:
            if op.upper() not in FILTER_OP:
                raise ProgrammingError('Not support filter Operator')
            else:
                new_filters.append((op.upper(), k, v))
        return new_filters
    
    def create(self, collection, data, mode='INSERT', **kwargs):
        raise NotImplementedError

    def update(self, collection, filters, data, **kwargs):
        raise NotImplementedError

    def delete(self, collection, filters, **kwargs):
        raise NotImplementedError
    
    def filter(self, collection, filters, fields=None,
               order_by=None, limit=DEFAULT_FILTER_LIMIT, **kwargs):
        raise NotImplementedError
    
    def get(self, collection, filters, fields=None, **kwargs):
        rows = self.filter(collection, filters, fields, limit=1, **kwargs)
        if rows:
            return rows[0]
        else:
            return None

    def exist(self, collection, filters, **kwargs):
        if filters:
            fields = list(filters.keys())[0]
            data = self.get(collection, filters, fields=fields, **kwargs)
            if data:
                return False
            else:
                return True
        else:
            raise ProgrammingError('exist without filter is not supported')