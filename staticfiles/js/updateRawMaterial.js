// Responsible for changing raw materials to update in raw material update view

document.querySelector("#select_material")
    .addEventListener("change", (e) => {
        const currentForm = e.currentTarget.parentElement
        currentForm.submit()
    });
