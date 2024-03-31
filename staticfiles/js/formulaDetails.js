window.onload = () => {
    sumContent();
    calculateNatOriginContent();
}

const elementsToDisable = document.querySelectorAll("input, select")

elementsToDisable.forEach((elem) => {
     elem.disabled = true;
})

function calculateNatOriginContent() {
    const rows = document.querySelectorAll(".form-row")
    const sumRawMaterials = Number(document.querySelector("#rm-sum-result").innerText)

    const rawResult = Array.from(rows).reduce((acc, curr) => {
        const content = curr.querySelector("input[id*='raw_material_content']").value
        const noc = curr.querySelector("input[id*='natural_origin_content']").value

        const calcResult = content * noc / 100

        return acc + calcResult

    }, 0)

    const result = Math.floor((rawResult / sumRawMaterials) * 100)
    if (sumRawMaterials <= 103 && sumRawMaterials >= 100) {
        document.querySelector("#noc-result").innerText = `${String(result)} %`
    } else {
        document.querySelector("#noc-result").innerText = "--- %"
    }
}

function sumContent() {
    const allContentFields = document.querySelectorAll("input[id*='raw_material_content']")
    const rmSum = Array.from(allContentFields).reduce((acc, curr) => {
        return acc + Number(curr.value);
    }, 0);
    document.getElementById('rm-sum-result').innerText = String(rmSum);
}