<template>
  <div v-if="timer" class="text-h6 text-center">
    {{ timeCalculated }}
  </div>
</template>

<script>
import { DateTime } from 'luxon'

export default {
  name: 'CountDownTimer',

  props: {
    endDate: {
      type: String,
      required: true
    }
  },

  data () {
    return {
      now: DateTime.local(),
      timer: null
    }
  },

  computed: {
    timeCalculated () {
      const endDateDateTimeObj = DateTime.fromISO(this.endDate)
      const theDiff = endDateDateTimeObj.diff(this.now, ['hours', 'minutes', 'seconds'])

      return `${theDiff.hours} h ${('0' + theDiff.minutes).slice(-2)} m ${('0' + Math.round(theDiff.seconds)).slice(-2)} s`
    }
  },

  watch: {
    endDate: {
      immediate: true,

      handler (endDateTimeStr) {
        const endDateTimeObj = DateTime.fromISO(endDateTimeStr)

        if (this.timer) {
          clearInterval(this.timer)
        }

        this.timer = setInterval(() => {
          this.now = DateTime.local()

          if (this.now > endDateTimeObj) {
            this.now = endDateTimeObj
            clearInterval(this.timer)
          }
        }, 1000)
      }
    }
  },

  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>