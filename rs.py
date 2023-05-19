import numpy as np
from numpy import polynomial as P

def generate_reed_solomon_code(data, ecc_bytes):
    # Generate the generator polynomial
    gen = P.polygen(np.uint8)
    
    generator_polynomial = P.polynomial.polymul.reduce([gen - i for i in range(ecc_bytes)])

    # Pad the data with zeros for the error correction bytes
    padded_data = np.pad(data, (0, ecc_bytes), mode='constant')

    # Compute the remainder polynomial
    _, remainder = P.polynomial.polydiv(padded_data, generator_polynomial)

    # Compute the Reed-Solomon code
    code = np.polyadd(padded_data, remainder)

    return code

# Example usage
data = np.array([1, 2, 3, 4, 5])
ecc_bytes = 2
rs_code = generate_reed_solomon_code(data, ecc_bytes)

print("Data:", data)
print("Reed-Solomon Code:", rs_code)
