import hashlib
import hmac
import time

class SignatureGenerator:
    def __init__(self, app_secret):
        self.app_secret = app_secret

    def generate_signature(self, endpoint, params):
        # Filter out 'sign' and 'access_token' and sort the remaining parameters alphabetically
        filtered_params = {k: v for k, v in params.items() if k not in ['sign', 'access_token']}
        sorted_params = sorted(filtered_params.items())
        
        # Concatenate the sorted query parameters in the format {key}{value}
        concatenated_params = ''.join(f"{k}{v}" for k, v in sorted_params)
        
        # Create the base string by concatenating the path and the concatenated parameters
        base_string = f"{endpoint}{concatenated_params}"
        
        # Wrap the base string with the secret key
        wrapped_string = f"{self.app_secret}{base_string}{self.app_secret}"
        
        # Create the HMAC-SHA256 signature
        signature = hmac.new(self.app_secret.encode(), wrapped_string.encode(), hashlib.sha256).hexdigest()
        
        return signature

# Example usage
# if __name__ == "__main__":
#     app_secret = "777"
#     endpoint = "/api/orders"
#     params = {
#         "limit": "20",
#         "timestamp": str(int(time.time())),
#         "app_key": "12345",
#         "access_token": "88888888"
#     }

#     signature_generator = SignatureGenerator(app_secret)
#     signature = signature_generator.generate_signature(endpoint, params)
#     print("Generated signature:", signature)
