class MessageBox extends HTMLElement {
  constructor() {
    super()
    const shaDom = this.attachShadow({ mode: "open" })
    this.p = this.h("p")
    this.p.innerText = "hello"
    this.p.setAttribute("style", "width:200px; height:200px;border:1px solid red")
    shaDom.appendChild(this.p)
  }

  h(el) {
    return document.createElement(el)
  }
}


window.customElements.define("message-box", MessageBox)