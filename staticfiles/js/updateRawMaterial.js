document.querySelector("#select_material")
    .addEventListener("change", (e) => {
        const currentForm = e.currentTarget.parentElement
        currentForm.submit()
    });