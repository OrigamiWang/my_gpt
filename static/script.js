let chatText = document.getElementById('chatText')
let submitBtn = document.getElementById('submitBtn')
let chatInfo = document.getElementById('chatInfo')
let session_id = null
// 页面加载成功时，获取session_id并保存在js中作为一次会话
window.onload = () => {
    console.log("the page is loaded...")
    fetch_session_id()
}
// 页面关闭时触发，将redis缓存中的数据持久化到mysql
window.onbeforeunload = () => {
    if (session_id != null) {
        navigator.sendBeacon('/cache/' + session_id, '');
        session_id = null
    }
}

chatText.oninput = () => {
    if (chatText.value === "") {
        submitBtn.value = "Input"
        submitBtn.setAttribute("disabled", "true")
    } else {
        submitBtn.value = "Send"
        submitBtn.removeAttribute("disabled")
    }
}

chatText.addEventListener("keyup", (event) => {
    // 回车 触发点击事件
    if (event.code === 'Enter') {
        submitBtn.click();
    }
})

function modify_submit_style() {
    submitBtn.setAttribute('disabled', '')
    submitBtn.value = 'Wait'

}

function recover_submit_style() {
    submitBtn.removeAttribute('disabled')
    submitBtn.value = 'Send'
}

function fetch_session_id() {
    fetch('/session_id')
        .then(function (response) {
            if (response) {
                session_id = response.headers.get('session_id')
                console.log("session_id is: " + session_id)
            }
        });
}

function setDivStyle(style) {
    style.backgroundColor = "#36292F"
    style.color = "#F3F9F1"
    style.width = "fit-content"
    style.maxWidth = "38%"
    style.padding = "1vw"
    style.margin = "2vh 3vw"
    style.borderRadius = "10px"
    style.wordBreak = "break-word"
}

function addQuestionDiv(text) {
    let question_div = document.createElement('div')
    let style = question_div.style
    question_div.innerText = text
    // 设置样式
    setDivStyle(style)
    style.float = "right"

    chatInfo.appendChild(question_div)
}

function addClearDiv() {
    let clear_div = document.createElement('div')
    clear_div.style.clear = "both"
    chatInfo.appendChild(clear_div)
}

function addAnswerDiv() {
    let answer_div = document.createElement('div')
    let style = answer_div.style
    // 设置样式
    setDivStyle(style)

    chatInfo.appendChild(answer_div)
    return answer_div
}

function appendAnswerText(question_div, text) {
    question_div.innerHTML = question_div.innerHTML + text
}

function submit() {
    console.log("submit...")
    modify_submit_style()
    let question = chatText.value
    // 清空输入框
    chatText.value = ""
    addQuestionDiv(question)
    addClearDiv()
    let url = "/gpt/" + session_id + "?question=" + question
    let source = new EventSource(url);
    let question_div = addAnswerDiv()
    source.onmessage = function (event) {
        if (event.data === "[DONE]") {
            recover_submit_style()
            source.close();
        } else {
            appendAnswerText(question_div, event.data)
            // chatInfo.innerText = chatInfo.innerText + event.data
        }
    }

}