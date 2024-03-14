const signUpButton = document.querySelector("button");
const submitButton = document.querySelector("#submit");
submitButton.addEventListener("click", () => {
    console.log("form has been submited");
})
signUpButton.addEventListener("click", () => {
    submitButton.click();
});
