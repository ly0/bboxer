<template>
  <div class="hello">
    <v-alert color="info" icon="info" value="true" transition="fade-transition" v-if="currentDrawing.labelId !== null">
      目前正在画 LabelId: {{ currentDrawing.labelId }}, LabelName: {{ currentDrawing.labelName }}
    </v-alert>

    <div class="canvasContainer">
      <!--<div class="previous" v-if="this.Store.imageLoaded">-->
      <!--<a>-->
      <!--<v-icon x-large>fa-chevron-circle-left</v-icon></a>-->
      <!--</div>-->

      <div id="drawing"></div>
      <!--<div class="next" v-if="this.Store.imageLoaded">-->
        <!--<a>-->
          <!--<v-icon x-large>fa-chevron-circle-right</v-icon>-->
        <!--</a>-->
      <!--</div>-->
    </div>

    <div v-if="!this.Store.imageLoaded && !this.Store.allDone">
      <v-progress-circular indeterminate v-bind:size="100" v-bind:width="7" color="grey"></v-progress-circular>
      <!--<div class="headline grey&#45;&#45;text" style="text-align: center">-->
      <!--LOADING-->
      <!--</div>-->
    </div>

    <div v-if="this.Store.allDone">
      <div class="headline grey--text" style="text-align: center">
        打标完成，请开始炼丹。
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.canvasContainer {
  display: flex;

  .previous {
    flex: 1;
    margin:auto;
    padding-right: 24px;

    i:hover {
      color: #424242;
    }

  }

  .drawing {
    flex: 1;
  }

  .next {
    flex: 1;
    margin:auto;
    padding-left: 24px;

    i:hover {
      color: #424242;
    }
  }

}
</style>
<script>
import 'svg.js/dist/svg.js'
import 'svg.draw.js/dist/svg.draw.js'
import Store from '@/store.js'

function Exception (message) {
  this.message = message
}
export default {
  name: 'HelloWorld',
  data () {
    return {
      Store: Store,
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
          component.currentDrawing.drawingObj = null
        }
      })(this)
      )

      bbox.draw()
    },
    loadImageData (url) {
      let img = this.drawing.image(url)

      img.loaded(((component) => {
        return function (loader) {
          this.size(loader.width, loader.height)
          this.parent().size(loader.width, loader.height)

          component.Store.imageLoaded = true
        }
      })(this)
      )
    }
  },

  beforeDestroy () {
    // 离开时注销绑定
    window.removeEventListener('keyup', this.canvasKeyEventsHandler)
  },
  mounted () {
    let draw = window.SVG('drawing')
    this.drawing = draw

    this.$bus.$on('startDrawBBox', ((component) => {
      return function (idx, tag, color) {
        if (component.currentDrawing.drawingObj !== null) {
          return
        }
        console.log('Event startDrawBBox')
        component.bbox_object(idx, tag, color)
      }
    })(this))
    // 传给左边栏数据

    this.$bus.$on('imageLoadRequest', ((component) => {
      return function (url) {
        component.objectCount = 0
        component.imageLoaded = false
        component.loadImageData(url)
      }
    })(this))

    window.addEventListener('keyup', this.canvasKeyEventsHandler)
  }
}
</script>
