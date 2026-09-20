const car=[];
const no=6;
for(let i=0;i<no;i++){
    const trail=document.createElement("div");
    const car2=document.createElement("img");
    trail.className="trcar";
    car2.src="Textures/car/RGBBlackCar.png";
    car2.className="car";
    //temporariliy here, will be altered based on where it goes later
    trail.style.left=(i*20)+"%";
    trail.style.top=19+Math.random()*40+"%";
    trail.speed=0.3+Math.random()*0.7;
    trail.appendChild(car2);
    document.body.appendChild(trail);
    car.push(trail);
}   
//i like to mov it move it 
function move(){
    for(let i=0;i<car.length;i++){
        let x=parseFloat(car[i].style.left);
        x+=car[i].speed;
        if(x>100){
            x=-10;
        }
        car[i].style.left=x+"%";
    }
    requestAnimationFrame(move);
}
move();

