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

/* Helper functions: */

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