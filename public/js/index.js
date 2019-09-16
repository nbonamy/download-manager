
// init vue
var vm = new Vue({
  el: '#app',
  data: {
    downloads: null,
    history: null
  },
  methods: {
    refresh() {
      this.refreshStatus();
      this.refreshHistory();
    },
    refreshStatus() {
      axios.get('/ws/status').then(response => {
        vm.downloads = response.data.items;
      });
    },
    refreshHistory() {
      axios.get('/ws/history').then(response => {
        vm.history = response.data.items;
      });
    },
    cancel(item) {
      this.$buefy.dialog.confirm({
        title: 'Cancel download',
        message: 'Are you sure you want to <b>cancel</b> this download? This action cannot be undone.',
        confirmText: 'Cancel download',
        cancelText: 'Keep it going',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => {
          axios.get('/ws/cancel/' + item.id).then(response => {
            vm.refresh();
          });
        }
      });
    },
    start(item) {
      axios.get('/ws/start/' + item.id).then(response => {
        vm.refreshStatus();
        setTimeout(vm.refreshHistory, 1000);
      });
    },
    finalize(item) {
      alert(item.id)
    },
    purge(item) {
      axios.get('/ws/purge/' + item.id).then(response => {
        vm.refreshHistory();
      });
    },
    add() {
      this.$buefy.dialog.prompt({
        title: 'Paste the URL to download',
        confirmText: 'Download',
        type: 'is-success',
        inputAttrs: {
          placeholder: 'https://uptobox.com/',
          length: 128
        },
        onConfirm: (value) => {
          if (value.length > 0) {
            axios.get('/ws/download?url=' + value).then(response => {
              vm.refreshStatus();
            });
          }
        }
      })
    }
  },
  beforeMount() {
    this.refresh();
    setInterval(() => this.refreshStatus(), 1000);
  }
})
