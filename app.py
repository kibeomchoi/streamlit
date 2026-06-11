<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>운석 피하기 게임</title>

<style>
body{
    margin:0;
    overflow:hidden;
    background:black;
    font-family:Arial,sans-serif;
}

canvas{
    display:block;
    margin:auto;
    background:linear-gradient(to bottom,#000428,#004e92);
}

#score{
    position:absolute;
    top:10px;
    left:10px;
    color:white;
    font-size:24px;
    font-weight:bold;
}

#gameOver{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    color:white;
    text-align:center;
    display:none;
}

button{
    padding:10px 20px;
    font-size:18px;
    cursor:pointer;
}
</style>
</head>

<body>

<div id="score">점수: 0</div>

<div id="gameOver">
    <h1>게임 오버</h1>
    <p id="finalScore"></p>
    <button onclick="restart()">다시하기</button>
</div>

<canvas id="game"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

canvas.width = 800;
canvas.height = 600;

let player = {
    x: canvas.width/2 - 25,
    y: canvas.height - 70,
    width:50,
    height:50,
    speed:7
};

let meteors = [];
let score = 0;
let gameRunning = true;

const keys = {};

document.addEventListener("keydown", e=>{
    keys[e.key]=true;
});

document.addEventListener("keyup", e=>{
    keys[e.key]=false;
});

function createMeteor(){
    meteors.push({
        x: Math.random()*(canvas.width-30),
        y:-30,
        size:20+Math.random()*30,
        speed:3+Math.random()*5
    });
}

setInterval(()=>{
    if(gameRunning){
        createMeteor();
    }
},500);

function update(){

    if(keys["ArrowLeft"]){
        player.x -= player.speed;
    }

    if(keys["ArrowRight"]){
        player.x += player.speed;
    }

    player.x = Math.max(0,Math.min(canvas.width-player.width,player.x));

    for(let i=meteors.length-1;i>=0;i--){

        meteors[i].y += meteors[i].speed;

        if(
            meteors[i].x < player.x + player.width &&
            meteors[i].x + meteors[i].size > player.x &&
            meteors[i].y < player.y + player.height &&
            meteors[i].y + meteors[i].size > player.y
        ){
            endGame();
        }

        if(meteors[i].y > canvas.height){
            meteors.splice(i,1);
            score++;
            document.getElementById("score").innerText =
            "점수: " + score;
        }
    }
}

function draw(){

    ctx.clearRect(0,0,canvas.width,canvas.height);

    for(let i=0;i<100;i++){
        ctx.fillStyle="white";
        ctx.fillRect(
            (i*83)%canvas.width,
            (i*57)%canvas.height,
            2,2
        );
    }

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
}

function gameLoop(){

    if(gameRunning){
        update();
    }

    draw();
    requestAnimationFrame(gameLoop);
}

function endGame(){
    gameRunning=false;

    document.getElementById("gameOver").style.display="block";
    document.getElementById("finalScore").innerText =
    "최종 점수: " + score;
}

function restart(){

    player.x = canvas.width/2 - 25;
    meteors = [];
    score = 0;

    document.getElementById("score").innerText =
    "점수: 0";

    document.getElementById("gameOver").style.display =
    "none";

    gameRunning = true;
}

gameLoop();
</script>

</body>
</html>
