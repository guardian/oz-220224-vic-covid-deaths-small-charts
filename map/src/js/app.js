import * as d3 from "d3"
import * as topojson from "topojson"
import { numberFormat } from './numberFormat.js';

var maps = [{
	"label" : "NSW",
	"centre" : [147,-33],
	"zoom" : 3.9,
	"active" : false
},{
	"label" : "Sydney",
	"centre" : [151,-33.75],
	"zoom" : 25,
	"active" : true
}]


var circlesOn = false

var selector_init = 'closest_pos'


function cleanNames(name) {
	name = name.replace(" (C)", "")
	name = name.replace(" (C)", "")
	name = name.replace(" (NSW)", "")
	return name
}

function init(dataFeed, lga, places, variable) {

	// console.log("printer", places.features)
	var dataKeys = Object.keys(dataFeed[0])

	console.log("dataFeed",dataFeed)

	console.log(dataKeys)


	// dataKeys = dataKeys.filter((d) => d != "LGA_NAME20")

	// var dropdown = d3.select("#dropdown")

	var selected = variable

	// dropdown.selectAll("option")
	// .data(dataKeys)
	// .enter()
	// .append("option")
	// .attr("value", function(d){ return d})
	// .text(function(d){return d})



	var context = d3.select(".nswMap")
	const container = d3.select("#dblogsnswgreenspacesmall")
	var isMobile;
	var windowWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
	var windowHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
	if (windowWidth < 610) {
			isMobile = true;
			maps[1].zoom = 50
	}	

	if (windowWidth >= 610){
			isMobile = false;
	}

	var width = document.querySelector("#dblogsnswgreenspacesmall").getBoundingClientRect().width
	
	var height = width*0.7
	
	if (windowHeight > windowWidth) {
		height = width*0.9
	}


	var ratio = (maps[0].active) ? maps[0].zoom : maps[1].zoom

	var centre = (maps[0].active) ? maps[0].centre : maps[1].centre

	var projection = d3.geoMercator()
                    .center(centre)
                    .scale(width*ratio)
                    .translate([width/2,height/2])

	container.select("#nswMap").remove()
	container.select(".tooltip").remove()

	var extent = d3.extent(dataFeed, d => +d.count)

	var max = d3.max(dataFeed, d => d.count)

	extent = [1,max]

	var mapData = d3.map(dataFeed, function(d) { return d.place; });

	var lockdownAreas = ["Fairfield (C)", 
						"Liverpool (C)", 
						"Canterbury-Bankstown (A)", 
						"Blacktown (C)",
						"Cumberland (A)",
						"Parramatta (C)",
						"Georges River (A)",
						"Campbelltown (C) (NSW)",
						"Bayside (A)",
						"Burwood (A)",
						"Strathfield (A)",
						"Penrith (C)"]



	var varData = {}

	dataFeed.forEach((d) => varData[d['ssc_name_2016']] = +d['closest_pos'])
	
	// dataFeed.map((d) => d[selected])

	var varDataRange = dataFeed.map((d) => +d['closest_pos'])

	console.log("vardata", varData)
	console.log("datarange",varDataRange)


	// var divColors = d3.scaleThreshold()
	var divColors = d3.scaleQuantile()
	// var divColors = d3.scaleQuantize()
		// .nice()
		.range(['#888C73', '#909966','#99A659','#A1B24D','#AABF40', '#B2CC33', '#BBD926', '#C3E619', '#CCF20D', '#D4FF00'].reverse())
		// .domain([-6,-4,-2,0,2,4,6])
		.domain(varDataRange)
		// .domain(d3.extent(varDataRange))

	// console.log("testo", divColors.quantiles())

	var svg = container.append("svg")	
	                .attr("width", width)
					.attr("height", height)
	                .attr("id", "nswMap")
	                .attr("overflow", "hidden")
	                .on("mousemove", tooltipMove)

	var tooltip = d3.select("#dblogsnswgreenspacesmall").append("div")
            .attr("class", "tooltip")
            .attr("id", "tooltip")
            .style("position", "absolute")
            .style("z-index", "20")
            .style("visibility", "hidden")
            .style("top", "30px")
            .style("left", "55px");                
              
	var defs = svg.append("defs")                

	defs
		.append("pattern")
		 .attr('id', 'diagonalHatch')
	    .attr('patternUnits', 'userSpaceOnUse')
	    .attr('width', 8)
	    .attr('height', 8)
	    .attr("patternTransform", "rotate(60)")
	  .append('rect')
	    .attr("width",1)
	    .attr("height",8)
	    .attr("transform", "translate(0,0)")
	    .attr("fill", "#767676")



	var features = svg.append("g")



	var path = d3.geoPath()
	    .projection(projection);

	// var burbs = topojson.feature(places,places.objects['nsw']).features  
	var burbs = topojson.feature(places,places.objects['nsw_suburbs_dissolved']).features

	// console.log("places", places)
	// console.log("burbs", burbs)

	var geo = topojson.feature(lga,lga.objects['nsw-lga-2019']).features   

	var lockdownLgas = geo.filter(d => lockdownAreas.includes(d.properties.LGA_NAME19))

	// console.log("lockdownLgas", lockdownLgas)



	features.append("g")
	    .selectAll("path")
	    .attr("id","lgas")
	    .data(burbs)
	    .enter()
		.append("path")
	        .attr("class", "lga")
	        // .attr("fill","#eaeaea")
			.attr("fill", (d) => { if (varData[d.properties['SSC_NAME16']]){
		        		return divColors(varData[d.properties['SSC_NAME16']])}
						else {
							// console.log(d.properties['SSC_NAME16'])
							return "#eaeaea"}
		        		
		        	})
	        .attr("stroke", "#bcbcbc")
	        .attr("data-tooltip","")
	        .attr("d", path)
	        .on("mouseover", tooltipIn)
            .on("mouseout", tooltipOut)
	          
// console.log(varData)	          

	features.append("g")
	    .selectAll("path")
	    .attr("id","metro-lockdown")
	    .data(lockdownLgas)
	    .enter().append("path")
	        .attr("fill", "url(#diagonalHatch)")
	        .attr("stroke", "#ff9f19")
	        .style("pointer-events", "none")
	        // .style("stroke-dasharray", ("3, 2"))
	        .attr("stroke-width", "1px")
	        .attr("d", path);           
        
		//  features.selectAll("text")
        //     .data(filterPlaces)
        //     .enter()
        //     .append("text")
        //     .text((d) => d.properties.name)
        //     .attr("x", (d) => projection([d.properties.longitude, d.properties.latitude])[0] + 20)
        //     .attr("y", (d) => projection([d.properties.longitude, d.properties.latitude])[1])
        //     .attr("text-anchor", "start")
        //     .attr("class","label")        




   	context.select("#keyDiv svg").remove();

   	var keyWidth = document.querySelector("#keyDiv").getBoundingClientRect().width
	keyWidth -= 50
   	// console.log(keyWidth)

    var keySvg = context.select("#keyDiv").append("svg")	
	                .attr("width", keyWidth)
					.attr("height", 50)
	                .attr("id", "key")
	                .attr("overflow", "hidden");

	var keySquare = keyWidth / 10;
    var barHeight = 15
    var textHeight = 30            	

    // console.log(divColors.domain())

	divColors.range().forEach(function(d, i) {

        keySvg.append("rect")
            .attr("x", keySquare * i)
            .attr("y", 20)
            .attr("width", keySquare)
            .attr("height", barHeight)
            .attr("fill", d)
            .attr("stroke", "#dcdcdc")
    })
            
    divColors.quantiles().forEach(function(d, i) {
		console.log(i)
		console.log(d)

            keySvg.append("text")
	            .attr("x", (i + 1) * keySquare)
	            // .attr("x", i * keySquare)
	            .attr("text-anchor", "middle")
	            .attr("y", textHeight + 20)
	            .attr("class", "keyLabel keyText")
	            .text(numberFormat(Math.round(+d)))
      
     
    })
// console.log("domain",divColors.domain())
    keySvg.append("text")
        .attr("x", keyWidth/2 + 5)
        .attr("text-anchor", "start")
        .attr("y", 16)
        .attr("class", "keyText keyLabel")
        .text("Further →")

    keySvg.append("text")
        .attr("x", keyWidth/2 - 5)
        .attr("text-anchor", "end")
        .attr("y", 16)
        .attr("class", "keyText keyLabel")
        .text("← Closer")    


    context.select("#keyDiv3 svg").remove();        

    var keyWidth3 = document.querySelector("#keyDiv3").getBoundingClientRect().width

    var keySvg3 = context.select("#keyDiv3").append("svg")	
	                .attr("width", keyWidth3)
					.attr("height", 80)
	                .attr("id", "key3")
	                .attr("overflow", "hidden");          

	keySvg3.append("rect")
		.attr("x",1)
		.attr("y",10)
		.attr("width", 30)
		.attr("height", 30)
		.attr("fill", "url(#diagonalHatch)")
		.attr("stroke", "#ff9f19")  	


	keySvg3.append("rect")
            .attr("x",1)
			.attr("y",10)
   			.attr("width", 30)
   			.attr("height", 30)
   			.attr("fill", "none")
	        .attr("stroke", "#ff9f19")
	        .attr("stroke-width", 2)
	        .attr('stroke-dasharray', '3,2')     

            
        
   	keySvg3.append("text")
            .attr("x",0)
			.attr("y",60)
            .attr("class", "keyText keyLabel")
            .text("LGAs of concern")    

    // context.select("#toggleCircles").on("click", function() {  
    
    // 	if (circlesOn) {
    // 		features.selectAll(".mapCircle").style("visibility", "hidden")
    // 		features.selectAll(".lga").attr("fill", d=> {
    // 			if (d.properties.change === "") {
	// 					return "#eaeaea"
	// 				}

	// 	        	else {
		        		
	// 	        		return divColors(d.properties.change)
	// 	        	}
    // 		})
    			
    // 		circlesOn = false
    // 	}

    // 	else {
    // 		features.selectAll(".mapCircle").style("visibility", "visible")
    // 		features.selectAll(".lga").attr("fill", "#eaeaea")
    // 		circlesOn = true

    // 	}

    // })


    function tooltipMove(d) {
            var leftOffset = 0
            var rightOffset = 0
            var mouseX = d3.mouse(this)[0]
            var mouseY = d3.mouse(this)[1]
            var half = width / 2;
            if (mouseX < half) {
                context.select("#tooltip").style("left", mouseX + "px");
                
            } else if (mouseX >= half) {
                context.select("#tooltip").style("left", (mouseX - 200) + "px");
                
            }

            if (mouseY < (height / 2)) {
                context.select("#tooltip").style("top", (mouseY + 30) + "px");
            } else if (mouseY >= (height / 2)) {
                context.select("#tooltip").style("top", (mouseY - 120) + "px");
            }
            
        }

    function tooltipIn(d) {

			var tipData = dataFeed.filter((m) => m['ssc_name_2016'] == d.properties.SSC_NAME16)[0]
			if (tipData){
				// console.log(tipData)

            // console.log(d.properties)
            var html
            if (d.properties.change != "") {
            	 html = `<b>${d.properties.SSC_NAME16}</b><br>
				 Average distance to public open space: ${numberFormat(Math.round(+tipData['closest_pos_grt_1.5ha']))} metres<br>
						`
            }
           
           	else {
           		 html = `<b>${d.properties.LGA_NAME19}</b><br>
            			Total in past 30 days: ${d.properties.cases}<br>
            			`
           	}

            context.select(".tooltip").html(html).style("visibility", "visible");


			}
			


        
        }

    function tooltipOut(d) {
        context.select(".tooltip").style("visibility", "hidden");
    }            


} // end init



Promise.all([
		d3.csv('<%= path %>/assets/syd_green.csv'),
		d3.json('<%= path %>/assets/nsw-lga-2019.json'),
		// d3.json('<%= path %>/assets/SSC_2016_AUST.json'),
		// d3.json('<%= path %>/assets/nsw.json')
		d3.json('<%= path %>/assets/nsw_suburbs_dissolved.json')
		// d3.json('<%= path %>/assets/nsw_geo.json')
		])
		.then((results) =>  {
			init(results[0], results[1], results[2], results[3], selector_init)

			// d3.select("#dropdown").on("change", function() {

			// 	selector_init = d3.select(this).property('value')

			// 	init(results[0], results[1], results[2], selector_init)

			// })


			var to=null
			var lastWidth = document.querySelector("#dblogsnswgreenspacesmall").getBoundingClientRect()
			window.addEventListener('resize', function() {
				var thisWidth = document.querySelector("#dblogsnswgreenspacesmall").getBoundingClientRect()
				if (lastWidth != thisWidth) {
					window.clearTimeout(to);
					to = window.setTimeout(function() {
						    init(results[0], results[1], results[2], results[3])
						}, 100)
				}
			
			})

});