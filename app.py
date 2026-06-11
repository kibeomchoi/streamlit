import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="운석 피하기", layout="centered")

st.title("☄️ 운석 피하기")
st.write("A = 왼쪽 이동 | D = 오른쪽 이동")

components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
body{
    margin:0;
    background:black;
    overflow:hidden;
}

canvas{
    display:block;
    margin:auto;
    background:linear-gradient(to bottom,#000428,#004e92);
    border:2px solid white;
}
</style>
</head>

<body>

<canvas id="game" width="800" height="600"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let player = {
    x:375,
    y:530,
    width:50,
    height:50,
    speed:8
};

let meteors = [];
let score = 0;
let gameOver = false;

const keys = {};

window.focus();

window.addEventListener("keydown", function(e){
    if(e.key === "a" || e.key === "A"){
        keys["left"] = true;
    }

    if(e.key === "d" || e.key === "D"){
        keys["right"] = true;
    }
});

window.addEventListener("keyup", function(e){
    if(e.key === "a" || e.key === "A"){
        keys["left"] = false;
    }

    if(e.key === "d" || e.key === "D"){
        keys["right"] = false;
    }
});

function createMeteor(){

    meteors.push({
        x:Math.random()*760,
        y:-40,
        size:20 + Math.random()*40,
        speed:3 + Math.random()*4
    });
}

setInterval(function(){

    if(!gameOver){
        createMeteor();
    }

},500);

function update(){

    if(gameOver){
        return;
    }

    if(keys["left"]){
        player.x -= player.speed;
    }

    if(keys["right"]){
        player.x += player.speed;
    }

    player.x = Math.max(
        0,
        Math.min(
            canvas.width-player.width,
            player.x
        )
    );

    for(let i=meteors.length-1;i>=0;i--){

        let m = meteors[i];

        m.y += m.speed;

        if(
            m.x < player.x + player.width &&
            m.x + m.size > player.x &&
            m.y < player.y + player.height &&
            m.y + m.size > player.y
        ){

            gameOver = true;

            setTimeout(function(){

                alert(
                    "게임 오버!\\n점수 : "
                    + score
                );

                location.reload();

            },100);

            return;
        }

        if(m.y > canvas.height){

            meteors.splice(i,1);
            score++;
        }
    }
}

function draw(){

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    ctx.fillStyle = "cyan";

    ctx.fillRect(
        player.x,
        player.y,
        player.width,
        player.height
    );

    meteors.forEach(function(m){

        ctx.beginPath();

        ctx.arc(
            m.x + m.size/2,
            m.y + m.size/2,
            m.size/2,
            0,
            Math.PI*2
        );

        ctx.fillStyle = "orange";
        ctx.fill();
    });

    ctx.fillStyle = "white";
    ctx.font = "24px Arial";

    ctx.fillText(
        "점수 : " + score,
        10,
        30
    );

    if(gameOver){

        ctx.fillStyle = "red";
        ctx.font = "48px Arial";

        ctx.fillText(
            "GAME OVER",
            260,
            250
        );
    }
}

function gameLoop(){

    update();
    draw();

    requestAnimationFrame(
        gameLoop
    );
}

gameLoop();

</script>

</body>
</html>
""", height=620)
