
document.getElementById("btnConvertir").addEventListener("click", async () => {
    
    const inputStr = document.getElementById("inputNumber").value.trim();
    const baseOrigen = parseInt(document.getElementById("inputBase").value);
    const bitsArquitectura = parseInt(document.getElementById("wordSize").value);
    const errorContenedor = document.getElementById("errorMessage");
    
    
    errorContenedor.innerText = "";
    document.getElementById("outBin").value = "";
    document.getElementById("outOct").value = "";
    document.getElementById("outDec").value = "";
    document.getElementById("outHex").value = "";

    if (inputStr === "") return;

    try {
        const response = await fetch("/api/convertir", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ number: inputStr, base: baseOrigen, bits: bitsArquitectura })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        document.getElementById("outBin").value = data.bin;
        document.getElementById("outOct").value = data.oct;
        document.getElementById("outDec").value = data.dec;
        document.getElementById("outHex").value = data.hex;
    } catch (error) {
        errorContenedor.innerText = "Error: " + error.message;
    }
});


document.getElementById('btnALU').addEventListener('click', async () => {
    const a = document.getElementById('aluA').value.trim();
    const b = document.getElementById('aluB').value.trim();
    const op = document.getElementById('aluOp').value;
    const out = document.getElementById('aluOut');
    const err = document.getElementById('aluError');
    err.innerText = '';
    out.value = '';

    try {
        if (a === '' || b === '') throw new Error('Ambos operandos deben proporcionarse.');
        const response = await fetch('/api/alu', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ a, b, operation: op })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error);
        out.value = data.result;
    } catch (e) {
        err.innerText = 'Error: ' + e.message;
    }
});