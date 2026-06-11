import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="운석 피하기", layout="centered")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body{
    margin:0;
    overflow:hidden;
    background:black;
}

canvas{
    display:block;
    margin:auto;
    background:linear-gradient(to bottom,#000428,#004e92);
}
</style>
</head>

<body>

<canvas id="game" width="800" height="600"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let player = {
    x: 375,
    y: 530,
    width:50,
    height:50,
    speed:7
};

let meteors = [];
let score = 0;

const keys = {};

document.addEventListener("keydown", e=>{
    keys[e.key]=true;
});

document.addEventListener("keyup", e=>{
    keys[e.key]=false;
});

function createMeteor(){
    meteors.push({
        x: Math.random()*770,
        y:-30,
        size:20+Math.random()*30,
        speed:3+Math.random()*5
    });
}

setInterval(createMeteor,500);

function update(){

    if(keys["ArrowLeft"]){
        player.x -= player.speed;
    }

    if(keys["ArrowRight"]){
        player.x += player.speed;
    }

    player.x = Math.max(0,Math.min(750,player.x));

    for(let i=meteors.length-1;i>=0;i--){

        meteors[i].y += meteors[i].speed;

        if(
            meteors[i].x < player.x + player.width &&
            meteors[i].x + meteors[i].size > player.x &&
            meteors[i].y < player.y + player.height &&
            meteors[i].y + meteors[i].size > player.y
        ){
            alert("게임 오버! 점수: " + score);
            location.reload();
        }

        if(meteors[i].y > 600){
            meteors.splice(i,1);
            score++;
        }
    }
}

function draw(){

    ctx.clearRect(0,0,800,600);

    ctx.fillStyle="cyan";
    ctx.fillRect(
        player.x,
        player.y,
        player.width,
        player.height
    );

    meteors.forEach(m=>{
        ctx.beginPath();
        ctx.arc(
            m.x+m.size/2,
            m.y+m.size/2,
            m.size/2,
            0,
            Math.PI*2
        );
        ctx.fillStyle="orange";
        ctx.fill();
    });

    ctx.fillStyle="white";
    ctx.font="24px Arial";
    ctx.fillText("점수: " + score,10,30);
}

function loop(){
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
""", height=620)
