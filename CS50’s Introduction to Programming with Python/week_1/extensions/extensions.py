types = {
    "gif": "image/gif",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "pdf": "application/pdf",
    "txt": "text/plain",
    "zip": "application/zip",
}

filename = input("File name: ").strip().lower()
ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
print(types.get(ext, "application/octet-stream"))
