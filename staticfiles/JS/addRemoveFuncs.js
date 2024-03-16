import {changeInputId} from "./helperFunctions";

function addRow() {
    const baseForm = document.querySelectorAll("div[id^=form-]");
    const lastForm = baseForm.item(baseForm.length - 1);

    const cloneForm = lastForm.cloneNode(true)

    const id = cloneForm.id.split("-")
    const baseId = id[0]
    const newId = Number(id[1]) + 1

    cloneForm.id = `${baseId}-${newId}`;

    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))
    totalForms.value = Number(totalForms.value) + 1

    changeInputId(cloneForm, newId)

    document.querySelector("#container").appendChild(cloneForm)
}

function removeRow() {
    const current_form = document.querySelector("#container").lastElementChild;
    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))
    if (current_form.id !== "form-0" && totalForms.value > 1) {
        totalForms.value = Number(totalForms.value) - 1
        current_form.remove()
    }
}



export {addRow};
export {removeRow};