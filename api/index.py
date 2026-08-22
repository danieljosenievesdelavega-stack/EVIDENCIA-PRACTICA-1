from flask import Flask, jsonify, request, send_from_directory
import os
app = Flask(__name__)

DIGITS = "0123456789ABCDEF"
SUPPORTED_BASES = {2, 8, 10, 16}
SUPPORTED_WORD_SIZES = {8, 16, 32, 64}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_number(value, base):
    value = value.strip().upper()

    if not value:
        raise ValueError("Debe proporcionar un número.")

    if base not in SUPPORTED_BASES:
        raise ValueError("La base seleccionada no es válida.")

    try:
        return int(value, base)
    except ValueError as error:
        raise ValueError(
            "Dígito inválido para la base seleccionada."
        ) from error

def format_number(value, base):
    if value == 0:
        return "0"
    result = []

    while value:
        value, remainder = divmod(value, base)
        result.append(DIGITS[remainder])

    return "".join(reversed(result))

def pad_number(value, bits, base):
    widths = {
        2: bits,
        8: (bits + 2) // 3,
        16: bits // 4
    }

    width = widths.get(base)
    return value.zfill(width) if width else value

def validate_binary(value):
    if not isinstance(value, str) or any(
        bit not in "01" for bit in value
    ):
        raise ValueError(
            "Las cadenas deben contener solo 0 y 1."
        )

def alu_bitwise(first, second, operation):
    validate_binary(first)
    validate_binary(second)

    width = max(len(first), len(second))

    first = first.zfill(width)
    second = second.zfill(width)

    operations = {
        "AND": lambda left, right: left == "1" and right == "1",
        "OR": lambda left, right: left == "1" or right == "1",
        "XOR": lambda left, right: left != right,
    }

    if operation not in operations:
        raise ValueError("Operación ALU desconocida.")

    return "".join(
        "1" if operations[operation](left, right) else "0"
        for left, right in zip(first, second)
    )

@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<path:filename>")
def files(filename):
    return send_from_directory(BASE_DIR, filename)


@app.post("/api/convertir")
def convert():
    data = request.get_json(silent=True) or {}

    try:
        value = parse_number(
            str(data.get("number", "")),
            int(data.get("base", 10))
        )

        bits = int(data.get("bits", 8))

        if bits not in SUPPORTED_WORD_SIZES:
            raise ValueError(
                "El tamaño de palabra no es válido."
            )
        maximum = (2 ** bits) - 1

        if value > maximum:
            raise ValueError(
                f"Overflow / Desbordamiento de Registro. "
                f"Máximo permitido en {bits} bits es {maximum}"
            )
        return jsonify({
            "bin": pad_number(
                format_number(value, 2),
                bits,
                2
            ),
            "oct": pad_number(
                format_number(value, 8),
                bits,
                8
            ),
            "dec": str(value),
            "hex": pad_number(
                format_number(value, 16),
                bits,
                16
            ),
        })

    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

@app.post("/api/alu")
def alu():
    data = request.get_json(silent=True) or {}

    try:
        result = alu_bitwise(
            str(data.get("a", "")).strip(),
            str(data.get("b", "")).strip(),
            data.get("operation", ""),
        )

        return jsonify({"result": result})

    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

if __name__ == "__main__":
    app.run(debug=True)