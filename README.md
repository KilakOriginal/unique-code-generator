# Unique Code Generator

The **Unique Code Generator** is a Python-based tool for generating unique codes and encoding them as either QR codes or EAN13/EAN8 barcodes. It supports generating codes from scratch or reading them from a file, and it can optionally embed a logo into QR codes.

## Features

- Generate unique numeric or alphanumeric codes.
- Encode codes as QR codes or EAN13/EAN8 barcodes.
- Embed a logo into QR codes.
- Save generated codes and images to a specified output directory.
- Create a manifest file (`manifest.csv`) with details of generated codes and their corresponding image files.
- Flexible command-line arguments for customization.

## Requirements

The following Python libraries are required:

- `qrcode`
- `barcode`
- `python-barcode`
- `pillow`

Install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage
Run the script using Python:
```bash
python generate.py [OPTIONS]
```

|Argument|Description|Default|
|---|---|---|
|`-f`, `--file`|Path to a file containing codes to process.|None|
|`-c`, `--count`|Number of codes to generate.|None|
|`-l`, `--length`|Length of each generated code.|12|
|`-a`, `--alphanum`|Generate alphanumeric codes instead of numeric.|False|
|`-t`, `--encoding-type`|Type of encoding to use (`ean13`, `ean8` or `qr`).|`ean13`|
|`-i`, `--image`|Path to an image file to embed in QR codes.|None|
|`-o`, `--output-dir`|Directory to save the generated codes and images.|`./output`|
|`-v`, `--verbose`|Enable verbose output.|False|
|`-q`, `--quiet`|Suppress all output.|False|
|`-d`, `--debug`|Enable debug output.|False|

## Examples
### Generate 10 numeric EAN13 barcodes
```bash
python generate.py -c 10
```

### Generate 5 alphanumeric QR codes with a logo
```bash
python generate.py -c 5 -a -t qr -i logo.png
```

### Read codes from a file and generate QR codes
```bash
python generate.py -f codes.txt -t qr
```

### Save output to a custom directory
```bash
python generate.py -c 10 -o ./custom_output
```

## Output
- **Generated Images:** Saved in the specified output directory.
- **Manifest File:** A `manifest.csv` file in the output directory containing the mapping of codes to their image files.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## Author
Developed by Malik Abdoul Hamidou