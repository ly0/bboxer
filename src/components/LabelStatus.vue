<template>
  <div id="labelStatus" v-if="Store.imageLoaded">
    <v-card color="blue-grey darken-2" class="white--text">
    <v-list>
      <v-card-title>
        <div class="title">已打标对象</div>
      </v-card-title>
      <div class="labeledObjectList">
        <v-list-tile avatar v-for="(item, index) in BBoxData" :key="index">
          <v-list-tile-content>
            <v-list-tile-title v-html="item.title.textContent"></v-list-tile-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-btn flat icon @click.native="deleteLabeledObject(index)">
              <v-icon color="white">fa-trash</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </div>
    </v-list>
    </v-card>
    <v-card color="grey darken-2" class="white--text">
      <v-card-title primary-title>
        <div class="title">标签列表</div>
      </v-card-title>
      <v-card-text>
        <v-chip close v-model="bboxtips" color="red" text-color="white">0-9键可以快速来一段BBox</v-chip>

        <div v-for="(item, index) in metaData.labels" :key="index">
          <v-btn
            color="info"
            :loading="drawing"
            @click.native="handleLabelCheckboxChange(index)"
          >
            {{ item }}
            <span slot="loader">Drawing...</span>
          </v-btn>

          <!--<v-switch :label="item" v-model="labeled" :value="index" @change="handleLabelCheckboxChange"></v-switch>-->
        </div>
      </v-card-text>
  <v-card-text>
        <v-btn
          color="success"
          @click.native="getBBoxResult()"
        >
          上传数据
        </v-btn>
    <span>
        剩余样本 {{ unlabeledLeft }}</span>
  </v-card-text>
    </v-card>
  </div>
</template>

<style>
  #labelStatus {
   position: absolute;
    bottom: 0px;
    width: 100%;
  }

  .labeledObjectList {
    overflow-y: scroll;
    max-height:300px;
  }

  .labeledObjectList::-webkit-scrollbar {
    width: 1em;
  }

  .labeledObjectList::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  }
  .labeledObjectList::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }

</style>
<script>
import VCardTitle from 'vuetify/es5/components/VCard/VCardTitle'
import Store from '@/store.js'

export default {
  components: {VCardTitle},
  name: 'LabelStatus',
  computed: {
  },
  methods: {
    _addLabelBBox (labelIdx, bboxSVGObject, bboxTitleSVGObject) {
      this.BBoxData.push({
        labelIdx: labelIdx,
        bbox: bboxSVGObject,
        title: bboxTitleSVGObject
      })
    },
    getBBoxResult () {
      let result = ''

      for (let item of this.BBoxData) {
        let parent = item.bbox.parentElement
        let parentBBox = parent.getBBox()
        let bbox = item.bbox.getBBox()

        result += `${item.labelIdx} ${(bbox.x / parentBBox.width).toFixed(16)} ${(bbox.y / parentBBox.height).toFixed(16)} ${(bbox.width / parentBBox.width).toFixed(16)} ${(bbox.height / parentBBox.height).toFixed(16)}\r\n`
      }

      // upload
      if (result === '') {
        let noDataConfirm = window.confirm('没有打任何Label，确定提交？')
        if (!noDataConfirm) {
          return
        }
      }
      this.http.post('/upload_label', {
        path: this.currentImageUrl,
        label_data: result
      }).then((resp) => {
        window.alert('上传成功')
        this.Store.imageLoaded = false
        for (let i of this.BBoxData) {
          i.bbox.remove()
          i.title.remove()
        }

        this.BBoxData = []
        this.unlabeledLeft -= 1
        this.getNextImage()
      })
    },
    handleLabelCheckboxChange (val) {
      this.$bus.$emit('startDrawBBox', val, this.metaData.labels[val], ['red', 'green', 'blue', 'cyan', 'yellow'][Math.floor(Math.random() * 5)])
    },
    deleteLabeledObject (idx) {
      this.BBoxData[idx].bbox.remove()
      this.BBoxData[idx].title.remove()
      this.BBoxData.splice(idx, 1)
    },
    _deleteLabelBBox (labelIdx) {
      if (labelIdx in this.BBoxData) {
        this.BBoxData[labelIdx].bbox.remove()
        this.BBoxData[labelIdx].title.remove()
      }
      delete this.BBoxData[labelIdx]
    },

    getNextImage () {
      this.http.get(
        '/next'
      ).then((resp) => {
        if (!resp.data) {
          this.Store.allDone = true
          return
        }
        this.currentImageUrl = resp.data
        this.$bus.$emit('imageLoadRequest', `/image/${resp.data}`)
      })
    },

    keyDownHandlers (e) {
      if (e.keyCode >= 48 && e.keyCode <= 57) {
        let labelIdx = e.keyCode - 48

        if (labelIdx < this.metaData.labels.length) {
          this.handleLabelCheckboxChange(labelIdx)
        }
      } else if (e.keyCode === 13) {
        // 回车按下，应该提交BBox
        this.getBBoxResult()
      }
    }
  },

  watch: {
  },
  data () {
    return {
      Store,
      currentImageUrl: '',
      BBoxData: [],
      unlabeledLeft: -1,
      labeled: [],
      metaData: {
        labels: [
        ]
      },
      drawing: false,
      bboxtips: true
    }
  },
  beforeDestroy () {
    window.removeEventListener('keydown', this.keyDownHandlers)
  },
  created () {
    this.$bus.$on('metaDataLoaded', function (id) {
      // ...
    })

    this.$bus.$on('labelChanged', ((component) => {
      return function (labelIdx, bboxSVGObject, bboxTitleSVGObject) {
        component._addLabelBBox(labelIdx, bboxSVGObject, bboxTitleSVGObject)
      }
    })(this)
    )

    window.addEventListener('keydown', this.keyDownHandlers)

    this.http.get(
      '/config'
    ).then((resp) => {
      this.unlabeledLeft = resp.data.image_left
      this.metaData.labels = resp.data.labels
      this.getNextImage()
    })
  }
}
</script>
