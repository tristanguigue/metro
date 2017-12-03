var SECONDS_TO_YEARS = 1 / (3600 * 24 * 365.25);
var MIN_COLOR = '#00ad00';
var NEUTRAL_COLOR = '#D3D3D3'
var MAX_COLOR = '#d30026';
var NA_COLOR = '#fcfcfc'
var MILLIONTH = 1 / 10**6

function formatPassengers(number) {
  return (MILLIONTH * number).toFixed(2)
}

function formatStationName(name) {
  return name.split('(')[0];
}

function formatYears(time) {
  return (SECONDS_TO_YEARS * time).toFixed(2);
}

function scaleTransform(number, scale) { 
  return number / (1 + 0.25 * (d3.event.transform.k - 1))
}

var container = d3.select('#map');
var parentWidth = container.node().getBoundingClientRect().width - 6;
var parentHeight = container.node().getBoundingClientRect().height - 6;

var margin = {
  left: parentWidth / 20,
  right: parentWidth / 20,
  bottom: 0,
  top: 0
};

var width = parentWidth - margin.left - margin.right;
var height = parentHeight - margin.top - margin.bottom;

var svg = container.append('svg')
   .attr('width', parentWidth)
   .attr('height', parentHeight);

var tipSegment = d3.tip()
  .attr('class', 'd3-tip segment-tip')
  .offset([-10, 0])
  .html(function(d) {
    var stationA = stations.features.find(function(station){
      return station.properties.pk == d.stationA;
    });
    var stationB = stations.features.find(function(station){
      return station.properties.pk == d.stationB;
    });
    return '<span>' + formatStationName(stationA.properties.name) + ' <small>' + gettext('to') + '</small> ' 
      + formatStationName(stationB.properties.name) + '<br><span class="number">' 
      + formatPassengers(d.traffic) + '</span> <small>' + gettext('millions') + ' ('
      + gettext('passengers/year') + ')</small>';
  });

var tipStation = d3.tip()
  .attr('class', 'd3-tip station-tip')
  .offset([-10, 0])
  .html(function(d) {
    var html =  formatStationName(d.properties.name) + '<br><span class="number">' +
      formatPassengers(d.properties.yearly_entries) + '</span> <small>' + gettext('millions') + ' ('
      + gettext('entries/year') + ')</small>';    
    
    if(d.properties.remove) {
      var positive = d.properties.remove.time_difference > 0;

      html += '<br><span>' + gettext('Time') + ' ' + (positive ? gettext('gained'): gettext('lost')) + ' '
        + gettext('if removed') + ': </span>'
        + '<span class="number ' + (positive ? 'positive': 'negative') + '">'
        + Math.abs(formatYears(d.properties.remove.time_difference)) + "</span>"
        + ' <small>' + gettext('years') + '</small>';
    }
    return html;
  });

svg.call(tipSegment);
svg.call(tipStation);

var g = svg.append('g')
   .attr('width', width)
   .attr('height', height)
   .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

var stations, edges, arrondissements;

function initializeMap() {
  if(!stations || !edges || !arrondissements){
    return
  }

  edges.forEach(function(edge){
    var reverseEdge = edges.find(function(e){
      return e.stationA === edge.stationB && e.stationB === edge.stationA && e.line === edge.line;
    });
    var reverseEdgeIndex = edges.findIndex(function(e){
      return e.stationA === edge.stationB && e.stationB === edge.stationA && e.line === edge.line;
    });
    if(reverseEdge) {
      edge.traffic += reverseEdge.traffic;
      edges.splice(reverseEdgeIndex, 1);
    }
  })

  var maxTraffic = d3.max(edges, function(edge) {
    return edge.traffic;
  });
  var maxEntries = d3.max(stations.features, function(d) {
    return d.properties.yearly_entries;
  });
  var maxTimeDiff = SECONDS_TO_YEARS * d3.max(stations.features, function(d) {
    return d.properties.remove ? d.properties.remove.time_difference : 0;
  });
  var minTimeDiff = SECONDS_TO_YEARS * d3.min(stations.features, function(d) {
    return d.properties.remove ? d.properties.remove.time_difference : 0;
  });

  // res = stations.features.sort(function(x, y){
  //   xdiff = x.properties.remove ? x.properties.remove.time_difference: 0
  //   ydiff = y.properties.remove ? y.properties.remove.time_difference: 0
  //   return d3.ascending(xdiff, ydiff);
  // })

  // res.slice(0, 10).forEach(function(s){ 
  //   console.log(s.properties.name,
  //     s.properties.remove ? formatYears(s.properties.remove.time_difference): 0,
  //     s.properties.remove ? s.properties.remove.time_difference_per_person: 0)
  // })

  // console.log(stations.features)
  
  var colorScale = d3.scaleLinear()
    .domain([minTimeDiff, 0, maxTimeDiff])
    .range([MIN_COLOR, NEUTRAL_COLOR, MAX_COLOR]);
  var segmentSizeScale = d3.scaleLinear().domain([0, maxTraffic]).range([1, 12]);
  var radiusScale = d3.scaleLinear().domain([0, maxTimeDiff]).range([1, 12]);
  var center = d3.geoCentroid(stations);

  var projection = d3.geoMercator()
  .fitExtent([[2, 2], [width - 2, height - 2]], stations)

  var projPath = d3.geoPath()
    .projection(projection);

  var arrElements =  g.selectAll('path')
      .data(arrondissements)
    .enter().append('path')
      .attr('d', projPath)
      .style('fill', '#f1f1f1')
      .style('stroke', 'black')
      .style('stroke-width', '0.1px')

  var edgeElements = g.selectAll('.edge')
      .data(edges)
    .enter().append('line', '.edge')
      .each(function(d) {
        var el = d3.select(this);
        var stationA = stations.features.find(function(station){
          return station.properties.pk == d.stationA;
        });
        var stationB = stations.features.find(function(station){
          return station.properties.pk == d.stationB;
        });
        el.attr('x1', projection(stationA.geometry.coordinates)[0])
        el.attr('x2', projection(stationB.geometry.coordinates)[0])
        el.attr('y1', projection(stationA.geometry.coordinates)[1])
        el.attr('y2', projection(stationB.geometry.coordinates)[1])
      })
      .style('stroke', function(d) {
        return d.color;
      })
      .style('stroke-width', function(d) {
        return segmentSizeScale(d.traffic);
      })
      .on('mouseover', tipSegment.show)
      .on('mouseout', tipSegment.hide)

  var stationElements = g.selectAll('.station')
      .data(stations.features)
    .enter().append('circle', '.station')
      .attr('r', function(d){
        var diff = d.properties.remove? SECONDS_TO_YEARS * Math.abs(d.properties.remove.time_difference): 0
        return radiusScale(diff);
      })
      .style('fill', function(d){
        return d.properties.remove ? colorScale(SECONDS_TO_YEARS * d.properties.remove.time_difference): NA_COLOR;
      })
      .style('stroke', 'black')
      .style('stroke-width', '0.1px')
      .attr('transform', function(d) {
          return 'translate(' + projection(d.geometry.coordinates) + ')'
      })
      .on('mouseover', tipStation.show)
      .on('mouseout', tipStation.hide);

  var zoom = d3.zoom()
      .scaleExtent([1, 5])
      .translateExtent([[0, 0], [width, height]])
      .extent([[0, 0], [width, height]])
      .on('zoom', zoomed);
  svg.call(zoom);

  function zoomed() {
    g.attr("transform", [
      "translate(" + [margin.left + d3.event.transform.x, margin.top + d3.event.transform.y] + ")",
      "scale(" + d3.event.transform.k + ")"
    ].join(" "));

    edgeElements.style('stroke-width', function(d) {
        return scaleTransform(segmentSizeScale(d.traffic), d3.event.transform.k);
    });
    stationElements.attr('r', function(d){
        var diff = d.properties.remove? SECONDS_TO_YEARS * Math.abs(d.properties.remove.time_difference): 0
        return scaleTransform(radiusScale(diff), d3.event.transform.k);
      })
  }

  $(".zoom_in").click(function() {
      zoom.scaleBy(g, 2);
  });
  $(".zoom_out").click(function() {
      zoom.scaleBy(g, 0.5);
  });


  // LEGEND
  svg.append("g")
    .attr("class", "legend legendTime")
    .attr("transform", "translate(10, 25)");

  var legend = d3.legendColor()
      .cells([minTimeDiff, minTimeDiff / 3, 0, maxTimeDiff / 3, maxTimeDiff])
      .labels([gettext('Large Loss'), gettext('Small Loss'), gettext('Neutral'), gettext('Small gain'), gettext('Large Gain')])
      .title(gettext('Time difference if station removed'))
      .scale(colorScale);

  svg.select(".legendTime")
    .call(legend);

  svg.append("g")
    .attr("class", "legend legendSize")
    .attr("transform", "translate(10, 160)");

}

d3.json('/static/data/stations.json', function(data) {
  stations = data
  initializeMap();
})

d3.json('/static/data/edges.json', function(data) {
    edges = data
  initializeMap();
})

d3.json('/static/data/arrondissements.geojson', function(data) {
  arrondissements = data.features
  initializeMap();
})


