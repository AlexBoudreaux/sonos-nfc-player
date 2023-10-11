import nfc

def read_nfc_tag():
    clf = nfc.ContactlessFrontend('usb')
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    clf.close()
    return tag
