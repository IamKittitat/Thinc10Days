const username = document.getElementById("inputUserName")
const password = document.getElementById("inputPassword")
const form = document.getElementById("form")
const errorElement = document.getElementById("error")

form.addEventListener("submit", (event) => {
    let messages = []
    if (messages.length > 0){
        e.preventDefault()
        errorElement.textContent = messages.join(", ")
    }
    if (password.value.length <= 6){
        messages.push("Password must be longer than 6 characters")
    }
    if (password.value === "password" || password.value === "Password"){
        messages.push("password can't be password")
    }
})