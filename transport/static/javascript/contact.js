// ask for the user
const request = new XMLHttpRequest()
const csrftoken = Cookies.get('csrftoken');
request.open('POST', "/get_user", true)
request.setRequestHeader("X-CSRFToken", csrftoken);
request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
request.onload = function () {
  const user = JSON.parse(request.responseText).user
  const room_name = 'lobby'
  // channels stuff
  const chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + room_name + '/');

  chatSocket.onclose = function(e) {
    console.error("Socket closed unexpectedly.", e)
  }



  function Convo_bubble(props){
    if (props.user === user){

      return(
        <div className='bubble_container'>
          <p className='bubble_info'> {props.user} </p>
          <div className='bubble'>{props.message}</div>
        </div>
      )

    }
    else {

      return (
        <div className='bubble_container_admin'>
          <p className='bubble_info'> {props.user} </p>
          <div className='bubble_admin'>{props.message}</div>
        </div>
      )

    }
  }


  class Chat_app extends React.Component {
    constructor(props) {
      super(props)
      this.state = {
        messages: [{message: 'Hi, how can I help you today?', user:'Support'}],
      }
      this.addMessage = this.addMessage.bind(this);
    }

    componentDidMount(){
      chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const sender = data['user']
        var message = data['message']
        console.log(sender)
        if (message !== ''){
          console.log('hello', this)
          this.setState({
            messages: [...this.state.messages, {message: message, user: sender}],
          })
          document.getElementById('message_input').value = ''
          }
      }
    }

    addMessage(){
      console.log('line 71')
      const text = document.getElementById('message_input').value
        if (text !== ''){
          chatSocket.send(JSON.stringify({
              'message': text,
              'user': user,
          }));
        }
      }

    checkEnter(e) {
      if (e.key === 'Enter'){
        this.addMessage()
      }
    }

    componentDidUpdate() {
      document.getElementById('scrollto').scrollIntoView()
    }
    render () {

      return (
        <div>
          <h1>Questions? A customer reppresentative will be happy to assist you</h1>
          <div className="chat_container">
            <div className="conversation_container">
              {this.state.messages.map(message => <div><Convo_bubble
              message={message.message} user={message.user} /><br /> </div>)
            }
            <div id='scrollto'></div>
            </div>
            <div className="Compose_message_container">
              <input  onKeyPress={() => this.checkEnter(event)} id='message_input' type='text' placeholder="Type your message here..."/>
              <button id="submit_message_button" onClick={() => this.addMessage()}><i className="fa fa-send"></i></button>

            </div>
          </div>
        </div>
      )
    }
  }


  ReactDOM.render(
    <Chat_app />, document.querySelector("#root")
  )
  // focus on the input bar
  document.querySelector("#message_input").focus()


}
request.send()
