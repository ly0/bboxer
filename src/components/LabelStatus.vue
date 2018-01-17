<template>
  <div id="labelStatus">
    <v-card color="grey darken-2" class="white--text">
      <v-card-title primary-title>
        <div class="headline">Label Status</div>
      </v-card-title>
      <v-card-text>
        <div v-for="(item, index) in metaData.labels">
          <v-switch :label="item" v-model="labeled" :value="index" @change="handleLabelCheckboxChange"></v-switch>
        </div>
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
</style>
<script>
export default {
  name: 'LabelStatus',
  computed: {
  },
  methods: {
    _addLabelBBox (labelIdx, bboxSVGObject, bboxTitleSVGObject) {
      if (labelIdx in this.BBoxData) {
        this.BBoxData[labelIdx].bbox.remove()
        this.BBoxData[labelIdx].title.remove()
      }
      this.BBoxData[labelIdx] = {
        bbox: bboxSVGObject,
        title: bboxTitleSVGObject
      }
    },
    handleLabelCheckboxChange (val) {
      // 等待删除
      let underDeleted = Object.keys(this.BBoxData).filter((e) => {
        return (val.indexOf(parseInt(e)) === -1)
      })
      // 等待增加
      let underAdded = val.filter((e) => {
        return !(e in this.BBoxData)
      })

      console.log('this.BBoxData', this.BBoxData, 'this.labeled', this.labeled, 'val', val, 'underDeleted', underDeleted, 'underAdded', underAdded)

      for (let idx of underDeleted) {
        console.log('Delete selected, label', idx)
        this._deleteLabelBBox(idx)
      }

      for (let idx of underAdded) {
        console.log('startDrawBBox', idx)
        this.$bus.$emit('startDrawBBox', idx, ['red', 'green', 'blue', 'cyan', 'yellow'][Math.floor(Math.random() * 5)])
      }
    },
    _deleteLabelBBox (labelIdx) {
      if (labelIdx in this.BBoxData) {
        this.BBoxData[labelIdx].bbox.remove()
        this.BBoxData[labelIdx].title.remove()
      }
      delete this.BBoxData[labelIdx]
    }
  },

  watch: {
  },
  data () {
    return {
      BBoxData: {},
      labeled: [],
      metaData: {
        labels: [
          '人手',
          '人脸'
        ]
      }
    }
  },
  created () {
    this.$bus.$on('metaDataLoaded', function (id) {
      // ...
    })

    this.$bus.$on('labelChanged', ((component) => {
        return (function (labelIdx, bboxSVGObject, bboxTitleSVGObject) {
          component._addLabelBBox(labelIdx, bboxSVGObject, bboxTitleSVGObject)
        })
      })(this)
    )
  }
}
</script>
