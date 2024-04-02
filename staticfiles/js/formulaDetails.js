/* Disable all elements for product formula details view */

const elementsToDisable = document.querySelectorAll("input, select")

elementsToDisable.forEach((elem) => {
    elem.disabled = true;
})
