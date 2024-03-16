import { addRow, removeRow } from "./addRemoveFuncs";

document.querySelector("#add-row")
    .addEventListener("click", () => {
        addRow();
    })

document.querySelector("#remove-row")
    .addEventListener("click", () => {
        removeRow();
    })
