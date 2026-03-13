const API = "https://notes-api-nsn5.onrender.com"

let token = null


async function register(){

    const email = document.getElementById("reg_email").value
    const username = document.getElementById("reg_user").value
    const password = document.getElementById("reg_pass").value

    const res = await fetch(API + "/users/register", {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            email:email,
            username:username,
            password:password
        })
    })

    const data = await res.json()

    document.getElementById("resultado").textContent =
        JSON.stringify(data,null,2)
}



async function login(){

    const email = document.getElementById("log_email").value
    const password = document.getElementById("log_pass").value

    const form = new URLSearchParams()

    form.append("username",email)
    form.append("password",password)

    const res = await fetch(API + "/users/login", {
        method:"POST",
        body: form
    })

    const data = await res.json()

    token = data.access_token

    document.getElementById("resultado").textContent =
        JSON.stringify(data,null,2)
}



async function getMe(){

    const res = await fetch(API + "/me", {
        headers:{
            "Authorization": "Bearer " + token
        }
    })

    const data = await res.json()

    document.getElementById("resultado").textContent =
        JSON.stringify(data,null,2)
}