import argparse
import logging
import os

from enum import Enum

class EncodingType(Enum):
    EAN13 = "ean13"
    QR = "qr"

def parse_args():
    parser = argparse.ArgumentParser(description="Generate unique codes.")

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="File containing codes to process",
    )
    
    parser.add_argument(
        "-c", "--count",
        type=int,
        help="Number of codes to generate",
    )    
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=12,
        help="Length of each code (default: 6)",
    )
    parser.add_argument(
        "-a", "--alphnum",
        action="store_true",
        help="Generate alphanumeric codes instead of numeric",
    )

    parser.add_argument(
        "-t", "--encoding-type",
        type=str,
        choices=[e.value for e in EncodingType],
        default=EncodingType.EAN13.value,
        help="Type of encoding to use (EAN13 or QR)",
    )

    parser.add_argument(
        "-i", "--image",
        type=str,
        default=None,
        help="Path to the image file to include in the generated QR codes",
    )

    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=os.path.join(os.getcwd(), "output"),
        help="Directory to save the generated codes",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output",
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug output",
    )

    return parser.parse_args()

def generate_codes(count: int, length: int = 12, alphnum: bool = False) -> list[int]:
    """
    Generate a list of unique codes.

    Args:
        count (int): The number of codes to generate.
        length (int): The length of each code. Default is 6.
        alphnum (bool): If True, generate alphanumeric codes. Default is False.

    Returns:
        list[int]: A list of unique codes.
    """

    import random
    import string

    if alphnum:
        logging.info("Generating alphanumeric codes")
        characters = string.ascii_letters + string.digits
    else:
        logging.info("Generating numeric codes")
        characters = string.digits

    codes = set()

    while len(codes) < count:
        code = ''.join(random.choice(characters) for _ in range(length))
        codes.add(code)

    logging.info(f"Generated {len(codes)} unique codes")
    return list(codes)

def read_codes_from_file(file_path: str) -> list[str]:
    """
    Read codes from a file.

    Args:
        file_path (str): The path to the file containing codes.

    Returns:
        list[str]: A list of codes read from the file.
    """

    logging.info(f"Reading codes from file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            codes = [line.strip() for line in f.readlines() if line.strip()]
        return codes
    except FileNotFoundError:
        logging.warning(f"File {file_path} not found. Aborting.")
        return []

def generate_encoded_images(codes: list[str], output_dir: str, encoding_type: EncodingType = EncodingType.EAN13, logo: str = None) -> None:
    """
    Generate encoded images for the given codes and create a manifest file.

    Args:
        codes (list[str]): The list of codes to encode.
        output_dir (str): The directory to save the generated images.
        encoding_type (EncodingType): The type of encoding to use (EAN13 or QR).
        logo (str): Path to the logo image to embed in QR codes (optional).
    """

    import qrcode
    from PIL import Image
    from barcode import EAN13
    from barcode.writer import ImageWriter

    # Validate and load the logo once
    logo_img = None
    if logo is not None and os.path.exists(logo):
        try:
            logo_img = Image.open(logo)
            logging.info(f"Loaded logo image: {logo}")
        except Exception as e:
            logging.warning(f"Failed to load logo image {logo}: {e}")
            logo_img = None

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        logging.info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # Prepare the manifest file
    manifest_path = os.path.join(output_dir, "manifest.csv")
    logging.info(f"Creating manifest file at {manifest_path}")

    # Initialize QR code object (reuse for efficiency)
    qr = None
    if encoding_type == EncodingType.QR:
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=5,
        )

    with open(manifest_path, "w") as manifest:
        logging.info(f"Generating {encoding_type.value} codes in {output_dir}")
        for code in codes:
            try:
                file_name = f"{code}.png"
                file_path = os.path.join(output_dir, file_name)

                if encoding_type == EncodingType.EAN13:
                    # Generate EAN13 barcode
                    barcode = EAN13(code.zfill(12), writer=ImageWriter())
                    barcode.save(file_path)
                elif encoding_type == EncodingType.QR:
                    # Generate QR code
                    qr.clear()  # Clear previous data
                    qr.add_data(code)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

                    # Add logo if available
                    if logo_img is not None:
                        qr_width, qr_height = img.size
                        logo_size = min(qr_width, qr_height) // 4
                        resized_logo = logo_img.resize((logo_size, logo_size))
                        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                        img.paste(resized_logo, pos)

                    img.save(file_path)
                else:
                    raise ValueError(f"Unsupported encoding type: {encoding_type}")

                # Write to the manifest file
                manifest.write(f"{file_name},{code}\n")

            except Exception as e:
                logging.error(f"Failed to generate {encoding_type.value} code for {code}: {e}")

    logging.info(f"Manifest file created at {manifest_path}")

def main():
    args = parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.WARNING)

    codes = read_codes_from_file(args.file) if args.file else generate_codes(args.count, args.length, args.alphnum)
    logging.info(f"{len(codes)} codes ready for encoding.")

    generate_encoded_images(codes, args.output_dir, EncodingType(args.encoding_type), args.image)
    logging.info("Encoding completed.")

    print(f"Generated {len(codes)} codes and saved them to {args.output_dir}.")

if __name__ == "__main__":
    main()