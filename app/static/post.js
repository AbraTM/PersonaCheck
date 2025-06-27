// Validating the data and sending it over to Flask Backend to be processed by the model

document.getElementById("PersonalityForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        Time_spent_alone : document.getElementById("aloneTime").value,
        Social_event_attendance : document.getElementById("spentOutside").value,
        Going_outside : document.getElementById("spentOutside").value,
        Friends_circle_size : document.getElementById("closeFriends").value,
        Post_frequency : document.getElementById("posts").value,
        Stage_fear : 0,
        Drained_after_socializing : 0
    }

    const stageFearRadio = document.querySelector("input[name='Stage_fear']:checked");
    data.Stage_fear = stageFearRadio ? (stageFearRadio.value === "yes" ? 1 : 0) : null;
    const drainedAfterSocailzingRadio = document.querySelector("input[name='Drained_after_socializing']:checked");
    data.Drained_after_socializing =drainedAfterSocailzingRadio ? (drainedAfterSocailzingRadio.value === "yes" ? 1 : 0) : null;

    try {
        console.log(data)
        const result = await postData(data)
        if(result){
            document.getElementById("submission_message").textContent = "Submission Successfull!!";
            document.getElementById("result_container").innerHTML = `
                <h2>${result.prediction === 1 ? "Extroverted" : "Introverted"}</h2>
            `
        }
    } catch (error) {
        document.getElementById("submission_message").textContent = `Submission Failed!!\nError : ${error.message}`;
    }
});

async function postData(data) {
    try {
        const res = await fetch("/submit", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });
        
        if(!res.ok){
            throw new Error(`Server responded with code ${res.status}`);
        }
        const result = res.json();
        console.log(result)
        return result;
    } catch (error) {
        console.log("Fetch failed : ", error);
    }
}