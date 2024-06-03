import json

def generate_html(usage_rates):
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokemon Usage Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <div id="chart"></div>
    <script>
        const data = {data};

        const width = 800;
        const height = 400;
        const svg = d3.select("#chart").append("svg")
                      .attr("width", width)
                      .attr("height", height);

        const x = d3.scaleBand()
                    .domain(data.map(d => d.species))
                    .range([0, width])
                    .padding(0.1);

        const y = d3.scaleLinear()
                    .domain([0, d3.max(data, d => d.usage)])
                    .nice()
                    .range([height, 0]);

        svg.append("g")
           .selectAll("rect")
           .data(data)
           .enter()
           .append("rect")
           .attr("x", d => x(d.species))
           .attr("y", d => y(d.usage))
           .attr("width", x.bandwidth())
           .attr("height", d => height - y(d.usage))
           .attr("fill", "steelblue");

        svg.append("g")
           .attr("transform", `translate(0,${height})`)
           .call(d3.axisBottom(x));

        svg.append("g")
           .call(d3.axisLeft(y));
    </script>
</body>
</html>"""
    
    data = [{"species": species, "usage": usage} for species, usage in usage_rates.items()]
    html_content = template.replace("{data}", json.dumps(data))
    with open("index.html", "w") as f:
        f.write(html_content)

generate_html(usage_rates)
