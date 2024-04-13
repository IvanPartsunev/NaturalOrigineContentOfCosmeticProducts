/* On load events: */

window.onload = () => {
    sumContent();
    calculateNatOriginContent();
}

/* Event listeners: */

document.querySelector("#noc-result")
    .addEventListener("click", (event) => {
        event.preventDefault();
        calculateNatOriginContent();
    })

document.querySelectorAll("input[type='number']").forEach((elem) => {
    elem.addEventListener("blur", (event) => {
        event.preventDefault();
        calculateNatOriginContent();
    })
})

document.querySelectorAll("input[id*='raw_material_content']").forEach((elem) => {
    elem.addEventListener("keyup", (event) => {
        event.preventDefault()
        sumContent();
    })
})


/* Add styles to elements*/

const fieldContainers = document.querySelectorAll('.field-container');
fieldContainers.forEach(container => {
    if (container.querySelector('[id*="trade_name"]') || container.querySelector('[id*="inci_name"]')) {
        container.classList.add('large-fields');
    }
});

fieldContainers.forEach(container => {
    if (container.querySelector('[id*="raw_material_content"]') || container.querySelector('[id*="natural_origin_content"]')) {
        container.classList.add('small-fields');
    }
});

fieldContainers.forEach(container => {
    if (container.querySelector('[id*="material_type"]')) {
        container.classList.add('type-fields');
        container.classList.add('custom-select-1');
    }
});

/* Base Functions: */

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

/*Helper functions:*/

function sumContent() {
    const allContentFields = document.querySelectorAll("input[id*='raw_material_content']")
    const rmSum = Array.from(allContentFields).reduce((acc, curr) => {
        return acc + Number(curr.value);
    }, 0);
    document.getElementById('rm-sum-result').innerText = String(rmSum);
}

function subtractContent(currentElem) {
    const rmSum = document.querySelector("#rm-sum-result")
    const currentElemId = currentElem.id
    const subtractValueInput = document.querySelector(`#${currentElemId} div input[id*='raw_material_content']`)
    const subtractValue = Number(subtractValueInput.value);
    const currentRmSum = Number(rmSum.innerText);

    rmSum.innerText = String(currentRmSum - subtractValue);
}

