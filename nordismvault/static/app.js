var resource_list = new Vue({
    delimiters: ["[[", "]]"],
    el: '#resource-list',
    data () {
        return {
            resources: null
        }
    },
    mounted () {
        var url = '/api/resource/';
        axios
            .get(url)
            .then(response => (this.resources = response.data))
    },
    filters: {
        clean_date (value) {
            if (value) {
                return moment(String(value)).format('MM/DD/YYYY hh:mm')
  }
      }
    },
})

var resource_form = new Vue({
    delimiters: ["[[", "]]"],
    el: '#resource-form',
    data: {
        file: ''
    },
    methods: {
        submitFile() {
            let formData = new FormData();
            formData.append('file', this.file);
            let filename = this.file.name;
            axios.post('api/resource/upload/',
              formData, {
                headers: {
                    'Content-type':'multipart/form-data',
                    'Content-Disposition': 'attachment; filename='+filename,
                    'filename': filename
                }
              }
            .catch(function () {
              console.log('Upload failed');
            }));
        },
        handleFileUpload() {
          this.file = this.$refs.file.files[0];
        }
    }
})