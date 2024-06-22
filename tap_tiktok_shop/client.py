import time
import requests
from api_signature import SignatureGenerator

class TikTokShopClient:
    BASE_URL = "https://open-api.tiktokglobalshop.com"

    def __init__(self, app_key, app_secret, access_token):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token
        self.signature_generator = SignatureGenerator(app_secret)

    def get_headers(self):
        """Return headers required for TikTok API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def fetch_endpoint(self, endpoint, params=None):
        """Fetch data from a specified endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        if params is None:
            params = {}
        params['app_key'] = self.app_key
        params['timestamp'] = int(time.time())
        params['access_token'] = self.access_token
        signature = self.signature_generator.generate_signature(endpoint, params)
        params['sign'] = signature

        response = requests.get(url, headers=self.get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_brands(self):
        """Fetch authorized brands."""
        return self.fetch_endpoint("/api/products/brands")

    def get_authorized_shop(self, shop_id=None):
        """Fetch authorized shops, optionally filtering by shop_id."""
        params = {}
        if shop_id:
            params['shop_id'] = shop_id
        return self.fetch_endpoint("/api/shop/get_authorized_shop", params)

    def get_categories(self, shop_id=None):
        """Fetch product categories, optionally filtering by shop_id."""
        params = {}
        if shop_id:
            params['shop_id'] = shop_id
        return self.fetch_endpoint("/api/products/categories", params)

    def get_attributes(self, category_id="850056"):
        """Fetch product attributes, optionally filtering by category_id."""
        params = {}
        if category_id:
            params['category_id'] = category_id
        return self.fetch_endpoint("/api/products/attributes", params)
