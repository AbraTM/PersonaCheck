// Handling Slider Values

const inputSliders = document.querySelectorAll(".slider");

inputSliders.forEach((slider) => {
    const output = document.getElementById(`output${slider.id}`);
    if(output){
        output.textContent = slider.value;
        slider.addEventListener("input", () => {
            output.textContent = slider.value;
        })
    }
});