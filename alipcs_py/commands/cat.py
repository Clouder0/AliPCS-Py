from typing import Optional

from alipcs_py.alipcs import AliPCSApi
from alipcs_py.commands.display import display_blocked_remotepath

import chardet


def cat(
    api: AliPCSApi,
    remotepath: str,
    encoding: Optional[str] = None,
    encrypt_password: bytes = b"",
):
    pcs_file = api.path(remotepath)

    if not pcs_file:
        return

    fs = api.file_stream(pcs_file.file_id, encrypt_password=encrypt_password)
    if not fs:
        display_blocked_remotepath(remotepath)
        return

    cn = fs.read()
    if cn:
        if encoding:
            print(cn.decode(encoding))
        else:
            r = chardet.detect(cn)
            if r["confidence"] > 0.5:
                print(cn.decode(r["encoding"]))
            else:
                print(cn)
