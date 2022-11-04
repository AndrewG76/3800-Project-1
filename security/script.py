import enc_interface as ei
import key_repository as kr

sPrKey = ei.genKey()
cPrKey = ei.genKey()
sPuKey = sPrKey.public_key()
cPuKey = cPrKey.public_key()


kr.saveKey("keys/sPrKey.pem", sPrKey)
kr.saveKey("keys/cPrKey.pem", cPrKey)
kr.saveKey("keys/sPuKey.pem", sPuKey)
kr.saveKey("keys/cPuKey.pem", cPuKey)


