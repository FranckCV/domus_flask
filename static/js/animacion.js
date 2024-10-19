const burst = new mojs.Burst({
    radius: { 0: 360 },
    count: 20,
    children: {
        shape: 'cross',
        stroke: 'teal',
        strokeWidth: { 6: 0 },
        angle: { 360: 0 },
        radius: { 30: 5 },
        duration: 3000
    }
});

const timeline = new mojs.Timeline({
    repeat: 3 
})
.add(burst)
.play();
