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
      labels: [
        '人手',
        '人脸'
      ],
      currentDrawing: {
        labelId: null,
        labelName: null
      }
    }
  },
  methods: {
    bbox_object (labelIdx, color) {

      this.currentDrawing.labelId = labelIdx
      this.currentDrawing.labelName = this.labels[labelIdx]

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

      bbox.on('drawstop', ((component) => {
        return function (e) {
          console.log('Draw done,', 'Label', labelIdx, 'Color', color)
          let parent = e.currentTarget.parentElement
          let parentSVG = window.SVG(parent)
          let rectBBox = e.currentTarget.getBBox()
          let parentBBox = e.currentTarget.parentElement.getBBox()
          let title = parentSVG.text(component.labels[labelIdx])

          title.font({
            family: '宋体',
            size: 21
          })
            .attr({stroke: color})
            .move(rectBBox.x, rectBBox.y)

//          component._addLabelBBox(labelIdx, e.currentTarget, title.node)
          component.$bus.$emit('labelChanged', labelIdx, e.currentTarget, title.node)

          component.currentDrawing.labelId = null
          component.currentDrawing.labelName = null
//          window.alert(`${labelIdx} ${(rectBBox.x / parentBBox.width).toFixed(16)} ${(rectBBox.y / parentBBox.height).toFixed(16)} ${(rectBBox.width / parentBBox.width).toFixed(16)} ${(rectBBox.height / parentBBox.height).toFixed(16)}`)
        }
      })(this)
      )

      bbox.draw()
    }
  },
  mounted () {
    let draw = window.SVG('drawing')

    this.drawing = draw

    let img = draw.image('http://a.hiphotos.baidu.com/image/pic/item/503d269759ee3d6d453aab8b48166d224e4adef5.jpg')

    img.loaded(function (loader) {
      this.size(loader.width, loader.height)
      this.parent().size(loader.width, loader.height)
    })


    this.$bus.$on('startDrawBBox', ((component) => {
      return function (idx, color) {
        console.log('Event startDrawBBox')
        component.bbox_object(idx, color);

      }
    })(this))
    // 传给左边栏数据

  }
}
</script>
