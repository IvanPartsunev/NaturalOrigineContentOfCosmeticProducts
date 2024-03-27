// Event listeners:

document.querySelector("#add-row")
    .addEventListener("click", () => addRow())

document.querySelector("#remove-row")
    .addEventListener("click", () => removeRow())

// document.querySelector("#select_material")
//     .addEventListener("change", (e) => {
//         const form = e.currentTarget.parentElement
//         removeErrors(form)
//     })

// document.querySelector("input[id*='raw_material_content']")
//     .addEventListener("change", () => sumContent())

// Base Functions:

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

function addRow() {
    const baseForm = document.querySelectorAll("div[id^=form-]");
    const lastForm = baseForm.item(baseForm.length - 1);

    const cloneForm = lastForm.cloneNode(true);

    changeFormElementsIds(cloneForm);
    removeErrors(cloneForm);

    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'));
    totalForms.value = Number(totalForms.value) + 1;

    document.querySelector("#container").appendChild(cloneForm);
}

function removeRow() {
    const current_form = document.querySelector("#container").lastElementChild;
    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))
    if (current_form.id !== "form-0" && totalForms.value > 1) {
        totalForms.value = Number(totalForms.value) - 1
        current_form.remove()
    }
}

// function sumContent() {
//     const allContentFields = document.querySelectorAll("input[id*='raw_material_content']")
//     let sum = 0
//
//     allContentFields.forEach(function (input) {
//         console.log
//         const value = parseFloat(input.value);
//
//         sum += value;
//     });

    // Display the result
    // document.getElementById('result').innerText = "Sum: " + sum;
// }

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