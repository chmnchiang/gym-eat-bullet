const loc = window.location;
const ws = new WebSocket(`ws://${loc.host}/ws`);
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const SCALE = 4;

function draw(arr) {
    const height = arr.length;
    const width = arr[0].length;
    console.log(arr);
    ctx.width = canvas.width = width * SCALE;
    ctx.height = canvas.height = height * SCALE;

    const imgData = ctx.createImageData(width, height);
    const pixelData = imgData.data;
    pixelData.length = height * width * 4;
    for (let i = 0; i < height; i++) {
        for (let j = 0; j < width; j++) {
            const base = i*width + j;
            pixelData[base*4 + 0] = arr[i][j][0];
            pixelData[base*4 + 1] = arr[i][j][1];
            pixelData[base*4 + 2] = arr[i][j][2];
            pixelData[base*4 + 3] = 255;
        }
    }

    ctx.putImageData(imgData, 0, 0);
    ctx.drawImage(canvas, 0, 0, width, height, 0, 0, width*SCALE, height*SCALE);
}

ws.onmessage = e => draw(JSON.parse(e.data));
