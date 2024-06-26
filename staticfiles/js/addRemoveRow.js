/* Event listeners: */

document.querySelector("#add-row")
    .addEventListener(
        "click",
        (event) => {
            event.preventDefault()
            addRow()
        })

document.querySelectorAll("a#remove-row").forEach((elem) => {
    elem.addEventListener(
        "click",
        (event) => {
            event.preventDefault()
            removeRow(
                event.target
                    .parentElement
                    .parentElement
                    .parentElement
            )
        }
    )
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

    cloneForm.scrollIntoView({behavior: "smooth"});
}

function removeRow(currForm) {
    const currentForm = currForm
    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))
    const initialForms = document.querySelector(('#id_form-INITIAL_FORMS'))

    if (currentForm.id.includes("form") && currentForm.id !== "form-0" && totalForms.value > 1) {
        totalForms.value = Number(totalForms.value) - 1;
        initialForms.value = Number(initialForms.value) - 1;

        subtractContent(currentForm);

        currentForm.classList.add("flip-out-hor-top")
        currentForm.addEventListener("animationend", () => {
            currentForm.remove();
            calculateNatOriginContent();
            updateFormIndices()
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

function addEventListeners(form) {
    form.addEventListener("keyup", () => sumContent());
    form.querySelectorAll("input[type='number']").forEach((elem) => {
        elem.addEventListener("blur", () => calculateNatOriginContent())
    })

    form.lastElementChild
        .querySelector("a#remove-row")
        .addEventListener(
            "click",
            (event) => {
                event.preventDefault()
                removeRow(
                    event.target
                        .parentElement
                        .parentElement
                        .parentElement
                )
            }
        );
}

function updateFormIndices() {
    const forms = document.querySelectorAll('.form-row');

    forms.forEach((form, index) => {

        form.id = `form-${index}`;
        form.querySelectorAll('input, select').forEach(input => {
            const name = input.name.replace(/-\d+-/, `-${index}-`);
            const id = input.id.replace(/-\d+-/, `-${index}-`);
            input.name = name;
            input.id = id;
        });
    });
}