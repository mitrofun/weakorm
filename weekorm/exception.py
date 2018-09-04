class ModelFieldNameException(Exception):
    """
    Raise for model name field exception
    """
    def __init__(self, *args, **kwargs):
        if kwargs:
            field_name = kwargs['field_name']
            model_name = kwargs['model_name']
            msg = f'Model {model_name}: Field with name `{field_name}` does not exist.'
            super(ModelFieldNameException, self).__init__(msg)
        else:
            super(ModelFieldNameException, self).__init__(*args)


class ModelFieldTypeException(Exception):
    """
    Raise for model field type exception
    """
    def __init__(self, *args, **kwargs):
        if kwargs:
            model = kwargs['model']
            field_name = kwargs['field_name']
            field_type = kwargs['field_type']
            value_type = kwargs['value_type']
            msg = f'Model {model}: Value field with name `{field_name}`' \
                  f' must be `{field_type}`, not `{value_type}`.'
            super(ModelFieldTypeException, self).__init__(msg)
        else:
            super(ModelFieldTypeException, self).__init__(*args)
