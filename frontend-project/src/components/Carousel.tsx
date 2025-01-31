import img1 from "../assets/I1.png"
import img2 from "../assets/I2.png"
import img3 from "../assets/I3.png"

export default function Carousel (){
    return (
        <div className="contenedorC" >
        <div id="carouselExampleSlidesOnly" className="carousel slide " data-bs-ride="carousel">
  <div className="carousel-inner">
    <div className="carousel-item active">
      <img src={img1}  id="imgC" className="d-block w-100" alt="pastel1" />
    </div>
    <div className="carousel-item">
      <img src={img2} id="imgC" className="d-block w-100" alt="pastel2" />
    </div>
    <div className="carousel-item">
      <img src={img3} id="imgC" className="d-block w-100" alt="pastel3"/>
    </div>
  </div>
</div>
</div>
    );
}