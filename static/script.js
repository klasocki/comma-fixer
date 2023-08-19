const commaFixingForm = document.querySelector(".comma-fixing-form");

const fixCommas = async (text) => {
    const inferResponse = await fetch(`baseline/fix-commas/`, {
        method: "POST",
        body: JSON.stringify({
            s: text
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    const inferJson = await inferResponse.json();

    return inferJson.s;
};

commaFixingForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const commaFixingInput = document.getElementById("comma-fixing-input");
    const commaFixingParagraph = document.querySelector(".comma-fixing-output");

    commaFixingParagraph.textContent = await fixCommas(commaFixingInput.value);
});