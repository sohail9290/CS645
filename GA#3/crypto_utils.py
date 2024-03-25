from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

def generate_rsa_keys():
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    pub_key = priv_key.public_key()
    return priv_key, pub_key

def sign_data(private_key, data):
    signature = private_key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature

def verify_signature(public_key, signature, data):
    try:
        public_key.verify(signature, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception as e:
        print(f"Verification Failed: {e}")
        return False