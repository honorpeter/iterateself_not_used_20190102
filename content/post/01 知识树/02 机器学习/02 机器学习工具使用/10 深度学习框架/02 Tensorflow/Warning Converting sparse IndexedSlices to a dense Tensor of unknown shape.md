---
title: Warning Converting sparse IndexedSlices to a dense Tensor of unknown shape
toc: true
date: 2018-11-10
---
# Tensorflow dense gradient explanation?



I recently implemented a model and when I ran it I received this warning:

```
UserWarning: Converting sparse IndexedSlices to a dense Tensor of unknown shape.
This may consume a large amount of memory.
"Converting sparse IndexedSlices to a dense Tensor of unknown shape. "
```

With some similar parameter settings (embedding dimensionalities) suddenly the model is ridiculously slow.

1. What does this warning imply? It appears that something I've done has caused all of the gradients to be dense and so backprop is doing dense matrix computations
2. If it's that there is an issue with the model that's causing this, how can I identify it and fix it?





This warning is printed when a sparse [`tf.IndexedSlices`](https://www.tensorflow.org/api_docs/python/tf/IndexedSlices) object is implicitly converted to a dense [`tf.Tensor`](https://www.tensorflow.org/api_docs/python/tf/Tensor). This typically happens when one op (usually [`tf.gather()`](https://www.tensorflow.org/api_docs/python/tf/gather)) backpropagates a sparse gradient, but the op that receives it does not have a specialized gradient function that can handle sparse gradients. As a result, TensorFlow automatically densifies the `tf.IndexedSlices`, which can have a devastating effect on performance if the tensor is large.

To fix this problem, you should try to ensure that the `params` input to `tf.gather()` (or the `params`inputs to [`tf.nn.embedding_lookup()`](https://www.tensorflow.org/versions/r0.7/api_docs/python/nn.html#embedding_lookup)) is a [`tf.Variable`](https://www.tensorflow.org/api_docs/python/tf/Variable). Variables can receive the sparse updates directly, so no conversion is needed. Although `tf.gather()` (and `tf.nn.embedding_lookup()`) accept arbitrary tensors as inputs, this may lead to a more complicated backpropagation graph, resulting in implicit conversion.




# 相关资料

- [Tensorflow dense gradient explanation?](https://stackoverflow.com/questions/35892412/tensorflow-dense-gradient-explanation)
