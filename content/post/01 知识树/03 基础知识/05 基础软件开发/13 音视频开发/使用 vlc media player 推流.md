---
title: 使用 vlc media player 推流
toc: true
date: 2018-12-08
---
# 使用 vlc media player 推流


这个是我最近使用的。

本来是从网络摄像头获得视频源进行处理的，但是为了调试方便，因为要对应不同的画面想要检测下识别的结果。

因此录制了网络摄像头的视频，然后，把视频用 VLC media player 进行推流。这样可以很方便的调整视频进度，切换到不同的画面下。


在接收 推流的时候遇到一个问题，

使用 VLC media player 推送的 rtsp 流是基于 udp 的，但是 opencv 调用 ffmpeg 接收 rtsp 流的时候，是强制使用 tcp 协议的。

因此，总是报出 method setup failed 461 client error 的错误。

嗯尝试了直接使用 ffmpeg 接收流：

```
ffmpeg -rtsp_transport tcp -i rtsp://localhost:8554/hello
ffmpeg -rtsp_transport udp -i rtsp://localhost:8554/hello
```

使用 udp 的接收是可以的，但是使用 tcp 的接收报出 461 error 。因此的确是这个问题。

后来 改为 推 http 格式的流就可以了。





# 相关资料

- [461 error](https://github.com/opencv/opencv/issues/8478)
- [opencv rtsp stream protocol](https://stackoverflow.com/questions/43047017/opencv-rtsp-stream-protocol)
- [Displaying RTSP-Stream using Xuggler: org.ffmpeg - h264 @ 15AC7660 error while decoding MB 34 60, bytestream (td)](https://stackoverflow.com/questions/36498689/displaying-rtsp-stream-using-xuggler-org-ffmpeg-h264-15ac7660-error-while)
- [opencv 接收 rtsp 流时强制使用 tcp](https://github.com/opencv/opencv/blob/3.1.0/modules/videoio/src/cap_ffmpeg_impl.hpp#L581)
