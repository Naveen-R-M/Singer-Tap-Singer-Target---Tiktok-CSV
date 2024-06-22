class TikTokShopSchemas:
    @staticmethod
    def get_authorized_shop_schema():
        return {
            "properties": {
                "region": {"type": "string"},
                "shop_cipher": {"type": "string"},
                "shop_code": {"type": "string"},
                "shop_id": {"type": "string"},
                "shop_name": {"type": "string"},
                "type": {"type": "integer"},
            }
        }
        
    @staticmethod
    def get_brands_schema():
        return {
            "properties": {
                "authorized_status": {"type": "integer"},
                "id": {"type": "string"},
                "is_t1_brand": {"type": "boolean"},
                "name": {"type": "string"},
            }
        }
        
    @staticmethod
    def get_categories_schema():
        return {
            "properties": {
                "id": {"type": "string"},
                "is_leaf": {"type": "boolean"},
                "local_display_name": {"type": "string"},
                "parent_id": {"type": "string"},
                "status": {"type": "array"},
            }
        }
        
    @staticmethod
    def get_attributes_schema():
        return {
            "properties": {
                "attribute_type": {"type": "integer"},
                "id": {"type": "string"},
                "input_type": {
                    "type": "object",
                    "properties": {
                        "is_customized": {"type": "boolean"},
                        "is_mandatory": {"type": "boolean"},
                        "is_multiple_selected": {"type": "boolean"}
                        }
                    },
                "name": {"type": "string"},
                "values": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"}
                            }
                    }
                }
            },
        }
