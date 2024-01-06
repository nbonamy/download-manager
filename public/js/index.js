
// init vue
var router = new VueRouter({
  mode: 'history',
  routes: []
});
var vm = new Vue({
  el: '#app',
  router,
  data: {
    isLoading: false,
    showFinalize: false,
    showAdd: false,
    configErrors: null,
    downloads: null,
    history: null,
    currentItem: null,
    url: null,
    title: null,
    destinations: null,
    subfolder: null,
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
        vm.subfolder = ''
      });
      vm.currentItem = item;
      vm.showFinalize = true;
    },
    doFinalize() {
      url = '/ws/finalize/' + vm.currentItem.id;
      url += '?title=' + encodeURIComponent(vm.title);
      url += '&dest=' + encodeURIComponent(vm.destination)
      url += '&subfolder=' + encodeURIComponent(vm.subfolder)
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
      axios.get('/ws/downloads').then(response => {
        vm.destinations = response.data.items
        vm.destination = vm.destinations[0].path
      });
      vm.showAdd = true;
      this.$nextTick(() => {
        //console.log(this.$refs);
        this.$refs.url.focus();
      });
    },
    doAdd() {
      if (vm.url.length > 0) {
        vm.showAdd = false
        this.download(vm.url, vm.destination);
        vm.url = null;
      }
    },
    download(url, dest) {
      axios.get('/ws/download?url=' + encodeURIComponent(url) + '&dest=' + dest).then(response => {
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
  },
  beforeMount() {
    axios.get('/ws/check').then(response => {
      if (response.data.status == 'ok') {
        this.refresh();
        setInterval(() => this.refreshStatus(), 1000);
      } else {
        vm.configErrors = response.data.errors;
      }
    })
  },
  mounted: function() {
    var self = this;
    q = this.$route.query;
    if (q.url != null) {
      this.isLoading = true;
      axios.get('/ws/info?url=' + encodeURIComponent(q.url)).then(response => {
        this.$buefy.dialog.confirm({
          title: 'Confirm download',
          message: '<p>Do you really want to download <b>' + response.data.title + '</b>?</p><p class="is-italic is-size-7"><br/>' + response.data.info.filename + '</p>',
          onConfirm: () => {
            self.download(q.url, '');
          }
        });
      }).finally(function (error) {
        self.isLoading = false;
      });
    }
  }
})
