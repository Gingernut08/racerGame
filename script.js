const car=[];
const no=6;
const top=30;
const bot=65;
for(let i=0;i<no;i++){
    const car2=document.createElement("img");
    car2.src="Textures/car/RGBBlackCar.png"
    car2.className="car";
    //temporariliy here, will be altered based on where it goes later
    car2.style.left=Math.random()*100+"%";
    car2.style.top=top+Math.random()*(bot-top)+"%";
    document.body.appendChild(car2);
    car.push(car2)
}
//i like to mov it move it 
function move(){
    for(let i=0;i<car.length;i++){
        let x=parseFloat(car[i].style.left);
        x+=0.2;
        if(x>100){
            x=-10
        }
        car[i].style.left=x+"%"
    }
    requestAnimationFrame(move);
}
move();