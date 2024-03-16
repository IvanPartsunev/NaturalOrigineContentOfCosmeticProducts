function changeInputId(formElements, newId) {
    console.log(formElements)
    const elements = formElements.querySelectorAll("input")

    elements.forEach((e) => {
        let initialId = e.id.split("-")
        let initialName = e.name.split("-")
        e.id = `${initialId[0]}-${newId}-${initialId[2]}`
        e.name = `${initialName[0]}-${newId}-${initialName[2]}`
    })
}

export {changeInputId};