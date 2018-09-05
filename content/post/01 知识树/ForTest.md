---
title: ForTest
toc: true
date: 2018-09-06
---
<script src="https://cdn.jsdelivr.net/npm/echarts@4.0.4/dist/echarts.common.min.js" integrity="sha256-CRtw4pUXzFosdt4rnjf2ZPyVHH48Rsd5ddXe6jZ6iPM=" crossorigin="anonymous"></script>
<div id="benchmark-chart" style="width: 100%;height: 400px;margin: auto;"></div>
<script>
var benchmarkChart = echarts.init(document.getElementById('benchmark-chart'));
var serial = {
  type: 'bar'
};
var option = {
  legend: {selected: {}},
  tooltip: {},
  dataset: {
    dimensions: ['ops', 'identity', 'identity+batch', 'sequence', 'sequence+optimizer', 'sequence+batch', 'sequence+optimizer+batch', 'table', 'table+optimizer', 'table+batch', 'table+optimizer+batch'],
    source: [
      {ops: '1 thread', 'identity': 280, 'identity+batch': 105, 'sequence': 354, 'sequence+optimizer': 294, 'sequence+batch': 104, 'sequence+optimizer+batch': 44, 'table': 650, 'table+optimizer': 295, 'table+batch': 361, 'table+optimizer+batch': 49},
      {ops: '2 threads', 'identity': 369, 'identity+batch': 143, 'sequence': 476, 'sequence+optimizer': 403, 'sequence+batch': 164, 'sequence+optimizer+batch': 71, 'table': 833, 'table+optimizer': 408, 'table+batch': 576, 'table+optimizer+batch': 85},
      {ops: '4 threads', 'identity': 548, 'identity+batch': 218, 'sequence': 670, 'sequence+optimizer': 537, 'sequence+batch': 204, 'sequence+optimizer+batch': 95, 'table': 1454, 'table+optimizer': 547, 'table+batch': 1101, 'table+optimizer+batch': 101},
      {ops: '8 threads', 'identity': 607, 'identity+batch': 274, 'sequence': 767, 'sequence+optimizer': 633, 'sequence+batch': 252, 'sequence+optimizer+batch': 123, 'table': 4260, 'table+optimizer': 643, 'table+batch': 2409, 'table+optimizer+batch': 138},
      {ops: '16 threads', 'identity': 805, 'identity+batch': 404, 'sequence': 1084, 'sequence+optimizer': 858, 'sequence+batch': 417, 'sequence+optimizer+batch': 193, 'table': 6573, 'table+optimizer': 936, 'table+batch': 5097, 'table+optimizer+batch': 257}
    ]
  },
  xAxis: {type: 'category'},
  yAxis: {},
  series: [
    serial,
    serial,
    serial,
    serial,
    serial,
    serial,
    serial,
    serial,
    serial,
    serial
  ]
};
option.dataset.dimensions.filter(function(value) {
  return value !== 'ops' && value !== 'identity' && value !== 'sequence' && value !== 'table';
}).forEach(function(item) {
  option.legend.selected[item] = false;
});
benchmarkChart.setOption(option);
</script>

<!--more-->

- provider : springboot 2.0 (hibernate 5.2.14)
- insert 100 users per thread : `save(1)` &times; 100
- batch : `saveAll(10)` &times; 10
- optimizer : default(50)
- source code : [olOwOlo/generation-type-benchmark](https://github.com/olOwOlo/generation-type-benchmark)

## APPENDIX

### 16 threads

Benchmark                                       | Mode | Cnt | Score |   Error | Units
----------------------------------------------- | ---- | --- | ----- | ------- | -----
GenerationTypeBenchmark.identity                |   ss |  30 | 0.805 | ± 0.013 |  s/op
GenerationTypeBenchmark.identityBatch           |   ss |  30 | 0.404 | ± 0.097 |  s/op
GenerationTypeBenchmark.sequence                |   ss |  30 | 1.084 | ± 0.011 |  s/op
GenerationTypeBenchmark.sequenceOptimizer       |   ss |  30 | 0.858 | ± 0.011 |  s/op
GenerationTypeBenchmark.sequenceBatch           |   ss |  30 | 0.417 | ± 0.093 |  s/op
GenerationTypeBenchmark.sequenceOptimizerBatch  |   ss |  30 | 0.193 | ± 0.064 |  s/op
GenerationTypeBenchmark.table                   |   ss |   5 | 6.573 | ± 1.118 |  s/op
GenerationTypeBenchmark.tableOptimizer          |   ss |  30 | 0.936 | ± 0.016 |  s/op
GenerationTypeBenchmark.tableBatch              |   ss |   5 | 5.097 | ± 0.230 |  s/op
GenerationTypeBenchmark.tableOptimizerBatch     |   ss |  30 | 0.257 | ± 0.048 |  s/op





<iframe id="embed_dom" name="embed_dom" frameborder="0" style="display:block;width:525px; height:245px;" src="https://www.processon.com/embed/mind/5ad211b6e4b0518eacaf908f"></iframe>
