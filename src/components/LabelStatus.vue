<template>
  <div id="labelStatus">
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
        <div v-for="(item, index) in metaData.labels">

          <v-btn
            color="info"
            :loading="drawing"
            @click.native="handleLabelCheckboxChange(index)"
            :disabled="loading2"
          >
            {{ item }}
            <span slot="loader">Drawing...</span>
          </v-btn>

          <!--<v-switch :label="item" v-model="labeled" :value="index" @change="handleLabelCheckboxChange"></v-switch>-->
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
export default {
  components: {VCardTitle},
  name: 'LabelStatus',
  computed: {
  },
  methods: {
    _addLabelBBox (labelIdx, bboxSVGObject, bboxTitleSVGObject) {
//      if (labelIdx in this.BBoxData) {
//        this.BBoxData[labelIdx].bbox.remove()
//        this.BBoxData[labelIdx].title.remove()
//      }

      this.BBoxData.push({
        labelIdx: labelIdx,
        bbox: bboxSVGObject,
        title: bboxTitleSVGObject
      })
    },
    handleLabelCheckboxChange (val) {
//      // 等待删除
//      let underDeleted = Object.keys(this.BBoxData).filter((e) => {
//        return (val.indexOf(parseInt(e)) === -1)
//      })
//      // 等待增加
//      let underAdded = val.filter((e) => {
//        return !(e in this.BBoxData)
//      })

//      console.log('this.BBoxData', this.BBoxData, 'this.labeled', this.labeled, 'val', val, 'underDeleted', underDeleted, 'underAdded', underAdded)

//      for (let idx of underDeleted) {
//        console.log('Delete selected, label', idx)
//        this._deleteLabelBBox(idx)
//      }

      this.$bus.$emit('startDrawBBox', val, ['red', 'green', 'blue', 'cyan', 'yellow'][Math.floor(Math.random() * 5)])

//      for (let idx of underAdded) {
//        console.log('startDrawBBox', idx)
//      }
    },
    deleteLabeledObject (idx) {
      this.BBoxData[idx].bbox.remove()
      this.BBoxData[idx].title.remove()
      this.BBoxData.splice(idx, 1);
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
      BBoxData: [],
      labeled: [],
      metaData: {
        labels: [
          '人手',
          '人脸'
        ]
      },
      drawing: false
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
