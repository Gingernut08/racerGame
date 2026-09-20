const car=[];
const no=6;
for(let i=0;i<no;i++){
    const trail=document.createElement("div");
    const car2=document.createElement("img");
    trail.className="trcar";
    car2.src="Textures/car/RGBBlackCar.png";
    car2.className="car";
    //temporariliy here, will be altered based on where it goes later//altered soignore
    trail.style.left=(i*20)+"%";
    trail.style.top=19+Math.random()*40+"%";
    trail.speed=0.3+Math.random()*0.7;  
    trail.sp=trail.speed;  
    trail.lane=parseFloat(trail.style.top);
    trail.s1=0.01+Math.random()*0.03;
    trail.s2=Math.random()*100;
    trail.s3=1+Math.random()*3;
    trail.appendChild(car2);
    document.body.appendChild(trail);
    car.push(trail);
}   
//i like to mov it move it 
function move(){
    for(let i=0;i<car.length;i++){
        //hmmm trafficc behaviour
        let x=parseFloat(car[i].style.left);
        let sp=car[i].speed;
        car[i].s2+=car[i].s1;
        let s5=Math.sin(car[i].s2)*car[i].s3;
        car[i].style.top=(car[i].lane+s5)+"%";
        let target=car[i].speed;
        for(let j=0;j<car.length;j++){
            if(i===j)continue;
            let pt1=parseFloat(car[j].style.left);
            let gap=pt1-x;        
       
            if(gap>0 && gap<3){
                target=0.15;
            } 
        }
        car[i].sp+=(sp-car[i].sp)*0.4;
        x+=car[i].sp;
        if(x>100){
            x=-10;
            car[i].lane=19+Math.random()*40;
        }
        car[i].style.left=x+"%";
    }
    requestAnimationFrame(move);
}
move();

