<script>
    import { onMount } from "svelte";
    import supportRussia from "../lib/support.json";
    let svg_width;
    let svg_height;
    let groupHeight;
    let groupWidth;
    

  onMount(() => {
    // width = Viewport.Width;
    // The svg
    var svg = d3.select("#map_support_viz")
    
    svg_width = Viewport.Width;
    svg_height = svg_width / 2;
    
    // Map and projection
    // var projection = d3
    //   .geoMercator()
    //   .scale(100)
    //   .center([0, 20])

    if(Viewport.Width >= 1000){
      var projection = d3.geoNaturalEarth1()
    } else {
      var projection = d3.geoNaturalEarth1()
        .scale(svg_width / 2 / Math.PI)
        .translate([svg_width / 2.2, svg_height / 2])
    }

    // Data and color scale
    var data = d3.map();

    const supports = new Set();
  
    for (const [key, value] of Object.entries(supportRussia)) {
      supports.add(value);
    }

    var colorScale = d3
      .scaleOrdinal()
      .domain(supports)
      // light gray, pink, orage, light blue, green, dark blue
      .range(["#ccc", "#ff9999", "#f2f0e7", "#a1bacb", "var(--dark-blue)", "#d52b1e", "yellow", "white"]);

      // Load external data and boot
      d3.queue()
        .defer(
          d3.json,
          "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
        )
        .defer(
          d3.csv,
          "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world_population.csv",
          function (d) {
            data.set(d.code, +d.pop);
          }
        )
        .await(ready);

    d3.select("#tooltip")
      .style("opacity", 0)
      .text("none")
    function ready(error, topo) {
      // Draw the map
      svg
        .append("g")
        .classed("group", true)
        .selectAll("path.country")
        .data(topo.features)
        .enter()
        .append("path")
        .classed("country", true)
        // draw each country
        .attr("d", d3.geoPath().projection(projection))
        .classed("d-path", true)
        .style('display', function(d){
          if (d.properties.name === "Antarctica"){
            return "none";
          }
        })
        // set the color of each country
        .attr("fill", function (d) {
          const name = d.properties.name;
          return colorScale(supportRussia[name]);
        })
        .attr("stroke", function (d) {
          const name = d.properties.name;
          if (name === "Russia") {
            return "black";
          }
        })
        .on("mouseover", function (d) {
          const name = d.properties.name;
          const color = colorScale(supportRussia[name]);
          d3.selectAll("path").style("opacity", 0.5);
          d3.selectAll(`path[fill='${color}']`).style("opacity", 1);
          this.style.cursor = "pointer";
          d3.select("#tooltip")
          .style("opacity", 1)
          .text(name + ": " + supportRussia[name])
        })
        .on("mouseleave", function (d) {
          d3.selectAll("path").style("opacity", 1);
          d3.select("#tooltip")
          .style("opacity", 0)
        });

        
        
        if(Viewport.Width >= 1000){
          svg_width = 1000;
          svg_height = 450;
          svg
          .attr("viewBox", `0 0 ${svg_width} ${svg_height}`)
          .attr("width", svg_width)
          .attr("height", svg_height)

          d3.select(".group")
          .attr("transform", "translate(0, 0)")

        }
        if(Viewport.Width < 1000){
          // get the size of the rendered map and adjust widths and heights accordingly
          // svg_width = document.querySelector(".group").getBBox().width;
          // svg_height = document.querySelector(".group").getBBox().height;
          
          // groupWidth = Viewport.Width;
          
          svg
          .attr("viewBox", `0 0 ${svg_width} ${svg_height }`)
          .attr("width", svg_width)
          .attr("height", svg_height)

        }   
    }
  });
</script>


<div class="colors-wrapper padding-sides padding-sides">
  <div class="column1">
    <p class="support">Pro Russia</p>
    <p class="support">Russia Leaning</p>
  </div>
  <div class="column2">
    <p class="support">Condemns Russia</p>
    <p class="support">West Leaning</p>
  </div>
  <div class="column3">
    <p class="support">Neutral</p>
    <p class="support">No data</p>
  </div>
</div>

<div class="svgWrapper column" style="position: relative">
  <div id="tooltip"></div>
  <svg id="map_support_viz" preserveAspectRatio="xMinYMin meet" ></svg>
</div>

<p class="article__body-text padding-sides">By invading ukraine, Vladimir Putin has divided the world. The West and its allies have presented a rare unified front against the Russian president’s attack. NATO is enjoying a surge of support within its member countries (<a href="/graphic-detail/2022/03/23/putins-aggression-has-bolstered-support-for-nato" data-analytics="in_body:link_1:para_1">and wannabe joiners</a>). The EU has projected the role of a <a href="/europe/the-eus-unity-over-ukraine-has-given-it-surprising-heft/21808306" data-analytics="in_body:link_2:para_1">first-rate power</a>. And co-ordinated efforts, including sanctions and banking restrictions, have punished Russia’s economy, <a href="/finance-and-economics/2022/03/30/under-unprecedented-sanctions-how-is-the-russian-economy-faring" data-analytics="in_body:link_3:para_1">at least in the short term</a>. But from other countries Russia still enjoys some support. The <a href="https://www.eiu.com/n/russia-can-count-on-support-from-many-developing-countries/" data-analytics="in_body:link_4:para_1">Economist Intelligence Unit</a>, our sister company, has measured government actions globally since the war broke out, and countries’ historical ties with Russia, to divide the world into three broad categories: governments that are West-leaning, Russia-leaning and neutral amid <a href="/briefing/2022/04/02/what-next-for-russia" data-analytics="in_body:link_5:para_1">the conflict</a>.
</p>

<style>
  #map_support_viz {
    display: inline-block;
    position: relative;
    left: 0;
    margin-top:50px;
  }
  #tooltip {
    background-color: white;
    padding: 10px;
    border: 1px solid var(--light-gray);
    border-radius: 5px;
    opacity: 0;
    width: fit-content;
    position: relative;
    top:50px;
    z-index: 2;
    color: #07203f;
    font-weight: 700;
  }
  .colors-wrapper{
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 30px;
  }
  .support:before {
    content: "";
    width: 20px;
    height: 20px;
    margin-right: 10px;
    background-color: var(--light-gray);
    display: inline-block;
  }
  .column1 .support:nth-child(1):before {
    background-color: var(--red);
  }
  .column1 .support:nth-child(2):before {
    background-color: var(--pink);
  }
  .column2 .support:nth-child(1):before {
    background-color: var(--dark-blue);
  }
  .column2 .support:nth-child(2):before {
    background-color: var(--light-blue);
  }
  .column3 .support:nth-child(1):before {
    background-color: var(--light-gray);
  }
  .column3 .support:nth-child(2):before {
    background-color: var(--light-color);
  }
  .support {
    width: fit-content;
    padding-left: 10px;
    margin: 0;
  }
  @media screen and (max-width: 500px){
    .colors-wrapper{
      display: flex;
      justify-content: center;
      flex-direction: column;
      gap: 10px;
    }
    .column2, .column3{
      margin-top: -10px;
    }
  }
  @media screen and (min-width: 1000px){
    #tooltip {
      margin: 0 auto -50px;
    }
  }
</style>