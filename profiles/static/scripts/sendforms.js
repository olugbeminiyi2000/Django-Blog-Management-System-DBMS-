const signUpButton = document.querySelector(".sign-up-button");
const signInButton = document.querySelector(".sign-in-button");
const signUpSubmit = document.querySelector("#sign-up");
const signInSubmit = document.querySelector("#sign-in");

signInSubmit.addEventListener("click", () => {
    console.log("sign-in form submitted.")
})
signUpSubmit.addEventListener("click", () => {
    console.log("sign-up form submitted.")
})
function clickSubmitSignUp() {
    signUpSubmit.click()
}
function clickSubmitSignIn() {
    signInSubmit.click()
}
signUpButton.addEventListener("click", clickSubmitSignUp)
signInButton.addEventListener("click", clickSubmitSignIn)
