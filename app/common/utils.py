"""
UTILS
"""

import re
import exifread


def is_email(dado):
    """
    Verifica se é e-mail ou não
    """
    # Expressões regulares para verificar se é um número de telefone ou e-mail
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # Verifica se o dado corresponde ao padrão de e-mail
    if re.match(email_pattern, dado):
        return True

    return False


def extract_image_metadata(file_path: str):
    metadata = {}
    with open(file_path, "rb") as file:
        tags = exifread.process_file(file)
        for tag, value in tags.items():
            metadata[tag] = str(value)

    return metadata
