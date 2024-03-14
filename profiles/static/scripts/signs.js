const signUp = document.querySelector(".up");
const signIn = document.querySelector(".in");


function changeDisplay_1() {
    const form_1 = document.querySelector(".form1");
    const form_2 = document.querySelector(".form2");
    if (signUp.classList.contains("sign-background")) {
        console.log("sign-up already displayed");
    }
    else {
        form_1.classList.remove("form-display");
        form_2.classList.add("form-display");
        signUp.classList.add("sign-background");
        signUp.classList.remove("sign-pointer");
        signIn.classList.add("sign-pointer");
        signIn.classList.remove("sign-background");
    }
}
function changeDisplay_2() {
    const form_1 = document.querySelector(".form1");
    const form_2 = document.querySelector(".form2");
    if (signIn.classList.contains("sign-background")) {
        console.log("sign-in already displayed");
    }
    else {
        form_2.classList.remove("form-display");
        form_1.classList.add("form-display");
        signUp.classList.remove("sign-background");
        signUp.classList.add("sign-pointer");
        signIn.classList.remove("sign-pointer");
        signIn.classList.add("sign-background");
    }
}
signUp.addEventListener("click", changeDisplay_1);
signIn.addEventListener("click", changeDisplay_2);
