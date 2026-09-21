const car=[];
const no=6;
for(let i=0;i<no;i++){
    const trail=document.createElement("div");
    const car2=document.createElement("img");
    trail.className="trcar";
    car2.src="../Textures/car/RGBBlackCar.png";
    car2.className="car";
    //temporariliy here, will be altered based on where it goes later//altered soignore
    trail.style.left=(i*20)+"%";
    trail.style.top=19+Math.random()*40+"%";
    trail.speed=0.3+Math.random()*0.7;  
    trail.sp=trail.speed;  
    trail.lane=parseFloat(trail.style.top);
    trail.s1=0.01+Math.random()*0.04;
    trail.s2=Math.random()*100;
    trail.s3=1+Math.random()*4;
    trail.appendChild(car2);
    document.body.appendChild(trail);
    car.push(trail);
}   
//i like to mov it move it 
let mouseX=0;
let mouseY=0;
document.addEventListener("mousemove",function(e){
    mouseX=e.clientX;
    mouseY=e.clientY
});
function move(){
    for(let i=0;i<car.length;i++){
        //hmmm trafficc behaviour
        let x=parseFloat(car[i].style.left);
        let sp=car[i].speed;
        let box=car[i].getBoundingClientRect();
        let mx=mouseX;
        let my=mouseY;
        if(mx>box.left && mx<boxx.right && my>box.top && my<box.bottom){
            target=0;
        }
        car[i].s2+=car[i].s1;
        let s5=Math.sin(car[i].s2)*car[i].s3;
        car[i].style.top=(car[i].lane+s5)+"%";
        let target=car[i].speed;
        for(let j=0;j<car.length;j++){
            if(i===j)continue;
            let pt1=parseFloat(car[j].style.left);
            let pt2=parseFloat(car[j].style.top);
            let gap=pt1-x;
            let side=Math.abs(pt2-parseFloat(car[i].style.top));
            if(gap>0 && gap<6 && side<3){
                target=0.15;
            } 
        }
        if(target===0.15){
            car[i].sp+=(target-car[i].sp)*0.4;
        }
        else{
            car[i].sp+=(target-car[i].sp)*0.8;
        }
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

//leaderboard time, lowk wish i had an easy way to use emojs here or memes thatd be really cool
fetch("leaderboard.json")
    .then(function(res){
        return res.json();
    })
    .then(function(data){
        console.log(data);        
        let lele=document.getElementById("lele");
        data.score.sort(function(a,b){
            return a.time-b.time;
        })  
           
            let head=document.createElement("div");
            let hrank=document.createElement("span");
            let hname=document.createElement("span");
            let htime=document.createElement("span");
            hrank.textContent="RANK";
            hname.textContent="NAME";
            htime.textContent="TIME";
            head.appendChild(hrank);
            head.appendChild(hname);
            head.appendChild(htime);
            lele.appendChild(head);
            head.className="head";
        for(let i=0;i<data.score.length;i++){
            console.log(data.score[i].name);
            console.log(data.score[i].time); 
            let row=document.createElement("div");
            let rank=document.createElement("span");
            let name= document.createElement("span");
            let time=document.createElement("span");
            rank.textContent=1+i;
            name.textContent=data.score[i].name;
            time.textContent=(data.score[i].time/100).toFixed(2)+"s";
            row.appendChild(rank);
            row.appendChild(name);
            row.appendChild(time);
            lele.appendChild(row);
            row.style.animationDelay=(i*0.1)+"s";
            if(i===0){
                row.style.border="3px solid gold";
                row.style.color="gold";
                row.className="one";
            }
            if(i===1){
                row.style.border="3px solid silver";
                row.style.color="silver";
                row.className="two";
            }
            if(i===2){
                row.style.border="3px solid #cd7f32"
                row.style.color="#cd7f32";
                row.className="three";
            }
        }

    })
let tut=document.getElementById("tut");
let pop=document.getElementById("pop");
let close=document.getElementById("cl");
tut.addEventListener("click",function(){
    pop.style.display="flex";
});
cl.addEventListener("click",function(){
    pop.style.display="none";
})

