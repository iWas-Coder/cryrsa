"""
Functions Module
~~~~~~~~~~~~~~~~

(...)
"""

from pwn import *
from Crypto.PublicKey import RSA
import modules.args as args
import modules.math as math
import time
import sys
import signal


def ctrl_c():
    """
    (...)
    """
    
    def def_handler(sig, frame):
        log.warn("Process cancelled by user D:")
        sys.exit(1)
    signal.signal(signal.SIGINT, def_handler)


def import_key():
    """
    (...)
    """
    
    with open(args.key(), 'r') as f:
        return RSA.importKey(f.read())


def extract(key: RSA.RsaKey):
    """
    (...)
    """
    
    extract = log.progress("Extraction")
    
    extract.status("Extracting public components...")
    time.sleep(2)
    
    log.info(f"e: {key.e}")
    log.info(f"n: {key.n}")
    
    time.sleep(1)
    
    if key.has_private():
        extract.status("Extracting private components...")
        time.sleep(2)
        
        log.info(f"p: {key.p}")
        log.info(f"q: {key.q}")
        m = key.n - (key.p + key.q - 1)
        log.info(f"m: {m}")
        log.info(f"d: {math.modinv(key.e, m)}")
        
        extract.success("Done! :)")
    else:
        extract.failure("No private component found :(")
        time.sleep(1)
        compute(key)


def compute(key: RSA.RsaKey):
    """
    (...)
    """
    
    compute = log.progress("Compute")
    compute.status("Performing prime factorization...")
    p, q = math.factorize(key.n, compute)
    
    if p and q:
        log.info(f"p: {p}")
        log.info(f"q: {q}")
        compute.success("Done! :)")
        
        m = key.n - (p + q -1)
        log.info(f"m: {m}")
        log.info(f"d: {math.modinv(key.e, m)}")
    else:
        compute.failure("No factors found :(")
