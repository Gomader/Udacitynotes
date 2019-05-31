const categoryMap = {
  '国内':"gn",
  '国际':"gj", 
  '财经':"cj", 
  '娱乐':"yl", 
  '军事':"js", 
  '体育':"ty", 
  '其他':"other"
}

Page({
  data:{
    categoryList: "",
    nowcategory:'国内',
    firstnewsifo:[],   
    nextnewsifo:[],
    hidden: true
  },
  onLoad(){
    this.setCategory()
    this.getNewsList()
  },
  onPullDownRefresh() {
    this.getNewsList(() => {
      wx.stopPullDownRefresh()
    })
  },
  setCategory(){
    this.setData({
      categoryList: ['国内', '国际', '财经', '娱乐', '军事', '体育', '其他']
    })
  },
  changeCategory(a){
    var cate = a.currentTarget.dataset.id
    this.setData({
      nowcategory: cate
    })
    this.getNewsList()
  },
  getNewsList(callback){
    wx.request({
      url: 'https://test-miniprogram.com/api/news/list',
      data:{
        type: categoryMap[this.data.nowcategory]
      },
      success: res =>{
        let result = res.data.result
        this.getfirstnewsifo(result)
        this.getnextnewsifo(result)
      },
      fail: err => {
        this.setData({
          hidden: false
        })
      },
      complete: () => {
        callback && callback()
      }
    })
  },
  regetnews(){
    this.getNewsList()
  },
  onPullDownRefresh(result) {
    this.getNewsList(() => {
      wx.stopPullDownRefresh()
    })
  },
  getfirstnewsifo(result){
    let firstnewsifo = []
    let pc = result[0].firstImage === 'undefined' ? '/images/failpicture.jpg' : result[0].firstImage
    firstnewsifo.push({
    picture: pc,
    title: result[0].title,
    publisher: result[0].source,
    time: this.daytyple(result[0].date),
    id: result[0].id
    })
    this.setData({
      firstnewsifo:firstnewsifo
    })
  },
  getnextnewsifo(result){
    let nextnewsifo = []
    for (let i = 1; i < result.length; i += 1){
      let pc = result[i].firstImage === 'undefined' ? '/images/failpicture.jpg' : result[i].firstImage
      let pub = result[i].source === "" ? '网络来源' : result[i].source
      nextnewsifo.push({
      nextspicture: pc,
      nextstitle: result[i].title,
      nextspublisher: pub,
      nexttime: this.daytyple(result[i].date),
      nextid: result[i].id
      })
    }
    this.setData({
      nextnewsifo:nextnewsifo
    })
  },
  daytyple(t){
    var d= new Date(t)
    var h= d.getHours()
    var m= d.getMinutes()
    if (h < 10) {
      h= "0" + h;
    }
    if (m < 10) {
      m= "0" + m;
    }
    return (h + ":" + m)
  },
  tonewsifo(a){
    var name = a.currentTarget.dataset.id
    wx.navigateTo({
      url: '/pages/information/information?id=' + name
    })
  },
  errorFunction(){
    
  }
})
