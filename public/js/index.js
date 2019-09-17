
// init vue
var vm = new Vue({
  el: '#app',
  data: {
    cfg_errors: null,
    downloads: null,
    history: null,
    showFinalize: false,
    currentItem: null,
    title: null,
    destinations: null,
    destination: null
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
      axios.get('/ws/title/' + item.id).then(response => {
        vm.title = response.data.title
      });
      axios.get('/ws/destinations').then(response => {
        vm.destinations = response.data.items
        vm.destination = vm.destinations[0]
      });
      vm.currentItem = item;
      vm.showFinalize = true;
    },
    doFinalize() {
      url = '/ws/finalize/' + vm.currentItem.id;
      url += '?title=' + encodeURIComponent(vm.title);
      url += '&dest=' + encodeURIComponent(vm.destination)
      axios.get(url).then(response => {
        vm.showFinalize = false;
        vm.refresh();
      });
    },
    purge(item) {
      axios.get('/ws/purge/' + item.id).then(response => {
        vm.refreshHistory();
      });
    },
    add() {
      var self = this;
      self.$buefy.dialog.prompt({
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
            }).catch(function (error) {
              self.$buefy.dialog.alert({
                title: 'Error',
                message: 'Download could not be started',
                type: 'is-danger',
                hasIcon: true,
                icon: 'alert-circle',
                iconPack: 'mdi'
              })
            });
          }
        }
      })
    }
  },
  beforeMount() {
    axios.get('/ws/check').then(response => {
      if (response.data.status == 'ok') {
        this.refresh();
        setInterval(() => this.refreshStatus(), 1000);
      } else {
        vm.cfg_errors = response.data.errors;
      }
    })
  }
})
