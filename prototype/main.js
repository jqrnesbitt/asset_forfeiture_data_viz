/* global d3, scrollama */

const width = 900,
    height = 600,
    margin = ({ top: 5, right: 5, bottom: 5, left: 5 }),
    side = 30;


//const circles = d3.select("svg")
//    .selectAll("circle")
//    .data(data)
//    .join("circle")
//    .attr("cx", width / 2)
//    .attr("cy", height / 2)
//    .attr("r", 10)
//    .style("fill", "steelblue")

const students = [
  {
    name: "Kate Chumbarova",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U024542SQ0L-3f65e1636643-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Brody Cormier",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U0111E7052T-b61b13c41cbd-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Maddie DiLullo",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01FXKY6SJF-41074f2ddaf1-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Alexandra Drossos",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01U1KNDMB2-4af3ea053529-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Julia Hossu",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01SV0YUY58-579f04d5ad9b-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Tony Hwang",
    img: "https://ca.slack-edge.com/T0WA5NWKG-UR7K0KEK0-303ea04a04ec-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Reece Koe",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01EZCWT7ML-ee74465887ca-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Lynn Marciano",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01GBHR4XPD-c8ff0970a988-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Jacquie Nesbitt",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01C8DP5Y5S-caae25859412-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Andi Peterson",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U0178TC524T-6c615a468415-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Prachi Varma",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01GGA67DD4-0d840997f59c-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Lucy Wu",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01DXFKHMLH-d3ee6c76fdbc-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Kevin Xuan",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01ELQL9RQR-0af537e3d5b4-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Shirley Zhong",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01EFF2TZV3-7675aae6a8ec-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  },
  {
    name: "Jude Zhu",
    img: "https://ca.slack-edge.com/T0WA5NWKG-U01HMRNAN1M-67ee1c9af4e1-512",
    var1: Math.random() * (width - margin.left - margin.right),
    var2: Math.random() * (height - margin.top - margin.bottom)
  }
]

const images = d3.select("svg")
  .append("g")
  .selectAll('image')
  .data(students)
  .join('image')
  .attr('href', d => d.img)
  .attr("x", d => width / 2 - 15)
  .attr('y', d => height / 2 - 15)
  .attr('width', side)
  .attr('height', side)
  .attr('preserveAspectRatio', "xMidYMin slice");

function moveLeft() {
    images
        .transition()
        .duration(750)
        .attr("x", 20)
}

function moveX() {
    images
        .transition()
        .duration(750)
        .attr("x", (d) => Math.random() * (width - margin.left - margin.right - side / 2))
}

function moveY() {
    images
    .transition()
    .duration(750)
    .attr("y", (d) => Math.random() * (height - margin.top - margin.bottom - side / 2))
}

//window.addEventListener("scroll", function (e) {
//    console.log(window.scrollY)
//})

const callbacks = [
    moveLeft,
    moveX,
    moveY,
    moveLeft,
    moveX,
    moveY,
    moveLeft,
    moveX,
    moveY,
    moveLeft,
    moveX
]

const steps = d3.selectAll(".step")

// instantiate the scrollama
const scroller = scrollama();

// setup the instance, pass callback functions
scroller
    .setup({
        step: ".step",
    })
    .onStepEnter((response) => {
        // { element, index, direction }
        callbacks[response.index]()

        steps.style("opacity", 0.1)
        d3.select(response.element).style("opacity", 1.0)

        console.log("enter", response)
    })
    .onStepExit((response) => {
        // { element, index, direction }
        console.log("exit", response)
    });

// setup resize event
window.addEventListener("resize", scroller.resize);