from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


import argparse

import secrets

parser = argparse.ArgumentParser("QR Code Arguments")
parser.add_argument("--size", help="Tamanho das Chaves RSA", required='true', type=int)

args = parser.parse_args()

key = RSA.generate(args.size)
private_key = key.export_key()
file_out = open(f"private_key.pem", "wb")
file_out.write(private_key)

public_key = key.publickey().export_key()
file_out = open(f"public_key.pem", "wb")
file_out.write(public_key)

aes_key = get_random_bytes(32)
file_out = open(f"aes_key.bin", "wb")
file_out.write(aes_key)