# 需要补充的

- 这个问题也遇到了，但是没看懂这个地方是说的什么。<span style="color:red;">看来还是要好好掌握 keras</span>


# CTC Loss InvalidArgumentError: sequence_length(b) <= time



I am running into this error while trying to use tf.nn.ctc_loss through keras (ctc_batch_cost):

> InvalidArgumentError (see above for traceback): sequence_length(4) <= 471

According to the documentation for tf.nn.ctc_loss, Input requirements are:

> sequence_length(b) <= time for all b
>
> max(labels.indices(labels.indices[:, 1] == b, 2)) <= sequence_length(b) for all b.

I am having a hard time understanding what this means-- what is `b` and what is `sequence_length(b)`?


回答：

In this case `b` is each example in a minibatch. `sequence_length(b)` is the number of time stamps you have for that example. This is specified in the `sequence_length` argument passed to `tf.nn.ctc_loss` which is a 1-d tensor of sequence lengths.


# 相关资料

- [CTC Loss InvalidArgumentError: sequence_length(b) <= time](https://stackoverflow.com/questions/43422949/ctc-loss-invalidargumenterror-sequence-lengthb-time)
- [ctc loss error - sequence_length(0) <= 3](https://stackoverflow.com/questions/48889769/ctc-loss-error-sequence-length0-3)
