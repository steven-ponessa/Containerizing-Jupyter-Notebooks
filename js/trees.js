// First undefine 'circles' so we can easily reload this file.
require.undef('trees');

define('trees', ['d3'], function (d3) {

    function build_tree_graph(container, jsonFileName, width, height) {       

        //var x = document.getElementById(containerTag);
        //x.innerHTML = "";

        console.log("in trees.js build_tree_graph")
        console.log(jsonFileName.jsonFile)

        var margin = { top: 20, right: 120, bottom: 20, left: 120 },
            canvas_height = height || 700,
            canvas_width = width || 960
        var tree_width = canvas_width - margin.right - margin.left,
            tree_height = canvas_height - margin.top - margin.bottom,
            tree_level_depth = 180;

        var i = 0,
            duration = 750,
            root;

        var tree = d3.layout.tree()
        //var tree = d3.tree()
            .size([tree_height, tree_width]);

        var diagonal = d3.svg.diagonal()
            .projection(function (d) { return [d.y, d.x]; });

        var svg = d3.select(container).append("svg")
            .attr("width", canvas_width)
            .attr("height", canvas_height)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        //d3.json("input_graph_tree.json", function (error, tree_data) {
        d3.json(jsonFileName.jsonFile, function (error, tree_data) {
            root = tree_data;
            root.x0 = tree_height / 2;
            root.y0 = 0;

            function collapse(d) {
                if (d.children) {
                    d._children = d.children;
                    d._children.forEach(collapse);
                    d.children = null;
                }
            }

            root.children.forEach(collapse);
            update(root);
        });

        //var treeGraph = document.getElementById(containerTag)
        //d3.select(treeGraph.frameElement).style("height", "800px");

        function update(source) {

            // Compute the new tree layout.
            var nodes = tree.nodes(root),
                links = tree.links(nodes);

            // Normalize for fixed-depth.
            nodes.forEach(function (d) { d.y = d.depth * tree_level_depth; });

            // Set unique ID for each node
            var node = svg.selectAll("g.node")
                .data(nodes, function (d) { return d.id || (d.id = ++i); });

            // Enter any new nodes at the parent's previous position.
            var new_nodes = node.enter().append("g")
                .attr("class", "node")
                .attr("transform", function (d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
                .on("click", click);

            new_nodes.append("circle")
                .attr("r", 1e-6)
                //.style("fill", function (d) { return d._children || d._children.length>0 ? "lightsteelblue" : "#fff"; });
                .style("fill", function (d) { return d._children  ? "lightsteelblue" : "#fff"; });

            new_nodes.append("text")
                .attr("x", function (d) { return d.children || d._children ? -10 : 10; })
                .attr("dy", ".35em")
                .attr("text-anchor", function (d) { return d.children || d._children ? "end" : "start"; })
                .text(function (d) { return d.name; })
                .style("fill-opacity", 1e-6);

            // Transition nodes to their new position.
            var moved_node = node.transition().duration(duration)
                .attr("transform", function (d) { return "translate(" + d.y + "," + d.x + ")"; });
            moved_node.select("circle")
                .attr("r", 4.5)
                .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; });
            moved_node.select("text")
                .style("fill-opacity", 1);

            // Transition exiting nodes to the parent's new position.
            var hidden_nodes = node.exit().transition().duration(duration)
                .attr("transform", function (d) { return "translate(" + source.y + "," + source.x + ")"; })
                .remove();
            hidden_nodes.select("circle")
                .attr("r", 1e-6);
            hidden_nodes.select("text")
                .style("fill-opacity", 1e-6);

            // Update the links…
            var link = svg.selectAll("path.link")
                .data(links, function (d) { return d.target.id; });

            // Enter any new links at the parent's previous position.
            link.enter().insert("path", "g")
                .attr("class", "link")
                .attr("d", function (d) {
                    var o = { x: source.x0, y: source.y0 };
                    return diagonal({ source: o, target: o });
                })
                .append("svg:title")
                .text(function (d, i) { return d.target.edge_name; });

            //Transition links to their new position.
            link.transition().duration(duration)
                .attr("d", diagonal);

            // Transition exiting nodes to the parent's new position.
            link.exit().transition().duration(duration)
                .attr("d", function (d) {
                    var o = { x: source.x, y: source.y };
                    return diagonal({ source: o, target: o });
                })
                .remove();

            // Stash the old positions for transition.
            nodes.forEach(function (d) {
                d.x0 = d.x;
                d.y0 = d.y;
            });
        }

        // Toggle children on click.
        function click(d) {
            if (d.children) {
                d._children = d.children;
                d.children = null;
            } else {
                d.children = d._children;
                d._children = null;
            }
            update(d);
        }

    }

    return build_tree_graph;
});

element.append('<small>&#127795; &#127876; Loaded trees.js &#127794; &#127796; </small>');