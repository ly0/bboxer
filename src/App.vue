<template>
  <v-app id="inspire" dark>
    <v-navigation-drawer
      clipped
      fixed
      v-model="drawer"
      app
    >
      <v-list dense>
        <!--<v-list-tile @click="dummyClick()">-->
          <!--<v-list-tile-action>-->
            <!--<v-icon>dashboard</v-icon>-->
          <!--</v-list-tile-action>-->
          <!--<v-list-tile-content>-->
            <!--<v-list-tile-title>概览</v-list-tile-title>-->
          <!--</v-list-tile-content>-->
        <!--</v-list-tile>-->
        <!--<v-list-tile @click="dummyClick()">-->
          <!--<v-list-tile-action>-->
            <!--<v-icon>settings</v-icon>-->
          <!--</v-list-tile-action>-->
          <!--<v-list-tile-content>-->
            <!--<v-list-tile-title>来一段BBox</v-list-tile-title>-->
          <!--</v-list-tile-content>-->
        <!--</v-list-tile>-->
        <v-label-status />
      </v-list>

    </v-navigation-drawer>
    <v-toolbar app fixed clipped-left>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>BBox Fucker</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
          <router-view/>
        </v-layout>
      </v-container>
    </v-content>
    <v-footer app fixed>
      <span>Canaan-Creative &copy; 2018 Some motherfucker BBox Editor by latyas</span>
    </v-footer>
  </v-app>

</template>

<script>
import LabelStatus from '@/components/LabelStatus'
export default {
  name: 'App',
  components: {
    'v-label-status': LabelStatus
  },
  methods: {
    dummyClick () {
      console.log('clicked')
    }
  },
  data: () => ({
    drawer: null
  }),
  props: {
    source: String
  }
}
</script>

<style>

  .input-group__details {
    min-height: 2px;
  }

  body {
    background: #212121;
  }
</style>
