from functools import wraps

from flask import render_template


def get_model_instance_from_id(model):
    """
    Decorator that gets the model instance from id in request
    path and prepends it to the args for the view function

    It renders a 404 page if the instance was not found
    """
    def actual_decorator(func):
        @wraps(func)
        def wrapper(id, *args, **kwargs):
            obj = model.query.get(id)
            if obj is None:
                return render_template("404.html"), 404

            return func(obj, *args, **kwargs)
        return wrapper
    return actual_decorator
