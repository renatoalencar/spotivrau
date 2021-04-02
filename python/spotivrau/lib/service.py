class ServiceError(Exception):
    pass


def service_error_serialize(fn):
    def _handler(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ServiceError as e:
            return {'message': str(e)}, 400

    return _handler
