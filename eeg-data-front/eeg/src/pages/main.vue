<template>
    <div style="position:relative; left:30px">
        <h3>EEG Data Tool</h3>
        <h5>Data Downloader</h5>
        <div style="max-width: 300px">
          <q-select v-model="dataType" :options="dataOptions" label="Select Data Type" />
          <q-select v-model="animal" :options="animalOptions" label="Select Animal" />
          <q-datetime-picker label="Select Start Date and Time" mode="datetime" default-standard="quasar" with-seconds=true v-model="startTime"></q-datetime-picker>
          <q-datetime-picker label="Select End Date and Time" mode="datetime" default-standard="quasar" with-seconds=true v-model="endTime"></q-datetime-picker>
          <q-btn color="primary" label="Get Data" @click="sendFileRequest"/>
          <q-btn color="deep-orange" label="Get Statistics" v-if="dataType === 'Temperature'" @click="getStatistics"/>
        </div>
        <div class="q-pa-md" style="max-width: 700px" v-if="dataType === 'Temperature'">
          <h5>Temperature Statistics</h5>
          <q-table
            title="Temperature Statistics"
            :data="statData"
            :columns="columns"
          />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      dataType: null,
      dataOptions: ['EEG', 'Temperature', 'Signal Strength'],
      animalOptions: ['AM304', 'AM305'],
      animal: null,
      startTime: '2018/11/1 00:00:00',
      endTime: '2018/11/1 00:00:00',
      columns: [
        { name: 'statistic', align: 'center', label: 'Statistic', field: 'Statistic' },
        { name: 'value', align: 'center', label: 'Value', field: 'Value' }
      ],
      statData: []
    }
  },
  methods: {
    log: function () {
      console.log(this.endTime)
    },
    sendFileRequest () {
      let reqUrl = null
      switch (this.dataType) {
        case 'EEG':
          reqUrl = 'http://192.168.1.194:8080/eeg'
          break
        case 'Temperature':
          reqUrl = 'http://192.168.1.194:8080/temp'
          break
        case 'Signal Strength':
          reqUrl = 'http://192.168.1.194:8080/ss'
          break
        default:
          return
      }
      const fileName = this.animal + ' ' + this.startTime.replace(/\//g, '-').replace(/:/g, '-') + ' ' + this.endTime.replace(/\//g, '-').replace(/:/g, '-') + ' ' + this.dataType + '.csv'
      axios({
        url: reqUrl,
        method: 'POST',
        responseType: 'blob',
        data: {
          animal: this.animal,
          start_time: this.startTime,
          end_time: this.endTime
        }
      })
        .then(response => {
          var fileURL = window.URL.createObjectURL(new Blob([response.data]))
          var fileLink = document.createElement('a')
          fileLink.href = fileURL
          fileLink.setAttribute('download', fileName)
          document.body.appendChild(fileLink)
          fileLink.click()
        }).catch(console.error)
    },
    getStatistics () {
      axios({
        url: 'http://192.168.1.194:8080/tempstats',
        method: 'POST',
        data: {
          animal: this.animal,
          start_time: this.startTime,
          end_time: this.endTime
        }
      })
        .then((response) => {
          console.log(this.statData)
          this.statData = response.data.data
          console.log(this.statData)
        })
    }
  }
}
</script>
