EXTERNAL_VALIDATION_RESPONSE = {
    "validationResult": {
        "issues": [
            {
                "code": "TABLE_field_code",
                "errors": [
                    {
                        "severity": "error",
                        "type": "external_check",
                        "message": "something went wrong in table cell",
                        "position": {"row": 0, "column": 0, "index": 0},
                    }
                ],
                "warnings": [],
            },
            {
                "code": "KEY-VALUE_field_code",
                "errors": [
                    {
                        "severity": "error",
                        "type": "external_check",
                        "message": "something went wrong in value of key-value pair",
                        "position": {"kv_id": "value", "index": 0},
                    }
                ],
                "warnings": [
                    {
                        "severity": "warning",
                        "type": "external_check",
                        "message": "some warning in key of key-value pair",
                        "position": {"kv_id": "key", "index": 0},
                    }
                ],
            },
            {
                "code": "GENERIC_field_code",
                "errors": [
                    {
                        "severity": "error",
                        "type": "external_check",
                        "message": "something went wrong in a simple field",
                    }
                ],
                "warnings": [],
            },
        ]
    }
}
