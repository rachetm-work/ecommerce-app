from src.framework.models import BaseModel


class ApiModelSerializer:
    """Serializer for db models"""

    def __init__(self, data_to_serialize=None, **kwargs):
        self.data_to_serialize = data_to_serialize

    def serialize(self):
        """Serialize models."""
        if not isinstance(self.data_to_serialize, list):
            self.data_to_serialize = [self.data_to_serialize]

        result = []
        for data in self.data_to_serialize:
            if isinstance(data, BaseModel):
                schema = data._schema
                serialized_data = schema.model_validate(data)
                result.append(serialized_data)
            else:  # Anything that is not a BaseModel. Eg: dict, Pydantic model, etc.
                result.append(data)

        return result
