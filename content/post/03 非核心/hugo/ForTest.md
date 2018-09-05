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

```
{{% alertNote %}}
MyBatis Generator 1.3.6 及以上
{{% /alertNote %}}

{{% alertNote %}}
1.3.6 在动态 SQL 模式下存在数个已修复的 BUG，由于 1.3.7 尚未发布，建议使用快照版本。
{{% /alertNote %}}

{{% admonition note "Note" %}}

本文基于 elide-spring-boot-starter 1.4.0 & Spring Boot 2，请注意有一些功能并不是 Elide 所直接提供的，关于该 starter 的更多信息于 [Github 主页](https://github.com/illyasviel/elide-spring-boot)查看。

{{% /admonition %}}


OK，现在来试试吧。

{{% admonition warning "Warning" %}}
请注意你的 JPA 及下文所述的注解最好放在 get 方法上，Elide 目前没有完全支持位于 field 上的注解。
{{% /admonition %}}
标识**实体**是否可删除


{{% admonition tip "Tip" %}}
在开启 Spring 的依赖注入后（由 starter 提供，默认开启），你可以在实体类中使用 `@Autowired`，`@Inject` 等注解注入 Bean 以供触发器函数使用...个人建议你关掉它，用下面提到的 Function Hooks。
{{% /admonition %}}



标识**实体**是否可删除

{{% admonition question "Question" %}}
JSON API 支持只删除关联而不删除实体，那么该注解是否于关系字段仍然有效？可以自行尝试一下~
{{% /admonition %}}
```

<iframe id="embed_dom" name="embed_dom" frameborder="0" style="display:block;width:400px; height:400px;" src="https://www.processon.com/embed/mind/5ad211b6e4b0518eacaf908f"></iframe>
