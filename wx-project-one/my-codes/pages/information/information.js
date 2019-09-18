
Page({
  data:{
    title:'',
    time:'',
    publisher:'',
    readtimes: 1,
    texts:[],
  },
  onLoad: function(options){
    this.changePagecolor()
    this.getnewsifo(options)
  },
  getnewsifo(options){
    wx.request({
      url: 'https://test-miniprogram.com/api/news/detail',
      data: {
        id: options.id
      },
      success: res => {
        let result = res.data.result
        this.drawPage(result)
      }
    })
  },
  changePagecolor(){
    wx.setNavigationBarColor({
      frontColor: '#000000',
      backgroundColor: '#FFFFFF'
    })
  },
  drawPage(result){
    let title = result.title
    let time = this.daytyple(result.date)
    let publisher = result.source
    let readtimes = result.readCount
    let texts = []
    for (let i = 0; i < result.content.length-1 ; i += 1) {
      if(result.content[i].type === 'image'){
        texts.push({
          type: result.content[i].type,
          text: result.content[i].src,
        })
      }
      else{
        texts.push({
          type: result.content[i].type,
          text: result.content[i].text,
        })
      }
    }
    console.log(texts)
    this.setData({
      title:title,
      time:time,
      publisher:publisher,
      readtimes:readtimes,
      texts:texts,
    })
  },
  daytyple(t) {
    var d = new Date(t)
    var h = d.getHours()
    var m = d.getMinutes()
    if (h < 10) {
      h = "0" + h;
    }
    if (m < 10) {
      m = "0" + m;
    }
    return (h + ":" + m)
  },
})

