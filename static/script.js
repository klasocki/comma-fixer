const commaFixingForm = document.querySelector(".comma-fixing-form");

const fixCommas = async (text) => {
    let request = {
        method: "POST",
        body: JSON.stringify({
            s: text
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    };
    const baselineResponse = await fetch(`baseline/fix-commas/`, request);
    const fixerResponse = await fetch(`fix-commas/`, request);
    const baselineJson = await baselineResponse.json();
    const inferJson = await fixerResponse.json();

    return {baseline: baselineJson.s, main: inferJson.s};
};

commaFixingForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const commaFixingInput = document.getElementById("comma-fixing-input");
    const commaFixingParagraph = document.querySelector(".comma-fixing-output");

    const fixed = await fixCommas(commaFixingInput.value);

    commaFixingParagraph.textContent = `Our model: ${fixed.main}\n\nBaseline model: ${fixed.baseline}`
});