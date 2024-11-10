from django.core.exceptions import ValidationError
import jsonschema

class JSONSchemaValidator:
    def __init__(self, limit_value):
        self.schema = limit_value

    def __call__(self, value):
        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(
                f"Invalid JSON data: {e.message}",
                params={'value': value}
            )

MY_JSON_FIELD_SCHEMA = {
    "type": "object",
    "properties": {
        "employee_name": {
            "type": "string",
            "maxLength": 100
        },
        "employee_phone": {
            "type": "string",
            # "pattern": r"^\d{3}-\d{3}-\d{4}$"  # Regex to match a phone number format
        },
        "employee_position": {
            "type": "string",
            "maxLength": 100
        }
    },
    "required": ["employee_name", "employee_phone", "employee_position"],
    "additionalProperties": False
}

