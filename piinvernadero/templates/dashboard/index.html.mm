{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Dashboard{% endblock %}</h1>
        <script src="{{ url_for('static', filename='jquery-1.8.3.min.js') }}"></script>
		<script type="text/javascript">
  {% for lugar in lugares %}
		$(function () {
		    $.getJSON('{{ url_for('dashboard.datajson', id=lugar['id'], sensor=3) }}', function (data) {
		        // Crea el grafico con el id del lugar
		        $('#{{lugar['name']}}').highcharts('StockChart', {
		            rangeSelector : {
		                selected : 2
		            },
		            title : {
		                text : '{{lugar['name']}}'
		            },
		            series : [{
		                name : '{{sensor}}',
		                data : [[1554487190000.0, 21.9], [1554487180000.0, 22.9], [1554487170000.0, 23.9], [1554487160000.0, 25.9], [1554487150000.0, 24.9], [1554487140000.0, 23.9]],
		                tooltip: {
		                    valueDecimals: 2
		                }
                             },{
                                name : '{{sensor}}',
                                data : [[1554487190000.0, 48.0], [1554487180000.0, 50.0], [1554487170000.0, 65.0], [1554487160000.0, 70.0], [1554487150000.0, 60.0], [1554487140000.0, 50.0]],
                                tooltip: {
                                    valueDecimals: 2
                                }

                               
		            }]
		        });
		    });
		});
  {% endfor %}

		</script>

{% endblock %}

{% block content %}

<script src="{{ url_for('static', filename='highstock.js') }}"></script>
<script src="{{ url_for('static', filename='highcharts-more.js') }}"></script>
<script src="{{ url_for('static', filename='exporting.js') }}"></script>
  {% for lugar in lugares %}
    <div id="{{lugar['name']}}" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
  {% endfor %}



{% endblock %}
