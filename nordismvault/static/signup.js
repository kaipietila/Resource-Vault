
var signup = new Vue({
    delimiters: ["[[", "]]"],
    el: '#signup',
    data () {
        return {
            sign_up_needed: false,
            formdata:{ username: '', password: '' }
        }
    },
    methods: {
        addSignUpForm () {
            this.sign_up_needed = !this.sign_up_needed
        },
        signUpUser () {
            let data = this.formdata
            axios.post('api/contributor/', { data }
            )
            .then(res => {
                console.log('Signed up succesfully');
             })
             .catch(err => { 
                console.log('Error during sign up');
             })
        }
    }
})