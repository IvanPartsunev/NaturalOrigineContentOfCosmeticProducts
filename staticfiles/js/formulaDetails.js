/* Disable all elements for product formula details view */

const elementsToDisable = document.querySelectorAll("input, select")

elementsToDisable.forEach((elem) => {
    console.log(elem)
    elem.disabled = true;
})
