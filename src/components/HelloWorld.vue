<template>
  <div class="hello">
    <v-alert color="info" icon="info" value="true" transition="fade-transition" v-if="currentDrawing.labelId !== null">
      目前正在画 LabelId: {{ currentDrawing.labelId }}, LabelName: {{ currentDrawing.labelName }}
    </v-alert>
    <div id="drawing"></div>
</div>
</template>

<style lang="scss">

</style>
<script>
import 'svg.js/dist/svg.js'
import 'svg.draw.js/dist/svg.draw.js'

function Exception (message) {
  this.message = message
}
export default {
  name: 'HelloWorld',
  data () {
    return {
      drawing: null,
      objectCount: 0,
      currentDrawing: {
        labelId: null,
        labelName: null,
        drawingObj: null
      }
    }
  },
  methods: {
    canvasKeyEventsHandler (e) {
      if (e.keyCode === 27) {
        // ESC
        if (this.currentDrawing.drawingObj !== null) {
          // 可取消
          let drawingObj = this.currentDrawing.drawingObj
          this.currentDrawing.drawingObj = null
          drawingObj.draw('cancel')

        }
      }
      console.log(e)
    },
    bbox_object (labelIdx, labelName, color) {

      this.currentDrawing.labelId = labelIdx
      this.currentDrawing.labelName = labelName

      if (this.drawing === null) {
        throw new Exception('Unexpected error, drawing is not initiated.')
      }
      let bbox = this.drawing.rect().attr({
        'fill-opacity': 0,
        stroke: color,
        'stroke-width': 2
      }).fill({
        'opacity': 0
      })

      this.currentDrawing.drawingObj = bbox

      bbox.on('drawstop', ((component) => {
        return function (e) {
          if (component.currentDrawing.drawingObj === null) {
            component.currentDrawing.labelId = null
            component.currentDrawing.labelName = null
            return
          }
          console.log('Draw done,', 'Label', labelIdx, 'Color', color)
          let parent = e.currentTarget.parentElement
          let parentSVG = window.SVG(parent)
          let rectBBox = e.currentTarget.getBBox()
          let title = parentSVG.text(`${labelName}${component.objectCount}`)

          title.font({
            family: '宋体',
            size: 21
          })
            .attr({stroke: color})
            .move(rectBBox.x, rectBBox.y)

          component.objectCount += 1

          component.$bus.$emit('labelChanged', labelIdx, e.currentTarget, title.node)

          component.currentDrawing.labelId = null
          component.currentDrawing.labelName = null
          // window.alert(`${labelIdx} ${(rectBBox.x / parentBBox.width).toFixed(16)} ${(rectBBox.y / parentBBox.height).toFixed(16)} ${(rectBBox.width / parentBBox.width).toFixed(16)} ${(rectBBox.height / parentBBox.height).toFixed(16)}`)
        }
      })(this)
      )

      bbox.draw()
    },
    loadImageData () {},
  },
  mounted () {
    let draw = window.SVG('drawing')

    this.drawing = draw

    let img = draw.image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1516851157&di=ab26fe65d7b1816b60c2e14e712e8135&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.newmotor.com.cn%2FUploadFiles%2Fimage%2F20150521%2F20150521182212961296.jpg')

    img.loaded(function (loader) {
      this.size(loader.width, loader.height)
      this.parent().size(loader.width, loader.height)
    })


    this.$bus.$on('startDrawBBox', ((component) => {
      return function (idx, tag, color) {
        console.log('Event startDrawBBox')
        component.bbox_object(idx, tag, color);

      }
    })(this))
    // 传给左边栏数据


    window.addEventListener('keyup', this.canvasKeyEventsHandler)

  }
}
</script>
