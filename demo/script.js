const API_URL = "https://notes-api-nsn5.onrender.com"

let token = localStorage.getItem("token")

document.addEventListener("DOMContentLoaded", () => {
if(token){
startApp()
}
})

function headers(){
return {
"Authorization": "Bearer " + token,
"Content-Type": "application/json"
}
}

function startApp(){
document.getElementById("auth").style.display = "none"
document.getElementById("app").classList.remove("hidden")
loadBoards()
}

function logout(){
localStorage.removeItem("token")
location.reload()
}

async function register(){

let email = reg_email.value
let username = reg_user.value
let password = reg_pass.value

if(!email || !username || !password){
alert("Campos vacíos")
return
}

let res = await fetch(API_URL+"/users/register",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({email,username,password})
})

if(!res.ok){
alert("Error al registrar")
return
}

alert("Usuario creado")
}

async function login(){

let form = new URLSearchParams()

form.append("username", login_email.value)
form.append("password", login_pass.value)

let res = await fetch(API_URL+"/users/login",{
method:"POST",
body:form
})

if(!res.ok){
alert("Credenciales incorrectas")
return
}

let data = await res.json()

token = data.access_token

localStorage.setItem("token",token)

startApp()
}

async function loadBoards(){

let res = await fetch(API_URL+"/boards",{
headers:headers()
})

let boards = await res.json()

let container = document.getElementById("boards")

container.innerHTML=""

boards.forEach(b=>{

let div = document.createElement("div")
div.className="board"
div.style.background=b.color || "#eee"

div.innerHTML = `

<div class="board-top">

<b>${b.name}</b>

<button class="delete-board"
onclick="deleteBoard(${b.id}, event)">✕</button>

</div>

`

div.onclick=()=>openBoard(b.id)

container.appendChild(div)

})
}

async function deleteBoard(id, e){

e.stopPropagation()

if(!confirm("¿Eliminar este tablero?")) return

await fetch(API_URL+"/boards/"+id,{
method:"DELETE",
headers:headers()
})

loadBoards()

}

async function createBoard(){

let name = board_name.value
let color = selectedColor

if(!name.trim()){
alert("El tablero necesita título")
return
}

await fetch(API_URL+"/boards",{
method:"POST",
headers:headers(),
body:JSON.stringify({name,color})
})

board_name.value=""

loadBoards()
}

async function openBoard(id){

let res = await fetch(API_URL+"/boards/"+id,{
headers:headers()
})

let board = await res.json()

currentTasks = board.tasks
currentBoard = id

let html = `
<h2>${board.name}</h2>

<div class="board-layout">

<div class="card">

<h3>Nueva tarea</h3>

<input id="task_title" class="modern-input" placeholder="Título">

<input id="task_desc" class="modern-input" placeholder="Descripción">

<select id="task_state" class="modern-input">
<option value="pendiente">Pendiente</option>
<option value="en progreso">En progreso</option>
<option value="completada">Completada</option>
</select>

<button class="primary modern-btn" onclick="createTask(${id})">
Añadir tarea
</button>

</div>

<div class="card tasks-panel" style="background:${board.color || "#f0f0f0"}">

<h3>Tareas</h3>

<div class="task-filters">

<button onclick="filterTasks('todas')">Todas</button>

<button onclick="filterTasks('pendiente')">Pendientes</button>

<button onclick="filterTasks('en progreso')">En progreso</button>

<button onclick="filterTasks('completada')">Completadas</button>

</div>

<div id="tasks"></div>

</div>

</div>
`

document.getElementById("board_detail").innerHTML = html

renderTasks(currentTasks,id)

}



function renderTasks(tasks, board_id){
    let div = document.getElementById("tasks")
    div.innerHTML = ""

    tasks.forEach(t=>{
        let el = document.createElement("div")
        el.className = "task " + (t.estado === "completada" ? "done" : "")
        el.dataset.taskId = t.id // guardamos el id de la tarea

        el.innerHTML = `
            <div class="task-info">
                <div class="task-title">${t.titulo}</div>
                <div class="task-desc">${t.descripcion || ""}</div>
                <span class="task-state ${t.estado.replace(" ","-")}">${t.estado}</span>
            </div>
            <button class="delete-task">X</button>
        `
        div.appendChild(el)
    })

    // Delegamos el click en el contenedor
    div.onclick = async function(e){
        let taskEl = e.target.closest(".task")
        if(!taskEl) return

        let taskId = taskEl.dataset.taskId
        if(!taskId) return

        // Si clickeamos el botón de borrar, eliminamos
        if(e.target.classList.contains("delete-task")){
            e.stopPropagation()
            deleteTask(taskId, board_id)
            return
        }

        // Sino, alternamos estado
        await cycleTaskState(taskId, board_id)
    }
}


async function createTask(board_id){

let titulo = task_title.value
let descripcion = task_desc.value
let estado = task_state.value

if(!titulo.trim()){
alert("La tarea necesita título")
return
}

await fetch(API_URL+"/tasks",{
method:"POST",
headers:headers(),
body:JSON.stringify({
titulo,
descripcion,
estado,
prioridad:1,
board_id
})
})

openBoard(board_id)
}

async function toggleTask(task_id,board_id,done){

let estado = done ? "completada" : "pendiente"

await fetch(API_URL+"/tasks/"+task_id,{
method:"PUT",
headers:headers(),
body:JSON.stringify({estado})
})

openBoard(board_id)
}

async function deleteTask(task_id,board_id){

await fetch(API_URL+"/tasks/"+task_id,{
method:"DELETE",
headers:headers()
})

openBoard(board_id)
}

function showLogin(){

login_form.classList.remove("hidden")
register_form.classList.add("hidden")

login_tab.classList.add("active")
register_tab.classList.remove("active")
}

function showRegister(){

register_form.classList.remove("hidden")
login_form.classList.add("hidden")

register_tab.classList.add("active")
login_tab.classList.remove("active")
}



let selectedColor = "#ffd6e0"

function selectColor(color, element){

selectedColor = color

document.querySelectorAll(".color-option").forEach(c=>{
c.classList.remove("active")
})

element.classList.add("active")
}

function filterTasks(filter){

currentFilter = filter

let tasks = currentTasks

if(filter!="todas"){
tasks = tasks.filter(t=>t.estado===filter)
}

renderTasks(tasks,currentBoard)

}

async function cycleTaskState(task_id, board_id) {
    // 1. Encontrar la tarea en el array local para saber su estado actual
    let task = currentTasks.find(t => t.id == task_id);
    if (!task) return;

    // 2. Definir el ciclo
    const estados = ["pendiente", "en progreso", "completada"];
    let idx = estados.indexOf(task.estado);
    let nuevoEstado = estados[(idx + 1) % estados.length];

    // 3. Notificar al servidor
    try {
        await fetch(API_URL + "/tasks/" + task_id, {
            method: "PUT",
            headers: headers(),
            body: JSON.stringify({ estado: nuevoEstado })
        });

        // 4. Refrescar el tablero completo para ver los cambios
        openBoard(board_id);
    } catch (error) {
        console.error("Error al actualizar estado:", error);
    }
}