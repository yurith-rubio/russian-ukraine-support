<script>
    import { onMount } from 'svelte';
    import spendings from '../lib/spendings.json';

    let total_spendings_russia = 0;
    let total_spendings_ukraine = 0;
    
    onMount (() => {
        total_spendings_russia = spendings.reduce((sum, current) => sum + current.russia, 0);
        total_spendings_ukraine = spendings.reduce((sum, current) => sum + current.ukraine, 0);

        // set the dimensions and margins of the graph
        if (Viewport.Width < 500) {
            var margin = {top: 10, right: 30, bottom: 20, left: 30};
            var width = 300;
            var height = 300;
        } else {
            var margin = {top: 10, right: 30, bottom: 20, left: 50};
            var width = 460 - margin.left - margin.right;
            var height = 460 - margin.top - margin.bottom;
        }
        
        // append the svg object to the body of the page
        var svg = d3.select("#spendings_viz")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        
        // List of subgroups = header of the csv files = soil condition here, in the example there are three subgroups: nitrogen, normal, stress
        var subgroups = ['russia', 'ukraine']

        // List of groups = species here = value of the first column called group -> I show them on the X axis - banana, poacee, sorgho, triticum
        var groups = d3.map(spendings, function(d){
            return(d.year)
        }).keys()

        // Add X axis
        var x = d3.scaleBand()
            .domain(groups)
            .range([0, width])
            .padding([0.05])
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickSize(0));

        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, 130])
            .range([ height, 0 ]);
        svg.append("g")
            .call(d3.axisLeft(y));

        // Another scale for subgroup position?
        var xSubgroup = d3.scaleBand()
            .domain(subgroups)
            .range([0, x.bandwidth()])
            .padding([0.3])

        // color palette = one color per subgroup
        var color = d3.scaleOrdinal()
            .domain(subgroups)
            .range(['var(--red)','var(--dark-blue)'])

        // Show the bars
        svg
            .append("g")
            .selectAll(".bar-group")
            // Enter in data = loop group per group
            .data(spendings)
            .enter()
            .append("g")
            .classed("bar-group", true)
            .attr("transform", function(d) {
                return "translate(" + x(d.year) + ",0)";
            })
            .selectAll("rect")
            .data(function(d) { return subgroups.map(function(key) {
                return {key: key, value: d[key]}; 
            }); })
            .enter()
            .append("rect")
            .classed("bar", true)
            .attr("x", function(d) { return xSubgroup(d.key); })
            .attr("y", function(d) { return y(d.value); })
            .attr("width", xSubgroup.bandwidth())
            .attr("height", function(d) { return height - y(d.value); })
            .attr("fill", function(d) { return color(d.key); })
            .on("mouseover", function(d) {
                d3.selectAll("rect").style("opacity", "0.5");
                d3.selectAll("text.label").style("opacity", "0.5");
                d3.selectAll(`text[fill='${color(d.key)}']`).style("opacity", "1");
                d3.selectAll(`rect[fill='${color(d.key)}']`).style("opacity", "1");
                this.style.cursor = "pointer";
            })
            .on("mouseleave", function(d) {
                d3.selectAll("rect").style("opacity", "1");
                d3.selectAll("text.label").style("opacity", "1");
            })

        svg
            .selectAll(".russian-label.label")
            .data(spendings)
            .enter()
            .append("text")
            .classed("russian-label label", true)
            .attr("x", function(d) {
                return x(d.year) + xSubgroup.bandwidth();
            })
            .attr("y", function(d) {
                return y(d.russia) - 25; 
            })
            .text(function(d) { 
                return '$' + d.russia;
            })
            .attr("text-anchor", "middle")
            .style("font-weight", "bold")
            .attr("fill", "var(--red)")

        svg
            .selectAll(".russian-gdp.label")
            .data(spendings)
            .enter()
            .append("text")
            .classed("russian-gdp label", true)
            .attr("x", function(d) {
                return x(d.year) + xSubgroup.bandwidth();
            })
            .attr("y", function(d) {
                return y(d.russia) - 5; 
            })
            .text(function(d) { return d.gdp_russia })
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .attr("fill", "var(--red)")


        svg
            .selectAll(".ukraine-label.label")
            .data(spendings)
            .enter()
            .append("text")
            .classed("ukraine-label label", true)
            .attr("x", function(d) {
                return x(d.year) + xSubgroup.bandwidth() + xSubgroup.bandwidth() * 1.4;
            })
            .attr("y", function(d) {
                return y(d.ukraine) - 25; 
            })
            .text(function(d) { 
                return '$' + d.ukraine; 
            })
            .attr("text-anchor", "middle")
            .style("font-weight", "bold")
            .attr("fill", "var(--dark-blue)")
        
        svg
            .selectAll(".ukraine-gdp.label")
            .data(spendings)
            .enter()
            .append("text")
            .classed("ukraine-gdp label", true)
            .attr("x", function(d) {
                return x(d.year) + xSubgroup.bandwidth() + xSubgroup.bandwidth() * 1.5;
            })
            .attr("y", function(d) {
                return y(d.ukraine) - 5; 
            })
            .text(function(d) { 
                return d.gdp_ukraine; 
            })
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .attr("fill", "var(--dark-blue)")
        
    });

</script>

<div class="svgWrapper" style="position: relative">
    <div>Total expenses: 
        <p>Russia: {total_spendings_russia}</p>
        <p>Ukraine: {total_spendings_ukraine} </p>
    </div>
    <svg id="spendings_viz"></svg>
</div>

<p class="article__body-text padding-sides">Russian and Ukrainian Military Spending</p>
<p class="article__body-text padding-sides">
Russian budget figures are somewhat obscured and difficult to clarify. Multiple sources cite different figures for Russia’s “defence” budget. The official number has been removed from Russian government websites. Recent estimates though put the 2024 number to be upwards of $110 billion, nearly double the pre-invasion 2021 figure. It’s now around 30% of Russia’s government budget, and close to 7% of its total GDP. (Most countries spend less than 2% of GDP on their military).
</p>
<p class="article__body-text padding-sides">
Ukraine’s military spending has, of course, sky-rocketed since the invasion. From 3% of GDP in 2021 to a staggering 20% in 2024. Knock-on effects and reducing funding for other parts of the economy has led to substantial dependency on overseas aid from friendly nations…
</p>
<p class="article__body-text padding-sides">
See our data.
</p>

<style>
    @media screen and (max-width: 500px){
        .svgWrapper{
            flex-direction: column;
        }
    }

</style>