// ask for the user
const request = new XMLHttpRequest()
const csrftoken = Cookies.get('csrftoken');
request.open('POST', "/get_user", true)
request.setRequestHeader("X-CSRFToken", csrftoken);
request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
request.onload = function () {
  const user = JSON.parse(request.responseText).user



  function Convo_bubble(props){
    if (props.user !== 'Customer Support'){

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
        messages: [{message: 'Hi, how can I help you today?', user:'Customer Support'}],
      }

    }

    addMessage(){
      const text = document.getElementById('message_input').value
      this.setState({
        messages: [...this.state.messages, {message: text, user: user}],
      })
      document.getElementById('message_input').value = ''
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
              <input id='message_input' type='text' />
              <button onClick={() => this.addMessage()} >Send</button>
            </div>
          </div>
        </div>
      )
    }
  }

  ReactDOM.render(
    <Chat_app />, document.querySelector("#root")
  )

}
request.send()
