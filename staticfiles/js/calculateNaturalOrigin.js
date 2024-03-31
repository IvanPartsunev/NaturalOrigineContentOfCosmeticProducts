/* On load events: */

window.onload = () => {
    sumContent();
    calculateNatOriginContent();
}

/* Event listeners: */

document.querySelector("#add-row")
    .addEventListener("click", () => addRow())

document.querySelectorAll("a#remove-row > i").forEach((elem) => {
    elem.addEventListener(
        "click",
        (event) => removeRow(
            event.target
                .parentElement
                .parentElement
                .parentElement
        ))
})

document.querySelector("#noc-result")
    .addEventListener("click", () => calculateNatOriginContent())

document.querySelectorAll("input[type='number']").forEach((elem) => {
        elem.addEventListener("blur", () => calculateNatOriginContent())
    })

document.querySelectorAll("input[id*='raw_material_content']").forEach((elem) => {
    elem.addEventListener("keyup", () => sumContent())
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
    }
});

/* Base Functions: */

function addRow() {
    const baseForm = document.querySelectorAll("div[id^=form-]");
    const lastForm = baseForm.item(baseForm.length - 1);

    const cloneForm = lastForm.cloneNode(true);

    changeFormElementsIds(cloneForm);
    removeErrors(cloneForm);
    addEventListeners(cloneForm)

    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'));
    totalForms.value = Number(totalForms.value) + 1;

    document.querySelector("#container").appendChild(cloneForm);
}

function removeRow(currForm) {
    const currentForm = currForm
    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))

    if (currentForm.id !== "form-0" && totalForms.value > 1) {
        totalForms.value = Number(totalForms.value) - 1;

        subtractContent(currentForm);

        currentForm.classList.add("flip-out-hor-top")
        currentForm.addEventListener("animationend", () => {
            currentForm.remove();
            calculateNatOriginContent();
        });
    }
}

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

// Helper functions:

function changeFormElementsIds(form) {

    const id = form.id.split("-");
    const baseId = id[0];
    const newId = Number(id[1]) + 1;
    form.id = `${baseId}-${newId}`;

    const elements = form.querySelectorAll("input, select[id^='id_form']");
    elements.forEach((e) => {
        let initialId = e.id.split("-");
        let initialName = e.name.split("-");
        e.id = `${initialId[0]}-${newId}-${initialId[2]}`;
        e.name = `${initialName[0]}-${newId}-${initialName[2]}`;
        e.value = "";
    })
}

function removeErrors(form) {
    const errors = form.querySelectorAll(".error-list-2")
    if (errors.length > 0) {
        errors.forEach((err) => err.remove());
    }
}

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

function addEventListeners(form) {
    form.addEventListener("keyup", () => sumContent());
    form.querySelectorAll("input[type='number']").forEach((elem) => {
        elem.addEventListener("blur", () => calculateNatOriginContent())
    })

    form.lastElementChild
        .querySelector("a#remove-row > i")
        .addEventListener(
            "click",
            (event) => removeRow(
                event.target
                    .parentElement
                    .parentElement
                    .parentElement
            )
        );
}
