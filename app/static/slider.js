const inputValue = document.getElementById("inputValue");
const outputValue = document.getElementById("outputValue");

inputValue.addEventListener("input", function() {
    outputValue.textContent = inputValue.value;
});