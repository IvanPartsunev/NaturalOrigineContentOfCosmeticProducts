/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./staticfiles/JS/addRemoveFuncs.js":
/*!******************************************!*\
  !*** ./staticfiles/JS/addRemoveFuncs.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   addRow: () => (/* binding */ addRow),\n/* harmony export */   removeRow: () => (/* binding */ removeRow)\n/* harmony export */ });\n/* harmony import */ var _helperFunctions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./helperFunctions */ \"./staticfiles/JS/helperFunctions.js\");\n\n\nfunction addRow() {\n    const baseForm = document.querySelectorAll(\"div[id^=form-]\");\n    const lastForm = baseForm.item(baseForm.length - 1);\n\n    const cloneForm = lastForm.cloneNode(true)\n\n    const id = cloneForm.id.split(\"-\")\n    const baseId = id[0]\n    const newId = Number(id[1]) + 1\n\n    cloneForm.id = `${baseId}-${newId}`;\n\n    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))\n    totalForms.value = Number(totalForms.value) + 1\n\n    ;(0,_helperFunctions__WEBPACK_IMPORTED_MODULE_0__.changeInputId)(cloneForm, newId)\n\n    document.querySelector(\"#container\").appendChild(cloneForm)\n}\n\nfunction removeRow() {\n    const current_form = document.querySelector(\"#container\").lastElementChild;\n    const totalForms = document.querySelector(('#id_form-TOTAL_FORMS'))\n    if (current_form.id !== \"form-0\" && totalForms.value > 1) {\n        totalForms.value = Number(totalForms.value) - 1\n        current_form.remove()\n    }\n}\n\n\n\n\n\n\n//# sourceURL=webpack://naturalorigincontentofcosmeticproducts/./staticfiles/JS/addRemoveFuncs.js?");

/***/ }),

/***/ "./staticfiles/JS/helperFunctions.js":
/*!*******************************************!*\
  !*** ./staticfiles/JS/helperFunctions.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   changeInputId: () => (/* binding */ changeInputId)\n/* harmony export */ });\nfunction changeInputId(formElements, newId) {\n    console.log(formElements)\n    const elements = formElements.querySelectorAll(\"input\")\n\n    elements.forEach((e) => {\n        let initialId = e.id.split(\"-\")\n        let initialName = e.name.split(\"-\")\n        e.id = `${initialId[0]}-${newId}-${initialId[2]}`\n        e.name = `${initialName[0]}-${newId}-${initialName[2]}`\n    })\n}\n\n\n\n//# sourceURL=webpack://naturalorigincontentofcosmeticproducts/./staticfiles/JS/helperFunctions.js?");

/***/ }),

/***/ "./staticfiles/JS/index.js":
/*!*********************************!*\
  !*** ./staticfiles/JS/index.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _addRemoveFuncs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./addRemoveFuncs */ \"./staticfiles/JS/addRemoveFuncs.js\");\n\n\ndocument.querySelector(\"#add-row\")\n    .addEventListener(\"click\", () => {\n        (0,_addRemoveFuncs__WEBPACK_IMPORTED_MODULE_0__.addRow)();\n    })\n\ndocument.querySelector(\"#remove-row\")\n    .addEventListener(\"click\", () => {\n        ;(0,_addRemoveFuncs__WEBPACK_IMPORTED_MODULE_0__.removeRow)();\n    })\n\n\n//# sourceURL=webpack://naturalorigincontentofcosmeticproducts/./staticfiles/JS/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./staticfiles/JS/index.js");
/******/ 	
/******/ })()
;