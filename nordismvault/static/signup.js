
var invite = new Vue({
    delimiters: ["[[", "]]"],
    el: '#invite',
    data () {
        return {
            invite_needed: false,
            email: ''
        }
    },
    methods: {
        addInviteForm () {
            this.invite_needed = !this.invite_needed
        },
        InviteRequest () {
            // posts to login/api/invitation
            axios.post('api/invitation/', {email: this.email}
            )
            .then(res => {
                console.log('Invitation requested succesfully');
             })
             .catch(err => { 
                console.log('Error during submission');
             })
        }
    }
})