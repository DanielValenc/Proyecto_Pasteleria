import  Navbar from './components/Navbar' ;
import Carousel from './components/Carousel';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './App.css'

function App() {
  

  return (
    <>

      <Navbar />
      <div id='contenidoFrase'>
      <p> Tu idea es nuestra receta perfecta</p>
      </div>
      <div id='contenidoCar'>
      <div className="container mt-5">
                <Carousel />
      </div>
      </div>
      
    </>
  )
}

export default App
