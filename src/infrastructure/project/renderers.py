from rest_framework.renderers import JSONRenderer

from .encoders import CustomJSONEncoder


class CustomJSONRenderer(JSONRenderer):
    encoder_class = CustomJSONEncoder
