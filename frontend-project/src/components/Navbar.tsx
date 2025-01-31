
import logo from '../assets/LOGOT.png'

export default function Navbar(){
return  ( 

    <nav className="navbar navbar-expand navbar-dark mi-navbar fixed-top">
        <div className="container">
          <a className="navbar-brand" id='miNavbar' href="#">
            <img  src={logo} alt="logo" className="logoT" />
               TartamIA
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li  className="nav-item">
                <a id="Opciones" className="nav-link" href="#">
                  Home
                </a>
              </li>
              <li className="nav-item items" >
                <a id="Opciones" className="nav-link" href="#">
                  Acerca de
                </a>
              </li>
              <li className="nav-item">
                <a id="Opciones" className="nav-link" href="#">
                ¡Haz tu Pastel!
                </a>
              </li>
              <li className="nav-item">
                <a id="Opciones" className="nav-link" href="#">
                  Contacto
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

);

}