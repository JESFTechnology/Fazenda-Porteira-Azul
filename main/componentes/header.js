const headerTemplate = document.createElement('template');

headerTemplate.innerHTML = `
    <style>

    header {
        width: 100%;
        max-width: 900px;
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0;
        flex-wrap: wrap;
        position: sticky;
        top: 0;
        z-index: 10;
    }

    header a {
        text-decoration: none;
        color: #1e90ff;
        font-weight: 600;
        font-size: 1rem;
        margin: 10px 20px;
        transition: 0.3s;
        border-bottom: 2px solid transparent;
        }

    header a:hover {
            color: #0d6efd;
            border-color: #0d6efd;
    }

    nav {
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    ul {
      padding: 0;
    }
    
    ul li {
      list-style: none;
      display: inline;
    }
  </style>

  <header>
    <nav>
      <ul>
        <li><a href="demo-main.html">Início</a></li>        
        <li><a href="demo-estoque.html">Estoque</a></li>
        <li><a href="demo-funcionario.html">Funcionários</a></li>
        <li><a href="">Maquinário</a></li>
      </ul>
    </nav>
  </header>
`;

class Header extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const shadowRoot = this.attachShadow({ mode: 'closed' });

    shadowRoot.appendChild(headerTemplate.content);
  }
}

customElements.define('header-component', Header);