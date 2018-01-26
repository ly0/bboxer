# bboxer
打框框，输出label文件用的，目前输出的是darknet的数据格式，理论上可以输出任何格式

大概这种感觉？嘛，大概先是这样了。
![image](https://user-images.githubusercontent.com/1551736/35431097-26998a5e-02b6-11e8-819f-75339ec4d72e.png)


## TODOLIST

* [ ] Gallery
* [ ] Backend
* [ ] 多人协作
* [ ] ????

## Build Setup

``` bash
# install dependencies
npm install

# pack all motherfucker things
npm run pack

cd dist
python3 server --labels=LABEL_FILE DATASET_PATH
```
