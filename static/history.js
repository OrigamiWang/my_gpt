let history_container = document.getElementById('history')
let history_arr

function create_history_box(id, input_value, sidebar_datetime) {
    // 1.
    let history_box = document.createElement('div')
    history_box.setAttribute('id', "box" + id)
    history_box.setAttribute('class', 'history_box')
    history_container.appendChild(history_box)
    // 2.
    let history_input = document.createElement('input')
    history_input.value = input_value
    history_input.setAttribute('disabled', '')
    history_input.setAttribute('id', "input" + id)
    history_input.setAttribute('class', 'left history_input')
    history_box.appendChild(history_input)
    // 3.
    let history_sidebar = document.createElement('div')
    history_sidebar.innerText = sidebar_datetime
    history_sidebar.setAttribute('id', "sidebar" + id)
    history_sidebar.setAttribute('class', 'right history_sidebar')
    history_box.appendChild(history_sidebar)

    let res = []
    res.push(history_box)
    res.push(history_input)

    return res
}

function mouse_enter(box, input) {
    box.addEventListener("mouseenter", () => {
        box.setAttribute('class', 'history_box mouse_enter_box')
        input.setAttribute('class', 'left history_input mouse_enter_input')
    })
}

function mouse_leave(box, input) {
    box.addEventListener("mouseleave", () => {
        box.setAttribute('class', 'history_box')
        input.setAttribute('class', 'left history_input')
    })
}

function remove_past_conversation() {
    console.log("remove past conversation...")
    let div = document.getElementById("chatInfo");
    while (div.hasChildNodes()) {
        div.removeChild(div.firstChild);
    }
}

function create_history_list() {

    for (let i = 0; i < history_arr.length; i++) {
        let history = history_arr[i]
        let res = create_history_box(history[0], history[1], history[2])
        let box = res[0]
        let input = res[1]
        mouse_enter(box, input)
        mouse_leave(box, input)
        access_history(box, input)
    }
}

function load_history_div(content_list) {
    console.log("history div loading...")
    content_list.forEach(content => {
        console.log(content)
        if (content[2] === 3) {
            //  回答
            let answer_div = addAnswerDiv()
            appendAnswerText(answer_div, content[3])
        } else {
            // 提问
            addQuestionDiv(content[3])
        }
        addClearDiv()
    })
}

function fetch_content_by_msg_id(msg_id) {
    fetch('/content/' + msg_id)
        .then(response => response.json())
        .then(data => {
            session_id = data["session_id"]
            let content_list = data["content_list"]
            load_history_div(content_list)
        })

}

// 访问历史记录
function access_history(box) {
    box.onclick = () => {
        // 先删除div内原本的所有元素
        remove_past_conversation()
        console.log("click box...")
        // message位于数据库的索引
        const id = box.id.substring(3)
        // id -> session_id -> content[]
        fetch_content_by_msg_id(id)

    }

}

async function fetch_load_history() {
    await fetch('/loadHistory')
        .then(response => response.json())
        .then(data => {
            history_arr = data
        })
}

async function load_history() {
    await fetch_load_history()
    create_history_list(history_arr)
}


